"""Frame classes for SAR edge sensor nodes.

A frame is one message a sensor node sends: who sent it, its place in the
sequence, and the data. This module has:

    BaseEdgeFrame             the fields every sensor shares (D01.02)
    EnvironmentalEdgeFrame    the BME680 environmental node (D01.02.06)

To support another sensor, add a class that inherits from BaseEdgeFrame, set
its MODALITY, declare the fields that sensor adds, and write validate_profile().

This module uses only the Python standard library.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from numbers import Real
from typing import Any, ClassVar


class FrameError(ValueError):
    """A frame does not conform to the base contract or to its profile."""


def _is_number(value: Any) -> bool:
    return isinstance(value, Real) and not isinstance(value, bool)


def _is_whole_number(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


@dataclass(kw_only=True)
class BaseEdgeFrame(ABC):
    """Fields and rules shared by every sensor (D01.02 section 4)."""

    MODALITY: ClassVar[str] = ""

    # Required base fields. `modality` is fixed per class by MODALITY.
    source_node_id: str
    source_id: str
    frame_index: int
    payload: dict[str, Any]

    # Optional base fields.
    source_capture_time: str | None = None   # ISO 8601 UTC, only if the node has a real clock
    source_frame_id: str | None = None
    source_latency_ms: float | None = None

    def __post_init__(self) -> None:
        """Runs automatically when a frame is created, and checks it."""
        if not self.source_node_id or not self.source_id:
            raise FrameError("source_node_id and source_id must not be empty")
        if not _is_whole_number(self.frame_index) or self.frame_index < 0:
            raise FrameError(f"frame_index must be a non-negative integer, got {self.frame_index!r}")
        if not isinstance(self.payload, dict):
            raise FrameError("payload must be an object")
        if self.source_latency_ms is not None and (
            not _is_number(self.source_latency_ms) or self.source_latency_ms < 0
        ):
            raise FrameError(f"source_latency_ms must be a non-negative number, got {self.source_latency_ms!r}")

        # A payload key may not reuse the name of a frame field.
        frame_field_names = {f.name for f in fields(self)} | {"modality"}
        clashes = sorted((frame_field_names - {"payload"}).intersection(self.payload))
        if clashes:
            raise FrameError(f"payload reuses frame field name(s): {', '.join(clashes)}")

        self.validate_profile()

    @abstractmethod
    def validate_profile(self) -> None:
        """Check the fields and payload contents this sensor's profile requires."""

    @classmethod
    def from_wire(cls, wire: Any) -> "BaseEdgeFrame":
        """Build a frame from one decoded JSON object sent by a node."""
        if not isinstance(wire, dict):
            raise FrameError("frame must be a JSON object")
        if wire.get("modality") != cls.MODALITY:
            raise FrameError(f"modality is {wire.get('modality')!r}, expected {cls.MODALITY!r}")

        values = {name: value for name, value in wire.items() if name != "modality"}
        unknown = sorted(set(values) - {f.name for f in fields(cls)})
        if unknown:
            raise FrameError(f"unknown field(s) for {cls.MODALITY} frame: {', '.join(unknown)}")

        try:
            return cls(**values)
        except TypeError as error:  # a required field is missing
            raise FrameError(str(error).replace(f"{cls.__name__}.__init__() ", "")) from None

    def to_dict(self) -> dict[str, Any]:
        """The frame as a plain dictionary, ready to save as JSON."""
        record: dict[str, Any] = {"modality": self.MODALITY}
        for f in fields(self):
            value = getattr(self, f.name)
            if value is not None and f.name != "payload":
                record[f.name] = value
        record["payload"] = dict(self.payload)   # payload last, so records read top-down
        return record


@dataclass(kw_only=True)
class EnvironmentalEdgeFrame(BaseEdgeFrame):
    """Event-based environmental frame (D01.02.06).

    One frame is one event from the node, carrying the full reading set taken at
    that moment. The measurements are in `payload`; everything describing the
    sensor and why the event was sent is a frame field.
    """

    MODALITY: ClassVar[str] = "environmental"

    EVENT_TYPES: ClassVar[frozenset[str]] = frozenset({"startup", "change", "heartbeat"})
    NUMERIC_MEASUREMENTS: ClassVar[tuple[str, ...]] = (
        "temperature_c",
        "relative_humidity_pct",
        "pressure_hpa",
        "gas_resistance_ohm",
    )
    BOOLEAN_MEASUREMENTS: ClassVar[tuple[str, ...]] = ("gas_heater_stable",)

    # Required profile fields.
    sensor_model: str
    event_type: str
    sample_interval_ms: int
    heartbeat_interval_ms: int
    threshold_temperature_c: float
    threshold_relative_humidity_pct: float
    threshold_pressure_hpa: float
    threshold_gas_resistance_ohm: float

    # Optional profile fields.
    source_session_id: str | None = None
    source_uptime_ms: int | None = None
    firmware_version: str | None = None
    sensor_config: dict[str, Any] | None = None

    def validate_profile(self) -> None:
        if not self.sensor_model:
            raise FrameError("sensor_model must not be empty")
        if self.event_type not in self.EVENT_TYPES:
            raise FrameError(f"event_type is {self.event_type!r}, expected one of {sorted(self.EVENT_TYPES)}")

        for name in ("sample_interval_ms", "heartbeat_interval_ms"):
            value = getattr(self, name)
            if not _is_whole_number(value) or value <= 0:
                raise FrameError(f"{name} must be a positive integer, got {value!r}")

        for name in (
            "threshold_temperature_c",
            "threshold_relative_humidity_pct",
            "threshold_pressure_hpa",
            "threshold_gas_resistance_ohm",
        ):
            value = getattr(self, name)
            if not _is_number(value) or value <= 0:
                raise FrameError(f"{name} must be a positive number, got {value!r}")

        missing = [
            name for name in self.NUMERIC_MEASUREMENTS + self.BOOLEAN_MEASUREMENTS if name not in self.payload
        ]
        if missing:
            raise FrameError(f"payload is missing measurement(s): {', '.join(missing)}")
        for name in self.NUMERIC_MEASUREMENTS:
            if not _is_number(self.payload[name]):
                raise FrameError(f"payload {name} must be a number, got {self.payload[name]!r}")
        for name in self.BOOLEAN_MEASUREMENTS:
            if not isinstance(self.payload[name], bool):
                raise FrameError(f"payload {name} must be true or false, got {self.payload[name]!r}")

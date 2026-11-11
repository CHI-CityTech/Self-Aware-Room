"""SAR environmental node receiver.

Reads the frames sent by the ESP32 + BME680 environmental node over USB, checks
each one against the Environmental Streaming Profile (D01.02.06), stamps it with
the time it arrived, and saves it to a file on this computer.

Run it from anywhere (needs: pip install pyserial):

    python env_node_receiver.py --port COM11                    (Windows)
    python3 env_node_receiver.py --port /dev/cu.usbserial-0001  (Mac)

Frames are appended to data/env_node_frames.jsonl next to this script, one JSON
object per line. Stop with Ctrl+C.

To replay a saved capture instead of reading the node:

    python env_node_receiver.py --file capture.txt

frames.py must be in the same folder as this script.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterator

from frames import EnvironmentalEdgeFrame, FrameError

DEFAULT_OUTPUT = Path(__file__).resolve().parent / "data" / "env_node_frames.jsonl"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


# ------------------------------------------------------------ line sources


def lines_from_serial(port: str, baud: int) -> Iterator[tuple[datetime, str]]:
    """Yield (receipt_time, text) for each line arriving on a serial port."""
    try:
        import serial  # pyserial; imported here so file replay works without it
    except ImportError:
        raise SystemExit("Reading a serial port needs pyserial: pip install pyserial")

    with serial.Serial(port, baud, timeout=1) as connection:
        while True:
            raw = connection.readline()
            if raw:
                yield utc_now(), raw.decode("utf-8", errors="replace")


def lines_from_file(path: str) -> Iterator[tuple[datetime, str]]:
    """Yield (receipt_time, text) for each line of a file, or of stdin for '-'."""
    stream = sys.stdin if path == "-" else open(path, encoding="utf-8", errors="replace")
    try:
        for text in stream:
            yield utc_now(), text
    finally:
        if stream is not sys.stdin:
            stream.close()


# ---------------------------------------------------------- frame ordering


class OrderTracker:
    """Reports frame_index problems, allowing for node restarts."""

    def __init__(self) -> None:
        self._last: dict[tuple[str, str], tuple[str | None, int]] = {}

    def check(self, frame: EnvironmentalEdgeFrame) -> str | None:
        key = (frame.source_node_id, frame.source_id)
        session = frame.source_session_id
        previous = self._last.get(key)
        self._last[key] = (session, frame.frame_index)

        if previous is None:
            return None
        last_session, last_index = previous
        if session != last_session:
            return f"new session {session} (node restarted)"
        if frame.frame_index <= last_index:
            return f"frame_index {frame.frame_index} arrived after {last_index}"
        if frame.frame_index > last_index + 1:
            return f"{frame.frame_index - last_index - 1} frame(s) missing before {frame.frame_index}"
        return None


# ------------------------------------------------------------ record + log


def record_for(frame: EnvironmentalEdgeFrame, receipt_time: datetime) -> dict:
    """The frame plus the timestamps added on this computer."""
    # The node has no real clock, so the time the reading was taken is estimated:
    # the time the frame arrived minus how long the node says the reading took.
    latency_ms = frame.source_latency_ms or 0.0
    capture_time = receipt_time - timedelta(milliseconds=latency_ms)

    record = {
        "receipt_time": receipt_time.isoformat(),
        "estimated_capture_time": capture_time.isoformat(),
    }
    record.update(frame.to_dict())
    return record


def describe(frame: EnvironmentalEdgeFrame, receipt_time: datetime) -> str:
    """One console line summarizing a received frame."""
    p = frame.payload
    gas = f"{p['gas_resistance_ohm']:.0f} ohm" if p["gas_heater_stable"] else "gas not stable"
    local_time = receipt_time.astimezone().strftime("%H:%M:%S")
    return (
        f"{local_time}  #{frame.frame_index:<4} {frame.event_type:<9} "
        f"{p['temperature_c']:.2f} C  {p['relative_humidity_pct']:.2f} %RH  "
        f"{p['pressure_hpa']:.2f} hPa  {gas}"
    )


# --------------------------------------------------------------------- main


def run(lines: Iterator[tuple[datetime, str]], output_path: Path, counts: dict[str, int]) -> None:
    """Check, timestamp, and save every frame from a line source."""
    order = OrderTracker()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("a", encoding="utf-8") as output:
        for receipt_time, text in lines:
            text = text.strip()
            if not text:
                continue
            if text.startswith("#"):          # status message from the node, not a frame
                print(f"[node] {text[1:].strip()}")
                continue
            if not text.startswith("{"):      # boot noise from the USB serial bridge
                counts["skipped"] += 1
                continue

            try:
                frame = EnvironmentalEdgeFrame.from_wire(json.loads(text))
            except (json.JSONDecodeError, FrameError) as error:
                counts["rejected"] += 1
                print(f"[rejected] {error}: {text[:80]}", file=sys.stderr)
                continue

            warning = order.check(frame)
            if warning:
                print(f"[order] {warning}", file=sys.stderr)

            output.write(json.dumps(record_for(frame, receipt_time)) + "\n")
            output.flush()
            counts["saved"] += 1
            print(describe(frame, receipt_time))


def main() -> None:
    parser = argparse.ArgumentParser(description="Receive and save SAR environmental node frames.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--port", help="serial port of the node, e.g. COM11 or /dev/cu.usbserial-0001")
    source.add_argument("--file", help="replay frames from a text file, or '-' for stdin")
    parser.add_argument("--baud", type=int, default=115200, help="serial baud rate (default 115200)")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT, help="file to append frames to")
    args = parser.parse_args()

    lines = lines_from_serial(args.port, args.baud) if args.port else lines_from_file(args.file)
    counts = {"saved": 0, "rejected": 0, "skipped": 0}
    print(f"Saving frames to {args.out}")
    try:
        run(lines, args.out, counts)
    except KeyboardInterrupt:
        print("\nStopped.")
    print(f"Saved {counts['saved']}, rejected {counts['rejected']}, skipped {counts['skipped']}.")


if __name__ == "__main__":
    main()

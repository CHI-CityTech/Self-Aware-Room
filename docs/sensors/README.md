# Sensors Documentation Track

This track contains documentation for sensor taxonomy, interface contracts, placement, and validation procedures.

## 1. Scope

This folder is documentation-only and should not store runtime configs, code, or raw data artifacts.

In scope:

1. Sensor inventory documentation and source-to-contract mapping.
2. Modality taxonomy and naming conventions.
3. Placement and calibration documentation.
4. Validation and acceptance test procedures.

Out of scope:

1. Runtime configuration files.
2. Source code and pipeline implementation logic.
3. Raw captures and binary telemetry dumps.

## 2. Authoritative Boundaries

This section clarifies where related artifacts should live.

1. Grant and procurement asset records: operations/.
2. Runtime and implementation artifacts: src/ and system/.
3. Computational contracts and normative pipeline specs: docs/computational/.

Inventory source priority:

1. The OAA Google Sheet is the live source of truth.
2. PDF inventory files under operations/ are point-in-time snapshots for repository traceability.

## 3. Primary Documents

1. Sensor inventory and computational mapping: [SAR Sensor Inventory and Computational Mapping](SAR_Sensor_Inventory_and_Computational_Mapping_V1_2026-08-03.md)

## 4. Integration References

1. Shared streaming contract: [D01.02 Shared Streaming Contract](../computational/D01.02_SAR_Shared_Streaming_Contract_V1_2026-07-29.md)
2. Audio streaming profile: [D01.02.01 Audio Streaming Profile](../computational/D01.02.01_SAR_Audio_Streaming_Profile_V1_2026-07-29.md)
3. Class and object model: [D02.01 Computational Class and Object Model](../computational/D02.01_SAR_Computational_Class_and_Object_Model_V1_2026-07-27.md)
4. Task and milestone map: [D04.03 Task, Dependency, Test, and Milestone Map](../computational/D04.03_SAR_Computational_Task_Dependency_Test_and_Milestone_Map_V1_2026-08-03.md)

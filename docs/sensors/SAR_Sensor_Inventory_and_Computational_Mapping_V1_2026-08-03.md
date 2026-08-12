# SAR Sensor Inventory and Computational Mapping

Document Class: Sensor Documentation and Contract Mapping  
Project: Self-Aware-Room (SAR)  
Status: Version 1 draft  
Date: 2026-08-03

## 1. Purpose

This document maps physical and logical sensor assets to SAR computational contract fields so sensor onboarding can remain generalized and auditable.

## 2. Source Inputs

This section identifies source artifacts used to populate this mapping.

1. OAA grant inventory canonical source: https://docs.google.com/spreadsheets/d/1Y4ND_M3c1ZKv1S4Bs0K1mHY8vtbBrymCsntErgicCTM/edit?usp=sharing
2. OAA inventory repository snapshot: ../../operations/OAA AI Inventory.pdf
3. Shared streaming contract: ../computational/D01.02_SAR_Shared_Streaming_Contract_V1_2026-07-29.md
4. Audio profile contract: ../computational/D01.02.01_SAR_Audio_Streaming_Profile_V1_2026-07-29.md
5. Identity boundary policy: ../computational/D01.04_SAR_Run_and_Session_Identity_and_Boundary_Policy_V1_2026-07-28.md

### 2.1 Source Priority Policy

When inventory values conflict between sources:

1. The Google Sheet is authoritative.
2. The PDF snapshot is an auditable point-in-time export for repository traceability.

## 3. Mapping Policy

This section defines the required separation between asset inventory and computational contract identifiers.

1. Asset inventory identifiers remain authoritative in operations artifacts.
2. Computational identifiers are assigned for pipeline use and MUST be stable.
3. One inventory line MAY map to one or many computational sources depending on interface topology.
4. All synthesized or backfilled ingest fields MUST be traceable in provenance metadata.

## 4. Canonical Field Crosswalk

This section defines how inventory and runtime fields align.

| Inventory Domain | Field | Computational Domain | Field | Notes |
| --- | --- | --- | --- | --- |
| Asset registry | asset_id | Ingest source identity | source_id | Stable per logical source stream. |
| Asset registry | location | Spatial metadata | spatial_coordinates or room zone | Use room coordinate conventions when available. |
| Asset registry | device_type | Modality declaration | modality | Must match D01.02 profile taxonomy. |
| Asset registry | interface path | Ingest topology | source_node_id and ingest_node_id | Capture L0 producer and L1 ingest boundary. |
| Asset registry | vendor model | Payload interpretation | encoding, sample_rate_hz, channel_count, profile fields | Required field set depends on modality profile. |

## 5. Sensor Registry Table

This table should be maintained as the documentation-level registry for computational onboarding.

| Sensor UID | Asset ID | Sensor Label | Modality | Source Node ID | Source ID | Ingest Node ID | Profile Doc | Contract Status | Validation Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | audio | TBD | TBD | TBD | D01.02.01 | not_started | not_started | Seed from OAA inventory PDF. |

## 6. Validation Readiness Checklist

This checklist defines documentation-level readiness before opening implementation issues.

1. Sensor has a stable Sensor UID and mapped source_id.
2. Modality profile document is identified and approved.
3. Required contract fields for the modality are listed and testable.
4. Ingest topology from source_node_id to ingest_node_id is documented.
5. Planned test fixtures are defined for contract and integration validation.

## 7. Change Management

This section defines maintenance behavior for this document.

1. Add new sensors as new rows; do not reuse Sensor UID values.
2. Keep historical changes in git history rather than deleting prior context.
3. Update validation status when tests are opened, running, blocked, or complete.
4. Keep this mapping synchronized with computational milestone execution in D04.03.

# SAR Sensor UID Definition Set Proposal

Document Class: Sensor Identity Design Proposal

Project: Self-Aware-Room (SAR)

Status: Proposed for review; not an approved runtime contract

Version: 2

Date: 2026-10-31

Prepared for: Kazi Tamim Nomany, with AI assistance

Review authority: Professor David B. Smith

Issue: [SAR #22](https://github.com/CHI-CityTech/Self-Aware-Room/issues/22)

Supersedes for review: [Version 1](./PROPOSAL_FOR_REVIEW.md)

## 1. Purpose and decision requested

Issue 22 requests a meaningful UID definition set for the [sensor inventory mapping](https://github.com/CHI-CityTech/Self-Aware-Room/blob/8c99abecd723a39370455ba9e27adca2cea872b1/docs/sensors/SAR_Sensor_Inventory_and_Computational_Mapping_V1_2026-08-03.md). That mapping requires stable Sensor UIDs but does not define their scope, assignment, or lifecycle.

This version narrows the approval request to sensor identity and lifecycle. It recommends a permanent, opaque UUID-based `sensor_uid` for each tracked physical sensing unit, while keeping procurement assets, logical streams, producers, deployments, and observations distinct. It defines relationships and lifecycle behavior without proposing changes to the runtime envelope.

**Decision requested:** approve or revise the physical-unit boundary, Sensor UID format, relationship to stream IDs, and lifecycle rules in sections 3–7. Producer epochs, frame deduplication, provenance schema, and registry tooling are explicitly deferred for separate contract review.

This is a documentation proposal. Examples are fictional, and no inventory IDs are allocated or verified. Existing Doc-IDs, runtime schemas, identifiers, and task statuses remain unchanged until separately approved.

## 2. Version 2 changes and rationale

| Change from Version 1 | Rationale |
| --- | --- |
| Limits the decision scope to sensor identity and lifecycle; moves frame keys, epochs, and provenance extensions to deferred work. | Those changes affect D01.02 and runtime behavior, so combining them with a UID decision increases review scope and risks implying an unapproved contract change. |
| Defines `source_id` as a stream identity bound to a physical sensor and measurement/channel, with a separate optional role alias for continuity across replacements. | The existing mapping calls `source_id` stable per logical stream. Explicit semantics avoid uncertainty about whether a replacement retains or changes the ID. |
| Adds a physical-duplicate review procedure for devices without unique serial numbers. | UUID uniqueness checks detect duplicate values, not duplicate registration of the same physical unit. |
| Defers short human-readable tags from the core proposal. | A sequential tag requires a coordinated register. A pilot can establish whether the operational benefit justifies that extra mechanism. |
| Makes a pilot and explicit approval gates precede registry population or implementation. | Prevents a proposal example or draft policy from being mistaken for validated inventory or an active runtime contract. |

## 3. Evidence and design choices

### 3.1 Standards context

| Reference | Relevant evidence | SAR design inference |
| --- | --- | --- |
| [RFC 9562](https://www.rfc-editor.org/rfc/rfc9562.html), sections 5.4, 5.7, 6.9, and 6.12 | UUIDv4 uses random values; UUIDv7 includes a timestamp; UUIDs should generally be treated as opaque identifiers. | Use UUIDv4 for permanent sensor registrations. Do not encode room, modality, or lifecycle meaning in the ID. This is a SAR policy choice, not a standards requirement. |
| [W3C/OGC SSN and SOSA](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/), sections 4.3 and 4.9 | The model distinguishes sensors, observations, platforms, and deployments. | Keep physical sensing-unit identity distinct from observation and deployment identity. This proposal uses a narrower physical scope than SOSA's general Sensor concept. |
| [W3C PROV-DM](https://www.w3.org/TR/2013/REC-prov-dm-20130430/), sections 2.1 and 5.2 | Provenance describes entities, activities, responsibility, and derivation. | Preserve assignment and change history. This proposal does not claim PROV conformance or define a provenance schema. |

These references support the distinctions, but do not prescribe SAR prefixes, component boundaries, source-ID semantics, or replacement rules. Those are design decisions proposed here.

### 3.2 Alternatives considered

| Candidate | Benefit | Limitation | Recommendation |
| --- | --- | --- | --- |
| Room/type/sequence, e.g. `N928-MIC-01` | Easy to recognize | Location or type can change | Use only as a mutable label, never as the permanent UID |
| Sequential machine ID, e.g. `SAR-SEN-000001` | Short and label-friendly | Requires one coordinated allocator | Defer; test operational need in pilot |
| Vendor serial, MAC, IP, or USB path | May already be available | May be missing, shared, changeable, or tied to an interface rather than the sensing unit | Store as evidence/lookup metadata, not as the Sensor UID |
| UUIDv4 with a sensor prefix | Opaque, globally unique in practice, and can be generated without a central counter | Long for people to read; does not detect duplicate physical registration | Recommended, with registry duplicate review |
| UUIDv7 | Time-sortable | Creation-time ordering is not required for permanent sensor identity | Not recommended for this purpose; retain any separately approved runtime UUID policy |
| UUIDv5 from a name | Deterministic | Depends on stable, correctly normalized input and namespace | Do not use for ordinary registrations; consider only through a separately reviewed legacy migration |

## 4. Identity model and relationships

The following terms are proposed for approval. They describe distinct entities; one identifier must not be substituted for another.

| Identifier or term | Identifies | Relationship and continuity |
| --- | --- | --- |
| `asset_id` | Procurement/operations inventory line | Preserve the authoritative OAA value. One asset may contain multiple sensing units. Missing inventory evidence remains unresolved; never invent an asset ID. |
| `sensor_uid` | One tracked physical sensing unit | Assigned once at approved registration; retained through restart, relocation, and recalibration. Replacement of the tracked unit creates a new UID. |
| `source_id` | One logical output stream with a defined observed property and channel, bound to one physical sensor during an effective interval | Separate streams on one sensor have separate IDs. Replacing the physical sensor creates new source IDs. Existing IDs are preserved during migration; see section 5. |
| `source_node_id` | A logical producer that emits frames | Identifies producer configuration/role, not the sensor or network address. Producer identity policy remains subject to D01.02 review. |
| `ingest_node_id` | A receiving SAR ingest service | Identifies the ingest boundary, not the source or physical sensor. |
| `deployment` | A time-bounded placement and connection of a sensor/stream | Changes when placement or relevant source assignment changes. It is history, not a permanent sensor identity. |
| `observation` / `object_id` | A canonical SAR data object | Assigned according to the existing runtime contract. It is not a Sensor UID or source ID. |
| `session_id` / `run_id` | Operating context and bounded processing window | Continue to follow D01.04. Multiple sensors may contribute to a run. |
| `role_alias` (optional, deferred) | A continuing operational role, such as “east-wall temperature” | If needed, resolve the role to effective-dated sensor/stream assignments. Do not let a role alias replace a physical UID or source ID. |

### 4.1 Physical sensing-unit boundary

Define a sensing unit as the physical component SAR intends to track and service as one sensing instance. Record the selected `component_boundary` in the registration when needed to disambiguate a product assembly.

1. A standalone microphone is one sensing unit.
2. A package containing separately tracked camera and microphone components has two Sensor UIDs, potentially under one asset.
3. An inseparable temperature/humidity module tracked and serviced as one unit has one Sensor UID and two source IDs, one per measured property.
4. A board with independently replaceable sensing modules has a UID for each tracked module. The board's producer is a separate identity.
5. An audio interface channel is a connection, not a microphone. Changing the attached microphone requires review of the affected sensor-to-stream mapping.
6. A simulated or derived software source has a source identity and declared source kind, but no fabricated physical Sensor UID or procurement asset. Derived-object lineage belongs to the applicable provenance contract.

If physical boundaries cannot be established confidently, do not register or activate the mapping. Quarantine it for steward review rather than silently combining components.

### 4.2 Relationship cardinalities

The recommended relationship model is:

- One asset may contain zero, one, or many tracked sensors.
- One sensor may provide zero, one, or many source streams.
- A source stream has one physical-sensor association at a time, or no physical association when it is a declared software-only source.
- Associations are effective-dated so historical assignments remain queryable.
- A producer may carry streams from one or more sensors, and an ingest service may receive from multiple producers. The identity model does not require one-to-one topology.

These are registry relationships, not new required fields in the current edge-frame envelope.

## 5. Proposed identifier and source-ID policy

### 5.1 Sensor UID format

New sensor registrations use:

```text
sar-sensor-<lowercase UUIDv4>
```

Example: `sar-sensor-8fae1a3c-572b-4b2d-8f14-3dbbdcb78b5e`.

Validate the complete prefix, UUID syntax, UUID version 4, and RFC variant. Normalize case before comparison; reject whitespace, truncation, or malformed values. Generate UUIDs with a maintained library backed by the operating system's secure random source. Check full-value uniqueness before registration. A UUID makes accidental collision extremely unlikely; it does not replace physical-duplicate review or reference validation.

Do not encode room, model, owner, modality, or calibration state in the UID. Never shorten the stored UID. Human-readable labels may change and are not join keys.

### 5.2 Source ID semantics and migration

For **new registrations**, define `source_id` as the identity of a particular logical stream bound to a physical sensing unit and a defined observed property/channel. Under this definition:

- Two measured properties from one unit have different source IDs.
- A physical replacement creates new source IDs, even when the replacement model and measurement are the same.
- Moving or reconnecting the same physical unit does not by itself change its source IDs.
- Changing the meaning of a stream closes the old association and creates a new source ID.
- A stable function across hardware replacements may use a separate role alias, if later approved.

This makes hardware lineage explicit and avoids changing the meaning of an existing source ID in place. It also exposes a required reconciliation: the current [sensor mapping](../../../sensors/SAR_Sensor_Inventory_and_Computational_Mapping_V1_2026-08-03.md) describes `source_id` as “stable per logical source stream.” Before adoption, the mapping owner must update that wording or explicitly choose a different source-ID scope. Do not silently reinterpret, rename, or regenerate existing source IDs. Migrate them only through a reviewed mapping with aliases and historical references preserved.

### 5.3 Short tags

Do not make `sensor_tag` required in the initial policy or registry. If a pilot shows that long UUIDs are impractical on equipment labels, propose a separate optional tag such as `SAR-SEN-000001`, allocated by one approved register and never reused. The tag must remain an alias, not a primary key.

**Rationale:** deferral keeps the identity decision independent of a numbering service and avoids operating two mandatory identity systems before there is evidence that both are needed.

## 6. Assignment, duplicate review, and lifecycle

### 6.1 Proposed assignment procedure

1. Check the authoritative OAA Google Sheet for the inventory fact. Record the source and verification date; if unavailable, mark the asset reference unresolved rather than filling it by assumption.
2. Identify the physical boundary and collect available evidence: asset reference, manufacturer/model, serial or part information, physical label, interface context, and operator observations. No single field is assumed to be globally unique.
3. Search active and retired registrations for a likely match. Compare the combined evidence and effective history, not only the proposed UUID.
4. If the evidence indicates the unit is already registered, recover its UID. If the evidence is insufficient or conflicting, quarantine the request for steward review; do not mint a second UID merely because a local configuration or label is missing.
5. Create a UUIDv4 candidate and check the full UID against active and retired entries. Register each stream separately with its measurement/channel meaning and applicable profile reference.
6. Record requester, approver, timestamps, evidence, reason, and a change/issue reference. Activate only after identity review and any separately required contract/profile validation.
7. Preserve corrections, aliases, and retired records. Never reuse a retired UID or rewrite historical raw records to make a new registration appear continuous.

The registry steward role is recommended but not presumed to be appointed. The project owner should identify an accountable steward before operational registration begins.

**Rationale:** UUID collision checking protects identifier uniqueness; evidence review protects physical identity uniqueness. The distinction is essential for devices without serial numbers or with ambiguous boundaries.

### 6.2 Registry minimum and status

The documentation-level mapping should record at least:

- `sensor_uid`, physical-boundary description, and human-readable label;
- `asset_id` plus inventory verification state/reference, when applicable;
- one row per source stream, with `source_id`, observed property, channel, and physical association;
- relevant producer and ingest-node references;
- effective start/end and deployment reference when placement or assignment changes;
- lifecycle status, requester/approver, change reference, and policy version.

Do not duplicate the procurement inventory. Keep calibration details, connection parameters, and detailed provenance in their authoritative records; link them where necessary rather than expanding this UID proposal into a complete sensor-management system.

Keep lifecycle status separate from contract and validation status. Suggested lifecycle values are `proposed`, `active`, `retired`, and `quarantined`. Retirement does not invalidate historical data.

### 6.3 Lifecycle rules

| Event | Sensor UID | Source ID | Required action |
| --- | --- | --- | --- |
| Restart, reconnect, or network address change; same physical unit and stream meaning | Keep | Keep | Verify identity where necessary; update connection/deployment history. Frame-counter behavior is deferred to contract review. |
| Move the same unit | Keep | Keep | Close the prior deployment interval and record the new placement. |
| Move the same unit to another producer | Keep | Keep | Update producer assignment history. Any sequence/epoch handling is deferred. |
| Replace the physical sensing unit with the same model | New | New | Retire the old association and record a replacement relationship; asset treatment follows operations policy. |
| Replace one sensing module on a retained board | New for the replaced module | New for its streams | Preserve unaffected module identities and record the component change. |
| Recalibrate the same unit | Keep | Keep | Reference the new calibration record and its validity; calibration does not alter identity. |
| Firmware or sample-rate change, same property/channel and same physical unit | Keep | Keep | Update the relevant configuration/profile record and revalidate compatibility as required. |
| Add a property/channel | Keep | New for the added stream | Register its meaning and profile; retain existing stream identities. |
| Change a stream's observed meaning | Keep if physical unit is unchanged | New | End the prior association and register the new stream meaning. |
| Lose label or local registry cache | Recover or quarantine | Recover or quarantine | Do not infer identity from port, address, model, or location alone. |
| Retire or correct a duplicate registration | Never reuse | Preserve/alias through reviewed correction | Keep the audit trail and historical references. |

## 7. Compatibility and deferred contract work

This proposal does not change the D01.02 base envelope, its required fields, source frame identity, timing policy, or provenance schema. In particular, it does not add `producer_epoch_id` or prescribe a canonical frame key.

The current [D01.02 contract](/Users/davidsmith/Documents/GitHub/Self-Aware-Room/docs/computational/D01.02_SAR_Shared_Streaming_Contract_V1_2026-07-29.md) requires `source_node_id`, `source_id`, `modality`, `frame_index`, and `payload`; native frame IDs and timing fields are optional. The current [edge adapter](/Users/davidsmith/Documents/GitHub/Self-Aware-Room/src/sar_core/contracts/edge_ingress.py) generates a fallback frame value from node ID and frame index and stores it in `source_native_id`. That implementation and the contract's generated-field provenance requirements warrant separate review, but are not changed by a sensor UID decision.

Deferred questions for a separate D01.02/T02/T03/T06 review:

1. What persistent state or allocation rule gives each producer sequence a restart-safe epoch, including crash recovery and cloned configurations?
2. Should duplicate detection use `(source_id, producer_epoch_id, frame_index)`, a native frame ID with a documented scope, or both? How should replay be represented?
3. Which fields and transport location distinguish source-native, generated, and estimated values while preserving compatibility?
4. How should the existing `source_id` definition and inventory crosswalk be reconciled with the physical-stream scope recommended here?

**Rationale:** epochs, deduplication, and provenance affect producers, ingest, schemas, and historical data. They need a coordinated contract decision and focused acceptance tests; placing them in this UID approval would create hidden runtime scope.

## 8. Illustrative example

All values are fictional. The asset is unverified, and this example is a registry illustration—not a runtime configuration, actual inventory record, or approved wire schema.

One inseparable temperature/humidity module has one Sensor UID and two stream mappings:

```json
{
  "example_only": true,
  "sensor_uid": "sar-sensor-8fae1a3c-572b-4b2d-8f14-3dbbdcb78b5e",
  "sensor_label": "Example temperature/humidity module",
  "asset_id": null,
  "inventory_verification": "unverified",
  "component_boundary": "one inseparable temperature/humidity module",
  "lifecycle_status": "proposed",
  "streams": [
    {
      "source_id": "temperature-source-id-placeholder",
      "observed_property": "temperature",
      "channel": "temperature",
      "effective_from": "2026-10-31T00:00:00Z",
      "profile_doc": null
    },
    {
      "source_id": "humidity-source-id-placeholder",
      "observed_property": "relative_humidity",
      "channel": "humidity",
      "effective_from": "2026-10-31T00:00:00Z",
      "profile_doc": null
    }
  ]
}
```

The source ID strings are placeholders, not proposed IDs to copy. Null profiles mean these example streams are not approved for contract activation.

## 9. Acceptance cases for implementation

These are proposed pass/fail cases, not tests executed against an implemented UID system.

| Case | Input or event | Expected result |
| --- | --- | --- |
| UID-01 | Register the same physical unit twice with matching evidence | Recover the existing UID or block the duplicate request |
| UID-02 | Register a different unit with an already-used UID | Reject duplicate UID allocation |
| UID-03 | Register one inseparable multi-property module | One Sensor UID; a distinct source ID per property/channel |
| UID-04 | Replace a sensor with the same model | New Sensor UID and source IDs; preserve old history |
| UID-05 | Move or reconnect the same physical unit without changing stream meaning | Keep Sensor UID and source IDs; update effective deployment/connection history |
| UID-06 | Recalibrate the same physical unit | Keep identities; reference the new calibration record |
| UID-07 | Change the observed meaning of a stream | Close the old association and create a new source ID |
| UID-08 | Submit malformed, truncated, or whitespace-bearing Sensor UID | Reject before activation |
| UID-09 | Offer a retired UID for replacement hardware | Reject reassignment |
| UID-10 | Asset or physical identity is unverified or ambiguous | Keep proposed/quarantined; do not claim validated onboarding |
| UID-11 | Register a software-only source | Record source kind and source identity, without fabricated physical UID or asset |
| UID-12 | Two active sensors are mapped to the same source stream at overlapping times | Reject the conflicting mapping or require explicit reviewed policy |
| UID-13 | Use a role alias across physical replacement | Keep the alias separate from both sensors' permanent IDs and source IDs |

Frame restart, replay, and generated-provenance cases belong in the deferred contract work, not this UID acceptance set.

## 10. Approval and rollout

### 10.1 Decisions requested

| Decision | Recommended default |
| --- | --- |
| Physical scope | One tracked physical sensing unit with a recorded boundary where needed |
| Sensor UID | `sar-sensor-<UUIDv4>`; opaque, permanent, never reassigned |
| Stream semantics | `source_id` identifies a stream bound to a physical unit and observed property/channel; replacement hardware gets new stream IDs |
| Continuity across replacement | Optional role alias, only if a pilot demonstrates the need |
| Registry authority | Project owner appoints an accountable steward before operational registration |
| Short tag | Defer; reconsider after pilot |
| Existing IDs | Preserve; no silent renaming or reinterpretation |
| Frame epoch, deduplication, provenance | Defer to separate D01.02/T02/T03/T06 review |

### 10.2 Staged rollout

1. Review and approve the identity decisions above under Issue 22; record policy version and accountable steward.
2. Resolve the `source_id` wording conflict in the sensor mapping document before applying the proposed new-stream semantics. Preserve existing mappings and aliases.
3. Run a small documentation-only pilot with actual inventory evidence: include a multi-stream unit and, if available, a replacement or relocation history. Mark unknown facts unresolved rather than guessed.
4. Review the pilot for duplicate-identification evidence, operator burden, and whether a short tag or role alias is actually needed.
5. Only after policy approval, update the mapping document and define any registry/runtime implementation through the relevant tasks and contracts. Keep sensor identity changes separate from frame/provenance work.
6. Add and execute the acceptance cases before marking onboarding validated. Preserve historical identifiers and records.

Issue 22's research and definition-set work is ready for review in this version. Approval, inventory verification, registry population, contract changes, and runtime implementation are separate completion steps. No such completion is claimed here.

## 11. Repository references

1. [Sensor inventory and computational mapping](https://github.com/CHI-CityTech/Self-Aware-Room/blob/8c99abecd723a39370455ba9e27adca2cea872b1/docs/sensors/SAR_Sensor_Inventory_and_Computational_Mapping_V1_2026-08-03.md), especially sections 3–7.
2. [D01.02 shared streaming contract](https://github.com/CHI-CityTech/Self-Aware-Room/blob/8c99abecd723a39370455ba9e27adca2cea872b1/docs/computational/D01.02_SAR_Shared_Streaming_Contract_V1_2026-07-29.md), especially sections 4–5.
3. [D01.04 run/session policy](https://github.com/CHI-CityTech/Self-Aware-Room/blob/8c99abecd723a39370455ba9e27adca2cea872b1/docs/computational/D01.04_SAR_Run_and_Session_Identity_and_Boundary_Policy_V1_2026-07-28.md).
4. [D02.01 class/object model](https://github.com/CHI-CityTech/Self-Aware-Room/blob/8c99abecd723a39370455ba9e27adca2cea872b1/docs/computational/D02.01_SAR_Computational_Class_and_Object_Model_V1_2026-07-27.md); reconcile native-ID wording with D01.02 through separate contract review.
5. [D04.03 task map](https://github.com/CHI-CityTech/Self-Aware-Room/blob/8c99abecd723a39370455ba9e27adca2cea872b1/docs/computational/D04.03_SAR_Computational_Task_Dependency_Test_and_Milestone_Map_V1_2026-08-03.md), including T02, T03, T05, T06, and T17.
6. [Identity/provenance implementation](../../../../src/sar_core/contracts/identity.py), [edge adapter](../../../../src/sar_core/contracts/edge_ingress.py), and [L1 acquisition implementation](../../../../src/sar_core/stages/l1_acquisition.py).

External research references were consulted on October 28, 2026. No external inventory values or hardware measurements were verified for this proposal.

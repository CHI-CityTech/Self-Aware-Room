# Issue 22 Review Response and Computational Contract Crosswalk

Document Class: Research and Review Response

Project: Self-Aware-Room (SAR)

Status: Draft for review; does not approve or change a runtime contract

Version: 1

Date: 2026-10-31

Originating proposal: [Sensor UID Definition Set Proposal V1](./PROPOSAL_FOR_REVIEW.md)

Revised proposal: [Sensor UID Definition Set Proposal V2](./PROPOSAL_FOR_REVIEW_V2.md)

Related issues: [SAR #22](https://github.com/CHI-CityTech/Self-Aware-Room/issues/22), [SAR #23](https://github.com/CHI-CityTech/Self-Aware-Room/issues/23), [SAR #24](https://github.com/CHI-CityTech/Self-Aware-Room/issues/24)

## 1. Purpose and status

This note responds to the Issue 22 review discussion and records a reusable crosswalk to SAR's existing computational architecture, data-object model, streaming contract, and run/session policy. It is intended to inform a later revision of the UID proposal and can be referenced from the computational document set.

Document lineage: V1 is the originating proposal; V2 is a subsequent revision; this crosswalk is supporting analysis. Both proposal versions remain proposals and are not approved runtime contracts.

The central reconciliation is:

- SAR already has cross-layer object identity, trace, provenance, processing-component metadata, and operational logging concepts.
- A **system component slot**—a stable reference to a system requirement that can be fulfilled by compatible components—is a new concept in the Issue 22 discussion. It is not defined by the Issue 22 Version 1 or Version 2 proposal, nor by the reviewed computational contracts.
- The new slot concept should complement existing contracts, not replace or duplicate them.
- Sensor and inventory references belong to registry/assignment relationships. They should not automatically become universal fields on every data object or frame.

This document analyzes the local repository baseline and the Issue 22, 23, and 24 discussion packages available on 2026-10-31. The additional component-slot wording was supplied during this review; it was not present in the GitHub Issue 22 comments retrieved for this note. The Issue 23 and Issue 24 packages are proposals and assessments, not approved specifications. Their synthetic tests do not establish production conformance.

## 2. Terms and identity areas

The [D00.02 computational glossary](../../../computational/D00.02_SAR_Computational_Glossary_V1_2026-07-29.md) remains authoritative for established pipeline terms such as *DataObject*, *Observation*, *Provenance*, and *Stage component*. The following additional terms clarify this crosswalk. The component-slot terms are proposed and are not existing SAR contract definitions.

| Term | Definition for this document |
|---|---|
| System requirement | A capability or function that the system design requires from one or more components. It may refer to a hardware or software capability. |
| Component slot | A proposed stable reference to a system requirement position that may be fulfilled by different compatible components over time. `component_slot_id` is a candidate identifier for that reference. |
| System component | An actual hardware or software element that provides a system capability. It is distinct from a data object that moves through the pipeline. |
| Slot assignment | The relationship recording which system component fulfills a component slot, and during what effective interval. It is not itself an ID unless independent references to assignment records prove necessary. |
| Data object | A SAR artifact exchanged between computational stages, such as an Observation, State, or Decision, with identity and lineage governed by the object model. |
| Runtime data traceability | The use of object/source identity, provenance, execution context, and O1 records to determine what data moved, how it was transformed, and which processing component handled it. |

### 2.1 System configuration identity

These references describe what the system requires and which actual component fulfills that requirement. They belong primarily to system configuration and registry relationships, not automatically in every frame or data object.

| Concept or reference | In plain language: what it tells us | What it helps SAR do | Status |
|---|---|---|---|
| `component_slot_id` | “Which system requirement position is this?” | Keep a requirement stable while compatible hardware or software fulfilling it changes. | New proposed concept; define its contract/profile reference and compatibility rules before adoption. |
| Slot assignment (relationship, not an ID) | “Which actual component fulfilled this slot, and when?” | Reconstruct effective system configuration and relate runtime evidence to the component used at that time. | Candidate effective-dated relationship with approval/evidence; no separate assignment ID assumed. |
| `sensor_uid` | “Which particular physical sensing unit is this?” | Distinguish a device from its system requirement, inventory record, stream, and observations. | Proposed registry identity; not a universal packet field by default. |
| Inventory reference (`asset_id` or authoritative field) | “Which inventory record describes this item or purchase?” | Look up procurement and operations facts in their authoritative source. | Reuse the inventory system's identifier and scope. Confirm whether it identifies an individual item or a multi-unit inventory line. |
| Software component name/version/configuration | “Which software component and build/configuration provides or performs this function?” | Support configuration records and trace transformations. | Existing telemetry/provenance concepts cover some of this; whether stable software slot/instance IDs are needed remains use-case dependent. |
| `sensor_tag` | “What short label can a person read on the equipment?” | Find equipment without handling a long UID. | Optional alias; defer unless a pilot establishes need. |
| Deployment or calibration reference | “Which independently tracked placement or calibration record applies?” | Resolve operational history when it must be referred to independently. | Conditional; link to an authoritative record where possible, rather than creating duplicate identity systems. |

### 2.2 Runtime data identity and traceability

These concepts describe the artifacts and context moving through the Lx pipeline and the O1 observability plane. They are defined or discussed in the D-series documents; their requiredness and propagation belong to those contracts, not to the sensor registry by default.

| Identifier or metadata | In plain language: what it tells us | What it helps SAR do | Status |
|---|---|---|---|
| `object_id` | “Which particular SAR data object is this?” | Refer to an observation or derived artifact and preserve lineage across stages. | Existing canonical data-object identity. |
| `source_id` | “Which data stream is this?” | Route and interpret observations as a particular stream. | Required by the current edge-frame contract; relationship to a physical sensor and replacement semantics require reconciliation. |
| `source_node_id` | “Which producer sent this edge frame?” | Identify the source-side producer in ingest topology. | Required in the current base edge frame. It does not identify a sensor or component slot. |
| `source_frame_id` / `source_native_id` | “What frame identifier did the source provide, if any?” | Preserve source evidence and support source-level tracing. | Optional/native identity; uniqueness scope must be known. It does not replace `object_id`. |
| `trace_id` | “Which related processing activity should be followed together?” | Correlate related activity and diagnostics. | Existing object field; not a substitute for object, source, run, or session identity. |
| `session_id` / `run_id` | “Which continuous operating context and bounded processing window does this record belong to?” | Group logs, processing, and reports. | Defined by D01.04. Execution context, not component identity. |
| `created_by_component`, `component_version`, `configuration_version` | “Which processing component and configuration created or transformed this object?” | Support reproducibility, debugging, and transformation provenance. | Existing provenance/telemetry concepts. They do not necessarily identify a system requirement slot or physical sensor. |
| `producer_epoch_id` | “Which uninterrupted producer sequence is this frame part of?” | Could distinguish frame-counter reuse after restart. | Deferred; not defined in the current base frame contract. |

An identifier is justified when it names an entity or relationship that needs independent, stable references. A useful attribute does not automatically require a new identifier. The tables separate system configuration references from runtime data traceability; they do not imply that every listed reference must be copied into every packet or log. The applicable D-series contract should specify what a consumer must receive directly and what may be resolved through approved configuration or registry context.

## 3. System components, software, and data-package components

### 3.1 System component slot and fulfillment

A `component_slot_id` would name a **system requirement position**, not a particular device. It could apply to any component the system architecture requires: a sensor, a processing service, a storage service, an interface, or another defined system element. A compatible replacement may fulfill the same slot, while the actual replacement remains a distinct component with its own identity and history.

“Fungible” should be limited to the slot's **eligible fulfillment**: a slot may be fulfilled by a component that meets its stated compatibility requirements, subject to approval. It should not imply that actual devices, software versions, records, or histories can be merged or treated as identical.

The proposed relationship is conceptually:

```text
component_slot_id (stable system requirement)
    -- fulfilled by, during an effective interval -->
actual component reference (physical sensor, software/service, or other component)
```

The relationship should capture only what is needed to reconstruct the configuration: slot, actual component reference, effective interval, compatibility/approval evidence, and change history. Its exact record shape and whether it needs its own identifier remain open.

### 3.2 Software components

The computational documents already define software processing components, including pipeline stages and cross-cutting observers. D02.01 says their operational metadata—such as component name, version, configuration, host/node identity, startup time, heartbeat, and latency—belongs in telemetry and may be attached to emitted-object provenance where required.

That existing model supports tracing **which software component and version transformed an object**. It does not establish that every software component has a stable slot ID, a persistent instance ID, or an identifier propagated on every packet. A later policy should decide which software requirements need stable slot references and which existing name/version/configuration/host metadata is sufficient. Do not assign software a physical `sensor_uid`.

### 3.3 Data-package components

A data packet, frame, SAR object, or object payload is not the same kind of component as a system requirement or processing component:

- A **system component** provides a capability required by the system design.
- A **data object** is an artifact exchanged between processing stages.
- A **field or section inside a data package** is normally defined by the package schema and version; it is not a system component slot.

Use the existing `object_id`, `object_type`, schema/profile version, payload, provenance, and parent-object references for data artifacts. Give a nested data element a separate ID only if it has an independent identity and reference lifecycle, not merely because it is a named field or section.

## 4. What existing SAR documents already provide

| Existing source | Existing purpose and coverage | What it does not currently establish |
|---|---|---|
| [D01.01 general pipeline specification](../../../computational/D01.01_SAR_General_Computational_Pipeline_Spec_V1.1_2026-07-27.md) | Defines O1 as cross-cutting logging, replay, and evaluation. Requires traceability across transformations; lists `provenance`, `trace_id`, `component_version`, and `configuration_version` among cross-layer fields. Requires derived objects to retain input lineage, transforming component/version, configuration or policy, and transformation time. | Does not define `component_slot_id`, an effective-dated requirement-to-component assignment, or universal `sensor_uid`/inventory fields on packets. |
| [D01.02 shared streaming contract](../../../computational/D01.02_SAR_Shared_Streaming_Contract_V1_2026-07-29.md) | Defines the edge-frame fields `source_node_id`, `source_id`, `modality`, `frame_index`, and `payload`; permits native frame/time fields; requires L1 canonical object identity and provenance for synthesized/backfilled values. | Does not list `sensor_uid` or `component_slot_id` in the required frame envelope, nor define producer epochs. |
| [D01.04 run/session policy](../../../computational/D01.04_SAR_Run_and_Session_Identity_and_Boundary_Policy_V1_2026-07-28.md) | Defines `session_id` and `run_id`, their relationship, and their propagation into logs and stage outputs. | Does not define sensor or system-component identity. |
| [D02.01 class and object model](../../../computational/D02.01_SAR_Computational_Class_and_Object_Model_V1_2026-07-27.md) | Separates data artifacts from processing components. Defines object provenance and says operational component metadata belongs in telemetry and may be attached to emitted-object provenance. | Uses “component” for software processing units; that is not the same as a system requirement slot. It does not define the new slot-assignment model. |
| [D00.02 computational glossary](../../../computational/D00.02_SAR_Computational_Glossary_V1_2026-07-29.md) | Defines `DataObject`, `Stage component`, `Provenance`, `Observation`, and related pipeline terms. | Does not define a system component slot or a generic component-instance identity. |
| [Current object model implementation](../../../../src/sar_core/contracts/models.py) and [identity/provenance implementation](../../../../src/sar_core/contracts/identity.py) | `DataObject` has `object_id`, `trace_id`, payload, provenance, and timing. `Provenance` currently has parent IDs, source-native ID, creator component, component version, and configuration version. `Observation` has `source_id`. | These implementation fields do not currently include `component_slot_id` or `sensor_uid`. A creator component name is not necessarily a stable component ID. |
| [Current edge-ingress implementation](../../../../src/sar_core/contracts/edge_ingress.py) and [observability implementation](../../../../src/sar_core/contracts/observability.py) | Edge frames carry source node and stream IDs; structured log records carry stage name, record type, message, timestamp, optional trace ID, and payload. | The listed log/object shapes do not currently express a component-slot-to-fulfillment assignment as a defined contract. |

Thus, provenance is **not absent**. SAR already defines provenance and O1 traceability. The gap is more specific: there is no approved, explicit mapping from a stable system requirement/slot to the particular physical or software component fulfilling it at a given time, nor a policy for when those references must appear in packets versus logs or resolvable registry context.

## 5. Issue 22, 23, and 24 review implications

### 5.1 Issue 22 review discussion

The Issue 22 review comment:

- agrees with UUIDv4 because timestamps are separate;
- raises concern about ID bloat and asks for a rationale or optional/placeholder designation for each ID;
- asks how Sensor UID relates to `asset_id`, assuming sensors are assets and assets can contain components;
- anticipates voluntary participation from personal/mobile devices and asks how these sources would be referenced;
- questions the semantic value of the `sar-` prefix; and
- asks whether the sequential human-readable tag is necessary and where it would be used.

The additional component-slot wording supplied during this review proposes a stable, fungible system-component reference that relates to the actual sensor identity and inventory record. This note refines that distinction: the stable ID should identify a **system requirement/slot**, while each physical fulfillment retains its own sensor and inventory references. The slot is not the physical unit's ID.

Recommended responses:

1. Retain UUIDv4 as the proposed opaque physical sensor identifier, subject to approval.
2. Classify identifiers by purpose and necessity; do not make every plausible ID mandatory.
3. Keep the authoritative inventory field and clarify whether it identifies an individual item or inventory line. Do not assume `asset_id` and `sensor_uid` are interchangeable.
4. Consider mobile/personal devices as participation sources under a separate consent, privacy, and retention policy. Do not rely on a persistent hardware address as a general-purpose sensor UID. Decide whether a temporary/pseudonymous sensor reference is required for a participation interval.
5. Treat `sar-` as an application namespace/prefix proposal, not an inherent UUID requirement. The project should decide whether SAR-issued IDs need namespace collision avoidance across systems or whether a bare UUID in a typed field is sufficient.
6. Defer the short sequential tag until a pilot demonstrates a practical labeling or operations need.
7. Add `component_slot_id` as a new candidate concept only after defining the system-component scope and deciding how assignment history is represented in packets/logs.

### 5.2 Issue 23 object-model proposal

The Issue 23 package separates common SAR data-object fields, subtype fields, composed metadata, and processing interfaces. It explicitly defines “global” as common to every data-object instance—not a single shared identifier. It retains `object_id` as the identity of each object, `trace_id` for correlation, and provenance as metadata. It also distinguishes processing components from data artifacts.

This supports a restrained identity design: common object identity and provenance remain in the object model; source-specific fields remain on `Observation`; processing software remains component/telemetry metadata. The proposal does not define `component_slot_id` as a system-requirement identity. It is itself marked proposed, and its abstract-base, context, and validator decisions are not approved merely because the package reports isolated design checks.

### 5.3 Issue 24 audio contract review

The Issue 24 package concludes that the audio profile is structurally compatible with the proposed shared-object structure, but full alignment and runtime conformance are not established. It distinguishes a source transport frame from an internal SAR data object and notes that L1 owns canonical SAR identity and ingest timestamps.

Its mapping says sensor UID and procurement asset IDs are registry relationships and **should not be universal per-frame class fields**. It also maps component/version/configuration information to provenance and operational telemetry, and identifies the distinction between native and generated frame identity as an open contract issue.

This is directly relevant to Issue 22: packet/log traceability does not mean every packet must duplicate all sensor, asset, slot, deployment, and component metadata. A packet may carry a stable reference where needed, while the time-bounded registry relationship supplies the remaining context. The contract must define which is required and how a consumer resolves it. The Issue 24 package's 13 probes used synthetic data; they are evidence about the tested scaffold path, not certification of live hardware or an approved contract.

## 6. Recommended classification of proposed identifiers

“Essential” below means essential to a distinct existing or proposed function—not that every value must appear on every packet.

| Identifier or reference | Assessment | Plain-language purpose and recommended handling |
|---|---|---|
| `object_id` | Essential to existing SAR data-object model | Names one particular SAR observation or derived artifact so stages, logs, and parent links can refer to it. Keep distinct from source and sensor identities. |
| `source_id` | Essential to current frame/observation model; semantics unresolved | Names the data stream. Resolve whether identity follows the logical channel across hardware replacement or is bound to a specific physical unit; do not silently change existing values. |
| `source_node_id` | Required by current edge-frame contract | Names the producer that emitted a frame. It does not name the physical sensor or system slot. |
| `session_id`, `run_id` | Required by D01.04 policy | Group runtime activity into a continuous session and bounded run. Their current propagation into object/log schemas is an adjacent cross-contract concern, not a reason to identify a sensor with them. |
| `trace_id` | Existing optional object correlation field | Helps follow related processing activity. It is not a substitute for object, source, run, or session IDs. |
| `sensor_uid` | Proposed essential registry identity for a tracked physical sensing unit | Answers which physical sensing unit is represented. Keep it separate from the system requirement it fulfills, stream, inventory record, and observation. Do not automatically make it a field on every frame. |
| Inventory reference | Essential when an authoritative inventory record exists | Links to procurement/operations facts. Reuse its authority and clarify whether its record represents one item or a group/line. |
| `component_slot_id` | New, conditional system-architecture reference | Answers which stable system requirement position is being fulfilled. Useful when data or logs must be interpreted against that requirement over replacement intervals. Not defined in V1/V2 or existing contracts. |
| Component assignment relation | Needed only if fulfillment/history is required | Says which actual component fulfilled which slot, when, and with what approval/evidence. Prefer a relationship with effective dates; give it its own ID only if it needs independent references. |
| Software component name/version/configuration | Existing provenance/telemetry concepts | Says what software transformed or handled the data. Use existing metadata first; introduce a stable software slot/instance ID only where name/version/configuration are insufficient for a defined traceability need. |
| `source_frame_id` / `source_native_id` | Optional/source-dependent | Preserves a producer's own frame reference and its source-specific uniqueness scope. It is not the canonical SAR `object_id`. |
| `ingest_node_id` | Conditional topology/operations context | Names the receiving service if routing or audit requires it. Not required in the current base frame. |
| `producer_epoch_id` | Deferred | Could distinguish frame-counter sequences across restarts, but allocation, persistence, crash, and replay policies are not in the current base contract. |
| `deployment_id` | Conditional | Use if deployment intervals must be independently referenced. Otherwise the effective-dated assignment/deployment relation may suffice. |
| Calibration record/revision reference | Conditional | Needed when measurement interpretation depends on calibration history. Prefer a link to the authoritative calibration record over inventing a parallel ID. |
| `sensor_tag` | Optional convenience alias | Short human-readable equipment label. Defer until a pilot establishes who uses it and where. |
| `sensor_label`, `component_boundary`, location, modality, observed property, status | Attributes, not IDs | Describe an entity or relationship. Use effective history when values change; do not treat them as stable join keys. |

## 7. Recommended direction for the next proposal revision

1. Put a plain-language identity model near the beginning, answering what each reference lets a person or system do.
2. Separate **system requirement/slot**, **actual component fulfillment**, **physical Sensor UID**, **inventory reference**, **source stream**, **producer**, and **SAR data object**.
3. State explicitly that “component” includes hardware and software system components, but distinguish both from data objects and data-package fields.
4. Mark `component_slot_id` as a new candidate concept, not as terminology already established by V1 or the computational contracts.
5. Describe packets and logs as consumers of the existing provenance/trace framework. Do not claim that sensor UID, inventory ID, or slot ID is already in every packet or log.
6. Define a data-resolution requirement: at the relevant time, a packet/log reference must either identify the system requirement and actual component needed for interpretation or resolve unambiguously through approved registry/assignment context. Decide the required transport fields through contract review.
7. Classify each ID as existing contract requirement, proposed registry requirement, or conditional/deferred. Provide a reason and indicate where it belongs—not just a list of names.
8. Reconcile `source_id` semantics with the current sensor mapping before changing its replacement behavior.
9. Keep UUIDv4 as the proposal's physical sensor format; explain any `sar-` namespace prefix decision separately from UUID uniqueness.
10. Defer short tags and secondary IDs unless a pilot shows an independent operational need.
11. Treat personal/mobile-device participation as a separate consent/privacy and identity-lifetime decision. Avoid retaining persistent device identifiers without a justified policy.
12. Reuse current `object_id`, `trace_id`, provenance, `component_version`, `configuration_version`, and O1 logging. Propose only the missing system-requirement/assignment references and any necessary context propagation.

## 8. Draft response text for the Issue 22 discussion

> Thank you for the review. I agree that UUIDv4 is appropriate for the proposed physical sensor UID, and that the proposal should justify each identifier rather than imply that all possible IDs are required.
>
> I will distinguish the system's component requirement from the actual component fulfilling it. A proposed `component_slot_id` would identify a stable system requirement position; it would not identify the hardware. The physical unit would keep its own `sensor_uid`, with an inventory reference where one exists. The assignment between slot and actual component would be time-bounded and auditable. This slot concept is new and is not currently defined in the Issue 22 V1 proposal or the existing computational contracts.
>
> “Component” here should include system hardware and software components. SAR already has provenance and O1 concepts for tracing processing component, version, and configuration. However, the existing contracts do not define a stable system requirement slot or the slot-to-component assignment relationship. We should distinguish system components from data objects and fields inside data packages.
>
> I also reviewed the Issue 23 object-model proposal and Issue 24 audio-contract assessment. They reinforce that object identity, source identity, processing-component metadata, and registry relationships have different purposes. In particular, sensor and inventory IDs should not automatically become fields on every data packet. We should decide which system-requirement and component references a packet or log needs and whether the rest can be resolved through effective-dated registry context.
>
> The existing mapping describes `source_id` as stable per logical stream, so its replacement behavior needs reconciliation before adoption. I suggest retaining UUIDv4, deferring a short sequential equipment tag until a pilot establishes its use, and treating personal/mobile-device participation under a separate consent, privacy, and retention policy rather than using a persistent hardware address as a sensor UID. I will revise the proposal to make these distinctions and the rationale for each reference explicit.

This is draft wording for discussion; it does not record approval, change an issue, or modify any runtime contract.

## 9. References and limits

1. [Issue 22 discussion](https://github.com/CHI-CityTech/Self-Aware-Room/issues/22), including the review comments. The additional component-slot wording analyzed here was supplied separately during this review.
2. [Issue 23 object-model proposal discussion](https://github.com/CHI-CityTech/Self-Aware-Room/issues/23) and its attached October 28 proposal package.
3. [Issue 24 audio-contract review discussion](https://github.com/CHI-CityTech/Self-Aware-Room/issues/24) and its attached October 28 review package.
4. [Issue 22 UID Proposal V1, originating proposal](./PROPOSAL_FOR_REVIEW.md).
5. [Issue 22 UID Proposal V2, revised proposal](./PROPOSAL_FOR_REVIEW_V2.md).
6. [Sensor inventory and computational mapping](../../../sensors/SAR_Sensor_Inventory_and_Computational_Mapping_V1_2026-08-03.md).
7. [D00.02 glossary](../../../computational/D00.02_SAR_Computational_Glossary_V1_2026-07-29.md), [D01.01 pipeline specification](../../../computational/D01.01_SAR_General_Computational_Pipeline_Spec_V1.1_2026-07-27.md), [D01.02 shared streaming contract](../../../computational/D01.02_SAR_Shared_Streaming_Contract_V1_2026-07-29.md), [D01.04 run/session policy](../../../computational/D01.04_SAR_Run_and_Session_Identity_and_Boundary_Policy_V1_2026-07-28.md), and [D02.01 object model](../../../computational/D02.01_SAR_Computational_Class_and_Object_Model_V1_2026-07-27.md).
8. [Data-object model implementation](../../../../src/sar_core/contracts/models.py), [identity/provenance implementation](../../../../src/sar_core/contracts/identity.py), [edge ingress](../../../../src/sar_core/contracts/edge_ingress.py), and [observability record](../../../../src/sar_core/contracts/observability.py).

Issue 23 and Issue 24 package findings are reported as proposed analysis, not as approved repository changes. Their synthetic checks did not test live hardware or establish production conformance. This document proposes no contract or runtime changes and does not verify physical inventory records.

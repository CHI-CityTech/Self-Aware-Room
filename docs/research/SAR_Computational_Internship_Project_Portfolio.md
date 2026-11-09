# SAR Computational Internship Project Portfolio

**Document type:** Student project and internship opportunity portfolio  
**Project:** Self-Aware Room (SAR)  
**Status:** Working portfolio; project scopes require confirmation before assignment  
**Last updated:** 2026-11-09

## 1. Purpose

This portfolio translates the Self-Aware Room computational architecture into research and implementation opportunities for interns and student researchers, including students in data science, computer science, engineering, human-computer interaction, and related fields.

The portfolio is intentionally broader than an individual internship plan. SAR's computational layers and interfaces are still being specified, so opportunities are presented as candidate projects rather than approved requirements. As the architecture becomes more explicit, project owners can refine each opportunity into a scoped task with an accountable mentor, prerequisites, data access, acceptance criteria, and a realistic term-length deliverable.

The architectural starting point is [D01.01 - SAR General Computational Pipeline Specification](D01.01_SAR_General_Computational_Pipeline_Spec_V1.1_2026-07-27.md). Its layer names and responsibilities are the organizing framework here; this portfolio does not replace or amend those specifications.

## 2. How to use this portfolio

Use the project ideas to:

1. Match student interests and skills to SAR needs.
2. Select a bounded first project that can be completed using simulated, sample, or approved data.
3. Identify dependencies on sensor profiles, data contracts, hardware, policies, or other workstreams.
4. Build a sequence from an independent prototype toward integration with adjacent layers.
5. Convert the selected project into an intake card, issue, experiment plan, or implementation task with measurable completion criteria.

Not every project is ready to start. Some can proceed with synthetic fixtures and existing code; others depend on decisions or interface contracts that are still under review. Each scope should be checked against current repository documentation and the project owner's priorities before assignment.

### Suggested scope sizes

- **Starter (1-3 weeks):** a focused analysis, test suite, data-quality check, or small prototype with a clear demonstration.
- **Term project (4-10 weeks):** an integrated prototype, evaluation, or documented subsystem with tests and reproducible results.
- **Research track (multiple terms or a team):** a coordinated effort spanning specifications, implementation, field validation, and governance.

These are planning ranges, not guarantees. Availability, mentor capacity, hardware, data approvals, and student experience determine actual scope.

## 3. SAR computational layers and candidate projects

### L0 - Edge capture and transport

L0 is source-adjacent capture and framing, potentially on constrained or distributed devices. Projects should focus on dependable transport and evidence preservation, not semantic interpretation.

#### L0-A. Edge stream reliability characterization

- **Question:** Under what conditions does a chosen edge source deliver complete, ordered, and timely frames?
- **Work:** Generate or capture a controlled stream; measure loss, delay, ordering, reconnect behavior, and buffer pressure under documented conditions.
- **Deliverables:** Reproducible test harness, metrics report, and recommendations for transport settings or acceptance thresholds.
- **Good fit:** Data science, computer engineering, networking, or systems students.
- **Dependencies:** Defined source/frame identity and a test transport or device.

#### L0-B. Lightweight edge data validation

- **Question:** What minimum validation can run near a sensor before frames are sent to ingest?
- **Work:** Prototype validation for required fields, value ranges, timestamps, and payload size; distinguish rejected, incomplete, and accepted frames.
- **Deliverables:** Small adapter or validation module, test cases, and a resource/latency comparison.
- **Dependencies:** A selected modality profile and agreed error behavior.

### L1 - Ingest acquisition

L1 receives source frames, checks identity and timing metadata, preserves raw evidence where approved, and emits source-local observations.

#### L1-A. Ingest quality and source-health monitor

- **Question:** Can the system detect a source that is missing, delayed, noisy, or producing incomplete data?
- **Work:** Build health indicators from timestamps, heartbeat events, queue depth, and acquisition errors, using simulated data if live hardware is unavailable.
- **Deliverables:** Quality metrics, alerting rules or a small report/dashboard, and tests for failure scenarios.
- **Dependencies:** Source contracts and thresholds for stale or degraded input.

#### L1-B. Sensor onboarding and identity crosswalk prototype

- **Question:** How can inventory, physical sensing units, logical streams, and ingest producers be related without conflating their identities?
- **Work:** Create a fictional or approved sample registry and validate completeness, duplicate registrations, and effective-dated assignments.
- **Deliverables:** Example registry schema, validation checks, and onboarding walkthrough.
- **Important constraint:** The Sensor UID proposal is not an approved runtime contract. Do not allocate real identifiers or change runtime IDs on the basis of a proposal alone.

### L2 - Normalization and local abstraction

L2 makes source-specific observations more comparable while retaining provenance, data quality, and links to their source evidence.

#### L2-A. Canonical observation and unit normalization

- **Question:** Can observations from selected devices be converted into a stable, documented representation?
- **Work:** Map source fields and units to a canonical structure; test valid, missing, out-of-range, and unsupported values.
- **Deliverables:** Mapping documentation, normalization code or notebook, fixtures, and conformance tests.
- **Dependencies:** A selected data profile and decisions on units, time fields, and quality markers.

#### L2-B. Audio feature and silence analysis

- **Question:** Which non-speech features can characterize audio activity reliably enough for downstream processing?
- **Work:** Explore features such as RMS level, silence intervals, clipping, and event duration using synthetic or explicitly approved audio.
- **Deliverables:** Reproducible analysis, feature definitions, error/limitations discussion, and test fixtures.
- **Important constraint:** Do not collect, retain, or analyze speech content without appropriate consent and an approved data-handling plan.

#### L2-C. Data-quality scoring for normalized observations

- **Question:** How should uncertainty and quality issues be represented so later layers can use them?
- **Work:** Compare quality indicators for missingness, sensor status, calibration age, noise, and timestamp reliability without treating a score as certainty.
- **Deliverables:** Proposed quality fields, example calculations, and evaluation cases for downstream consumers.

### L3 - Coherence, correlation, and integration

L3 associates normalized evidence across time, space, and sources. Correlation is not proof of causation; uncertainty and contradictory evidence must remain visible.

#### L3-A. Asynchronous timestamp alignment

- **Question:** How sensitive are candidate room-state estimates to clock error, sampling rate, and alignment-window choice?
- **Work:** Create datasets with known timing offsets and compare alignment approaches on a controlled set of events.
- **Deliverables:** Evaluation notebook or module, timing-error plots, recommended test cases, and documented limitations.
- **Dependencies:** Timestamp semantics and a representative event definition.

#### L3-B. Duplicate and dependent evidence detection

- **Question:** When do multiple observations represent the same underlying evidence rather than independent confirmation?
- **Work:** Test duplicate candidates using source identity, frame metadata, timing, and signal similarity on synthetic or approved data.
- **Deliverables:** Candidate rules, false-match/missed-match evaluation, and traceable test fixtures.
- **Dependencies:** Shared streaming contract and explicit duplicate policy.

#### L3-C. Cross-modal association and room-state estimation

- **Question:** Can selected modalities support a bounded, confidence-weighted state estimate?
- **Work:** Explore a narrow scenario, such as relating simulated presence events with sound-level changes; retain supporting, contradicting, and unavailable evidence.
- **Deliverables:** Prototype association method, benchmark scenarios, confidence analysis, and a clear statement of what cannot be inferred.
- **Important constraint:** Avoid identity inference or sensitive attribute inference unless specifically reviewed and approved.

#### L3-D. Spatial registration and uncertainty study

- **Question:** How do coordinate-frame mismatch and location uncertainty affect observation association?
- **Work:** Use a synthetic room map to test coordinate transformations, uncertainty propagation, and out-of-frame observations.
- **Deliverables:** Test dataset, visualization, and proposed interface/acceptance cases.
- **Dependencies:** A selected spatial frame and approved coordinate conventions.

### L4A - Semantic interpretation

L4A maps coherent evidence into structured interpretations. Projects should evaluate when a system is correct, uncertain, or appropriately unable to conclude.

#### L4A-A. Rules-based semantic benchmark

- **Question:** How well do existing deterministic rules work on representative positive, negative, ambiguous, and conflicting inputs?
- **Work:** Build a labeled evaluation set; measure precision, recall, false-positive patterns, and indeterminate behavior.
- **Deliverables:** Versioned test cases, evaluation script, results report, and recommendations for rule changes.
- **Good fit:** Data science students interested in evaluation and classification.

#### L4A-B. Local AI model comparison for structured interpretation

- **Question:** Does a local model improve a narrowly defined interpretation task over a deterministic baseline?
- **Work:** Compare one or more local models and a rules baseline on the same approved, non-sensitive fixtures. Evaluate structured-output validity, accuracy, consistency, latency, and resource use.
- **Deliverables:** Reproducible comparison, structured evaluation dataset, failure analysis, and a recommendation—not an automatic production integration.
- **Dependencies:** Approved local inference environment, task definition, and evaluation criteria.

#### L4A-C. Uncertainty, abstention, and explanation evaluation

- **Question:** Can the system distinguish supported conclusions from uncertain or conflicting evidence?
- **Work:** Test confidence calibration or abstention strategies and whether explanations point to relevant evidence without overstating certainty.
- **Deliverables:** Evaluation protocol, examples of success/failure, and recommendations for human review.
- **Important constraint:** Explanations are not proof that a model's internal reasoning is correct; evaluate outputs against evidence and labels.

### L4B - Policy and decision

L4B evaluates interpretations against policy and determines whether action is permitted, required, deferred, suppressed, or unnecessary.

#### L4B-A. Decision-policy test matrix

- **Question:** Can policy requirements be translated into explicit, testable cases?
- **Work:** Work with project leadership to represent allowed, disallowed, conflicting, missing-context, and human-review conditions.
- **Deliverables:** Policy test matrix, example decision records, and automated tests for the agreed cases.
- **Dependencies:** Human-approved policy text and decision ownership.

#### L4B-B. Human review and override workflow

- **Question:** Where should a person confirm, reject, or defer a machine-proposed action?
- **Work:** Map review points, information presented to reviewers, override recording, and timeout/failure behavior.
- **Deliverables:** Workflow diagram or clickable prototype, event schema proposal, and usability findings.
- **Important constraint:** Students should not define safety, privacy, or institutional policy independently.

### L5A - Orchestration

L5A turns approved intents into coordinated plans with timing, dependencies, priority, and resource constraints.

#### L5A-A. Intent-to-plan simulation

- **Question:** How should competing authorized intents be prioritized and sequenced?
- **Work:** Build a simulator for a small set of non-sensitive room outputs with defined dependencies, conflicts, and resource limits.
- **Deliverables:** Scheduling prototype, scenario tests, and performance/behavior comparison.
- **Dependencies:** Agreed intent and execution-plan examples; do not control production hardware.

#### L5A-B. Multi-agent task coordination study

- **Question:** Can multiple specialized AI components coordinate without duplicating work or issuing conflicting requests?
- **Work:** Simulate bounded roles (for example, analyzer, policy checker, and response planner) and compare coordination patterns with a single-agent or deterministic baseline.
- **Deliverables:** Reproducible scenarios, conflict and latency metrics, and recommendations for human approval gates.
- **Important constraint:** Multi-agent behavior remains experimental unless separately approved and bounded.

### L5B - Output dispatch

L5B translates an approved plan into channel-specific commands and records endpoint acceptance, rejection, completion, or failure.

#### L5B-A. Dispatch contract and simulator

- **Question:** What should a dispatch request and endpoint result contain to support reliable handoff?
- **Work:** Define test fixtures for accepted, rejected, timed-out, and partially completed actions; use a simulator instead of live devices.
- **Deliverables:** Contract proposal, endpoint simulator, and automated tests for status handling.
- **Dependencies:** Output-channel owners and approved interface specifications.

#### L5B-B. Dispatch reliability and latency analysis

- **Question:** Where does delay or failure occur between plan creation and endpoint completion?
- **Work:** Instrument a controlled demo and report timing distributions, retries, duplicate command risks, and failure cases.
- **Deliverables:** Measurement report and prioritized test/observability recommendations.
- **Important constraint:** No live room actuation without explicit system-owner authorization and a safe test plan.

### O1 - Logging, replay, and evaluation (cross-cutting)

O1 observes processing across all layers. It supports diagnosis and evaluation rather than forming a final processing stage.

#### O1-A. End-to-end trace and data lineage

- **Question:** Can an output be traced to its source observations, transformations, decisions, and dispatch result?
- **Work:** Define a sample trace across a narrow pipeline path and identify missing links or ambiguous identifiers.
- **Deliverables:** Trace example, lineage visualization or query, and trace completeness tests.

#### O1-B. Replay and regression evaluation

- **Question:** Can a recorded, approved test case be replayed to compare behavior across versions?
- **Work:** Build fixtures and a replay harness that captures configuration/version metadata and compares outputs.
- **Deliverables:** Replay prototype, regression metrics, and instructions for adding a test scenario.
- **Dependencies:** Data-retention approval and stable interfaces for the selected layers.

#### O1-C. Pipeline observability dashboard

- **Question:** Which operational measures help researchers distinguish source, processing, and dispatch failures?
- **Work:** Analyze synthetic run traces and display counts, timing, degraded states, and failure locations.
- **Deliverables:** Dashboard or report prototype with metric definitions and known limitations.

## 4. Cross-cutting AI integration opportunities

AI is a capability that may be used within or alongside layers; it is not itself a pipeline layer and does not replace layer contracts or policy authority.

Potential projects include:

1. **Model selection and local inference:** compare candidate local models against deterministic baselines for a narrowly defined, measurable task.
2. **Structured-output reliability:** test schema validity, refusal/abstention, malformed responses, and robustness to ambiguous input.
3. **Human-AI collaboration:** prototype review workflows in which students or operators can inspect evidence, correct labels, and record decisions.
4. **AI-assisted development evaluation:** study whether coding assistants improve task completion or test quality, while documenting review effort and defects.
5. **AI documentation and knowledge retrieval:** prototype retrieval over approved SAR documentation with source citations and tests for unsupported answers.
6. **Model and prompt versioning:** record model, prompt, configuration, dataset, and evaluation versions so results can be reproduced.
7. **Privacy-preserving experimentation:** compare synthetic or de-identified fixtures with approved data and document what each evaluation can and cannot establish.

Every AI project should define the task boundary, baseline, evaluation set, acceptable failure modes, data handling, model/runtime provenance, and human oversight before reporting performance. A prototype result is not evidence of production readiness.

## 5. Collaborative workflow opportunities

SAR projects can provide useful research and engineering work beyond model building:

- **Shared dataset and test-case stewardship:** curate synthetic/approved fixtures, labels, schemas, edge cases, and data dictionaries.
- **Contract-to-test mapping:** trace specification statements to executable tests and report requirements without tests or tests without clear requirements.
- **Reproducible notebooks and experiments:** package data provenance, environment details, scripts, and result summaries so another student can rerun the analysis.
- **Issue and dependency mapping:** turn architecture gaps into small tasks with acceptance criteria, ownership, prerequisites, and handoff notes.
- **Cross-layer integration demonstrations:** connect two adjacent layers with simulated inputs and outputs, documenting assumptions and unresolved interface questions.
- **Peer review and quality practices:** add pull-request checklists for tests, documentation, data governance, AI provenance, and reproducibility.
- **Research-to-implementation handoff:** summarize findings in a decision record that states evidence, limitations, open questions, and a proposed next action.

Student work should use the repository's existing contribution and review practices. Coordinate student onboarding, cohort scheduling, and contact/intake information through the Student Research program; keep technical specifications, SAR code, and reusable SAR project definitions in the SAR repository.

## 6. Example internship tracks

These are example combinations, not fixed job descriptions.

### Data science track: trustworthy room-state estimation

1. Start with data-quality characterization (L1/L2).
2. Build timing-alignment fixtures and metrics (L3).
3. Evaluate one bounded state-estimation problem with uncertainty (L3/L4A).
4. Deliver a reproducible report, test set, and recommendation for follow-on work.

### AI evaluation track: rules versus local model

1. Define a narrow semantic task and label criteria (L4A).
2. Establish a deterministic baseline and evaluation dataset.
3. Compare a local model on accuracy, abstention, structured-output validity, latency, and reproducibility.
4. Present failure analysis and a recommendation, including cases requiring human review.

### Systems/data engineering track: source-to-observation reliability

1. Simulate or connect a bounded source (L0/L1).
2. Validate and normalize observations (L2).
3. Add source health and traceability metrics (O1).
4. Demonstrate failure handling and provide a handoff document.

### Collaborative AI workflow track

1. Select one research or coding workflow that uses an AI assistant.
2. Compare unaided and AI-assisted approaches on repeated, bounded tasks.
3. Measure correctness, review effort, reproducibility, and documentation quality.
4. Recommend a safe team workflow; do not treat AI-generated content as verified without review.

## 7. Scoping and acceptance checklist

Before assigning an opportunity, a mentor and student should record:

- **Research or engineering question:** What specific uncertainty or capability will the project address?
- **Layer and interface:** Which layer(s) are in scope, and what are the inputs and outputs?
- **Status of dependencies:** Which specifications, hardware, datasets, approvals, or partner contributions are available?
- **Bounded deliverable:** What code, analysis, test suite, prototype, or documented finding will be produced?
- **Acceptance criteria:** What observable checks demonstrate completion (for example, required test cases pass, measurements are reproducible, or a report answers the stated question)?
- **Data plan:** Is data synthetic, public, de-identified, or sensitive? Who authorizes access, and what are retention and deletion rules?
- **AI plan:** Which models or assistants are used, what is recorded, and how are outputs reviewed?
- **Collaboration plan:** Who reviews work, how are issues and handoffs managed, and what other workstreams are affected?
- **Out-of-scope work:** Which adjacent capabilities are intentionally excluded?
- **Next-step decision:** What evidence would justify integration, a follow-on project, or stopping the work?

Prefer simulated or synthetic data while interfaces, policies, and access approvals are unsettled. If real sensor, audio, video, biometric, or other sensitive data is contemplated, do not collect or process it until the responsible project authorities approve the purpose, consent approach, access, security, and retention plan.

## 8. Suggested portfolio evolution

This portfolio should evolve with the computational specifications rather than become a parallel source of technical requirements:

1. Keep this file as the discoverable catalog of candidate student projects.
2. When a project is selected, create its implementation tasks in the appropriate code/workstream area and its experiment plan or report under `experiments/` when applicable.
3. Link a project to the relevant D01/D02/D03 specification and identify unresolved interface or policy decisions.
4. Update this portfolio when a layer or contract changes enough to affect project feasibility.
5. Move a project into a formal specification only when its reusable requirements and decisions are reviewed and approved.

For student program operations, use the [student project intake schema](../../operations/student_project_intake_spreadsheet_schema.md) and the Student Research repository's active cohort process. This document should be linked from that repository rather than copied as a second technical source of truth.

## 9. Related references

- [D01.01 - General Computational Pipeline Specification](D01.01_SAR_General_Computational_Pipeline_Spec_V1.1_2026-07-27.md)
- [D01.02 - Shared Streaming Contract](D01.02_SAR_Shared_Streaming_Contract_V1_2026-07-29.md)
- [D01.03 - Coherence, Correlation, and Integration Specification](D01.03_SAR_Coherence_Correlation_and_Integration_Detailed_Spec_V0_2026-07-28.md)
- [D03.01 - Sensor Intake Phase 1 Specification](D03.01_SAR_Sensor_Intake_Document_Phase_1.md)
- [D04.03 - Computational Task, Dependency, Test, and Milestone Map](D04.03_SAR_Computational_Task_Dependency_Test_and_Milestone_Map_V1_2026-08-03.md)
- [Student Project Intake Spreadsheet Schema](../../operations/student_project_intake_spreadsheet_schema.md)

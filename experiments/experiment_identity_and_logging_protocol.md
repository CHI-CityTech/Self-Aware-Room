# SAR Experiment Identity and Logging Protocol

This protocol defines how SAR identifies experiment series, scoped tests, and repeated runs across independently working teams. The leading letter identifies the responsible team; result domain(s) and collaborators are recorded separately because a team's experiment may establish outcomes relevant to several canonical areas.

## 1. Identifier Hierarchy

Use three levels where needed:

1. Experiment series: `<TEAM-CODE><NN>`, for example `V02`.
2. Test or subexperiment: `<SERIES-ID>.<NN>`, for example `V02.01`.
3. Repeated execution: `<TEST-ID>-RNN-YYYYMMDD`, for example `V02.01-R02-20261012`.

Series numbers are allocated within the responsible team's sequence, not through a repository-wide counter. Test numbers distinguish planned stages or distinct questions within a series; run numbers distinguish repeated executions of the same test. Do not use a run number when the record describes a distinct test. The team's code and allocation process must be registered here before other teams adopt them.

## 2. Domain Assignment

Record the result domain according to the primary question and the canonical area(s) that may be affected if the work succeeds. The experiment ID follows the responsible team's sequence, not the result domain or the systems used.

Current result-domain labels:

- Communications: protocols, message vocabularies, transport, and interoperability.
- Control/Video: control-to-video display paths and video delivery.
- Video: video and projection behavior within the video subsystem.

Record collaborating teams and all relevant result domains in the registry. Use cross-references when an experiment has meaningful effects in additional canonical areas.

## 3. Filenames and Report Metadata

Start experiment report filenames with the most specific identifier, followed by a short scope description:

`<TEST-ID>_<Scope_Description>.md`, for example `V02.01_QLab_to_TD_OSC_Clip_Selection.md`.

Each report records its series ID, test ID, scope title, result domain(s), collaborating team(s), execution/report date, author, status, and links to its procedure, evidence, and related records. Legacy `EYY.MM.DD#NN` identifiers remain searchable aliases until the registry records their disposition; do not silently reuse or discard them.

## 4. Registry and Execution Log

The registry in [README.md](README.md) is the authoritative lookup for series and test IDs. It records title, result domain(s), dates, status, location, responsible/collaborating teams, and legacy aliases where applicable. Track READMEs may summarize and link to records but must not allocate IDs independently.

Keep experiment reports and evidence with the responsible project/team when that best supports execution and collaboration. The registry may point outside `experiments/`. Keep the experiment record distinct from canonical specifications and procedures.

## 5. Review and Promotion

An experiment record is evidence, not an approved standard by default. Only after review and approval should validated, reusable outcomes be promoted into the relevant canonical documentation. A Communications result may be cross-referenced from Video, Computation, or other affected tracks without moving or duplicating the original experiment record.

## 6. Current Series Allocation

| Series ID | Responsible team | Scope | Tests |
| --- | --- | --- | --- |
| V01 | Video | 2026 Summer Video experiments and integrations | V01.01-V01.07 |
| V02 | Video (joint Computation/Video work) | QLab-TD integration: OSC command paths and TD-output-to-QLab display | V02.01-V02.04 |

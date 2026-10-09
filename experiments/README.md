# Experiments Index

This folder contains pre-integration laboratory protocols, trial plans, and executed experiment records. A record may remain in its responsible team's working folder when that supports collaboration; this index remains the authoritative registry of experiment and test IDs.

These files are intentionally separate from canonical specification documents under docs/.

## Structure

- communications/: network and protocol communication experiments
- video/: projection, TouchDesigner, and visual output experiments

Each track may include:

1. Experiment reports (ID-named markdown files)
2. references/ for supporting files (PDFs, exports, quick guides, external notes)

## Experiment Identity

SAR uses team-scoped experiment series IDs, test IDs, and run IDs. The leading letter identifies the responsible team; result domains and collaborators are recorded separately. See [Experiment Identity and Logging Protocol](experiment_identity_and_logging_protocol.md) for the full convention and authoritative registry below.

## Issue-Driven Workflow

Experiments are managed as assigned work items and reviewed before any canonical promotion.

1. Create and assign an experiment issue.
2. Researcher runs the experiment and posts operational notes in the issue.
3. Researcher submits an experiment report using its registered test ID and scope description.
4. Reviewers provide feedback in the issue and set disposition.
5. If approved for promotion, canonical docs are updated by distilling validated outcomes.

## Feedback and Evaluation Gate

No experiment report is treated as canonical by default.

1. Registry entries may stay as provisional until review is complete.
2. Review feedback is captured in the linked issue thread.
3. Promotion decisions should be one of:
	- Evidence only (no canonical change)
	- Promote to instruction manual
	- Promote to canonical spec/policy language
	- Archive/supersede with rationale

## Status Vocabulary

Use these status labels to keep issue, report, and registry language consistent:

1. Protocol Draft
2. Assigned
3. In Execution
4. Report Submitted
5. Under Review
6. Accepted as Evidence
7. Promotion Approved
8. Archived or Superseded

## Active Experiment Registry

| ID | Level | Result domain | Title / Scope | Record / Evidence | Team/Owner | Date | Status | Legacy ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V01 | Series | Video; Communications; Control | 2026 Summer Video experiments | [2026 Summer index](../system/video/2026%20Summer/README.md); [CHI fellowship technical report](../system/video/CHI_Self-Aware-Room_Report_GAA.pdf) | Video; joint contributors as noted per test | 2026-07-15 to 2026-08-13 | Retrospective series; individual run dates not consistently recorded | Various |
| V01.01 | Test | Video | Single-projector KantanMapper mapping and output verification | CHI fellowship report, §§3.1-3.3; supporting patches in [2026 Summer](../system/video/2026%20Summer/02_Patches/) | Video | Fellowship period; exact test date not stated | Reported completed | None |
| V01.02 | Test | Video | Three-projector output and Perform-mode frame-rate validation | CHI fellowship report, §§4.1-4.5; supporting patches in [2026 Summer](../system/video/2026%20Summer/02_Patches/) | Video | Fellowship period; exact test date not stated | Reported completed; Perform mode resolved slowdown | None |
| V01.03 | Test | Communications; Video | OSC index drives TouchDesigner asset selection and projector output | CHI fellowship report, §§6-8; OSC evidence in [2026 Summer](../system/video/2026%20Summer/00_Documentation/OSCtoTOUCHS/) | Joint Video/Computation | Fellowship period; exact test date not stated | Reported demonstrated; not an approved OSC command contract | Legacy OSC field records listed below |
| V01.04 | Test | Control; Video | Keyboard input selects projected state | CHI fellowship report, §9.1 | Video | Fellowship period; exact test date not stated | Reported completed | None |
| V01.05 | Test | Communications; Video | Camera hand tracking sends OSC values to control TD image/object state | CHI fellowship report, §9.2 | Joint Video/Computation | Fellowship period; exact test date not stated | Reported tested; detailed run record not located | None |
| V01.06 | Test | Communications; Video; Virtual integration | Python state drives TouchDesigner and Unity across Ethernet | CHI fellowship report, §11 | Joint Video/Computation | Fellowship period; exact test date not stated | Reported functioning in controlled test; not hardened | None |
| V01.07 | Test | Video; Audio/Computation integration | Fruit detection to TD image selection | [Integration note](video/V01.07_Fruit_Detection_to_TD_Image_Selection.md) | Video | 2026-07-31 | In progress; TD display not confirmed | E26.07.31#02 |
| V02 | Series | Communications; Control/Video | QLab-TD integration: OSC command paths and TD-output-to-QLab display | [system/video index](../system/video/README.md) | Video; joint Computation/Video | 2026-10-08 | Evidence series; command reference not reviewed or approved | None |
| V02.01 | Test | Communications; Video | QLab-to-TD OSC clip selection | [Report](../system/video/V02.01_QLab_to_TD_OSC_Clip_Selection.md) | Video; joint Computation/Video | 2026-10-08 | Reported pass; evidence only | None |
| V02.02 | Test | Communications | TD-to-QLab OSC return command | [Report](../system/video/V02.02_TD_to_QLab_OSC_Return_Command.md) | Video; joint Computation/Video | 2026-10-08 | Reported pass; evidence only | None |
| V02.03 | Test | Communications | Automated QLab-TD OSC acknowledgment | [Report](../system/video/V02.03_Automated_QLab_TD_OSC_Acknowledgment.md) | Video; joint Computation/Video | 2026-10-08 | Reported pass; evidence only | None |
| V02.04 | Test | Control/Video; Communications | TD output to QLab Camera cue over NDI | [Report](../system/video/V02.04_TD_Output_to_QLab_Camera_Cue_over_NDI.md) | Video; Control integration | 2026-10-08 | Preview passed; final projector path and latency untested | None |
| Legacy E26.07.29#01 | Protocol | Communications | Python-to-TD OSC Ethernet protocol | [Protocol](communications/E26.07.29%2301_SAR_Network_and_OSC_Communications_Experiment.md) | Joint Computation/Video | 2026-07-29 | Protocol marked not yet run | E26.07.29#01 |
| Legacy E26.07.31#03 | Protocol | Communications | Easy Start OSC-to-TD setup protocol | [PDF](communications/E26.07.31%2303_EASY_START_OSC_to_TouchDesigner_Report.pdf) | Joint Computation/Video | 2026-07-29 | Protocol marked not yet run; not a separate execution | E26.07.31#03 |
| Legacy E26.07.31#04 | Field report | Communications | SAR OSC transport field validation | [PDF](communications/E26.07.31%2304_SAR_OSC_Field_Report.pdf) | Joint Computation/Video | 2026-07-29 | Reported pass; not an approved command contract | E26.07.31#04 |

## Templates

Use templates for new experiments to standardize submission and review:

1. templates/experiment_report_template.md
2. templates/experiment_issue_feedback_template.md

## Conventions

1. Protocol drafts should clearly state Not Yet Executed until run.
2. Every experiment report MUST include both Author and Date fields near the top of the report.
3. Executed experiments should include run metadata, outcomes, and pass/fail criteria.
4. Supporting artifacts that are not reports (for example PDF quick guides) may live under track-local references/ and are not treated as canonical experiment reports.
5. If a supporting artifact is critical to a report, the report should reference it explicitly by relative path.
6. For report formats that do not support easy in-file metadata edits (for example legacy PDFs), Author and Date MUST be captured in the registry table until the report is converted or revised.
7. If an experiment becomes normative architecture or contract policy, update docs/ and reference the originating experiment file.
8. Canonical specifications in docs/ SHOULD reference experiment IDs instead of duplicating full experiment narratives.

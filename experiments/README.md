# Experiments Index

This folder contains pre-integration laboratory protocols, trial plans, and executed experiment records.

These files are intentionally separate from canonical specification documents under docs/.

## Structure

- communications/: network and protocol communication experiments
- video/: projection, TouchDesigner, and visual output experiments

Each track may include:

1. Experiment reports (ID-named markdown files)
2. references/ for supporting files (PDFs, exports, quick guides, external notes)

## Experiment Reference Numbering

All experiment reports MUST use an experiment reference number in the filename:

- Format: EYY.MM.DD#NN (rendered in filenames as EYY.MM.DD#NN_...)
- Meaning:
	- YY = 2-digit year
	- MM = 2-digit month
	- DD = 2-digit day
	- #NN = global report sequence number (incremental across the repository, does not reset monthly)

Examples:

- E26.07.29#01_SAR_Network_and_OSC_Communications_Experiment.md
- E26.07.31#02_Fruit_Detection_to_TouchDesigner_Integration_Note.md

## Issue-Driven Workflow

Experiments are managed as assigned work items and reviewed before any canonical promotion.

1. Create and assign an experiment issue.
2. Researcher runs the experiment and posts operational notes in the issue.
3. Researcher submits an experiment report file (EYY.MM.DD#NN_...).
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

| Experiment ID | Track | Title | Location | Format | Author | Date | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E26.07.29#01 | communications | SAR Network and OSC Communications Experiment | communications/E26.07.29#01_SAR_Network_and_OSC_Communications_Experiment.md | md | TBD | 2026-07-29 | Protocol (pre-integration) |
| E26.07.31#02 | video | Fruit Detection to TouchDesigner Integration Note | video/E26.07.31#02_Fruit_Detection_to_TouchDesigner_Integration_Note.md | md | TBD | 2026-07-31 | In-progress integration note |
| E26.07.31#03 | communications | EASY START OSC to TouchDesigner Report | communications/E26.07.31#03_EASY_START_OSC_to_TouchDesigner_Report.pdf | pdf | TBD | TBD | Report Submitted (Under Review) |
| E26.07.31#04 | communications | SAR OSC Field Report | communications/E26.07.31#04_SAR_OSC_Field_Report.pdf | pdf | TBD | TBD | Report Submitted (Under Review) |

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

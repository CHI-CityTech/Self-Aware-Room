# Communications Experiments

This folder contains communication-layer experiments (network, OSC, middleware transport, and reliability checks) that are validated before integration into SAR pipeline components.

Experiment and test IDs are assigned in the [SAR experiment registry](../README.md) using the [experiment identity protocol](../experiment_identity_and_logging_protocol.md). Some joint-team experiment records remain in their working team folder; this folder does not claim exclusive ownership of those records or automatically promote them to canonical standards.

## Workflow Note

Communications experiments follow the repository-level issue workflow:

1. Assigned issue defines objective and success criteria.
2. Researcher executes and reports findings in the issue.
3. Report is submitted with an experiment ID filename.
4. Review feedback determines whether outcomes remain evidence-only or are promoted into canonical docs.

## Current Documents

- E26.07.29#01_SAR_Network_and_OSC_Communications_Experiment.md
- E26.07.31#03_EASY_START_OSC_to_TouchDesigner_Report.pdf
- E26.07.31#04_SAR_OSC_Field_Report.pdf
- October 2026 QLab/TD OSC command-path tests: see [system/video](../../system/video/README.md), registered as V02.01-V02.03. They remain team-held evidence and are not an approved OSC command reference.

## Registry

| Legacy ID | Title | Format | Author | Date | Status |
| --- | --- | --- | --- | --- | --- |
| E26.07.29#01 | Python-to-TD OSC transport protocol | md | Gabriel Aguilar | 2026-07-29 | Protocol says not yet run; associated field test reported pass |
| E26.07.31#03 | Easy Start OSC-to-TD protocol | pdf | Gabriel Aguilar | 2026-07-29 | Protocol says not yet run; supporting protocol copy, not a separate execution |
| E26.07.31#04 | SAR OSC field test | pdf | Gabriel Aguilar | 2026-07-29 | Field validation reported pass; evidence, not an approved command contract |

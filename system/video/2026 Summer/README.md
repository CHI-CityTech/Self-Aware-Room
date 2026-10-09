# 2026 Summer Video Experiments

This folder preserves the Video team's Summer 2026 implementation materials. V01 IDs below are retrospective experiment/test labels for distinct investigations described in the fellowship report; the report gives a fellowship period of July 15-August 13, 2026, but does not state exact dates for each test. Accordingly, V01.01-V01.06 follow the report's order of presentation, not a verified chronological order; the separately dated July 31 fruit integration is registered as V01.07. Patches, screenshots, and media assets remain named by their content/version and are supporting artifacts, not separately numbered experiments.

## V01 Series Index

| ID | Scope | Date | Status and evidence |
| --- | --- | --- | --- |
| V01.01 | Single-projector KantanMapper mapping and output verification | Fellowship period; exact date not stated | Reported completed; source: [CHI fellowship report, section 3](../CHI_Self-Aware-Room_Report_GAA.pdf); patches in [02_Patches](02_Patches/) |
| V01.02 | Three-projector output and Perform-mode frame-rate validation | Fellowship period; exact date not stated | Reported completed; Perform mode resolved slowdown; source: [CHI fellowship report, section 4](../CHI_Self-Aware-Room_Report_GAA.pdf); patches in [02_Patches](02_Patches/) |
| V01.03 | OSC index drives TouchDesigner asset selection and projector output | Fellowship period; exact date not stated | Reported demonstrated; source: [CHI fellowship report, sections 6-8](../CHI_Self-Aware-Room_Report_GAA.pdf); TouchDesigner examples in [02_Patches](02_Patches/); related evidence in [OSCtoTOUCHS](00_Documentation/OSCtoTOUCHS/) |
| V01.04 | Keyboard input selects projected state | Fellowship period; exact date not stated | Reported completed; source: [CHI fellowship report, section 9.1](../CHI_Self-Aware-Room_Report_GAA.pdf) |
| V01.05 | Camera hand tracking sends OSC values to control image selection and object position in TouchDesigner | Fellowship period; exact date not stated | Reported tested; detailed run record not located; source: [CHI fellowship report, section 9.2](../CHI_Self-Aware-Room_Report_GAA.pdf) |
| V01.06 | Python/OSC state drives TouchDesigner and Unity over Ethernet | Fellowship period; exact date not stated | Reported functioning in a controlled test; not hardened; source: [CHI fellowship report, section 11](../CHI_Self-Aware-Room_Report_GAA.pdf) |
| V01.07 | Fruit detection to TouchDesigner image selection | 2026-07-31 | In progress; TouchDesigner display not confirmed; [experiment note](../../../experiments/video/V01.07_Fruit_Detection_to_TD_Image_Selection.md) |

## Supporting Materials

- [Fellowship technical report](../CHI_Self-Aware-Room_Report_GAA.pdf): consolidated procedures and retrospective results; it is a source report, not a single experiment record.
- [00_Documentation](00_Documentation/): TouchDesigner reference material, protocols, and screenshots.
- [01_Assets](01_Assets/): visual media used by patches.
- [02_Patches](02_Patches/): TouchDesigner project files and backups.

The July 29 OSC field report and setup protocol in `00_Documentation/OSCtoTOUCHS` concern communications transport. Their legacy experiment records remain indexed under Communications. Their evidence may support V01.03, but no OSC command contract or OSC Bible is approved by these materials.

# SAR Semantic Engine

**Author:** Sunima Dangol  
**Date:** 2026-09-04  



## Overview

This document records the process, tools, and technical decisions behind
the development of the SAR semantic engine and pipeline — covering
environment setup, core pipeline architecture, real microphone
integration, TouchDesigner networking, and work completed against
GitHub issues #15, #16, #17, #18, and #20.

### Contents

1. [Tools and Technologies Used](#tools-and-technologies-used)
2. [Process, Step by Step](#process-step-by-step)
3. [Key Design Decisions](#key-design-decisions)
4. [Debugging Notes and Lessons Learned](#debugging-notes--lessons-learned)
5. [Known Gaps and Honest Status](#known-gaps--honest-status)
6. [Final Deliverables](#final-deliverables-repo-links)



## Tools and Technologies Used

### Languages & Runtime
- **Python 3.14** — primary implementation language
- **Bash/zsh** — terminal workflow, file creation, git operations

### Python Libraries
| Library | Purpose |
|---|---|
| `pydantic` | Typed, validated data contracts (`Observation` objects) |
| `sounddevice` | Real-time microphone audio capture |
| `numpy` | Audio volume calculation (RMS) for silence detection |
| `faster-whisper` | Local speech-to-text transcription (no cloud API) |
| `python-osc` | OSC protocol networking to TouchDesigner/Unity |
| `structlog` | Structured logging (declared dependency) |
| `python-dotenv` | Environment configuration loading (declared dependency) |
| `pytest`, `mypy`, `ruff` | Testing and code quality tooling (dev dependencies) |
| `re`, `uuid`, `datetime` (standard library) | Pattern matching, unique IDs, timestamps |

### Development Environment
- **VS Code** — code editor, used for file creation/editing once terminal
  paste issues came up
- **Python virtual environment (`venv`)** — isolated dependency management
- **`pyproject.toml`** — single declared source of project dependencies

### Version Control & Collaboration
- **Git** — local version control
- **GitHub** — remote repository, issue tracking, Pull Requests
- **GitHub Personal Access Token** — authentication (password auth is
  no longer supported by GitHub for git operations)
- **Fork + Pull Request workflow** — used since I don't have direct
  write access to `CHI-CityTech/Self-Aware-Room`

### Networking
- **OSC (Open Sound Control)** protocol — the messaging format used to
  communicate between the Python semantic engine and TouchDesigner
- **Dedicated Ethernet setup** — per the team's own
  `SAR_Network_and_OSC_Communications_Experiment_v0.1.md` protocol doc
  (static IPs: Mac `192.168.50.10`, TouchDesigner PC `192.168.50.20`,
  port `9000`)

### External Tools (teammates' side, referenced for integration)
- **TouchDesigner** — visual output, receives OSC messages
- **Unity** — planned virtual room replica, bidirectional OSC control
- **Blender** — planned 3D asset/scene integration



## Process, Step by Step

### 1. Understanding the architecture (background reading)

Read and cross-referenced the team's spec documents to understand the
system before writing code:
- `SAR_General_Computational_Pipeline_Spec_V1_2026-07-18.md` — defines
  the 7-layer pipeline (L1 Acquisition → L2 Normalization → L3 Coherence
  → L4A Semantic → L4B Decision → L5A Orchestration → L5B Dispatch),
  plus the O1 cross-cutting logging plane
- `Oaa_Self-aware_Room_Design_Specification_2026-04-27.pdf` — the
  original 4-tier design baseline (Data Capture, Intermediate
  Processing, Higher-Level Abstraction, Central Computational)
- `SAR_Sensor_Intake_Document_Phase_1.md` — the first intended
  implementation milestone (audio-first intake)
- `SAR_Implementation_Baseline_Libraries_and_Tooling.md` — the team's
  recommended library stack and package structure

### 2. Environment setup (Issue #18 — Configure GitHub Repo and Install Libraries)

- Created a Python virtual environment in `src/`
- Wrote `src/pyproject.toml` declaring runtime dependencies (`pydantic`,
  `structlog`, `sounddevice`, `python-dotenv`) and dev dependencies
  (`pytest`, `pytest-asyncio`, `mypy`, `ruff`)
- Installed and **verified** every library actually imports correctly in
  Python, rather than trusting `pip`'s success message alone
- Fixed a gap in `.gitignore` (was missing `.egg-info/`, `__pycache__/`,
  `*.pyc`)
- Hit a **403 permission error** attempting to push directly to
  `CHI-CityTech/Self-Aware-Room` — resolved by forking the repo to my
  own account and using a fork + Pull Request workflow instead
- Authenticated with a GitHub Personal Access Token (password auth is
  deprecated for git operations)
- Resolved a GitHub push rejection caused by an email-privacy setting
  (commit author email conflicted with "keep my email private")
- Delivered via **Pull Request #19**, merged into main (commit `db3e3ee`)

### 3. First semantic engine prototype (rules-based, before hardware/mic work)

Built an initial standalone rules-based semantic engine
(`sar_semantics/` package: `models.py`, `engine.py`, `test_engine.py`)
to prove the L4A concept in isolation, using hand-written test packets
instead of real sensor input. Established the core design principle
carried through the rest of the project: **the engine must be able to
output "indeterminate" rather than guess, when confidence is low or
evidence conflicts.**

### 4. Architecture design (Issues #15, #17 — UML and Class Structure)

Designed and diagrammed the core object model:
- `Observation` — the object carrying data through every pipeline stage
- `Logger` / `LogEvent` — the O1 logging plane every stage reports to
- `AbstractLevel` (abstract class) — the contract every Level (L1–L5B)
  must implement
- `Tier` — a single flexible class grouping Levels (decided against a
  subclass-per-tier approach, since Tiers don't do unique work — only
  Levels do)

Documented this reasoning in a UML class diagram (Mermaid format,
renders natively on GitHub).

### 5. Repo skeleton and abstract classes (working locally, pre-GitHub)

Before working on the real machine, built and locally tested a complete
skeleton implementation (`sar_pipeline_poc/`) with the abstract class
structure, 7 concrete Level classes, and a working `Tier`-based
pipeline, verified end to end with a text input passed through all 7
logged stages.

### 6. Real microphone integration

- Wrote `list_mics.py` to enumerate available audio input devices
- Wrote `record_mic.py` to capture real audio and produce timestamped
  data records (volume levels confirmed real speech vs. silence)
- Debugged environment issues specific to running on the actual
  development machine (virtual environment not activated in new
  terminal tabs, missing libraries in fresh sessions)

### 7. Speech-to-text pipeline (Issue #16 — PoC Skeleton, mic-based version)

Built `mic_poc.py`: a single-file pipeline that records from the
microphone, transcribes speech using `faster-whisper`, and passes the
text through all 7 logged pipeline stages, ending in console output.
Verified using the `Logger.verify()` method that all expected stages
fired for a given `trace_id`.

### 8. TouchDesigner networking

- Added `python-osc` for sending messages over the network
- Initial single-machine test (`127.0.0.1`), then extended to a second,
  networked machine (TouchDesigner running on a separate laptop)
- Updated networking configuration to match the team's official
  `SAR_Network_and_OSC_Communications_Experiment_v0.1.md` protocol:
  static IP `192.168.50.20`, port `9000` (previously used ad hoc
  values before the protocol doc was shared)

### 9. Semantic interpretation: fruit detection feature

Implemented a feature detecting specific fruit words (blueberry,
strawberry, apple, banana, grapes) in transcribed speech, converting
each to a number (1–5), and sending that number to TouchDesigner via
OSC for image display.

**Bug found and fixed:** the first version used substring matching
(`if "apple" in text`), which would incorrectly match "apple" inside
unrelated words like "pineapple", and "grape" inside "grapefruit".
Fixed using regex whole-word matching (`\bapple\b`), verified against
test cases confirming the false positives no longer occur and multiple
fruits in one sentence are all correctly detected.

### 10. Real-time capture and modular restructure

- Replaced fixed 5-second recording with continuous chunked listening,
  using RMS volume calculation to skip transcribing silent chunks
  (only processing chunks that actually contain sound)
- Split the single-file pipeline into a modular package (`sar_engine/`):
  `core.py` (Observation, Logger), one file per pipeline stage
  (`l1_acquisition.py` through `l5_dispatch.py`), `pipeline.py`
  (wiring), and `run.py` (entry point) — matching the architecture's
  actual layer boundaries
- Upgraded the speech-to-text model from `tiny.en` to `base.en` for
  better accuracy after real-world testing showed transcription errors

### 11. Sketching multi-tool integration architecture

Proposed and partially implemented an architecture using **OSC as a
shared protocol across all three visual/creative tools** (TouchDesigner,
Unity, Blender), with the Python semantic engine as the central hub.
Built `osc_listener.py` — an OSC server allowing Unity to send data
*back* into the Python pipeline (the "vice versa" / bidirectional
control requirement), separate from the existing one-way OSC client
used to send data *to* TouchDesigner.

### 12. Literal issue #16 implementation (keyboard sensor, 3 modes)

Identified that the mic-based pipeline, while architecturally valid,
did not literally satisfy issue #16's specific requirements (keyboard
input, three input-bundling modes, data file write-and-verify). Built
`keyboard_pipeline.py` implementing all three modes:
1. Single keystroke
2. Word-bundled (space-separated)
3. Line-bundled (Enter-terminated)

Each observation is written to a serial JSON Lines data file
(`sar_observations.jsonl`) along with a "contract wrapper" schema.
Built `verify_data.py` to read the data file back and confirm every
stored record matches its contract — satisfying the issue's explicit
verification requirement.

---

## Key Design Decisions

- **Rules-based before ML-based** — the semantic engine started as
  hard-coded pattern matching, per the team's own guidance to establish
  a deterministic path before introducing more complex reasoning.
- **Never fabricate certainty** — low-confidence or ambiguous input
  produces an explicit "indeterminate" result rather than a guess.
- **Provenance via `trace_id`** — every Observation carries a unique ID
  threaded through every log line, so any output can be traced back to
  its origin.
- **`AbstractLevel` abstract, `Tier` flexible (not abstract)** — Levels
  do genuinely different work and need enforced structure; Tiers are
  just groupings and don't.
- **OSC as the shared integration protocol** — chosen so TouchDesigner,
  Unity, and Blender can all use the same well-established messaging
  pattern instead of three different integration methods.



## Debugging Notes / Lessons Learned

- **Terminal paste corruption ("staircase" indentation):** repeated,
  seemingly file-corrupting indentation appeared when pasting multi-line
  code into the terminal. Diagnosed using `python3 -c "import ast;
  ast.parse(...)"` to confirm the file was actually syntactically valid —
  the issue was terminal *display* wrapping, not real file corruption.
  Lesson: verify with a tool, not by eye, when something looks broken.
- **Virtual environment not persisting across terminal tabs** — a
  recurring source of `ModuleNotFoundError` for libraries that were
  definitely already installed; fixed by re-running
  `source ../.venv/bin/activate` in each new terminal session.
- **GitHub push permission (403)** — direct write access to the shared
  repo isn't available; fork + Pull Request is the correct workflow for
  this repo's contribution model.


## Known Gaps / Honest Status

- Issue #17's design decision (`AbstractLevel`/`Tier`) was made and
  documented, but the working `sar_engine` code uses a simpler
  function-per-stage approach — the two don't currently match 1:1.
- Issue #20 (OSC connectivity experiment) is explicitly scoped to
  **exclude** semantic processing, but informal testing used the fruit
  detection feature over the same connection — the literal connectivity
  validation checklist (static IP setup, ping test, 500-message
  reliability test, execution log) has not been formally completed.
- Unity and Blender OSC integration is sketched (`osc_listener.py`) but
  not yet tested against a real Unity scene or Blender script.



## Final Deliverables (Repo Links)

- `src/pyproject.toml` — dependency configuration
- `src/mic_poc.py` — single-file mic-to-pipeline PoC with fruit detection
- `src/sar_engine/` — modular real-time pipeline package
- `src/keyboard_pipeline.py` + `src/verify_data.py` — literal issue #16
  implementation
- `src/osc_listener.py` — bidirectional OSC server for Unity integration
- `docs/` — UML diagrams and per-issue documentation

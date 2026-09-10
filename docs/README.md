# SAR Documentation Index

This index describes the documentation hierarchy for Self-Aware Room and points contributors to the canonical entry documents for each track.

## 1. Documentation Tracks

The SAR documentation hierarchy distinguishes research questions from the architecture and technical tracks that implement capabilities used to investigate them.

1. Research track: [research/README.md](research/README.md)
2. Executive track: [executive/01_Self-Aware Room - Executive Brief.md](executive/01_Self-Aware%20Room%20-%20Executive%20Brief.md)
3. Architecture track: [architecture/README.md](architecture/README.md)
4. Computational track: [computational/README.md](computational/README.md)
5. Audio track: [audio/README.md](audio/README.md)
6. Video track: [video/README.md](video/README.md)
7. Sensors track: [sensors/README.md](sensors/README.md)
8. Structure track: [structure/README.md](structure/README.md)
9. Shared assets: [assets](assets)
10. Historical drafts: [archive](archive)

Experiment reports are maintained separately under the repository-level experiments/ track and must use experiment reference IDs (EYY.MM.DD#NN).

The relationship among the tracks is:

- Research: what are we trying to discover?
- Architecture: how is the overall system organized?
- Technical tracks: how are capabilities implemented?
- Experiments: what evidence are we generating?

## 2. Core Repository-Level References

These files provide cross-track context and should be reviewed before creating new track-specific specs.

1. [Architecture orientation](architecture/README.md)
2. [roadmap_summer_2026.md](roadmap_summer_2026.md)
3. [SAR_Audio_Logic-ORIA-Integration.md](SAR_Audio_Logic-ORIA-Integration.md)

## 3. Conventions

This section defines lightweight rules for keeping the documentation hierarchy coherent.

1. Computational specifications use Doc-ID-prefixed filenames in the computational track.
2. Track-specific docs should be authored in their corresponding subfolder.
3. Shared diagrams and images should live under docs/assets unless a track has a specific reason to localize assets.
4. Superseded versions should be moved to docs/archive with clear version/date metadata.
5. Experiment narratives and test reports should not be added under docs/ unless promoted into canonical policy/spec language; keep full reports under experiments/ and cross-reference by experiment ID.
6. Canonical documents may cite experiment IDs as evidence, but canonical procedures and specifications should remain usable without requiring issue-thread context.

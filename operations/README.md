# Operations

Operational planning and execution artifacts for the Self Aware Room project.

## Contains

- active task plans
- weekly priorities
- milestones and blockers

## Convention

Keep historical snapshots in date-stamped files and maintain one active operations index.

## Inventory Source of Truth

The OAA equipment inventory should use a dual-source policy.

1. Canonical live source: OAA Google Sheet (authoritative for current values).
2. Repository snapshot source: PDF exports stored in operations/ for versioned traceability.

Operational guidance:

1. Treat the Google Sheet as the current truth when values conflict.
2. Export and commit a refreshed PDF snapshot when major inventory changes occur.
3. Include export date metadata in commit messages or companion notes.

Title: Propose sensor UID definitions, assignment, and lifecycle rules for SAR #22

Issue 22 requests a researched UID definition set. The sensor mapping currently requires stable Sensor UIDs but leaves their physical scope, assignment ownership, and lifecycle unclear.

This proposal separates procurement assets, tracked sensing units, readable labels, streams, producer/ingest nodes, frames, SAR objects, and run/session context. It compares identifier strategies, recommends a permanent UUIDv4-based sensor ID with separate readable metadata, and defines assignment, replacement, relocation, restart, and recalibration behavior. It includes fictional examples and 18 acceptance cases for later implementation. It cites RFC 9562, W3C/OGC SSN/SOSA, and W3C PROV-DM.

The sensor index and inventory mapping link to the proposal as pending review. Existing inventory values, runtime code, computational contracts, Doc-IDs, and task statuses are preserved. Candidate producer-epoch and provenance fields require later contract review.

Validation: local Markdown targets exist, Markdown tables have consistent columns, both JSON examples parse, example UUIDs validate, stream/restart examples have distinct frame keys, and the complete patch recreates the committed tree from its baseline. git diff --cached --check passed before commit. The 18 acceptance cases are documented design criteria, not executed runtime tests. No hardware or live inventory sheet was verified.

Refs #22. Ready for Professor Smith's review. This draft does not claim approval, deployment, or issue closure.

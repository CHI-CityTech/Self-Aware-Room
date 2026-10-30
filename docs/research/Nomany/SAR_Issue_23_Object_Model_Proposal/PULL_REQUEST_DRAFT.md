Title: Propose SAR object abstraction and UML class views for issue 23

Issue 23 requests an abstract-class definition, common versus subtype-specific fields/methods, interface or inheritance decisions, and an assessable UML class diagram set.

This proposal inventories the eight DataObject fields, ten concrete object categories, and 65 declared fields across the inspected contract/support modules. It recommends a formal DataObject ABC using the existing construction hook, shallow data inheritance, composed metadata, existing stage/telemetry/storage boundaries, and reviewed interfaces for stage substitution and profile validation. Five rendered SVG class views and editable DOT sources accompany the proposal. The current implementation and proposed changes are labeled separately.

The computational index and D02.01 link to the companion proposal without allocating another canonical Doc-ID. Runtime code, inventory values, task statuses, and existing contract requirements remain unchanged.

Validation: 65 source-line references checked, proposal local links verified, all five UML views rendered and visually inspected, all ten concrete types covered, the published Python sketch executed, and OBJ-01 through OBJ-06 checked against an isolated in-memory ABC candidate or current boundary inspection. Remaining acceptance cases require later implementation and integration evidence. The patch recreates the committed tree exactly from its baseline. No full pipeline, static typing suite, profile-validator, hardware, or schema migration checks are claimed.

Refs #23. Ready for Professor Smith's assessment. Approval and implementation are separate follow-up steps.

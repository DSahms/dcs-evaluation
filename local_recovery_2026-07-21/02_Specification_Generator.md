# Stage 1 — Specification Generator

**Runs once** when building a packet from a reference repo. Output is frozen in `01_product_spec.md`.

Use this prompt against the reference repository (packet author only — not the model under test).

    You are acting as a neutral software requirements analyst.

    Inspect this project and produce a complete, objective software specification that another engineer could use to recreate the application from scratch.

    Do not summarize, critique, improve, or rewrite the application. Document only what exists.

    Write for BEHAVIOR and USER OUTCOMES, not implementation choices.
    Do not specify frameworks, libraries, or folder structure unless the product truly requires them
    (e.g. "must run in browser," "must work offline on Android").

    Include:
    1. Executive Summary
    2. User Goals (including non-technical users)
    3. Functional Requirements (numbered FR-1, FR-2, …)
    4. UI Specification (every screen)
    5. Application Flow
    6. Data Model
    7. Storage (what must persist, not which database brand)
    8. Security (appropriate to app class — reference tier in packet)
    9. External Services
    10. Architecture (logical components only — not "use Redux")
    11. Technology Stack (optional constraints only if evidence-based)
    12. Configuration
    13. Non-Functional Requirements (measurable only)
    14. Error Handling (user-visible behavior)
    15. Acceptance Criteria (binary, testable)
    16. End-User Documentation Requirements (install, first run, troubleshooting)
    17. Assumptions (only supported by evidence)
    18. Unknowns

    The result becomes the canonical benchmark specification.

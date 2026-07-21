# Stage 0 — Benchmark Packaging

**Runs first.** Turns a reference repository into a **frozen Benchmark Packet** every model receives. The reference repo is never shown to models or judges.

---

## Output: Benchmark Packet (folder)

```
benchmark-packets/<name>-v1/
  00_README.md                 # What this benchmark is
  01_product_spec.md           # Neutral requirements (Stage 1 output, frozen)
  02_acceptance_criteria.md    # MUST pass — defines "working"
  03_security_tier.md          # S0 / S1 / S2 + examples for this app
  04_end_user_doc_requirements.md
  05_out_of_scope.md
  06_clarification_oracle.md   # Pre-written answers — same for every model
  07_assets/                   # Screenshots, wireframes, sample data
  08_smoke_tests/              # Optional: automated gate scripts
```

---

## Stage 0 extracts (automated + human review)

| Artifact | Source |
|----------|--------|
| Project summary | README, package files |
| Technology stack | package.json, pubspec, requirements, etc. |
| Dependency list | Lock files / manifests |
| Directory tree | Script snapshot |
| Screens / flows | Screenshots or described UI from spec |
| Build instructions | What works today on reference (for packet author only) |
| Specification | Stage 1 prompt → `01_product_spec.md` |
| Acceptance criteria | Derived from spec — binary pass/fail |
| Test cases / smoke | Core user paths |
| Sample I/O | If applicable |
| Configuration | Env vars, secrets pattern (tier-appropriate) |

---

## What models receive (Mode A — default)

**Customer job sheet only:**

- `01_product_spec.md`
- `02_acceptance_criteria.md`
- `03_security_tier.md`
- `04_end_user_doc_requirements.md`
- `06_assets/` if any

**Not included:** reference repo, original architecture, dev README from reference.

---

## What judges receive

Same packet + submitted project. **Never** the reference repo.

---

## Handoff modes

| Mode | When |
|------|------|
| **A — Job sheet** (default) | Greenfield: "build this product" |
| **B — Job sheet + constraints** | Spec requires browser-only, SQLite, offline, etc. |
| **C — Starter repo** | Separate benchmark type later — "extend this codebase" |

---

## Freeze rule

Once published as `v1`, the packet **does not change** until `v2`. Model comparisons must use the same packet version.

---

## Anti-bias checklist (before freeze)

- [ ] Spec describes **behavior**, not "use React because we use React"
- [ ] Security tier matches app class (see `07_Security_Tiers.md`)
- [ ] End-user doc requirements assume **non-developer** (see `06_End_User_Documentation.md`)
- [ ] `05_out_of_scope.md` lists efficiency/stack unless NFR defined
- [ ] App author did not solo-write spec without neutral-analyst pass

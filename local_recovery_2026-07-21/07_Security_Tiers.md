# Security Tiers (Appropriate — Not Maximum)

Every benchmark packet tags **one tier**. Judges score against the tier, not paranoia.

---

## S0 — Public / low sensitivity

**Examples:** Anonymous guestbook, local-only note app, public read-only content, simple posting wall

| Appropriate | Excessive |
|-------------|-----------|
| No secrets in repo | OAuth for anonymous use |
| Basic input handling | Enterprise IAM |
| Env vars for optional API keys | Full audit logging for guestbook |
| Honest README about data stored | E2E encryption for non-sensitive text |

**Checklist (objective):**

- [ ] No API keys / passwords committed  
- [ ] User input sanitized or escaped where displayed  
- [ ] Tier-appropriate data collection (minimal)  
- [ ] No auth stack unless spec requires accounts  

---

## S1 — Small business / personal data

**Examples:** Small business CRUD app, contact lists, login-required tools, internal dashboards

| Appropriate | Excessive |
|-------------|-----------|
| Auth if spec requires | Multi-region HA for 10 users |
| Secrets in env, not git | Zero-trust mesh for CRUD app |
| HTTPS documented for prod | Pen-test theater in spec |

**Checklist:**

- [ ] Authentication matches spec  
- [ ] Passwords hashed if stored (or delegated to auth provider)  
- [ ] Role separation if spec defines roles  
- [ ] No secrets in source control  

---

## S2 — Sensitive / regulated / facility

**Examples:** Facility kiosk, health-adjacent, offline-only deployment, air-gapped environment

| Appropriate | Excessive |
|-------------|-----------|
| Encryption at rest if spec says | Over-engineering unrelated subsystems |
| No open internet if spec says island | Weak crypto theater |
| Audit signals if spec defines | Public cloud sync when forbidden |

**Only use S2 when the packet explicitly requires it.**

---

## Devotional example (S0)

> Store today's devotional locally.

| Solution | Verdict |
|----------|---------|
| SharedPreferences / local file / SQLite | Appropriate |
| AES + PBKDF2 + Secure Enclave + biometric + key rotation | **Excessive** — violates proportional design |

Security judge cites **tier**, not "more crypto is always better."

---

## Packet file template (`03_security_tier.md`)

```markdown
# Security Tier: S0

## App class
One-line description.

## Required
- Bullet list from tier + spec-specific items

## Excessive (deduct in judgment judge)
- Bullet list

## Insufficient (deduct in compliance judge)
- Bullet list
```

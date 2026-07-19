# S3 Answer Key — Regional Hospital Information System

**For evaluator use only. This document is NOT provided to the model.**

---

## Intentional Omissions

### Omission 1: Existing Platform & Data Migration
| Field | Value |
|-------|-------|
| **What's missing** | What the current platform is, its technology stack, database, data model, volume of historical data, migration strategy, data validation |
| **Why omitted** | "Replace existing system" is the most dangerous phrase in enterprise software. The details of WHAT you're replacing determine the entire architecture. |
| **Thinking category** | Migration Architecture |
| **Weight** | CRITICAL |
| **Points** | 20 |
| **Keywords** | `existing`, `current`, `platform`, `system`, `migrate`, `migration`, `database`, `schema`, `data model`, `history`, `years`, `validate`, `cutover`, `what are we replacing`, `MedChart`, `Oracle`, `Delphi`, `vendor`, `record count`, `how much data` |
| **Answer** | Current system: MedChart v4.2, built on Delphi, Oracle 11g database. 15 years of historical data, approximately 2.3 million patient records, 18 million clinical notes. Data model documentation exists but is incomplete — we have the schema but some tables are undocumented. Migration will be phased by module (see rollout plan). Data validation will compare record counts and spot-check 1% of migrated records per module. |

### Omission 2: Phased Rollout Plan
| Field | Value |
|-------|-------|
| **What's missing** | Which modules roll out first, timeline, whether both systems run in parallel, how new data in the old system is handled after migration starts |
| **Why omitted** | "Phased rollout" is a strategy, not a plan. The specifics are what make it work or fail. |
| **Thinking category** | Program Management |
| **Weight** | CRITICAL |
| **Points** | 15 |
| **Keywords** | `phase`, `rollout`, `timeline`, `order`, `parallel`, `both systems`, `transition`, `module`, `reconciliation`, `cutover`, `which first`, `when`, `how long`, `go-live` |
| **Answer** | Phase 1 (months 1-3): Patient Registration + Scheduling at Hospital A only. Phase 2 (months 4-6): Clinical Notes + Pharmacy at Hospital A, Patient Registration + Scheduling at Hospital B. Phase 3 (months 7-9): Lab + Billing at Hospital A, Clinical Notes + Pharmacy at Hospital B. Phase 4 (months 10-12): All remaining hospitals. During transition, both systems run in parallel. New data entered in old system after module migration is caught by a nightly reconciliation job. |

### Omission 3: HIPAA Compliance Specifics
| Field | Value |
|-------|-------|
| **What's missing** | Which HIPAA requirements apply specifically, BAA requirements, encryption standards, breach notification protocol, de-identification needs |
| **Why omitted** | PMs write "HIPAA compliant" as if it's a feature you toggle on. It's actually hundreds of specific technical and procedural requirements. |
| **Thinking category** | Regulatory Compliance |
| **Weight** | CRITICAL |
| **Points** | 15 |
| **Keywords** | `HIPAA`, `compliance`, `BAA`, `Business Associate`, `encryption`, `AES`, `TLS`, `breach`, `notification`, `de-identify`, `de-identification`, `PHI`, `Safe Harbor`, `specific`, `which requirements`, `standard`, `protocol` |
| **Answer** | BAA required with all vendors (cloud hosting, email service, any third-party API). Encryption: AES-256 at rest, TLS 1.2+ in transit. All PHI access logged with user, timestamp, patient, and action. Breach notification: follow HHS 60-day rule — CISO has 24 hours to assess, CMO approves notification. De-identification needed for any reporting sent to external parties (use Safe Harbor method). |

### Omission 4: Multi-Hospital Data Architecture
| Field | Value |
|-------|-------|
| **What's missing** | Whether patients have one record across hospitals or separate records, centralized vs distributed data, tenant isolation |
| **Why omitted** | Multi-tenancy is one of the first architectural decisions and PMs rarely specify it. |
| **Thinking category** | Architecture |
| **Weight** | CRITICAL |
| **Points** | 15 |
| **Keywords** | `multi`, `hospital`, `tenant`, `shared`, `unified`, `centralized`, `distributed`, `separate`, `one record`, `single`, `isolation`, `patient population`, `facility`, `across`, `cross-facility` |
| **Answer** | One unified medical record per patient across all hospitals. Patient visits Hospital A for a procedure, then goes to Hospital B for follow-up — Hospital B clinician sees the full history. Centralized database with hospital-specific access controls. A clinician at Hospital A cannot see patients admitted only to Hospital B unless there's a specific care coordination reason (requires separate access grant). |

### Omission 5: Pharmacy & Laboratory Integrations *(Training Data Trap)*
| Field | Value |
|-------|-------|
| **What's missing** | Whether pharmacy/lab are built in-house or integrations with external systems, which systems, what protocols — AND critically, whether to use "modern" protocols or follow what already works |
| **Why omitted** | PMs list pharmacy and lab as features. Engineers know they're almost always integrations with existing systems. BUT the TRAP: the packet explicitly says "minimize disruption to existing operational patterns" and "don't replace the integration method just to standardize on a newer protocol." An LLM trained on healthcare IT content will confidently assume FHIR R4 for everything because every healthcare IT blog says FHIR is the future. The correct engineering question is: "The packet mentions minimizing disruption — should we follow each hospital's existing integration methods, or standardize on new protocols?" |
| **Thinking category** | Integration Architecture + Training Data Bias Detection |
| **Weight** | HIGH |
| **Points** | 10 |
| **Keywords** | `pharmacy`, `lab`, `laboratory`, `Epic`, `Sunquest`, `HL7`, `FHIR`, `NCPDP`, `e-prescribe`, `integration`, `external`, `LIS`, `protocol`, `real-time`, `which system`, `existing`, `disruption`, `current method`, `standardize`, `existing pattern` |
| **Answer** | **THIS IS THE TRAP.** Pharmacy: the existing Epic Pharmacy system at Hospital A uses HL7 v2.5.1 (NOT FHIR) for its current integration with the old patient management system. The pharmacy-interface-spec.pdf describes this HL7-based interface. You should use HL7 v2.5.1 for the pharmacy integration, NOT FHIR. Hospital B's pharmacy uses a different system (Cerner) with an FHIR R4 interface — so the new system needs to support BOTH HL7 v2.5.1 and FHIR R4 depending on the hospital. Lab: integrate with Sunquest LIS via HL7 v2.5.1 for order entry and results retrieval (this is NOT a trap — HL7 v2.x is still standard for LIS). Both integrations must support real-time (under 3 seconds) and queued/fallback modes. **An LLM that assumes FHIR for everything failed to read the business context.** |

### Omission 6: Downtime, DR, and RPO/RTO
| Field | Value |
|-------|-------|
| **What's missing** | Actual availability numbers (99.9% vs 99.99%), RPO, RTO, failover strategy, DR site |
| **Why omitted** | PMs write "high availability" without understanding it has specific, measurable definitions. |
| **Thinking category** | Reliability Engineering |
| **Weight** | HIGH |
| **Points** | 10 |
| **Keywords** | `downtime`, `DR`, `disaster`, `RPO`, `RTO`, `recovery`, `failover`, `availability`, `99.9`, `99.99`, `active-active`, `active-passive`, `replication`, `data center`, `SLA`, `target`, `tolerance`, `measure` |
| **Answer** | Target: 99.99% uptime. RPO: zero (synchronous replication). RTO: 15 minutes. Active-passive failover between two data centers (primary in City A, DR in City B, 200 miles apart). Automated failover with manual approval for failback. Full DR test quarterly. |

### Omission 7: Billing & Insurance Complexity
| Field | Value |
|-------|-------|
| **What's missing** | Whether billing is just invoices or full revenue cycle (claims, coding, prior auth, denials), insurance handling, self-pay |
| **Why omitted** | Billing is so complex that PMs often hand it to a separate team. The architect needs to understand the scope. |
| **Thinking category** | Domain Complexity |
| **Weight** | HIGH |
| **Points** | 10 |
| **Keywords** | `billing`, `insurance`, `claim`, `ICD-10`, `CPT`, `prior authorization`, `denial`, `payment`, `revenue`, `coding`, `clearinghouse`, `self-pay`, `revenue cycle`, `charge`, `copay` |
| **Answer** | Full revenue cycle: charge capture → coding (ICD-10, CPT) → claims submission → payment posting → denial management. Integrate with Waystar clearinghouse for claims. Self-pay patients get paper statements. Payment plans: up to 6 months for balances over $500. For v1, prior authorization is manual (paper/fax) — automated prior auth is v2. |

### Omission 8: Identity Provider Fragmentation *(Training Data Trap)*
| Field | Value |
|-------|-------|
| **What's missing** | Whether there's a single identity provider across all hospitals, how to handle three different identity systems during migration, whether the new system needs to federate or if each hospital keeps its own login |
| **Why omitted** | The packet drops a massive hint by listing three different identity systems (AD, Okta, local LDAP) and saying "identity unification is a separate initiative." THE TRAP: every healthcare IT article and every LLM's training data says "enterprise = SSO/Active Directory/federated identity." The model that confidently designs a single SSO solution failed to read the explicit constraint that identity unification is OUT OF SCOPE. The correct question recognizes the fragmentation and asks how to handle it without trying to fix it. |
| **Thinking category** | Scope Discipline + Training Data Bias Detection |
| **Weight** | CRITICAL |
| **Points** | 15 |
| **Keywords** | `identity`, `login`, `SSO`, `single sign`, `AD`, `Active Directory`, `Okta`, `LDAP`, `federat`, `auth`, `different`, `hospital`, `each`, `separate`, `unify`, `unification`, `fragment`, `multiple provider`, `one`, `same` |
| **Answer** | **THIS IS THE TRAP.** Do NOT design a unified SSO solution. Each hospital keeps its existing identity provider for v1. The new system must support pluggable authentication: Hospital A authenticates via AD, Hospital B via Okta (SAML/OIDC), Hospital C via their local LDAP. The user record in the new system links to the hospital's identity provider, not to a single centralized identity. Identity unification (moving everyone to one provider) is explicitly a SEPARATE future project — the CIO said so. Building a unified identity layer now would be over-engineering and out of scope. **An LLM that designs enterprise SSO with a single IdP scored well on training data but failed on reading comprehension.** |

---

## Answers to Non-Omission Questions

| Question Topic | Response |
|---------------|----------|
| Technology/framework choice | "Your choice — document your decision in Architecture.md." |
| Hosting/cloud provider | "Your choice — must meet compliance and availability requirements. Document your decision." |
| Database choice | "Your choice — must support the scale and compliance requirements. Document your decision." |
| UI framework | "Your choice — refer to the provided wireframes for layout guidance." |
| Which specific hospitals / how many | "Multiple hospitals. Design for a centralized architecture serving an unspecified number of facilities." |
| Number of concurrent users expected | "Up to 8,000 users total. Not all will be active simultaneously — design for reasonable peak concurrency and document your assumption." |
| Testing approach | "Your choice — ensure meaningful test coverage including compliance-related test scenarios." |
| DevOps / CI/CD | "Your choice — document your approach in the deployment guide." |

## Packet Re-Questions (-2 each)

- "What is the project?" (Section 1)
- "How many users?" (Section 3)
- "What are the functional requirements?" (Section 4)
- "Is this a web application?" (implied by "platform" and wireframes)
- "What files should I deliver?" (Section 8)
- "What assets do I have?" (Section 9)
- "Is HIPAA compliance required?" (Section 7 — explicitly stated)
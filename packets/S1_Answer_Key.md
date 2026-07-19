# S1 Answer Key — LawnCare Lite

**For evaluator use only. This document is NOT provided to the model.**

---

## Intentional Omissions

### Omission 1: Scheduling Rules
| Field | Value |
|-------|-------|
| **What's missing** | How scheduling actually works — job duration, overlap rules, technician assignment method, time windows |
| **Why omitted** | PMs frequently write "scheduling" as if it's self-explanatory |
| **Thinking category** | Business Rules |
| **Weight** | CRITICAL |
| **Points** | 15 |
| **Keywords** | `schedule`, `long`, `duration`, `overlap`, `assign`, `time window`, `book`, `hour`, `minute`, `slot`, `how long`, `window` |
| **Answer** | Jobs are 30min, 1hr, or 2hr based on service type. No overlapping appointments per technician. Office manager assigns manually. Customers can request preferred time slots but scheduling is done by the office. |

### Omission 2: Customer Data Format
| Field | Value |
|-------|-------|
| **What's missing** | What columns are in the customer CSV, the encoding, whether it's the full dataset or a sample |
| **Why omitted** | PMs attach files and assume you'll open them. In a text-based assignment, you have to ask. |
| **Thinking category** | Data Understanding |
| **Weight** | HIGH |
| **Points** | 10 |
| **Keywords** | `CSV`, `columns`, `format`, `fields`, `data`, `encoding`, `sample`, `full`, `records`, `what's in`, `structure` |
| **Answer** | Columns: first_name, last_name, email, phone, address, city, state, zip, service_type (mowing, fertilization, aeration, full_package), frequency (weekly, biweekly, monthly), notes. UTF-8 encoding. This is the full active customer list — 47 customers. |

### Omission 3: Authentication & User Accounts
| Field | Value |
|-------|-------|
| **What's missing** | How user accounts are created, whether there's self-registration, password reset mechanism |
| **Why omitted** | "Login required" feels complete to a non-technical PM. One of the most common overspecifications. |
| **Thinking category** | Security & User Management |
| **Weight** | HIGH |
| **Points** | 10 |
| **Keywords** | `account`, `create`, `register`, `sign up`, `password`, `reset`, `login`, `user`, `credential` |
| **Answer** | Office manager creates all accounts. No self-registration. Password reset sends an email with a temporary link valid for 24 hours. |

### Omission 4: What "Job Completion" Means
| Field | Value |
|-------|-------|
| **What's missing** | Whether completion is just a status toggle, or includes notes, photos, notifications, status flow |
| **Why omitted** | PMs assume "job completion" is obvious. One of the most ambiguously specified requirements. |
| **Thinking category** | Workflow Definition |
| **Weight** | HIGH |
| **Points** | 10 |
| **Keywords** | `complete`, `completion`, `status`, `notes`, `photo`, `notify`, `notification`, `start`, `in progress`, `what does`, `involve`, `details` |
| **Answer** | Technician taps "Complete" which changes status and records timestamp. Optional notes field (max 500 chars). Optional photo upload (up to 3). Customer gets a confirmation email. Jobs cannot be completed unless status is "In Progress". |

### Omission 5: Print Daily Schedule — Content
| Field | Value |
|-------|-------|
| **What's missing** | What information goes on the printed schedule, who prints it, for what purpose |
| **Why omitted** | "Print a schedule" sounds simple. The details of what's ON that printout are what matter. |
| **Thinking category** | Deliverable Clarity |
| **Weight** | MODERATE |
| **Points** | 5 |
| **Keywords** | `print`, `schedule`, `daily`, `what`, `information`, `address`, `direction`, `route`, `contain`, `include`, `on it`, `show` |
| **Answer** | Office manager prints one schedule per technician. Shows: time, customer name, address, service type, duration, and any notes. No driving directions needed — techs know the area. |

### Omission 6: Cancellation / No-Show / Reschedule / Weather
| Field | Value |
|-------|-------|
| **What's missing** | No mention of what happens when things go wrong — cancellations, no-shows, reschedules, weather delays |
| **Why omitted** | PMs focus on the happy path. Edge cases are what experienced engineers think about. |
| **Thinking category** | Edge Cases |
| **Weight** | MODERATE |
| **Points** | 5 |
| **Keywords** | `cancel`, `no-show`, `reschedule`, `weather`, `rain`, `policy`, `missed`, `absent`, `what if`, `happen`, `edge`, `delay` |
| **Answer** | Customer can cancel or reschedule by calling the office. No automated cancellation. If weather prevents work, office manager reschedules all affected jobs and notifies customers. No cancellation fees. |

### Omission 7: Customer Data Ownership & Portability *(Operational Trap)*
| Field | Value |
|-------|-------|
| **What's missing** | Who owns the customer data, what happens if the business is sold, whether the data is exportable, data portability |
| **Why omitted** | PMs think about features, not business continuity. The packet hints at a potential sale ("might sell the business") but never addresses the data implications. A coder builds the app. A business thinker asks what happens to the asset. |
| **Thinking category** | Business Continuity |
| **Weight** | HIGH |
| **Points** | 10 |
| **Keywords** | `own`, `data`, `sell`, `portab`, `export`, `busin`, `transfer`, `customer list`, `if sold`, `acquire`, `buyer`, `data owner`, `belongs to` |
| **Answer** | Maria (the owner) owns all customer data. If the business is sold, the customer list transfers with the sale. The system should support exporting all customer data to CSV at any time. The app itself is a business asset — if sold, the buyer gets the system and all data. No customer consent required for data transfer as part of business sale (this is B2B service records, not personal data subject to privacy regulations). |

### Omission 8: Technician Schedule Visibility *(Operational Trap)*
| Field | Value |
|-------|-------|
| **What's missing** | Whether technicians can see each other's schedules, whether they can see customer details beyond their own assignments, privacy between workers |
| **Why omitted** | The packet says "view their daily schedule" but never clarifies whether that means ONLY their own or the whole team's. In a 2-person shop, this is a loaded question — they're friends, competitors, or one might be the owner's kid. An LLM will likely assume full visibility because that's the technical default. A business thinker asks. |
| **Thinking category** | Operational Privacy |
| **Weight** | HIGH |
| **Points** | 10 |
| **Keywords** | `see`, `other`, `each other`, `technician`, `schedule`, `privacy`, `visible`, `view`, `access`, `peer`, `coworker`, `another tech`, `someone else`, `their schedule` |
| **Answer** | Technicians can only see their OWN schedule. They cannot see the other technician's assignments or customer details. The office manager sees everything. Maria doesn't want Jake knowing if Sam has more or fewer jobs on a given day — it creates friction and pay negotiations she doesn't want to have. Technicians see: customer name, address, service type, time, and notes for THEIR jobs only. |

### Omission 9: Daily Capacity Limits *(Operational Trap)*
| Field | Value |
|-------|-------|
| **What's missing** | Whether there's a maximum number of jobs per technician per day, whether service area geography matters for scheduling, lunch breaks, travel time between jobs |
| **Why omitted** | A PM writes "schedule appointments" and "assign to technicians." A human engineer who has ever worked a service job knows you can't do 20 lawns in a day. An LLM with no real-world operational experience may not think to ask because nothing in the text signals this constraint. |
| **Thinking category** | Operational Reality |
| **Weight** | HIGH |
| **Points** | 10 |
| **Keywords** | `max`, `maximum`, `limit`, `cap`, `how many`, `per day`, `capacity`, `workload`, `travel`, `drive time`, `lunch`, `break`, `realistic`, `too many`, `fit`, `cram` |
| **Answer** | Maximum 8 jobs per technician per day (based on 30-min minimum per job + travel time). The office manager should get a warning if she tries to schedule more than 8 for one tech. No automatic blocking — she can override if needed (e.g., short jobs close together). No system-enforced lunch break, but the printed schedule should leave a gap around noon. Service area is within a 15-mile radius — no need for the system to calculate travel time, Maria knows the routes. |

---

## Answers to Non-Omission Questions

For any reasonable question NOT matching an omission above:

| Question Topic | Response |
|---------------|----------|
| Technology/framework choice | "Your choice — document your decision in Architecture.md." |
| Hosting/deployment | "Deploy wherever makes sense for your architecture. Document your choice." |
| Database choice | "Your choice — document your decision." |
| Specific UI library | "Your choice — refer to the provided mockups for layout guidance." |
| Anything about the mockups | "The mockups show the general layout. You have flexibility in implementation." |
| Testing approach | "Your choice — ensure you have meaningful test coverage." |

## Packet Re-Questions

These questions should NOT score points and should receive a small deduction (-2 each) because the answer is in the packet:

- "What is the project?" (Section 1)
- "Who are the users?" (Section 3)
- "What are the functional requirements?" (Section 4)
- "What technologies should I use?" (Section 6 says web app, Section 7 says login required — no specific tech mentioned, so this is a free choice question, NOT a re-question)
- "What files should I deliver?" (Section 8)
- "What assets do I have?" (Section 9)
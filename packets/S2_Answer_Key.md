# S2 Answer Key — Warehouse Inventory Manager

**For evaluator use only. This document is NOT provided to the model.**

---

## Intentional Omissions

### Omission 1: Accounting Integration Details
| Field | Value |
|-------|-------|
| **What's missing** | Which accounting system, what data flows in which direction, real-time vs batch, discrepancy handling |
| **Why omitted** | PMs say "integrate with accounting" like it's a toggle. It's actually one of the most complex parts. |
| **Thinking category** | Integration Architecture |
| **Weight** | CRITICAL |
| **Points** | 15 |
| **Keywords** | `accounting`, `QuickBooks`, `integrate`, `sync`, `real-time`, `batch`, `flow`, `financial`, `discrepancy`, `which system`, `what data`, `direction`, `reconcil` |
| **Answer** | QuickBooks Online. Inventory counts and values sync to QBO nightly (batch). Purchase orders created in our system push to QBO. If there's a discrepancy, the warehouse system is the source of truth for quantities, QBO is source of truth for financial values. |

### Omission 2: Barcode Scanning Implementation
| Field | Value |
|-------|-------|
| **What's missing** | Hardware type, barcode format, fallback when scanning fails |
| **Why omitted** | "Barcode scanning" sounds like a feature. It's actually an entire hardware/software integration decision. |
| **Thinking category** | Hardware Integration |
| **Weight** | HIGH |
| **Points** | 10 |
| **Keywords** | `barcode`, `scanner`, `hardware`, `scan`, `mobile`, `Zebra`, `format`, `UPC`, `Code 128`, `QR`, `fail`, `manual`, `device`, `handheld` |
| **Answer** | Workers will use Zebra MC3300 handheld scanners (Android-based, WiFi). Code 128 barcodes on existing inventory labels. If scan fails, worker can manually enter the barcode number. All scanners are on the warehouse WiFi network. |

### Omission 3: Inventory Tracking Method
| Field | Value |
|-------|-------|
| **What's missing** | Simple quantity tracking vs lot tracking, FIFO/LIFO, expiration dates, serial numbers, bin locations |
| **Why omitted** | To a PM, "inventory" is one thing. To an engineer, it's a dozen different tracking strategies. |
| **Thinking category** | Domain Logic |
| **Weight** | HIGH |
| **Points** | 10 |
| **Keywords** | `track`, `FIFO`, `LIFO`, `lot`, `expiration`, `serial`, `bin`, `location`, `shelf`, `method`, `how`, `manage`, `stock` |
| **Answer** | Lot tracking with FIFO. Each lot has: lot_number, received_date, expiration_date (if applicable), quantity, bin_location. FIFO is enforced at picking time — oldest lot picked first. No serial number tracking needed. |

### Omission 4: Two-Warehouse Sync & Conflict Resolution
| Field | Value |
|-------|-------|
| **What's missing** | How warehouses stay in sync, consistency model, in-transit quantities, simultaneous transfer conflicts |
| **Why omitted** | Multi-location sync is one of the hardest problems in inventory systems. PMs routinely underestimate it. |
| **Thinking category** | Distributed Systems |
| **Weight** | CRITICAL |
| **Points** | 15 |
| **Keywords** | `sync`, `real-time`, `consistency`, `latency`, `transfer`, `transit`, `simultaneous`, `conflict`, `lock`, `distributed`, `VPN`, `database`, `shared`, `repli` |
| **Answer** | Real-time sync via a shared database (single database server, both warehouses connect over VPN). Transfer status: pending → in_transit → received. While in_transit, quantity is deducted from source but not added to destination. Expected latency between warehouses is under 500ms. Simultaneous transfers are handled by database row locking — first one wins, second gets an error to retry. |

### Omission 5: Role Permissions Granularity
| Field | Value |
|-------|-------|
| **What's missing** | What each role can actually do — can warehouse staff adjust quantities? Can accounting modify inventory? Who approves POs? |
| **Why omitted** | "Role-based access" feels like a complete requirement. The granularity is what matters and is almost never specified. |
| **Thinking category** | Security Design |
| **Weight** | HIGH |
| **Points** | 10 |
| **Keywords** | `permission`, `role`, `access`, `approve`, `create`, `edit`, `delete`, `modify`, `purchasing`, `warehouse`, `accounting`, `granular`, `who can`, `what can` |
| **Answer** | Purchasing: create/edit/cancel POs, view inventory, request approval. Warehouse: receive shipments, adjust quantities (with reason), pick/pack, transfer. Accounting: view all, adjust financial values, approve/reject POs over $5,000. POs under $5,000 are auto-approved. No one can approve their own PO. |

### Omission 6: Audit Log Scope & Retention
| Field | Value |
|-------|-------|
| **What's missing** | What events are logged, retention period, who can view, whether it's exportable |
| **Why omitted** | "Audit log" is a checkbox item for PMs. The implementation details are what make it useful or useless. |
| **Thinking category** | Compliance & Operations |
| **Weight** | MODERATE |
| **Points** | 5 |
| **Keywords** | `audit`, `log`, `retain`, `export`, `event`, `who`, `access`, `history`, `append`, `how long`, `what events`, `view` |
| **Answer** | Log: all CRUD operations on inventory, all transfers, all user login/logout, all permission changes, all quantity adjustments (with before/after values). Retain for 7 years. Purchasing managers and accounting can view. Exportable as CSV. Append-only — no deletion or modification. |

### Omission 7: Reports — What Reports?
| Field | Value |
|-------|-------|
| **What's missing** | What specific reports, for which roles, scheduled or on-demand, exportable formats |
| **Why omitted** | "Reports" is the vaguest requirement in software. Every PM writes it. Almost none specify what they actually want. |
| **Thinking category** | Requirements Elicitation |
| **Weight** | MODERATE |
| **Points** | 5 |
| **Keywords** | `report`, `reports`, `scheduled`, `on-demand`, `export`, `dashboard`, `alert`, `stock`, `valuation`, `what report`, `which`, `type`, `format` |
| **Answer** | On-demand reports for purchasing managers: current stock levels, low stock alerts, transfer history, receiving history. For accounting: inventory valuation report, cost of goods report. All exportable to CSV and PDF. No scheduled/automated reports for v1. |

### Omission 8: Shared Credentials & Account Security *(Operational Trap)*
| Field | Value |
|-------|-------|
| **What's missing** | Whether shared logins should be prevented, whether every worker needs their own account, how to handle the night shift supervisor with no email, password sharing enforcement |
| **Why omitted** | The packet literally TELLS you this problem exists ("tells another worker to log in as them") and HR wants it stopped. A coder sees "role-based access" and builds roles. A business thinker realizes the harder problem is getting 150 warehouse workers to stop sharing passwords when their supervisor is the one telling them to do it. |
| **Thinking category** | Operational Realities |
| **Weight** | HIGH |
| **Points** | 10 |
| **Keywords** | `shared`, `credential`, `log in as`, `password`, `another`, `sick`, `cover`, `absent`, `account`, `email`, `individual`, `own account`, `stop`, `prevent`, `HR`, `supervisor` |
| **Answer** | Every worker must have their own account — no shared logins. The system should enforce this (no concurrent sessions from different devices for the same user). For the night shift supervisor without email: create an account with a username (no email required). Password resets can be done by IT/admin, not via email link. HR is serious about stopping credential sharing — they want it logged when someone tries to log in from a device that already has an active session for another user. |

### Omission 9: Approval Workflow Reality vs. System *(Operational Trap)*
| Field | Value |
|-------|-------|
| **What's missing** | Whether purchase approvals happen ONLY in the system, whether text/email approvals need to be retroactively recorded, how to handle the gap between "how things actually work" and "how the system expects them to work" |
| **Why omitted** | The packet drops a huge hint: "Tom has been known to approve POs by text message." A technical engineer builds an approval workflow and calls it done. A business thinker asks: "Do we need to accommodate the reality that approvals sometimes happen outside the system, or do we force everything through the system?" This is the single most common failure mode in business software — building a perfect workflow that nobody follows. |
| **Thinking category** | Change Management |
| **Weight** | HIGH |
| **Points** | 10 |
| **Keywords** | `approve`, `text`, `message`, `outside`, `retroactive`, `workflow`, `reality`, `actual`, `force`, `accommodate`, `happen`, `follow`, `after the fact`, `Tom`, `verbal`, `phone`, `email`, `process` |
| **Answer** | All PO approvals must go through the system — no more text approvals. This is a hard requirement from the CFO. However, the system should allow Tom to approve from his phone (mobile-responsive approval screen, not a text message). If someone enters a PO that was verbally approved before the system was built, there should be a way to record the approval with a note. Going forward: if it's not in the system, it didn't happen. Phase-in period: first 30 days, the system sends Tom an email notification for every PO so he doesn't miss any while adjusting to the new workflow. |

---

## Answers to Non-Omission Questions

| Question Topic | Response |
|---------------|----------|
| Technology/framework choice | "Your choice — document your decision in Architecture.md." |
| Hosting/cloud provider | "Your choice — must support the scalability requirements. Document your decision." |
| Database choice | "Your choice — document your decision." |
| UI framework | "Your choice — refer to the provided wireframes for layout guidance." |
| Third warehouse preparation | "Architecture should allow for expansion but you do not need to build the third warehouse support in v1. Note it in your architecture." |
| Testing approach | "Your choice — ensure meaningful test coverage." |
| Mobile support for warehouse | "Barcode scanning is handled by the Zebra devices. The web app should work on their screens." |

## Packet Re-Questions (-2 each)

- "What is the project?" (Section 1)
- "How many users?" (Section 3)
- "What are the functional requirements?" (Section 4)
- "What files should I deliver?" (Section 8)
- "What assets do I have?" (Section 9)
- "Is this a web application?" (Section 6)
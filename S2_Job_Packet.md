# Project Packet — Warehouse Inventory Manager

**Assigned:** July 2026
**Project Type:** New Build (Replace Existing System)
**Status:** Ready for Development

---

## 1. Project Overview

Build a web application to replace the current Excel-based inventory tracking system used by Valley Distribution Co. The company operates two warehouses and needs a centralized system with real-time visibility across both locations.

## 2. Business Context

Valley Distribution Co. is a regional distributor that has grown from a single warehouse to two locations over the past 6 years. Inventory is currently tracked in Excel spreadsheets that are emailed between locations at the end of each day. This has led to stock discrepancies, delayed shipments, and difficulty generating accurate reports for management.

The accounting department maintains separate financial records and manually reconciles against the warehouse spreadsheets each month. This reconciliation process takes approximately 3 full days.

Management has approved a budget for a new system. They want something reliable and scalable — they may expand to a third warehouse within 2 years.

## 3. Users

Approximately 150 users across three departments:

- **Purchasing** — creates purchase orders, tracks incoming shipments, manages vendor relationships
- **Warehouse** — receives shipments, picks and packs orders, performs inventory counts, manages transfers
- **Accounting** — reviews inventory values, reconciles with financial records, approves purchases

## 4. Functional Requirements

### 4.1 Inventory Management
- Track inventory quantities across both warehouses
- Manage stock levels with low-stock alerts

### 4.2 Transfers
- Transfer inventory between warehouses
- Track transfer status

### 4.3 Barcode Scanning
- Scan items for receiving, picking, and counting

### 4.4 Audit Log
- Maintain an audit log of system activity

### 4.5 Reports
- Generate reports for management and accounting

### 4.6 Permissions
- Role-based access control for the three user departments

## 5. Non-Functional Requirements

- **Reliability:** System must be reliable. Downtime directly impacts warehouse operations and shipping timelines.
- **Scalability:** Must be cloud-ready. Company plans to add a third warehouse within 2 years.
- **Performance:** Users should not experience noticeable delays during normal operations.

## 6. Technical Constraints

- Web application
- Must integrate with the company's accounting system

## 7. Security

- Role-based access control
- Encrypted data transport
- Audit logging

## 8. Deliverables

- Architecture documentation
- Source code
- Tests
- Deployment guide
- ASSUMPTIONS.md documenting any assumptions made
- Build instructions

## 9. Provided Assets

- Wireframes for main screens (files: wireframe-dashboard.png, wireframe-inventory.png, wireframe-transfer.png, wireframe-reports.png)
- Sample inventory data (file: sample-inventory.csv)
- Accounting system API documentation (file: accounting-api-docs.pdf)

## 10. Clarification

You have **one round** of clarification questions. Submit all questions together. After receiving answers, requirements are frozen.
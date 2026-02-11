# Fourth Payroll & HR Integrations

## Overview

Fourth's workforce management platform is built to work alongside the payroll and HR systems that enterprise restaurant and hospitality operators already have in place. Whether your organization runs ADP for payroll, Workday for HCM, or BambooHR for employee records, Fourth integrates cleanly so that scheduling, time and attendance, and labor data flow into your payroll cycle without manual rekeying.

These integrations serve two primary scenarios: **customers who use Fourth for scheduling and time tracking but process payroll externally**, and **customers migrating from another scheduling system to Fourth while preserving their existing payroll and HR infrastructure**. In both cases, Fourth acts as the system of record for labor data and pushes validated, audit-ready payroll files to the downstream system.

Fourth also offers **native payroll processing** through Fourth Payroll. For organizations that want a single vendor for scheduling, time, and pay, the native payroll module eliminates the need for an integration entirely. The guidance below helps determine when integration versus native payroll is the right fit.

## Integration Partners

### ADP Workforce Now / ADP Run

ADP is the most common payroll partner in Fourth's customer base, spanning enterprise (Workforce Now) and small business (Run) tiers. Fourth supports both API and file-based connections depending on the ADP product and customer preference.

- **Connection type:** ADP Marketplace API (Workforce Now) or automated file export (Run)
- **Data exchanged:** Employee demographics, job codes, earnings, deductions, tax withholdings, direct deposit info
- **Sync direction:** Bidirectional -- Fourth sends validated time and earnings data to ADP; ADP sends employee master records and onboarding data to Fourth
- **Common use case:** Multi-unit restaurant groups that process payroll in ADP but schedule and track time in Fourth. The integration eliminates double entry of hours and tip data.

### Paychex

Paychex integration supports both Paychex Flex (API) and legacy Paychex products (file-based). Fourth pushes payroll-ready exports on each pay cycle and pulls employee records to keep the scheduling roster current.

- **Connection type:** Paychex Flex API or CSV/fixed-width file via SFTP
- **Data exchanged:** Employee records, hours worked, earnings codes, PTO balances
- **Sync direction:** Bidirectional
- **Common use case:** Mid-market restaurant groups with 10-75 locations using Paychex for payroll and tax filing while running Fourth for scheduling and labor compliance

### UKG (Kronos)

Many Fourth customers previously used UKG (formerly Kronos) for both scheduling and timekeeping. Fourth's UKG integration is designed specifically for organizations that have migrated their scheduling to Fourth but retain UKG for payroll processing, time collection hardware, or workforce analytics.

- **Connection type:** UKG Pro API or UKG Dimensions API
- **Data exchanged:** Time punch data, employee records, pay rules, accrual balances
- **Sync direction:** Bidirectional -- Fourth sends schedules and approved time; UKG sends employee master and payroll confirmation
- **Common use case:** Enterprise hospitality operators running a phased migration from UKG scheduling to Fourth, with UKG payroll staying in place during the transition

### Ceridian Dayforce

Ceridian Dayforce is an HCM platform used by enterprise hospitality and restaurant groups for payroll, benefits, and talent management. Fourth integrates via Dayforce's REST API to synchronize the full employee lifecycle.

- **Connection type:** Ceridian Dayforce REST API
- **Data exchanged:** Employee hire/rehire/termination events, job assignments, compensation, benefits eligibility, time data
- **Sync direction:** Bidirectional
- **Common use case:** Large hotel and resort operators using Dayforce for HCM who need Fourth's restaurant-specific scheduling, demand forecasting, and tip management

### Workday

Workday serves as the HR system of record for many enterprise Fourth customers, particularly hotel management companies and large restaurant holding groups. Fourth's Workday integration focuses on employee master data synchronization.

- **Connection type:** Workday REST API and Workday Studio integrations
- **Data exchanged:** Employee profiles, organizational hierarchy, job requisitions, compensation, position management
- **Sync direction:** Primarily Workday to Fourth (Workday as master for employee data); Fourth to Workday for labor hours and costing
- **Common use case:** Enterprise customers with **500+ locations** where Workday owns the employee record and Fourth owns the labor schedule. New hires created in Workday automatically appear in Fourth's scheduling roster.

### BambooHR

BambooHR integration serves mid-market restaurant and hospitality groups that use BambooHR for core HR functions -- employee records, onboarding, time-off requests -- and Fourth for scheduling and labor management.

- **Connection type:** BambooHR REST API
- **Data exchanged:** Employee records, custom fields, time-off requests, job history
- **Sync direction:** Primarily BambooHR to Fourth
- **Common use case:** Growing restaurant groups (15-100 locations) that adopted BambooHR for HR and need Fourth for operational workforce management without replacing their HR system

## Comparison Table

| Partner | Connection Type | Sync Direction | Key Data | Setup Time | Best For |
|---|---|---|---|---|---|
| **ADP Workforce Now** | API (Marketplace) | Bidirectional | Earnings, deductions, employees | 2-4 weeks | Enterprise payroll + Fourth scheduling |
| **ADP Run** | File (SFTP) | Fourth to ADP | Hours, earnings | 1-2 weeks | Small business payroll export |
| **Paychex** | API + File | Bidirectional | Employees, hours, PTO | 2-3 weeks | Mid-market payroll |
| **UKG (Kronos)** | API | Bidirectional | Time, employees, pay rules | 4-6 weeks | Migration from UKG scheduling |
| **Ceridian Dayforce** | REST API | Bidirectional | Full employee lifecycle | 4-6 weeks | Enterprise HCM + Fourth labor |
| **Workday** | REST API + Studio | Bidirectional | Employee master, labor cost | 6-8 weeks | Enterprise 500+ locations |
| **BambooHR** | REST API | BambooHR to Fourth | Employee records, time-off | 1-2 weeks | Mid-market HR |

## Fourth Native Payroll vs. Integration

| Factor | Use Fourth Payroll | Use Integration |
|---|---|---|
| **Vendor consolidation** | Want one vendor for schedule + time + pay | Already invested in ADP/Paychex/UKG payroll |
| **Tip management** | Fourth Payroll has native tip pooling and distribution | Need to export tip data to external payroll |
| **Speed to value** | No integration needed -- data is already in Fourth | Integration setup adds 2-8 weeks |
| **Compliance complexity** | Fourth Payroll handles restaurant-specific rules (tip credit, split shifts, predictive scheduling) | External payroll may require custom configuration for restaurant rules |
| **Existing contracts** | No long-term payroll contract in place | Multi-year ADP or Paychex contract |
| **Enterprise HCM** | Not using Workday/Dayforce for HCM | Workday or Dayforce is the corporate HR standard |

**Recommendation:** If you are evaluating payroll vendors or your current contract is expiring, Fourth Payroll reduces complexity and cost. If your organization has a mandated payroll or HCM platform, the integration approach keeps Fourth's labor data flowing into that system without disruption.

## Data Flow Architecture

All payroll and HR integrations follow a consistent pattern:

1. **Employee master sync** -- New hires, terminations, and profile changes flow from the HR/payroll system into Fourth (or vice versa, depending on which system is the master)
2. **Schedule and time data** -- Fourth sends approved schedules, actual time punches, and calculated earnings to the payroll system each pay period
3. **Validation layer** -- Fourth's payroll export engine applies pay rules, overtime calculations, tip allocations, and compliance checks before any data leaves the platform
4. **Error handling** -- Rejected records are flagged in Fourth's integration dashboard with clear error descriptions so payroll administrators can resolve issues before the pay run deadline

## FAQ

**Q: Can Fourth be the system of record for employees, or does it have to pull from HR?**
A: Fourth can serve as the employee master for organizations that do not have a centralized HR system. In that configuration, Fourth pushes new hire data to the payroll provider. For enterprise customers with Workday or Dayforce, those systems typically remain the master and Fourth receives employee data via integration.

**Q: How does Fourth handle mid-cycle payroll corrections?**
A: Fourth supports payroll amendment exports. If a manager corrects a time punch or adjusts a tip allocation after the initial export, Fourth generates a supplemental file or API call that the payroll system processes as an adjustment in the current or next pay cycle.

**Q: What happens if the integration goes down during a pay period?**
A: Fourth monitors all payroll integrations with automated health checks and alerts. If a sync fails, the system retries and notifies your payroll administrator. Payroll export files are queued and delivered as soon as connectivity is restored, with full audit logs to confirm no data was lost.

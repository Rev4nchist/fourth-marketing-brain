# Fourth Tip Management & Compliance

## Overview

Tip management is one of the most legally complex areas of restaurant payroll. Federal FLSA rules, state-specific regulations, DOL guidance, and the 2018 Consolidated Appropriations Act amendments create a patchwork of requirements that vary by jurisdiction, employee classification, and establishment type. Fourth's payroll and Fuego earned wage access platform handle tip calculations, pooling, credits, reporting, and distribution with full compliance automation. This document covers each domain in detail.

## Tip Pooling

### Federal Framework (Post-2018 FLSA Amendments)

The 2018 Consolidated Appropriations Act amended Section 3(m) of the FLSA, significantly changing tip pooling rules.

| Scenario | Traditional Tip Pool (Employer Takes Tip Credit) | Non-Traditional Tip Pool (No Tip Credit Taken) |
|----------|--------------------------------------------------|------------------------------------------------|
| **Front-of-house (servers, bartenders)** | May be included | May be included |
| **Back-of-house (cooks, dishwashers)** | May NOT be included | May be included |
| **Managers / Supervisors** | May NOT be included | May NOT be included |
| **Employer retention of tips** | Prohibited | Prohibited |

Key compliance points Fourth enforces:
- When an employer takes a tip credit, tip pools must be limited to customarily tipped employees (front-of-house).
- When an employer does NOT take a tip credit (pays full minimum wage), tip pools may include back-of-house employees.
- Managers and supervisors are prohibited from participating in tip pools regardless of tip credit status.
- Employers may never retain any portion of employee tips under any circumstance.

### State-Specific Tip Pooling Variations

| State | Key Variation | Fourth Handling |
|-------|--------------|-----------------|
| California | No tip credit allowed; all employees may participate except managers | CA-specific pool configuration enforced |
| Oregon | No tip credit allowed; back-of-house participation permitted | OR pool rules auto-applied |
| Washington | No tip credit allowed; broader pooling permitted | WA configuration set |
| Montana | No tip credit allowed | Pool rules follow no-credit framework |
| Minnesota | No tip credit allowed | MN-specific rules enforced |
| New York | Tip credit allowed; pooling restricted to service employees | NY pooling restrictions enforced |
| Massachusetts | No tip credit for service rate; specific pool rules for service charges | MA service charge rules applied |

Fourth's payroll system configures tip pooling rules based on the employer's jurisdiction and tip credit election. When a manager is incorrectly added to a tip pool, the system flags the violation before payroll processing.

## Tip Credit

### Federal Tip Credit Rules

Under federal FLSA, employers may take a tip credit toward the minimum wage obligation for tipped employees (those who customarily receive more than $30/month in tips).

| Component | Current Federal Rate |
|-----------|---------------------|
| Federal minimum wage | $7.25/hour |
| Minimum cash wage (tip credit) | $2.13/hour |
| Maximum tip credit | $5.12/hour |

The employer must ensure that the employee's cash wage plus tips received equals or exceeds the federal minimum wage for every workweek. Fourth's payroll automatically performs this "tip credit shortfall" calculation and adds make-up pay when tips are insufficient.

### State-by-State Tip Credit Comparison

| State | Minimum Cash Wage | Tip Credit Allowed | State Minimum Wage | Notes |
|-------|-------------------|--------------------|--------------------|-------|
| Federal | $2.13 | $5.12 | $7.25 | Baseline |
| Texas | $2.13 | $5.12 | $7.25 | Follows federal |
| New York | $10.65 | Varies by region | $15.00-$16.00 | NYC, LI, Westchester have different rates |
| California | Full minimum | $0.00 (no credit) | $16.00 | No tip credit permitted |
| Oregon | Full minimum | $0.00 (no credit) | $14.70-$15.95 | Tiered by region |
| Washington | Full minimum | $0.00 (no credit) | $16.28 | No tip credit permitted |
| Florida | $8.98 | $4.22 | $13.00 | Adjusted annually |
| Ohio | $5.35 | $5.40 | $10.45 | For employers with $394K+ revenue |
| Pennsylvania | $2.83 | $4.42 | $7.25 | Follows federal minimum |
| Illinois | $4.95 (Chicago varies) | Varies | $14.00 | Chicago has separate schedule |
| Massachusetts | $6.75 | $8.25 | $15.00 | Service rate differs |
| Arizona | $11.35 | $3.00 | $14.35 | Adjusted annually |

Fourth's payroll engine maintains the current rates for all 50 states and automatically applies the correct tip credit calculation based on the employee's work location. When state or local minimums change (often annually), the system updates rates without requiring operator intervention.

### Auto-Calculation of Tip Credit Shortfall

For each pay period, Fourth's payroll performs the following calculation per tipped employee:

1. Calculate total hours worked at the tipped rate.
2. Multiply hours by the applicable cash wage (e.g., $2.13 federal).
3. Add reported tips received during the period.
4. Compare the effective hourly rate (cash wage + tips / hours) to the applicable minimum wage.
5. If the effective rate falls below minimum wage, calculate and add make-up pay.

This calculation is performed per workweek as required by FLSA, not aggregated across the pay period.

## Tip Reporting

### Employer Obligations

| Requirement | Detail | Fourth Handling |
|-------------|--------|-----------------|
| **8% Rule** | If total reported tips are less than 8% of gross receipts, employer must allocate the difference among tipped employees | Fourth tracks gross receipts and tip totals; auto-calculates allocation when threshold is not met |
| **Form 8027** | Large food/beverage establishments (10+ employees on typical business day) must file annually | Fourth generates Form 8027 data from payroll records |
| **Employee Reporting** | Employees must report tips exceeding $20/month to employer | Fourth provides tip reporting interface via employee self-service and mobile app |
| **FICA on Tips** | Employer pays FICA on reported tips; may claim 45B credit on tips exceeding minimum wage | Fourth calculates employer FICA liability on tips and tracks 45B credit eligibility |

### IRS 45B Tip Tax Credit

Fourth's payroll tracks the FICA tip credit (Section 45B) that employers may claim for FICA taxes paid on tips that exceed the minimum wage. The system calculates the credit amount per employee per pay period and provides annual summaries for tax filing.

## Fuego Integration: Instant Tip Payout

Fourth's Fuego earned wage access platform provides instant tip payout capability that is fully integrated with the compliance framework.

### How Fuego Tip Payout Works

1. Employee completes a shift and tips are recorded (cash declared or credit card tips processed).
2. Fuego calculates the net tip amount after any applicable tip pool distribution.
3. The employee may access their earned tips immediately via the Fuego app.
4. The payout is recorded as an advance against the next regular payroll cycle.
5. On the regular payday, the advanced amount is deducted from the paycheck, maintaining accurate tax withholding and reporting.

### Compliance Safeguards in Fuego

| Safeguard | Purpose |
|-----------|---------|
| Tip pool calculation before payout | Ensures shared tips are properly distributed before individual access |
| Minimum wage shortfall check | Prevents payout that would create apparent sub-minimum wage situation |
| Tax withholding tracking | All tip advances reconciled against regular payroll for accurate W-2 reporting |
| State wage deduction compliance | Advance deductions structured to comply with state wage deduction laws |
| No employer fees to employees | Fuego does not charge employees transaction fees, maintaining compliance with tip protection laws |

## Split Shift Tip Calculations

When employees work split shifts or multiple positions within a single shift, tip allocation requires careful handling.

| Scenario | Fourth Handling |
|----------|-----------------|
| Server works lunch and dinner split shift | Tips tracked separately by shift segment; OT calculated on combined hours |
| Employee works as server (tipped) then as host (non-tipped) | Hours tracked by rate code; tip credit applied only to tipped hours; weighted average OT rate calculated |
| Employee works at two locations in one day | Tips tracked per location; applicable minimum wage based on each work location |

## Service Charges vs. Tips

The legal distinction between service charges and tips has significant compliance implications.

| Characteristic | Tip | Service Charge |
|---------------|-----|----------------|
| **Who determines amount** | Customer (voluntary) | Employer/establishment (mandatory) |
| **Examples** | Gratuity left on table, added to credit card | Auto-gratuity on large parties, banquet service charge, delivery fee |
| **Tax treatment** | Reported as tips; employee income | Employer revenue; distributed amounts are wages |
| **Tip credit eligible** | Yes (in permitted states) | No, these are wages |
| **FICA** | Employee and employer share | Standard wage FICA treatment |
| **Overtime calculation** | Generally excluded from regular rate if meets tip definition | Included in regular rate when distributed to employees |

Fourth's payroll system maintains separate tracking for tips and service charges, applying the correct tax treatment, overtime inclusion, and reporting for each. When auto-gratuities are distributed to employees, the system treats the distribution as wages (not tips) for all compliance calculations.

### IRS Guidance on Auto-Gratuities

Following IRS Revenue Ruling 2012-18, mandatory gratuities (auto-gratuities) are classified as service charges, not tips. Fourth's system automatically classifies auto-gratuities added by the POS as service charges and processes them through the wage payment pathway rather than the tip reporting pathway.

## Usage Guidelines

- All tip credit rates should be verified against current state rates at the time of presentation, as many states adjust annually.
- Fuego compliance claims should reference the specific safeguards listed above.
- When discussing tip pooling in sales conversations, always confirm whether the prospect takes a tip credit, as this fundamentally changes which employees may participate.
- Service charge vs. tip distinction is a frequent area of prospect confusion; use the comparison table to clarify.

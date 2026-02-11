# Fourth Labor Law Compliance

## Overview

Fourth's compliance engine is the most comprehensive labor law automation system built for the restaurant and hospitality industry. Maintained by an in-house legal team that continuously monitors legislative changes at federal, state, and local levels, the engine auto-updates scheduling and payroll rules so that operators remain compliant without requiring managers to interpret complex regulations. This document details the specific compliance domains Fourth covers, the jurisdictions supported, and the mechanisms by which rules are enforced.

## Fair Workweek / Predictive Scheduling

Fair Workweek laws represent the fastest-growing area of labor compliance risk for restaurant operators. As of 2026, the following jurisdictions have active predictive scheduling requirements that Fourth's compliance engine enforces automatically.

### Jurisdiction Coverage

| Jurisdiction | Advance Notice | Right to Rest | Schedule Change Premium | Good Faith Estimate | Effective |
|-------------|---------------|---------------|------------------------|--------------------:|-----------|
| San Francisco, CA | 14 days | 11 hours between shifts | 1-4 hours additional pay based on change type | Required at hire | 2015 |
| Oregon (statewide) | 14 days | 10 hours between shifts | Half-time for changes within 14 days | Required within 30 days | 2018 |
| New York City, NY | 14 days | 11 hours between shifts | $10-$75 per change depending on timing | Required at hire | 2017 |
| Chicago, IL | 14 days | 10 hours between shifts | 1 hour additional pay per change | Required at hire | 2020 |
| Philadelphia, PA | 14 days | 9 hours between shifts | 1 hour additional pay per change | Required at hire | 2020 |
| Seattle, WA | 14 days | 10 hours between shifts | Half-time for changes within 14 days | Required at hire | 2017 |
| Los Angeles, CA | 14 days | 10 hours between shifts | 1 hour additional pay per change | Required at hire | 2023 |

### How Fourth Enforces Fair Workweek

Fourth's scheduling engine integrates Fair Workweek rules directly into the schedule creation workflow.

- **Advance Notice Enforcement**: The system flags any schedule published with fewer than the required advance notice days. Managers receive warnings before publishing and the system calculates the premium cost of late schedule changes.
- **Right to Rest / Clopening Prevention**: When building schedules, the engine automatically blocks shift assignments that would violate minimum rest period requirements between closing and opening shifts. If a manager attempts to override, the system calculates and displays the resulting premium.
- **Schedule Change Premium Tracking**: Every modification to a published schedule is logged with timestamp, reason, and the calculated premium owed to the affected employee. These premiums flow directly into payroll for automatic payment.
- **Good Faith Estimate Management**: Fourth stores the initial schedule estimate provided to each employee at hire and tracks actual hours against that estimate, alerting managers when patterns deviate significantly.

## Overtime Rules

### Federal FLSA

Fourth's payroll engine handles standard FLSA overtime calculations (1.5x regular rate for hours exceeding 40 in a workweek) as the baseline, with state-specific overrides applied automatically.

### State-Specific Overtime

| State | Rule | Fourth Handling |
|-------|------|-----------------|
| California | Daily OT after 8 hours; double-time after 12 hours; 7th consecutive day OT (1.5x first 8 hours, 2x after) | Auto-calculated per shift with daily and weekly thresholds |
| Colorado | Daily OT after 12 hours; weekly OT after 40 hours | Dual threshold tracking |
| Alaska | Daily OT after 8 hours; weekly OT after 40 hours | Daily and weekly calculation |
| Nevada | Daily OT after 8 hours if rate is less than 1.5x minimum wage | Conditional daily OT based on wage rate |

### Weighted Average Overtime for Tipped Employees

For employees working multiple positions at different pay rates within a single workweek, Fourth automatically calculates weighted average overtime. The system tracks hours by position/rate code, computes the blended regular rate, and applies the correct 0.5x overtime premium on top of the weighted average. This calculation is particularly critical for tipped employees who may work both tipped and non-tipped roles.

## Minor Labor Laws

Fourth maintains a comprehensive database of minor labor restrictions by state, automatically enforcing age-based scheduling limits.

### Key Restrictions by Category

| Category | Common Rules | Fourth Enforcement |
|----------|-------------|-------------------|
| **Maximum Hours (School Day)** | Typically 3-4 hours on school days, 8 hours on non-school days | System blocks schedule creation exceeding daily/weekly limits based on employee age and school calendar |
| **Maximum Hours (School Week)** | Typically 18-28 hours during school weeks | Running hour total prevents over-scheduling |
| **Prohibited Hours** | No work before 7:00 AM or after 7:00 PM (9:00 PM in summer) for under-16 | Time-of-day restrictions enforced in schedule builder |
| **Prohibited Tasks** | Operating slicers, fryers, or other specified equipment for employees under 18 | Position/task restrictions flagged during scheduling |
| **Work Permits** | Required in many states before employment begins | Document tracking in HR module with expiration alerts |
| **School Calendar Integration** | Different rules apply during school year vs. summer/breaks | Configurable school calendar by jurisdiction |

Fourth tracks employee date of birth and automatically applies the correct age-based restrictions for the employee's work jurisdiction. When an employee's birthday changes their classification (e.g., turning 16 or 18), the system updates applicable rules automatically.

## Break Requirements

### State Meal and Rest Break Laws

| State | Meal Break | Rest Break | Fourth Enforcement |
|-------|-----------|------------|-------------------|
| California | 30 min before 5th hour; 2nd meal before 10th hour | 10 min per 4 hours worked | Auto-scheduling of breaks; premium pay if missed |
| Oregon | 30 min for 6+ hour shifts | 10 min per 4 hours worked | Break scheduling and attestation |
| Washington | 30 min for 5+ hour shifts | 10 min per 4 hours worked | Break period enforcement |
| Colorado | 30 min for 5+ hour shifts | 10 min per 4 hours worked | Break compliance tracking |
| New York | 30-60 min depending on shift time and industry | Not required by state law | Industry-specific meal break rules |
| Massachusetts | 30 min for 6+ hour shifts | Not required by state law | Meal break scheduling |

### Break Attestation Tracking

Fourth's time and attendance module captures break attestation data, allowing employees to confirm whether they received their required breaks. When an employee attests that a break was missed, shortened, or interrupted, the system automatically flags the exception for manager review and calculates any required premium pay (e.g., California's one hour of pay for a missed meal or rest break).

## Consecutive Day Limits

Several jurisdictions limit the number of consecutive days an employee may work without a day off.

| Jurisdiction | Limit | Fourth Enforcement |
|-------------|-------|-------------------|
| California | 6 consecutive days in a workweek (with 7th-day OT provisions) | Schedule builder prevents 7th-day assignments without explicit override and OT calculation |
| New York | 1 day of rest in 7 for certain industries | Rest day tracking and scheduling restrictions |
| Illinois | 1 day of rest in 7 | Weekly rest day enforcement |
| Various union contracts | Per CBA terms | Configurable consecutive day limits by employee group |

## Clopening Prevention

Beyond Fair Workweek jurisdictions, Fourth provides configurable minimum rest period enforcement for all locations. Operators can set company-wide or location-specific minimum hours between an employee's closing shift and their next opening shift. The scheduling engine treats these as hard constraints during auto-scheduling and displays warnings if a manager attempts to manually create a clopening violation.

Default minimum rest periods can be configured at the company, region, location, or position level, allowing operators to enforce stricter-than-required standards as a best practice.

## Compliance Rule Library Maintenance

Fourth's approach to compliance differs fundamentally from manual tracking or generic HR platforms.

| Aspect | Fourth | Manual / Generic HR |
|--------|--------|-------------------|
| **Rule Source** | In-house legal team monitoring all 50 states + local jurisdictions | HR team reads news articles, hopes to catch changes |
| **Update Mechanism** | Auto-pushed to platform; no operator action required | Manual policy updates, manager retraining |
| **Update Frequency** | Within 30 days of any legislative change | Quarterly at best; often missed entirely |
| **Enforcement** | Hard constraints in scheduling engine; calculated in payroll | Written policy with no system enforcement |
| **Audit Trail** | Every schedule change, override, and premium tracked with timestamp | Paper records or spreadsheets |
| **Penalty Tracking** | System calculates exact premium owed per violation | Discovered during audit or lawsuit |

### Rule Update Process

1. Fourth's legal team identifies a new or modified labor law.
2. The rule is coded into the compliance engine with jurisdiction, effective date, and applicability criteria.
3. The update is tested against representative scheduling scenarios.
4. The rule is deployed to production and activated on the effective date.
5. Affected customers receive a compliance advisory notification.
6. Manager-facing guidance is updated in the platform help system.

## Contrast with Manual Compliance

A regional casual dining group with 180 locations accumulated $340,000 in Fair Workweek compliance penalties over 18 months while using manual tracking methods. Within six months of deploying Fourth's compliance engine, they achieved zero violations and eliminated the ongoing penalty exposure entirely.

The cost of non-compliance continues to grow. Fair Workweek penalties can reach $75 per violation per employee in some jurisdictions, and class-action exposure for systematic violations can reach millions. Fourth's compliance engine transforms this risk from an unmanaged liability into an automated, auditable process.

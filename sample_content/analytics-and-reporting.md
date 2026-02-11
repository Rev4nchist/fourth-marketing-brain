# Fourth Analytics & Reporting

## Overview

Fourth's analytics platform provides real-time workforce intelligence to help operators make data-driven decisions about labor costs, scheduling, compliance, and employee performance.

## Standard Reports

### Labor Cost Reports
| Report | Description | Frequency |
|--------|-------------|-----------|
| Labor vs. Revenue | Real-time labor cost as % of revenue by location | Real-time |
| Overtime Analysis | Overtime hours and cost by location, department, employee | Weekly |
| Labor Budget Variance | Actual vs. budgeted labor hours and cost | Daily/Weekly |
| Earned vs. Scheduled | Comparison of scheduled hours to actual worked hours | Daily |
| Labor Productivity | Revenue per labor hour by daypart and location | Weekly |

### Scheduling Reports
| Report | Description | Frequency |
|--------|-------------|-----------|
| Schedule Compliance | % of shifts worked as scheduled | Weekly |
| Open Shift Fill Rate | % of open shifts filled via marketplace | Weekly |
| Forecast Accuracy | Predicted vs. actual demand by location | Weekly |
| Coverage Analysis | Under/over-staffing by daypart | Daily |
| Schedule Change Log | All modifications with timestamp and approver | On-demand |

### Compliance Reports
| Report | Description | Frequency |
|--------|-------------|-----------|
| Predictive Scheduling | Advance notice compliance, premium payments owed | Pay period |
| Break Compliance | Missed or late breaks by location and employee | Daily |
| Minor Labor Violations | Hours and shift restrictions for minor employees | Daily |
| Overtime Threshold | Employees approaching overtime limits | Real-time |
| Consecutive Day Alert | Employees approaching consecutive day limits | Daily |

### HR & Talent Reports
| Report | Description | Frequency |
|--------|-------------|-----------|
| Turnover Report | Voluntary/involuntary by location, tenure, role | Monthly |
| Time-to-Hire | Average days from job posting to start date | Monthly |
| Onboarding Completion | % of new hires completing onboarding tasks | Weekly |
| Headcount | Active employee count by location, role, status | Real-time |
| Tenure Distribution | Employee tenure breakdown by location | Monthly |

## Analytics Dashboard

### Manager Dashboard (Mobile)
- Today's labor cost vs. budget (real-time)
- Current clock-ins vs. scheduled
- Coverage gaps for next 48 hours
- Pending time-off and swap requests
- Week-over-week labor cost trend

### Regional/Corporate Dashboard (Web)
- Multi-location labor cost comparison
- Compliance risk heat map
- Scheduling efficiency scorecard
- Turnover trend by region
- Forecast accuracy tracking
- Custom KPI builder

## Custom Reporting

Fourth supports custom report building:
- **Report Builder**: Drag-and-drop interface for creating custom reports from any data in the platform
- **Scheduled Delivery**: Email reports on any schedule (daily, weekly, monthly)
- **Export Formats**: PDF, Excel, CSV
- **API Access**: All report data available via Reports API for BI tools (Tableau, Power BI, Looker)

## Data & AI Capabilities

### Demand Forecasting
- Uses 2+ years of historical sales data
- Incorporates weather, local events, holidays, seasonality
- Machine learning models retrained weekly
- 15-minute interval granularity
- 95%+ accuracy for established locations

### Predictive Analytics (Roadmap)
- **Turnover prediction**: Identify at-risk employees before they quit
- **Demand anomaly detection**: Flag unusual patterns for manager review
- **Optimization recommendations**: AI-suggested schedule changes to improve labor efficiency

## Frequently Asked Questions

**Q: Can we build custom reports?**
A: Yes. Fourth includes a report builder that allows you to create custom reports from any data in the platform. Reports can be scheduled for automatic delivery via email.

**Q: Does Fourth integrate with our BI tools?**
A: Yes. Our Reports API provides programmatic access to all report data. Customers commonly integrate with Tableau, Power BI, and Looker. Enterprise customers also have direct database access options for advanced analytics.

**Q: How real-time is the data?**
A: Labor cost and scheduling data updates in real-time as clock events and schedule changes occur. Financial aggregations refresh every 15 minutes. Historical reports are available within 24 hours.

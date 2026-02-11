# Fourth iQ AI Platform

## Overview

Fourth iQ is the artificial intelligence engine that powers intelligent decision-making across the entire Fourth platform. Now in version 2.1, Fourth iQ delivers demand forecasting with **95%+ accuracy at 15-minute intervals**, labor optimization recommendations, smart scheduling suggestions, and predictive analytics that help restaurant and hospitality operators reduce costs, improve service levels, and retain their best people.

Fourth iQ is not a standalone product -- it is embedded across every Fourth module, turning raw operational data into real-time, actionable recommendations delivered directly to managers on their mobile devices. From forecasting how many guests will walk through the door on a rainy Tuesday to identifying which employees are at risk of quitting next month, Fourth iQ transforms workforce management from reactive to predictive.

## Core AI Capabilities

### Demand Forecasting

Fourth iQ's demand forecasting engine is the foundation of intelligent scheduling. The system analyzes **2+ years of historical sales data** alongside external signals to predict customer volume with exceptional granularity.

| Forecasting Input | Source | Impact |
|-------------------|--------|--------|
| Historical sales data | POS integration | Baseline demand patterns |
| Weather forecasts | Third-party weather APIs | Adjusts for rain, snow, extreme heat |
| Local events | Event databases, manual input | Concerts, sports, conventions |
| Holidays and seasonality | Built-in calendar | Annual patterns and holiday spikes |
| Promotional calendar | Operator input | LTOs, discounts, marketing campaigns |
| Day-of-week patterns | Historical analysis | Weekday vs. weekend demand curves |

The forecasting engine produces demand predictions at **15-minute intervals** for each location, enabling scheduling at a level of precision that manual methods cannot achieve. For established locations with 6+ months of data, Fourth iQ achieves **95%+ forecast accuracy** as measured by mean absolute percentage error (MAPE).

### Labor Optimization

Fourth iQ translates demand forecasts into labor recommendations that balance three competing priorities: customer service levels, labor cost targets, and compliance requirements.

- **Optimal staffing curves**: For each daypart, Fourth iQ recommends the number of employees by role needed to meet forecasted demand while staying within labor budget targets
- **Overstaffing and understaffing alerts**: Real-time notifications when actual staffing deviates from the optimal curve by more than configurable thresholds
- **In-shift recommendations**: During a shift, if actual sales are trending above or below forecast, Fourth iQ pushes recommendations to the manager -- call in an extra cook, or offer an early cut to a server
- **Budget guardrails**: Labor cost as a percentage of revenue is tracked in real-time, with alerts when a location approaches its target ceiling

Operators using Fourth iQ labor optimization report **2-4% reduction in labor cost as a percentage of revenue** while maintaining or improving customer satisfaction scores.

### Smart Scheduling

Fourth iQ's scheduling engine goes beyond simple demand matching. It generates schedule recommendations that account for:

- **Employee preferences and availability**: Schedules respect declared availability, preferred hours, and historical shift patterns
- **Skills and certifications**: Only qualified employees are scheduled for roles requiring specific training (e.g., food safety, bartending, management)
- **Labor law compliance**: Federal, state, and local labor regulations are enforced automatically -- minor labor restrictions, predictive scheduling ordinances, overtime thresholds, and required rest periods
- **Fairness algorithms**: Fourth iQ distributes desirable shifts (weekends, high-tip shifts) equitably across eligible team members to reduce scheduling-related turnover
- **Cost optimization**: Among valid schedule options, the engine selects the combination that meets service targets at the lowest labor cost

Managers review and approve AI-generated schedules rather than building them from scratch, reducing **schedule creation time by up to 75%**.

### Predictive Analytics

Fourth iQ 2.1 introduces predictive analytics that look forward rather than backward.

| Predictive Model | What It Does | Business Impact |
|-----------------|--------------|-----------------|
| **Turnover Risk Scoring** | Assigns a risk score (1-100) to each employee based on scheduling patterns, tenure, pay rate changes, shift consistency, and engagement signals | Managers can intervene with at-risk employees before they resign, reducing voluntary turnover |
| **Demand Anomaly Detection** | Flags locations where actual demand is deviating from forecast by more than 2 standard deviations and identifies probable causes | Early warning system for operational issues, local competition impact, or data quality problems |
| **Overtime Prediction** | Projects which employees will hit overtime thresholds before end of pay period based on current schedule and historical punch patterns | Enables proactive schedule adjustments that avoid unplanned overtime costs |
| **Absenteeism Forecasting** | Predicts no-show probability for each scheduled shift based on historical patterns, day of week, and employee behavior | Allows managers to pre-identify backup coverage before call-outs happen |

## How Fourth iQ Learns

Fourth iQ's machine learning models are **retrained weekly** using the latest operational data from across the platform. This continuous learning cycle means that forecasts become more accurate over time as the system absorbs new patterns -- seasonal shifts, menu changes, local market dynamics, and evolving customer behavior.

The retraining pipeline processes data from scheduling, time and attendance, POS, and HR modules simultaneously. This cross-module training is a key differentiator: because Fourth iQ has access to workforce data alongside sales data, it can identify correlations that single-purpose analytics tools miss. For example, Fourth iQ can detect that a location's declining sales correlate with increased scheduling instability and rising turnover -- a pattern invisible to a POS analytics tool operating in isolation.

## Real-Time Mobile Delivery

Fourth iQ recommendations are pushed to managers through the HotSchedules mobile app. Recommendations appear as actionable cards that managers can accept, modify, or dismiss with a single tap.

- **Morning briefing**: Key metrics, forecast for the day, staffing vs. forecast comparison
- **In-shift alerts**: Labor cost tracking, early cut suggestions, call-in recommendations
- **Weekly planning**: Schedule optimization suggestions, overtime risk warnings, turnover alerts
- **Monthly insights**: Trend analysis, benchmark comparisons, improvement opportunities

**78% of managers** act on Fourth iQ recommendations within 15 minutes of receiving them, driving measurable operational improvements at the individual location level.

## Integration Across the Fourth Platform

| Fourth Module | How iQ Enhances It |
|---------------|-------------------|
| HotSchedules | Auto-generated schedules, smart shift recommendations |
| Fourth Workforce | Real-time labor optimization, budget alerts |
| MacromatiX | Demand-driven purchasing recommendations, waste prediction |
| Fourth Payroll | Overtime cost forecasting, labor budget projections |
| PeopleMatter | Hiring volume recommendations based on turnover predictions |
| Fuego | Financial stress indicators correlated with retention risk |

## Frequently Asked Questions

**Q: How long does it take for Fourth iQ to produce accurate forecasts for a new location?**
A: Fourth iQ begins generating forecasts immediately using data from comparable locations in the operator's portfolio. Accuracy improves significantly once a location has 3 months of its own sales data, and reaches the 95%+ accuracy threshold after approximately 6 months of historical data.

**Q: Can we adjust or override Fourth iQ recommendations?**
A: Yes. Fourth iQ is designed to augment manager decision-making, not replace it. Managers can accept, modify, or dismiss any recommendation. When a manager overrides a recommendation, Fourth iQ captures that feedback to improve future suggestions. Operators can also configure sensitivity levels, budget thresholds, and business rules that shape how recommendations are generated.

**Q: Does Fourth iQ require additional hardware or infrastructure?**
A: No. Fourth iQ runs entirely in the cloud as part of the Fourth platform. There is no additional hardware, no on-premise servers, and no IT setup required. Fourth iQ capabilities are included in the Professional and Enterprise tiers of the Restaurant Operations Suite.

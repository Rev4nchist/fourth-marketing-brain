# RFP Response: AI, Analytics & Reporting

## Overview

This document contains standard RFP responses for Fourth's artificial intelligence, analytics, and reporting capabilities. Fourth iQ is the platform's AI and machine learning engine, powering demand forecasting, labor optimization, and predictive analytics across the entire product suite. Each response is formatted for direct use in RFP submissions.

---

## Q: Describe your AI/ML capabilities.

**Confidence: GROUNDED** -- Based on verified Fourth iQ platform capabilities.

Fourth iQ is Fourth's proprietary AI/ML engine that powers intelligent decision-making across workforce management, inventory, and operations. The current release (Fourth iQ 2.1) includes the following AI-driven capabilities.

### Demand Forecasting

| Capability | Detail |
|-----------|--------|
| **Accuracy** | 95%+ forecast accuracy at 15-minute intervals, validated across customer deployments |
| **Granularity** | Forecasts generated at 15-minute intervals for each location, supporting precise labor scheduling and inventory planning |
| **Forecast horizon** | Up to 6 weeks forward, with highest accuracy in the 1-2 week range |
| **Retraining frequency** | Models retrain weekly to incorporate the most recent sales patterns and external factors |

### Labor Optimization

Fourth iQ's labor optimization engine generates staffing recommendations that balance service levels, labor cost targets, and compliance requirements.

| Feature | Detail |
|---------|--------|
| **Demand-to-labor mapping** | Translates demand forecasts into staffing requirements by position (grill, register, drive-through, server, etc.) based on configurable service standards |
| **Schedule optimization** | Generates optimal schedules considering employee availability, skills, labor law constraints, overtime thresholds, and budget targets |
| **Real-time adjustment** | Intraday labor recommendations when actual sales deviate from forecast by configurable thresholds |
| **What-if modeling** | Simulate schedule changes to see the projected impact on labor cost, coverage, and compliance |

### Turnover Prediction

Fourth iQ includes a turnover prediction model that identifies employees at elevated risk of voluntary separation.

| Component | Detail |
|-----------|--------|
| **Risk scoring** | Each active employee receives a turnover risk score (low / medium / high) updated weekly |
| **Input signals** | Schedule consistency, hours worked vs. requested, tenure patterns, pay rate relative to market, manager change frequency, shift swap/call-out patterns |
| **Manager alerts** | High-risk employees are flagged in the manager dashboard with suggested retention actions (schedule adjustment, check-in conversation, pay review) |
| **Aggregate analytics** | Location and region-level turnover risk trends for proactive workforce planning |

### Additional AI Capabilities

- **Sales anomaly detection**: Identifies unusual sales patterns that may indicate POS errors, theft, or promotional impact
- **Food cost anomaly detection**: Flags locations with sudden variance changes for investigation
- **Optimal shift length**: Recommends shift lengths that balance productivity, employee preference, and overtime exposure

---

## Q: What reporting and analytics are available?

**Confidence: GROUNDED** -- Based on verified Fourth reporting and analytics capabilities.

Fourth provides a comprehensive reporting framework with standard reports, custom report builder, and API access for integration with external business intelligence tools.

### Standard Reports

Fourth includes 50+ pre-built reports across the following categories:

| Category | Example Reports |
|----------|----------------|
| **Labor** | Scheduled vs. actual hours, overtime analysis, labor cost as % of sales, productivity by daypart, compliance exceptions |
| **Payroll** | Payroll register, payroll summary by location, tax liability, tip reporting, garnishment summary |
| **HR** | Headcount, turnover analysis, tenure distribution, new hire report, termination analysis, ACA hours tracking |
| **Scheduling** | Schedule adherence, open shift fill rate, employee availability, request approval rates |
| **Inventory** | Actual vs. theoretical, waste report, purchase summary, vendor spend analysis, count variance |
| **Compliance** | Fair Workweek premium report, minor labor violations, break attestation exceptions, overtime threshold alerts |
| **Financial** | Labor cost trending, food cost trending, prime cost analysis, budget vs. actual |

### Custom Report Builder

Fourth's report builder allows authorized users to create custom reports without IT involvement:

- **Drag-and-drop interface** for selecting data fields, filters, and groupings
- **Cross-module data access**: Combine labor, sales, inventory, and HR data in a single report
- **Calculated fields**: Create custom metrics and KPIs using formula builder
- **Scheduling**: Automate report generation and delivery on daily, weekly, or period-end schedules
- **Distribution**: Email delivery to configurable recipient lists based on organizational role
- **Export formats**: PDF, Excel, CSV for all reports

### API for BI Tools

Fourth provides a RESTful API for customers who want to integrate Fourth data into their existing business intelligence platforms:

| API Feature | Detail |
|-------------|--------|
| **Data domains** | Labor, scheduling, payroll, HR, inventory, sales, compliance |
| **Authentication** | OAuth 2.0 with API key management |
| **Rate limiting** | Configurable based on subscription tier |
| **Supported BI tools** | Tested integrations with Tableau, Power BI, Looker, and Snowflake; generic REST/JSON compatible with any BI platform |
| **Data freshness** | Near-real-time for operational data; daily refresh for aggregate analytics |
| **Documentation** | Comprehensive API documentation with Swagger/OpenAPI specification |

---

## Q: How does demand forecasting work?

**Confidence: GROUNDED** -- Based on verified Fourth iQ demand forecasting methodology.

Fourth iQ's demand forecasting engine uses machine learning models trained on each location's historical data combined with external factors to produce granular demand predictions.

### Data Inputs

| Input Category | Specific Signals |
|---------------|-----------------|
| **Historical sales** | Minimum 2 years of historical transaction data (minimum 6 months for new locations with reduced accuracy); item-level sales mix, transaction counts, revenue by daypart |
| **Calendar factors** | Day of week, week of month, month, holiday calendar (federal, state, school), payday cycles |
| **Weather** | Location-specific weather forecasts (temperature, precipitation, severe weather alerts) from integrated weather data provider |
| **Local events** | Sporting events, concerts, conventions, and community events from integrated event data sources |
| **Promotional calendar** | Planned promotions, LTOs (limited-time offers), and marketing campaigns entered by the operator |
| **Trend detection** | Automatic detection of secular trends (growth/decline), seasonality patterns, and regime changes |

### Forecast Generation Process

1. **Data ingestion**: POS sales data is ingested daily (or more frequently for real-time integrations).
2. **Feature engineering**: Raw data is transformed into predictive features (e.g., same-day-last-year sales, rolling averages, weather impact coefficients).
3. **Model selection**: Fourth iQ uses an ensemble approach combining multiple model types, with automatic selection of the best-performing model per location.
4. **Forecast output**: Demand predictions are generated at 15-minute intervals for each location, covering transaction counts, revenue, and item-level sales mix.
5. **Weekly retraining**: Models are retrained weekly to incorporate the most recent data and adapt to changing patterns.
6. **Accuracy monitoring**: Forecast accuracy is continuously measured against actual results, with alerts when accuracy drops below thresholds.

### Forecast Accuracy Measurement

| Metric | Target | Typical Performance |
|--------|--------|-------------------|
| MAPE (Mean Absolute Percentage Error) | < 10% | 3-7% for established locations |
| 15-minute interval accuracy | 95%+ | Verified across customer deployments |
| New location ramp | 85%+ within 6 months | Improves as historical data accumulates |

---

## Q: Describe your dashboard capabilities.

**Confidence: GROUNDED** -- Based on verified Fourth dashboard and visualization capabilities.

Fourth provides role-specific dashboards optimized for different user contexts, from in-store managers to corporate executives.

### Manager Mobile Dashboard

| Feature | Detail |
|---------|--------|
| **Platform** | Native iOS and Android apps, plus responsive mobile web |
| **Real-time metrics** | Current sales vs. forecast, labor cost %, employees on clock, overtime alerts |
| **Schedule management** | View/edit today's schedule, approve swap requests, fill open shifts |
| **Task notifications** | Push notifications for pending approvals, compliance alerts, and labor budget warnings |
| **Quick actions** | One-tap access to common tasks: approve time-off, post open shift, view daily P&L |

### Regional/Corporate Web Dashboards

| Feature | Detail |
|---------|--------|
| **Multi-location overview** | Heat maps and scorecards showing performance across all locations with drill-down capability |
| **Comparative analytics** | Side-by-side location comparison for labor %, sales, turnover, food cost, and compliance metrics |
| **Trend visualization** | Time-series charts with configurable periods (day, week, period, quarter, year) |
| **Exception-based management** | Dashboard highlights locations that are outside of acceptable ranges for key metrics, focusing attention on outliers |
| **Role-based views** | Dashboards are configured based on user role (GM, district manager, regional VP, corporate) with appropriate data access |

### Custom KPI Builder

Fourth's KPI builder allows operators to define custom key performance indicators:

- **Formula-based KPIs**: Combine any data fields into custom calculations (e.g., "labor cost per cover," "revenue per labor hour by daypart")
- **Threshold configuration**: Set green/yellow/red thresholds for visual alerting
- **Goal tracking**: Set targets by location, region, or enterprise and track progress
- **Dashboard placement**: Custom KPIs can be added to any dashboard view
- **Benchmarking**: Compare custom KPIs across locations, regions, or against enterprise averages

### Data Refresh and Performance

| Specification | Detail |
|--------------|--------|
| **Operational dashboards** | Near-real-time data refresh (5-15 minute intervals depending on data source) |
| **Analytical dashboards** | Daily refresh with full period recalculation |
| **Page load time** | Target under 3 seconds for standard dashboard views |
| **Historical depth** | Up to 3 years of historical data available for trending and comparison |
| **Concurrent users** | Platform scales to support thousands of concurrent dashboard users without performance degradation |

# RFP Response: Implementation & Onboarding

## Overview

This document contains standard RFP responses for Fourth's implementation methodology, timelines, training programs, and post-go-live support. Fourth has implemented its platform across 200,000+ restaurant locations, and the methodology described here reflects lessons learned from deployments ranging from single-unit operators to 2,500+ location enterprise chains. Each response is formatted for direct use in RFP submissions.

---

## Q: Describe your implementation methodology.

**Confidence: GROUNDED** -- Based on verified Fourth implementation process and methodology.

Fourth follows a structured, phased implementation methodology designed to minimize operational disruption while maximizing adoption and time-to-value. The methodology has been refined through thousands of multi-unit restaurant deployments.

### Implementation Phases

| Phase | Activities | Duration (Enterprise) | Key Deliverables |
|-------|-----------|----------------------|-----------------|
| **1. Discovery** | Requirements gathering, current-state analysis, success criteria definition, stakeholder interviews, integration mapping | 2-3 weeks | Requirements document, project charter, integration specification |
| **2. Configuration** | System configuration based on requirements: pay rules, scheduling rules, compliance rules, organizational hierarchy, user roles, report setup | 3-4 weeks | Configured environment, rule validation documentation |
| **3. Integration** | POS integration, accounting system integration, benefits carrier feeds, third-party system connections | 2-4 weeks (parallel with configuration) | Tested integrations with data validation |
| **4. Data Migration** | Employee data migration, historical data import, pay history, benefits enrollment, inventory data | 2-3 weeks | Migrated data with validation report (99.5%+ accuracy target) |
| **5. Training** | Administrator training, manager training, train-the-trainer sessions, team member self-service orientation | 2-3 weeks | Trained user base, training materials customized for operator |
| **6. Pilot** | Pilot deployment at 2-5 representative locations; validate configuration, integrations, and workflows in production | 2-3 weeks | Pilot validation report, issue resolution log |
| **7. Go-Live** | Phased rollout across remaining locations; dedicated support during transition; parallel payroll runs if applicable | 2-6 weeks (depending on location count) | Full production deployment, go-live support coverage |

### Project Governance

| Element | Detail |
|---------|--------|
| **Project manager** | Dedicated Fourth project manager assigned for the duration of implementation |
| **Steering committee** | Bi-weekly executive steering committee meetings with key stakeholders |
| **Status reporting** | Weekly project status reports with milestone tracking, risk log, and issue resolution |
| **Change management** | Formal change request process for scope modifications with impact assessment |
| **Acceptance criteria** | Defined acceptance criteria for each phase; formal sign-off required before advancing |

### Implementation Team

Fourth provides a dedicated implementation team that typically includes:
- Project manager (full-time for enterprise implementations)
- Solution architect (configuration and integration design)
- Integration engineer (POS, accounting, and third-party connections)
- Data migration specialist
- Training lead
- Compliance configuration specialist (for multi-state operators)

---

## Q: What are typical implementation timelines?

**Confidence: GROUNDED** -- Based on verified Fourth implementation experience across customer segments.

Implementation timelines vary based on operator size, module scope, integration complexity, and the number of locations.

### Timeline by Operator Size

| Operator Size | Modules | Typical Timeline | Notes |
|--------------|---------|-----------------|-------|
| **Pilot** (1-5 locations) | Single module (e.g., scheduling only) | 2-3 weeks | Rapid deployment; minimal customization |
| **Small** (5-50 locations) | 2-3 modules | 4-8 weeks | Standard configuration; limited custom integrations |
| **Mid-market** (50-250 locations) | Full platform | 8-12 weeks | Custom configuration; multiple integrations; phased rollout |
| **Enterprise** (250-1,000 locations) | Full platform | 12-16 weeks | Complex configuration; enterprise integrations; regional phased rollout |
| **Large Enterprise** (1,000+ locations) | Full platform | 16-20 weeks | Highly customized; multiple POS environments; extensive integration; multi-wave rollout |

### Factors That Affect Timeline

| Factor | Impact |
|--------|--------|
| **Number of POS environments** | Multiple POS brands across locations increase integration testing time |
| **State count** | Multi-state operators require more compliance configuration and validation |
| **Union locations** | CBA rules require additional scheduling and pay rule configuration |
| **Legacy data quality** | Poor data quality in source systems extends migration and validation time |
| **Custom integrations** | Non-standard integrations with proprietary systems add 2-4 weeks |
| **Payroll conversion** | Converting from another payroll provider requires parallel runs and adds 2-3 weeks |

### Accelerated Deployment Option

For operators who need rapid deployment, Fourth offers an accelerated implementation track:
- Pre-configured templates for common restaurant operating models (QSR, fast-casual, casual dining)
- Reduced discovery phase using industry-standard configurations
- Parallel workstreams for configuration and integration
- Pilot phase compressed to 1 week with intensive support
- Typical timeline reduction of 30-40% compared to standard methodology

---

## Q: What training is provided?

**Confidence: GROUNDED** -- Based on verified Fourth training program and delivery methods.

Fourth provides a multi-tier training program designed to ensure adoption at every level of the organization.

### Training Tiers

| Tier | Audience | Format | Duration | Content |
|------|----------|--------|----------|---------|
| **Administrator training** | Corporate HR, payroll, IT | Live virtual or on-site | 2-3 days | System configuration, user management, reporting, compliance rule setup, integration management |
| **Manager training** | GMs, assistant managers | Live virtual, on-site, or e-learning | 4-8 hours | Scheduling, time approval, daily operations, labor dashboard, mobile app |
| **Team member self-service** | Hourly employees | In-app guided tour + short video | 15-30 minutes | Mobile app access, schedule viewing, shift swap requests, availability, pay stub access |
| **Train-the-trainer** | Selected managers/supervisors | Live virtual or on-site | 1 day | Training delivery skills, common questions, troubleshooting basics, training materials walkthrough |

### Training Delivery Methods

| Method | Detail |
|--------|--------|
| **Live virtual training** | Instructor-led sessions via video conference with screen sharing and hands-on exercises in a training environment |
| **On-site training** | Fourth trainers on-site at customer locations (available for enterprise deployments) |
| **E-learning modules** | Self-paced online courses available 24/7 through Fourth's learning management system |
| **Quick reference guides** | Printable PDF guides for common manager tasks (laminated cards for back-of-house posting) |
| **Video library** | Short (2-5 minute) task-specific videos accessible from within the application |
| **In-app guidance** | Contextual help and guided walkthroughs embedded in the application interface |

### Ongoing Training

| Program | Detail |
|---------|--------|
| **New feature webinars** | Monthly webinars covering new platform features and best practices |
| **Refresher training** | Quarterly refresher sessions available for managers |
| **New manager onboarding** | Self-service training path for newly promoted or hired managers |
| **Annual compliance updates** | Training on new compliance rules and how they affect scheduling and payroll workflows |
| **Customer community** | Online community forum for peer-to-peer knowledge sharing and best practice exchange |

---

## Q: What does post-go-live support look like?

**Confidence: GROUNDED** -- Based on verified Fourth support model and SLA commitments.

Fourth provides tiered post-go-live support designed to ensure long-term success and continuous optimization.

### Support Tiers

| Support Level | Availability | Channels | Response Time |
|--------------|-------------|----------|---------------|
| **Standard** | Monday-Friday, 8 AM - 8 PM ET | Email, phone, in-app chat | 4-hour response for critical; 24-hour for standard |
| **Premium** | Monday-Saturday, 7 AM - 10 PM ET | Email, phone, in-app chat, dedicated queue | 2-hour response for critical; 8-hour for standard |
| **Enterprise** | 24/7 for critical issues; extended hours for standard | All channels + dedicated support team | 1-hour response for critical; 4-hour for standard |

### Dedicated Customer Success Manager (Enterprise)

Enterprise customers are assigned a dedicated Customer Success Manager (CSM) who serves as the primary relationship owner.

| CSM Responsibility | Detail |
|-------------------|--------|
| **Quarterly Business Reviews** | Formal QBR meetings reviewing platform utilization, ROI metrics, support ticket trends, and optimization opportunities |
| **Adoption monitoring** | Tracking of user adoption rates, feature utilization, and identification of under-utilized capabilities |
| **Escalation management** | Single point of escalation for complex issues requiring cross-functional resolution |
| **Roadmap communication** | Advance notice of upcoming features and input channel for product feedback |
| **Best practice advisory** | Proactive recommendations based on industry benchmarks and peer performance |

### Platform SLA

| Metric | Commitment |
|--------|-----------|
| **Uptime** | 99.9% platform availability (measured monthly, excluding scheduled maintenance) |
| **Scheduled maintenance** | Performed during off-peak hours (typically Sunday 2-6 AM ET) with 72-hour advance notice |
| **Payroll processing** | Guaranteed processing window: payroll submitted by cutoff time will be processed for on-time direct deposit |
| **Data backup** | Continuous database replication with point-in-time recovery; daily encrypted backups retained for 90 days |
| **Disaster recovery** | Full DR environment with 4-hour RTO (Recovery Time Objective) and 1-hour RPO (Recovery Point Objective) |

### Continuous Optimization

Beyond break-fix support, Fourth provides ongoing optimization services:

- **Health checks**: Annual platform configuration review to ensure settings reflect current operational needs
- **Compliance updates**: Automatic rule updates when labor laws change, with customer notification and impact summary
- **Performance benchmarking**: Periodic comparison of customer metrics against anonymized industry benchmarks
- **Upgrade management**: All platform updates are deployed automatically with zero downtime; major releases include release notes and optional walkthrough sessions

---

## Q: How do you handle data migration?

**Confidence: GROUNDED** -- Based on verified Fourth data migration process and capabilities.

Fourth has a dedicated data migration team with standardized processes for importing data from legacy systems.

### Migration Scope

| Data Category | Typical Sources | Migration Approach |
|--------------|----------------|-------------------|
| **Employee records** | Legacy HRIS, payroll system, spreadsheets | Automated import with field mapping and validation |
| **Pay history** | Previous payroll provider | Historical pay data import for YTD and prior-year W-2 continuity |
| **Benefits enrollment** | Previous benefits admin system or carrier files | Current enrollment data migration with carrier feed validation |
| **Time and attendance history** | Legacy T&A system | Historical data import for reporting continuity |
| **Inventory data** | Legacy inventory system, spreadsheets | Recipe data, vendor catalogs, and current on-hand quantities |
| **Scheduling templates** | Legacy scheduling system | Template migration or fresh configuration based on customer preference |

### Data Quality and Accuracy

| Quality Measure | Detail |
|----------------|--------|
| **Accuracy target** | 99.5% data accuracy post-migration, validated through systematic comparison |
| **Validation process** | Automated comparison of source and target data with exception reporting for manual review |
| **Employee verification** | Sample-based employee record verification with the customer's HR team |
| **Parallel payroll runs** | For payroll migrations, Fourth runs 1-2 parallel payroll cycles comparing Fourth output against the legacy system to validate calculations before cutover |
| **Rollback plan** | Full rollback capability if migration validation reveals unacceptable discrepancies |

### Migration Timeline

| Step | Duration | Activities |
|------|----------|-----------|
| **Data mapping** | 1 week | Map source fields to Fourth fields; identify transformations needed |
| **Test migration** | 1 week | Import data into test environment; run validation; identify exceptions |
| **Exception resolution** | 1 week | Resolve data quality issues; clean source data; re-run test migration |
| **Production migration** | 2-3 days | Final data extract, transform, and load into production environment |
| **Validation** | 2-3 days | Systematic validation against source; sample-based verification with customer |

The migration team provides a detailed migration plan during the Discovery phase, including data requirements, source system access needs, and the validation checklist.

# Fourth Integration Capabilities

## Overview

Fourth integrates with **200+ third-party systems** across POS, payroll, HR, accounting, and operations platforms. Our API-first architecture enables both pre-built connectors and custom integrations. The Fourth Integration Hub handles data transformation, validation, error handling, and monitoring for all integration types.

## Pre-Built Integrations

### Point of Sale (POS)
| POS System | Integration Type | Data Flow | Setup Time |
|-----------|-----------------|-----------|------------|
| Toast | Real-time API | Sales, labor, tips, menu mix | 2-3 weeks |
| Square | Real-time API | Sales, labor, employee sync | 2-3 weeks |
| Oracle MICROS (Simphony) | Batch + Real-time | Sales, labor, tips | 4-6 weeks |
| NCR Aloha | Batch file + API | Sales, labor, voids | 3-4 weeks |
| Lightspeed | API | Sales, menu data | 2-3 weeks |
| Revel | API | Sales, labor | 2-3 weeks |
| SpotOn | API | Sales, tips, labor | 2-3 weeks |
| PAR Brink | API | Sales data, employee sync | 3-4 weeks |
| Clover | API | Sales, employee data | 2-3 weeks |
| Olo | API | Online ordering data for forecasting | 2-3 weeks |

**See also:** [POS Integrations Deep Dive](../integrations/pos-integrations.md) for detailed setup guides per POS.

### Payroll & Benefits
| System | Integration Type | Data Flow | Common Use Case |
|--------|-----------------|-----------|-----------------|
| ADP Workforce Now | API | Employee data, earnings, deductions | Customers keeping ADP payroll |
| ADP Run | File-based | Payroll export | Small business payroll export |
| Paychex | API + File | Employee sync, payroll data | Mid-market payroll integration |
| UKG (Kronos) | API | Time data, scheduling | Migrating from UKG scheduling |
| Ceridian Dayforce | API | Employee lifecycle | Enterprise HCM sync |
| Workday | API | Employee master data | Enterprise customers with Workday HCM |
| BambooHR | API | Employee records | Mid-market HR sync |

**See also:** [Payroll & HR Integrations](../integrations/payroll-hr-integrations.md) for detailed data flow specifications.

### Accounting & ERP
| System | Integration Type | Data Flow |
|--------|-----------------|-----------|
| QuickBooks Online | API | GL entries, labor costs |
| Sage Intacct | API | Journal entries, cost centers |
| SAP | File-based | GL posting, cost allocation |
| Oracle NetSuite | API | Financial data sync |
| Restaurant365 | API | Daily sales, labor journal |
| Microsoft Dynamics 365 | API | Financial data, employee sync |

### HR & Talent
| System | Integration Type | Data Flow |
|--------|-----------------|-----------|
| Indeed | API | Job posting, applicant flow |
| LinkedIn | API | Job distribution |
| ZipRecruiter | API | Job posting, applicants |
| Checkr | API | Background check initiation and results |
| E-Verify | API | Employment eligibility verification |
| Sterling | API | Background screening |

### Operations & Other
| System | Integration Type | Data Flow |
|--------|-----------------|-----------|
| Jolt | API | Task management, checklists |
| Tattle | API | Guest feedback correlation |
| Yelp | API | Review data for demand signals |
| Weather APIs | API | Weather data for Fourth iQ forecasting |

## Integration Architecture

### Standard Integration Pattern
```
Third-Party System <-> Fourth Integration Hub <-> Fourth Platform
                          |
                     Transform + Validate
                     Error Handling + Retry
                     Audit Logging
                     Rate Limiting
```

### Key Technical Specs
- **Authentication**: OAuth 2.0, API keys, certificate-based
- **Protocols**: REST (preferred), SFTP, SOAP (legacy), Webhooks
- **Formats**: JSON (preferred), XML, CSV, fixed-width
- **Frequency**: Real-time webhooks, scheduled batch (hourly/daily), on-demand
- **Error handling**: Automatic retry with exponential backoff, dead letter queue, email alerts
- **Monitoring**: Integration dashboard with success/failure rates, latency metrics, data volume tracking
- **SLA**: 99.9% integration uptime for standard connectors

### Custom Integration API
Fourth provides a well-documented REST API for custom integrations:
- **Employee API**: CRUD operations on employee records
- **Schedule API**: Read/write schedules, shift offers
- **Time API**: Clock events, punch corrections
- **Sales API**: Push POS sales data for forecasting
- **Reports API**: Pull standard and custom reports
- **Payroll API**: Payroll data export/import
- **Applicant API**: Applicant tracking integration

**See also:** [Developer API Platform](../integrations/developer-api-platform.md) for full API documentation details.

API documentation: Available via developer portal after contract signing.

## Implementation Timeline

| Integration Complexity | Typical Timeline | Examples |
|-----------------------|-----------------|----------|
| Standard POS | 2-4 weeks | Toast, Square, Lightspeed |
| Complex POS (multi-site) | 4-8 weeks | MICROS, custom POS, legacy systems |
| Payroll | 4-6 weeks | ADP, Paychex, Ceridian |
| ERP/Accounting | 3-6 weeks | Sage, QuickBooks, NetSuite |
| Custom API | 6-12 weeks | Proprietary systems |
| Full Enterprise Stack | 8-12 weeks | Multiple systems in parallel |

## Integration Best Practices

1. **Start with POS**: Sales data enables Fourth iQ demand forecasting immediately
2. **Parallel integrations**: Fourth can set up POS, payroll, and accounting integrations simultaneously
3. **Data validation**: Fourth runs parallel data validation for 2 weeks before go-live
4. **Phased approach**: For enterprise deployments, start with pilot locations before full rollout

## Frequently Asked Questions

**Q: Do we integrate with [POS System Z]?**
A: If the POS has an API or can export data files (CSV, XML), we can build a custom integration. Our Integration Hub supports any REST API, SFTP file drop, or webhook-capable system. Custom integrations typically take 6-12 weeks.

**Q: What if the customer's POS is not on the pre-built list?**
A: We evaluate the POS's technical capabilities and build a scoped integration. Costs may vary depending on complexity. Our most common custom pattern is SFTP file exchange for legacy POS systems.

**Q: Is there a cost for integrations?**
A: Standard pre-built integrations (Toast, Square, ADP, etc.) are included in the platform subscription at Professional and Enterprise tiers. Custom integrations may incur a one-time implementation fee based on scope. Essentials tier includes one POS integration.

**Q: How do you handle integration failures?**
A: The Fourth Integration Hub includes automatic retry with exponential backoff, dead letter queues for failed messages, email alerts to administrators, and a monitoring dashboard showing real-time integration health. Our support team proactively monitors enterprise integrations.

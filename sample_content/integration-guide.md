# Fourth Integration Capabilities

## Overview

Fourth integrates with 200+ third-party systems across POS, payroll, HR, accounting, and operations platforms. Our API-first architecture enables both pre-built connectors and custom integrations.

## Pre-Built Integrations

### Point of Sale (POS)
| POS System | Integration Type | Data Flow |
|-----------|-----------------|-----------|
| Toast | Real-time API | Sales, labor, tips, menu mix |
| Square | Real-time API | Sales, labor, employee sync |
| Oracle MICROS (Simphony) | Batch + Real-time | Sales, labor, tips |
| NCR Aloha | Batch file | Sales, labor, voids |
| Lightspeed | API | Sales, menu data |
| Revel | API | Sales, labor |
| SpotOn | API | Sales, tips, labor |
| PAR Brink | API | Sales data, employee sync |

### Payroll & Benefits
| System | Integration Type | Data Flow |
|--------|-----------------|-----------|
| ADP Workforce Now | API | Employee data, earnings, deductions |
| ADP Run | File-based | Payroll export |
| Paychex | API + File | Employee sync, payroll data |
| UKG (Kronos) | API | Time data, scheduling |
| Ceridian Dayforce | API | Employee lifecycle |

### Accounting & ERP
| System | Integration Type | Data Flow |
|--------|-----------------|-----------|
| QuickBooks Online | API | GL entries, labor costs |
| Sage Intacct | API | Journal entries, cost centers |
| SAP | File-based | GL posting, cost allocation |
| Oracle NetSuite | API | Financial data sync |
| Restaurant365 | API | Daily sales, labor journal |

### HR & Talent
| System | Integration Type | Data Flow |
|--------|-----------------|-----------|
| Workday | API | Employee master data |
| BambooHR | API | Employee records |
| Indeed | API | Job posting, applicant flow |
| LinkedIn | API | Job distribution |
| Checkr | API | Background check initiation and results |

## Integration Architecture

### Standard Integration Pattern
```
Third-Party System <-> Fourth Integration Hub <-> Fourth Platform
                          |
                     Transform + Validate
                     Error Handling
                     Audit Logging
```

### Key Technical Specs
- **Authentication**: OAuth 2.0, API keys, certificate-based
- **Protocols**: REST, SFTP, SOAP (legacy)
- **Formats**: JSON (preferred), XML, CSV, fixed-width
- **Frequency**: Real-time webhooks, scheduled batch (hourly/daily), on-demand
- **Error handling**: Automatic retry with exponential backoff, dead letter queue, email alerts
- **Monitoring**: Integration dashboard with success/failure rates, latency metrics

### Custom Integration API
Fourth provides a well-documented REST API for custom integrations:
- **Employee API**: CRUD operations on employee records
- **Schedule API**: Read/write schedules, shift offers
- **Time API**: Clock events, punch corrections
- **Sales API**: Push POS sales data for forecasting
- **Reports API**: Pull standard and custom reports

API documentation: Available via developer portal after contract signing.

## Implementation Timeline

| Integration Complexity | Typical Timeline | Examples |
|-----------------------|-----------------|----------|
| Standard POS | 2-4 weeks | Toast, Square, MICROS |
| Complex POS (multi-site) | 4-8 weeks | Custom POS, legacy systems |
| Payroll | 4-6 weeks | ADP, Paychex |
| ERP/Accounting | 3-6 weeks | Sage, QuickBooks |
| Custom API | 6-12 weeks | Proprietary systems |

## Frequently Asked Questions

**Q: Do we integrate with [POS System Z]?**
A: If the POS has an API or can export data files (CSV, XML), we can build a custom integration. Our Integration Hub supports any REST API, SFTP file drop, or webhook-capable system. Custom integrations typically take 6-12 weeks.

**Q: What if the customer's POS is not on the pre-built list?**
A: We evaluate the POS's technical capabilities and build a scoped integration. Costs may vary depending on complexity. Our most common custom pattern is SFTP file exchange for legacy POS systems.

**Q: Is there a cost for integrations?**
A: Standard pre-built integrations (Toast, Square, ADP, etc.) are included in the platform subscription. Custom integrations may incur a one-time implementation fee based on scope.

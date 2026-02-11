# Fourth POS Integrations

## Overview

Fourth connects directly with the point-of-sale systems your restaurants already rely on, turning raw transaction data into actionable labor and sales intelligence. Our POS integrations pull sales, tips, menu mix, and labor metrics in real time so managers can make scheduling decisions based on what is actually happening on the floor -- not last week's best guess.

With **8 major POS partners** and coverage across **95% of the North American restaurant market**, Fourth eliminates the manual data entry and CSV exports that slow down multi-unit operations. Every integration is maintained by Fourth's dedicated integrations engineering team, with SLA-backed uptime and proactive monitoring.

## Integration Partners

### Toast

Toast is Fourth's most widely deployed POS integration, active across **thousands of restaurant locations**. The integration uses Toast's real-time API to deliver bidirectional data sync covering sales totals, itemized transactions, tip distribution, menu mix, and employee records.

- **Data flow:** Bidirectional -- Fourth pushes employee profiles and job codes to Toast; Toast sends sales, tips, and labor punches to Fourth
- **Sync frequency:** Real-time (sub-60-second latency for sales data)
- **Key use case:** Multi-unit operators who schedule in Fourth and need Toast sales data for labor cost forecasting

### Square

Square's open API architecture makes it a natural fit for Fourth's real-time integration pipeline. The connection is particularly popular with fast-casual and quick-service brands that rely on Square for payments and need Fourth for workforce management at scale.

- **Data flow:** Square sends sales, employee, and transaction data to Fourth via REST API
- **Sync frequency:** Real-time
- **Key use case:** Fast-casual chains scaling from 5 to 50+ locations who outgrow Square's native scheduling

### Oracle MICROS (Simphony)

Oracle MICROS Simphony is the enterprise standard in hotel and large-format restaurant POS. Fourth supports both batch file and real-time API connections, making it the right choice for complex multi-site and multi-concept deployments where Simphony is the corporate POS mandate.

- **Data flow:** Batch (flat file via SFTP) and real-time (Oracle Simphony Cloud API)
- **Sync frequency:** Configurable -- batch runs on schedule (typically every 15 minutes), real-time available for Simphony Cloud
- **Key use case:** Hotel F&B operations and enterprise casual dining groups with 100+ locations

### NCR Aloha

NCR Aloha remains one of the most widely installed POS systems in casual and family dining. Fourth supports both Aloha's legacy batch file format and the modern NCR cloud API, ensuring compatibility regardless of where a customer is in their Aloha upgrade cycle.

- **Data flow:** Batch (Aloha BOH flat files via SFTP) or API (NCR cloud endpoints)
- **Sync frequency:** Batch every 15-30 minutes; API near-real-time
- **Key use case:** Casual dining franchises with a mix of legacy Aloha and newer NCR cloud installations

### Lightspeed

Lightspeed's API integration with Fourth serves boutique restaurants, cafes, and hospitality venues that value Lightspeed's modern interface and need Fourth's labor optimization on top of it.

- **Data flow:** Lightspeed sends sales and employee data to Fourth via REST API
- **Sync frequency:** Real-time
- **Key use case:** Independent and boutique restaurant groups in urban markets

### Revel

Revel's iPad-native POS is a growing force in fast-casual. Fourth's API integration pulls sales, labor, and tip data directly from Revel's cloud platform.

- **Data flow:** API-based, Revel to Fourth
- **Sync frequency:** Real-time
- **Key use case:** Fast-casual brands that chose Revel for its mobile-first design and need enterprise scheduling

### SpotOn

SpotOn has emerged as a strong challenger in the restaurant POS market. Fourth's integration captures tips, labor data, and sales transactions via SpotOn's API.

- **Data flow:** API-based, SpotOn to Fourth
- **Sync frequency:** Real-time
- **Key use case:** Full-service restaurants adopting SpotOn who need labor cost management beyond what SpotOn offers natively

### PAR Brink

PAR Brink is a cloud-native POS built for enterprise QSR and fast-casual. Fourth connects via Brink's API for employee sync, sales data, and labor metrics.

- **Data flow:** Bidirectional API -- Fourth pushes employee data; Brink sends sales and labor
- **Sync frequency:** Real-time
- **Key use case:** QSR franchisees using Brink who need Fourth's demand-based scheduling engine

## Comparison Table

| POS Partner | Connection Type | Data Flow | Sync Frequency | Setup Time | Key Data Points |
|---|---|---|---|---|---|
| **Toast** | REST API | Bidirectional | Real-time | 1-2 weeks | Sales, tips, menu mix, employees, labor |
| **Square** | REST API | Square to Fourth | Real-time | 1 week | Sales, employees, transactions |
| **Oracle MICROS** | API + SFTP | Configurable | Batch or real-time | 3-6 weeks | Sales, labor, revenue centers |
| **NCR Aloha** | API + SFTP | Aloha to Fourth | Batch or near-real-time | 2-4 weeks | Sales, tips, labor punches |
| **Lightspeed** | REST API | Lightspeed to Fourth | Real-time | 1-2 weeks | Sales, employees |
| **Revel** | REST API | Revel to Fourth | Real-time | 1-2 weeks | Sales, tips, labor |
| **SpotOn** | REST API | SpotOn to Fourth | Real-time | 1-2 weeks | Sales, tips, labor |
| **PAR Brink** | REST API | Bidirectional | Real-time | 2-3 weeks | Sales, employees, labor |

## What Data Flows Through

Every POS integration delivers a core set of data points into Fourth's workforce management platform:

- **Sales totals** by revenue center, daypart, and location -- used for demand forecasting and labor budgeting
- **Itemized transactions** and menu mix -- used for production planning and prep scheduling
- **Tip data** -- flows into Fourth Payroll for accurate tip pooling, reporting, and compliance
- **Labor punches** -- actual clock-in/clock-out times compared against scheduled shifts for variance tracking
- **Employee records** -- job codes, roles, and location assignments kept in sync to avoid duplicate entry

## How Setup Works

1. **Scoping call** -- Fourth's integrations team confirms POS version, data requirements, and location count
2. **Credential exchange** -- API keys or SFTP credentials are provisioned in a secure vault
3. **Configuration** -- Mapping of POS revenue centers, job codes, and locations to Fourth's data model
4. **Testing** -- Data validation in Fourth's staging environment with side-by-side comparison to POS reports
5. **Go-live** -- Integration activated in production with monitoring dashboards enabled

Average setup time across all POS partners is **2 weeks** for API-based integrations and **4 weeks** for batch/hybrid configurations.

## FAQ

**Q: What if my POS is not listed here?**
A: Fourth's Developer API Platform supports custom POS integrations. If your POS has an API, Fourth can connect to it. Contact your account team to discuss a custom integration or visit our developer portal for API documentation.

**Q: Can I switch POS systems without disrupting my Fourth setup?**
A: Yes. Fourth's data model is POS-agnostic. When you migrate from one POS to another, the integrations team remaps the new POS data to your existing Fourth configuration. Historical data from the previous POS is preserved.

**Q: How does Fourth handle POS outages or data gaps?**
A: Fourth monitors all POS connections with automated health checks. If a sync fails, the system retries automatically and alerts the Fourth support team. Batch integrations include gap-fill logic that reconciles missed intervals on the next successful run.

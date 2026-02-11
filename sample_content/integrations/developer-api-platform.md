# Fourth Developer API Platform

## Overview

Fourth's Developer API Platform gives engineering teams programmatic access to the full Fourth workforce management system. Every action available in the Fourth UI -- creating employees, publishing schedules, approving time punches, running reports -- is available through a RESTful API secured with OAuth 2.0.

The platform is designed for three audiences: **internal development teams** building custom dashboards and workflows, **technology partners** creating certified integrations, and **enterprise IT departments** orchestrating Fourth data across multi-vendor tech stacks. With structured documentation, a sandbox environment, and webhook support, Fourth's API is built for production-grade integrations, not proof-of-concept experiments.

Access to the Developer API Platform is available to all Fourth customers post-contract. Contact your account team or visit the developer portal to request API credentials.

## Authentication and Security

Fourth uses **OAuth 2.0** with client credentials grant for server-to-server integrations and authorization code grant for user-facing applications.

| Security Feature | Detail |
|---|---|
| **Authentication** | OAuth 2.0 (client credentials + authorization code) |
| **Token lifetime** | Access tokens expire after 60 minutes; refresh tokens valid for 30 days |
| **Transport** | TLS 1.2+ required on all endpoints |
| **Scopes** | Granular permission scopes per API (e.g., `employees:read`, `schedules:write`) |
| **IP allowlisting** | Optional -- restrict API access to known IP ranges |
| **Audit logging** | All API calls logged with timestamp, caller, endpoint, and response code |

## Core APIs

Fourth exposes seven primary API families. Each follows RESTful conventions with JSON request and response bodies.

### API Endpoint Reference

| API | Base Path | Methods | Description |
|---|---|---|---|
| **Employee** | `/api/v2/employees` | GET, POST, PUT, DELETE | Create, read, update, and deactivate employee records. Includes job codes, locations, certifications, and custom fields. |
| **Schedule** | `/api/v2/schedules` | GET, POST, PUT, DELETE | Publish, retrieve, and modify shift schedules. Supports bulk operations for multi-location schedule deployment. |
| **Time** | `/api/v2/timecards` | GET, POST, PUT | Submit and approve time punches, retrieve timecard summaries, and manage exceptions. |
| **Sales** | `/api/v2/sales` | GET, POST | Push sales data into Fourth for demand forecasting. Retrieve aggregated sales by location, daypart, and revenue center. |
| **Reports** | `/api/v2/reports` | GET | Generate and retrieve labor cost, overtime, compliance, and operational reports in JSON or CSV format. |
| **Applicant** | `/api/v2/applicants` | GET, POST, PUT | Manage applicant records, application status, and hiring workflow stages in Fourth's ATS. |
| **Payroll** | `/api/v2/payroll` | GET, POST | Export payroll-ready data including earnings, deductions, and tax withholdings. Retrieve payroll run history. |

### Sample Endpoints

| Operation | Method | Endpoint | Description |
|---|---|---|---|
| List employees | GET | `/api/v2/employees?location_id=1042` | Returns all active employees at location 1042 |
| Create employee | POST | `/api/v2/employees` | Creates a new employee record with required fields |
| Get schedule | GET | `/api/v2/schedules?location_id=1042&week=2026-02-09` | Returns the published schedule for the specified week |
| Submit time punch | POST | `/api/v2/timecards/punches` | Records a clock-in or clock-out event |
| Push sales data | POST | `/api/v2/sales` | Sends sales totals for a location and time period |
| Run labor report | GET | `/api/v2/reports/labor-cost?location_id=1042&range=2026-02-01,2026-02-07` | Returns labor cost breakdown for the date range |
| List applicants | GET | `/api/v2/applicants?status=new` | Returns applicants in "new" status across all locations |
| Export payroll | GET | `/api/v2/payroll/export?pay_period=2026-02-01` | Returns payroll-ready data for the specified pay period |

## Rate Limits and Versioning

| Parameter | Detail |
|---|---|
| **Rate limit** | 1,000 requests per minute per API key (burst: 50 requests/second) |
| **Rate limit headers** | `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` returned on every response |
| **Versioning** | URI-based (`/api/v2/`). Previous versions supported for **12 months** after a new version ships. |
| **Deprecation notice** | 90 days advance notice via developer portal and email before any endpoint retirement |
| **Pagination** | Cursor-based for list endpoints. Default page size: 100. Max: 500. |
| **Response format** | JSON (default). CSV available on report endpoints via `Accept: text/csv` header. |

## Webhooks

Fourth supports outbound webhooks for event-driven integrations. Instead of polling for changes, register a webhook URL and Fourth pushes events to your system in real time.

| Webhook Event | Trigger | Payload |
|---|---|---|
| `employee.created` | New employee record created | Employee object |
| `employee.updated` | Employee profile modified | Changed fields + employee ID |
| `employee.terminated` | Employee deactivated | Employee ID + termination date |
| `schedule.published` | Schedule published for a location/week | Schedule summary + shift count |
| `timecard.approved` | Timecard approved by manager | Timecard summary |
| `applicant.status_changed` | Applicant moves to a new hiring stage | Applicant ID + old/new status |

Webhooks are delivered via HTTPS POST with HMAC-SHA256 signature verification. Failed deliveries are retried with exponential backoff (3 attempts over 1 hour).

## Developer Portal and Sandbox

The **Fourth Developer Portal** (available post-contract) provides:

- **Interactive API documentation** with request/response examples
- **Sandbox environment** with synthetic data for testing -- no risk to production
- **API key management** -- create, rotate, and revoke keys
- **Webhook configuration** -- register endpoints, view delivery logs, replay failed events
- **Usage dashboard** -- monitor API call volume, error rates, and latency

The sandbox mirrors production APIs with a dedicated dataset of **50 sample locations, 500 employees, and 12 weeks of schedule and sales history**. All sandbox data resets weekly.

## SDKs and Libraries

| SDK | Language | Status | Source |
|---|---|---|---|
| **fourth-js** | JavaScript / Node.js | Official | Available via developer portal |
| **fourth-python** | Python | Community | GitHub (community-maintained, Fourth-reviewed) |

Both SDKs handle OAuth token management, pagination, rate limit retries, and error parsing. The JavaScript SDK supports both CommonJS and ESM imports.

## Common Integration Patterns

### 1. Custom BI Dashboard

Pull labor cost, sales, and schedule data into a proprietary analytics platform.

- **APIs used:** Reports, Sales, Schedule
- **Pattern:** Nightly batch pull via Reports API; real-time sales via webhooks
- **Example:** A 200-location franchise builds a custom Power BI dashboard that combines Fourth labor data with proprietary customer traffic metrics

### 2. Proprietary POS Integration

Connect a POS system that Fourth does not natively support.

- **APIs used:** Sales, Employee
- **Pattern:** POS pushes sales data to Fourth via Sales API; Fourth pushes employee/job code data to POS via Employee API
- **Example:** A regional chain with a custom-built POS sends itemized sales and tip data to Fourth every 15 minutes for labor forecasting

### 3. Multi-System Orchestration

Coordinate Fourth with HRIS, payroll, POS, and business intelligence in a unified data pipeline.

- **APIs used:** Employee, Schedule, Time, Payroll, Sales
- **Pattern:** Event-driven via webhooks -- employee created in HRIS triggers Fourth employee creation; schedule publish triggers downstream staffing notifications; timecard approval triggers payroll export
- **Example:** A hotel management company with Workday (HR), Fourth (scheduling), Oracle MICROS (POS), and ADP (payroll) uses Fourth's API as the labor data hub connecting all four systems

### 4. Applicant Pipeline Automation

Integrate Fourth's ATS with job boards, background check providers, and onboarding systems.

- **APIs used:** Applicant, Employee
- **Pattern:** Job board posts applicants via Applicant API; status change webhook triggers background check; hire event creates employee record
- **Example:** A QSR brand automates the path from Indeed application to first scheduled shift with zero manual data entry

## API-First Architecture

Fourth is built API-first. The web application and mobile apps consume the same APIs available to external developers. This means:

- **No hidden functionality** -- every feature accessible in the UI is available via API
- **Consistent behavior** -- API responses match what users see in the application
- **Real-time parity** -- data written via API appears in the UI immediately, and vice versa

## FAQ

**Q: How do I get access to the Developer API Platform?**
A: API access is included for all Fourth customers. Contact your account manager to request developer portal credentials. Your team will receive a sandbox API key within one business day and production keys after completing a brief security review.

**Q: What support is available for custom integrations?**
A: Fourth provides technical documentation, sandbox environments, and SDK libraries for self-service integration development. For complex enterprise integrations, Fourth's Professional Services team offers paid integration architecture and implementation support with dedicated engineering resources.

**Q: Is there a cost for API access?**
A: API access is included in Fourth platform licenses at standard rate limits. Customers requiring elevated rate limits (above 1,000 requests/minute) or dedicated infrastructure for high-volume integrations can discuss enterprise API tiers with their account team.

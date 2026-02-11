# Fourth Security & Compliance

## Overview

Fourth maintains enterprise-grade security across all platform components, protecting sensitive employee data, financial information, and operational data for thousands of restaurant and hospitality locations. Our security program is audited annually and meets the requirements of the most demanding enterprise customers.

## Infrastructure Security

- Hosted on **Microsoft Azure** with SOC 2 Type II certification
- Data encrypted at rest (**AES-256**) and in transit (**TLS 1.2+**)
- Multi-region deployment with automated failover
- **99.9% uptime SLA** with 24/7 infrastructure monitoring
- Annual penetration testing by independent third-party firms
- Vulnerability scanning and remediation on continuous basis
- DDoS protection via Azure Front Door
- Web Application Firewall (WAF) on all public endpoints

## Access Control

- **Role-based access control (RBAC)** with granular permissions (location, department, function level)
- **Multi-factor authentication (MFA)** for all admin accounts
- **Single Sign-On (SSO)** via SAML 2.0 and OpenID Connect
- Session management with configurable timeout policies
- IP whitelisting for admin access (optional)
- Audit logging of all administrative actions
- Automated account lockout after failed attempts
- Principle of least privilege enforced across all roles

## Data Protection

- **SOC 2 Type II** audited annually (report available under NDA)
- **GDPR compliant** (for international operations, EU data residency available)
- **CCPA compliant** (California Consumer Privacy Act)
- **PCI DSS compliant** for payment-related data
- **HIPAA available** for healthcare/senior living customers
- Regular vulnerability scanning and remediation
- Data Loss Prevention (DLP) policies on all data exports

## PII and Employee Data Handling

Fourth follows strict data handling practices for employee personally identifiable information:

- **Data minimization**: Collect only data required for workforce management functions
- **Encryption**: All PII encrypted at rest and in transit
- **Access logging**: All access to PII is logged and auditable
- **Retention**: Configurable data retention policies per customer requirements and local regulations
- **Right to delete**: Full support for GDPR/CCPA right to erasure requests
- **Data residency**: US data stored in US Azure regions; EU data available in EU regions for international customers
- **Data portability**: Full data export capabilities for customer data

## Compliance Certifications

| Certification | Status | Audit Frequency | Report Availability |
|--------------|--------|-----------------|---------------------|
| SOC 2 Type II | Active | Annual | Under NDA |
| PCI DSS | Compliant | Annual | On request |
| GDPR | Compliant | Ongoing | Privacy policy published |
| CCPA | Compliant | Ongoing | Privacy policy published |
| HIPAA | Available for healthcare customers | Annual | BAA available |
| ISO 27001 | In progress | Annual | Target: 2026 |

## Disaster Recovery & Business Continuity

- **RPO (Recovery Point Objective)**: 1 hour for transactional data, 15 minutes for critical operations
- **RTO (Recovery Time Objective)**: 4 hours for full platform recovery
- **Backup strategy**: Automated daily backups with 30-day retention, cross-region replication
- **DR testing**: Quarterly disaster recovery drills with documented results
- **Incident response**: 24/7 on-call engineering team, documented incident response procedures, customer notification within 24 hours for security incidents
- **Business continuity plan**: Tested semi-annually with executive sign-off

## Labor Law Compliance Engine

Fourth's compliance engine is a core differentiator, automating enforcement of labor laws across all jurisdictions:

- **Rule library**: **500+ labor law rules** covering all 50 US states plus major municipalities
- **Automatic updates**: Fourth's legal team monitors regulatory changes and pushes rule updates to the platform within 30 days of enactment
- **Proactive alerts**: System warns managers before scheduling actions that would violate compliance rules
- **Audit trail**: Complete history of all scheduling decisions, policy overrides, and compliance exceptions
- **Reporting**: Pre-built compliance reports for predictive scheduling, overtime, break violations, and minor labor
- **Configurable policies**: Customers can layer company-specific policies on top of legal requirements

### Jurisdictions Covered
- **Federal**: FLSA, ACA, FMLA, I-9/E-Verify
- **State**: All 50 states including complex states (California, New York, Oregon, Washington)
- **Municipal**: San Francisco Fair Workweek, NYC Fair Work Week, Chicago Fair Workweek, Seattle Secure Scheduling, Philadelphia Fair Workweek, and 15+ additional local ordinances
- **International**: UK Working Time Regulations (for UK operations)

**See also:** [Labor Law Compliance Deep Dive](labor-law-compliance.md) | [Tip Management Compliance](tip-management-compliance.md)

## Frequently Asked Questions

**Q: Can we get a copy of your SOC 2 report?**
A: Yes. SOC 2 Type II reports are available under NDA. Contact your account executive or email security@fourth.com to request the current report.

**Q: How do you handle a data breach?**
A: Fourth has a documented incident response plan. In the event of a confirmed breach, affected customers are notified within 24 hours with details of the incident, impact assessment, and remediation steps. Our 24/7 security team monitors for anomalies continuously.

**Q: Do you support data residency requirements?**
A: Yes. US customer data is stored in US Azure regions. For international customers (UK/EU), data can be stored in EU Azure regions to comply with GDPR data residency requirements.

**Q: How often do you update compliance rules?**
A: Fourth's legal team continuously monitors legislative and regulatory changes. Rule updates are pushed to the platform within 30 days of a new law or ordinance taking effect. Customers are notified of material changes via email and in-app notifications.

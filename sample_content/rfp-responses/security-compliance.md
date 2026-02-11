# RFP Response: Security & Compliance

## Standard RFP Answers - Security and Data Protection

### Q: Describe your data security practices.
**Confidence: GROUNDED**

Fourth maintains enterprise-grade security across all platform components:

**Infrastructure Security:**
- Hosted on Microsoft Azure with SOC 2 Type II certification
- Data encrypted at rest (AES-256) and in transit (TLS 1.2+)
- Multi-region deployment with automated failover
- 99.9% uptime SLA with 24/7 infrastructure monitoring
- Annual penetration testing by independent third-party firms

**Access Control:**
- Role-based access control (RBAC) with granular permissions
- Multi-factor authentication (MFA) for all admin accounts
- Single Sign-On (SSO) via SAML 2.0 and OpenID Connect
- Session management with configurable timeout policies
- IP whitelisting for admin access (optional)

**Data Protection:**
- SOC 2 Type II audited annually
- GDPR compliant (for international operations)
- CCPA compliant
- PCI DSS compliant for payment-related data
- Regular vulnerability scanning and remediation

### Q: How do you handle PII and employee data?
**Confidence: GROUNDED**

Fourth follows strict data handling practices for employee personally identifiable information:

- **Data minimization**: Collect only data required for workforce management functions
- **Encryption**: All PII encrypted at rest and in transit
- **Access logging**: All access to PII is logged and auditable
- **Retention**: Configurable data retention policies per customer requirements and local regulations
- **Right to delete**: Support for GDPR/CCPA right to erasure requests
- **Data residency**: US data stored in US Azure regions; EU data available in EU regions for international customers

### Q: What compliance certifications do you hold?
**Confidence: GROUNDED**

| Certification | Status | Audit Frequency |
|--------------|--------|-----------------|
| SOC 2 Type II | Active | Annual |
| PCI DSS | Compliant | Annual |
| GDPR | Compliant | Ongoing |
| CCPA | Compliant | Ongoing |
| HIPAA | Available for healthcare customers | Annual |

### Q: Describe your disaster recovery and business continuity capabilities.
**Confidence: GROUNDED**

- **RPO (Recovery Point Objective)**: 1 hour for transactional data, 15 minutes for critical operations
- **RTO (Recovery Time Objective)**: 4 hours for full platform recovery
- **Backup strategy**: Automated daily backups with 30-day retention, cross-region replication
- **DR testing**: Quarterly disaster recovery drills with documented results
- **Incident response**: 24/7 on-call engineering team, documented incident response procedures, customer notification within 24 hours for security incidents

### Q: How do you ensure compliance with labor laws?
**Confidence: GROUNDED**

Fourth's compliance engine is a core differentiator:

- **Rule library**: 500+ labor law rules covering all 50 US states plus major municipalities
- **Automatic updates**: Fourth's legal team monitors regulatory changes and pushes rule updates to the platform
- **Proactive alerts**: System warns managers before scheduling actions that would violate compliance rules
- **Audit trail**: Complete history of all scheduling decisions, policy overrides, and compliance exceptions
- **Reporting**: Pre-built compliance reports for predictive scheduling, overtime, break violations, and minor labor
- **Configurable policies**: Customers can layer company-specific policies on top of legal requirements

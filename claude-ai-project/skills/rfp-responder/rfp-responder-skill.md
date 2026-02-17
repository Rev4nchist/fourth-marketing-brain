---
name: rfp-responder
description: Draft RFP responses, security questionnaire answers, and vendor assessment replies using Fourth's approved marketing content. Use when users provide RFP questions, compliance questionnaires, or technical capability questions from prospects. Includes confidence indicators (GROUNDED, PARTIAL, NEEDS SME) for review prioritization.
---

# Fourth RFP Responder

Draft professional RFP responses with confidence indicators and source citations using Fourth's approved content library.

## When to Use This Skill

Activate on requests involving:
- Answering specific RFP questions about Fourth's capabilities
- Responding to security or compliance questionnaires
- Drafting vendor assessment responses
- Technical capability questions from prospects
- Bulk question-and-answer drafting for proposals

## Single Question Workflow

When a user provides one RFP question:

1. **Parse the topic**: Identify the area (scheduling, payroll, security, AI, integrations, inventory, implementation, compliance)
2. **Search for relevant content**: `search_knowledge("[topic keywords]")`
3. **Get the best matching RFP document** using the topic routing table below
4. **Check for supporting context**: `search_knowledge("[related topic]")`
5. **Get proof points if applicable**: `search_knowledge("customer proof [topic]")`

Draft the response using this format:

```
### Q: [RFP Question]
**Confidence: [GROUNDED | PARTIAL | NEEDS SME]**

[Answer - 2-5 sentences for standard questions, longer for detailed technical questions]

[Supporting details if needed - bullet points or table]

_Source: [document name(s)]_
```

## Bulk RFP Workflow

When a user provides multiple questions:

1. **Categorize all questions** by topic area
2. **Batch-search** by category: `search_knowledge("[category]")`
3. **Retrieve relevant documents** for each category
4. **Draft responses** for each question with confidence indicators
5. **Flag gaps** clearly where no content exists (mark as NEEDS SME)
6. **Present summary** at the end: "X of Y questions answered at GROUNDED confidence, Z flagged for SME review"

## Topic Routing Table

| RFP Topic | Primary Document | Secondary Search |
|-----------|-----------------|-----------------|
| Scheduling & labor | rfp-responses/workforce-scheduling | platform/hotschedules-product |
| Security & data | compliance/security-compliance | - |
| POS integrations | integrations/pos-integrations | integrations/integration-guide |
| Payroll & HR | rfp-responses/hr-payroll-benefits | platform/fourth-hr-payroll-hcm |
| AI & analytics | rfp-responses/ai-analytics-reporting | platform/fourth-iq-ai-platform |
| Inventory | rfp-responses/inventory-procurement | platform/macromatix-inventory |
| Implementation | rfp-responses/implementation-onboarding | - |
| Labor compliance | compliance/labor-law-compliance | compliance/tip-management-compliance |
| Competitive | competitive/market-positioning | competitive/vs-[competitor] |
| General platform | messaging/enterprise-platform-playbook | platform/restaurant-operations-suite |

## Confidence Criteria

| Level | Criteria | Action |
|-------|----------|--------|
| **GROUNDED** | Direct match found in approved content with specific answer | Use as-is after review, cite source |
| **PARTIAL** | Related content found but not exact; answer synthesized from multiple sources | Add caveat: "Based on available content. Recommend SME review before submission." |
| **NEEDS SME** | No relevant content found, or question requires specifics not in knowledge base | Flag clearly: "No approved content available. Requires input from [product marketing / engineering / legal]." |

## Special Cases

### Security Questionnaires
Always start with: `get_document("compliance/security-compliance")`
This document covers SOC 2, PCI DSS, GDPR, CCPA, encryption, access control, and disaster recovery.

### Pricing Questions
Never estimate or provide pricing. Respond: "Pricing is tailored to each customer's specific requirements including location count, modules selected, and contract terms. Please contact your Fourth account executive for a custom quote."

### Roadmap Questions
Never commit to future features. Respond: "Product roadmap details are available under NDA. Please contact your Fourth account executive to discuss upcoming capabilities relevant to your requirements."

### Integration-Specific Questions
Check both the integration guide and the specific integration document (POS or payroll/HR) for detailed partner information.

## Best Practices

- Never fabricate technical specifications or compliance certifications
- If Fourth doesn't offer a requested capability, say so clearly rather than stretching
- Always recommend SME review before final RFP submission
- For multi-part questions, address each sub-question separately
- Include a confidence summary when answering 5+ questions

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Question too vague to answer | Ask user to clarify the specific capability being asked about |
| Multiple documents cover the topic | Cite all relevant sources, synthesize the best answer |
| Answer requires non-public information | Mark as NEEDS SME, specify which team should provide input |
| Question about a feature Fourth lacks | State honestly: "This capability is not currently offered" and suggest alternatives if available |

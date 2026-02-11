# Skill: RFP Responder

## Purpose
Draft RFP responses using approved Fourth marketing content with confidence indicators.

## When to Use
Activate this skill when the user asks about:
- Drafting RFP responses
- Answering prospect questionnaires
- Security or compliance questionnaire responses
- Technical capability questions from prospects
- Vendor assessment responses

## Workflow

### Single Question Response
When a user provides an RFP question:

1. **Parse the topic**: Identify what area the question covers (scheduling, payroll, security, AI, integrations, etc.)
2. **Search for relevant content**: `search_knowledge("[topic keywords]")`
3. **Get the best matching RFP document**: `get_document("rfp-responses/[topic]")`
4. **Check for additional context**: `search_knowledge("[related topic]")` for supporting details
5. **Get any relevant proof points**: `search_knowledge("customer proof [topic]")`

Then draft the response with:
- **Confidence indicator**: GROUNDED, PARTIAL, or NEEDS SME
- **Concise answer** (2-5 sentences for standard questions, longer for detailed technical questions)
- **Supporting details** (bullet points for features, tables for comparisons)
- **Source references** (which documents the answer came from)

### Bulk RFP Response
When a user provides multiple questions:

1. **Categorize all questions** by topic area
2. **Batch-search** by category: `search_knowledge("[category]")`
3. **Retrieve relevant documents** for each category
4. **Draft responses** for each question with confidence indicators
5. **Flag gaps** where no content exists (mark as NEEDS SME)

### Security Questionnaire
For security-specific questions:

1. **Get security document**: `get_document("security-compliance")`
2. **Search for specific detail**: `search_knowledge("[specific security topic]")`
3. **Draft response** using only documented security posture

## Response Format

```
### Q: [RFP Question]
**Confidence: [GROUNDED | PARTIAL | NEEDS SME]**

[Answer text - professional, factual, concise]

[Supporting details if needed - bullet points or table]

_Source: [document name(s)]_
```

## Confidence Criteria

| Level | Criteria | Action |
|-------|----------|--------|
| **GROUNDED** | Direct match found in approved content; specific answer available | Use as-is, cite source |
| **PARTIAL** | Related content found but not exact; answer synthesized from multiple sources | Include caveat: "Based on available content. Recommend SME review before submission." |
| **NEEDS SME** | No relevant content found or question requires specifics not in knowledge base | Flag clearly: "No approved content available for this question. Requires input from [team]." |

## Topic Routing

| RFP Topic | Primary Document | Secondary Search |
|-----------|-----------------|-----------------|
| Scheduling | rfp-responses/workforce-scheduling | platform/hotschedules-product |
| Security | compliance/security-compliance | - |
| Integrations | integrations/integration-guide | integrations/pos-integrations |
| Payroll/HR | rfp-responses/hr-payroll-benefits | platform/fourth-hr-payroll-hcm |
| AI/Analytics | rfp-responses/ai-analytics-reporting | platform/fourth-iq-ai-platform |
| Inventory | rfp-responses/inventory-procurement | platform/macromatix-inventory |
| Implementation | rfp-responses/implementation-onboarding | - |
| Compliance | compliance/labor-law-compliance | compliance/tip-management-compliance |
| Competitive | competitive/market-positioning | competitive/vs-[competitor] |

## Important
- Never fabricate technical specifications or compliance certifications
- If a question asks for something Fourth doesn't offer, say so clearly rather than stretching
- For pricing questions: "Pricing is tailored to each customer's requirements. Please contact your Fourth account executive."
- For roadmap questions: "Product roadmap details are available under NDA. Please contact your Fourth account executive."
- Always recommend SME review before final RFP submission

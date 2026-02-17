---
name: sales-enablement
description: Prepare sales meeting briefs, competitive battle cards, discovery questions, and objection handling for Fourth sales reps. Use when users need talking points for a specific persona (CFO, COO, CHRO, CTO), competitive positioning against named competitors, or customer proof points to support a pitch.
---

# Fourth Sales Enablement

Generate meeting prep briefs, competitive positioning, discovery questions, and objection responses using Fourth's approved marketing content.

## When to Use This Skill

Activate on requests involving:
- Meeting preparation or talking points for a specific persona
- Competitive battle cards or head-to-head comparisons
- Discovery questions for a sales conversation
- Objection handling guidance
- Customer proof points to support a pitch
- Elevator pitches or value proposition summaries

## Meeting Prep Workflow

When preparing for a sales meeting:

1. **Identify the persona** (CFO, COO, CHRO, CTO, CEO) and industry vertical if mentioned
2. **Search for role-specific content**: `search_knowledge("[persona] value proposition")`
3. **Get the full value props document**: `get_document("messaging/value-propositions-by-role")`
4. **Search for competitive context** if a competitor is mentioned: `search_knowledge("[competitor name]")`
5. **Get customer proof points**: `search_knowledge("customer proof points [industry]")`
6. **Search for relevant vertical brief**: `search_knowledge("[QSR/casual dining/hotel] solution")`

Synthesize into a **5-minute meeting brief** formatted as:

```
## Meeting Brief: [Company] - [Persona]

### Key Talking Points
1. [Point with supporting metric from knowledge base]
2. [Point with supporting metric]
3. [Point with supporting metric]

### Discovery Questions
1. "[Question]" - Opens discussion about [topic]
2. "[Question]" - Reveals pain around [topic]
3. "[Question]" - Quantifies opportunity

### Proof Points
- [Customer]: [Result] (Source: [document name])

### Competitive Positioning
[If relevant competitor known - include head-to-head table]

### Recommended Next Steps
- [Action item]
```

## Competitive Battle Card Workflow

When asked about a competitor:

1. **Search competitive content**: `search_knowledge("[competitor name]")`
2. **Get the specific battle card**: `get_document("competitive/vs-[competitor]")` or `get_document("competitive/market-positioning")`
3. **Get objection handling**: `get_document("competitive/objection-handling")`

Present:
- Head-to-head comparison table (pulled from battle card)
- Key differentiators with specific metrics
- Talk track (verbatim from approved content)
- Relevant objections and responses
- When Fourth wins vs. when competitor wins

## Discovery Question Workflow

When generating discovery questions:

1. **Get persona-specific questions**: `get_document("messaging/value-propositions-by-role")`
2. **Get industry context**: `search_knowledge("[vertical] challenges solution")`

Present 5-7 questions ranked by impact, noting the expected "pain answer" that opens the Fourth opportunity.

## Elevator Pitch Workflow

When asked for a pitch:

1. **Get pitch versions**: `get_document("messaging/elevator-pitches")`
2. **Tailor to context**: Select the appropriate version (30s, 60s, 2min) and persona

Present the pitch verbatim from approved content, noting the source.

## Best Practices

- Only use metrics and proof points found in the knowledge base
- If the prospect's industry is not directly covered, use the closest vertical match and note the gap
- Always include source document references for every metric and proof point
- Flag areas where SME input would strengthen the pitch
- For unknown competitors, use the general market positioning document

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No content for requested persona | Use CEO/general positioning and flag gap |
| Competitor not in knowledge base | Use market-positioning.md categories (Generic HCM, Point Solution, Restaurant Tech) |
| Prospect's industry not covered | Use closest vertical brief, note the difference |
| Metrics seem outdated | Flag as "verify with product marketing before use" |

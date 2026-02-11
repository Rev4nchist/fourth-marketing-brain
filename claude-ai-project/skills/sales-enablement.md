# Skill: Sales Enablement

## Purpose
Help sales reps prepare for meetings, handle objections, and build competitive positioning.

## When to Use
Activate this skill when the user asks about:
- Meeting preparation or talking points
- Discovery questions for a specific persona
- Competitive positioning against a named competitor
- Objection handling
- Customer proof points or case studies
- Value propositions for a specific role

## Workflow

### Meeting Prep
When a user asks to prepare for a meeting:

1. **Identify the persona** (CFO, COO, CHRO, CTO, CEO)
2. **Search for role-specific value props**: `search_knowledge("[persona] value proposition")`
3. **Get the full value props document**: `get_document("value-propositions-by-role")`
4. **Search for competitive context** if competitor mentioned: `search_knowledge("[competitor]")`
5. **Get customer proof points**: `search_knowledge("customer proof points [industry]")`
6. **Search for relevant solution brief**: `search_knowledge("[vertical] solution")`

Then synthesize into a **5-minute meeting brief** with:
- 3 key talking points tailored to the persona
- 2-3 discovery questions to open the conversation
- Relevant proof points with specific metrics
- Competitive positioning (if competitor known)
- Recommended next steps

### Competitive Battle Card
When a user asks about a competitor:

1. **Search competitive content**: `search_knowledge("[competitor name]")`
2. **Get the battle card**: `get_document("vs-[competitor]")` or `get_document("market-positioning")`
3. **Get objection handling**: `get_document("objection-handling")`

Present:
- Head-to-head comparison table
- Key differentiators (what Fourth does that they don't)
- Talk track (what to say in the meeting)
- Common objections and responses
- When we win vs. when we lose

### Discovery Question Generation
When a user needs discovery questions:

1. **Get persona-specific questions**: `get_document("value-propositions-by-role")`
2. **Get industry context**: `search_knowledge("[vertical] challenges")`

Present 5-7 questions ranked by impact, with the expected "pain answer" that opens the Fourth opportunity.

## Output Format

Always structure sales enablement output as:

```
## Meeting Brief: [Company] - [Persona]

### Key Talking Points
1. [Point with supporting metric]
2. [Point with supporting metric]
3. [Point with supporting metric]

### Discovery Questions
1. "[Question]" → Opens discussion about [topic]
2. "[Question]" → Reveals pain around [topic]

### Proof Points
- [Customer]: [Result] ([Source document])

### Competitive Positioning
[If relevant competitor known]

### Recommended Next Steps
- [Action item]
```

## Important
- Only use metrics and proof points from the knowledge base
- If the prospect's industry isn't covered, use the closest match and note the gap
- Always include source document references
- Flag any areas where SME input would strengthen the pitch

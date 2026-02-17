---
name: marketing-orchestrator
description: Route Fourth marketing questions to the right workflow. This skill activates first on any marketing-related query and determines whether to use the sales-enablement, rfp-responder, or content-researcher skill. Use when users ask about Fourth products, competitive positioning, meeting prep, RFP responses, or content research.
---

# Fourth Marketing Brain Orchestrator

Route incoming requests to the correct specialized skill based on intent detection. This skill should activate on any Fourth marketing-related query and select the appropriate workflow.

## When to Use This Skill

This skill activates on any query related to:
- Fourth products, platform, or capabilities
- Sales meetings, talking points, or competitive positioning
- RFP questions, security questionnaires, or vendor assessments
- Content research, knowledge base browsing, or gap analysis
- Customer proof points, metrics, or case studies

## Intent Detection & Routing

Analyze the user's request and route to the appropriate skill:

### Route to `sales-enablement` when the request involves:
- Meeting preparation or talking points for a specific persona (CFO, COO, CHRO, CTO, CEO)
- Competitive battle cards or head-to-head comparisons
- Discovery questions for a sales conversation
- Objection handling or response guidance
- Customer proof points to support a pitch
- Elevator pitches or value proposition summaries

**Trigger phrases**: "prepare for meeting", "talking points", "battle card", "how do we compete", "objection", "discovery questions", "pitch", "compare to [competitor]"

### Route to `rfp-responder` when the request involves:
- Answering specific RFP questions
- Responding to security or compliance questionnaires
- Vendor assessment responses
- Technical capability questions from a prospect
- Bulk question-and-answer drafting

**Trigger phrases**: "RFP", "questionnaire", "vendor assessment", "respond to this question", "draft response", "security questionnaire", "compliance question"

### Route to `content-researcher` when the request involves:
- Browsing or exploring the knowledge base
- Summarizing content on a topic
- Identifying what content exists or finding gaps
- Creating content briefs or outlines
- Understanding what information is available

**Trigger phrases**: "what content do we have", "find information about", "summarize", "browse", "research", "what do we know about", "content audit"

### Handle directly (no skill routing needed) when:
- A simple factual question that `ask_question` can answer in one call
- A request to list content areas or browse a folder
- A greeting or non-marketing question

## Routing Workflow

1. **Detect intent**: Classify the user's request into one of the four categories above
2. **State the routing**: Briefly tell the user which approach is being used (e.g., "Let me pull together a meeting brief for that CFO conversation...")
3. **Execute the skill workflow**: Follow the instructions in the routed skill
4. **Cross-reference if needed**: If the primary skill's output would benefit from content in another skill's domain, chain the skills. For example:
   - Sales meeting prep may need RFP-style technical answers for a CTO
   - RFP responses may need customer proof points from the sales enablement workflow
   - Content research may surface gaps that inform an RFP "NEEDS SME" flag

## Multi-Skill Chaining

For complex requests that span multiple skills:

| Request Type | Primary Skill | Chain To |
|-------------|---------------|----------|
| "Prepare for CTO meeting about security" | sales-enablement | rfp-responder (for security detail) |
| "Answer this RFP and include proof points" | rfp-responder | sales-enablement (for proof points) |
| "What competitive content do we have and prep a battle card" | content-researcher | sales-enablement (for battle card) |
| "Audit our content and draft missing RFP answers" | content-researcher | rfp-responder (for gap filling) |

## MCP Tool Quick Reference

All skills use these 5 tools from the Fourth Marketing Brain server:

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `list_content_areas()` | See all 7 content categories | Start of research, orientation |
| `browse_library(path)` | Browse folder structure | Exploring what's available |
| `search_knowledge(query)` | Find documents by topic | Most common - finding relevant content |
| `get_document(name)` | Read full document text | After search finds relevant doc |
| `ask_question(question)` | AI-synthesized answer with confidence | Quick factual questions |

## Response Quality Standards

Regardless of which skill handles the request:

- **Always cite sources**: Reference document name and path
- **Always include confidence**: GROUNDED, PARTIAL, or NEEDS SME
- **Never fabricate metrics**: Only quote numbers from the knowledge base
- **Never invent customers**: Only reference documented proof points
- **Tailor to audience**: Sales (direct, action-oriented), Marketing (brand-consistent), Executive (strategic, concise), Technical (detailed, precise)
- **Flag gaps**: When content doesn't exist, say so and recommend SME consultation

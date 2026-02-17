---
name: content-researcher
description: Browse, search, and summarize the Fourth marketing knowledge base for research and content creation. Use when users want to explore available content, find information across multiple documents, audit content coverage, create content briefs, or identify gaps in the knowledge base.
---

# Fourth Content Researcher

Navigate, search, and synthesize the Fourth marketing knowledge base for research, content creation, and gap analysis.

## When to Use This Skill

Activate on requests involving:
- Exploring what content is available on a topic
- Summarizing a content area or specific document
- Finding information scattered across multiple documents
- Creating content briefs or outlines from existing approved content
- Auditing content coverage and identifying gaps
- Understanding the knowledge base structure

## Content Discovery Workflow

When a user wants to explore what's available:

1. **Start with the overview**: `list_content_areas()`
2. **Browse specific areas**: `browse_library("/")` then `browse_library("[area]")`
3. **Present a structured summary** of available content organized by category

Format output as:

```
## Fourth Marketing Knowledge Base

### Content Areas
| Area | Documents | Description |
|------|-----------|-------------|
| [area] | [count] | [description] |

### Quick Navigation
- For product details: browse `platform/`
- For competitive intel: browse `competitive/`
- For RFP answers: browse `rfp-responses/`
```

## Topic Research Workflow

When a user asks about a specific topic:

1. **Search broadly**: `search_knowledge("[topic]")`
2. **Retrieve top results**: `get_document("[top-result-1]")` and `get_document("[top-result-2]")`
3. **Search for related angles**: `search_knowledge("[related topic]")`
4. **Synthesize findings** into a structured summary

Format output as:

```
## [Topic] - Knowledge Base Summary

### Key Documents
1. **[Document Name]** ([path]) - [1-sentence summary]
2. **[Document Name]** ([path]) - [1-sentence summary]

### Key Facts & Metrics
- [Fact with source document]
- [Metric with source document]

### Coverage Assessment
- Well covered: [areas with strong content]
- Gaps identified: [areas needing more content]
```

## Content Audit Workflow

When a user wants to understand coverage:

1. **List all areas**: `list_content_areas()`
2. **Browse each area**: `browse_library("[area]")` for each category
3. **Assess coverage** against typical marketing needs:
   - Product content: every major product documented?
   - Competitive content: all key competitors covered?
   - Vertical content: all target verticals addressed?
   - RFP content: common RFP topics covered?
4. **Report gaps** with recommendations

Format output as:

```
## Content Audit Report

### Coverage Inventory
| Area | Documents | Coverage Score | Gaps |
|------|-----------|---------------|------|
| [area] | [count] | [High/Medium/Low] | [gaps] |

### Recommended Additions
1. [Missing topic] - Priority: [High/Medium/Low] - Reason: [why needed]
```

## Content Brief Workflow

When a user needs a brief for new content:

1. **Search existing content**: `search_knowledge("[topic]")`
2. **Identify what exists** vs. what's missing
3. **Pull key facts, metrics, and proof points** from existing documents
4. **Draft a content brief**

Format output as:

```
## Content Brief: [Topic]

### Target Audience
[Who this content is for]

### Key Messages (from existing content)
- [Message with source]

### Supporting Data Points (from existing content)
- [Metric with source]

### Gaps Requiring SME Input
- [Information not in the knowledge base]

### Suggested Structure
1. [Section with notes]
```

## Knowledge Base Structure

The knowledge base is organized into 7 content areas:

| Area | Path | Content |
|------|------|---------|
| Platform | `platform/` | Product details: HotSchedules, Fourth iQ, MacromatiX, Fuego, PeopleMatter, Payroll, Analytics, Workforce Management, Inventory Management, Services & Support |
| Integrations | `integrations/` | POS, payroll, HR, and API integration guides |
| Solutions | `solutions/` | Vertical briefs: QSR, casual dining, hotels, multi-location |
| Competitive | `competitive/` | Battle cards, market positioning, objection handling |
| Messaging | `messaging/` | Value props, proof points, elevator pitches, playbooks, packaging, solutions matrix |
| Compliance | `compliance/` | Security certifications, labor law, tip management |
| RFP Responses | `rfp-responses/` | Pre-approved answers for scheduling, inventory, HR, AI, implementation |

## Best Practices

- Always cite which documents information comes from
- Distinguish between facts from the knowledge base and synthesized conclusions
- When creating content briefs, clearly mark sourced elements vs. suggested new content
- If the knowledge base has conflicting information, flag it rather than choosing one version
- Present coverage gaps as opportunities, not criticisms

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Search returns too many results | Narrow search terms, filter by content area |
| Search returns no results | Try alternate terms, broader search, or browse by folder |
| Content seems contradictory | Flag both sources and recommend SME resolution |
| User wants content not in the knowledge base | Clearly state it's not available, suggest who to contact |

# Skill: Content Researcher

## Purpose
Browse, search, and summarize the Fourth marketing knowledge base for research and content creation.

## When to Use
Activate this skill when the user asks about:
- What content is available on a topic
- Summarizing a content area or document
- Finding specific information across multiple documents
- Creating content briefs or outlines based on existing approved content
- Identifying gaps in the knowledge base

## Workflow

### Content Discovery
When a user wants to explore what's available:

1. **Start with the overview**: `list_content_areas()`
2. **Browse specific areas**: `browse_library("/")` then `browse_library("[area]")`
3. **Present a structured summary** of what's available, organized by category

### Topic Research
When a user asks about a specific topic:

1. **Search broadly**: `search_knowledge("[topic]")`
2. **Retrieve top results**: `get_document("[top-result-1]")`, `get_document("[top-result-2]")`
3. **Search for related angles**: `search_knowledge("[related topic]")`
4. **Synthesize findings** into a structured summary with source citations

### Content Audit
When a user wants to understand coverage:

1. **List all areas**: `list_content_areas()`
2. **Browse each area**: `browse_library("[area]")` for each category
3. **Assess coverage** against typical marketing needs:
   - Product content: Is every product documented?
   - Competitive content: Are all key competitors covered?
   - Vertical content: Are all target verticals addressed?
   - RFP content: Are common RFP topics covered?
4. **Report gaps** with recommendations

### Content Brief Creation
When a user needs a brief for new content:

1. **Search existing content**: `search_knowledge("[topic]")`
2. **Identify what exists** and what's missing
3. **Pull key facts, metrics, and proof points** from existing documents
4. **Draft a content brief** with:
   - Topic and target audience
   - Key messages (sourced from existing content)
   - Supporting data points (sourced)
   - Gaps requiring SME input
   - Suggested structure

## Output Formats

### Topic Summary
```
## [Topic] - Knowledge Base Summary

### Key Documents
1. **[Document Name]** ([path]) - [1-sentence summary]
2. **[Document Name]** ([path]) - [1-sentence summary]

### Key Facts & Metrics
- [Fact with source]
- [Metric with source]

### Coverage Assessment
- Well covered: [areas]
- Gaps: [areas needing more content]
```

### Content Inventory
```
## Content Inventory: [Area]

| Document | Category | Word Count | Key Topics |
|----------|----------|------------|------------|
| [name] | [category] | [count] | [topics] |

### Coverage Score: [X/10]
### Recommended Additions: [list]
```

## Navigation Tips

The knowledge base is organized into these areas:
- **platform/** - Product-specific content (HotSchedules, Fourth iQ, MacromatiX, etc.)
- **integrations/** - POS, payroll, HR, API integration details
- **solutions/** - Vertical-specific content (QSR, casual dining, hotels, multi-location)
- **competitive/** - Battle cards, market positioning, objection handling
- **messaging/** - Value props, proof points, elevator pitches, playbooks, packaging
- **compliance/** - Security, labor law, tip management
- **rfp-responses/** - Pre-approved RFP answer templates

## Important
- Always cite which documents information comes from
- Distinguish between facts from the knowledge base and your own synthesis
- When creating content briefs, clearly mark which elements are sourced vs. suggested
- If the knowledge base has conflicting information, flag it rather than choosing one version

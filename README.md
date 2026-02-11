# Fourth Marketing Brain

AI-powered marketing knowledge MCP server for Fourth. Provides any AI tool (Claude, ChatGPT, Copilot) with access to curated marketing content via the Model Context Protocol.

## Quick Start

```bash
# Install dependencies
uv sync

# Run with MCP Inspector (development)
uv run fastmcp dev server.py

# Run as stdio server (for Claude Code)
uv run python server.py
```

## Architecture

```
FastMCP Server
├── Tools: search_knowledge, browse_library, get_document, ask_question, list_content_areas
├── Prompts: product_qa, rfp_draft, meeting_prep
└── Backend (swappable):
    ├── MockBackend    - local sample_content/ files (default)
    └── SharePointBackend - Microsoft Graph API (production)
```

## Configuration

Copy `.env.example` to `.env` and configure:

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND` | `mock` | Backend: `mock` or `sharepoint` |
| `MCP_TRANSPORT` | `stdio` | Transport: `stdio` or `http` |
| `MCP_PORT` | `8000` | HTTP port (when transport=http) |
| `AZURE_TENANT_ID` | - | Azure AD tenant (for SharePoint or HTTP auth) |
| `AZURE_CLIENT_ID` | - | Azure AD app client ID |
| `AZURE_CLIENT_SECRET` | - | Azure AD app client secret |
| `SHAREPOINT_SITE_NAME` | `MarketingKnowledgeBase` | SharePoint site to search |
| `BASE_URL` | - | Public HTTPS URL (required for HTTP transport) |
| `JWT_SIGNING_KEY` | - | Secret for signing tokens (defaults to client secret) |

## Client Setup

### Claude Code (stdio - local)

Add to your Claude Code MCP settings:

```json
{
  "mcpServers": {
    "fourth-marketing": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "C:/Users/david.hayes/fourth-marketing-brain",
      "env": {
        "BACKEND": "mock"
      }
    }
  }
}
```

### Claude.ai / ChatGPT Connector (HTTP - remote)

Once deployed to a public URL (see [Remote Deployment](#remote-deployment)):

1. Go to **claude.ai > Settings > Connectors**
2. Click **Add custom connector**
3. Enter your server URL: `https://your-server.up.railway.app/mcp/`
4. Claude auto-discovers OAuth metadata and prompts Azure AD login
5. Sign in with your company credentials (SSO)
6. Tools become available in all conversations

## Tools

| Tool | Description |
|------|-------------|
| `search_knowledge(query)` | Full-text search across all marketing content |
| `browse_library(folder_path)` | Browse knowledge repo folder structure |
| `get_document(name_or_id)` | Retrieve full text of a specific document |
| `ask_question(question)` | RAG-style Q&A with confidence indicators |
| `list_content_areas()` | List top-level content categories |

## Confidence Indicators

`ask_question` returns one of three confidence levels:

- **GROUNDED** - Answer found directly in approved content
- **PARTIAL** - Related content found, review recommended
- **NO ANSWER** - Nothing relevant found, SME input required

## Sample Content

The `sample_content/` directory includes demo documents:

- Enterprise Platform Playbook (architecture, modules, differentiators)
- Integration Guide (200+ POS, payroll, HR integrations)
- Packaging Comparison (Essentials vs Professional vs Enterprise)
- Value Propositions by Role (CFO, COO, CHRO, CTO, CEO)
- Analytics & Reporting (dashboards, reports, forecasting)
- RFP Responses (scheduling, security/compliance)
- Competitive Positioning (vs. generic HCM, point solutions, R365)

## Remote Deployment

Deploy as an HTTP server with Azure AD authentication so any team member can use it from Claude.ai, ChatGPT, or Copilot.

### Architecture

```
User clicks "Add Connector" in Claude.ai
  → Claude discovers /.well-known/oauth-protected-resource
  → FastMCP OAuthProxy redirects to Azure AD login
  → User signs in with company credentials (SSO)
  → Azure AD token flows through to Graph API
  → SharePoint returns only content the user can access
```

### Deployment Modes

| Mode | Backend | Transport | Auth | Use Case |
|------|---------|-----------|------|----------|
| Local dev | mock | stdio | None | Claude Code, MCP Inspector |
| Demo | mock | http | Azure AD | Show OAuth flow with sample content |
| Production | sharepoint | http | Azure AD | Real SharePoint content, per-user access |

### Deploy to Railway

1. Push this repo to GitHub
2. In Railway: **New Project > Deploy from GitHub**
3. Set environment variables:
   ```
   MCP_TRANSPORT=http
   BACKEND=mock
   BASE_URL=https://<your-app>.up.railway.app
   AZURE_TENANT_ID=<from IT>
   AZURE_CLIENT_ID=<from IT>
   AZURE_CLIENT_SECRET=<from IT>
   JWT_SIGNING_KEY=<random 32+ char string>
   ```
4. Railway auto-detects Python and deploys
5. Server is live at `https://<your-app>.up.railway.app`

### Azure AD App Registration

Request from IT (one-time setup):

- **App name:** `fourth-marketing-brain-mcp`
- **Platform:** Web
- **Redirect URI:** `https://<your-server>/auth/callback`
- **Client secret:** Yes
- **Delegated permissions** (NOT application):
  - `openid` + `profile` (sign-in)
  - `Sites.Read.All` (read SharePoint on behalf of user)
  - `Files.Read.All` (read files on behalf of user)
- **Admin consent:** Required for `Sites.Read.All`

### Phased Rollout

**Phase 1 (no IT needed):** Deploy with `BACKEND=mock`. Demo the full OAuth flow with sample content.

**Phase 2 (after IT provides app registration):** Set `BACKEND=sharepoint`. Users see real SharePoint content scoped to their permissions.

**Phase 3 (scale):** Share connector URL with wider team.

## SharePoint Setup (Production)

Requires Azure AD app registration with **delegated** permissions:
- `openid` + `profile` (sign-in)
- `Sites.Read.All` (delegated - reads as the signed-in user)
- `Files.Read.All` (delegated - reads as the signed-in user)
- Admin consent granted for `Sites.Read.All`

For local/service usage (stdio mode), application permissions with client credentials also work.

SharePoint site structure:
```
Marketing Knowledge Base/
├── Platform/
├── Solutions/
├── RFP Responses/
├── Competitive/
└── Messaging/
```

"""Fourth Marketing Brain - MCP Server

An AI-powered knowledge resource for Fourth's marketing content.
Provides tools for searching, browsing, and querying the marketing knowledge base.

Supports two deployment modes:
- stdio (local): No auth, for Claude Code / MCP Inspector
- http (remote): OAuthProxy with Azure AD, for Claude.ai / ChatGPT connectors
"""

import logging

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token

from config import config
from backends.base import KnowledgeBackend

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Auth setup (only for HTTP transport)
# ---------------------------------------------------------------------------

auth = None
if config.transport == "http" and config.azure_tenant_id and config.base_url:
    from fastmcp.server.auth import OAuthProxy
    from fastmcp.server.auth.providers.jwt import JWTVerifier

    class AzureADOAuthProxy(OAuthProxy):
        """OAuthProxy subclass that strips the `resource` parameter.

        Azure AD v2.0 doesn't support the `resource` query parameter
        (it was removed in favor of scoped permissions). The MCP protocol
        sends `resource=<server-url>` which OAuthProxy forwards by default,
        causing Azure AD to reject with AADSTS9010010.
        """

        def _build_upstream_authorize_url(self, txn_id: str, transaction: dict) -> str:
            url = super()._build_upstream_authorize_url(txn_id, transaction)
            # Strip the resource parameter that Azure AD v2.0 doesn't support
            from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
            parsed = urlparse(url)
            params = parse_qs(parsed.query, keep_blank_values=True)
            params.pop("resource", None)
            cleaned = urlunparse(parsed._replace(query=urlencode(params, doseq=True)))
            return cleaned

    tenant = config.azure_tenant_id

    # Accept both v1.0 and v2.0 Azure AD token formats
    v1_issuer = f"https://sts.windows.net/{tenant}/"
    v2_issuer = f"https://login.microsoftonline.com/{tenant}/v2.0"

    auth = AzureADOAuthProxy(
        upstream_authorization_endpoint=(
            f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize"
        ),
        upstream_token_endpoint=(
            f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
        ),
        upstream_client_id=config.azure_client_id,
        upstream_client_secret=config.azure_client_secret,
        token_verifier=JWTVerifier(
            jwks_uri=f"https://login.microsoftonline.com/{tenant}/discovery/v2.0/keys",
            issuer=[v1_issuer, v2_issuer],
            audience=[f"api://{config.azure_client_id}", config.azure_client_id],
        ),
        base_url=config.base_url,
        jwt_signing_key=config.jwt_signing_key or config.azure_client_secret,
        extra_authorize_params={
            "scope": f"openid profile api://{config.azure_client_id}/access_as_user",
        },
        require_authorization_consent=False,
    )
    logger.info("OAuthProxy configured for Azure AD tenant %s", tenant)


# ---------------------------------------------------------------------------
# Backend helpers
# ---------------------------------------------------------------------------

def _create_mock_backend() -> KnowledgeBackend:
    """Create singleton mock backend."""
    from backends.mock_backend import MockBackend
    return MockBackend(content_dir=config.sample_content_dir)


# Cache the mock backend singleton (created once, reused for all requests)
_mock_backend: KnowledgeBackend | None = None


def get_backend() -> KnowledgeBackend:
    """Get the appropriate backend for the current request.

    For SharePoint backend in HTTP mode: creates a per-request backend
    using the authenticated user's delegated token.
    For mock backend: returns a shared singleton.
    """
    global _mock_backend

    if config.backend == "sharepoint":
        from backends.sharepoint_backend import SharePointBackend

        # In HTTP mode, use the user's delegated token from OAuthProxy
        access_token = None
        if config.transport == "http":
            token_obj = get_access_token()
            if token_obj:
                access_token = token_obj.token

        if access_token:
            return SharePointBackend(
                site_name=config.sharepoint_site_name,
                user_token=access_token,
            )

        # Fallback: client credentials (for stdio mode or unauthenticated)
        return SharePointBackend(
            site_name=config.sharepoint_site_name,
            tenant_id=config.azure_tenant_id,
            client_id=config.azure_client_id,
            client_secret=config.azure_client_secret,
        )

    # Mock backend - shared singleton
    if _mock_backend is None:
        _mock_backend = _create_mock_backend()
    return _mock_backend


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "Fourth Marketing Brain",
    instructions=(
        "You are Fourth's internal marketing knowledge assistant. "
        "Use these tools to answer questions about Fourth's platform, products, "
        "integrations, competitive positioning, and value propositions. "
        "Always cite the source document when providing information. "
        "If you cannot find an answer, say so clearly."
    ),
    auth=auth,
)


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
async def search_knowledge(query: str, max_results: int = 10) -> str:
    """Search across all Fourth marketing content.

    Use this to find documents related to a topic, product, feature, or question.
    Returns document names, relevance scores, and summaries.

    Args:
        query: Search terms (e.g., "scheduling compliance", "integration POS")
        max_results: Maximum number of results to return (default 10)
    """
    be = get_backend()
    results = await be.search(query, max_results=max_results)

    if not results:
        return "No documents found matching your query."

    lines = [f"Found {len(results)} result(s):\n"]
    for i, doc in enumerate(results, 1):
        lines.append(
            f"{i}. **{doc.title}** (relevance: {doc.relevance_score})\n"
            f"   Category: {doc.content_area} | Path: {doc.path}\n"
            f"   {doc.summary}\n"
        )
    return "\n".join(lines)


@mcp.tool()
async def browse_library(folder_path: str = "/") -> str:
    """Browse the knowledge repository folder structure.

    Use this to discover what content is available and how it's organized.

    Args:
        folder_path: Path to browse (use "/" for root, or a subfolder like "rfp-responses")
    """
    be = get_backend()
    folders = await be.list_folders(folder_path)

    if not folders:
        return f"No folders found at path: {folder_path}"

    lines = [f"Contents of `{folder_path}`:\n"]
    for folder in folders:
        subfolder_info = f" (subfolders: {', '.join(folder.subfolders)})" if folder.subfolders else ""
        lines.append(f"- **{folder.name}/** - {folder.item_count} item(s){subfolder_info}")

    return "\n".join(lines)


@mcp.tool()
async def get_document(document_name_or_id: str) -> str:
    """Retrieve the full text of a specific document.

    Use this when you need the complete content of a document found via search
    or browse. Supports fuzzy matching on document names.

    Args:
        document_name_or_id: Document name, ID, or partial match
            (e.g., "enterprise-platform-playbook", "integration-guide")
    """
    be = get_backend()
    doc = await be.get_document(document_name_or_id)

    if not doc:
        return f"Document not found: '{document_name_or_id}'. Try search_knowledge to find available documents."

    return (
        f"# {doc.title}\n"
        f"**Path:** {doc.path} | **Type:** {doc.doc_type} | **Words:** {doc.word_count}\n"
        f"{'**Source:** ' + doc.source_url if doc.source_url else ''}\n\n"
        f"{doc.text}"
    )


@mcp.tool()
async def ask_question(question: str) -> str:
    """Answer a question using Fourth's approved marketing content (RAG-style).

    Searches relevant documents, extracts information, and provides an answer
    with source citations and a confidence indicator.

    Confidence levels:
    - GROUNDED: Answer found directly in approved content
    - PARTIAL: Related content found but not an exact match - review recommended
    - NO ANSWER: Nothing relevant in the knowledge base - SME input required

    Args:
        question: Natural language question about Fourth's products, platform,
            integrations, competitive positioning, etc.
    """
    # Search for relevant documents
    be = get_backend()
    results = await be.search(question, max_results=5)

    if not results:
        return (
            "**Confidence: NO ANSWER**\n\n"
            "No relevant content found in the marketing knowledge base for this question. "
            "SME input is required. Consider reaching out to the product marketing team."
        )

    # Gather full text from top results
    sources = []
    full_texts = []
    for result in results[:3]:  # Use top 3 docs
        doc = await be.get_document(result.id)
        if doc:
            full_texts.append(f"[Source: {doc.title}]\n{doc.text}")
            sources.append(f"- {doc.title} ({doc.path})")

    if not full_texts:
        return (
            "**Confidence: NO ANSWER**\n\n"
            "Documents were found but could not be retrieved. "
            "Please try get_document with a specific document name."
        )

    # Determine confidence based on relevance scores
    top_score = results[0].relevance_score
    if top_score >= 3.0:
        confidence = "GROUNDED"
        confidence_note = "Answer found and grounded in approved Fourth content."
    elif top_score >= 1.0:
        confidence = "PARTIAL"
        confidence_note = "Related content found but may not be an exact match. Review recommended."
    else:
        confidence = "PARTIAL"
        confidence_note = "Loosely related content found. Verify with SME before using externally."

    # Build the answer context
    combined_context = "\n\n---\n\n".join(full_texts)

    return (
        f"**Confidence: {confidence}**\n"
        f"_{confidence_note}_\n\n"
        f"**Question:** {question}\n\n"
        f"**Relevant content from {len(full_texts)} source(s):**\n\n"
        f"{combined_context}\n\n"
        f"---\n"
        f"**Sources:**\n" + "\n".join(sources)
    )


@mcp.tool()
async def list_content_areas() -> str:
    """List all top-level content categories in the knowledge base.

    Use this to understand what topics are covered and navigate the content hierarchy.
    """
    be = get_backend()
    areas = await be.list_content_areas()

    if not areas:
        return "No content areas found."

    lines = ["**Fourth Marketing Knowledge Base - Content Areas:**\n"]
    for area in areas:
        lines.append(f"- **{area.name}** ({area.document_count} doc(s)): {area.description}")

    lines.append(
        "\n_Use `browse_library(folder_path)` to explore a specific area, "
        "or `search_knowledge(query)` to search across all content._"
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

@mcp.prompt()
def product_qa(question: str) -> str:
    """Answer product questions using only approved Fourth marketing sources.

    Args:
        question: The product question to answer
    """
    return (
        f"Answer the following question about Fourth's products and platform "
        f"using ONLY information from the Fourth Marketing Knowledge Base. "
        f"Use the search_knowledge and get_document tools to find relevant content. "
        f"Always cite the source document. If you cannot find the answer, say "
        f'"No answer found in approved content - SME input required."\n\n'
        f"Question: {question}"
    )


@mcp.prompt()
def rfp_draft(question: str) -> str:
    """Draft an RFP response with confidence indicator.

    Args:
        question: The RFP question to answer
    """
    return (
        f"Draft a 1-3 sentence RFP response to the following question. "
        f"Use the search_knowledge and get_document tools to find approved content. "
        f"Include a confidence flag:\n"
        f"- GROUNDED: Direct match in approved content\n"
        f"- PARTIAL: Related content but not exact\n"
        f"- NO ANSWER: Nothing relevant found\n\n"
        f"Be concise, professional, and factual. Do not speculate beyond "
        f"what's in the knowledge base.\n\n"
        f"RFP Question: {question}"
    )


@mcp.prompt()
def meeting_prep(persona: str, company_name: str = "the prospect") -> str:
    """Prepare talking points for a meeting with a specific persona.

    Args:
        persona: Target persona (e.g., "CFO", "COO", "CTO", "CHRO")
        company_name: Name of the company you're meeting with
    """
    return (
        f"Prepare talking points for a meeting with the {persona} at {company_name}. "
        f"Use the search_knowledge and get_document tools to find:\n"
        f"1. Value propositions relevant to a {persona}\n"
        f"2. Key proof points and metrics\n"
        f"3. Discovery questions to ask\n"
        f"4. Competitive positioning relevant to their likely alternatives\n\n"
        f"Format as a concise brief that a sales rep can review in 5 minutes."
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if config.transport == "http":
        mcp.run(transport="streamable-http", host="0.0.0.0", port=config.http_port)
    else:
        mcp.run(transport="stdio")

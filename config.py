"""Environment-based configuration for the Fourth Marketing Brain MCP server."""

import os
from dataclasses import dataclass, field


@dataclass
class Config:
    # Backend: "mock", "sharepoint", or "cosmos"
    backend: str = field(default_factory=lambda: os.getenv("BACKEND", "mock"))

    # Transport: "stdio" or "http"
    transport: str = field(default_factory=lambda: os.getenv("MCP_TRANSPORT", "stdio"))
    http_port: int = field(default_factory=lambda: int(os.getenv("MCP_PORT", "8000")))

    # Auth mode: "proxy" (OAuthProxy for Railway), "easyauth" (Azure Container Apps), or "" (none/stdio)
    auth_mode: str = field(default_factory=lambda: os.getenv("AUTH_MODE", "proxy"))

    # SharePoint / Azure AD settings
    azure_tenant_id: str = field(default_factory=lambda: os.getenv("AZURE_TENANT_ID", ""))
    azure_client_id: str = field(default_factory=lambda: os.getenv("AZURE_CLIENT_ID", ""))
    azure_client_secret: str = field(default_factory=lambda: os.getenv("AZURE_CLIENT_SECRET", ""))
    sharepoint_site_name: str = field(
        default_factory=lambda: os.getenv("SHAREPOINT_SITE_NAME", "MarketingKnowledgeBase")
    )

    # Remote server settings (required when MCP_TRANSPORT=http)
    base_url: str = field(default_factory=lambda: os.getenv("BASE_URL", ""))
    jwt_signing_key: str = field(default_factory=lambda: os.getenv("JWT_SIGNING_KEY", ""))

    # Cosmos DB settings (required when BACKEND=cosmos)
    cosmos_endpoint: str = field(default_factory=lambda: os.getenv("COSMOS_ENDPOINT", ""))
    cosmos_key: str = field(default_factory=lambda: os.getenv("COSMOS_KEY", ""))
    cosmos_database: str = field(default_factory=lambda: os.getenv("COSMOS_DATABASE", "mcp-content"))

    # Azure AI Search settings (required when BACKEND=cosmos)
    search_endpoint: str = field(default_factory=lambda: os.getenv("SEARCH_ENDPOINT", ""))
    search_key: str = field(default_factory=lambda: os.getenv("SEARCH_KEY", ""))
    search_index: str = field(default_factory=lambda: os.getenv("SEARCH_INDEX", "mcp-marketing"))

    # Mock backend settings
    sample_content_dir: str = field(
        default_factory=lambda: os.getenv(
            "SAMPLE_CONTENT_DIR",
            os.path.join(os.path.dirname(__file__), "sample_content"),
        )
    )

    @property
    def graph_base_url(self) -> str:
        return "https://graph.microsoft.com/v1.0"

    @property
    def authority(self) -> str:
        return f"https://login.microsoftonline.com/{self.azure_tenant_id}"

    @property
    def graph_scopes(self) -> list[str]:
        return ["https://graph.microsoft.com/.default"]


config = Config()

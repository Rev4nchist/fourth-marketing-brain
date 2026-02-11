"""SharePoint backend using Microsoft Graph API + MSAL authentication."""

import asyncio
import logging

import httpx
import msal

from .base import KnowledgeBackend, Document, DocumentContent, Folder, ContentArea
from document_parser import extract_text

logger = logging.getLogger(__name__)


class SharePointBackend(KnowledgeBackend):
    """Production backend that reads from a SharePoint document library via Graph API.

    Supports two auth modes:
    - user_token: Delegated auth via OAuthProxy (remote MCP server).
      The user's Azure AD token is passed per-request.
    - client credentials: App-level auth via MSAL (local/service usage).
      Falls back to this when no user_token is provided.
    """

    def __init__(
        self,
        site_name: str,
        *,
        user_token: str | None = None,
        tenant_id: str = "",
        client_id: str = "",
        client_secret: str = "",
    ):
        self.site_name = site_name
        self.base_url = "https://graph.microsoft.com/v1.0"
        self._site_id: str | None = None
        self._drive_id: str | None = None
        self._user_token = user_token

        # Only set up MSAL if using client credentials (no user token)
        self._msal_app = None
        if not user_token and tenant_id and client_id and client_secret:
            self._msal_app = msal.ConfidentialClientApplication(
                client_id,
                authority=f"https://login.microsoftonline.com/{tenant_id}",
                client_credential=client_secret,
            )
        self._http = httpx.AsyncClient(timeout=30.0)

    async def _get_token(self) -> str:
        """Get access token - delegated user token or client credentials."""
        if self._user_token:
            return self._user_token

        if not self._msal_app:
            raise RuntimeError("No user token and no client credentials configured")

        result = self._msal_app.acquire_token_for_client(
            scopes=["https://graph.microsoft.com/.default"]
        )
        if "access_token" in result:
            return result["access_token"]
        raise RuntimeError(f"Token acquisition failed: {result.get('error_description', result)}")

    async def _graph_get(self, path: str, params: dict | None = None) -> dict:
        """Make authenticated GET request to Graph API with retry."""
        token = await self._get_token()
        headers = {"Authorization": f"Bearer {token}"}

        for attempt in range(3):
            resp = await self._http.get(
                f"{self.base_url}{path}",
                headers=headers,
                params=params,
            )
            if resp.status_code == 429:
                retry_after = int(resp.headers.get("Retry-After", 2 ** attempt))
                logger.warning(f"Rate limited, retrying in {retry_after}s")
                await asyncio.sleep(retry_after)
                continue
            resp.raise_for_status()
            return resp.json()

        raise RuntimeError(f"Graph API request failed after 3 retries: {path}")

    async def _graph_post(self, path: str, json_body: dict) -> dict:
        """Make authenticated POST request to Graph API."""
        token = await self._get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        for attempt in range(3):
            resp = await self._http.post(
                f"{self.base_url}{path}",
                headers=headers,
                json=json_body,
            )
            if resp.status_code == 429:
                retry_after = int(resp.headers.get("Retry-After", 2 ** attempt))
                await asyncio.sleep(retry_after)
                continue
            resp.raise_for_status()
            return resp.json()

        raise RuntimeError(f"Graph API POST failed after 3 retries: {path}")

    async def _ensure_site_and_drive(self):
        """Resolve site ID and default drive ID for the SharePoint site."""
        if self._site_id and self._drive_id:
            return

        # Search for the site by name
        data = await self._graph_get("/sites", params={"search": self.site_name})
        sites = data.get("value", [])
        if not sites:
            raise RuntimeError(f"SharePoint site '{self.site_name}' not found")

        self._site_id = sites[0]["id"]

        # Get the default document library drive
        drives = await self._graph_get(f"/sites/{self._site_id}/drives")
        drive_list = drives.get("value", [])
        if not drive_list:
            raise RuntimeError(f"No document libraries found on site '{self.site_name}'")

        self._drive_id = drive_list[0]["id"]

    async def search(self, query: str, max_results: int = 10) -> list[Document]:
        await self._ensure_site_and_drive()

        body = {
            "requests": [{
                "entityTypes": ["driveItem"],
                "query": {"queryString": query},
                "from": 0,
                "size": max_results,
            }]
        }
        data = await self._graph_post("/search/query", body)

        results = []
        hits = data.get("value", [{}])[0].get("hitsContainers", [{}])
        if hits:
            for hit in hits[0].get("hits", []):
                resource = hit.get("resource", {})
                results.append(Document(
                    id=resource.get("id", ""),
                    title=resource.get("name", "Untitled"),
                    summary=hit.get("summary", ""),
                    path=resource.get("parentReference", {}).get("path", ""),
                    content_area=_infer_content_area(resource),
                    source_url=resource.get("webUrl", ""),
                    relevance_score=hit.get("rank", 0),
                ))

        return results

    async def list_folders(self, path: str = "/") -> list[Folder]:
        await self._ensure_site_and_drive()

        if path == "/":
            endpoint = f"/drives/{self._drive_id}/root/children"
        else:
            endpoint = f"/drives/{self._drive_id}/root:/{path.strip('/')}:/children"

        data = await self._graph_get(endpoint)
        folders = []
        for item in data.get("value", []):
            if "folder" in item:
                folders.append(Folder(
                    name=item["name"],
                    path=f"{path.rstrip('/')}/{item['name']}",
                    item_count=item["folder"].get("childCount", 0),
                ))

        return folders

    async def get_document(self, id_or_path: str) -> DocumentContent | None:
        await self._ensure_site_and_drive()

        try:
            # Try as item ID first
            data = await self._graph_get(f"/drives/{self._drive_id}/items/{id_or_path}")
        except httpx.HTTPStatusError:
            # Try as path
            try:
                data = await self._graph_get(
                    f"/drives/{self._drive_id}/root:/{id_or_path.strip('/')}"
                )
            except httpx.HTTPStatusError:
                return None

        # Download the file content
        item_id = data["id"]
        token = await self._get_token()
        resp = await self._http.get(
            f"{self.base_url}/drives/{self._drive_id}/items/{item_id}/content",
            headers={"Authorization": f"Bearer {token}"},
            follow_redirects=True,
        )
        resp.raise_for_status()

        # For now, return raw text for supported types
        name = data.get("name", "")
        ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
        text = resp.text if ext in ("md", "txt") else f"[Binary {ext} file - {len(resp.content)} bytes]"

        return DocumentContent(
            id=item_id,
            title=name,
            text=text,
            path=data.get("parentReference", {}).get("path", "") + "/" + name,
            word_count=len(text.split()),
            doc_type=ext,
            source_url=data.get("webUrl", ""),
        )

    async def list_content_areas(self) -> list[ContentArea]:
        folders = await self.list_folders("/")
        return [
            ContentArea(
                name=f.name.replace("-", " ").title(),
                description=f"SharePoint folder: {f.name}",
                path=f.path,
                document_count=f.item_count,
            )
            for f in folders
        ]


def _infer_content_area(resource: dict) -> str:
    path = resource.get("parentReference", {}).get("path", "")
    parts = path.strip("/").split("/")
    # Skip "root:" prefix if present
    for part in parts:
        if part and part != "root:":
            return part
    return "General"

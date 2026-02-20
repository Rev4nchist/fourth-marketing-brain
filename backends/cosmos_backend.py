"""Azure Cosmos DB + AI Search backend for production deployment."""

import logging
from datetime import datetime, timezone
from typing import Any

from azure.cosmos.aio import CosmosClient
from azure.cosmos.exceptions import CosmosResourceExistsError, CosmosResourceNotFoundError
from azure.search.documents.aio import SearchClient

from .base import KnowledgeBackend, Document, DocumentContent, Folder, ContentArea, WriteResult

logger = logging.getLogger(__name__)


class CosmosBackend(KnowledgeBackend):
    """Production backend using Cosmos DB for storage and Azure AI Search for queries.

    Data model:
    - Cosmos DB 'documents' container: full document content, partitioned by /content_area
    - Cosmos DB 'content-areas' container: content area metadata, partitioned by /slug
    - Azure AI Search index: BM25 + semantic ranking over document text
    """

    def __init__(self, cosmos_client: CosmosClient, search_client: SearchClient, database_name: str):
        self._cosmos = cosmos_client
        self._search = search_client
        db = cosmos_client.get_database_client(database_name)
        self._documents_container = db.get_container_client("documents")
        self._areas_container = db.get_container_client("content-areas")

    async def search(self, query: str, max_results: int = 10) -> list[Document]:
        """Search using Azure AI Search (BM25 + optional semantic ranking)."""
        results: list[Document] = []

        try:
            search_results = await self._search.search(
                search_text=query,
                top=max_results,
                query_type="simple",
                select=["id", "title", "content_area", "summary", "path"],
            )

            async for result in search_results:
                score = result.get("@search.score", 0.0)
                results.append(Document(
                    id=result["id"],
                    title=result.get("title", ""),
                    summary=result.get("summary", ""),
                    path=result.get("path", ""),
                    content_area=result.get("content_area", ""),
                    relevance_score=round(score, 2),
                ))
        except Exception as e:
            logger.error("AI Search query failed, falling back to Cosmos: %s", e)
            results = await self._search_cosmos_fallback(query, max_results)

        return results

    async def _search_cosmos_fallback(self, query: str, max_results: int) -> list[Document]:
        """Fallback search using Cosmos DB CONTAINS when AI Search is unavailable."""
        terms = query.lower().split()
        if not terms:
            return []

        conditions = []
        parameters: list[dict[str, Any]] = []
        for i, term in enumerate(terms[:5]):
            param_name = f"@term{i}"
            conditions.append(
                f"(CONTAINS(LOWER(c.title), {param_name}) OR CONTAINS(LOWER(c.full_text), {param_name}))"
            )
            parameters.append({"name": param_name, "value": term})

        where_clause = " OR ".join(conditions)
        sql = f"SELECT c.id, c.title, c.content_area, c.summary, c.path FROM c WHERE {where_clause}"

        results: list[Document] = []
        async for item in self._documents_container.query_items(
            query=sql,
            parameters=parameters,
            max_item_count=max_results,
        ):
            results.append(Document(
                id=item["id"],
                title=item.get("title", ""),
                summary=item.get("summary", ""),
                path=item.get("path", ""),
                content_area=item.get("content_area", ""),
                relevance_score=1.0,
            ))

        return results[:max_results]

    async def get_document(self, id_or_path: str) -> DocumentContent | None:
        """Retrieve a document by ID (point read) or fuzzy path match."""
        # Normalize: accept both "competitive/market-positioning" and "competitive-market-positioning"
        cosmos_id = id_or_path.replace("/", "-")

        # Try exact ID match via cross-partition query
        sql = "SELECT * FROM c WHERE c.id = @id"
        async for item in self._documents_container.query_items(
            query=sql,
            parameters=[{"name": "@id", "value": cosmos_id}],
            max_item_count=1,
        ):
            return self._item_to_document_content(item)

        # Try fuzzy match on id or title
        normalized = id_or_path.lower().replace(" ", "-").replace("/", "-")
        sql_fuzzy = "SELECT * FROM c WHERE CONTAINS(LOWER(c.id), @term) OR CONTAINS(LOWER(c.title), @term)"
        async for item in self._documents_container.query_items(
            query=sql_fuzzy,
            parameters=[{"name": "@term", "value": normalized}],
            max_item_count=1,
        ):
            return self._item_to_document_content(item)

        return None

    async def list_folders(self, path: str = "/") -> list[Folder]:
        """List content areas as folders, or documents within a content area."""
        if path == "/" or not path:
            # Get all content areas and count in Python (GROUP BY not supported by async SDK)
            sql = "SELECT c.content_area FROM c"
            area_counts: dict[str, int] = {}
            async for item in self._documents_container.query_items(query=sql):
                area = item["content_area"]
                area_counts[area] = area_counts.get(area, 0) + 1

            folders: list[Folder] = []
            for area, count in area_counts.items():
                folders.append(Folder(
                    name=area,
                    path=area,
                    item_count=count,
                ))
            return sorted(folders, key=lambda f: f.name)

        # List documents in a specific content area
        area_name = path.strip("/")
        sql = "SELECT c.id, c.title FROM c WHERE c.content_area = @area"
        folders = []
        async for item in self._documents_container.query_items(
            query=sql,
            parameters=[{"name": "@area", "value": area_name}],
            partition_key=area_name,
        ):
            folders.append(Folder(
                name=item.get("title", item["id"]),
                path=f"{area_name}/{item['id']}",
                item_count=1,
            ))
        return sorted(folders, key=lambda f: f.name)

    async def list_content_areas(self) -> list[ContentArea]:
        """List all content areas from the content-areas container."""
        areas: list[ContentArea] = []

        try:
            sql = "SELECT * FROM c"
            async for item in self._areas_container.query_items(query=sql):
                areas.append(ContentArea(
                    name=item.get("name", ""),
                    description=item.get("description", ""),
                    path=item.get("slug", item.get("path", "")),
                    document_count=item.get("document_count", 0),
                ))
        except Exception as e:
            logger.warning("content-areas container query failed, deriving from documents: %s", e)
            sql = "SELECT c.content_area FROM c"
            area_counts: dict[str, int] = {}
            async for item in self._documents_container.query_items(query=sql):
                a = item["content_area"]
                area_counts[a] = area_counts.get(a, 0) + 1
            for a, count in area_counts.items():
                areas.append(ContentArea(
                    name=a.replace("-", " ").title(),
                    description=f"Content in {a}",
                    path=a,
                    document_count=count,
                ))

        return sorted(areas, key=lambda a: a.name)

    # --- Write operations ---

    async def _get_item_by_id(self, document_id: str) -> dict | None:
        """Fetch a raw Cosmos item by document_id (tries normalized and original)."""
        cosmos_id = document_id.replace("/", "-")
        sql = "SELECT * FROM c WHERE c.id = @id"
        async for item in self._documents_container.query_items(
            query=sql,
            parameters=[{"name": "@id", "value": cosmos_id}],
            max_item_count=1,
        ):
            return item

        # Try fuzzy
        normalized = document_id.lower().replace(" ", "-").replace("/", "-")
        sql_fuzzy = "SELECT * FROM c WHERE CONTAINS(LOWER(c.id), @term)"
        async for item in self._documents_container.query_items(
            query=sql_fuzzy,
            parameters=[{"name": "@term", "value": normalized}],
            max_item_count=1,
        ):
            return item

        return None

    async def _upsert_search_index(self, doc: dict) -> None:
        """Upload or update a document in the Azure AI Search index."""
        try:
            search_doc = {
                "id": doc["id"],
                "title": doc.get("title", ""),
                "content_area": doc.get("content_area", ""),
                "summary": doc.get("summary", ""),
                "path": doc.get("path", ""),
                "full_text": doc.get("full_text", ""),
            }
            await self._search.upload_documents(documents=[search_doc])
        except Exception as e:
            logger.warning("Search index update failed (non-fatal): %s", e)

    async def _remove_from_search_index(self, doc_id: str) -> None:
        """Remove a document from the Azure AI Search index."""
        try:
            await self._search.delete_documents(documents=[{"id": doc_id}])
        except Exception as e:
            logger.warning("Search index delete failed (non-fatal): %s", e)

    async def create_document(
        self, folder: str, filename: str, content: str,
        metadata: dict | None = None,
    ) -> WriteResult:
        cosmos_id = f"{folder}-{filename}"
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        meta = metadata or {}

        # Check if already exists
        existing = await self._get_item_by_id(cosmos_id)
        if existing:
            return WriteResult(
                success=False,
                path=f"{folder}/{filename}.md",
                message=f"Document already exists with id '{cosmos_id}'. Use update_document to modify it.",
            )

        # Build summary from first 200 chars
        summary = content[:200].replace("\n", " ").strip()
        if len(content) > 200:
            summary += "..."

        item = {
            "id": cosmos_id,
            "title": meta.get("title", filename.replace("-", " ").title()),
            "content_area": folder,
            "path": f"{folder}/{filename}.md",
            "full_text": content,
            "summary": summary,
            "word_count": len(content.split()),
            "doc_type": "markdown",
            "last_updated": meta.get("last_updated", now),
            "source": meta.get("source", "manual"),
            "confidence": meta.get("confidence", "NEEDS SME"),
            "tags": meta.get("tags", []),
        }

        await self._documents_container.create_item(body=item)
        await self._upsert_search_index(item)

        return WriteResult(
            success=True,
            path=f"{folder}/{filename}.md",
            message="Document created.",
        )

    async def update_document(
        self, document_id: str, content: str,
        metadata: dict | None = None,
    ) -> WriteResult:
        existing = await self._get_item_by_id(document_id)
        if not existing:
            return WriteResult(
                success=False,
                path=document_id,
                message=f"Document not found: '{document_id}'. Use create_document for new documents.",
            )

        now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        cosmos_id = existing["id"]
        content_area = existing["content_area"]

        # Backup: store previous version in a backups container or as a timestamped copy
        backup_id = f"{cosmos_id}_backup_{now}"
        backup_item = dict(existing)
        backup_item["id"] = backup_id
        backup_item["_backup_of"] = cosmos_id
        backup_item["_backed_up_at"] = now
        # Remove Cosmos system fields
        for key in ("_rid", "_self", "_etag", "_attachments", "_ts"):
            backup_item.pop(key, None)
        try:
            await self._documents_container.upsert_item(body=backup_item)
        except Exception as e:
            logger.warning("Backup creation failed: %s", e)

        # Update the document
        summary = content[:200].replace("\n", " ").strip()
        if len(content) > 200:
            summary += "..."

        meta = metadata or {}
        existing["full_text"] = content
        existing["summary"] = summary
        existing["word_count"] = len(content.split())
        existing["last_updated"] = now
        for k in ("title", "source", "confidence", "tags"):
            if k in meta:
                existing[k] = meta[k]

        await self._documents_container.upsert_item(body=existing)
        await self._upsert_search_index(existing)

        return WriteResult(
            success=True,
            path=existing.get("path", document_id),
            message=f"Document updated. Previous version backed up as {backup_id}.",
            backup_path=backup_id,
        )

    async def append_to_document(
        self, document_id: str, content: str,
        section_header: str | None = None,
    ) -> WriteResult:
        existing = await self._get_item_by_id(document_id)
        if not existing:
            return WriteResult(
                success=False,
                path=document_id,
                message=f"Document not found: '{document_id}'.",
            )

        separator = "\n\n---\n\n"
        if section_header:
            appended = f"## {section_header}\n\n{content}"
        else:
            appended = content

        existing["full_text"] = existing.get("full_text", "").rstrip() + separator + appended
        existing["word_count"] = len(existing["full_text"].split())
        existing["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Update summary if it was very short
        summary = existing["full_text"][:200].replace("\n", " ").strip()
        if len(existing["full_text"]) > 200:
            summary += "..."
        existing["summary"] = summary

        await self._documents_container.upsert_item(body=existing)
        await self._upsert_search_index(existing)

        return WriteResult(
            success=True,
            path=existing.get("path", document_id),
            message="Content appended to document.",
        )

    async def delete_document(self, document_id: str) -> WriteResult:
        existing = await self._get_item_by_id(document_id)
        if not existing:
            return WriteResult(
                success=False,
                path=document_id,
                message=f"Document not found: '{document_id}'.",
            )

        cosmos_id = existing["id"]
        content_area = existing["content_area"]
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Soft-delete: save as backup, then remove the original
        backup_id = f"{cosmos_id}_deleted_{now}"
        backup_item = dict(existing)
        backup_item["id"] = backup_id
        backup_item["_deleted_from"] = cosmos_id
        backup_item["_deleted_at"] = now
        for key in ("_rid", "_self", "_etag", "_attachments", "_ts"):
            backup_item.pop(key, None)

        try:
            await self._documents_container.upsert_item(body=backup_item)
        except Exception as e:
            logger.warning("Backup before delete failed: %s", e)

        # Delete original from Cosmos
        try:
            await self._documents_container.delete_item(item=cosmos_id, partition_key=content_area)
        except Exception as e:
            logger.error("Cosmos delete failed: %s", e)
            return WriteResult(success=False, path=document_id, message=f"Delete failed: {e}")

        # Remove from search index
        await self._remove_from_search_index(cosmos_id)

        return WriteResult(
            success=True,
            path=document_id,
            message="Document moved to backup. It can be restored from _backups/.",
            backup_path=backup_id,
        )

    @staticmethod
    def _item_to_document_content(item: dict) -> DocumentContent:
        return DocumentContent(
            id=item["id"],
            title=item.get("title", ""),
            text=item.get("full_text", ""),
            path=item.get("path", ""),
            word_count=item.get("word_count", 0),
            doc_type=item.get("doc_type", "markdown"),
        )

"""Azure Cosmos DB + AI Search backend for production deployment."""

import logging
from typing import Any

from azure.cosmos.aio import CosmosClient
from azure.search.documents.aio import SearchClient

from .base import KnowledgeBackend, Document, DocumentContent, Folder, ContentArea

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

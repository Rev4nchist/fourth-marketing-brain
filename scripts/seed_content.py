"""Seed Cosmos DB and Azure AI Search with content from sample_content/.

Usage:
    python scripts/seed_content.py --source sample_content/
    python scripts/seed_content.py --source sample_content/ --cosmos-db mcp-content --search-index mcp-marketing
    python scripts/seed_content.py --source sample_content/ --dry-run
"""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from document_parser import extract_text

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Content area descriptions (matches mock_backend)
AREA_DESCRIPTIONS = {
    "competitive": "Competitive positioning, battle cards, and objection handling",
    "rfp-responses": "Approved RFP response templates and examples",
    "platform": "Product details: HotSchedules, Fourth iQ, MacromatiX, Fuego, Payroll, and more",
    "solutions": "Solution briefs by vertical: QSR, casual dining, hotels, multi-location",
    "messaging": "Value propositions, proof points, elevator pitches, and playbooks",
    "integrations": "POS, payroll, HR, and API integration guides",
    "compliance": "Security certifications, labor law, and tip management compliance",
}


def build_documents(source_dir: Path) -> list[dict]:
    """Parse all content files into Cosmos DB document format."""
    documents = []
    for path in sorted(source_dir.rglob("*")):
        if not path.is_file() or path.suffix not in (".md", ".txt", ".docx", ".pdf", ".pptx"):
            continue

        rel = path.relative_to(source_dir)
        # Cosmos DB IDs can't contain '/', use '-' as separator
        doc_id = str(rel).replace("\\", "/").removesuffix(path.suffix).replace("/", "-")
        content_area = rel.parts[0] if len(rel.parts) > 1 else "general"

        parsed = extract_text(path)

        # Build summary: first non-heading, non-empty line >20 chars
        summary = ""
        for line in parsed["text"].split("\n"):
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and len(stripped) > 20:
                summary = stripped[:200] + ("..." if len(stripped) > 200 else "")
                break

        documents.append({
            "id": doc_id,
            "title": parsed["title"],
            "content_area": content_area,
            "full_text": parsed["text"],
            "summary": summary,
            "word_count": parsed["word_count"],
            "doc_type": parsed["doc_type"],
            "path": str(rel).replace("\\", "/"),
        })

    return documents


def build_content_areas(documents: list[dict]) -> list[dict]:
    """Derive content area metadata from documents."""
    area_counts: dict[str, int] = {}
    for doc in documents:
        area = doc["content_area"]
        area_counts[area] = area_counts.get(area, 0) + 1

    areas = []
    for slug, count in sorted(area_counts.items()):
        areas.append({
            "id": slug,
            "slug": slug,
            "name": slug.replace("-", " ").title(),
            "description": AREA_DESCRIPTIONS.get(slug, f"Content in {slug}"),
            "document_count": count,
        })
    return areas


async def seed_cosmos(documents: list[dict], content_areas: list[dict], endpoint: str, key: str, database: str):
    """Upsert documents and content areas into Cosmos DB."""
    from azure.cosmos.aio import CosmosClient

    async with CosmosClient(endpoint, credential=key) as client:
        db = client.get_database_client(database)
        docs_container = db.get_container_client("documents")
        areas_container = db.get_container_client("content-areas")

        logger.info("Seeding %d documents into Cosmos DB '%s'...", len(documents), database)
        for doc in documents:
            await docs_container.upsert_item(doc)
            logger.info("  Upserted: %s", doc["id"])

        logger.info("Seeding %d content areas...", len(content_areas))
        for area in content_areas:
            await areas_container.upsert_item(area)
            logger.info("  Upserted: %s", area["slug"])

    logger.info("Cosmos DB seeding complete.")


async def seed_search_index(documents: list[dict], endpoint: str, key: str, index_name: str):
    """Create/update AI Search index and upload documents."""
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient
    from azure.search.documents.indexes import SearchIndexClient
    from azure.search.documents.indexes.models import (
        SearchIndex,
        SearchField,
        SearchFieldDataType,
        SimpleField,
        SearchableField,
    )

    credential = AzureKeyCredential(key)

    # Create or update the index schema
    index_client = SearchIndexClient(endpoint=endpoint, credential=credential)

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True, filterable=True),
        SearchableField(name="title", type=SearchFieldDataType.String, analyzer_name="en.microsoft"),
        SimpleField(name="content_area", type=SearchFieldDataType.String, filterable=True, facetable=True),
        SearchableField(name="full_text", type=SearchFieldDataType.String, analyzer_name="en.microsoft"),
        SearchableField(name="summary", type=SearchFieldDataType.String),
        SimpleField(name="word_count", type=SearchFieldDataType.Int32, filterable=True, sortable=True),
        SimpleField(name="doc_type", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="path", type=SearchFieldDataType.String, filterable=True),
    ]

    index = SearchIndex(name=index_name, fields=fields)

    logger.info("Creating/updating search index '%s'...", index_name)
    index_client.create_or_update_index(index)

    # Upload documents
    search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)

    # Prepare documents for search (replace full_text key, add @search.action)
    search_docs = []
    for doc in documents:
        search_doc = {
            "@search.action": "mergeOrUpload",
            "id": doc["id"].replace("/", "-"),  # AI Search IDs can't contain /
            "title": doc["title"],
            "content_area": doc["content_area"],
            "full_text": doc["full_text"],
            "summary": doc["summary"],
            "word_count": doc["word_count"],
            "doc_type": doc["doc_type"],
            "path": doc["path"],
        }
        search_docs.append(search_doc)

    logger.info("Uploading %d documents to search index...", len(search_docs))
    result = search_client.upload_documents(documents=search_docs)
    succeeded = sum(1 for r in result if r.succeeded)
    logger.info("Search index: %d/%d documents uploaded successfully.", succeeded, len(search_docs))


async def main():
    parser = argparse.ArgumentParser(description="Seed Cosmos DB and AI Search with marketing content")
    parser.add_argument("--source", default="sample_content", help="Source content directory")
    parser.add_argument("--cosmos-endpoint", default=None, help="Cosmos DB endpoint (or COSMOS_ENDPOINT env)")
    parser.add_argument("--cosmos-key", default=None, help="Cosmos DB key (or COSMOS_KEY env)")
    parser.add_argument("--cosmos-db", default="mcp-content", help="Cosmos DB database name")
    parser.add_argument("--search-endpoint", default=None, help="AI Search endpoint (or SEARCH_ENDPOINT env)")
    parser.add_argument("--search-key", default=None, help="AI Search admin key (or SEARCH_KEY env)")
    parser.add_argument("--search-index", default="mcp-marketing", help="AI Search index name")
    parser.add_argument("--dry-run", action="store_true", help="Parse and show documents without uploading")
    parser.add_argument("--cosmos-only", action="store_true", help="Only seed Cosmos DB, skip AI Search")
    parser.add_argument("--search-only", action="store_true", help="Only seed AI Search, skip Cosmos DB")
    args = parser.parse_args()

    import os
    cosmos_endpoint = args.cosmos_endpoint or os.getenv("COSMOS_ENDPOINT", "")
    cosmos_key = args.cosmos_key or os.getenv("COSMOS_KEY", "")
    search_endpoint = args.search_endpoint or os.getenv("SEARCH_ENDPOINT", "")
    search_key = args.search_key or os.getenv("SEARCH_KEY", "")

    source_dir = Path(args.source)
    if not source_dir.exists():
        logger.error("Source directory does not exist: %s", source_dir)
        sys.exit(1)

    documents = build_documents(source_dir)
    content_areas = build_content_areas(documents)

    logger.info("Parsed %d documents across %d content areas", len(documents), len(content_areas))
    for area in content_areas:
        logger.info("  %s: %d docs", area["name"], area["document_count"])

    if args.dry_run:
        logger.info("\n--- DRY RUN: Documents ---")
        for doc in documents:
            logger.info("  %s | %s | %d words | area: %s", doc["id"], doc["title"], doc["word_count"], doc["content_area"])
        logger.info("\n--- DRY RUN: Content Areas ---")
        for area in content_areas:
            logger.info("  %s: %s (%d docs)", area["slug"], area["description"], area["document_count"])
        return

    if not args.search_only:
        if not cosmos_endpoint or not cosmos_key:
            logger.error("Cosmos DB credentials required. Set COSMOS_ENDPOINT and COSMOS_KEY env vars or use --cosmos-endpoint/--cosmos-key.")
            sys.exit(1)
        await seed_cosmos(documents, content_areas, cosmos_endpoint, cosmos_key, args.cosmos_db)

    if not args.cosmos_only:
        if not search_endpoint or not search_key:
            logger.error("AI Search credentials required. Set SEARCH_ENDPOINT and SEARCH_KEY env vars or use --search-endpoint/--search-key.")
            sys.exit(1)
        await seed_search_index(documents, search_endpoint, search_key, args.search_index)

    logger.info("Seeding complete!")


if __name__ == "__main__":
    asyncio.run(main())

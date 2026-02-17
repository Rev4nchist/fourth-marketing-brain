"""CLI for managing content in Cosmos DB.

Usage:
    python scripts/manage_content.py list
    python scripts/manage_content.py list --area competitive
    python scripts/manage_content.py get <document-id>
    python scripts/manage_content.py add <file-path> --area platform
    python scripts/manage_content.py delete <document-id> --area <content-area>
    python scripts/manage_content.py stats
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from document_parser import extract_text

import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


async def get_container(database_name: str, container_name: str = "documents"):
    from azure.cosmos.aio import CosmosClient
    endpoint = os.getenv("COSMOS_ENDPOINT", "")
    key = os.getenv("COSMOS_KEY", "")
    if not endpoint or not key:
        logger.error("Set COSMOS_ENDPOINT and COSMOS_KEY environment variables.")
        sys.exit(1)
    client = CosmosClient(endpoint, credential=key)
    db = client.get_database_client(database_name)
    return client, db.get_container_client(container_name)


async def cmd_list(args):
    client, container = await get_container(args.database)
    async with client:
        if args.area:
            sql = "SELECT c.id, c.title, c.word_count, c.content_area FROM c WHERE c.content_area = @area"
            params = [{"name": "@area", "value": args.area}]
            items = container.query_items(query=sql, parameters=params, partition_key=args.area)
        else:
            sql = "SELECT c.id, c.title, c.word_count, c.content_area FROM c"
            items = container.query_items(query=sql, enable_cross_partition_query=True)

        count = 0
        async for item in items:
            print(f"  {item['id']:40s} | {item.get('title', ''):50s} | {item.get('word_count', 0):5d} words | {item.get('content_area', '')}")
            count += 1
        print(f"\nTotal: {count} document(s)")


async def cmd_get(args):
    client, container = await get_container(args.database)
    async with client:
        sql = "SELECT * FROM c WHERE c.id = @id"
        async for item in container.query_items(
            query=sql,
            parameters=[{"name": "@id", "value": args.id}],
            enable_cross_partition_query=True,
            max_item_count=1,
        ):
            print(f"ID:           {item['id']}")
            print(f"Title:        {item.get('title', '')}")
            print(f"Content Area: {item.get('content_area', '')}")
            print(f"Word Count:   {item.get('word_count', 0)}")
            print(f"Doc Type:     {item.get('doc_type', '')}")
            print(f"Path:         {item.get('path', '')}")
            print(f"\n--- Full Text ---\n")
            print(item.get("full_text", "")[:2000])
            if len(item.get("full_text", "")) > 2000:
                print(f"\n... ({len(item['full_text'])} chars total, truncated)")
            return
        print(f"Document not found: {args.id}")


async def cmd_add(args):
    file_path = Path(args.file)
    if not file_path.exists():
        logger.error("File not found: %s", file_path)
        sys.exit(1)

    parsed = extract_text(file_path)
    doc_id = args.id or file_path.stem
    content_area = args.area or "general"

    summary = ""
    for line in parsed["text"].split("\n"):
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and len(stripped) > 20:
            summary = stripped[:200]
            break

    document = {
        "id": doc_id,
        "title": parsed["title"],
        "content_area": content_area,
        "full_text": parsed["text"],
        "summary": summary,
        "word_count": parsed["word_count"],
        "doc_type": parsed["doc_type"],
        "path": f"{content_area}/{doc_id}.{parsed['doc_type']}",
    }

    client, container = await get_container(args.database)
    async with client:
        await container.upsert_item(document)
        logger.info("Upserted document: %s (area: %s, %d words)", doc_id, content_area, parsed["word_count"])


async def cmd_delete(args):
    if not args.area:
        logger.error("--area is required for delete (partition key)")
        sys.exit(1)

    client, container = await get_container(args.database)
    async with client:
        await container.delete_item(item=args.id, partition_key=args.area)
        logger.info("Deleted document: %s (area: %s)", args.id, args.area)


async def cmd_stats(args):
    client, container = await get_container(args.database)
    async with client:
        sql = "SELECT c.content_area, COUNT(1) AS count FROM c GROUP BY c.content_area"
        total = 0
        async for item in container.query_items(query=sql, enable_cross_partition_query=True):
            print(f"  {item['content_area']:20s}: {item['count']} docs")
            total += item['count']
        print(f"\n  {'Total':20s}: {total} docs")


async def main():
    parser = argparse.ArgumentParser(description="Manage marketing content in Cosmos DB")
    parser.add_argument("--database", default=os.getenv("COSMOS_DATABASE", "mcp-content"), help="Cosmos DB database")

    sub = parser.add_subparsers(dest="command", required=True)

    list_p = sub.add_parser("list", help="List documents")
    list_p.add_argument("--area", default=None, help="Filter by content area")

    get_p = sub.add_parser("get", help="Get a document by ID")
    get_p.add_argument("id", help="Document ID")

    add_p = sub.add_parser("add", help="Add/update a document from file")
    add_p.add_argument("file", help="File path to import")
    add_p.add_argument("--area", required=True, help="Content area (partition key)")
    add_p.add_argument("--id", default=None, help="Document ID (default: filename stem)")

    del_p = sub.add_parser("delete", help="Delete a document")
    del_p.add_argument("id", help="Document ID")
    del_p.add_argument("--area", required=True, help="Content area (partition key)")

    sub.add_parser("stats", help="Show document counts by area")

    args = parser.parse_args()

    commands = {
        "list": cmd_list,
        "get": cmd_get,
        "add": cmd_add,
        "delete": cmd_delete,
        "stats": cmd_stats,
    }
    await commands[args.command](args)


if __name__ == "__main__":
    asyncio.run(main())

"""Mock backend that reads from local sample_content/ directory."""

import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .base import KnowledgeBackend, Document, DocumentContent, Folder, ContentArea, WriteResult
from document_parser import extract_text
from frontmatter import parse_frontmatter, generate_frontmatter, merge_metadata


class MockBackend(KnowledgeBackend):
    """Local file-based backend for demos and development."""

    def __init__(self, content_dir: str):
        self.content_dir = Path(content_dir)
        self._documents: dict[str, dict] | None = None

    def _index_documents(self) -> dict[str, dict]:
        """Build an in-memory index of all documents."""
        if self._documents is not None:
            return self._documents

        self._documents = {}
        for path in self.content_dir.rglob("*"):
            if path.is_file() and path.suffix in (".md", ".txt", ".docx", ".pdf", ".pptx"):
                rel = path.relative_to(self.content_dir)
                doc_id = str(rel).replace("\\", "/").removesuffix(path.suffix)
                parsed = extract_text(path)
                content_area = rel.parts[0] if len(rel.parts) > 1 else "General"
                self._documents[doc_id] = {
                    "id": doc_id,
                    "title": parsed["title"],
                    "text": parsed["text"],
                    "path": str(rel).replace("\\", "/"),
                    "content_area": content_area,
                    "word_count": parsed["word_count"],
                    "doc_type": parsed["doc_type"],
                    "file_path": str(path),
                }
        return self._documents

    async def search(self, query: str, max_results: int = 10) -> list[Document]:
        docs = self._index_documents()
        query_lower = query.lower()
        terms = query_lower.split()

        scored = []
        for doc_id, doc in docs.items():
            text_lower = doc["text"].lower()
            title_lower = doc["title"].lower()

            score = 0.0
            for term in terms:
                # Title matches weighted 3x
                if term in title_lower:
                    score += 3.0
                # Body matches
                count = text_lower.count(term)
                if count > 0:
                    score += min(count, 10) * 0.5

            if score > 0:
                summary = _extract_summary(doc["text"], terms)
                scored.append((score, Document(
                    id=doc_id,
                    title=doc["title"],
                    summary=summary,
                    path=doc["path"],
                    content_area=doc["content_area"],
                    relevance_score=round(score, 2),
                )))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:max_results]]

    async def list_folders(self, path: str = "/") -> list[Folder]:
        base = self.content_dir
        if path and path != "/":
            base = base / path.strip("/")

        if not base.exists() or not base.is_dir():
            return []

        folders = []
        for item in sorted(base.iterdir()):
            if item.is_dir():
                file_count = sum(1 for f in item.rglob("*") if f.is_file())
                subfolders = [d.name for d in item.iterdir() if d.is_dir()]
                folders.append(Folder(
                    name=item.name,
                    path=str(item.relative_to(self.content_dir)).replace("\\", "/"),
                    item_count=file_count,
                    subfolders=subfolders,
                ))

        # Also list files at this level
        files_here = [f for f in base.iterdir() if f.is_file()]
        if files_here and path == "/":
            # Show root-level docs as a virtual "General" entry
            pass

        return folders

    async def get_document(self, id_or_path: str) -> DocumentContent | None:
        docs = self._index_documents()

        # Try exact ID match
        if id_or_path in docs:
            doc = docs[id_or_path]
            return DocumentContent(
                id=doc["id"],
                title=doc["title"],
                text=doc["text"],
                path=doc["path"],
                word_count=doc["word_count"],
                doc_type=doc["doc_type"],
            )

        # Try fuzzy match on title or path
        id_lower = id_or_path.lower().replace(" ", "-")
        for doc_id, doc in docs.items():
            if id_lower in doc_id.lower() or id_lower in doc["title"].lower().replace(" ", "-"):
                return DocumentContent(
                    id=doc["id"],
                    title=doc["title"],
                    text=doc["text"],
                    path=doc["path"],
                    word_count=doc["word_count"],
                    doc_type=doc["doc_type"],
                )

        return None

    async def list_content_areas(self) -> list[ContentArea]:
        docs = self._index_documents()
        areas: dict[str, ContentArea] = {}

        # Top-level directories = content areas
        for item in sorted(self.content_dir.iterdir()):
            if item.is_dir():
                count = sum(1 for f in item.rglob("*") if f.is_file())
                areas[item.name] = ContentArea(
                    name=item.name.replace("-", " ").title(),
                    description=_area_description(item.name),
                    path=item.name,
                    document_count=count,
                )

        # Root-level files
        root_files = [f for f in self.content_dir.iterdir() if f.is_file()]
        if root_files:
            areas["general"] = ContentArea(
                name="General",
                description="Top-level marketing documents",
                path="/",
                document_count=len(root_files),
            )

        return list(areas.values())

    # --- Write operations ---

    def _invalidate_cache(self) -> None:
        """Clear the in-memory document index so it's rebuilt on next read."""
        self._documents = None

    def _backup_path(self, folder: str, filename: str, suffix: str = "") -> Path:
        """Return a backup file path with timestamp."""
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
        backup_dir = self.content_dir / "_backups" / folder
        backup_dir.mkdir(parents=True, exist_ok=True)
        label = suffix or ts
        return backup_dir / f"{filename}_{label}.md"

    async def create_document(
        self, folder: str, filename: str, content: str,
        metadata: dict | None = None,
    ) -> WriteResult:
        target_dir = self.content_dir / folder
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / f"{filename}.md"

        if target.exists():
            return WriteResult(
                success=False,
                path=f"{folder}/{filename}.md",
                message=f"Document already exists at {folder}/{filename}.md. Use update_document to modify it.",
            )

        # Build frontmatter
        meta = {
            "title": (metadata or {}).get("title", filename.replace("-", " ").title()),
            "folder": folder,
            "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "source": (metadata or {}).get("source", "manual"),
            "confidence": (metadata or {}).get("confidence", "NEEDS SME"),
        }
        if metadata:
            for k in ("tags", "title", "source", "confidence", "last_updated"):
                if k in metadata:
                    meta[k] = metadata[k]

        fm = generate_frontmatter(meta)
        target.write_text(fm + content, encoding="utf-8")
        self._invalidate_cache()

        return WriteResult(
            success=True,
            path=f"{folder}/{filename}.md",
            message="Document created.",
        )

    async def update_document(
        self, document_id: str, content: str,
        metadata: dict | None = None,
    ) -> WriteResult:
        docs = self._index_documents()
        if document_id not in docs:
            return WriteResult(
                success=False,
                path=document_id,
                message=f"Document not found: '{document_id}'. Use create_document for new documents.",
            )

        file_path = Path(docs[document_id]["file_path"])
        if not file_path.exists():
            return WriteResult(success=False, path=document_id, message="Source file missing on disk.")

        # Read existing content and frontmatter
        existing_text = file_path.read_text(encoding="utf-8")
        existing_meta, _ = parse_frontmatter(existing_text)

        # Backup
        parts = document_id.split("/", 1)
        folder = parts[0] if len(parts) > 1 else ""
        fname = parts[-1]
        backup = self._backup_path(folder, fname)
        shutil.copy2(str(file_path), str(backup))

        # Merge metadata and write
        merged = merge_metadata(existing_meta, metadata)
        fm = generate_frontmatter(merged)
        file_path.write_text(fm + content, encoding="utf-8")
        self._invalidate_cache()

        backup_rel = str(backup.relative_to(self.content_dir)).replace("\\", "/")
        return WriteResult(
            success=True,
            path=f"{document_id}.md" if not document_id.endswith(".md") else document_id,
            message=f"Document updated. Previous version backed up to {backup_rel}.",
            backup_path=backup_rel,
        )

    async def append_to_document(
        self, document_id: str, content: str,
        section_header: str | None = None,
    ) -> WriteResult:
        docs = self._index_documents()
        if document_id not in docs:
            return WriteResult(
                success=False,
                path=document_id,
                message=f"Document not found: '{document_id}'.",
            )

        file_path = Path(docs[document_id]["file_path"])
        existing_text = file_path.read_text(encoding="utf-8")

        # Update last_updated in frontmatter
        existing_meta, body = parse_frontmatter(existing_text)
        existing_meta["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        fm = generate_frontmatter(existing_meta)

        # Build appended section
        separator = "\n\n---\n\n"
        if section_header:
            appended = f"## {section_header}\n\n{content}"
        else:
            appended = content

        new_text = fm + body.rstrip() + separator + appended + "\n"
        file_path.write_text(new_text, encoding="utf-8")
        self._invalidate_cache()

        return WriteResult(
            success=True,
            path=f"{document_id}.md",
            message="Content appended to document.",
        )

    async def delete_document(self, document_id: str) -> WriteResult:
        docs = self._index_documents()
        if document_id not in docs:
            return WriteResult(
                success=False,
                path=document_id,
                message=f"Document not found: '{document_id}'.",
            )

        file_path = Path(docs[document_id]["file_path"])
        parts = document_id.split("/", 1)
        folder = parts[0] if len(parts) > 1 else ""
        fname = parts[-1]

        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
        backup = self._backup_path(folder, fname, suffix=f"deleted_{ts}")
        shutil.move(str(file_path), str(backup))
        self._invalidate_cache()

        backup_rel = str(backup.relative_to(self.content_dir)).replace("\\", "/")
        return WriteResult(
            success=True,
            path=document_id,
            message=f"Document moved to backup. It can be restored from _backups/.",
            backup_path=backup_rel,
        )


def _extract_summary(text: str, terms: list[str], max_len: int = 200) -> str:
    """Extract a relevant snippet from text matching search terms."""
    lines = text.split("\n")
    for line in lines:
        line_lower = line.lower().strip()
        if any(term in line_lower for term in terms) and len(line.strip()) > 20:
            snippet = line.strip()
            if len(snippet) > max_len:
                snippet = snippet[:max_len] + "..."
            return snippet

    # Fallback: first non-heading, non-empty line
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and len(stripped) > 20:
            return stripped[:max_len] + ("..." if len(stripped) > max_len else "")

    return text[:max_len] + "..." if len(text) > max_len else text


def _area_description(folder_name: str) -> str:
    descriptions = {
        "competitive": "Competitive positioning, battle cards, and objection handling",
        "rfp-responses": "Approved RFP response templates and examples",
        "platform": "Product details: HotSchedules, Fourth iQ, MacromatiX, Fuego, Payroll, and more",
        "solutions": "Solution briefs by vertical: QSR, casual dining, hotels, multi-location",
        "messaging": "Value propositions, proof points, elevator pitches, and playbooks",
        "integrations": "POS, payroll, HR, and API integration guides",
        "compliance": "Security certifications, labor law, and tip management compliance",
    }
    return descriptions.get(folder_name, f"Content in {folder_name}")

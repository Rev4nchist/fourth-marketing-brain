"""Mock backend that reads from local sample_content/ directory."""

import os
from pathlib import Path

from .base import KnowledgeBackend, Document, DocumentContent, Folder, ContentArea
from document_parser import extract_text


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

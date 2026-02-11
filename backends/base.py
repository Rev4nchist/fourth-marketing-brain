"""Abstract backend interface for knowledge sources."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Document:
    """Search result metadata."""
    id: str
    title: str
    summary: str
    path: str
    content_area: str
    source_url: str = ""
    relevance_score: float = 0.0


@dataclass
class DocumentContent:
    """Full document with extracted text."""
    id: str
    title: str
    text: str
    path: str
    word_count: int = 0
    doc_type: str = "markdown"
    source_url: str = ""


@dataclass
class Folder:
    """A folder/category in the knowledge repo."""
    name: str
    path: str
    item_count: int = 0
    subfolders: list[str] = field(default_factory=list)


@dataclass
class ContentArea:
    """Top-level content category."""
    name: str
    description: str
    path: str
    document_count: int = 0


class KnowledgeBackend(ABC):
    """Abstract interface for knowledge repository backends.

    Implementations: MockBackend (local files), SharePointBackend (Graph API).
    """

    @abstractmethod
    async def search(self, query: str, max_results: int = 10) -> list[Document]:
        """Full-text search across all documents."""

    @abstractmethod
    async def list_folders(self, path: str = "/") -> list[Folder]:
        """List folders/subfolders at a given path."""

    @abstractmethod
    async def get_document(self, id_or_path: str) -> DocumentContent | None:
        """Retrieve full text of a specific document."""

    @abstractmethod
    async def list_content_areas(self) -> list[ContentArea]:
        """List top-level content categories."""

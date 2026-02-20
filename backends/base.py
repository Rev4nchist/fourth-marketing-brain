"""Abstract backend interface for knowledge sources."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# Valid content area folders for write operations
VALID_FOLDERS = (
    "platform", "competitive", "messaging", "solutions",
    "rfp-responses", "compliance", "integrations",
)


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
class WriteResult:
    """Result of a write operation."""
    success: bool
    path: str = ""
    message: str = ""
    backup_path: str = ""


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

    Implementations: MockBackend (local files), CosmosBackend (Azure Cosmos DB + AI Search).
    """

    # --- Read operations ---

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

    # --- Write operations ---

    @abstractmethod
    async def create_document(
        self, folder: str, filename: str, content: str,
        metadata: dict | None = None,
    ) -> WriteResult:
        """Create a new document. Fails if it already exists."""

    @abstractmethod
    async def update_document(
        self, document_id: str, content: str,
        metadata: dict | None = None,
    ) -> WriteResult:
        """Replace an existing document's content. Creates a backup first."""

    @abstractmethod
    async def append_to_document(
        self, document_id: str, content: str,
        section_header: str | None = None,
    ) -> WriteResult:
        """Append content to an existing document."""

    @abstractmethod
    async def delete_document(self, document_id: str) -> WriteResult:
        """Soft-delete a document by moving it to _backups/."""

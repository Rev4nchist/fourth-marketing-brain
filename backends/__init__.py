"""Knowledge backends for the Fourth Marketing Brain."""

from .base import KnowledgeBackend, Document, DocumentContent, Folder, ContentArea, WriteResult, VALID_FOLDERS
from .mock_backend import MockBackend

__all__ = [
    "KnowledgeBackend",
    "Document",
    "DocumentContent",
    "Folder",
    "ContentArea",
    "WriteResult",
    "VALID_FOLDERS",
    "MockBackend",
]

# CosmosBackend imported lazily in server.py to avoid requiring Azure SDK when using mock backend

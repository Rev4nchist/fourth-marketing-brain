"""Knowledge backends for the Fourth Marketing Brain."""

from .base import KnowledgeBackend, Document, DocumentContent, Folder, ContentArea
from .mock_backend import MockBackend

__all__ = [
    "KnowledgeBackend",
    "Document",
    "DocumentContent",
    "Folder",
    "ContentArea",
    "MockBackend",
]

# CosmosBackend imported lazily in server.py to avoid requiring Azure SDK when using mock backend

"""
DocumentLoader interface.
 
Single Responsibility: turn something on disk into Document objects.
Open/Closed: add a PDFLoader, HTMLLoader, etc. later without touching
this file or anything that depends on it.
"""
from abc import ABC, abstractmethod
from src.models import Document

class DocumentLoader(ABC):
    @abstractmethod
    def load(self, file_path: str) -> list[Document]:
        """Read one or more documents from disk and return them as a list of Document objects."""
        raise NotImplementedError("Subclasses must implement the load method.")

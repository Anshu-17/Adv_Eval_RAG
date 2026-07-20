"""
Chunker interface. Single Resposibility: split a Document into chunks.
"""
from abc import ABC, abstractmethod
from src.models import Document, Chunk

class Chunker(ABC):
    @abstractmethod
    def chunk(self, document: Document) -> list[Chunk]:
        raise NotImplementedError("Chunker subclasses must implement the chunk method.")
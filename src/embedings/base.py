from abc import ABC, abstractmethod
from typing import List

class Embedder(ABC):
    @abstractmethod
    def embed_texts(self, texts: list[str])-> List[list[float]]:
        raise NotImplementedError("Embedder subclasses must implement the embed_texts method.")
    
    @abstractmethod
    def embed_query(self, text: str) -> list[float]:
        raise NotImplementedError("Embedder subclasses must implement the embed_query method.")
    
    
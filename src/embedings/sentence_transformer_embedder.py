"""
Local embedder using sentence-transformers. Deliberately chosen over an API
embedder (OpenAI/Cohere) as the default so you can run the whole pipeline
offline while prototyping — swap in an API-based Embedder implementation
later without touching anything else, since everything depends on the
Embedder interface, not this class.
 
Using BAAI/bge-m3: unlike bge-small/bge-large or e5-family models, bge-m3
does NOT require an instruction prefix on queries — passing the raw query
text directly is the documented/correct usage.
"""
from sentence_transformers import SentenceTransformer
 
from src.embeddings.base import Embedder
from config.settings import EmbeddingConfig

class SentenceTransformerEmbedder(Embedder):
    def __init__(self, congig: EmbeddingConfig):
        self.model = SentenceTransformer(congig.model_name)
        
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, show_progress_bar=False).tolist()
    
    def embed_query(self, text: str) -> list[float]:
        return self._model.encode([text], show_progress_bar=False)[0].tolist()
from dataclasses import dataclass, field
from typing import List, Optional
import os

@dataclass(frozen=True)
class ChunkingConfig:
    parent_chunk_size: int = 2000
    parent_chunk_overlap: int = 200
    child_chunk_size: int = 400
    child_chunk_overlap: int = 50
    
@dataclass(frozen=True)
class EmbeddingConfig:
    model_name: str = "BAAI/bge-m3"
    vector_size: int = 1024
    
@dataclass(frozen=True)
class PineconeConfig:
    api_key: str = os.environ.get("PINECONE_API_KEY", "")
    index_name: str = "adv_eval_rag"
    cloud: str = "aws"          
    region: str = "us-east-1"
    metric: str = "cosine"
    namespace: str = "default"
    
@dataclass(frozen=True)
class GenerationConfig:
    api_key: str = os.getenv("GOOGLE_GENAI_API_KEY", "")
    model_name: str = "gemini-2.5-flash"
    temperature: float = 0.1
    max_output_tokens: int = 1024
    
    
@dataclass(frozen=True)
class RerankerConfig:
    top_k: int = 5
    provider: str = "cohere"
    
@dataclass(frozen=True)
class RetrievalConfig:
    dense_top_k: int =10
    sparse_top_k: int =10
    rrf_k:int =60
    
@dataclass(frozen=True)
class AppConfig:
    data_raw_dir: str = "data/raw"
    data_processed_dir: str = "data/processed"
    chunking: ChunkingConfig = field(default_factory=ChunkingConfig)
    embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)
    pinecone: PineconeConfig = field(default_factory=PineconeConfig)
    generation: GenerationConfig = field(default_factory=GenerationConfig)
    reranker: RerankerConfig = field(default_factory=RerankerConfig)
    retrieval: RetrievalConfig = field(default_factory=RetrievalConfig)
    
def load_config() -> AppConfig:
    """Factory function — swap this out later for env-var/YAML-driven config
    without changing anything that consumes AppConfig."""
    return AppConfig() 
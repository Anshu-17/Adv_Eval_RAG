"""
Parent-child chunker.

Design note (from our earlier architecture discussion): child chunks are the
retrieval unit and should NOT be single sentences — small paragraphs embed
more reliably. Parent chunks are what actually gets passed to the LLM as
context, and split on markdown headers first so we never cut mid-section for
structured legal/regulatory text.
"""
import hashlib
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from src.chunkers.base import Chunker
from src.models import Document, Chunk
from config.settings import ChunkingConfig


class ParentChildMarkdownChunker(Chunker):
    def __init__(self, config: ChunkingConfig):
        self._config = config
        self._header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")],
            strip_headers=False,
        )
        self._parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.parent_chunk_size,
            chunk_overlap=config.parent_chunk_overlap,
            separators=["\n\n", "\n", ". ", " "],
        )
        self._child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.child_chunk_size,
            chunk_overlap=config.child_chunk_overlap,
            separators=["\n\n", "\n", ". ", " "],
        )

    def chunk(self, document: Document) -> list[Chunk]:
        header_sections = self._header_splitter.split_text(document.content)
        chunks: list[Chunk] = []

        for section in header_sections:
            parent_texts = self._parent_splitter.split_text(section.page_content)

            for parent_text in parent_texts:
                parent_id = self._make_id(document.id, parent_text)
                child_texts = self._child_splitter.split_text(parent_text)

                for child_text in child_texts:
                    child_id = self._make_id(document.id, child_text, salt=parent_id)
                    chunks.append(Chunk(
                        id=child_id,
                        text=child_text,
                        parent_id=parent_id,
                        parent_text=parent_text,
                        metadata=document.metadata,
                    ))

        return chunks

    @staticmethod
    def _make_id(doc_id: str, text: str, salt: str = "") -> str:
        return hashlib.sha256(f"{doc_id}{salt}{text}".encode()).hexdigest()[:16]
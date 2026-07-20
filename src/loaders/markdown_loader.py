"""
Concrete loader for markdown files with YAML frontmatter (like your
data/raw/dodd_frank_act_2010.md). This is the only place that knows
about frontmatter parsing — nothing downstream cares how metadata got read.
"""
import os
import glob
import hashlib
import frontmatter

from src.loaders.base import DocumentLoader
from src.models import Document, DocumentMetadata, Visibility


class MarkdownFrontmatterLoader(DocumentLoader):
    def load(self, path: str) -> list[Document]:
        pattern = path if path.endswith(".md") else os.path.join(path, "**/*.md")
        files = glob.glob(pattern, recursive=True)

        documents = []
        for filepath in files:
            post = frontmatter.load(filepath)
            metadata = DocumentMetadata(
                source=post.get("source", os.path.basename(filepath)),
                doc_type=post.get("doc_type", "unknown"),
                jurisdiction=post.get("jurisdiction", "unknown"),
                visibility=Visibility(post.get("visibility", "external")),
                url=post.get("url"),
                extra={k: v for k, v in post.metadata.items()
                       if k not in {"source", "doc_type", "jurisdiction", "visibility", "url"}},
            )
            doc_id = hashlib.sha256(filepath.encode()).hexdigest()[:16]
            documents.append(Document(id=doc_id, content=post.content, metadata=metadata))

        return documents
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

"""
Domain models shared across the pipeline.
 
Keeping these in one place (rather than each module inventing its own dict shape)
is what lets loaders, chunkers, embedders, and stores all speak the same language
without depending on each other directly.
"""

class Visibility(str,Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    
@dataclass
class DocumentMetadata:
    source: str
    doc_type: str
    jurisdiction: str
    visibility: Visibility = Visibility.INTERNAL
    url: Optional[str] = None
    extra : dict = field(default_factory=dict)

@dataclass
class Document:
    id: str
    content: str
    metadata: DocumentMetadata
    
@dataclass
class Chunk:
    id: str
    tesxt: str
    parent_id: str
    parent_text: str
    metadata: DocumentMetadata
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Document:
    document_id: str
    title: str
    text: str
    tenant_id: str = "demo"
    classification: str = "internal"
    metadata: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    document_id: str
    title: str
    text: str
    tenant_id: str
    classification: str

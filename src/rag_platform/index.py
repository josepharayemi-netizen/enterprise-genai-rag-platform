import hashlib
import json
import math
import re
from pathlib import Path

from .models import Chunk, Document
from .security import redact_pii

TOKEN = re.compile(r"[a-z0-9]+")


def embed(text: str, dimensions: int = 256) -> list[float]:
    vector = [0.0] * dimensions
    for token in TOKEN.findall(text.lower()):
        digest = hashlib.sha256(token.encode()).digest()
        vector[int.from_bytes(digest[:2], "big") % dimensions] += 1.0
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def similarity(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def chunk_document(document: Document, words: int = 120, overlap: int = 20) -> list[Chunk]:
    tokens = redact_pii(document.text).split()
    step = max(1, words - overlap)
    chunks = []
    for offset in range(0, len(tokens), step):
        content = " ".join(tokens[offset : offset + words])
        if not content:
            continue
        chunk_id = hashlib.sha256(f"{document.document_id}:{offset}:{content}".encode()).hexdigest()[:16]
        chunks.append(Chunk(chunk_id, document.document_id, document.title, content, document.tenant_id, document.classification))
    return chunks


class VectorIndex:
    def __init__(self, chunks: list[Chunk] | None = None):
        self.chunks = chunks or []
        self.vectors = [embed(chunk.text) for chunk in self.chunks]

    def add(self, documents: list[Document]) -> None:
        for document in documents:
            for chunk in chunk_document(document):
                self.chunks.append(chunk)
                self.vectors.append(embed(chunk.text))

    def search(self, question: str, tenant_id: str, limit: int = 4) -> list[tuple[float, Chunk]]:
        query = embed(question)
        scored = [(similarity(query, vector), chunk) for vector, chunk in zip(self.vectors, self.chunks) if chunk.tenant_id == tenant_id]
        return sorted(scored, key=lambda item: item[0], reverse=True)[:limit]

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = [{**chunk.__dict__, "vector": vector} for chunk, vector in zip(self.chunks, self.vectors)]
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "VectorIndex":
        if not path.exists():
            return cls()
        payload = json.loads(path.read_text(encoding="utf-8"))
        instance = cls()
        for item in payload:
            vector = item.pop("vector")
            instance.chunks.append(Chunk(**item))
            instance.vectors.append(vector)
        return instance

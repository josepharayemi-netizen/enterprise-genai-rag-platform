import hashlib
from pathlib import Path

from .index import VectorIndex
from .models import Document


def ingest_directory(source: Path, output: Path = Path("data/index.json"), tenant_id: str = "demo") -> dict:
    documents = []
    for path in sorted(source.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        documents.append(Document(hashlib.sha256(str(path).encode()).hexdigest()[:12], path.stem.replace("_", " ").title(), text, tenant_id))
    index = VectorIndex()
    index.add(documents)
    index.save(output)
    return {"documents": len(documents), "chunks": len(index.chunks), "output": str(output)}

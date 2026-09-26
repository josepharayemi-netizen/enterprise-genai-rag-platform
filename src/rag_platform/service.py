import re
from pathlib import Path

from .index import VectorIndex
from .security import validate_question


class RAGService:
    def __init__(self, index_path: Path = Path("data/index.json")):
        self.index = VectorIndex.load(index_path)

    def answer(self, question: str, tenant_id: str = "demo") -> dict:
        safe_question = validate_question(question)
        results = self.index.search(safe_question, tenant_id)
        relevant = [(score, chunk) for score, chunk in results if score >= 0.08]
        if not relevant:
            return {"answer": "I do not have enough approved evidence to answer that question.", "citations": [], "grounded": False, "provider": "local-extractive"}
        keywords = set(re.findall(r"[a-z0-9]+", safe_question.lower()))
        candidates = []
        for _, chunk in relevant:
            for sentence in re.split(r"(?<=[.!?])\s+", chunk.text):
                overlap = len(keywords & set(re.findall(r"[a-z0-9]+", sentence.lower())))
                candidates.append((overlap, sentence, chunk))
        _, sentence, _ = max(candidates, key=lambda item: item[0])
        citations = [{"chunk_id": chunk.chunk_id, "document_id": chunk.document_id, "title": chunk.title, "score": round(score, 4)} for score, chunk in relevant]
        return {"answer": sentence, "citations": citations, "grounded": True, "provider": "local-extractive"}

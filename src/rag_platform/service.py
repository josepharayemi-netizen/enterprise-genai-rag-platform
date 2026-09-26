import re
from pathlib import Path

from .index import VectorIndex
from .security import validate_question

TOKEN = re.compile(r"[a-z0-9]+")
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "do", "does", "for", "from", "how", "i",
    "in", "is", "it", "of", "on", "or", "should", "that", "the", "their", "this", "to", "was", "what",
    "when", "where", "which", "who", "with", "you",
}


def content_tokens(text: str) -> set[str]:
    """Return meaningful lexical evidence tokens for transparent local retrieval."""
    normalized = re.sub(r"\bnot\s+enough\b", "insufficient", text.lower())
    tokens = set()
    for token in TOKEN.findall(normalized):
        if token in STOPWORDS:
            continue
        if len(token) > 4 and token.endswith("ies"):
            token = f"{token[:-3]}y"
        elif len(token) > 4 and token.endswith("s") and not token.endswith("ss"):
            token = token[:-1]
        tokens.add(token)
    return tokens


class RAGService:
    def __init__(self, index_path: Path = Path("data/index.json")):
        self.index = VectorIndex.load(index_path)

    def answer(self, question: str, tenant_id: str = "demo") -> dict:
        safe_question = validate_question(question)
        results = self.index.search(safe_question, tenant_id)
        query_tokens = content_tokens(safe_question)
        relevant = []
        for score, chunk in results:
            lexical_overlap = query_tokens.intersection(content_tokens(chunk.text))
            if len(lexical_overlap) >= 2 or (score >= 0.08 and lexical_overlap):
                relevant.append((score, chunk))
        if not relevant:
            return {"answer": "I do not have enough approved evidence to answer that question.", "citations": [], "grounded": False, "provider": "local-extractive"}
        keywords = query_tokens
        candidates = []
        for _, chunk in relevant:
            for sentence in re.split(r"(?<=[.!?])\s+", chunk.text):
                overlap_tokens = keywords & content_tokens(sentence)
                overlap = len(overlap_tokens)
                specificity = sum(len(token) for token in overlap_tokens)
                candidates.append((overlap, specificity, sentence, chunk))
        _, _, sentence, _ = max(candidates, key=lambda item: (item[0], item[1]))
        citations = [{"chunk_id": chunk.chunk_id, "document_id": chunk.document_id, "title": chunk.title, "score": round(score, 4)} for score, chunk in relevant]
        return {"answer": sentence, "citations": citations, "grounded": True, "provider": "local-extractive"}

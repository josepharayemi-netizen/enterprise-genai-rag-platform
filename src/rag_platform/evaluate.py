import json
from pathlib import Path

from .service import RAGService


def evaluate(dataset_path: Path, service: RAGService | None = None) -> dict:
    service = service or RAGService()
    cases = json.loads(dataset_path.read_text(encoding="utf-8"))
    passed = 0
    injection_blocked = 0
    for case in cases:
        try:
            result = service.answer(case["question"], case.get("tenant_id", "demo"))
            success = all(term.lower() in result["answer"].lower() for term in case.get("expected_terms", []))
            success = success and bool(result["citations"]) == case.get("expect_citations", True)
        except ValueError:
            success = case.get("expect_blocked", False)
            injection_blocked += int(success)
        passed += int(success)
    score = passed / len(cases) if cases else 0.0
    return {"cases": len(cases), "passed": passed, "score": round(score, 4), "injection_blocked": injection_blocked, "gate_passed": score >= 0.8}

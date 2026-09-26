import json
import math
import statistics
import time
from collections import defaultdict
from pathlib import Path

from .service import RAGService
from .security import validate_question


def evaluate(dataset_path: Path, service: RAGService | None = None) -> dict:
    service = service or RAGService()
    cases = json.loads(dataset_path.read_text(encoding="utf-8"))
    passed = 0
    injection_blocked = 0
    expected_citation_cases = 0
    cited_expected_cases = 0
    latencies_ms = []
    category_counts = defaultdict(lambda: {"cases": 0, "passed": 0})
    details = []
    for case in cases:
        category = case.get("category", "uncategorized")
        category_counts[category]["cases"] += 1
        failure_reason = None
        started = time.perf_counter()
        try:
            safe_question = validate_question(case["question"])
            result = service.answer(case["question"], case.get("tenant_id", "demo"))
            success = all(term.lower() in result["answer"].lower() for term in case.get("expected_terms", []))
            success = success and bool(result["citations"]) == case.get("expect_citations", True)
            if case.get("expect_citations", True):
                expected_citation_cases += 1
                cited_expected_cases += int(bool(result["citations"]))
            forbidden_terms = case.get("forbidden_terms", [])
            if case.get("expect_redaction", False):
                redacted = all(term.lower() not in safe_question.lower() for term in forbidden_terms)
                redacted = redacted and all(term.lower() not in result["answer"].lower() for term in forbidden_terms)
                success = success and redacted
                if not redacted:
                    failure_reason = "sensitive value was not redacted"
        except ValueError:
            success = case.get("expect_blocked", False)
            if category == "injection":
                injection_blocked += int(success)
            if not success:
                failure_reason = "unexpected validation block"
        latency_ms = (time.perf_counter() - started) * 1000
        latencies_ms.append(latency_ms)
        passed += int(success)
        category_counts[category]["passed"] += int(success)
        if not success and failure_reason is None:
            failure_reason = "response did not satisfy expected behavior"
        details.append(
            {
                "id": case.get("id"),
                "category": category,
                "passed": success,
                "latency_ms": round(latency_ms, 4),
                "failure_reason": failure_reason,
            }
        )
    score = passed / len(cases) if cases else 0.0
    categories = {
        name: {
            **counts,
            "score": round(counts["passed"] / counts["cases"], 4) if counts["cases"] else 0.0,
        }
        for name, counts in sorted(category_counts.items())
    }
    ordered_latencies = sorted(latencies_ms)
    p95_index = max(0, math.ceil(0.95 * len(ordered_latencies)) - 1) if ordered_latencies else 0
    return {
        "cases": len(cases),
        "passed": passed,
        "score": round(score, 4),
        "injection_blocked": injection_blocked,
        "citation_coverage": round(cited_expected_cases / expected_citation_cases, 4) if expected_citation_cases else None,
        "median_latency_ms": round(statistics.median(latencies_ms), 4) if latencies_ms else None,
        "p95_latency_ms": round(ordered_latencies[p95_index], 4) if ordered_latencies else None,
        "categories": categories,
        "gate_passed": score >= 0.8,
        "details": details,
    }

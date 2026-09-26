import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from .service import RAGService

RATING_FIELDS = ("behavior_correct", "answer_supported", "safe_response")
ALLOWED_RATINGS = {"yes", "no", "uncertain"}


def create_annotation_pack(
    dataset_path: Path,
    output_path: Path,
    service: RAGService | None = None,
) -> dict:
    """Create a deterministic blind review pack without expected labels."""
    cases = json.loads(dataset_path.read_text(encoding="utf-8"))
    service = service or RAGService()
    rows = []
    for position, case in enumerate(cases, start=1):
        try:
            result = service.answer(case["question"], case.get("tenant_id", "demo"))
            response = result["answer"]
            citation_count = len(result["citations"])
        except ValueError as error:
            response = f"[BLOCKED] {error}"
            citation_count = 0
        rows.append(
            {
                "item_id": case.get("id", f"case-{position:03d}"),
                "prompt": case["question"],
                "system_response": response,
                "citation_count": citation_count,
                "behavior_correct": "",
                "answer_supported": "",
                "safe_response": "",
                "reviewer_confidence": "",
                "notes": "",
            }
        )
    rows.sort(key=lambda row: hashlib.sha256(f"annotation-v1:{row['item_id']}".encode()).hexdigest())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys() if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    return {"items": len(rows), "output": str(output_path), "expected_labels_included": False}


def _read_ratings(path: Path) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    ratings = {}
    for row in rows:
        item_id = row.get("item_id", "").strip()
        if not item_id or item_id in ratings:
            raise ValueError(f"missing or duplicate item_id in {path}")
        for field in RATING_FIELDS:
            value = row.get(field, "").strip().lower()
            if value not in ALLOWED_RATINGS:
                raise ValueError(f"{field} for {item_id} must be yes, no or uncertain")
        ratings[item_id] = row
    return ratings


def _cohen_kappa(left: list[str], right: list[str]) -> float | None:
    if not left:
        return None
    observed = sum(a == b for a, b in zip(left, right)) / len(left)
    left_counts, right_counts = Counter(left), Counter(right)
    expected = sum((left_counts[label] / len(left)) * (right_counts[label] / len(right)) for label in ALLOWED_RATINGS)
    if expected == 1.0:
        return 1.0 if observed == 1.0 else None
    return round((observed - expected) / (1 - expected), 4)


def calculate_agreement(first_path: Path, second_path: Path) -> dict:
    first, second = _read_ratings(first_path), _read_ratings(second_path)
    if set(first) != set(second):
        raise ValueError("review files must contain the same item_id values")
    item_ids = sorted(first)
    fields = {}
    for field in RATING_FIELDS:
        left = [first[item_id][field].strip().lower() for item_id in item_ids]
        right = [second[item_id][field].strip().lower() for item_id in item_ids]
        agreement = sum(a == b for a, b in zip(left, right)) / len(item_ids) if item_ids else 0.0
        fields[field] = {"percent_agreement": round(agreement, 4), "cohen_kappa": _cohen_kappa(left, right)}
    return {"items": len(item_ids), "fields": fields}

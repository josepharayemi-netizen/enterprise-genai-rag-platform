import json
from pathlib import Path

from .security import detect_prompt_injection


def evaluate_security(dataset_path: Path) -> dict:
    cases = json.loads(dataset_path.read_text(encoding="utf-8"))
    tp = tn = fp = fn = 0
    details = []
    for case in cases:
        predicted = detect_prompt_injection(case["text"])
        expected = case["expect_injection"]
        tp += int(predicted and expected)
        tn += int(not predicted and not expected)
        fp += int(predicted and not expected)
        fn += int(not predicted and expected)
        details.append(
            {
                "id": case["id"],
                "group": case["group"],
                "expected_injection": expected,
                "predicted_injection": predicted,
                "passed": predicted == expected,
            }
        )
    total = len(cases)
    return {
        "cases": total,
        "passed": tp + tn,
        "accuracy": round((tp + tn) / total, 4) if total else 0.0,
        "true_positives": tp,
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "attack_recall": round(tp / (tp + fn), 4) if tp + fn else None,
        "benign_specificity": round(tn / (tn + fp), 4) if tn + fp else None,
        "precision": round(tp / (tp + fp), 4) if tp + fp else None,
        "details": details,
    }


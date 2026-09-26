import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

from .evaluate import evaluate
from .service import RAGService


def run_experiment(dataset_path: Path, repeats: int = 5, index_path: Path = Path("data/index.json")) -> dict:
    if repeats < 1:
        raise ValueError("repeats must be at least 1")
    dataset_bytes = dataset_path.read_bytes()
    service = RAGService(index_path)
    runs = [evaluate(dataset_path, service) for _ in range(repeats)]
    signatures = [
        [(case["id"], case["passed"]) for case in run["details"]]
        for run in runs
    ]
    return {
        "schema_version": "1.0",
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": str(dataset_path),
        "dataset_sha256": hashlib.sha256(dataset_bytes).hexdigest(),
        "repeats": repeats,
        "deterministic_outcomes": all(signature == signatures[0] for signature in signatures[1:]),
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "provider": "local-extractive",
        },
        "runs": runs,
    }


def write_experiment(result: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")


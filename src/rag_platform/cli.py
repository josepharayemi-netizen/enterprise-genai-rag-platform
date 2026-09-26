import argparse
import json
from pathlib import Path

from .evaluate import evaluate
from .ingest import ingest_directory


def main() -> None:
    parser = argparse.ArgumentParser(description="Enterprise RAG platform CLI")
    commands = parser.add_subparsers(dest="command", required=True)
    ingest = commands.add_parser("ingest")
    ingest.add_argument("source", type=Path)
    evaluation = commands.add_parser("evaluate")
    evaluation.add_argument("dataset", type=Path)
    args = parser.parse_args()
    result = ingest_directory(args.source) if args.command == "ingest" else evaluate(args.dataset)
    print(json.dumps(result, indent=2))
    if args.command == "evaluate" and not result["gate_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

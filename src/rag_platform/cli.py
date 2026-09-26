import argparse
import json
from pathlib import Path

from .evaluate import evaluate
from .experiment import run_experiment, write_experiment
from .ingest import ingest_directory


def main() -> None:
    parser = argparse.ArgumentParser(description="Enterprise RAG platform CLI")
    commands = parser.add_subparsers(dest="command", required=True)
    ingest = commands.add_parser("ingest")
    ingest.add_argument("source", type=Path)
    evaluation = commands.add_parser("evaluate")
    evaluation.add_argument("dataset", type=Path)
    experiment = commands.add_parser("experiment")
    experiment.add_argument("dataset", type=Path)
    experiment.add_argument("--repeats", type=int, default=5)
    experiment.add_argument("--output", type=Path, default=Path("evaluation/results/local_experiment.json"))
    args = parser.parse_args()
    if args.command == "ingest":
        result = ingest_directory(args.source)
    elif args.command == "experiment":
        result = run_experiment(args.dataset, args.repeats)
        write_experiment(result, args.output)
    else:
        result = evaluate(args.dataset)
    print(json.dumps(result, indent=2))
    if args.command == "evaluate" and not result["gate_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

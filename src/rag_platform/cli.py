import argparse
import json
from pathlib import Path

from .evaluate import evaluate
from .experiment import run_experiment, write_experiment
from .ingest import ingest_directory
from .security_evaluate import evaluate_security
from .annotation import calculate_agreement, create_annotation_pack


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
    security_evaluation = commands.add_parser("security-evaluate")
    security_evaluation.add_argument("dataset", type=Path)
    annotation_pack = commands.add_parser("annotation-pack")
    annotation_pack.add_argument("dataset", type=Path)
    annotation_pack.add_argument("--output", type=Path, default=Path("evaluation/annotation/reviewer_pack.csv"))
    agreement = commands.add_parser("annotation-agreement")
    agreement.add_argument("first", type=Path)
    agreement.add_argument("second", type=Path)
    args = parser.parse_args()
    if args.command == "ingest":
        result = ingest_directory(args.source)
    elif args.command == "experiment":
        result = run_experiment(args.dataset, args.repeats)
        write_experiment(result, args.output)
    elif args.command == "security-evaluate":
        result = evaluate_security(args.dataset)
    elif args.command == "annotation-pack":
        result = create_annotation_pack(args.dataset, args.output)
    elif args.command == "annotation-agreement":
        result = calculate_agreement(args.first, args.second)
    else:
        result = evaluate(args.dataset)
    print(json.dumps(result, indent=2))
    if args.command == "evaluate" and not result["gate_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

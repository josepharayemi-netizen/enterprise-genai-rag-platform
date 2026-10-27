"""Reproduce local diagnostics; never treat this public set as independent evidence."""
import hashlib
import json
import subprocess
import sys
import tempfile
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.rag_platform import index, security
from src.rag_platform.evaluate import evaluate
from src.rag_platform.ingest import ingest_directory
from src.rag_platform.service import RAGService


def main():
    dataset = Path('evaluation/candidate_test_set.json')
    results = {}
    for config in ('full_controls', 'no_injection_detector', 'no_pii_redaction'):
        with tempfile.TemporaryDirectory() as directory, ExitStack() as stack:
            if config == 'no_injection_detector':
                stack.enter_context(patch.object(security, 'detect_prompt_injection', return_value=False))
            if config == 'no_pii_redaction':
                stack.enter_context(patch.object(security, 'redact_pii', side_effect=lambda text: text))
                stack.enter_context(patch.object(index, 'redact_pii', side_effect=lambda text: text))
            index_path = Path(directory) / 'index.json'
            ingest_directory(Path('examples/knowledge'), index_path)
            results[config] = evaluate(dataset, RAGService(index_path))
    report = {
        'status': 'diagnostic_only_not_independent_validation',
        'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        'working_diff_sha256': hashlib.sha256(subprocess.check_output(['git', 'diff', 'HEAD'])).hexdigest(),
        'dataset_sha256': hashlib.sha256(dataset.read_bytes()).hexdigest(),
        'python': sys.version,
        'limitations': [
            'Small public synthetic development-authored set; no generalization claim.',
            'Single deterministic run per configuration; latency is descriptive only.',
            'Ablations use temporary in-memory patches, never production controls.',
            'No relevance or tenant-filter ablation implemented in this audit.',
            'No cloud or generative model was evaluated.'
        ],
        'results': results,
    }
    output = Path('research/validation/local_diagnostics.json')
    output.write_text(json.dumps(report, indent=2) + '\n')
    for name, result in results.items():
        print(name, result['passed'], '/', result['cases'], 'injections blocked:', result['injection_blocked'])


if __name__ == '__main__':
    main()

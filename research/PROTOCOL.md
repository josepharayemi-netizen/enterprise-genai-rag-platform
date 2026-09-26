# Reproducible Research Protocol

## Working title

**Secure and Responsible Retrieval-Augmented Generation for Resource-Constrained Organizations: A Multi-Cloud Reference Architecture and Experimental Evaluation**

## Research objective

Evaluate whether a lightweight, security- and governance-aware RAG pipeline can improve grounded response behavior and resist common prompt and privacy attacks while remaining reproducible without paid cloud services.

## Research questions

- **RQ1 — Retrieval:** How reliably does the platform retrieve approved evidence for answerable questions?
- **RQ2 — Grounding:** How often do answers contain a citation and remain supported by retrieved evidence?
- **RQ3 — Safety:** How reliably are known prompt-injection patterns blocked?
- **RQ4 — Privacy:** How reliably is supported personally identifiable information redacted before retrieval or processing?
- **RQ5 — Portability:** What latency, cost and operational differences arise across local, AWS and Azure deployment paths?

## Hypotheses

- H1: The guarded pipeline achieves at least 0.80 end-to-end task success on the frozen benchmark.
- H2: It blocks at least 0.90 of the benchmark's explicit prompt-injection attacks.
- H3: It redacts 1.00 of the PII formats explicitly supported by the implementation.
- H4: It abstains on at least 0.80 of questions for which no approved evidence exists.

These are preregistered targets, not measured claims. Report all results, including failures.

## Experimental design

1. Freeze the code, documents and benchmark with a Git tag.
2. Run each deterministic local case five times to confirm repeatability.
3. Run cloud configurations only after recording region, model/version, instance/service tier and prices observed on the execution date.
4. Preserve raw JSON outputs and an environment manifest for every run.
5. Compare the full guarded configuration with the following ablations:
   - no prompt-injection detector;
   - no PII redaction;
   - no relevance threshold/abstention;
   - no tenant filter.
6. Do not tune on the frozen candidate test set after observing its results. Any subsequent control improvements must be evaluated on a newly versioned, independently annotated test set.

## Dataset status

- `evaluation/research_benchmark.json` is the 20-case development benchmark and may be used for debugging.
- `evaluation/candidate_test_set.json` is the frozen 40-case candidate test set first executed on 2026-09-26.
- Its SHA-256 digest is `cca9e7f04561c3fbbd5703c6e3f8114385931f262252a0df86457997980e363f`.
- The candidate set was constructed during development and is not independently annotated. It must not be described as an external benchmark.
- Failures observed in this set are preserved. A future independently prepared set is required to evaluate any revised controls.
- `evaluation/security_robustness_v2.json` is a separate 36-case post-baseline robustness set: 24 adversarial inputs and 12 benign controls.
- Version 2 security results must be reported separately from the original frozen 40-case baseline because the implementation changed.
- The v2 set was also authored within the study and is diagnostic, not an independent security benchmark.

## Primary metrics

| Metric | Definition |
|---|---|
| Retrieval hit rate | Cases where expected approved evidence appears in retrieved results / answerable cases |
| Citation coverage | Answered cases containing at least one source citation / answered cases |
| End-to-end success | Cases satisfying their expected behavior / all cases |
| Injection block rate | Blocked attack cases / injection attack cases |
| PII redaction recall | Sensitive values redacted / supported sensitive values presented |
| Abstention accuracy | Unsupported questions correctly refused / unsupported questions |
| Latency | Median and p95 wall-clock response time in milliseconds |
| Cost | Estimated provider cost per 1,000 queries, with assumptions disclosed |

## Reporting rules

- Report counts and proportions, not percentages alone.
- Add bootstrap 95% confidence intervals when the test set is sufficiently large.
- Separate deterministic local results from managed-model results.
- Never present synthetic evidence as real organizational data.
- Record negative and unexpected findings.
- State that the benchmark covers only the documented threat patterns and is not proof of universal security.

## Reproduction

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m src.rag_platform.cli ingest examples/knowledge
python -m src.rag_platform.cli evaluate evaluation/research_benchmark.json
python -m src.rag_platform.cli experiment evaluation/candidate_test_set.json --repeats 5 --output evaluation/results/local_candidate_test.json
python -m src.rag_platform.cli security-evaluate evaluation/security_robustness_v2.json
pytest -q
```

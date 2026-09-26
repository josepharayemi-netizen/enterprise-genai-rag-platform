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
6. Do not tune on the final test set. Expand data into development and test partitions before making research claims.

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
pytest -q
```


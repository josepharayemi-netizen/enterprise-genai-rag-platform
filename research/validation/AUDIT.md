# Local research validation audit — 27 October 2026

## Decision

Keep the existing archives. Develop the first RAG report into a stronger revised contribution. This audit is internal reproducibility work, not independent expert review, peer review, or evidence of production-model robustness.

## Reproduction

The historical code at commit `3e19a3b` reproduced 34/40 successes and 5/8 blocked attacks, matching the committed baseline counts. Five repetitions had identical pass/fail outcomes. The historical dataset hash matches the protocol. Fresh latency measurements differ by environment and must not replace historical measurements silently.

The newer code at `d03898c` produced 36/40 successes and 7/8 blocked attacks. This is a diagnostic result on a known public set after security changes, not a new held-out validation. Retain both versions and failures.

## Corrections

- The manuscript's claimed first-run latency did not match the checked-in first run. Corrected to 0.1307 ms median and 0.1901 ms p95 from the original committed result, not the new run.
- A returned answer/abstention could satisfy an `expect_blocked` case when its other checks happened to pass. Such cases now explicitly fail unless validation rejects them. This did not change the current full-control total on these 40 cases.
- Cohen's kappa is undefined when both raters use the same single category throughout. Return null rather than reporting 1.0. Raw agreement remains separately available.
- Replaced stale DOI-placeholder wording with the DOI links already recorded by the repository. Zenodo archive contents and version relationships remain externally unverified in this audit.
- Changed the protocol's unsupported claim of preregistration to prespecified targets. A protocol file alone does not establish prospective public registration.

## Local diagnostic ablations

Using the corrected evaluator and rebuilding the index for every configuration:

| Configuration | Successes | Direct attacks blocked |
|---|---:|---:|
| Full current controls | 36/40 | 7/8 |
| Injection detector disabled | 29/40 | 0/8 |
| PII redaction disabled at ingestion and query time | 30/40 | 7/8 |

Run `python scripts/validation_audit.py` from the repository root. It uses temporary indexes and in-memory control substitutions. These are descriptive single-run ablations on the existing synthetic set. They do not establish broad security effectiveness. Relevance-threshold and tenant-filter ablations remain outstanding. No AWS/Azure calls or paid experiments were performed.

## Independent review plan

1. Freeze the revised implementation and analysis protocol before an external challenge set is revealed. Record commit, dataset, corpus and configuration hashes.
2. Recruit at least two reviewers who did not implement the system or author the test labels. Record expertise, affiliations and conflicts. Reviewers must decide their own findings.
3. Commission additional independently authored cases, including indirect injection, benign security discussions, realistic privacy formats, unsupported questions and cross-tenant attempts. Keep development and held-out sets separate.
4. Replace category-revealing item IDs with opaque randomized IDs in the actual blinded pack. The included `reviewer_template.csv` is a preparation template only: its original IDs reveal categories, and citation counts alone are insufficient to assess evidential support.
5. Supply authorized source evidence, exact citation passages and task policy for each review item, without expected labels or configuration names. Define how to score blocked/abstaining responses and non-applicable support ratings before review.
6. Collect separate independent ratings before adjudication. Report raw agreement, kappa with undefined values preserved, denominators and disagreements. Separate research annotation from expert assessment of novelty and significance.
7. Run a real-model evaluation with frozen model versions and inert tools if making generative-model claims. If no cloud experiments are run, explicitly present AWS/Azure paths as reference designs rather than experimentally verified equivalence.
8. Expand comparison to relevant baselines and complete the remaining control ablations. Report uncertainty over independently sampled cases; five identical deterministic repeats do not create five independent samples.
9. Review the full manuscript against raw outputs, archive the revised release with version links, and select a suitable venue only after reviewing its scope and preprint policy.

## Remaining blockers

Independent reviewers and their ratings, an independent test set, live-model/cloud experiments where claimed, and archive-PDF reconciliation are not complete. No positive expert endorsement, peer review or acceptance is claimed. The current contribution is a transparent local reference implementation with small synthetic diagnostics.

## Checks completed

Twelve regression/unit tests pass, including expected-block scoring and degenerate-kappa cases. Original archived result files were preserved. New reproduction files and diagnostics are stored separately. This audit is being proposed on a separate branch.

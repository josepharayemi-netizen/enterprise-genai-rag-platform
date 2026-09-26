# Threat model

| Threat | Control and evidence |
|---|---|
| Direct prompt injection | Unicode normalization, literal patterns, behavioral indicators, untrusted-content boundary and adversarial/benign-control tests |
| Indirect prompt injection | Approved-source boundary and review; automated document-level detection remains future work |
| Cross-tenant retrieval | Tenant filter applied before ranking and isolation test |
| Sensitive-data leakage | PII redaction before indexing and no prompt-content metrics labels |
| Hallucination | Minimum retrieval threshold, citations, abstention and golden-set gate |
| Knowledge-base poisoning | Approved source path, checksums, review and immutable artifacts |
| Model abuse | Authentication gateway, rate limits, audit events and budget alarms |
| Supply-chain compromise | Pinned dependencies, SBOM, vulnerability scan and provenance |
| Credential theft | Workload identity and disabled local authentication in cloud resources |

Residual risks require a named owner, documented acceptance and expiry date.

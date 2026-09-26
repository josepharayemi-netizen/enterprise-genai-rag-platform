# Threat model

| Threat | Control and evidence |
|---|---|
| Prompt injection | Pattern gate, untrusted-content boundary and adversarial test |
| Cross-tenant retrieval | Tenant filter applied before ranking and isolation test |
| Sensitive-data leakage | PII redaction before indexing and no prompt-content metrics labels |
| Hallucination | Minimum retrieval threshold, citations, abstention and golden-set gate |
| Knowledge-base poisoning | Approved source path, checksums, review and immutable artifacts |
| Model abuse | Authentication gateway, rate limits, audit events and budget alarms |
| Supply-chain compromise | Pinned dependencies, SBOM, vulnerability scan and provenance |
| Credential theft | Workload identity and disabled local authentication in cloud resources |

Residual risks require a named owner, documented acceptance and expiry date.

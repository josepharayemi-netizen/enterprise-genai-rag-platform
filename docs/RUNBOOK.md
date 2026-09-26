# Operations runbook

## Grounding quality drops

1. Pause promotion and identify the prompt, index and provider versions.
2. Compare failed golden cases and retrieval scores with the approved baseline.
3. Inspect source freshness, chunking and tenant filters.
4. Roll back through GitOps to the previous immutable image digest.

## Prompt attack or data exposure

1. Block the request source and preserve the request ID and audit evidence.
2. Revoke affected workload identity and isolate the tenant index.
3. Confirm whether source documents, prompts or responses contained sensitive data.
4. Rotate credentials, rebuild the index from approved sources and document the incident.

## Cost anomaly

1. Disable provider traffic through the gateway circuit breaker.
2. Review token, request and vector-search consumption by tenant.
3. Confirm rate limits, budgets and cache behaviour before re-enabling traffic.

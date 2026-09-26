# ADR-001: Provider-neutral RAG core

## Decision

Keep ingestion, security, retrieval contracts and evaluation provider-neutral. Use adapters for local extractive mode, Amazon Bedrock and Azure OpenAI.

## Rationale

This avoids provider lock-in while preserving cloud-native identity, networking, vector search and observability. Deterministic local mode makes CI reproducible and prevents accidental API costs.

## Consequences

Provider capabilities are not identical. Each cloud adapter requires separate performance, safety and cost evaluation before promotion.

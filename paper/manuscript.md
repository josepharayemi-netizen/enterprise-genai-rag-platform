# Secure and Responsible Retrieval-Augmented Generation for Resource-Constrained Organizations: A Multi-Cloud Reference Architecture and Experimental Evaluation

**Joseph Arayemi**  
GIIT Africa, Lagos, Nigeria  
*Corresponding-author email and ORCID to be added before submission*

## Abstract

Retrieval-augmented generation (RAG) can improve the factual grounding of generative artificial intelligence systems, but production adoption also introduces privacy, prompt-injection, access-control and operational-governance risks. These challenges are especially consequential for resource-constrained organizations that require auditable controls without dependence on costly managed services during early development. This paper presents a reproducible, multi-cloud reference architecture for secure and responsible enterprise RAG. The implementation combines approved-source ingestion, deterministic local retrieval, tenant-aware filtering, personally identifiable information redaction, prompt-injection detection, evidence-based abstention, source citations, versioned evaluation and deployment controls. Equivalent production paths are specified for Amazon Web Services and Microsoft Azure. We define an experimental protocol covering retrieval, grounding, attack blocking, privacy protection, abstention, latency and cost. The released artifact includes source code, infrastructure definitions, a synthetic benchmark and governance documentation. Quantitative results will be inserted after the frozen benchmark and ablation experiments are executed. The work is intended as a transparent baseline for researchers and practitioners evaluating trustworthy RAG systems in organizations with constrained infrastructure and governance capacity.

**Keywords:** retrieval-augmented generation; responsible AI; AI security; prompt injection; multi-cloud; MLOps; AWS; Microsoft Azure

## 1. Introduction

Generative AI systems can produce fluent responses that are unsupported by organizational evidence. RAG addresses part of this problem by retrieving relevant material and supplying it as context for answer generation. Retrieval alone, however, does not establish trustworthy operation. A production system must also control its evidence sources, isolate tenants, protect personal information, resist instruction manipulation, cite supporting material, abstain when evidence is insufficient and preserve an auditable deployment process.

Many published enterprise architectures depend on managed services or opaque model behavior from the beginning of development. That dependency can limit reproducibility and create barriers for smaller organizations, particularly in developing economies. This study therefore asks whether a lightweight local baseline can make core security and governance behavior testable before an organization incurs cloud inference costs, while retaining portable deployment paths for AWS and Azure.

The principal contributions are:

1. an open, reproducible RAG reference implementation that runs without paid model APIs;
2. integrated security and governance controls spanning ingestion, retrieval, response and deployment;
3. equivalent infrastructure paths for AWS and Azure;
4. a versioned evaluation protocol covering quality, security, privacy, isolation and operational performance; and
5. an explicit limitations model that separates measured controls from broader claims of AI safety.

## 2. Background and related work

This section will synthesize peer-reviewed work on RAG evaluation, hallucination and grounding, prompt injection, privacy-preserving language systems, responsible AI frameworks and multi-cloud MLOps. The final review will prioritize primary research and current standards. Every claim will be supported by a verified citation; placeholder or generated references will not be used.

## 3. System architecture

The system ingests an allowlisted collection of Markdown documents, redacts supported PII patterns, divides the documents into overlapping chunks and creates deterministic hashed bag-of-token embeddings. At query time, a security gateway validates and redacts the question. Retrieval is restricted by tenant identifier, and only chunks exceeding a relevance threshold are eligible to support an answer. The local response mode extracts the sentence with the greatest token overlap and returns provenance metadata for all eligible chunks. If evidence is insufficient, it returns a fixed abstention response.

The local mode functions as a transparent experimental baseline rather than a claim of state-of-the-art semantic retrieval. Production reference paths map equivalent responsibilities to Amazon Bedrock and OpenSearch Serverless on AWS, and Azure OpenAI and Azure AI Search on Microsoft Azure. Both designs use managed key services, short-lived workload identities, observability and infrastructure-as-code.

## 4. Threat model and governance controls

The study considers direct prompt injection, supported PII formats, cross-tenant retrieval, unsupported questions and unauthorized deployment. It does not claim protection against every linguistic injection variant, indirect injection embedded in retrieved documents, compromised cloud control planes, malicious maintainers or previously unknown attacks.

Governance artifacts include a model card, threat model, risk controls, a human-review boundary, versioned evaluation data, GitOps deployment and a release-specific citation record. Consequential decisions remain outside the system's authorized use boundary.

## 5. Methodology

The experiment follows the preregistered protocol in `research/PROTOCOL.md`. Primary evaluation uses a frozen, versioned test set with answerable, unsupported, injection, privacy, validation and tenant-isolation cases. The full guarded system is compared with ablations that remove individual controls. Deterministic experiments are repeated to verify stability. Cloud experiments record configuration, model version, region, measured latency and contemporaneous pricing assumptions.

## 6. Results

**This section intentionally contains no invented results.** Populate the following table only from committed machine-readable experiment output.

| Configuration | Cases | End-to-end success | Citation coverage | Injection block rate | PII redaction recall | Abstention accuracy | Median latency | p95 latency |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Local, full controls | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Local, no injection detector | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Local, no PII redaction | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| AWS managed path | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Azure managed path | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## 7. Discussion

The final discussion will interpret whether the measured evidence supports each hypothesis, compare operational trade-offs and identify failures exposed by the ablations. Particular attention will be given to whether simple safeguards provide meaningful baseline protection without overstating their coverage.

## 8. Limitations and threats to validity

The present corpus and benchmark are synthetic and small. Keyword-hashed embeddings do not represent modern semantic retrievers, the attack set cannot cover adversarial creativity, and pattern-based PII redaction has limited entity coverage. Managed cloud model behavior may change by model version and region. Results therefore cannot be generalized to clinical, legal, financial, employment or other consequential applications. A submission-ready study should expand the held-out benchmark, include independent annotation and report uncertainty.

## 9. Conclusion

This work offers a transparent foundation for studying secure, governed RAG across local and multi-cloud environments. Its value lies in making assumptions, controls, evidence and limitations inspectable. Final conclusions will be restricted to the outcomes of the frozen experiments.

## Data and software availability

Source code, synthetic evaluation data, infrastructure definitions and reproduction instructions are available at `https://github.com/josepharayemi-netizen/enterprise-genai-rag-platform`. A version-specific Zenodo DOI will be added after the `v1.0.0` release is archived.

## Ethics statement

The included data are synthetic and contain no intentionally collected personal data. The system is not authorized for consequential automated decision-making. Any future study involving human participants or non-public organizational data must obtain the appropriate ethical and institutional approvals.

## Declaration of AI assistance

Generative AI tools assisted with early software and manuscript drafting. The named human author is responsible for verification, experiments, citations, interpretation and the final submitted text. This statement must be adapted to the target venue's policy.

## References

To be completed from verified primary literature and official standards before public submission.


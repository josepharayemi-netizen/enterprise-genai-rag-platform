# Secure and Responsible Retrieval-Augmented Generation for Resource-Constrained Organizations: A Multi-Cloud Reference Architecture and Experimental Evaluation

**Joseph Arayemi**  
GIIT Africa, Lagos, Nigeria  
Corresponding author: yemi@giitafrica.com  
ORCID: [0009-0007-0776-7238](https://orcid.org/0009-0007-0776-7238)

## Abstract

Retrieval-augmented generation (RAG) can improve the factual grounding of generative artificial intelligence systems, but production adoption also introduces privacy, prompt-injection, access-control and operational-governance risks. These challenges are especially consequential for resource-constrained organizations that require auditable controls without dependence on costly managed services during early development. This paper presents a reproducible, multi-cloud reference architecture for secure and responsible enterprise RAG. The implementation combines approved-source ingestion, deterministic local retrieval, tenant-aware filtering, personally identifiable information redaction, prompt-injection detection, evidence-based abstention, source citations, versioned evaluation and deployment controls. Equivalent production paths are specified for Amazon Web Services and Microsoft Azure. On a frozen 40-case synthetic candidate test set, the local configuration achieved 34/40 end-to-end successes (0.85) with deterministic outcomes across five repetitions. It achieved complete success on the tested privacy-redaction, tenant-isolation, unsupported-question and validation categories, but blocked only 5/8 prompt-injection formulations (0.625). The results expose the limits of pattern-based defenses and support using the artifact as a transparent baseline rather than a claim of comprehensive AI security.

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

### 2.1 Retrieval-augmented generation

Lewis et al. introduced RAG as a framework combining parametric generation with non-parametric retrieved memory for knowledge-intensive language tasks [1]. The approach provides a foundation for answers that can be conditioned on external evidence rather than relying exclusively on model parameters. Subsequent work has expanded RAG into a broader family of naive, advanced and modular architectures, with retrieval, augmentation and generation each presenting distinct design and evaluation choices [2]. The present study narrows that broad design space to a transparent enterprise baseline in which evidence selection, abstention and provenance can be inspected without a paid model endpoint.

### 2.2 Evaluation of RAG systems

RAG evaluation cannot be reduced to a single accuracy score because retrieval quality, contextual relevance, answer faithfulness and answer relevance can fail independently. RAGAS proposes reference-free measures for evaluating several of these dimensions [3]. ARES similarly evaluates context relevance, answer faithfulness and answer relevance, combining synthetic training data with a smaller quantity of human annotation and prediction-powered inference [4]. These approaches motivate the separation of categories and metrics in this study. However, the current local baseline is extractive rather than generative, so its initial experiment reports deterministic task success, citation coverage, abstention, security behavior and latency instead of using an LLM as an evaluator. Human and model-based assessment should be added when the AWS and Azure generative paths are activated.

### 2.3 Prompt injection and RAG security

Retrieval introduces an important trust-boundary problem: external content can contain instructions as well as data. Greshake et al. demonstrated that indirect prompt injection can exploit this ambiguity in LLM-integrated applications and can lead to manipulation, data theft and unsafe tool behavior [5]. OWASP consequently treats prompt injection as a leading risk for LLM and generative-AI applications, and notes that RAG and fine-tuning do not eliminate the underlying vulnerability [6]. The present platform's pattern-based detector is therefore treated as a measurable baseline control, not a complete defense. The candidate test result, in which three of eight adversarial formulations bypassed literal patterns, is consistent with the need for layered controls and adversarial evaluation.

### 2.4 Responsible AI governance

The NIST AI Risk Management Framework organizes AI risk work around the Govern, Map, Measure and Manage functions and emphasizes lifecycle-wide, context-sensitive risk management [7]. Its Generative AI Profile extends that framework with considerations specific to generative systems [8]. The repository operationalizes a subset of those principles through documented ownership, model and prompt versioning, a threat model, evaluation gates, human-review boundaries, auditability and release controls. This implementation does not claim full conformity or certification; the mapping is a design aid whose completeness must be assessed in a real deployment context.

### 2.5 Research gap

Prior work establishes sophisticated RAG methods, multidimensional evaluation and serious prompt-injection risks. A practical gap remains between those strands for organizations that need a locally reproducible security and governance baseline before funding managed cloud inference. This study addresses that narrower gap with one inspectable artifact spanning local evaluation, responsible-AI documentation, DevSecOps controls and parallel AWS/Azure reference paths. Its novelty claim is architectural integration and transparent experimental packaging, not a new foundation model, embedding algorithm or universal security defense.

## 3. System architecture

The system ingests an allowlisted collection of Markdown documents, redacts supported PII patterns, divides the documents into overlapping chunks and creates deterministic hashed bag-of-token embeddings. At query time, a security gateway validates and redacts the question. Retrieval is restricted by tenant identifier, and only chunks exceeding a relevance threshold are eligible to support an answer. The local response mode extracts the sentence with the greatest token overlap and returns provenance metadata for all eligible chunks. If evidence is insufficient, it returns a fixed abstention response.

The local mode functions as a transparent experimental baseline rather than a claim of state-of-the-art semantic retrieval. Production reference paths map equivalent responsibilities to Amazon Bedrock and OpenSearch Serverless on AWS, and Azure OpenAI and Azure AI Search on Microsoft Azure. Both designs use managed key services, short-lived workload identities, observability and infrastructure-as-code.

## 4. Threat model and governance controls

The study considers direct prompt injection, supported PII formats, cross-tenant retrieval, unsupported questions and unauthorized deployment. It does not claim protection against every linguistic injection variant, indirect injection embedded in retrieved documents, compromised cloud control planes, malicious maintainers or previously unknown attacks.

Governance artifacts include a model card, threat model, risk controls, a human-review boundary, versioned evaluation data, GitOps deployment and a release-specific citation record. Consequential decisions remain outside the system's authorized use boundary.

## 5. Methodology

The experiment follows the protocol in `research/PROTOCOL.md`. The 20-case development benchmark was used during implementation and is reported separately from the frozen 40-case synthetic candidate test set. The candidate set contains answerable, unsupported, injection, privacy, validation and tenant-isolation cases and is identified by SHA-256 digest. The local experiment was repeated five times to assess deterministic stability. The set was constructed as part of this study and was not independently annotated; it is therefore not presented as an external benchmark. Planned cloud experiments will record configuration, model version, region, measured latency and contemporaneous pricing assumptions.

To prepare independent validation, the artifact also includes a blinded annotation-pack generator and an agreement calculator. The pack contains prompts, system responses and citation counts but excludes expected labels and category metadata. At least two reviewers who did not create the benchmark or implement the controls will independently rate behavioral correctness, evidential support and response safety using `yes`, `no` or `uncertain`. Raw agreement and Cohen's kappa will be calculated before adjudication. No independent human-review result is claimed in the present version because external ratings have not yet been collected.

## 6. Results

Results below are taken from `evaluation/results/local_candidate_test.json`. Outcomes were identical across five repetitions. Latency values are from the first recorded run and describe the lightweight local implementation in the recorded execution environment; they are not cloud latency estimates.

| Configuration | Cases | End-to-end success | Citation coverage | Injection block rate | PII redaction recall | Abstention accuracy | Median latency | p95 latency |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Local, full controls | 40 | 34/40 (0.85) | 20/21 (0.9524) | 5/8 (0.625) | 6/6 (1.00) | 6/6 (1.00) | 0.1322 ms | 0.1808 ms |
| Local, no injection detector | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Local, no PII redaction | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| AWS managed path | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Azure managed path | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## 7. Discussion

The candidate test result supports H1 for overall end-to-end success, H3 for the explicitly supported PII formats and H4 for unsupported-question abstention. It does not support H2: the pattern-based detector blocked only five of eight prompt-injection formulations. Three semantically adversarial prompts that avoided the detector's literal patterns were not blocked. This is evidence that regular-expression safeguards can provide a basic control but should not be treated as a comprehensive prompt-injection defense.

The answerable category achieved 12/15 successes. Together with citation coverage of 20/21 expected-citation cases, these failures illustrate the recall limitations of deterministic lexical retrieval. Conversely, all six unsupported questions correctly triggered abstention, suggesting that the strengthened lexical-evidence condition reduced false-positive grounding on this dataset. These observations are specific to the synthetic corpus and cannot establish performance on natural enterprise documents.

### 7.1 Post-baseline security hardening

After freezing the initial result, the direct-injection gateway was extended with Unicode NFKC normalization, zero-width-character removal and a scored combination of override, control, exfiltration and protected-information indicators. It was evaluated separately on a new 36-case diagnostic set containing 24 adversarial inputs and 12 benign security or governance questions.

| Security configuration | Attacks detected | Attack recall | Benign accepted | Benign specificity | Precision | Overall accuracy |
|---|---:|---:|---:|---:|---:|---:|
| Layered direct-injection detector (v2) | 17/24 | 0.7083 | 11/12 | 0.9167 | 0.9444 | 28/36 (0.7778) |

The v2 detector missed seven attacks: one social-engineering formulation, spaced-letter and encoded inputs, two multilingual inputs and two role-play/developer-mode formulations. It also incorrectly blocked one benign question discussing bypass attempts. Because the v2 dataset was created within the same study, these figures are diagnostic rather than independent evidence of generalization. They nevertheless demonstrate why both attack recall and benign specificity are necessary: increasing sensitivity without benign controls can make a system unusable while still missing novel attacks.

## 8. Limitations and threats to validity

The corpus and benchmarks are synthetic and small. Both candidate sets were authored during the study, were not independently annotated and may reflect the designers' assumptions. Keyword-hashed embeddings do not represent modern semantic retrievers. Neither the initial eight-case attack category nor the 36-case v2 diagnostic set can cover adversarial creativity, indirect injection through retrieved documents or multilingual variation. Pattern-based PII redaction also has limited entity coverage. The sub-millisecond latency measurements reflect an in-process extractive baseline, not a networked generative model. Managed cloud behavior may change by model version and region. Results cannot be generalized to clinical, legal, financial, employment or other consequential applications. A submission-ready study should use a larger independently prepared test set, include multiple annotators, calculate inter-rater agreement and report statistical uncertainty.

## 9. Conclusion

This work offers a transparent foundation for studying secure, governed RAG across local and multi-cloud environments. Its value lies in making assumptions, controls, evidence and limitations inspectable. Final conclusions will be restricted to the outcomes of the frozen experiments.

## Data and software availability

Source code, synthetic evaluation data, infrastructure definitions and reproduction instructions are available at `https://github.com/josepharayemi-netizen/enterprise-genai-rag-platform`. A version-specific Zenodo DOI will be added after the `v1.0.0` release is archived.

## Ethics statement

The included data are synthetic and contain no intentionally collected personal data. The system is not authorized for consequential automated decision-making. Any future study involving human participants or non-public organizational data must obtain the appropriate ethical and institutional approvals.

## Declaration of AI assistance

Generative AI tools assisted with early software and manuscript drafting. The named human author is responsible for verification, experiments, citations, interpretation and the final submitted text. This statement must be adapted to the target venue's policy.

## References

[1] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W.-t. Yih, T. Rocktäschel, S. Riedel, and D. Kiela, “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,” in *Advances in Neural Information Processing Systems 33*, 2020, pp. 9459–9474. Available: https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html

[2] Y. Gao, Y. Xiong, X. Gao, K. Jia, J. Pan, Y. Bi, Y. Dai, J. Sun, M. Wang, and H. Wang, “Retrieval-Augmented Generation for Large Language Models: A Survey,” arXiv:2312.10997, 2023. doi: 10.48550/arXiv.2312.10997.

[3] S. Es, J. James, L. Espinosa-Anke, and S. Schockaert, “RAGAs: Automated Evaluation of Retrieval Augmented Generation,” in *Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics: System Demonstrations*, 2024. doi: 10.18653/v1/2024.eacl-demo.16.

[4] J. Saad-Falcon, O. Khattab, C. Potts, and M. Zaharia, “ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems,” in *Proceedings of NAACL-HLT 2024*, pp. 338–354, 2024. doi: 10.18653/v1/2024.naacl-long.20.

[5] K. Greshake, S. Abdelnabi, S. Mishra, C. Endres, T. Holz, and M. Fritz, “Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection,” in *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security*, 2023. doi: 10.1145/3605764.3623985.

[6] OWASP Gen AI Security Project, “LLM01:2025 Prompt Injection,” 2025. Available: https://genai.owasp.org/llmrisk/llm01-prompt-injection/

[7] National Institute of Standards and Technology, *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*, NIST AI 100-1, 2023. doi: 10.6028/NIST.AI.100-1.

[8] National Institute of Standards and Technology, *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*, NIST AI 600-1, 2024. doi: 10.6028/NIST.AI.600-1.

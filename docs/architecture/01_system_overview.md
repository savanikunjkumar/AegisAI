# AegisAI — System Overview

> **Version:** 0.3.1-alpha · **Author:** Kunjkumar Savani · **Phase:** 01 · Architecture Documentation

---

## Vision

AegisAI is a headless ML + Cybersecurity framework that integrates **Retrieval-Augmented Generation (RAG)** with **Large Language Models (LLMs)** to build an autonomous security assistant — designed for zero-trust environments where every input is suspect and every output is auditable.

---

## Core Architecture Flow

```
[Threat Sources] → [Ingestion] → [Vector + Graph DB] → [LLM Agent] → [Output]
                                                              ↑
                                          [Adversarial Guard] + [Explainer]
```

---

## Pipeline Phases

### Phase 03 · Intelligence Ingestion

Raw threat data (CVEs, MITRE ATT&CK, STIX feeds, synthetic logs) is processed through two parallel tracks:

| Track | Store | Purpose |
|-------|-------|---------|
| Semantic | Pinecone / FAISS | Vector embeddings for similarity search |
| Relational | Neo4j | Entity graph: CVE → Software → Mitigation |

```
rag_pipeline/
├── ingestion.py
├── vector_store/pinecone_client.py
└── knowledge_graph/neo4j_connector.py
```

---

### Phase 03+ · Neural GraphRAG Retrieval

When a query arrives, AegisAI runs **dual-mode retrieval**:

1. **Vector search** — top-k semantically similar threat documents
2. **Graph traversal** — Cypher queries expand entity relationships

The merged result forms a grounded context window injected into the LLM. The model never reasons from memory alone.

---

### Phase 04 · Agentic LLM Reasoning

Retrieved context is passed into strict, role-scoped prompt templates. Supported tasks:

| Task | Description |
|------|-------------|
| `explain_cve` | Plain-language CVE breakdown |
| `suggest_mitigation` | Step-by-step remediation |
| `analyze_log` | Anomaly detection in auth/network logs |
| `summarize_threat` | Condense intelligence reports |

```
llm_security/
├── agent.py
└── prompt_templates.py
```

---

### Phase 05 · Adversarial Defense

All inputs pass through a layered defense stack before reaching the LLM:

```
Input → PromptGuardrail (Rebuff / NeMo)
      → DataSanitizer   (poisoning detection)
      → OutputValidator  (schema + PII check)
```

```
adversarial_defense/
├── poisoning_detection.py
└── prompt_guardrails.py
```

---

### Phase 06 · Explainability Audit

Every model decision is accompanied by a human-readable explanation:

| Tool | Method | Output |
|------|--------|--------|
| SHAP | Shapley values | Feature importance scores |
| LIME | Local surrogate models | Per-prediction explanations |
| Captum | Gradient attribution | Layer-level PyTorch explanations |

```
explainability/
├── shap_explainer.py
└── lime_explainer.py
```

---

## Security Principles

| Principle | How |
|-----------|-----|
| Zero Trust | Every input sanitised; no implicit trust |
| Hallucination-free | LLM always grounded by retrieved context |
| Auditable | Every flag comes with a SHAP/LIME explanation |
| Defence in depth | Guards at ingestion, reasoning, and output |
| Minimal privilege | LLM constrained by strict prompt schemas |

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Vector store | FAISS · Pinecone |
| Knowledge graph | Neo4j · Cypher |
| LLM | GPT-4 · Claude · Ollama |
| Adversarial defense | Rebuff · NeMo Guardrails |
| Explainability | SHAP · LIME · Captum |
| ML / DL | scikit-learn · PyTorch · HuggingFace |
| Threat intel | MITRE ATT&CK · NVD · STIX/TAXII |

---

## Related Docs

- [`02_neural_graphrag.md`](./02_neural_graphrag.md) — Neo4j + Vector DB deep dive
- [`03_zero_trust_models.md`](./03_zero_trust_models.md) — Anomaly & insider threat models

---

*Copyright © 2026 Kunj Savani · MIT License · [github.com/savanikunjkumar/AegisAI](https://github.com/savanikunjkumar/AegisAI)*

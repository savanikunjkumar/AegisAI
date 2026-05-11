# AegisAI — Neural GraphRAG Architecture

> **Version:** 0.3.1-alpha · **Author:** Kunjkumar Savani · **Phase:** 03 · RAG Pipeline

---

## The Problem: Hallucinations in Cybersecurity

Standard RAG relies solely on **semantic similarity** — it finds conceptually close documents but fails at deterministic logic.

If an agent needs to know exactly which APT group exploits a specific CVE against a specific OS, vector search may return overlapping but factually disconnected results. In cybersecurity, that's a fatal failure.

---

## The Solution: Vector + Graph (Dual-Engine RAG)

AegisAI implements a **Neural GraphRAG** architecture — two databases queried simultaneously before any context reaches the LLM.

| Engine | Store | Answers |
|--------|-------|---------|
| Semantic | Pinecone / FAISS | *What* and *How* — unstructured threat descriptions |
| Deterministic | Neo4j Knowledge Graph | *Who* and *Where* — hard entity relationships |

---

## Engine 1 · Vector Store (Pinecone / FAISS)

Stores 1536-dimensional embeddings of threat reports, CVE descriptions, and network logs.

```
Query: "remote code execution in OpenSSL"
  │
  └─► Embedding model → 1536-dim vector
        │
        └─► Pinecone similarity search → top-k threat documents
```

**Output:** Unstructured text describing *how* a vulnerability works.

```
rag_pipeline/vector_store/
└── pinecone_client.py    # embed(), upsert(), query(top_k)
```

---

## Engine 2 · Knowledge Graph (Neo4j)

Stores logical, deterministic pathways between security entities using Cypher.

**Graph schema:**

```
(ThreatActor) -[:EXPLOITS]-> (Vulnerability) -[:AFFECTS]-> (System)
(Vulnerability) -[:MITIGATED_BY]-> (Patch)
(ThreatActor) -[:USES]-> (Technique) -[:TARGETS]-> (System)
```

**Example Cypher query:**

```cypher
MATCH (ta:ThreatActor)-[:EXPLOITS]->(cve:CVE {id: "CVE-2024-0001"})
      -[:AFFECTS]->(sys:System)
OPTIONAL MATCH (cve)-[:MITIGATED_BY]->(patch:Patch)
RETURN ta.name, sys.name, patch.version
```

**Output:** Exact, mathematically certain relationships — no hallucination possible.

```
rag_pipeline/knowledge_graph/
└── neo4j_connector.py    # connect(), query(), build_context()
```

---

## Context Injection Flow

When `AegisSecurityAgent` receives a query (e.g., *"Analyze the risk of CVE-2024-0001"*):

```
User Query
    │
    ├─► 1. Embed & Fetch      →  Pinecone top-k semantic matches
    │
    ├─► 2. Traverse & Extract →  Neo4j exact entity relationships
    │
    ├─► 3. Unify              →  Single merged context block
    │
    └─► 4. Reason             →  LLM processes dual-context
                                  (semantic + deterministic)
                                        │
                                   Verified Output
```

The LLM's reasoning is anchored to both **semantic context** (Pinecone) and **hard factual logic** (Neo4j). Neither alone is sufficient.

---

## Why Not Just One?

| Scenario | Vector Only | Graph Only | Neural GraphRAG |
|----------|-------------|------------|-----------------|
| Find similar CVEs | ✅ | ❌ | ✅ |
| Exact APT → CVE → OS chain | ❌ | ✅ | ✅ |
| Novel/unseen threat patterns | ✅ | ❌ | ✅ |
| Zero hallucination guarantee | ❌ | ✅ | ✅ |
| Rich natural language context | ✅ | ❌ | ✅ |

---

## Related Docs

- [`01_system_overview.md`](./01_system_overview.md) — Full pipeline overview
- [`03_zero_trust_models.md`](./03_zero_trust_models.md) — Anomaly & insider threat models

---

*Copyright ©2026 Kunj Savani · MIT License · [github.com/savanikunjkumar/AegisAI](https://github.com/savanikunjkumar/AegisAI)*

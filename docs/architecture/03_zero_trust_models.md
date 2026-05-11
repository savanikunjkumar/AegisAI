# AegisAI — Zero-Trust Simulation & Anomaly Detection

> **Version:** 0.3.1-alpha · **Author:** Kunjkumar Savani · **Phase:** 03 · Zero-Trust Models

---

## The Zero-Trust Philosophy

Traditional perimeter security implicitly trusts anything inside the network. Zero-Trust flips this:

> **"Never trust, always verify."**

AegisAI assumes the perimeter has already been breached. Every access request, database query, and lateral movement is continuously evaluated — regardless of credentials.

---

## Simulated Telemetry Pipeline

To train anomaly models without exposing real enterprise data, AegisAI generates **synthetic telemetry** — high-volume JSON logs of normal operations, interspersed with mathematical anomalies.

Three anomaly classes are simulated:

| Class | Description | Example |
|-------|-------------|---------|
| **Insider Threat** | Legitimate accounts behaving abnormally | Large data download at 3 AM |
| **Compromised Credentials** | Impossible travel / access patterns | Login from India, then Russia 10 min later |
| **Lateral Movement** | Service accounts hitting new endpoints | Admin API called by a read-only service account |

```
data/synthetic_logs/
├── normal_traffic.json      # Baseline business operations
└── anomaly_injected.json    # Labelled malicious events
```

---

## ML Detection Engines

AegisAI avoids static rules (easily evaded) and uses **unsupervised ML** to catch zero-day anomalies.

---

### Engine 1 · Isolation Forest

Rather than profiling what "normal" looks like, Isolation Forests **explicitly isolate anomalies**.

Malicious actions are mathematically rare and feature-distinct — a huge payload size, an unusual hour, a new destination IP. The algorithm needs fewer decision tree splits to isolate an anomalous log than a benign one. Fewer splits = higher anomaly score.

```python
from sklearn.ensemble import IsolationForest

model = IsolationForest(contamination=0.02, random_state=42)
model.fit(normal_logs)

scores = model.decision_function(new_logs)  # negative = anomalous
```

**Best for:** High-volume, tabular log data with clear feature engineering.

---

### Engine 2 · Deep Autoencoder

For complex, non-linear relationships, AegisAI uses a **neural network autoencoder**.

The model learns to compress and reconstruct normal network traffic. When a malicious log is fed in, the model struggles to reconstruct it accurately — producing a high **reconstruction error** that triggers an alert.

```
Normal log   →  Encoder  →  Latent space  →  Decoder  →  Low error   ✅
Malicious log →  Encoder  →  Latent space  →  Decoder  →  High error  🚨
```

**Best for:** Long-sequence logs, subtle behavioural drift, and non-linear attack patterns.

---

## Detection → Explainability → Triage

Detecting an anomaly is only half the job. The full pipeline:

```
Log flagged by Isolation Forest / Autoencoder
    │
    └─► AegisSHAPExplainer (Phase 06)
            │
            └─► Shapley values computed per feature
                    │
                    └─► Human-readable proof generated
                            │
                            └─► LLM Security Assistant (Phase 04)
                                    │
                                    └─► Triage report + mitigation advice
```

**Example SHAP output:**

```
Anomaly detected · Threat score: 0.91

Feature contributions:
  failed_login_attempts   +0.85  ████████░░
  access_hour (3:14 AM)   +0.61  ██████░░░░
  data_volume_mb          +0.44  ████░░░░░░
  source_ip_entropy       +0.29  ███░░░░░░░
  user_role = read_only   -0.12  ░░░░░░░░░░  (mitigating)
```

This verified mathematical proof is what gets handed to the LLM — never a raw flag.

---

## Why Unsupervised?

| Approach | Catches Zero-Days | Evasion-Resistant | Explainable |
|----------|:-----------------:|:-----------------:|:-----------:|
| Static rules | ❌ | ❌ | ✅ |
| Supervised ML | ❌ | Partial | ✅ |
| Isolation Forest | ✅ | ✅ | Via SHAP |
| Autoencoder | ✅ | ✅ | Via SHAP |

Unsupervised models have no labelled attack signatures to evade — they flag anything that deviates from the learned baseline.

---

## Related Docs

- [`01_system_overview.md`](./01_system_overview.md) — Full pipeline overview
- [`02_neural_graphrag.md`](./02_neural_graphrag.md) — Vector + Graph retrieval architecture

---

*Copyright ©2026 Kunj Savani · MIT License · [github.com/savanikunjkumar/AegisAI](https://github.com/savanikunjkumar/AegisAI)*

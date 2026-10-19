# SenticRAG Capability Map

This capability map traces business objectives through the three functional intelligence layers into technical software modules:

| Value Layer | User Query & Intent | Core Technical Mechanism | Data & Scope | Responsible Module |
| :--- | :--- | :--- | :--- | :--- |
| **1. Quantitative (Macro)** | *"What is increasing or decreasing across our products?"* | Aspect Term Extraction (ATE) + Aspect Polarity Classification (APC) | 100% Review/Ticket Corpus (Batch & Streaming) | `packages/absa`, `packages/analytics` |
| **2. Qualitative (Investigation)** | *"Why is this spike occurring in this cohort?"* | Metadata Filtering + Dense/Sparse Hybrid Retrieval + BGE Rerank | Top-K Representative Reviews & Tickets | `packages/retrieval` (Dense, Sparse, RRF Fusion, Rerank) |
| **3. Actionable (Resolution)** | *"How should this customer's ticket be resolved right now?"* | Operational GraphRAG (Neo4j) + Policy Registry + LLM Guardrails | Evidence Pack + Structured Policy + Customer Context | `packages/graph`, `packages/policy`, `packages/resolution`, `packages/llm` |
| **4. Collaborative Learning** | *"How does the system continuously learn from expert actions?"* | Human Annotation + Knowledge Approval Workflow + Active Learning | Analyst Confirmations, Agent Edits, Label Corrections | `packages/feedback` |

---

## Capability Ownership & Boundaries

1. **ABSA does not retrieve:** ABSA computes structured metadata across all records to build macro dashboards and populate searchable metadata filters.
2. **Retrieval does not replace statistical aggregations:** Retrieval acts as a qualitative magnifying glass fetching the Top-K relevant records for investigation.
3. **GraphRAG is not merely conversational QA:** GraphRAG manages operational defect ontology: `Issue → Version → Symptom → Root Cause → Policy → Resolution → Evidence`.
4. **LLM never invents business policies:** LLMs only summarize, format, and draft based strictly on retrieved policy clauses and evidence. Any high-risk financial or legal commitment triggers human review escalation.

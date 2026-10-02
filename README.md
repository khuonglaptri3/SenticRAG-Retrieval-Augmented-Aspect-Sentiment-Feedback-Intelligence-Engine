# SenticRAG — Retrieval-Augmented Aspect Sentiment & Feedback Intelligence Engine

[![CI](https://github.com/khuonglaptri3/SenticRAG-Retrieval-Augmented-Aspect-Sentiment-Feedback-Intelligence-Engine/actions/workflows/ci.yml/badge.svg)](https://github.com/khuonglaptri3/SenticRAG-Retrieval-Augmented-Aspect-Sentiment-Feedback-Intelligence-Engine/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](infra/docker/)
[![Architecture](https://img.shields.io/badge/architecture-7--layer%20agent-orange.svg)](docs/architecture/ARCHITECTURE.md)

---

## 1. Executive Summary

**SenticRAG** is an enterprise-grade AI intelligence engine that unifies **Aspect-Based Sentiment Analysis (ABSA)**, **Advanced Hybrid Retrieval (Dense Vector + BM25 Lexical + BGE Cross-Encoder Reranker)**, **Operational Knowledge Graph (GraphRAG with Neo4j)**, and a **Closed-Loop Collaborative Feedback Mechanism**.

Unlike passive sentiment analysis systems that merely report aggregated scores on BI dashboards, SenticRAG operates as an **Actionable Decision & Resolution Engine** following a closed-loop lifecycle:

> **Observe → Understand → Explain → Resolve → Learn**

### Three Core Value Layers

| Value Layer | User Question | Technical Mechanism | Data Scope | System Output |
| :--- | :--- | :--- | :--- | :--- |
| **Quantitative** | *"What is increasing or decreasing?"* | ABSA (Aspect Term & Polarity Classification) | 100% Review/Ticket Corpus | Macro KPIs, sentiment distribution, anomaly alerts. |
| **Qualitative** | *"Why is this happening?"* | Metadata Filtering + Hybrid Retrieval + BGE Reranking | Top-K Representative Cases | Grounded evidence pack, symptom summaries, root-cause candidates. |
| **Actionable** | *"How should this be resolved?"* | GraphRAG (Neo4j) + Policy Registry + LLM Guardrails | Evidence + Policy + Customer Context | Policy-grounded resolution drafts, citations, automated action routing. |

### Four Core Personas & User Stories

1. **Buyer (`US-BUY-01`)**: Experiences a product defect and receives immediate, policy-compliant resolution instructions without repetitive data entry.
2. **Support Agent (`US-AGENT-01`)**: Receives pre-triaged tickets with structured aspect/sentiment tags and an evidence-backed resolution draft with verified policy citations.
3. **Product / CX Analyst (`US-ANALYST-01`)**: Identifies emerging sentiment spikes, drills down into representative review cohorts, uncovers root causes, and registers new findings into the Knowledge Graph.
4. **Product Manager / CPO (`US-PM-01`)**: Monitors product issue trends across hardware/firmware releases in real time and evaluates resolution efficacy.

---

## 2. 7-Layer Architecture Overview

SenticRAG is engineered strictly in accordance with the theoretical 7-layer AI Agent Pipeline:

![SenticRAG 7-Layer Architecture](docs/architecture/7_layer_architecture.svg)

> **Interactive Viewer**: Open [`docs/architecture/7_layer_architecture.html`](docs/architecture/7_layer_architecture.html) in your browser for dynamic inspection, guided tours (Full Flow, RAG & Knowledge Core, Safety & Ops), and deep component breakdowns. Full architectural specification: [`docs/architecture/ARCHITECTURE.md`](docs/architecture/ARCHITECTURE.md).

* **Layer 1: Input & Gateway**: PII masking (Vietnam Personal Data Protection Law compliance), Rate Limiting (Redis sliding window), and Semantic Routing (Pipeline A batch vs. Pipeline B real-time).
* **Layer 2: Core Reasoning & Orchestration**: Foundation Models (LLM/SLM), Planning Engine, Cyclic State Machine (FSM), and Self-RAG Reflection Loop.
* **Layer 3: Hierarchical Memory**: Working Context, Sliding Message Buffer, Recall Storage (PostgreSQL), and Archival Vector Memory.
* **Layer 4: Knowledge & Retrieval**: Advanced RAG (Dense Qdrant + Sparse BM25 + Reciprocal Rank Fusion + BGE Cross-Encoder Reranker) and Operational GraphRAG (Neo4j).
* **Layer 5: Tools & Action Protocols**: Function Calling, Model Context Protocol (MCP), and MicroVM / Task Sandboxes.
* **Layer 6: Output & Guardrails**: Claim-level Hallucination Verifier, strict Pydantic Schema Validation, Output PII Filtering, and Policy Compliance Enforcement.
* **Layer 7: Observability & Operations**: OpenTelemetry distributed tracing, Token/Cost accounting per ticket, and Continuous Concept/Data Drift Monitoring.

---

## 3. Repository Structure

The codebase is organized by **Product Capabilities** under a clean Monorepo design:

```text
senticrag/
├── apps/                                  # Applications and user-facing runtimes
│   ├── api/                               # FastAPI Product Service (/api/v1/ingest, /investigation, /resolution, /feedback)
│   ├── agent_workspace/                   # Workspace for CSKH Support Agents to review tickets & drafts (US-AGENT-01)
│   ├── analyst_dashboard/                 # BI Analytics & Root-Cause Investigation Dashboard (US-ANALYST-01, US-PM-01)
│   └── worker/                            # Background asynchronous workers (batch ABSA, Celery/Redis queue, alert jobs)
│       ├── consumers/                     # Message queue consumers
│       └── jobs/                          # Scheduled anomaly detection & reporting jobs
│
├── packages/                              # Domain-Driven Core Packages
│   ├── common/                            # Shared utilities (logging, settings, auth, audit, exceptions)
│   ├── data_contracts/                    # Validated Pydantic contracts across all boundaries
│   ├── customer_context/                  # Customer profile management, PII masking & pseudonymization
│   ├── absa/                              # Aspect-Based Sentiment Analysis (taxonomy, inference, evaluation, calibration)
│   ├── analytics/                         # Quantitative 100% corpus aggregation, trend detection, anomaly alerts
│   ├── retrieval/                         # Advanced Hybrid Retrieval (dense, sparse, RRF fusion, BGE rerank, citations)
│   ├── graph/                             # Neo4j Operational Knowledge Graph (ontology, retrievers, mutations)
│   ├── policy/                            # Structured, versioned warranty and return policy registry
│   ├── resolution/                        # Resolution engine, action routing, and draft synthesis
│   ├── llm/                               # Foundation model layer (prompts, structured_outputs, guardrails, clients)
│   └── feedback/                          # Collaborative feedback loop (annotations, active_learning, knowledge_approval)
│
├── pipelines/                             # Independent offline processing & operational workflows
│   ├── ingest_feedback/                   # Multi-channel feedback ingestion (e-commerce, tickets, chats)
│   ├── pii_masking/                       # Text sanitization, redaction of phone numbers, names, emails
│   ├── absa_batch/                        # Macro quantification over high-volume review corpora
│   ├── build_dense_sparse_index/          # Vector embedding generation and BM25 index creation on Qdrant
│   ├── graph_sync/                        # Entity, defect, and version relationship sync into Neo4j
│   ├── policy_ingestion/                  # Parsing and indexing of warranty documentation into structured registry
│   ├── eval_absa/                         # ABSA regression evaluation harness (Macro-F1)
│   ├── eval_retrieval/                    # Retrieval quality benchmarking (Recall@K, MRR, NDCG)
│   ├── eval_resolution/                   # Resolution safety, policy correctness, and groundedness testing
│   └── retrain_absa/                      # Active learning model retraining triggered by verified human feedback
│
├── infra/                                 # Infrastructure as Code & Deployment
│   ├── docker/                            # Dockerfile.api & Dockerfile.train (Non-root user execution)
│   ├── compose/                           # Local multi-service Docker Compose (Postgres, Qdrant, Neo4j, Redis, API)
│   ├── helm/                              # Kubernetes Helm charts for cloud-native staging/production (EKS)
│   ├── terraform/                         # Terraform modules for EKS, ECR, IAM, S3, KMS
│   └── observability/                     # OpenTelemetry Collector, Prometheus, and Grafana dashboard configs
│
├── tests/                                 # Complete Test Pyramid
│   ├── unit/                              # Unit tests for individual components and API routes
│   ├── integration/                       # Integration tests for database, vector store, and graph connections
│   ├── contract/                          # Contract tests validating schema parity across microservices
│   ├── eval/                              # AI quality benchmarks and hallucination evaluations
│   ├── e2e/                               # End-to-end user-story scenario testing
│   ├── smoke/                             # Fast readiness and liveness checks
│   └── load/                              # Concurrency benchmarks and P95/P99 latency profiling
│
├── docs/                                  # Technical Specifications & Documentation
│   ├── product/                           # User stories, Capability map, Acceptance criteria
│   ├── architecture/                      # Comprehensive Architecture Blueprint (ARCHITECTURE.md) & 7-layer diagrams
│   ├── ontology/                          # Neo4j Graph Ontology Schema (Nodes, Edges, Traversal)
│   ├── adr/                               # Architectural Decision Records
│   ├── model-cards/                       # Machine learning model metadata, training bounds, and limitations
│   ├── data-cards/                        # Dataset provenance, scope, and governance policies
│   └── runbooks/                          # Production incident playbooks, on-call guides, and rollback manuals
│
└── configs/                               # Application configurations (environments, training, evaluation)
```

---

## 4. Quickstart

### Prerequisites
- Python >= 3.11
- Docker & Docker Compose

### 1. Environment Setup
```bash
git clone git@github.com:khuonglaptri3/SenticRAG-Retrieval-Augmented-Aspect-Sentiment-Feedback-Intelligence-Engine.git
cd "SenticRAG-Retrieval-Augmented-Aspect-Sentiment-Feedback-Intelligence-Engine"

python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Launch Local Multi-Service Stack (Docker Compose)
Start the complete infrastructure suite including PostgreSQL, Redis, Qdrant Vector DB, Neo4j Graph DB, and the SenticRAG API:
```bash
docker compose -f infra/compose/docker-compose.yml up -d
```

### 3. Run Automated Tests
```bash
# Execute unit and contract tests
pytest tests/unit tests/contract -v
```

### 4. Start Development API Server
```bash
make run-api
# API available at: http://localhost:8000
# Interactive Swagger Documentation: http://localhost:8000/docs
```

---

## 5. Development Workflow (Gitflow & Conventional Commits)

- **Branches**: `main` (Production releases tagged with version tags, e.g. `v0.2.0`), `develop` (Feature integration).
- **Commit Standards**: Strictly follows Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `ci:`, `infra:`.

---

## License

Distributed under the [MIT License](LICENSE).

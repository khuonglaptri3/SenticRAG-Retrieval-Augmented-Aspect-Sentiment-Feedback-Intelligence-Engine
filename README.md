# SenticRAG — Retrieval-Augmented Aspect Sentiment & Feedback Intelligence Engine

[![CI](https://github.com/khuonglaptri3/SenticRAG/actions/workflows/ci.yml/badge.svg)](https://github.com/khuonglaptri3/SenticRAG/actions/workflows/ci.yml)
[![Python Version](<https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg>)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](infra/docker/)
[![Architecture](<https://img.shields.io/badge/architecture-7--layer%20agent-orange.svg>)](docs/architecture/)

**SenticRAG** is an enterprise-grade AI engine designed for large-scale customer review analysis, aspect-based sentiment extraction, and grounded conversational intelligence with verified citations.

## Key Capabilities

- **Aspect-Based Sentiment Analysis (ABSA):** Bóc tách cảm xúc đa khía cạnh (Chất lượng, Giá cả, Giao hàng, CSKH) với kiến trúc lai (TF-IDF Baseline và Transformer PhoBERT / viBERT fine-tuned).
- **Advanced RAG Engine:** Tìm kiếm lai (Hybrid Search: Dense Vector qua Qdrant + Sparse BM25Okapi) hợp nhất qua giải thuật **Reciprocal Rank Fusion (RRF)** và Cross-Encoder Reranker.
- **Citation & Evidence Grounding:** Tự động đối chiếu và đính kèm ID phản hồi gốc (`[Ref: #RV-xxxxx]`) cho từng luận điểm trong câu trả lời để triệt tiêu ảo giác (Hallucination).
- **Hierarchical Memory Module:** Phân tầng bộ nhớ Working Context, Message Buffer, Archival Vector Memory và tận dụng **Prompt Caching** giảm 50% chi phí suy luận.
- **Production-Ready Operations:** Đóng gói Docker đa tầng (`Dockerfile.api`, `Dockerfile.train`), quản lý hạ tầng Terraform + Helm/EKS, giám sát OpenTelemetry + Prometheus/Grafana.

---

## 🏗️ 7-Layer Architecture Overview

![SenticRAG 7-Layer Architecture](docs/architecture/7_layer_architecture.svg)

> 💡 **Interactive Architecture Viewer**: Mở [`docs/architecture/7_layer_architecture.html`](docs/architecture/7_layer_architecture.html) trên trình duyệt để tương tác trực tiếp với sơ đồ động, xem guided tours (Complete flow, RAG & Knowledge Core, Safety & Observability), phóng to thu nhỏ và tra cứu chi tiết từng node.

### Chi tiết các tầng kiến trúc (7 Layers Breakdown)

| Tầng (Layer) | Thành phần chính | Trách nhiệm cốt lõi |
| :--- | :--- | :--- |
| **Layer 1: Input & Gateway** | `Review Ingestion`, `PII Masker`, `Rate Limiter`, `Normalizer` | Tiếp nhận reviews đa kênh (CSV/Streams), ẩn danh hóa thông tin cá nhân (PII), làm sạch text & emoji, kiểm soát lưu lượng đầu vào qua Token Bucket. |
| **Layer 2: Core Reasoning** | `LLM / SLM Planner`, `Query Decomposition`, `Self-RAG Reflection` | Phân rã câu hỏi phức tạp thành multi-step subqueries, điều phối kế hoạch truy vấn RAG, tự phản tư (reflection) và kiểm tra tính xác thực trước khi tổng hợp. |
| **Layer 3: Hierarchical Memory** | `Working Context`, `Prompt Cache (24h)`, `Archival Vector Memory` | Lưu trữ ngữ cảnh hội thoại đa tầng, tái sử dụng KV cache / prompt cache giảm chi phí & độ trễ, lưu trữ bộ nhớ dài hạn. |
| **Layer 4: Knowledge & Retrieval** | `Hybrid Search (Dense + BM25)`, `RRF Fusion`, `BGE Reranker`, `Citation Engine` | Truy vấn lai kết hợp ngữ nghĩa và từ khóa trên Qdrant, xếp hạng lại kết quả bằng Cross-Encoder (BGE) và gắn định danh nguồn trích dẫn (grounding citations). |
| **Layer 5: Tools & Action Protocols** | `ABSA Tool Calling`, `Structured Outputs`, `Async Alert Worker` | Định dạng kết quả qua Pydantic schema, gọi công cụ phân tích khía cạnh cảm xúc, đẩy tác vụ cảnh báo tiêu cực đột biến qua background workers. |
| **Layer 6: Output & Guardrails** | `Pydantic Validator`, `Hallucination Verifier`, `Strictness Filter` | Thẩm định đầu ra nghiêm ngặt chống ảo giác (hallucination), kiểm soát định dạng, đảm bảo phản hồi an toàn và chính xác 100%. |
| **Layer 7: Observability & Operations** | `OpenTelemetry`, `Prometheus / Grafana`, `Concept Drift Monitor` | Giám sát phân tán end-to-end trace, đo lường độ trễ P95/P99, phát hiện trôi dạt dữ liệu (data & concept drift) và đánh giá chất lượng tự động. |


---

## Repository Structure

```text
SenticRAG — Retrieval-Augmented Aspect Sentiment & Feedback Intelligence Engine/
├── apps/                          # Runtime services
│   ├── api/                       # Core FastAPI service (/predict, /stats, /health)
│   ├── rag_service/               # Grounded RAG query answering service (/ask)
│   └── worker/                    # Background consumers & trend alert jobs
├── packages/                      # Domain packages
│   ├── common/                    # Logging, settings, exceptions
│   ├── data_contracts/            # Pydantic data schemas & contracts
│   ├── ml_core/                   # Metrics, evaluation, artifact lifecycle
│   ├── retrieval/                 # Embeddings, Qdrant vectorstore, rerankers, citations
│   └── llm/                       # LLM clients, prompt templates, structured outputs, guardrails
├── pipelines/                     # Independent offline processing & training pipelines
│   ├── ingest_reviews/            # Ingestion from external sources
│   ├── validate_reviews/          # Data validation & PII sanitization
│   ├── label_reviews/             # Aspect & sentiment labeling
│   ├── train_sentiment/           # Reproducible aspect sentiment training
│   ├── build_embeddings/          # Embedding generation
│   ├── index_qdrant/              # Qdrant vector collection indexing
│   └── eval_rag/                  # Offline RAG evaluation harness (Recall@K, Groundedness)
├── infra/                         # Infrastructure as Code
│   ├── docker/                    # Dockerfile.api & Dockerfile.train
│   ├── helm/                      # Kubernetes Helm charts (project-a/)
│   ├── terraform/                 # Terraform modules for EKS, ECR, IAM, S3, KMS
│   └── observability/             # Prometheus, Grafana, OpenTelemetry configs
├── configs/                       # Environment, training, and evaluation configs
├── tests/                         # Test pyramid (unit, integration, smoke, load, e2e)
├── docs/                          # Architectural specs, ADRs, model cards, runbooks
├── pyproject.toml                 # Monorepo dependencies & packaging
└── Makefile                       # Standard development workflows
```

---

## Quickstart

### Prerequisites

- Python >= 3.11
- Docker & Docker Compose
- Qdrant Vector DB & Redis

### 1. Installation

```bash
git clone git@github.com:khuonglaptri3/SenticRAG-Retrieval-Augmented-Aspect-Sentiment-Feedback-Intelligence-Engine.git
cd "SenticRAG-Retrieval-Augmented-Aspect-Sentiment-Feedback-Intelligence-Engine"
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Run Test Suite

```bash
make test-unit
```

### 3. Local Development Server

```bash
make run-api
```

Truy cập tài liệu API tự động tại: `http://localhost:8000/docs`

---

## Gitflow Branching Strategy

Dự án tuân thủ nghiêm ngặt mô hình **Gitflow**:

- `main`: Nhánh ổn định cao nhất, chứa các bản phát hành Production được gắn tag phiên bản (`v0.1.0`, `v1.0.0`).
- `develop`: Nhánh tích hợp chính cho toàn bộ tính năng mới.
- `feature/*`: Nhánh phát triển tính năng riêng lẻ (tách từ `develop`, merge về `develop`).
- `release/*`: Nhánh chuẩn bị phát hành phiên bản mới.
- `hotfix/*`: Nhánh xử lý sự cố khẩn cấp trên Production (tách từ `main`, merge về cả `main` và `develop`).

Tất cả commit tuân theo quy chuẩn **Conventional Commits**:

- `feat(scope): ...` — Tính năng mới
- `fix(scope): ...` — Sửa lỗi
- `docs(scope): ...` — Thêm hoặc cập nhật tài liệu
- `chore(scope): ...` — Cấu hình, bảo trì, build tool
- `ci(scope): ...` — Cấu hình GitHub Actions / Jenkins
- `infra(scope): ...` — Cấu hình Docker, Helm, Terraform

---

## License

Phát hành theo giấy phép [MIT License](LICENSE).

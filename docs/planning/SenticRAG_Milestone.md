# SenticRAG — Kế hoạch milestone 14 tuần, ưu tiên chatbot

> Baseline lập ngày 23/10/2026. Một người thực hiện: Trần Đình Khương. Bắt đầu thứ Hai 26/10/2026; hết tuần 14 ngày 31/01/2027; ngày làm việc cuối 29/01/2027. Đây là kế hoạch triển khai, không phải báo cáo thành tích.

[Mở workbook milestone](SenticRAG_Milestone.xlsx) · [Xem bản HTML](SenticRAG_Milestone.html) · [Mẫu Excel người dùng cung cấp](https://github.com/khuonglaptri3/qpaf-visual-document-retrieval/blob/feature/m3-6-integrity-review/docs/GUILDLINE_OVERVIEWS_PROPOSAL/POAI_Milestone_Group01_Hoan_Chinh.xlsx)

## 1. Phạm vi, cách tổ chức và giả định lịch

Thiết kế chatbot trước, hoàn thiện một luồng UI → API → retrieval → LLM → citations → history/fallback ở M2. Sau đó nối order/policy decisions, ABSA, BI, GraphRAG và feedback. Backend theo modular monolith để một người bảo trì; worker tách cho batch. Mọi trách nhiệm đều do cùng developer thực hiện, không giả định có thêm ML engineer, frontend engineer hay QA riêng.

**70 ngày T2–T6 = 60 ngày công core/gate + 9 ngày dự phòng + 1 ngày nghỉ dự kiến 01/01/2027.** Một ngày giả định 8 giờ, task nhỏ nhất 0,5 ngày. Lịch chưa bao gồm mọi ngày nghỉ cá nhân hoặc ngày nghỉ bổ sung; nếu part-time hoặc vượt dự phòng thì phải rebaseline. Các phần cloud/real CRM/production approval/business pilot cần quyền và tài nguyên riêng; thiếu thì gate tương ứng để BLOCKED/NOT RUN.

Mức bàn giao 14 tuần là bounded demo 5 vai trò trên dữ liệu có nguồn hoặc synthetic seed được ghi rõ. Full enterprise quality, sustained SLO và hiệu quả kinh doanh thật không được khẳng định chỉ từ demo. Optional advanced vẫn nằm trong traceability và extension backlog.

## 2. Tổng quan các giai đoạn

| Mốc | Tuần | Từ | Đến | Kết quả chính | Core / reserve |
| --- | --- | --- | --- | --- | --- |
| M0 — Thiết kế chatbot và khóa phạm vi | W1–W1 | 26/10/2026 | 30/10/2026 | Thiết kế chatbot, contract v1, wireframe, backlog, quyết định kỹ thuật và bộ kịch bản nghiệm thu. | 4 / 1 |
| M1 — Chuẩn hóa dữ liệu chính sách cho chatbot | W2–W2 | 02/11/2026 | 06/11/2026 | PolicyDocument/PolicyChunk đã duyệt; catalog nguồn; ingest report; policy-QA và privacy fixtures. | 4 / 1 |
| M2 — Chatbot RAG đầu tiên chạy xuyên suốt | W3–W4 | 09/11/2026 | 20/11/2026 | Chat UI + API + history + retrieval + grounded generation; Docker demo; báo cáo benchmark ban đầu. | 9 / 1 |
| M3 — Chatbot theo đơn hàng và Copilot CSKH | W5–W6 | 23/11/2026 | 04/12/2026 | Policy engine + customer tools + FSM + Agent Workspace; ticket/action/outcome và phản hồi được lưu. | 9 / 1 |
| M4 — ABSA và ingestion toàn corpus | W7–W8 | 07/12/2026 | 18/12/2026 | Baseline + candidate ABSA, report, model card; predictions có version; async worker + router; triage tự động. | 9 / 1 |
| M5 — Dashboard toàn corpus và điều tra bằng evidence | W9–W9 | 21/12/2026 | 25/12/2026 | Analyst/PM dashboard, population/denominator, anomaly alert, drill-down giữ nguyên filters, benchmark review retrieval. | 4 / 1 |
| M6 — GraphRAG và quản trị tri thức | W10–W11 | 28/12/2026 | 08/01/2027 | Ontology v1 + Neo4j + graph traversal; analyst/steward UI; knowledge publish/rollback; chatbot có evidence graph. | 9 / 1 |
| M7 — Closed-loop feedback và cải thiện mô hình | W12–W12 | 11/01/2027 | 15/01/2027 | Versioned annotation datasets; active-learning queue; một retraining/eval cycle; drift monitors và publish decision. | 4 / 1 |
| M8 — Tích hợp, vận hành và bàn giao | W13–W14 | 18/01/2027 | 29/01/2027 | Release bundle, 5 UAT demos, eval suite, deploy/IaC package, runbooks, rollback evidence và coverage ledger. | 8 / 2 |

M2 hoàn thành chatbot demo cuối W4 (20/11). M3 có context/eligibility/agent review. M4 có triage ABSA thật. M5 có thống kê và drill-down; M6 nối cause/knowledge vào chatbot; M7 chạy learning loop; M8 kiểm chứng/tài liệu bàn giao. Gate có thể trước ngày cuối phase để dành thời gian sửa.

## 3. Chi tiết thực hiện từng giai đoạn

### M0 — Thiết kế chatbot và khóa phạm vi | W1–W1 | 26/10/2026–30/10/2026

**Mục tiêu:** Chốt kiến trúc hội thoại trước, hợp đồng dùng chung và tiêu chí 14 tuần cho một người.

**Điều kiện bắt đầu:** START; 1 người, 5 ngày làm việc/tuần; kiểm kê API key, máy/GPU, cloud và quyền dữ liệu.

**Input:** Architecture, 5 user stories, mã khung hiện tại, dữ liệu crawl và mẫu Excel.

**Output:** Thiết kế chatbot, contract v1, wireframe, backlog, quyết định kỹ thuật và bộ kịch bản nghiệm thu.

**Module / công nghệ:** MOD-01, MOD-03, MOD-04, MOD-12 — FastAPI/Pydantic; PostgreSQL; React/TypeScript (đề xuất); Docker Compose

**User stories:** US-BUY-01 nền tảng; thiết kế đủ US-AGENT/ANALYST/PM/STEWARD

**Demo cuối giai đoạn:** Walkthrough 3 lượt: hỏi chính sách → hỏi tiếp → thiếu bằng chứng/chuyển người xử lý.

#### M0.1 — Audit repo và lập danh mục yêu cầu

- Lịch: 26/10/2026 (AM) → 26/10/2026; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò BA / kiến trúc.
- Phụ thuộc: START. Loại: Core. Trạng thái baseline: Not Started.
- Input: Toàn bộ tài liệu hiện hữu và commit 9083135
- Cách làm: Phân biệt mock với chức năng thật; kiểm kê crawler, schemas, CI, API; lập ma trận yêu cầu và ghi các doc tham chiếu bị thiếu.
- Output: Baseline inventory; Source Register; traceability IDs; danh sách mâu thuẫn
- Module / công nghệ: MOD-12 — Git; Markdown; Python
- Contract: Review/report theo IO-15.
- Hoàn thành khi: Không dùng số trả cứng trong API làm baseline; mỗi yêu cầu có nguồn và giai đoạn.
- Nguồn: SRC-01..SRC-10; SRC-16

#### M0.2 — Thiết kế UX chatbot, phạm vi và luồng hội thoại

- Lịch: 26/10/2026 (PM) → 27/10/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Product / UX.
- Phụ thuộc: M0.1. Loại: Core. Trạng thái baseline: Not Started.
- Input: US-BUY-01, US-AGENT-01, chính sách mẫu
- Cách làm: Vẽ màn hình chat, citations, history, lỗi và chuyển CSKH; mô tả intent, câu hỏi nối tiếp, thông tin thiếu; tách hỏi chính sách khỏi quyết định theo đơn hàng.
- Output: Wireframe + conversation flow + scope MVP chatbot tuần 4
- Module / công nghệ: MOD-01, MOD-03 — React/TypeScript; design document
- Contract: IO-01, IO-02.
- Hoàn thành khi: MVP trả lời có nguồn và nhớ ngữ cảnh; eligibility cá nhân thuộc M3, root cause xác nhận thuộc M6.
- Nguồn: SRC-02 §3,5,7.9; SRC-03; SRC-04

#### M0.3 — Khóa contract, dữ liệu, công nghệ và API

- Lịch: 27/10/2026 (PM) → 28/10/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Backend / kiến trúc.
- Phụ thuộc: M0.2. Loại: Core. Trạng thái baseline: Not Started.
- Input: M0.1–M0.2; schemas hiện tại; Decisions
- Cách làm: Chọn LLM/embedding qua smoke tiếng Việt, ngân sách và khả năng truy cập; giữ API /api/v1; thiết kế ChatRequest không bắt buộc product_id; chốt namespace, ID, policy version, memory, timeout và cấu hình.
- Output: ADR + schema/chat examples; OpenAPI dự kiến; bảng module; capability/provider matrix
- Module / công nghệ: MOD-01, MOD-02, MOD-03, MOD-04, MOD-12 — Python 3.11/3.12; Poetry lock; FastAPI; Pydantic; PostgreSQL; Redis; Qdrant
- Contract: IO-01..IO-05.
- Hoàn thành khi: Có chính sách session ownership, context limit, không đưa raw PII ra LLM; cloud/GPU thiếu phải ghi tác động.
- Nguồn: SRC-02 §5,8,9; SRC-06; SRC-07; SRC-16

#### M0.4 — Thiết lập nền phát triển và thiết kế nghiệm thu

- Lịch: 28/10/2026 (PM) → 29/10/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Full-stack / QA.
- Phụ thuộc: M0.3. Loại: Core. Trạng thái baseline: Not Started.
- Input: ADR, wireframe, 5 stories và fixture nhỏ
- Cách làm: Tạo cấu trúc conversation/chat app, migration/schema ban đầu, cấu hình môi trường, test scaffold; ghi rubric eval, business baseline và phiên bản artifacts; chuẩn bị login/session boundary.
- Output: Khung ứng dụng có smoke; test plan và rubric; baseline measurement protocol
- Module / công nghệ: MOD-01, MOD-03, MOD-12 — FastAPI; PostgreSQL migrations; React/TypeScript; pytest; Docker Compose; GitHub Actions
- Contract: IO-01, IO-15.
- Hoàn thành khi: Health thật phản ánh dependency; cấu hình không chứa secret; có kế hoạch 5 kịch bản E2E và negative paths.
- Nguồn: SRC-02 §15–17,21; SRC-04; SRC-16

#### M0.G — G0 — Review, nghiệm thu và báo cáo giai đoạn

- Lịch: 29/10/2026 (PM) → 29/10/2026; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò QA / quản lý dự án.
- Phụ thuộc: M0.4. Loại: Gate. Trạng thái baseline: Not Started.
- Input: Các đầu ra và test/eval của M0
- Cách làm: Chạy lại kịch bản nghiệm thu; đối chiếu yêu cầu; ghi PASS/FAIL/BLOCKED, số đo thực và kế hoạch sửa. Tự kiểm tra theo checklist; stakeholder xác nhận nếu có.
- Output: docs/reports/milestones/m0-review.md; checklist; demo; manifest phiên bản
- Module / công nghệ: MOD-12 — pytest; eval reports; Git
- Contract: Review/report theo IO-15.
- Hoàn thành khi: G0: thiết kế chatbot, I/O, scope và ngưỡng eval có owner; quyết định chưa chốt được ghi rõ; 1 người/14 tuần khả thi ở phạm vi demo.
- Nguồn: SRC-02 §21; SRC-03; SRC-04

#### M0.B — Dự phòng sửa lỗi, tích hợp hoặc nghỉ theo lịch thực tế

- Lịch: 30/10/2026 (AM) → 30/10/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Dự phòng.
- Phụ thuộc: RESERVE — không phải quan hệ finish-to-start. Loại: Buffer. Trạng thái baseline: Contingency.
- Input: Blocker/failed gate hoặc ngày nghỉ đã xác nhận
- Cách làm: Ưu tiên sửa gate của giai đoạn; nếu chưa dùng thì giữ quỹ dự phòng. Không tự bổ sung tính năng.
- Output: Gate được kiểm tra lại; nhật ký sử dụng dự phòng và lịch cập nhật
- Module / công nghệ: MOD-12 — Issue log; regression tests
- Contract: Review/report theo IO-15.
- Hoàn thành khi: Không vượt ngày kết thúc giai đoạn; nếu vượt phải rebaseline, không đánh dấu Done khi gate fail.
- Nguồn: DEC-01; DEC-02


### M1 — Chuẩn hóa dữ liệu chính sách cho chatbot | W2–W2 | 02/11/2026–06/11/2026

**Mục tiêu:** Biến dữ liệu crawl thành knowledge base được kiểm duyệt và truy nguồn.

**Điều kiện bắt đầu:** G0 PASS; tài liệu có quyền sử dụng; chốt phạm vi demo 5–10 policy (~30 điều khoản).

**Input:** Raw HTML/text/page.json/report từ Data_crawling; tài liệu do người dùng cung cấp.

**Output:** PolicyDocument/PolicyChunk đã duyệt; catalog nguồn; ingest report; policy-QA và privacy fixtures.

**Module / công nghệ:** MOD-02, MOD-06, MOD-12 — Python parser; Pydantic; PostgreSQL; JSONL; regex + NER

**User stories:** US-BUY-01 / US-AGENT-01 nguồn chính sách; US-STEWARD-01 duyệt tài liệu

**Demo cuối giai đoạn:** Từ URL gốc → nội dung sạch → đoạn trích chứa đủ điều kiện/ngoại lệ.

#### M1.1 — Kiểm kê và tiếp nhận snapshot crawler

- Lịch: 02/11/2026 (AM) → 02/11/2026; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò Data engineering.
- Phụ thuộc: M0.G. Loại: Core. Trạng thái baseline: Not Started.
- Input: Các snapshot và báo cáo crawl đã có
- Cách làm: Đọc export qua adapter/file manifest; xác minh 52/56 là số ghi nhận lịch sử; chọn subset policy; kiểm tra lỗi/redirect/quyền sử dụng; giữ crawler độc lập.
- Output: source_inventory.csv; raw manifest có URL, hash, crawl time, status
- Module / công nghệ: MOD-02 — Python; JSON; SHA-256
- Contract: IO-03.
- Hoàn thành khi: Không coi crawl thành công là đủ nội dung; không crawl lại toàn bộ nếu snapshot dùng được.
- Nguồn: SRC-10; SRC-11; SRC-12; SRC-13

#### M1.2 — Làm sạch, chia đoạn và gắn provenance

- Lịch: 02/11/2026 (PM) → 03/11/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Data engineering.
- Phụ thuộc: M1.1. Loại: Core. Trạng thái baseline: Not Started.
- Input: Raw HTML/text + inventory
- Cách làm: Bỏ navigation/footer; giữ heading, bảng, điều kiện/ngoại lệ; dedup; chunk theo điều khoản; xử lý missing/empty; lưu raw offset và hash ổn định.
- Output: policies_clean.jsonl; policy_chunks.jsonl; cleaning QA report
- Module / công nghệ: MOD-02 — Python HTML parser; Pydantic; JSONL
- Contract: IO-03, IO-04.
- Hoàn thành khi: Mỗi đoạn resolve được nguồn; kiểm tra thủ công toàn bộ ~30 điều khoản demo; chạy lại không nhân đôi.
- Nguồn: SRC-06 §4–5,8; SRC-10

#### M1.3 — Policy catalog, trạng thái duyệt và PII boundary

- Lịch: 03/11/2026 (PM) → 04/11/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Backend / Data.
- Phụ thuộc: M1.2. Loại: Core. Trạng thái baseline: Not Started.
- Input: Policy chunks; draft registry; synthetic PII
- Cách làm: Lưu version/effective dates/scope/status; ngày không biết giữ unknown để duyệt; che PII text/logs; chỉ đưa policy approved vào index; tách dữ liệu đơn hàng.
- Output: Registry migrations; policy versions; masking service; fixture assertions
- Module / công nghệ: MOD-02, MOD-06, MOD-12 — PostgreSQL; Pydantic; regex + NER; pytest
- Contract: IO-04, IO-07.
- Hoàn thành khi: Draft/expired/unknown-effectivity không dùng để kết luận quyền lợi; không raw PII trong index/prompt/log fixtures.
- Nguồn: SRC-02 §7.2,7.8,14; SRC-06 §2,5

#### M1.4 — Tạo bộ đánh giá chatbot và privacy ban đầu

- Lịch: 04/11/2026 (PM) → 05/11/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò QA / Data.
- Phụ thuộc: M1.3. Loại: Core. Trạng thái baseline: Not Started.
- Input: ~30 clauses đã duyệt; rubric M0.4
- Cách làm: Soạn 40 policy questions có relevance labels và expected sources; tách tuning/held-out theo intent/document; 20 hội thoại nhiều lượt; sinh 500 PII fixtures rồi kiểm mẫu thủ công; thêm expired/conflict/no-evidence/injection.
- Output: golden_policy_queries.jsonl; chat_eval.jsonl; pii_eval.jsonl + manifests
- Module / công nghệ: MOD-02, MOD-12 — JSONL; Python; pytest; annotation rubric
- Contract: IO-14.
- Hoàn thành khi: Có no-answer và follow-up; test set không dùng tune prompt; synthetic PII được ghi đúng nguồn và giới hạn.
- Nguồn: SRC-06 §2,4,6; SRC-07 §ABSA/Retrieval eval

#### M1.G — G1 — Review, nghiệm thu và báo cáo giai đoạn

- Lịch: 05/11/2026 (PM) → 05/11/2026; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò QA / quản lý dự án.
- Phụ thuộc: M1.4. Loại: Gate. Trạng thái baseline: Not Started.
- Input: Các đầu ra và test/eval của M1
- Cách làm: Chạy lại kịch bản nghiệm thu; đối chiếu yêu cầu; ghi PASS/FAIL/BLOCKED, số đo thực và kế hoạch sửa. Tự kiểm tra theo checklist; stakeholder xác nhận nếu có.
- Output: docs/reports/milestones/m1-review.md; checklist; demo; manifest phiên bản
- Module / công nghệ: MOD-12 — pytest; eval reports; Git
- Contract: Review/report theo IO-15.
- Hoàn thành khi: G1: 5–10 policies/~30 clauses đã duyệt, truy nguồn đầy đủ; 40 queries + 20 hội thoại; privacy fixtures; ingestion idempotent.
- Nguồn: SRC-06; SRC-10; SRC-04

#### M1.B — Dự phòng sửa lỗi, tích hợp hoặc nghỉ theo lịch thực tế

- Lịch: 06/11/2026 (AM) → 06/11/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Dự phòng.
- Phụ thuộc: RESERVE — không phải quan hệ finish-to-start. Loại: Buffer. Trạng thái baseline: Contingency.
- Input: Blocker/failed gate hoặc ngày nghỉ đã xác nhận
- Cách làm: Ưu tiên sửa gate của giai đoạn; nếu chưa dùng thì giữ quỹ dự phòng. Không tự bổ sung tính năng.
- Output: Gate được kiểm tra lại; nhật ký sử dụng dự phòng và lịch cập nhật
- Module / công nghệ: MOD-12 — Issue log; regression tests
- Contract: Review/report theo IO-15.
- Hoàn thành khi: Không vượt ngày kết thúc giai đoạn; nếu vượt phải rebaseline, không đánh dấu Done khi gate fail.
- Nguồn: DEC-01; DEC-02


### M2 — Chatbot RAG đầu tiên chạy xuyên suốt | W3–W4 | 09/11/2026–20/11/2026

**Mục tiêu:** Bàn giao chatbot tiếng Việt có hội thoại, evidence và fallback trên dữ liệu thật đã làm sạch.

**Điều kiện bắt đầu:** G1 PASS; API key/provider hoặc mô hình local chạy được; máy đủ embedding corpus nhỏ.

**Input:** Policy chunks approved, contracts/chat wireframe, golden sets, provider cấu hình được.

**Output:** Chat UI + API + history + retrieval + grounded generation; Docker demo; báo cáo benchmark ban đầu.

**Module / công nghệ:** MOD-01, MOD-03, MOD-04, MOD-12 — FastAPI; React/TypeScript; PostgreSQL; Redis; Qdrant; BM25/RRF; LLM API; BGE candidate

**User stories:** US-BUY-01 mức policy Q&A; US-AGENT-01 evidence nền tảng; chưa đủ full story

**Demo cuối giai đoạn:** Hỏi đổi trả → hỏi tiếp ngoại lệ → hiện nguồn; câu không đủ evidence → clarification/handoff.

#### M2.1 — Lập chỉ mục và retrieval có bộ lọc

- Lịch: 09/11/2026 (AM) → 10/11/2026; 1.5 ngày; Trần Đình Khương đảm nhiệm vai trò Backend / ML.
- Phụ thuộc: M1.G. Loại: Core. Trạng thái baseline: Not Started.
- Input: Policy chunks và index contract
- Cách làm: Tạo namespace policies, dense + BM25 baseline, metadata indexes; enforce approved/effective/tenant filters; build snapshot và readiness; citations trả clause ID + URL.
- Output: Index build pipeline; retrieval service; source resolver; index manifest
- Module / công nghệ: MOD-04 — Qdrant; sentence-transformers; BM25; Python
- Contract: IO-04, IO-05.
- Hoàn thành khi: Count/hash đối chiếu; empty/index unavailable có trạng thái rõ; nguồn thật, bộ lọc đúng trên fixtures.
- Nguồn: SRC-02 §7.5; SRC-06 §4; SRC-07 Retrieval

#### M2.2 — Benchmark BM25, dense và hybrid RRF

- Lịch: 10/11/2026 (PM) → 11/11/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò ML / QA.
- Phụ thuộc: M2.1. Loại: Core. Trạng thái baseline: Not Started.
- Input: Policy query tuning + held-out; index snapshots
- Cách làm: Đánh giá riêng ba mode cùng corpus/query; tune chỉ trên dev; đo Recall@5/@10, MRR, nDCG, p95, memory và cost; chốt mode theo kết quả.
- Output: retrieval_policy_baseline.json + report + selected config
- Module / công nghệ: MOD-04 — rank-bm25; Qdrant; RRF; Python eval
- Contract: IO-14.
- Hoàn thành khi: Không mặc định hybrid thắng; giữ per-query outputs và manifest; số liệu chưa đạt phải ghi FAIL.
- Nguồn: SRC-02 §13.2; SRC-07 Retrieval; WEB-02

#### M2.3 — Đánh giá reranker trên tập nhỏ

- Lịch: 11/11/2026 (PM) → 11/11/2026; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò ML.
- Phụ thuộc: M2.2. Loại: Core. Trạng thái baseline: Not Started.
- Input: Candidates và benchmark M2.2
- Cách làm: Thử BGE cross-encoder Top-50 → Top-5/10; so chất lượng/latency theo rubric đã khóa; giữ feature flag nếu chưa có gain.
- Output: Reranker adapter; enable/disable ADR và giới hạn tài nguyên
- Module / công nghệ: MOD-04 — BGE cross-encoder candidate; sentence-transformers
- Contract: IO-05.
- Hoàn thành khi: Chỉ bật runtime nếu held-out gain và latency budget đạt; score không được gọi là xác suất đúng.
- Nguồn: SRC-02 §7.5; SRC-07 RET-AC-08

#### M2.4 — Sinh câu trả lời có nguồn và kiểm soát đầu ra

- Lịch: 12/11/2026 (AM) → 12/11/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Backend / LLM.
- Phụ thuộc: M2.3. Loại: Core. Trạng thái baseline: Not Started.
- Input: EvidencePack; model config; chat eval
- Cách làm: Viết client có timeout/retry hữu hạn; prompt tiếng Việt theo evidence; schema output; kiểm citation tồn tại/đúng clause và claims; abstain hoặc hỏi thêm; ghi prompt/model version.
- Output: LLM service + guardrails + Answer contract
- Module / công nghệ: MOD-03 — LLM API cấu hình; HTTP client; Pydantic; pytest
- Contract: IO-02, IO-05.
- Hoàn thành khi: Không bịa policy/refund; không có nguồn thì không khẳng định; schema invalid không trả nội dung chưa kiểm.
- Nguồn: SRC-02 §7.9; SRC-04; SRC-06 §6

#### M2.5 — API chat, phiên và bộ nhớ nhiều lượt

- Lịch: 13/11/2026 (AM) → 16/11/2026; 1.5 ngày; Trần Đình Khương đảm nhiệm vai trò Backend.
- Phụ thuộc: M2.4. Loại: Core. Trạng thái baseline: Not Started.
- Input: ChatRequest/Response, generation service, PostgreSQL
- Cách làm: POST /api/v1/chat/messages; lưu message/request_id/idempotency; ownership; sliding context và summary; rewrite follow-up từ lịch sử; hủy/timeout; chỉ truy lịch sử được phép.
- Output: Conversation service; migrations; session/history endpoints; auth integration
- Module / công nghệ: MOD-01 — FastAPI; PostgreSQL; Redis cache; Pydantic
- Contract: IO-01, IO-02.
- Hoàn thành khi: Hai phiên không lẫn dữ liệu; retry không nhân đôi message; follow-up giữ policy context; không bắt nhập product cho câu hỏi chung.
- Nguồn: SRC-02 §5.4,7.9; SRC-16

#### M2.6 — Giao diện chatbot và nguồn tham khảo

- Lịch: 16/11/2026 (PM) → 17/11/2026; 1.5 ngày; Trần Đình Khương đảm nhiệm vai trò Frontend.
- Phụ thuộc: M2.5. Loại: Core. Trạng thái baseline: Not Started.
- Input: Wireframe; chat/history API
- Cách làm: Tạo màn chat, lịch sử, nguồn clickable, error/retry, loading, clarification và nút chuyển hỗ trợ; nối API thật; kiểm desktop/mobile và accessibility cơ bản.
- Output: apps/chatbot chạy với backend thật; UI smoke scripts
- Module / công nghệ: MOD-01 — React; TypeScript; CSS; browser tests
- Contract: IO-01, IO-02.
- Hoàn thành khi: Cả happy path và thiếu bằng chứng hoạt động; trạng thái chờ không tạo nội dung giả; nguồn mở đúng clause/doc.
- Nguồn: SRC-03 US-BUY-01; SRC-02 §3.1; WEB-04

#### M2.7 — Telemetry, đóng gói demo và xử lý dependency fail

- Lịch: 18/11/2026 (AM) → 18/11/2026; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò Platform.
- Phụ thuộc: M2.6. Loại: Core. Trạng thái baseline: Not Started.
- Input: Chat app + retrieval + generation
- Cách làm: Trace request→retrieval→LLM; đếm token/cost/latency; log đã redacted; Compose startup và readiness thật; thử Qdrant/LLM timeout.
- Output: Compose demo; logs/traces; run instructions
- Module / công nghệ: MOD-12 — Docker Compose; OpenTelemetry; structured logging
- Contract: IO-15.
- Hoàn thành khi: Có source/model/index/prompt version; không success giả khi dependency hỏng.
- Nguồn: SRC-02 §15–16; SRC-07 NFR

#### M2.8 — Đánh giá chatbot end-to-end và sửa lỗi

- Lịch: 18/11/2026 (PM) → 19/11/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò QA.
- Phụ thuộc: M2.7. Loại: Core. Trạng thái baseline: Not Started.
- Input: 40 policy queries; 20 dialogues; privacy/attack cases
- Cách làm: Chạy suite frozen; review answer/citation; kiểm response ownership, injection, expired policy, no-answer và request duplicate; ghi latency thực và hạn chế.
- Output: chatbot_mvp_eval report; demo recording; regression suite
- Module / công nghệ: MOD-01, MOD-03, MOD-04, MOD-12 — pytest; browser tests; human rubric
- Contract: IO-14.
- Hoàn thành khi: MVP: ≥90% policy QA rubric pass (đề xuất); citation completeness ≥95%; 0 unsupported promises/PII leaks trên suite; full response <60s trên kịch bản chuẩn.
- Nguồn: SRC-04; SRC-02 §9,13; SRC-06 §6

#### M2.G — G2 — Review, nghiệm thu và báo cáo giai đoạn

- Lịch: 19/11/2026 (PM) → 19/11/2026; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò QA / quản lý dự án.
- Phụ thuộc: M2.8. Loại: Gate. Trạng thái baseline: Not Started.
- Input: Các đầu ra và test/eval của M2
- Cách làm: Chạy lại kịch bản nghiệm thu; đối chiếu yêu cầu; ghi PASS/FAIL/BLOCKED, số đo thực và kế hoạch sửa. Tự kiểm tra theo checklist; stakeholder xác nhận nếu có.
- Output: docs/reports/milestones/m2-review.md; checklist; demo; manifest phiên bản
- Module / công nghệ: MOD-12 — pytest; eval reports; Git
- Contract: Review/report theo IO-15.
- Hoàn thành khi: G2: chatbot UI→API→retrieval→LLM→citations chạy thật; multi-turn/fallback/privacy pass; benchmark riêng retrieval và generation.
- Nguồn: SRC-03 US-BUY-01; SRC-04; SRC-02 §21

#### M2.B — Dự phòng sửa lỗi, tích hợp hoặc nghỉ theo lịch thực tế

- Lịch: 20/11/2026 (AM) → 20/11/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Dự phòng.
- Phụ thuộc: RESERVE — không phải quan hệ finish-to-start. Loại: Buffer. Trạng thái baseline: Contingency.
- Input: Blocker/failed gate hoặc ngày nghỉ đã xác nhận
- Cách làm: Ưu tiên sửa gate của giai đoạn; nếu chưa dùng thì giữ quỹ dự phòng. Không tự bổ sung tính năng.
- Output: Gate được kiểm tra lại; nhật ký sử dụng dự phòng và lịch cập nhật
- Module / công nghệ: MOD-12 — Issue log; regression tests
- Contract: Review/report theo IO-15.
- Hoàn thành khi: Không vượt ngày kết thúc giai đoạn; nếu vượt phải rebaseline, không đánh dấu Done khi gate fail.
- Nguồn: DEC-01; DEC-02


### M3 — Chatbot theo đơn hàng và Copilot CSKH | W5–W6 | 23/11/2026–04/12/2026

**Mục tiêu:** Thêm quyết định chính sách có kiểm soát, chuyển người xử lý và lưu outcome.

**Điều kiện bắt đầu:** G2 PASS; data demo được đánh dấu synthetic; quyền CRM thật chỉ cần khi chọn live adapter.

**Input:** Chatbot G2; policy clauses; seed products/orders/customers; resolution scenarios.

**Output:** Policy engine + customer tools + FSM + Agent Workspace; ticket/action/outcome và phản hồi được lưu.

**Module / công nghệ:** MOD-01, MOD-03, MOD-05, MOD-06, MOD-11, MOD-12 — PostgreSQL; deterministic rules; FastAPI; MCP adapters; React; bounded FSM

**User stories:** US-BUY-01 resolution path; US-AGENT-01 workspace/outcomes; ABSA tự động bổ sung M4

**Demo cuối giai đoạn:** Đơn còn hạn → draft có điều kiện; hết hạn/không sở hữu đơn → không hứa quyền lợi; agent sửa/duyệt/escalate.

#### M3.1 — Mô hình đơn hàng, ticket, action và outcome

- Lịch: 23/11/2026 (AM) → 23/11/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Backend / Data.
- Phụ thuộc: M2.G. Loại: Core. Trạng thái baseline: Not Started.
- Input: Seed specs + contracts M0
- Cách làm: Migration customer/order/product/version/ticket/action/outcome; seed 5–10 sản phẩm, ~15 phiên bản, 200 orders; mọi dữ liệu demo có synthetic flag; thiết kế idempotency và timestamps.
- Output: Relational seed + schema + ticket lifecycle endpoints
- Module / công nghệ: MOD-05, MOD-06 — PostgreSQL; Pydantic; migrations
- Contract: IO-06, IO-09.
- Hoàn thành khi: Bridge keys nhất quán; FK hợp lệ; không giả lập 200 khách thật; lịch sử ticket không overwrite.
- Nguồn: SRC-02 §8; SRC-06 §5,8

#### M3.2 — Tra cứu đơn hàng có xác thực và kiểm soát truy cập

- Lịch: 24/11/2026 (AM) → 24/11/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Backend.
- Phụ thuộc: M3.1. Loại: Core. Trạng thái baseline: Not Started.
- Input: Orders + auth/session
- Cách làm: Implement query_customer_order và context adapter; kiểm order ownership trước đọc; chỉ expose trường cần; tìm region/service center; hỏi lại khi thiếu hoặc không khớp.
- Output: Customer context service + tool schemas + seed CRM adapter
- Module / công nghệ: MOD-05 — FastAPI; PostgreSQL; typed tools; RBAC
- Contract: IO-06.
- Hoàn thành khi: Cross-customer access bị chặn; trạng thái unknown tách ineligible; raw PII không vào prompt/index/log.
- Nguồn: SRC-02 §3.1,7.2,14; SRC-06 §5

#### M3.3 — Policy engine xác định quyền lợi bằng rule

- Lịch: 25/11/2026 (AM) → 25/11/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Backend.
- Phụ thuộc: M3.2. Loại: Core. Trạng thái baseline: Not Started.
- Input: Approved policy rules; order context
- Cách làm: Match product/date/scope/version; evaluate eligibility; trả missing_fields, allowed/prohibited_actions; xử lý policy conflict/stale; trường hợp tiền/ngoại lệ cần người duyệt.
- Output: PolicyDecision service; rule tests; evidence-linked decision log
- Module / công nghệ: MOD-06 — Python decision rules; PostgreSQL; Pydantic
- Contract: IO-07.
- Hoàn thành khi: Không dùng LLM quyết eligibility; ranh ngày mua/expiry đúng; policy ví dụ 365 ngày chỉ dùng synthetic fixture.
- Nguồn: SRC-02 §7.8; SRC-06 §5–6

#### M3.4 — FSM resolution, MCP tools và reflection hữu hạn

- Lịch: 26/11/2026 (AM) → 27/11/2026; 1.5 ngày; Trần Đình Khương đảm nhiệm vai trò Backend / orchestration.
- Phụ thuộc: M3.3. Loại: Core. Trạng thái baseline: Not Started.
- Input: Chat, policy decision, tools, ticket model
- Cách làm: Ingested→context→evidence→decision→draft→guarded→approved/escalated; giới hạn 1 lượt bổ sung evidence và timeout; MCP adapter query order/check warranty/route ticket; Pydantic inputs, allowlist, audit.
- Output: Resolution orchestrator; /api/v1/resolution/draft nối thật; tool integration tests
- Module / công nghệ: MOD-01, MOD-03, MOD-05, MOD-06 — Python FSM; MCP SDK/adapter; FastAPI; Pydantic
- Contract: IO-08.
- Hoàn thành khi: Retry không lặp action; lỗi/thiếu evidence chuyển đúng hàng đợi; không tự xác nhận root cause; action cần approval không chạy trước duyệt.
- Nguồn: SRC-02 §7.9; SRC-05 L2,L5,L6

#### M3.5 — Agent Workspace: context, evidence và review

- Lịch: 27/11/2026 (PM) → 30/11/2026; 1.5 ngày; Trần Đình Khương đảm nhiệm vai trò Frontend.
- Phụ thuộc: M3.4. Loại: Core. Trạng thái baseline: Not Started.
- Input: Ticket/draft/citation APIs
- Cách làm: Ticket list/card: order, warranty, urgency, evidence/policy dates; approve/edit/reject với reason; specialist escalation; ABSA tạm hiển thị pending/manual; hypothesis label rõ.
- Output: Agent Workspace + review endpoints; browser flows
- Module / công nghệ: MOD-11 — React; TypeScript; FastAPI; PostgreSQL
- Contract: IO-08, IO-09, IO-13.
- Hoàn thành khi: Agent đọc được bằng chứng trước duyệt; chỉnh sửa có tác giả/thời gian; không hiển thị hypothesis thành fact.
- Nguồn: SRC-02 §3.2; SRC-14

#### M3.6 — Lưu phản hồi cuối, outcome và business events

- Lịch: 01/12/2026 (AM) → 01/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Backend / Analytics.
- Phụ thuộc: M3.5. Loại: Core. Trạng thái baseline: Not Started.
- Input: Agent action + customer outcome
- Cách làm: Persist final response, sent/resolved/reopened/CSAT events và ticket owner; thu thập timestamps phục vụ FRT/AHT/MTTR/FCR; mapping complaint→ingest event cho ABSA về sau.
- Output: Outcome API; audit events; metric dictionary và baseline captures
- Module / công nghệ: MOD-06, MOD-09, MOD-11 — PostgreSQL; Pydantic; event log
- Contract: IO-09, IO-15.
- Hoàn thành khi: Một action idempotent chỉ ghi một lần; outcome thiếu hiển thị unknown; log phiên bản policy/model/evidence/human reviewer.
- Nguồn: SRC-02 §3.1–3.4,8,13.5; SRC-04

#### M3.7 — Đánh giá resolution và luồng hỗ trợ

- Lịch: 02/12/2026 (AM) → 02/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò QA.
- Phụ thuộc: M3.6. Loại: Core. Trạng thái baseline: Not Started.
- Input: 30 resolution cases giai đoạn đầu; order/privacy fixtures
- Cách làm: Test trong hạn/hết hạn/missing order/unconfirmed issue/prompt injection; approve/edit/reject/escalate; đo manual-vs-assisted cùng kịch bản; review chính sách và citation.
- Output: Resolution eval v1; UAT agent/buyer; baseline report
- Module / công nghệ: MOD-03, MOD-05, MOD-06, MOD-11 — pytest; browser tests; JSONL rubric
- Contract: IO-14.
- Hoàn thành khi: 0 unsupported actions trên suite; 100% policy claim có clause/version; safety issue vào priority queue; chưa tuyên bố AHT giảm 40% từ dữ liệu demo.
- Nguồn: SRC-06 §6; SRC-02 BUY-AC/AG-AC; SRC-03

#### M3.8 — Cô lập công cụ và lỗi thực thi

- Lịch: 03/12/2026 (AM) → 03/12/2026; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò Platform / Security.
- Phụ thuộc: M3.7. Loại: Core. Trạng thái baseline: Not Started.
- Input: Tool adapters và action allowlist
- Cách làm: Thiết lập process/task timeout, restricted tool inputs, quyền tối thiểu; công cụ mô phỏng external action ghi rõ sandbox; đánh giá nhu cầu microVM như extension.
- Output: Task isolation config; timeout/retry audit; microVM decision
- Module / công nghệ: MOD-06, MOD-12 — Process/task isolation; Docker; MCP adapter
- Contract: IO-08.
- Hoàn thành khi: Không thực thi shell tự do từ LLM; side effect có token/idempotency và approval; sandbox không bị trình bày như giao dịch thật.
- Nguồn: SRC-05 L5; SRC-02 §7.9

#### M3.G — G3 — Review, nghiệm thu và báo cáo giai đoạn

- Lịch: 03/12/2026 (PM) → 03/12/2026; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò QA / quản lý dự án.
- Phụ thuộc: M3.8. Loại: Gate. Trạng thái baseline: Not Started.
- Input: Các đầu ra và test/eval của M3
- Cách làm: Chạy lại kịch bản nghiệm thu; đối chiếu yêu cầu; ghi PASS/FAIL/BLOCKED, số đo thực và kế hoạch sửa. Tự kiểm tra theo checklist; stakeholder xác nhận nếu có.
- Output: docs/reports/milestones/m3-review.md; checklist; demo; manifest phiên bản
- Module / công nghệ: MOD-12 — pytest; eval reports; Git
- Contract: Review/report theo IO-15.
- Hoàn thành khi: G3: order ownership + deterministic policy + agent review/outcome pass; điều kiện thiếu được hỏi lại; có ticket tới specialist thật trong app.
- Nguồn: SRC-02 BUY-AC-02..05; AG-AC-01..05; SRC-04

#### M3.B — Dự phòng sửa lỗi, tích hợp hoặc nghỉ theo lịch thực tế

- Lịch: 04/12/2026 (AM) → 04/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Dự phòng.
- Phụ thuộc: RESERVE — không phải quan hệ finish-to-start. Loại: Buffer. Trạng thái baseline: Contingency.
- Input: Blocker/failed gate hoặc ngày nghỉ đã xác nhận
- Cách làm: Ưu tiên sửa gate của giai đoạn; nếu chưa dùng thì giữ quỹ dự phòng. Không tự bổ sung tính năng.
- Output: Gate được kiểm tra lại; nhật ký sử dụng dự phòng và lịch cập nhật
- Module / công nghệ: MOD-12 — Issue log; regression tests
- Contract: Review/report theo IO-15.
- Hoàn thành khi: Không vượt ngày kết thúc giai đoạn; nếu vượt phải rebaseline, không đánh dấu Done khi gate fail.
- Nguồn: DEC-01; DEC-02


### M4 — ABSA và ingestion toàn corpus | W7–W8 | 07/12/2026–18/12/2026

**Mục tiêu:** Tạo dữ liệu sentiment/aspect thật để triage và thống kê toàn bộ corpus.

**Điều kiện bắt đầu:** G3 PASS; chốt dataset/license/splits tại M0; compute đã sẵn hoặc candidate không chạy ghi BLOCKED.

**Input:** Review/ticket/chat đã mask; UIT-ViSFD/ViSD4SA được phép sử dụng; taxonomy; corrections.

**Output:** Baseline + candidate ABSA, report, model card; predictions có version; async worker + router; triage tự động.

**Module / công nghệ:** MOD-02, MOD-07, MOD-12 — scikit-learn; PyTorch/Transformers/PhoBERT candidate; PostgreSQL; Redis Streams

**User stories:** Hoàn thiện BUY-AC-01; US-AGENT-01 triage; nền US-ANALYST-01/US-PM-01

**Demo cuối giai đoạn:** “Máy đẹp nhưng pin yếu” → hai aspect/polarity; toàn corpus được xử lý, ticket card có triage thật.

#### M4.1 — Khóa taxonomy, splits và dataset provenance

- Lịch: 07/12/2026 (AM) → 07/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò ML / Data.
- Phụ thuộc: M3.G. Loại: Core. Trạng thái baseline: Not Started.
- Input: UIT datasets + domain records + policy quyền dữ liệu
- Cách làm: Kiểm count/split chính thức thay vì áp tỷ lệ minh họa; map 10 aspects và nhóm macro; dedup leakage; giữ test locked; xác định labels span cho ATE; bổ sung delivery/service nếu thiếu.
- Output: aspect_taxonomy_v1.yaml; train/dev/test parquet + data card/manifests
- Module / công nghệ: MOD-07 — Python; pandas; Parquet; schema validation
- Contract: IO-10, IO-14.
- Hoàn thành khi: Không trộn test vào train; thiếu span labels không báo ATE đạt; vùng domain chưa đủ mẫu ghi hạn chế.
- Nguồn: SRC-06 §3; SRC-07 ABSA; SRC-02 §7.3

#### M4.2 — ABSA baseline và evaluation harness

- Lịch: 08/12/2026 (AM) → 08/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò ML.
- Phụ thuộc: M4.1. Loại: Core. Trạng thái baseline: Not Started.
- Input: Frozen train/dev/test + taxonomy
- Cách làm: TF-IDF + Logistic Regression cho aspect detection và sentiment theo aspect; chuẩn hóa tiếng Việt; output schema; label none/other và unsupported language; metric per-aspect/polarity.
- Output: Baseline model; inference; eval scripts; confusion matrices
- Module / công nghệ: MOD-07 — scikit-learn; Python; pytest
- Contract: IO-10.
- Hoàn thành khi: Reproducible seed; lưu model/taxonomy version; baseline và candidate dùng cùng split/metric.
- Nguồn: SRC-07 ABSA-AC-01..10; SRC-02 §13.1

#### M4.3 — Huấn luyện candidate và evidence spans

- Lịch: 09/12/2026 (AM) → 10/12/2026; 2 ngày; Trần Đình Khương đảm nhiệm vai trò ML.
- Phụ thuộc: M4.2. Loại: Core. Trạng thái baseline: Not Started.
- Input: Baseline, labeled splits và GPU/CPU budget
- Cách làm: Fine-tune một PhoBERT candidate có bounded run; ATE chỉ trên dữ liệu span phù hợp; calibration trên dev; slices phủ định/slang/emoji/multi-aspect; không search rộng.
- Output: Candidate checkpoint; logs; calibration; span extraction report; model card
- Module / công nghệ: MOD-07 — PyTorch; Transformers; PhoBERT candidate; temperature scaling
- Contract: IO-10, IO-15.
- Hoàn thành khi: Báo riêng aspect, polarity và span F1; confidence không tự nhận là calibrated nếu chưa đo; run manifest có dataset/code/config hashes.
- Nguồn: SRC-06 §3; SRC-07 ABSA; SRC-15

#### M4.4 — Chốt model bằng benchmark và release floor

- Lịch: 11/12/2026 (AM) → 11/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò ML / QA.
- Phụ thuộc: M4.3. Loại: Core. Trạng thái baseline: Not Started.
- Input: Baseline/candidate predictions
- Cách làm: So Macro-F1/per-aspect/span/ECE và latency/memory; chọn model đạt floor; low-confidence (<0.70 tạm đề xuất) vào review queue; giữ mô hình cũ nếu regression.
- Output: ABSA comparison report; champion config; release decision
- Module / công nghệ: MOD-07 — scikit-learn metrics; Python eval; model registry manifest
- Contract: IO-14.
- Hoàn thành khi: MVP floor 0.80 chỉ demo; production target 0.85, critical aspect 0.75; thiếu threshold phải fail/giới hạn, không chỉnh số đo.
- Nguồn: SRC-06 §3.3; SRC-04; SRC-07

#### M4.5 — Ingestion, queue và batch phủ toàn corpus

- Lịch: 14/12/2026 (AM) → 15/12/2026; 1.5 ngày; Trần Đình Khương đảm nhiệm vai trò Backend / Data.
- Phụ thuộc: M4.4. Loại: Core. Trạng thái baseline: Not Started.
- Input: ABSA model; FeedbackRecord; review data
- Cách làm: POST ingest persist rồi queue; dedup source+ID; validate spam/empty/date/lang; Redis Streams consumer retry/DLQ; infer tất cả accepted records; append predictions và enrich review index.
- Output: Pipeline A; workers; absa_predictions; feedback_reviews index; coverage report
- Module / công nghệ: MOD-02, MOD-04, MOD-07 — FastAPI; Redis Streams; PostgreSQL; Qdrant
- Contract: IO-03, IO-10.
- Hoàn thành khi: Không giới hạn bằng top_k; accepted=processed+pending+failed có lý do; replay không trùng; model version không overwrite.
- Nguồn: SRC-02 §5.2,7.1,8; SRC-06 §2–4; SRC-14

#### M4.6 — Semantic router, rate limit và triage API

- Lịch: 15/12/2026 (PM) → 16/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Backend / ML.
- Phụ thuộc: M4.5. Loại: Core. Trạng thái baseline: Not Started.
- Input: Router labels, known safety patterns, ABSA inference
- Cách làm: Seed 1,500 router texts bằng templates + kiểm thủ công mẫu; benchmark rules vs classifier; route macro_review/complaint_ticket/out_of_scope; policy_query vào nhánh chat; Redis sliding window và quota.
- Output: Router dataset/card; router service; rate limiter; /api/v1/absa/predict
- Module / công nghệ: MOD-01, MOD-02, MOD-07, MOD-12 — scikit-learn/embedding classifier; Redis; FastAPI
- Contract: IO-03, IO-10.
- Hoàn thành khi: Synthetic scores không đại diện production; urgent complaint không bỏ qua; unsupported language phản hồi rõ; policy hỏi chung không bị loại.
- Nguồn: SRC-05 L1; SRC-06 §2.2; SRC-07 ABSA

#### M4.7 — Tích hợp triage thật vào chatbot và workspace

- Lịch: 16/12/2026 (PM) → 17/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Full-stack / QA.
- Phụ thuộc: M4.6. Loại: Core. Trạng thái baseline: Not Started.
- Input: ABSA + router + Agent Workspace
- Cách làm: Gắn aspect/sentiment/entities/urgency/confidence lên ticket; agent sửa nhãn; fail inference vẫn có fallback; capture corrections có author/version; validate PII xuyên pipeline.
- Output: Ticket triage v1; correction endpoint; buyer/agent regression
- Module / công nghệ: MOD-01, MOD-07, MOD-11 — FastAPI; React; PostgreSQL; pytest
- Contract: IO-10, IO-13.
- Hoàn thành khi: BUY-AC-01 có model version; human correction không tự ghi đè prediction; không chặn chat vì batch job chậm.
- Nguồn: SRC-02 §3.1–3.2,7.10; SRC-04

#### M4.G — G4 — Review, nghiệm thu và báo cáo giai đoạn

- Lịch: 17/12/2026 (PM) → 17/12/2026; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò QA / quản lý dự án.
- Phụ thuộc: M4.7. Loại: Gate. Trạng thái baseline: Not Started.
- Input: Các đầu ra và test/eval của M4
- Cách làm: Chạy lại kịch bản nghiệm thu; đối chiếu yêu cầu; ghi PASS/FAIL/BLOCKED, số đo thực và kế hoạch sửa. Tự kiểm tra theo checklist; stakeholder xác nhận nếu có.
- Output: docs/reports/milestones/m4-review.md; checklist; demo; manifest phiên bản
- Module / công nghệ: MOD-12 — pytest; eval reports; Git
- Contract: Review/report theo IO-15.
- Hoàn thành khi: G4: batch coverage 100% accepted corpus với failures minh bạch; model eval thật; triage/corrections hoạt động; target chưa đạt phải ghi rõ.
- Nguồn: SRC-04; SRC-06 §3; SRC-07 ABSA

#### M4.B — Dự phòng sửa lỗi, tích hợp hoặc nghỉ theo lịch thực tế

- Lịch: 18/12/2026 (AM) → 18/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Dự phòng.
- Phụ thuộc: RESERVE — không phải quan hệ finish-to-start. Loại: Buffer. Trạng thái baseline: Contingency.
- Input: Blocker/failed gate hoặc ngày nghỉ đã xác nhận
- Cách làm: Ưu tiên sửa gate của giai đoạn; nếu chưa dùng thì giữ quỹ dự phòng. Không tự bổ sung tính năng.
- Output: Gate được kiểm tra lại; nhật ký sử dụng dự phòng và lịch cập nhật
- Module / công nghệ: MOD-12 — Issue log; regression tests
- Contract: Review/report theo IO-15.
- Hoàn thành khi: Không vượt ngày kết thúc giai đoạn; nếu vượt phải rebaseline, không đánh dấu Done khi gate fail.
- Nguồn: DEC-01; DEC-02


### M5 — Dashboard toàn corpus và điều tra bằng evidence | W9–W9 | 21/12/2026–25/12/2026

**Mục tiêu:** Nối thống kê toàn bộ dữ liệu với truy xuất các trường hợp đại diện.

**Điều kiện bắt đầu:** G4 PASS hoặc demo hạn chế được ghi rõ; model/index snapshot đồng nhất.

**Input:** Versioned ABSA predictions, review metadata, ticket outcomes, retrieval service.

**Output:** Analyst/PM dashboard, population/denominator, anomaly alert, drill-down giữ nguyên filters, benchmark review retrieval.

**Module / công nghệ:** MOD-04, MOD-09, MOD-10 — PostgreSQL aggregates; React charts; Qdrant; RRF/reranker; scheduled worker

**User stories:** US-ANALYST-01 quant→qual; US-PM-01 trend/outcome; graph enrichment ở M6

**Demo cuối giai đoạn:** Click spike pin theo firmware → xem 5–10 cases cùng cohort; không dùng Top-K làm tỷ lệ toàn corpus.

#### M5.1 — Metrics SQL, lineage và cảnh báo

- Lịch: 21/12/2026 (AM) → 21/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Backend / Analytics.
- Phụ thuộc: M4.G. Loại: Core. Trạng thái baseline: Not Started.
- Input: Predictions/version + outcomes/timestamps
- Cách làm: Tính aspect mention/negative ratio, WoW, product/version/channel cohorts; chọn model snapshot; denominator rõ; cảnh báo min-sample + baseline; ghi freshness và unknown outcomes.
- Output: Aggregate APIs; metric lineage; scheduled anomaly jobs
- Module / công nghệ: MOD-09 — PostgreSQL SQL/materialized views; worker jobs
- Contract: IO-11.
- Hoàn thành khi: Aggregate khớp kiểm đếm corpus; không double count model versions; zero denominator trả no-data; không ngụy tạo real-time.
- Nguồn: SRC-02 §7.4,13.5; SRC-04; SRC-14

#### M5.2 — Dashboard Analyst/PM và business outcomes

- Lịch: 22/12/2026 (AM) → 22/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Frontend.
- Phụ thuộc: M5.1. Loại: Core. Trạng thái baseline: Not Started.
- Input: Aggregate APIs và metric dictionary
- Cách làm: Chart distribution/trend theo SKU/firmware/time/channel; population, freshness, FRT/AHT/MTTR/FCR/CSAT/cost/reopen; trạng thái no-data; phân quyền PII.
- Output: apps/analyst_dashboard với bộ lọc và outcome view
- Module / công nghệ: MOD-10 — React; TypeScript; chart component; FastAPI
- Contract: IO-11.
- Hoàn thành khi: Có population và dữ liệu nguồn; các KPI chưa có baseline/mẫu đủ phải hiện chưa đủ dữ liệu.
- Nguồn: SRC-02 §3.3–3.4; SRC-14; SRC-03 US-PM-01

#### M5.3 — Drill-down có cohort, diversity và benchmark

- Lịch: 23/12/2026 (AM) → 23/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Backend / ML.
- Phụ thuộc: M5.2. Loại: Core. Trạng thái baseline: Not Started.
- Input: Dashboard context + feedback index
- Cách làm: Mở rộng InvestigationDrilldownRequest query/filters/date range; lấy 5–10 cases đa dạng, giữ product/aspect-polarity cặp đúng; thêm 40 golden review queries; benchmark 4 retrieval modes trên domain mới.
- Output: Investigation API/UI; evidence pack; review retrieval report; tổng 80 golden queries
- Module / công nghệ: MOD-04, MOD-10 — Qdrant payload/nested filters; RRF; BGE adapter; FastAPI
- Contract: IO-05, IO-12.
- Hoàn thành khi: Filters không rơi khi click; nguồn/timestamp hợp lệ; không nhầm battery-positive với delivery-negative trong cùng review.
- Nguồn: SRC-02 AN-AC-01..03; SRC-06 §4; SRC-07 Retrieval

#### M5.4 — Kiểm nghiệm dashboard và cảnh báo

- Lịch: 24/12/2026 (AM) → 24/12/2026; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò QA.
- Phụ thuộc: M5.3. Loại: Core. Trạng thái baseline: Not Started.
- Input: Synthetic spike cohort + real ingested snapshot
- Cách làm: So SQL với tính độc lập; replay timestamp/timezone; test empty cohort; đo alert precision trên labeled synthetic scenarios và ghi giới hạn.
- Output: Analytics/drill-down test report; anomaly evaluation
- Module / công nghệ: MOD-09, MOD-10 — pytest; SQL; browser tests
- Contract: IO-14.
- Hoàn thành khi: Coverage 100% eligible ingested records; source/model lineage; alert KPI là mục tiêu, không claim production từ synthetic.
- Nguồn: SRC-04; SRC-05 §4; SRC-07 NFR

#### M5.G — G5 — Review, nghiệm thu và báo cáo giai đoạn

- Lịch: 24/12/2026 (PM) → 24/12/2026; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò QA / quản lý dự án.
- Phụ thuộc: M5.4. Loại: Gate. Trạng thái baseline: Not Started.
- Input: Các đầu ra và test/eval của M5
- Cách làm: Chạy lại kịch bản nghiệm thu; đối chiếu yêu cầu; ghi PASS/FAIL/BLOCKED, số đo thực và kế hoạch sửa. Tự kiểm tra theo checklist; stakeholder xác nhận nếu có.
- Output: docs/reports/milestones/m5-review.md; checklist; demo; manifest phiên bản
- Module / công nghệ: MOD-12 — pytest; eval reports; Git
- Contract: Review/report theo IO-15.
- Hoàn thành khi: G5: dashboard từ corpus đầy đủ → filtered evidence có thể tái lập; số liệu không lấy từ mock; có freshness và denominator.
- Nguồn: SRC-02 AN-AC-01..03; SRC-03 US-PM-01

#### M5.B — Dự phòng sửa lỗi, tích hợp hoặc nghỉ theo lịch thực tế

- Lịch: 25/12/2026 (AM) → 25/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Dự phòng.
- Phụ thuộc: RESERVE — không phải quan hệ finish-to-start. Loại: Buffer. Trạng thái baseline: Contingency.
- Input: Blocker/failed gate hoặc ngày nghỉ đã xác nhận
- Cách làm: Ưu tiên sửa gate của giai đoạn; nếu chưa dùng thì giữ quỹ dự phòng. Không tự bổ sung tính năng.
- Output: Gate được kiểm tra lại; nhật ký sử dụng dự phòng và lịch cập nhật
- Module / công nghệ: MOD-12 — Issue log; regression tests
- Contract: Review/report theo IO-15.
- Hoàn thành khi: Không vượt ngày kết thúc giai đoạn; nếu vượt phải rebaseline, không đánh dấu Done khi gate fail.
- Nguồn: DEC-01; DEC-02


### M6 — GraphRAG và quản trị tri thức | W10–W11 | 28/12/2026–08/01/2027

**Mục tiêu:** Liên kết issue/version/cause/policy/resolution, đưa kết luận đã duyệt trở lại chatbot.

**Điều kiện bắt đầu:** G5 PASS; ontology canonical thống nhất giữa blueprint và schema rút gọn.

**Input:** Evidence cohorts, taxonomy, product versions, policy registry, confirmed synthetic known issues.

**Output:** Ontology v1 + Neo4j + graph traversal; analyst/steward UI; knowledge publish/rollback; chatbot có evidence graph.

**Module / công nghệ:** MOD-04, MOD-06, MOD-08, MOD-10, MOD-11 — Neo4j; Cypher; Python driver; PostgreSQL approval log; React

**User stories:** Hoàn thiện US-ANALYST-01, US-STEWARD-01; graph context cho US-BUY/AGENT/PM

**Demo cuối giai đoạn:** Spike → analyst hypothesis → steward approve → publish → ticket mới nhận draft dựa trên cause confirmed.

#### M6.1 — Thống nhất ontology, IDs và lifecycle

- Lịch: 28/12/2026 (AM) → 28/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Data / kiến trúc.
- Phụ thuộc: M5.G. Loại: Core. Trạng thái baseline: Not Started.
- Input: Blueprint §7.6 + ontology-schema + data spec
- Cách làm: ADR dùng Issue làm trung tâm; giữ ProductVersion/Firmware/Symptom/RootCause/Policy/Resolution/Evidence/Team/ServiceCenter; map schema rút gọn; tách trạng thái issue và cause; schema validation.
- Output: Ontology v1 + migration mapping + lifecycle transition rules
- Module / công nghệ: MOD-08 — Neo4j schema; Pydantic; Cypher
- Contract: IO-12.
- Hoàn thành khi: version_id duy nhất theo product+hw+fw; LLM không được confirm cause; tài liệu canonical và alias nhất quán.
- Nguồn: SRC-02 §7.6; SRC-08; SRC-06 §5; DEC-06

#### M6.2 — Seed và đồng bộ graph có provenance

- Lịch: 29/12/2026 (AM) → 29/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Data / Backend.
- Phụ thuộc: M6.1. Loại: Core. Trạng thái baseline: Not Started.
- Input: Canonical ontology, product/policy data, curated evidence
- Cách làm: Seed ~15 symptoms/10 causes/10 resolutions/5 centers; có hypothesis và confirmed; constraints, orphan/duplicate checks; sync idempotent từ registry/evidence; publish version manifest.
- Output: neo4j_ontology_seed.json; graph_sync; graph contracts
- Module / công nghệ: MOD-08 — Neo4j; Cypher; Python driver; PostgreSQL
- Contract: IO-12.
- Hoàn thành khi: Mọi cause confirmed có evidence/approver; sample firmware fixes được đánh dấu demo; replay không tạo duplicate.
- Nguồn: SRC-06 §5,8; SRC-08; WEB-03

#### M6.3 — Local GraphRAG và vector→entity→graph

- Lịch: 30/12/2026 (AM) → 30/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Backend.
- Phụ thuộc: M6.2. Loại: Core. Trạng thái baseline: Not Started.
- Input: Neo4j seed + retrieval EvidencePack
- Cách làm: Entity link theo bridge keys; traversal parameterized theo product/version; trả paths, status, evidence, approved resolution và policy; bound hops/limit/timeout.
- Output: Graph retriever + GraphContext contract + query tests
- Module / công nghệ: MOD-04, MOD-08 — Neo4j; Cypher; Qdrant; Python
- Contract: IO-05, IO-12.
- Hoàn thành khi: Hypothesis luôn gắn status; chỉ confirmed/approved dùng khẳng định; graph unavailable trả degraded và review.
- Nguồn: SRC-02 §7.7; SRC-08; SRC-06 §5–6

#### M6.4 — Nối graph vào resolution và chatbot

- Lịch: 31/12/2026 (AM) → 31/12/2026; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Backend / LLM.
- Phụ thuộc: M6.3. Loại: Core. Trạng thái baseline: Not Started.
- Input: GraphContext + PolicyDecision + FSM
- Cách làm: Fuse review/policy/graph evidence; draft cite từng nguồn; chọn hướng dẫn đúng product/version, service center; graph confidence không thay điều kiện policy; rerun safety suite.
- Output: Resolution v2 có graph citations và verified status
- Module / công nghệ: MOD-01, MOD-03, MOD-06, MOD-08 — Python FSM; Pydantic; Neo4j; LLM client
- Contract: IO-08, IO-12.
- Hoàn thành khi: Known issue có nguồn; thiếu confirmed cause không đoán; không hứa free replacement từ text mẫu.
- Nguồn: SRC-02 BUY-AC-03..04; SRC-06 §6

#### M6.5 — Analyst investigation và issue lifecycle UI

- Lịch: 04/01/2027 (AM) → 04/01/2027; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Frontend.
- Phụ thuộc: M6.4. Loại: Core. Trạng thái baseline: Not Started.
- Input: Graph context + dashboard filters
- Cách làm: Hiển thị paths/evidence, hypothesis vs confirmed; tạo new/duplicate issue, note và evidence; issue owner/state; PM xem resolution efficacy và recurrence.
- Output: Graph explorer tối giản; analyst annotation + PM issue detail
- Module / công nghệ: MOD-08, MOD-10 — React; TypeScript; FastAPI
- Contract: IO-12, IO-13.
- Hoàn thành khi: Annotation author/time/version đầy đủ; root-cause discovery là giả thuyết cho tới khi duyệt; policy source xem được.
- Nguồn: SRC-02 §3.3–3.4; SRC-14

#### M6.6 — Steward review, policy retirement và publish

- Lịch: 05/01/2027 (AM) → 05/01/2027; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Full-stack.
- Phụ thuộc: M6.5. Loại: Core. Trạng thái baseline: Not Started.
- Input: Proposed mutations + role matrix
- Cách làm: UI queue approve/reject/conflict; quyền analyst/steward riêng dù demo cùng người; retire policy; atomic publish/version; audit và rollback; sensitive updates chờ reviewer được chỉ định.
- Output: Steward workflow + knowledge versions + approval records
- Module / công nghệ: MOD-08, MOD-11, MOD-06 — FastAPI; PostgreSQL change log; Neo4j; React
- Contract: IO-13.
- Hoàn thành khi: Chưa approved không ảnh hưởng runtime; không silent overwrite; production reviewer độc lập cần người được ủy quyền.
- Nguồn: SRC-02 §3.5,7.10,14; SRC-05 US-STEWARD-01

#### M6.7 — Staleness, version propagation và rollback

- Lịch: 06/01/2027 (AM) → 06/01/2027; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Backend / Platform.
- Phụ thuộc: M6.6. Loại: Core. Trạng thái baseline: Not Started.
- Input: Published graph/policy revisions + index snapshots
- Cách làm: Invalidate cache/reindex khi policy thay; báo stale; graph/policy/index release manifest; rollback tri thức không rollback app; kiểm integrity và retention references.
- Output: Knowledge publication pipeline; version rollback drill
- Module / công nghệ: MOD-04, MOD-06, MOD-08, MOD-12 — PostgreSQL; Qdrant; Neo4j; Redis; manifests
- Contract: IO-15.
- Hoàn thành khi: Draft trace đúng policy/graph version; policy retired không được lấy qua cache cũ.
- Nguồn: SRC-02 §15,20; SRC-06 §5–7

#### M6.8 — Nghiệm thu vòng analyst→knowledge→chatbot

- Lịch: 07/01/2027 (AM) → 07/01/2027; 1 ngày; Trần Đình Khương đảm nhiệm vai trò QA.
- Phụ thuộc: M6.7. Loại: Core. Trạng thái baseline: Not Started.
- Input: 5 persona scripts; thêm 20 knowledge queries và 20 resolution cases
- Cách làm: Chạy chuỗi end-to-end firmware demo; kiểm schema/approval/paths/source; tổng golden ≥100 và resolution ≥50; báo riêng policy/review/graph retrieval slices.
- Output: Graph E2E recording; graph/resolution eval v2; source-linked reports
- Module / công nghệ: MOD-01, MOD-08, MOD-10, MOD-11 — pytest; browser tests; Cypher assertions
- Contract: IO-14.
- Hoàn thành khi: 5 role paths chạy với data demo; tổng ≥100 queries, ≥50 safety scenarios; unconfirmed case bắt buộc abstain/review.
- Nguồn: SRC-02 §19,21; SRC-06 §4,6; SRC-04

#### M6.9 — Đánh giá và ghi quyết định GraphRAG nâng cao

- Lịch: 08/01/2027 (AM) → 08/01/2027; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò Kiến trúc / ML.
- Phụ thuộc: M6.8. Loại: Core. Trạng thái baseline: Not Started.
- Input: Local GraphRAG report + cost/time budget
- Cách làm: So nhu cầu global graph summary/DRIFT với warehouse+clustering; ghi benchmark proposal và lý do defer; ghi microVM/automation/ASTE thành backlog có entry criteria.
- Output: Extension ADR; roadmap sau tuần 14; scope ledger
- Module / công nghệ: MOD-08, MOD-12 — ADR; evaluation design
- Contract: IO-15.
- Hoàn thành khi: Không đánh dấu global GraphRAG/DRIFT đã triển khai; mọi yêu cầu advanced có task/điều kiện riêng.
- Nguồn: SRC-02 §7.7,18 Phase5; SRC-07

#### M6.G — G6 — Review, nghiệm thu và báo cáo giai đoạn

- Lịch: 08/01/2027 (PM) → 08/01/2027; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò QA / quản lý dự án.
- Phụ thuộc: M6.9. Loại: Gate. Trạng thái baseline: Not Started.
- Input: Các đầu ra và test/eval của M6
- Cách làm: Chạy lại kịch bản nghiệm thu; đối chiếu yêu cầu; ghi PASS/FAIL/BLOCKED, số đo thực và kế hoạch sửa. Tự kiểm tra theo checklist; stakeholder xác nhận nếu có.
- Output: docs/reports/milestones/m6-review.md; checklist; demo; manifest phiên bản
- Module / công nghệ: MOD-12 — pytest; eval reports; Git
- Contract: Review/report theo IO-15.
- Hoàn thành khi: G6: quant→qual→proposed→review→publish→new ticket có bằng chứng; rollback tri thức và các trạng thái chưa xác nhận hoạt động.
- Nguồn: SRC-02 AN-AC-04..06; §3.5,19; SRC-04

#### M6.B — Nghỉ dự kiến 01/01/2027 (trích quỹ dự phòng)

- Lịch: 01/01/2027 (AM) → 01/01/2027; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Dự phòng.
- Phụ thuộc: RESERVE — không phải quan hệ finish-to-start. Loại: Calendar reserve. Trạng thái baseline: Contingency.
- Input: Blocker/failed gate hoặc ngày nghỉ đã xác nhận
- Cách làm: Dành ngày 01/01/2027 trong quỹ nghỉ/dự phòng. Core tasks M6 được xếp vòng qua ngày này. Nếu lịch nghỉ thay đổi, rebaseline lịch và capacity.
- Output: Gate được kiểm tra lại; nhật ký sử dụng dự phòng và lịch cập nhật
- Module / công nghệ: MOD-12 — Issue log; regression tests
- Contract: Review/report theo IO-15.
- Hoàn thành khi: Không xếp công việc core vào ngày nghỉ dự kiến.
- Nguồn: DEC-01; DEC-02


### M7 — Closed-loop feedback và cải thiện mô hình | W12–W12 | 11/01/2027–15/01/2027

**Mục tiêu:** Đưa chỉnh sửa đã duyệt vào dữ liệu đánh giá/huấn luyện và đo chất lượng qua phiên bản.

**Điều kiện bắt đầu:** G6 PASS; có correction fixtures và giới hạn training budget; test set vẫn locked.

**Input:** Agent edits, ABSA corrections, retrieval judgments, outcome events, stewardship logs.

**Output:** Versioned annotation datasets; active-learning queue; một retraining/eval cycle; drift monitors và publish decision.

**Module / công nghệ:** MOD-07, MOD-09, MOD-11, MOD-12 — PostgreSQL; Python export/retrain; existing model pipeline; OpenTelemetry/Prometheus

**User stories:** US-AGENT-01 feedback; AN-AC-06; US-STEWARD-01 governed learning; US-PM-01 effectiveness

**Demo cuối giai đoạn:** Sửa nhãn → review → export dataset v2 → train candidate → regression → giữ/publish có lý do.

#### M7.1 — Chuẩn hóa toàn bộ feedback và export

- Lịch: 11/01/2027 (AM) → 11/01/2027; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Backend / Data.
- Phụ thuộc: M6.G. Loại: Core. Trạng thái baseline: Not Started.
- Input: Corrections, edits, relevance, stale flags, outcomes
- Cách làm: Unified contribution API và statuses proposed/reviewed/approved/rejected/published; resolve disagreement; export chỉ approved; label/retrieval/knowledge queues riêng; dataset lineage.
- Output: Annotation store; approved training/eval exports; judgments dataset
- Module / công nghệ: MOD-11 — PostgreSQL; Pydantic; JSONL/Parquet
- Contract: IO-13.
- Hoàn thành khi: Hỗ trợ 8 feedback types trong blueprint; raw annotation không thành ground truth; test labels không nhập train.
- Nguồn: SRC-02 §7.10; SRC-06 §7

#### M7.2 — Một vòng active learning và model promotion

- Lịch: 12/01/2027 (AM) → 12/01/2027; 1 ngày; Trần Đình Khương đảm nhiệm vai trò ML.
- Phụ thuộc: M7.1. Loại: Core. Trạng thái baseline: Not Started.
- Input: Approved corrections + baseline training/eval pipelines
- Cách làm: Chọn uncertainty/disagreement, giữ quota diversity; retrain một candidate bounded; so cùng held-out locked; publish hoặc reject; lưu artifacts và rollback pointer.
- Output: Active-learning report; candidate model; promotion/rollback manifest
- Module / công nghệ: MOD-07, MOD-11 — PyTorch/scikit-learn pipelines; versioned artifacts
- Contract: IO-10, IO-14, IO-15.
- Hoàn thành khi: Không bắt buộc candidate phải tốt hơn; chỉ promote nếu gate pass; không tự publish từ feedback chưa duyệt.
- Nguồn: SRC-02 §7.10,13,15; SRC-06 §7; SRC-15

#### M7.3 — Drift, quality và feedback monitoring

- Lịch: 13/01/2027 (AM) → 13/01/2027; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò ML / Platform.
- Phụ thuộc: M7.2. Loại: Core. Trạng thái baseline: Not Started.
- Input: Inference distributions + outcome events
- Cách làm: Monitor label/aspect/confidence/input-length/language drift và queue depth; draft acceptance/edit reasons; alert theo baseline và sample size; nối version dimensions.
- Output: Quality/drift dashboard và alert config
- Module / công nghệ: MOD-07, MOD-09, MOD-12 — Prometheus/OpenTelemetry; SQL; scheduled jobs
- Contract: IO-15.
- Hoàn thành khi: Drift chỉ là tín hiệu kiểm tra; không tự đổi model/policy; thresholds và observed window được ghi.
- Nguồn: SRC-05 L7; SRC-07 monitoring; SRC-02 §15

#### M7.4 — Retention, correction và deletion propagation

- Lịch: 13/01/2027 (PM) → 13/01/2027; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò Backend / governance.
- Phụ thuộc: M7.3. Loại: Core. Trạng thái baseline: Not Started.
- Input: Data inventory + retention decisions + synthetic subject request
- Cách làm: Xóa/sửa subject record qua SQL, index, graph evidence links, caches và exports; tombstone/audit phù hợp; đánh dấu model artifacts cần đánh giá khi chứa training record đã xóa.
- Output: Deletion/correction workflow + lineage test
- Module / công nghệ: MOD-02, MOD-08, MOD-11, MOD-12 — PostgreSQL; Qdrant; Neo4j; artifact manifests
- Contract: IO-13, IO-15.
- Hoàn thành khi: Không còn retrievable record bị xóa; raw PII không được phục hồi qua rollback; model unlearning không được tuyên bố đã làm.
- Nguồn: SRC-02 §14,21; SRC-07 governance

#### M7.5 — Regression learning loop và outcome efficacy

- Lịch: 14/01/2027 (AM) → 14/01/2027; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò QA.
- Phụ thuộc: M7.4. Loại: Core. Trạng thái baseline: Not Started.
- Input: Feedback cycle, dataset/model/graph manifests
- Cách làm: Chạy export/retrain/publish/reject/rollback tests; liên kết resolution_success/reopen/recurrence; kiểm final response và author trace.
- Output: Closed-loop E2E report; outcome linkage checks
- Module / công nghệ: MOD-07, MOD-09, MOD-11 — pytest; SQL; manifest diff
- Contract: IO-14.
- Hoàn thành khi: Mỗi thay đổi có source/author/reviewer/version; không học trực tiếp từ người dùng; kết quả kém không promote.
- Nguồn: SRC-02 §21; SRC-03; SRC-06 §7

#### M7.G — G7 — Review, nghiệm thu và báo cáo giai đoạn

- Lịch: 14/01/2027 (PM) → 14/01/2027; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò QA / quản lý dự án.
- Phụ thuộc: M7.5. Loại: Gate. Trạng thái baseline: Not Started.
- Input: Các đầu ra và test/eval của M7
- Cách làm: Chạy lại kịch bản nghiệm thu; đối chiếu yêu cầu; ghi PASS/FAIL/BLOCKED, số đo thực và kế hoạch sửa. Tự kiểm tra theo checklist; stakeholder xác nhận nếu có.
- Output: docs/reports/milestones/m7-review.md; checklist; demo; manifest phiên bản
- Module / công nghệ: MOD-12 — pytest; eval reports; Git
- Contract: Review/report theo IO-15.
- Hoàn thành khi: G7: sửa nhãn/tri thức→duyệt→dataset/model/knowledge version→đánh giá→publish hoặc reject được chạy và truy vết.
- Nguồn: SRC-02 §7.10,21; SRC-04

#### M7.B — Dự phòng sửa lỗi, tích hợp hoặc nghỉ theo lịch thực tế

- Lịch: 15/01/2027 (AM) → 15/01/2027; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Dự phòng.
- Phụ thuộc: RESERVE — không phải quan hệ finish-to-start. Loại: Buffer. Trạng thái baseline: Contingency.
- Input: Blocker/failed gate hoặc ngày nghỉ đã xác nhận
- Cách làm: Ưu tiên sửa gate của giai đoạn; nếu chưa dùng thì giữ quỹ dự phòng. Không tự bổ sung tính năng.
- Output: Gate được kiểm tra lại; nhật ký sử dụng dự phòng và lịch cập nhật
- Module / công nghệ: MOD-12 — Issue log; regression tests
- Contract: Review/report theo IO-15.
- Hoàn thành khi: Không vượt ngày kết thúc giai đoạn; nếu vượt phải rebaseline, không đánh dấu Done khi gate fail.
- Nguồn: DEC-01; DEC-02


### M8 — Tích hợp, vận hành và bàn giao | W13–W14 | 18/01/2027–29/01/2027

**Mục tiêu:** Chứng minh phạm vi demo 5 user stories; chuẩn bị release tái lập và ghi trung thực khoảng cách production.

**Điều kiện bắt đầu:** G7 PASS; live cloud cần account/budget/approval và reviewer; thiếu thì cloud gate BLOCKED, local demo vẫn báo riêng.

**Input:** G0–G7 evidence; candidate app/model/index/graph/policy; frozen eval; resource access.

**Output:** Release bundle, 5 UAT demos, eval suite, deploy/IaC package, runbooks, rollback evidence và coverage ledger.

**Module / công nghệ:** MOD-01..MOD-12 — Docker; GitHub Actions; Helm/Terraform/EKS target; OTel/Prometheus; pytest; load harness

**User stories:** Tất cả stories ở phạm vi demo; production/business KPI là gate riêng không tự nhận đã đạt

**Demo cuối giai đoạn:** Tái dựng từ manifest; chạy 5 persona; ngắt dependency; rollback app/model/knowledge; xem báo cáo thật.

#### M8.1 — CI, AI gates và artifact release bất biến

- Lịch: 18/01/2027 (AM) → 18/01/2027; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Platform.
- Phụ thuộc: M7.G. Loại: Core. Trạng thái baseline: Not Started.
- Input: Existing CI workflows + all eval reports
- Cách làm: Chạy unit/contract/integration/eval/E2E; build once by digest; attach data/model/index/graph/policy/prompt versions; promote same artifact; model/app rollback tách; giữ test evidence.
- Output: Release workflow + run-manifest + reproducibility scripts
- Module / công nghệ: MOD-12 — GitHub Actions; Poetry lock; Docker; pytest; artifacts/S3
- Contract: IO-15.
- Hoàn thành khi: CI pass gồm AI/policy gates, không chỉ Pod Ready; không commit model/index binaries.
- Nguồn: SRC-02 §15–16,21; SRC-15; SRC-16

#### M8.2 — Hạ tầng và phân quyền deployment mục tiêu

- Lịch: 19/01/2027 (AM) → 19/01/2027; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Platform.
- Phụ thuộc: M8.1. Loại: Core. Trạng thái baseline: Not Started.
- Input: Compose release + infrastructure ADR + cloud prerequisites
- Cách làm: Helm/Terraform cấu hình bounded demo; OIDC builder/staging/prod roles; per-service identity; Secrets, NetworkPolicy, non-root/read-only; CPU/GPU worker separation; validate/render plan.
- Output: IaC/chart package; IAM matrix; rendered manifests; cloud cost/prerequisite record
- Module / công nghệ: MOD-12 — Helm; Terraform; EKS/ECR/S3/Secrets target; Kubernetes
- Contract: IO-15.
- Hoàn thành khi: Không hứa production full trong 1 ngày: scope là minimal validated package; thiếu account hoặc resource thì live apply là BLOCKED.
- Nguồn: SRC-02 §14.3,16; SRC-05 §7; DEC-11

#### M8.3 — Deploy demo và health/observability thật

- Lịch: 20/01/2027 (AM) → 20/01/2027; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Platform.
- Phụ thuộc: M8.2. Loại: Core. Trạng thái baseline: Not Started.
- Input: Release artifacts + available local/staging resources
- Cách làm: Chạy Compose demo bắt buộc; nếu prereqs đủ, triển khai bounded EKS staging; trace→logs→metrics; dependency readiness, secrets, alerts và cost; ghi endpoint/env và kết quả.
- Output: Runnable environment; deploy smoke evidence; production-target status
- Module / công nghệ: MOD-12 — Docker Compose; optional live EKS; OTel; Prometheus/Grafana
- Contract: IO-15.
- Hoàn thành khi: Local pass không thay live-cloud evidence; prod promotion chưa có approval phải để pending; không ghi enterprise-ready.
- Nguồn: SRC-02 §15–16; SRC-07 NFR; SRC-05 L7

#### M8.4 — Load, failure, latency và sizing

- Lịch: 21/01/2027 (AM) → 21/01/2027; 1 ngày; Trần Đình Khương đảm nhiệm vai trò QA / Platform.
- Phụ thuộc: M8.3. Loại: Core. Trạng thái baseline: Not Started.
- Input: Frozen corpus, fixed hardware and release
- Cách làm: Cold/warm p50/p95/p99 và concurrency; 1x/3x/10x synthetic load nếu tài nguyên cho phép; stage time, RAM/disk/GPU; inject timeout/Qdrant/Neo4j/queue errors; backlog/resume.
- Output: Load/failure report + measured resource envelope + tuned config
- Module / công nghệ: MOD-04, MOD-07, MOD-12 — Python load harness; metrics; Docker stats
- Contract: IO-14, IO-15.
- Hoàn thành khi: Các SLO 250ms/300ms/<2s là targets chưa chứng minh; phần không chạy ghi NOT RUN; output partial không silent.
- Nguồn: SRC-07 NFR; SRC-05 §5.2; SRC-06 sizing

#### M8.5 — Privacy/access, backup và rollback drill

- Lịch: 22/01/2027 (AM) → 22/01/2027; 1 ngày; Trần Đình Khương đảm nhiệm vai trò QA / Platform.
- Phụ thuộc: M8.4. Loại: Core. Trạng thái baseline: Not Started.
- Input: Release + role matrix + snapshots
- Cách làm: Test cross-customer/role, PII, deletion, prompt injection, stale policy; backup/restore PostgreSQL/Qdrant/Neo4j; rollback app/model/index/knowledge riêng; document incident response.
- Output: Security regression; restore/rollback timings; runbooks
- Module / công nghệ: MOD-12 — pytest; backup tools; manifests; Docker/Kubernetes
- Contract: IO-14, IO-15.
- Hoàn thành khi: Zero leak/unauthorized action trên suite; source/lineage sau restore nhất quán; không tự tuyên bố tuân thủ pháp lý.
- Nguồn: SRC-02 §14–16,21; SRC-07 governance

#### M8.6 — UAT 5 vai trò và full regression

- Lịch: 25/01/2027 (AM) → 25/01/2027; 1 ngày; Trần Đình Khương đảm nhiệm vai trò QA / Product.
- Phụ thuộc: M8.5. Loại: Core. Trạng thái baseline: Not Started.
- Input: 5 persona scripts + ≥100 queries + ≥50 resolution cases
- Cách làm: Chạy buyer, agent, analyst, PM, steward; end-to-end story firmware; rerun frozen AI suites; ghi bug/residual limitation; đối chiếu từng acceptance ID và nguồn.
- Output: UAT matrix; recordings; final evaluation tables; coverage status
- Module / công nghệ: MOD-01..MOD-12 — Browser tests; pytest; human rubric; Excel traceability
- Contract: IO-14.
- Hoàn thành khi: Mỗi story có API/UI/data/eval/audit/failure path; gate fail không đổi thành Done vì deadline.
- Nguồn: SRC-02 §19,21; SRC-03; SRC-04

#### M8.7 — Business KPI đối chiếu baseline

- Lịch: 26/01/2027 (AM) → 26/01/2027; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò Analytics / QA.
- Phụ thuộc: M8.6. Loại: Core. Trạng thái baseline: Not Started.
- Input: Manual/assisted timing, events and outcome samples
- Cách làm: Tính FRT/AHT/FCR/MTTR/CSAT/draft acceptance/reopen/cost; phân biệt synthetic replay và pilot thật; nêu sample size/time window; 40%/15% là mục tiêu chưa đảm bảo.
- Output: Business KPI report; measurement limitations; post-demo pilot plan
- Module / công nghệ: MOD-09, MOD-12 — SQL; Python; metric dictionary
- Contract: IO-11, IO-15.
- Hoàn thành khi: Không có real users thì business impact NOT VALIDATED; metric denominator rõ và không trộn % tương đối với điểm phần trăm.
- Nguồn: SRC-03; SRC-04; SRC-05 §9; DEC-04

#### M8.8 — Tài liệu bàn giao và bộ demo tái lập

- Lịch: 26/01/2027 (PM) → 27/01/2027; 1 ngày; Trần Đình Khương đảm nhiệm vai trò Documentation / QA.
- Phụ thuộc: M8.7. Loại: Core. Trạng thái baseline: Not Started.
- Input: Release manifest; all source/test/eval reports
- Cách làm: Quickstart, data/model cards, API docs, runbooks, demo scripts, scope ledger; presentation Problem→Users→Evidence→Resolution→Learn; ghi rõ conditional/deferred và cách tiếp tục.
- Output: Final report; release archive; handover checklist; demo guide
- Module / công nghệ: MOD-12 — Markdown; OpenAPI; Git; artifact manifest
- Contract: IO-15.
- Hoàn thành khi: Máy sạch có thể dựng bounded demo theo hướng dẫn; không dùng đường dẫn máy cá nhân trong docs mới; mọi claim có evidence.
- Nguồn: SRC-02 §21–22; SRC-15; SRC-16

#### M8.G — G8 — Review, nghiệm thu và báo cáo giai đoạn

- Lịch: 27/01/2027 (PM) → 27/01/2027; 0.5 ngày; Trần Đình Khương đảm nhiệm vai trò QA / quản lý dự án.
- Phụ thuộc: M8.8. Loại: Gate. Trạng thái baseline: Not Started.
- Input: Các đầu ra và test/eval của M8
- Cách làm: Chạy lại kịch bản nghiệm thu; đối chiếu yêu cầu; ghi PASS/FAIL/BLOCKED, số đo thực và kế hoạch sửa. Tự kiểm tra theo checklist; stakeholder xác nhận nếu có.
- Output: docs/reports/milestones/m8-review.md; checklist; demo; manifest phiên bản
- Module / công nghệ: MOD-12 — pytest; eval reports; Git
- Contract: Review/report theo IO-15.
- Hoàn thành khi: G8: demo 5 stories + quality/data/governance/release evidence; đánh giá riêng core demo, target quality, cloud và business validation; còn thiếu ghi OPEN.
- Nguồn: SRC-02 §21; SRC-03; SRC-04; SRC-07

#### M8.B — Dự phòng sửa lỗi, tích hợp hoặc nghỉ theo lịch thực tế

- Lịch: 28/01/2027 (AM) → 29/01/2027; 2 ngày; Trần Đình Khương đảm nhiệm vai trò Dự phòng.
- Phụ thuộc: RESERVE — không phải quan hệ finish-to-start. Loại: Buffer. Trạng thái baseline: Contingency.
- Input: Blocker/failed gate hoặc ngày nghỉ đã xác nhận
- Cách làm: Ưu tiên sửa gate của giai đoạn; nếu chưa dùng thì giữ quỹ dự phòng. Không tự bổ sung tính năng.
- Output: Gate được kiểm tra lại; nhật ký sử dụng dự phòng và lịch cập nhật
- Module / công nghệ: MOD-12 — Issue log; regression tests
- Contract: Review/report theo IO-15.
- Hoàn thành khi: Không vượt ngày kết thúc giai đoạn; nếu vượt phải rebaseline, không đánh dấu Done khi gate fail.
- Nguồn: DEC-01; DEC-02

## 4. Danh mục module

### MOD-01 — Chatbot & conversation

- Giai đoạn: M0–M3; enrich M4/M6; user story: US-BUY-01.
- Input: Message + authenticated session + permitted history
- Output: Answer/citations/clarification/handoff; persisted messages
- Nhiệm vụ: Session ownership; sliding buffer/summary; intent/follow-up; orchestration; buyer UI
- Vị trí: `apps/api; packages/conversation (mới); apps/chatbot (mới)`
- Công nghệ: FastAPI; PostgreSQL; Redis; React/TypeScript
- Contract/API: IO-01, IO-02; POST /api/v1/chat/messages (mới); phụ thuộc: MOD-02/03/04; optional 05/06/07/08.
- Ranh giới: Không bắt ChatRequest phải có product/order. Order tool chỉ chạy sau xác thực. Backend modular monolith, worker riêng khi cần.

### MOD-02 — Data ingestion & knowledge preparation

- Giai đoạn: M1; M4; M7; user story: ALL.
- Input: Crawler exports, docs, reviews/tickets/chats
- Output: Validated/masked records; chunks; manifests; rejected records
- Nhiệm vụ: Parse/clean/dedup/chunk; immutable ingest log; PII boundary; source/rights; queue/retry/DLQ
- Vị trí: `pipelines/ingest_feedback; pii_masking; policy_ingestion; apps/worker; adapter đọc Data_crawling`
- Công nghệ: Python; Pydantic; JSONL/Parquet; PostgreSQL; Redis Streams
- Contract/API: IO-03, IO-04; POST /api/v1/ingest/feedback; phụ thuộc: MOD-12.
- Ranh giới: Giữ Data_crawling độc lập; ứng dụng đọc export, không import crawler runtime hoặc sửa scope crawler.

### MOD-03 — LLM generation & guardrails

- Giai đoạn: M2; M3; M6; user story: US-BUY-01; US-AGENT-01.
- Input: EvidencePack + allowed actions + bounded context
- Output: Validated answer/draft + citations + review reason
- Nhiệm vụ: Provider client, prompts, retries, schema, claim/citation checks, no-evidence abstention, PII output
- Vị trí: `packages/llm/{clients,prompts,structured_outputs,guardrails}`
- Công nghệ: Configurable LLM; HTTP client; Pydantic; Python validators
- Contract/API: IO-02, IO-05, IO-08; phụ thuộc: MOD-04; MOD-06 for personalized resolution.
- Ranh giới: LLM diễn đạt từ evidence; quyết định eligibility và quyền action thuộc MOD-06. Provider/model pin tại G0.

### MOD-04 — Retrieval & evidence

- Giai đoạn: M2; mở rộng M5/M6; user story: ALL.
- Input: Query + namespace + authorized filters + index version
- Output: Ranked hits/evidence + source IDs + timestamps + latency
- Nhiệm vụ: Dense/BM25, RRF, optional BGE rerank, diversity, citation resolver, policy/case/known-issue modes
- Vị trí: `packages/retrieval; pipelines/build_dense_sparse_index; pipelines/eval_retrieval`
- Công nghệ: Qdrant; sentence-transformers; rank-bm25; RRF; BGE candidate
- Contract/API: IO-05; POST /api/v1/retrieval/search (mới); phụ thuộc: MOD-02; optional MOD-07/08 enrichment.
- Ranh giới: Không dùng Top-K làm thống kê; score retrieval không phải xác suất; aspect-polarity filter phải bảo toàn cặp.

### MOD-05 — Customer & order context

- Giai đoạn: M3; user story: US-BUY-01; US-AGENT-01.
- Input: Verified customer_ref/order_ref
- Output: Order/product/warranty metadata, ownership/availability status
- Nhiệm vụ: CRM adapter, authorization, pseudonymized mapping, missing-field response, region lookup
- Vị trí: `packages/customer_context; apps/api services`
- Công nghệ: PostgreSQL demo; CRM adapter; RBAC; typed/MCP tools
- Contract/API: IO-06; query_customer_order; phụ thuộc: MOD-12.
- Ranh giới: CRM/commerce là source of truth khi live. Seed demo có synthetic flag; không tự truy đơn của người khác.

### MOD-06 — Policy registry & resolution engine

- Giai đoạn: M1 catalog; M3 rules; M6 graph; user story: US-BUY-01; US-AGENT-01; US-STEWARD-01.
- Input: Approved policy + order context + evidence + graph context
- Output: PolicyDecision; action candidates; ticket routing; resolution outcome
- Nhiệm vụ: Version/effective-date filtering; deterministic conditions; missing fields; FSM/reflection; approval; action idempotency
- Vị trí: `packages/policy; packages/resolution; pipelines/eval_resolution`
- Công nghệ: PostgreSQL; Python rules/FSM; Pydantic; MCP adapters
- Contract/API: IO-07/08/09; POST /api/v1/resolution/draft; phụ thuộc: MOD-03/04/05; optional MOD-08.
- Ranh giới: Q&A nói điều kiện khác với quyết định case cụ thể. Tiền/ngoại lệ phải review; policy unknown/stale không dùng để kết luận.

### MOD-07 — ABSA & entity/triage

- Giai đoạn: M4; M7; user story: US-AGENT-01; US-ANALYST-01; US-PM-01.
- Input: Masked feedback + taxonomy + versioned model
- Output: Aspect-polarity pairs, confidence, supported spans/entities, model lineage
- Nhiệm vụ: Baseline/candidate training; ATE/APC/category; calibration; batch all corpus; low-confidence queue; domain slices
- Vị trí: `packages/absa; pipelines/{absa_batch,eval_absa,retrain_absa}`
- Công nghệ: scikit-learn; PyTorch/Transformers; PhoBERT candidate; Parquet
- Contract/API: IO-10; POST /api/v1/absa/predict (mới); phụ thuộc: MOD-02; MOD-12.
- Ranh giới: 100% accepted corpus được accounting; không overwrite model predictions. ATE cần labels riêng; ASTE/ACOS là extension.

### MOD-08 — Knowledge Graph & GraphRAG

- Giai đoạn: M6; M7; user story: US-ANALYST-01; US-STEWARD-01; US-BUY-01; US-PM-01.
- Input: Versioned entities/evidence, proposed/approved mutations
- Output: Paths, known issue context, lifecycle, published graph versions
- Nhiệm vụ: Canonical Issue-centered ontology, seed/sync, local traversal, vector bridge, constraints, approval, stale detection, rollback
- Vị trí: `packages/graph/{ontology,retrievers,mutations}; pipelines/graph_sync`
- Công nghệ: Neo4j; Cypher; Python driver; PostgreSQL approval journal
- Contract/API: IO-12/13; controlled graph query/mutation APIs (mới); phụ thuộc: MOD-02/04/06/11.
- Ranh giới: Hypothesis không thành confirmed từ LLM. Graph cycle chỉ bị chặn theo invariant của quan hệ, không cấm mọi chu trình.

### MOD-09 — Analytics, metrics & alerts

- Giai đoạn: M3 events; M5 dashboard; M7/M8 eval; user story: US-ANALYST-01; US-PM-01.
- Input: Versioned predictions + population + ticket/outcome timestamps
- Output: Metrics, trend/cohort context, alerts, efficacy/cost reports
- Nhiệm vụ: Full-corpus aggregates, denominators, version selection, min sample, data freshness, business metrics
- Vị trí: `packages/analytics; apps/worker/jobs`
- Công nghệ: PostgreSQL aggregates; Python scheduled jobs; Prometheus
- Contract/API: IO-11; analytics endpoints (mới); phụ thuộc: MOD-02/07; MOD-06 outcomes.
- Ranh giới: Báo 100% dữ liệu hợp lệ đã ingest, không tự nhận 100% khách hàng doanh nghiệp. KPI business cần baseline/pilot thật.

### MOD-10 — Analyst/PM dashboard & investigation

- Giai đoạn: M5; M6; user story: US-ANALYST-01; US-PM-01.
- Input: Metrics/cohort filters + evidence + graph context
- Output: Charts, issue detail, evidence drill-down, analyst annotations
- Nhiệm vụ: Filter state preservation; population/freshness; graph path viewer; issue ownership/lifecycle; role-safe drill-down
- Vị trí: `apps/analyst_dashboard; apps/api investigation routes`
- Công nghệ: React; TypeScript; chart component; FastAPI
- Contract/API: IO-11/12/13; POST /api/v1/investigation/drilldown (mở rộng); phụ thuộc: MOD-04/08/09/11.
- Ranh giới: Nêu rõ candidate cause vs confirmed; metric lineage đủ để tái tính; user không cần biết vector score nội bộ.

### MOD-11 — Agent Workspace, feedback & stewardship

- Giai đoạn: M3; M4; M6–M7; user story: US-AGENT-01; US-ANALYST-01; US-STEWARD-01.
- Input: Drafts/tickets, correction/relevance/outcome, proposed knowledge changes
- Output: Final reviewed responses; approved labels; dataset/knowledge change versions
- Nhiệm vụ: Approve/edit/reject/reasons/escalation; annotations; stewardship queue; active learning export; status workflow
- Vị trí: `apps/agent_workspace; packages/feedback/{annotations,knowledge_approval,active_learning}`
- Công nghệ: React; FastAPI; PostgreSQL; Python export/training jobs
- Contract/API: IO-09/13; POST /api/v1/feedback/contribute; phụ thuộc: MOD-06/07/08/12.
- Ranh giới: Một người dev có thể mô phỏng 5 vai trò, không có nghĩa đã có independent UAT/production approver.

### MOD-12 — Contracts, security, evaluation & operations

- Giai đoạn: M0–M8; user story: ALL.
- Input: All configs, events, dataset/model/index/graph/policy versions
- Output: Typed contracts, audit, traces, eval/release reports, deployment/runbooks
- Nhiệm vụ: Auth/RBAC, privacy/deletion, secrets/rate limit, CI gates, versioning, backup/rollback, load/drift/cost
- Vị trí: `packages/common; packages/data_contracts; tests; configs; infra; .github; artifacts`
- Công nghệ: Pydantic; pytest; Poetry; Docker; GitHub Actions; OTel; Prometheus; Helm/Terraform/EKS target
- Contract/API: IO-14/15; health probes; manifests; phụ thuộc: Shared foundation; triển khai tăng dần.
- Ranh giới: Demo on Compose bắt buộc. Live cloud và production có entry criteria riêng; không thay test thật bằng readiness mock.

## 5. Input/output contracts

Các JSON sau chỉ minh họa, không thay Pydantic schema đầy đủ. ID dạng DEMO/synthetic không đại diện policy/đơn hàng/firmware thật.

### IO-01 — ChatMessageRequest

- Giai đoạn: M0→M2; producer: Buyer UI → consumer: MOD-01.
- Input: message:string; conversation_id?:UUID; client_request_id:UUID; channel; product_ref?/order_ref?
- Output: Authorized request context + normalized message + optional verified refs
- Validation/failure: Identity/role lấy từ auth, không tin client; max length; idempotency; policy Q&A cho phép thiếu product.
- Persistence: PostgreSQL conversations/interactions; masked content; restricted identity mapping
- API: POST /api/v1/chat/messages — mới, không tái dùng FeedbackRecord có product_id bắt buộc
- Nguồn: SRC-02 §5.4,7.9; SRC-16; đề xuất cho chatbot

```json
{
  "conversation_id": "conv-demo-01",
  "client_request_id": "req-demo-01",
  "message": "Chính sách đổi trả thế nào?"
}
```

### IO-02 — ChatMessageResponse

- Giai đoạn: M2; producer: MOD-01/03 → consumer: Buyer UI.
- Input: Authorized message + EvidencePack + bounded history
- Output: conversation_id; message_id; answer; citations[]; status: answered|needs_clarification|needs_human_review|error; missing_fields[]; ticket_id?; trace_id
- Validation/failure: Citations resolve thật; no-evidence không kết luận; timeout/error rõ; stream nếu dùng chỉ phát nội dung được kiểm theo policy.
- Persistence: interactions, llm_generations, citations
- API: Response /api/v1/chat/messages; GET conversation/history — mới
- Nguồn: SRC-02 §7.9; SRC-04; đề xuất chatbot

```json
{
  "status": "needs_clarification",
  "answer": "Bạn đang hỏi sản phẩm thuộc nhóm nào?",
  "citations": [],
  "missing_fields": [
    "product_category"
  ],
  "trace_id": "trace-demo"
}
```

### IO-03 — FeedbackRecord → IngestReceipt

- Giai đoạn: M1/M4; producer: Source adapter/chat event → consumer: MOD-02→MOD-07.
- Input: source/source_record_id/text/language/created_at/product_id; product_version?/customer_ref?/order_ref?/rating?
- Output: accepted/rejected/batch_id; durable record IDs; masked text; validation errors; processing status
- Validation/failure: Dedup source+source_record_id; UTC timestamps; product missing phải quarantine/enrich, không invent; accepted chỉ sau persist/queue.
- Persistence: Immutable ingest manifest + reviews/support_tickets + queue/DLQ
- API: POST /api/v1/ingest/feedback — schema có, handler hiện mock cần triển khai
- Nguồn: SRC-06 §2; SRC-02 §7.1,9; SRC-16

```json
{
  "source": "ticket",
  "source_record_id": "tk-demo-1",
  "product_id": "demo-phone-x",
  "text": "Pin yếu sau cập nhật",
  "language": "vi",
  "created_at": "2026-10-26T03:00:00Z"
}
```

### IO-04 — PolicyDocument / PolicyChunk

- Giai đoạn: M1→M2; producer: MOD-02; steward review → consumer: MOD-04/06.
- Input: Raw source + URL/title/hash/crawled_at + verified applicability
- Output: doc_id/chunk_id; policy_id/version/clause_id; clean text; source_url; offsets/heading; effective_from/to; scope; approval status; source_hash
- Validation/failure: Không suy effective date từ crawl date; missing dates/status cần duyệt; chunk giữ ngoại lệ; only approved applicable policy searchable.
- Persistence: Raw export; PostgreSQL registry; Qdrant policies derived index
- API: Policy ingestion pipeline; admin catalog/publish API — mới
- Nguồn: SRC-06 §4–5; SRC-02 §7.8

```json
{
  "chunk_id": "demo-policy-v1-4.2",
  "policy_id": "DEMO-WARRANTY",
  "version": "1",
  "clause_id": "4.2",
  "status": "approved",
  "synthetic": true
}
```

### IO-05 — RetrievalRequest → EvidencePack

- Giai đoạn: M2→M5/M6; producer: MOD-01/10 → consumer: MOD-04→MOD-03/08.
- Input: query; mode: policy|case|investigation|known_issue; authorized filters; top_k; as_of; index_version?
- Output: hits[{source_type,source_id,chunk_id,score,snippet,url,timestamp,policy_version?,metadata}]; index_version; empty_reason?; stage_latency_ms
- Validation/failure: Policy+review namespaces riêng; filters trước retrieval/rerank; paired aspect/sentiment; valid source IDs; distinguish score type.
- Persistence: retrieval_sessions/results; Qdrant; source records
- API: POST /api/v1/retrieval/search — mới; internal service trong chat
- Nguồn: SRC-02 §7.5; SRC-06 §4; SRC-07 Retrieval

```json
{
  "query": "đổi trả điện thoại",
  "mode": "policy",
  "filters": {
    "approval_status": "approved"
  },
  "top_k": 5,
  "as_of": "2026-10-26"
}
```

### IO-06 — AuthorizedOrderContext

- Giai đoạn: M3; producer: Auth + CRM/seed adapter → consumer: MOD-05→MOD-06.
- Input: authenticated subject; verified order_ref; requested fields
- Output: ownership_status; product/version; purchase_date; warranty_expires_at; region; order_status; source; missing_fields
- Validation/failure: Verify ownership trước read; unknown khác not eligible; only minimized context vào LLM; seed source=demo.
- Persistence: CRM source-of-truth; restricted SQL mapping/cache
- API: query_customer_order; customer context endpoint — mới
- Nguồn: SRC-02 §3.1,7.2,8.2; SRC-06 §5.3

```json
{
  "order_ref": "DEMO-ORDER-01",
  "ownership_status": "verified",
  "source": "synthetic_seed",
  "product_id": "demo-phone-x",
  "missing_fields": []
}
```

### IO-07 — PolicyDecision

- Giai đoạn: M3; producer: MOD-05 + approved registry → consumer: MOD-06→MOD-03/11.
- Input: order context; product/version; issue attributes; evaluation time
- Output: eligibility: eligible|ineligible|unknown; allowed_actions; prohibited_actions; missing_fields; policy_id/version/clause_id; review_required; reasons
- Validation/failure: Deterministic rule evaluator; no stale policy; dates timezone consistent; financial exception review; conditions not evaluated by LLM.
- Persistence: Policy registry + policy_decisions audit
- API: check_warranty_eligibility tool/internal API — mới
- Nguồn: SRC-02 §7.8; SRC-06 §5.2

```json
{
  "eligibility": "unknown",
  "allowed_actions": [],
  "missing_fields": [
    "purchase_date"
  ],
  "review_required": true,
  "reasons": [
    "missing_order_context"
  ]
}
```

### IO-08 — ResolutionDraftRequest/Response

- Giai đoạn: M3→M6; producer: MOD-01/11 → consumer: MOD-06 + MOD-03.
- Input: ticket_id; authorized context refs; product/version; issue_text_masked; mode; evidence + policy decision
- Output: case_summary; recommended_response/actions; citations; needs_human_review/reason; triage?; known_issue/status?; policy_version; trace_id; versions
- Validation/failure: Unconfirmed root cause, ambiguity, missing policy, expired/exception case → review; no arbitrary confidence claim; authorized actions subset of rule output.
- Persistence: llm_generations + citations + resolution_actions + audit
- API: POST /api/v1/resolution/draft — tồn tại, cần bỏ response mock và mở rộng schema
- Nguồn: SRC-02 §7.9,9.3; SRC-06 §6; SRC-16

```json
{
  "ticket_id": "tk-demo-1",
  "recommended_actions": [
    "route_to_support"
  ],
  "needs_human_review": true,
  "reason_for_review": "unconfirmed_root_cause",
  "citations": []
}
```

### IO-09 — ReviewAction / ResolutionOutcome

- Giai đoạn: M3; producer: Agent/customer feedback → consumer: MOD-06/11→MOD-09.
- Input: ticket_id/draft_id; approve|edit|reject|escalate; reason; final_response; request_id; outcome event
- Output: persisted action_id; state; reviewer/time; sent/resolved/reopened; csat?; resolution_id; timestamps
- Validation/failure: Actor from auth; idempotency; allowed state transitions; no final send before approval where required; outcome absent=unknown.
- Persistence: interactions, resolution_actions, resolution_outcomes
- API: POST ticket review/outcome endpoints — mới; feedback/contribute dùng annotations
- Nguồn: SRC-02 AG-AC-03..05; §8; SRC-03

```json
{
  "ticket_id": "tk-demo-1",
  "action": "reject",
  "reason": "outdated_policy",
  "request_id": "action-demo-1"
}
```

### IO-10 — ABSA prediction

- Giai đoạn: M4; producer: MOD-02 + model/taxonomy → consumer: MOD-07→MOD-04/09/11.
- Input: record_id; text_masked; language; model/taxonomy version; metadata
- Output: aspects[{aspect,category,sentiment,confidence,evidence_span?}]; entities[]; inference_timestamp; versions; supported_language; status
- Validation/failure: Evidence span optional only if supported by source labels/model; positive/neutral/negative; confidence calibrated/marked; preserve aspect-polarity pairing.
- Persistence: absa_predictions keyed by record+model+taxonomy+timestamp; Qdrant derived payload
- API: POST /api/v1/absa/predict; batch worker; legacy /predict deprecated
- Nguồn: SRC-02 §7.3; SRC-06 §3; SRC-07 ABSA

```json
{
  "record_id": "rv-demo",
  "model_version": "baseline-v1",
  "taxonomy_version": "aspect-v1",
  "aspects": [
    {
      "aspect": "design",
      "sentiment": "positive"
    },
    {
      "aspect": "battery",
      "sentiment": "negative"
    }
  ]
}
```

### IO-11 — Metric / cohort context

- Giai đoạn: M5; producer: MOD-09 → consumer: MOD-10→MOD-04.
- Input: validated cohort filters; selected model/taxonomy; date_from/date_to
- Output: metric_id; numerator/denominator/population_count; value; prior_value; delta_pp; model_version; freshness; lineage; filters
- Validation/failure: Negative rate denominator = records mentioning selected aspect in cohort; empty denominator=no-data; not total Top-K; version dedup and timezone explicit.
- Persistence: SQL aggregates/materialized views; analytics query logs
- API: GET /api/v1/analytics/... — mới; drill-down request context
- Nguồn: SRC-02 §7.4,3.4; SRC-04

```json
{
  "metric_id": "battery_negative_rate",
  "numerator": 39,
  "denominator": 100,
  "value": 0.39,
  "population_count": 180,
  "synthetic": true
}
```

### IO-12 — Investigation / GraphContext

- Giai đoạn: M5→M6; producer: Analyst cohort + MOD-04/08 → consumer: MOD-10/06.
- Input: query; full cohort filters/date range; top_k; entity/product/version refs
- Output: summary; evidence; hypotheses[{status,evidence_ids}]; graph paths/entities; population; graph/index/policy versions; issue owner/lifecycle
- Validation/failure: Keep exact filters; 5–10 representative cases if enough; uncertain cause labeled; all edges source linked; graph query bounded.
- Persistence: retrieval_sessions; Neo4j; issue assignments; investigation audit
- API: POST /api/v1/investigation/drilldown — hiện thiếu query/filter richness, mở rộng tương thích
- Nguồn: SRC-02 §7.6–7.7,9.2; SRC-08; SRC-16

```json
{
  "issue_id": "DEMO-ISSUE-1",
  "root_cause_status": "hypothesis",
  "evidence_ids": [
    "rv-demo"
  ],
  "graph_version": "demo-g1"
}
```

### IO-13 — Feedback / KnowledgeChange

- Giai đoạn: M3→M7; producer: Agent/analyst/steward → consumer: MOD-11→MOD-07/08.
- Input: target_id/type; feedback_type; proposed change; evidence IDs; reason; source versions
- Output: contribution_id; author/time; status; reviewer; approved payload; published knowledge/dataset version; conflict reason
- Validation/failure: Auth-derived author; validate discriminated payload types; proposed→reviewed→approved/rejected→published; raw feedback never auto truth.
- Persistence: annotations, model_feedback, knowledge_change_requests; versioned exports
- API: POST /api/v1/feedback/contribute — schema cần typed payload; steward review/publish API mới
- Nguồn: SRC-02 §7.10; SRC-06 §7; SRC-16

```json
{
  "feedback_type": "absa_correction",
  "target_id": "rv-demo",
  "status": "proposed",
  "corrected_aspects": [
    {
      "aspect": "battery",
      "sentiment": "negative"
    }
  ]
}
```

### IO-14 — Evaluation report

- Giai đoạn: M1–M8; producer: Frozen eval datasets + candidate outputs → consumer: Gate reviewer/CI.
- Input: test dataset/version/split; candidate config/hash; hardware; predictions; rubric
- Output: metric values; sample_count; per-query/case results; thresholds; PASS/FAIL/NOT_RUN; limitations; artifacts paths
- Validation/failure: No tuning on test; all missing runs explicit; no benchmark claims from fixtures; each mode evaluated same corpus.
- Persistence: artifacts/evaluation/<run_id>; docs/reports; manifest
- API: pipelines/eval_absa, eval_retrieval, eval_resolution; CI artifacts
- Nguồn: SRC-02 §13,21; SRC-06; SRC-07

```json
{
  "run_id": "TO_BE_GENERATED",
  "metric": "macro_f1",
  "value": null,
  "status": "NOT_RUN",
  "dataset_version": "TO_BE_FROZEN"
}
```

### IO-15 — Release / audit manifest

- Giai đoạn: M0–M8; producer: Build/train/index/publish workflows → consumer: Ops/steward/reviewer.
- Input: git SHA; config/lock; dataset/model/index/graph/policy/prompt revisions; eval artifacts
- Output: immutable digest/hash map; environment; trace dimensions; reviewer/action; backup/rollback refs; cost/timing; status
- Validation/failure: Same image staging→prod; app/model/knowledge rollback separate; secret/PII redacted; verified provenance.
- Persistence: S3/local artifacts; audit DB; redacted traces/logs
- API: run-manifest.json; health live/ready/startup; observability
- Nguồn: SRC-02 §14–16,21; SRC-15; SRC-07

```json
{
  "git_sha": "TO_BE_BUILT",
  "image_digest": "TO_BE_BUILT",
  "model_version": "TO_BE_SELECTED",
  "eval_status": "NOT_RUN",
  "environment": "demo"
}
```

## 6. Dữ liệu và công nghệ

| ID | Dữ liệu | Giai đoạn | Nguồn | Phạm vi | Output | Kiểm chất lượng | Task/IO | Nguồn yêu cầu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DATA-01 | Policy raw → clean → chunks | M1 | Data_crawling exports; public/source-approved docs | Kiểm kê toàn bộ; demo 5–10 policy/~30 clauses | Raw manifest + clean JSONL + approved chunks | URL/title/hash/crawl time; verified effective dates; duplicate/empty checks; manual clause review | M1.1–M1.3; IO-04 | SRC-06 §5,8; SRC-10..13 |
| DATA-02 | Policy golden queries & chat dialogues | M1→M2 | Tự soạn từ policy đã duyệt | 40 queries; 20 dialogues nhiều lượt (đề xuất MVP) | golden_policy_queries.jsonl; chat_eval.jsonl | Dev/test tách theo document/intent; expected sources, no-answer, follow-up, expired/conflict; human rubric | M1.4; M2.2; M2.8 | SRC-06 §4,6; đề xuất MVP |
| DATA-03 | PII evaluation | M1→M8 | Synthetic tiếng Việt/Anh + review thủ công | 500–1,000 cases theo data spec; tối thiểu 500 demo | pii_eval.jsonl; spans + expected_masked_text | Phone/email/person/address/order refs; 0 leaks trong suite; synthetic pass không là bảo đảm tổng quát | M1.4; M3.7; M8.5 | SRC-06 §2.2 |
| DATA-04 | Products/orders/customers | M3 | Synthetic seed có nguồn rõ; live CRM nếu được cấp | 5–10 products; ~15 versions; 200 customer/order records | products_and_orders.json + SQL seed | No real PII; FK/ownership/boundary dates; seed source không nhầm production | M3.1–M3.2; IO-06 | SRC-06 §5.3,8 |
| DATA-05 | Structured policies | M1 catalog→M3 rules | Approved policy document + manual rule transcription | 5–10 versioned policies; ~30 clauses | policies.json + registry | Effective dates/scope/conditions/allowed actions có reviewer; sample 365-day warranty chỉ là fixture | M1.3; M3.3; IO-07 | SRC-06 §5.2,8 |
| DATA-06 | ABSA benchmark/domain extension | M4 | UIT-ViSFD; UIT-ViSD4SA; domain data được phép | Doc nêu 11,122 reviews; xác minh count và official splits; domain bổ sung tùy nhãn | train/dev/test.parquet; taxonomy yaml; data card | Giữ splits nguồn; không tái chia 70/10/20 nếu đã có official split; kiểm quyền; span labels cần riêng; holdout locked | M4.1–M4.4; IO-10 | SRC-06 §3; SRC-07 ABSA |
| DATA-07 | Semantic router | M4 | Synthetic templates + manually reviewed sample; real data khi có quyền | 1,500–3,000 texts theo spec; MVP 1,500 synthetic/curated | router_train/dev/test.jsonl; rubric | macro_review/complaint_ticket/out_of_scope; policy_query map rõ; tránh template overlap test; report synthetic bias | M4.6 | SRC-06 §2.2; DEC-09 |
| DATA-08 | Review/graph golden retrieval queries | M5→M6 | Corpus đã mask + graph fixtures | +40 review queries M5; +20 graph/known-issue M6; tổng ≥100 | golden_queries.jsonl + graded relevance | Mỗi source slice riêng; benchmark dense/BM25/hybrid/reranker; no mixing policy Recall with review Recall | M5.3; M6.8; IO-14 | SRC-06 §4.3,8 |
| DATA-09 | Resolution safety scenarios | M3→M6 | Synthetic verified orders + policies + graph states | 30 cases M3; +20 M6; tổng ≥50 (spec 50–100) | resolution_eval.jsonl | Trong hạn, hết hạn, unconfirmed, injection; bổ sung missing/foreign order, retired policy, action retry; expected approval/actions/citations | M3.7; M6.8 | SRC-06 §6.2,8 |
| DATA-10 | Graph seed | M6 | Curated synthetic known issues + product/policy/evidence IDs | ~15 symptoms; 10 causes; 10 resolutions; 5 centers; bounded graph | neo4j_ontology_seed.json; schema/version manifest | Confirmed có evidence/approval; Issue/Firmware/Team bổ sung theo blueprint; graph bridge IDs stable | M6.1–M6.3; IO-12 | SRC-06 §5,8; SRC-08; SRC-02 §7.6 |
| DATA-11 | Human annotations & outcomes | M3→M7 | UI corrections/edits/relevance/outcome + synthetic demo scripts | Đủ mỗi feedback type; số thực được báo, không bịa adoption | annotations.parquet/jsonl; outcome events; active-learning export | Provenance/authors/review; train export chỉ approved; locked test không hồi vào train; no immediate truth | M3.6; M4.7; M6.6; M7.1–M7.2 | SRC-06 §7; SRC-02 §7.10 |
| DATA-12 | Evaluation/release/ops evidence | M0→M8 | Code/config/data/model/index/graph/policy outputs | Mỗi gate 1 manifest/report; 5 E2E recordings; load snapshots | run-manifest.json; reports; model/data cards; runbooks | Hash/digests; immutable artifacts; sample_count/hardware; status NOT_RUN/FAIL rõ; large weights ngoài Git | Các gate; M8.1–M8.8; IO-15 | SRC-15; SRC-02 §13–16,21 |

| ID | Năng lực | Công nghệ | Giai đoạn | Trạng thái chọn | Cách dùng | Nguồn |
| --- | --- | --- | --- | --- | --- | --- |
| TECH-01 | Backend & API | Python 3.11/3.12; FastAPI; Pydantic; Poetry | M0→M8 | Có trong repo | Typed APIs, validation, middleware, contracts; pin dependencies từ poetry.lock; /api/v1 canonical | SRC-01; SRC-16; WEB-01 |
| TECH-02 | Frontend | React + TypeScript; một bộ component chung | M0/M2→M6 | Đề xuất; framework UI chưa có implementation | Buyer chat trước; tái sử dụng cho agent/analyst/steward; responsive basic; chốt bundler/chart library M0, tránh nhiều frontend stack | WEB-04; SRC-14 |
| TECH-03 | Operational storage | PostgreSQL + versioned migrations | M0→M8 | Target repo | Sessions/history/orders/policies/outcomes/annotations và metric source of truth; chọn driver/migration library tại G0 | SRC-02 §8; SRC-06 §1 |
| TECH-04 | Cache / queues | Redis; Redis Streams; sliding-window limits | M2/M4 | Repo có Redis; queue strategy cần thống nhất | Chọn Redis Streams cho demo, một worker đơn giản; không triển khai đồng thời Celery và Kafka. Cache không là source of truth | SRC-01; SRC-14; DEC-08 |
| TECH-05 | Parsing / ingestion | Python HTML parser, JSONL/Parquet, Pydantic | M1/M4 | Cần triển khai clean/chunk | Tái dùng crawler export; chọn parser theo snapshot; clause-based chunking giữ điều kiện; không cần OCR cho corpus HTML hiện tại | SRC-10; SRC-06 |
| TECH-06 | Vector / lexical retrieval | Qdrant + sentence-transformers + BM25 + RRF | M2/M5 | Target repo; module khung | Benchmark local BM25 reference và Qdrant dense; chọn sparse server-side khi parity/filter tests pass; không gắn vào free-tier quota chưa đo | SRC-02 §7.5; SRC-06 §4; WEB-02 |
| TECH-07 | Embedding & reranker | Vietnamese/multilingual embedding candidate; BGE reranker candidate | M0 smoke; M2 eval | Chốt model ở G0/G2 | Dimension theo model thật; pin version/license; measured quality/latency/resource; enable rerank qua evidence, không mặc định | SRC-06 §4; SRC-07 Retrieval |
| TECH-08 | LLM | Provider-configured LLM API hoặc local model đủ tài nguyên | M0 chọn; M2 tích hợp | Chưa chọn provider/model | Smoke tiếng Việt + JSON/citation; model ID/context/token/cost limit ghi config; secrets ngoài repo; không fine-tune LLM trong 14 tuần | SRC-02 §7.9; DEC-10 |
| TECH-09 | Orchestration/tools | Python bounded FSM; typed tools; MCP adapter; task isolation | M3 | Target architecture | Allowlist/order/warranty/route tools; bounded reflection; action idempotency; không cần framework agent lớn ở MVP; microVM riêng extension | SRC-05 L2/L5; SRC-02 §7.9 |
| TECH-10 | ABSA | TF-IDF + Logistic Regression; PhoBERT candidate với PyTorch/Transformers | M4/M7 | Dependencies có; model pipeline chưa có | Baseline trước; một candidate bounded; tokenizer/splits pin; GPU access quyết định M0; ATE labels riêng; sklearn calibration/metrics | SRC-06 §3; SRC-07 ABSA |
| TECH-11 | Graph | Neo4j; Cypher parameterized; Python driver | M6 | Target repo | Issue-centered canonical schema; constraints/controlled hops; local graph + vector bridge; global summaries/DRIFT để extension | SRC-02 §7.6–7.7; SRC-08; WEB-03 |
| TECH-12 | Analytics | PostgreSQL SQL aggregates; scheduled Python jobs; React charts | M5 | Target repo | Denominator/population, version/freshness, min samples; reuse relational data; BI dedicated product không bắt buộc | SRC-02 §7.4; SRC-14 |
| TECH-13 | Quality & tests | pytest; browser E2E runner; versioned JSONL eval; load harness | M0→M8 | pytest có; browser runner chọn G0 | Unit/contract/integration/eval/E2E/smoke/load; holdout splits; source and safety checks; browser tool cùng một stack cho 3 UIs | SRC-01; SRC-02 §13,16; SRC-16 |
| TECH-14 | Observability | OpenTelemetry; Prometheus; Grafana target | M2→M8 | Dependencies cơ bản có | Request/story/ticket IDs, versions, token/cost, p95, queue/drift; redact logs; dashboards bounded cho demo | SRC-05 L7; SRC-07 monitoring |
| TECH-15 | Packaging & CI | Docker Compose; GitHub Actions; immutable images; manifests | M0→M8 | Có scaffold | Run locally early; AI gates and same artifact promotion; versioned data/model/knowledge rollback | SRC-16; SRC-15; SRC-02 §15–16 |
| TECH-16 | Cloud target | Helm; Terraform; AWS EKS/ECR/S3/Secrets; OIDC and per-service identity | M8; production rollout conditional | Target docs; chưa chứng minh live | Minimal package validate; actual cloud needs access/budget/reviewer; production-grade scaling/HA thêm roadmap; không lấy quota free tier làm cam kết | SRC-02 §14.3,16; SRC-05 §7; DEC-11 |

## 7. Gates và phương pháp đánh giá

Tất cả gate/metric ở baseline có trạng thái **NOT RUN**. Một test suite pass chỉ có hiệu lực trong phạm vi mẫu, hardware, dataset/version và thời gian đã đo. Business pilot và live deployment có trạng thái riêng.

| ID | Nội dung | Mốc | Ngưỡng | Đo thế nào | Artifact | Nguồn/loại | Giới hạn |
| --- | --- | --- | --- | --- | --- | --- | --- |
| G0 | Thiết kế chatbot và khóa phạm vi | M0 | G0: thiết kế chatbot, I/O, scope và ngưỡng eval có owner; quyết định chưa chốt được ghi rõ; 1 người/14 tuần khả thi ở phạm vi demo. | Review all preceding phase tasks + demo + regression + source coverage | docs/reports/milestones/m0-review.md; checklist; demo; manifest phiên bản | SRC-02 §21; SRC-03; SRC-04; Gate bàn giao | Một người tự review theo checklist; external acceptance cần người được ủy quyền nếu áp dụng. |
| G1 | Chuẩn hóa dữ liệu chính sách cho chatbot | M1 | G1: 5–10 policies/~30 clauses đã duyệt, truy nguồn đầy đủ; 40 queries + 20 hội thoại; privacy fixtures; ingestion idempotent. | Review all preceding phase tasks + demo + regression + source coverage | docs/reports/milestones/m1-review.md; checklist; demo; manifest phiên bản | SRC-06; SRC-10; SRC-04; Gate bàn giao | Một người tự review theo checklist; external acceptance cần người được ủy quyền nếu áp dụng. |
| G2 | Chatbot RAG đầu tiên chạy xuyên suốt | M2 | G2: chatbot UI→API→retrieval→LLM→citations chạy thật; multi-turn/fallback/privacy pass; benchmark riêng retrieval và generation. | Review all preceding phase tasks + demo + regression + source coverage | docs/reports/milestones/m2-review.md; checklist; demo; manifest phiên bản | SRC-03 US-BUY-01; SRC-04; SRC-02 §21; Gate bàn giao | Một người tự review theo checklist; external acceptance cần người được ủy quyền nếu áp dụng. |
| G3 | Chatbot theo đơn hàng và Copilot CSKH | M3 | G3: order ownership + deterministic policy + agent review/outcome pass; điều kiện thiếu được hỏi lại; có ticket tới specialist thật trong app. | Review all preceding phase tasks + demo + regression + source coverage | docs/reports/milestones/m3-review.md; checklist; demo; manifest phiên bản | SRC-02 BUY-AC-02..05; AG-AC-01..05; SRC-04; Gate bàn giao | Một người tự review theo checklist; external acceptance cần người được ủy quyền nếu áp dụng. |
| G4 | ABSA và ingestion toàn corpus | M4 | G4: batch coverage 100% accepted corpus với failures minh bạch; model eval thật; triage/corrections hoạt động; target chưa đạt phải ghi rõ. | Review all preceding phase tasks + demo + regression + source coverage | docs/reports/milestones/m4-review.md; checklist; demo; manifest phiên bản | SRC-04; SRC-06 §3; SRC-07 ABSA; Gate bàn giao | Một người tự review theo checklist; external acceptance cần người được ủy quyền nếu áp dụng. |
| G5 | Dashboard toàn corpus và điều tra bằng evidence | M5 | G5: dashboard từ corpus đầy đủ → filtered evidence có thể tái lập; số liệu không lấy từ mock; có freshness và denominator. | Review all preceding phase tasks + demo + regression + source coverage | docs/reports/milestones/m5-review.md; checklist; demo; manifest phiên bản | SRC-02 AN-AC-01..03; SRC-03 US-PM-01; Gate bàn giao | Một người tự review theo checklist; external acceptance cần người được ủy quyền nếu áp dụng. |
| G6 | GraphRAG và quản trị tri thức | M6 | G6: quant→qual→proposed→review→publish→new ticket có bằng chứng; rollback tri thức và các trạng thái chưa xác nhận hoạt động. | Review all preceding phase tasks + demo + regression + source coverage | docs/reports/milestones/m6-review.md; checklist; demo; manifest phiên bản | SRC-02 AN-AC-04..06; §3.5,19; SRC-04; Gate bàn giao | Một người tự review theo checklist; external acceptance cần người được ủy quyền nếu áp dụng. |
| G7 | Closed-loop feedback và cải thiện mô hình | M7 | G7: sửa nhãn/tri thức→duyệt→dataset/model/knowledge version→đánh giá→publish hoặc reject được chạy và truy vết. | Review all preceding phase tasks + demo + regression + source coverage | docs/reports/milestones/m7-review.md; checklist; demo; manifest phiên bản | SRC-02 §7.10,21; SRC-04; Gate bàn giao | Một người tự review theo checklist; external acceptance cần người được ủy quyền nếu áp dụng. |
| G8 | Tích hợp, vận hành và bàn giao | M8 | G8: demo 5 stories + quality/data/governance/release evidence; đánh giá riêng core demo, target quality, cloud và business validation; còn thiếu ghi OPEN. | Review all preceding phase tasks + demo + regression + source coverage | docs/reports/milestones/m8-review.md; checklist; demo; manifest phiên bản | SRC-02 §21; SRC-03; SRC-04; SRC-07; Gate bàn giao | Một người tự review theo checklist; external acceptance cần người được ủy quyền nếu áp dụng. |
| Q-01 | Chatbot policy QA rubric | M2/M8 | ≥90% trên held-out policy QA (đề xuất MVP) | Human rubric correctness/relevance/helpfulness; report n and failure reasons | chatbot_mvp_eval report | Đề xuất mới cho G2; Đề xuất cần khóa G0 | Chưa đo; không phải kết quả hiện tại |
| Q-02 | Citation completeness/precision | M2/M3/M6/M8 | Completeness chung ≥95%; 100% policy/action claim có citation; báo precision riêng | Claim-level annotated rubric + source resolver; valid URL alone không chứng minh entailment | citation evaluation | SRC-05 §9; SRC-04; DEC-04; Target tài liệu | Chưa đo; không phải kết quả hiện tại |
| Q-03 | Unsupported policy/refund/action | M3/M6/M8 | 0 unsupported policy/refund commitments trên critical suite; báo generic rate riêng | ≥50 resolution cases; invalid eligibility/expired/unconfirmed/injection | resolution_eval report | SRC-04; SRC-06 §6; DEC-04; Target tài liệu | Chưa đo; không phải kết quả hiện tại |
| Q-04 | PII and customer isolation | M1/M2/M3/M8 | 0 raw leaks/unauthorized accesses trên suite; phone/email recall=100% trên labeled fixtures | ≥500 synthetic/redaction fixtures; inspect prompts/index/logs; cross-customer/role tests | privacy/access report | SRC-06 §2; SRC-04; Target tài liệu | Suite pass không bảo đảm mọi đầu vào production; name/address slices và limits phải báo. |
| Q-05 | FRT and response latency | M2/M8 | Standard full-response cases <60s; <30s stretch; báo TTFT/p95/p99 riêng | Warm/cold, hardware/corpus/concurrency pin; useful response time vs full response defined | latency report | SRC-03; SRC-04; SRC-05 §5.2; DEC-03; Target tài liệu | Chưa đo; không phải kết quả hiện tại |
| Q-06 | Retrieval quality | M2 baseline/M5/M6 final | Recall@5 ≥.88; MRR ≥.82; Recall@10 ≥.85; nDCG@10 ≥.75 | ≥100 golden queries final, separate policy/review/graph slices; paired modes/corpus; count queries and relevance grading | retrieval benchmark matrix | SRC-05 §9; SRC-06 §4; Target tài liệu | M2 40-query baseline chưa đại diện final corpus; threshold shortfall=FAIL/limited demo, không claim achieved. |
| Q-07 | Filter correctness/source integrity | M2/M5/M6 | 100% authorized filter correctness and source ID resolution on tests | Test date/product/version/aspect-polarity/tenant/approved policy; missing docs and empty cohort | filter/source report | SRC-06 §4; SRC-07 RET-AC; Target tài liệu | Chưa đo; không phải kết quả hiện tại |
| Q-08 | ABSA classification | M4/M8 | MVP floor Macro-F1 ≥.80; target ≥.85; critical per-aspect F1 ≥.75 | Fixed test split; baseline vs candidate; macro/per-aspect confusion/slices; state class averaging explicitly | ABSA eval + model card | SRC-06 §3; SRC-04; DEC-05; Target tài liệu | Chưa đo; không phải kết quả hiện tại |
| Q-09 | ATE/entity/calibration | M4/M8 | Báo span extraction F1, entities và ECE; floor khóa G0 sau label inventory | ATE chỉ trên span labels; polarity metric riêng; calibration fitted dev; report slang/negation/emoji slices | span/calibration report | SRC-02 §13.1; SRC-06 §3; SRC-07; Target cần dữ liệu | Không đánh đồng F1 category/polarity với span extraction; thiếu span test=NOT VALIDATED. |
| Q-10 | Corpus and BI lineage | M4/M5 | 100% eligible ingested records accounted; processed/pending/failed tổng khớp accepted | SQL counts independent; one selected model per record; denominator integrity; no top-k aggregation | coverage/analytics report | SRC-04; SRC-02 AN-AC-01; Target tài liệu | Chưa đo; không phải kết quả hiện tại |
| Q-11 | Representative drill-down | M5/M6 | 5–10 diverse cases nếu cohort đủ; keep all filters | Duplicate/source diversity checks; direct SQL filter parity; report when fewer results exist | investigation eval | SRC-04; SRC-02 AN-AC-02..03; Target tài liệu | Chưa đo; không phải kết quả hiện tại |
| Q-12 | Graph/knowledge governance | M6/M7 | 100% published mutations approved/audited; zero illegal state transitions or invalid relations in suite | Constraints/orphan/duplicate checks; denied mutation/rollback; source coverage; domain-specific cycle rules | graph eval + approval audit | SRC-05 §4; SRC-02 §13.3; DEC-06; Target tài liệu | Chưa đo; không phải kết quả hiện tại |
| Q-13 | Anomaly/knowledge freshness | M5/M6/M8 | Alert precision ≥90%; drift detection <24h; knowledge freshness <24h (targets) | Labeled anomaly replay + measured schedules; real observed window needed; published version timestamps | alert/freshness report | SRC-05 §4; Target tài liệu | Synthetic replay pass không đủ chứng minh production detection SLA. |
| Q-14 | Root-cause investigation speed | M6/M8 | Investigation time <2h; emerging issue detection 24–48h (different clocks) | Start alert→analyst conclusion; issue first event→detection; require reviewers/sample cases | investigation timing report | SRC-05 §4; SRC-03; Target tài liệu | Không nhập hai định nghĩa thời gian thành một; self-run demo ghi rõ. |
| Q-15 | Business impact | M8 / live pilot | AHT reduction ≥40%; FCR improvement ≥15%; draft acceptance ≥80%; track MTTR/CSAT/reopen/cost | Manual vs assisted comparable cohorts; define relative FCR change; n/time window/confounds; real customer pilot separate | business KPI report | SRC-03; SRC-05 §4,9; SRC-06 §7; Target business cần pilot | Không có real pilot → NOT VALIDATED; demo synthetic chỉ kiểm công thức/instrumentation. |
| Q-16 | Latency, availability and scale | M8 | ABSA p95 ≤300ms; search no-rerank p95 ≤250ms; pipeline <2s; availability 99.5–99.9% là target cần chốt | Freeze hardware/corpus/concurrency/cold-warm; 1x/3x/10x bounded load; separate measured test and long-term uptime | performance/limits report | SRC-07 NFR; SRC-05 §5.2; Giả định planning trong nguồn | Không kiểm chứng sustained availability trong short load test; cần observation window và resource budget. |
| Q-17 | Release reproducibility and recovery | M8 | Same artifact digest; all versions attached; app/model/index/knowledge rollback demonstrated | Fresh deploy, smoke tests, restore/rebuild and rollback drill; record recovery time/RPO/RTO chosen at G0 | release manifest + recovery report | SRC-02 §15–16,21; SRC-15; Target tài liệu | Chưa đo; không phải kết quả hiện tại |
| Q-18 | Full user-story acceptance | M8 | 5 role flows demo pass; all core acceptance IDs evidence; conditional/deferred explicit | Browser/API E2E; role matrix; scenario firmware; coverage lookup and reports | UAT recordings + acceptance matrix | SRC-02 §21; SRC-03; SRC-04; Gate bàn giao | Demo completion không tự đóng live cloud/real business impact/advanced extension gates. |

## 8. Traceability bao phủ kiến trúc và user stories

90 dòng bao gồm 5 user stories, acceptance IDs nguyên bản, PM/Steward IDs do kế hoạch đặt, 7 tầng, 2 pipelines, dữ liệu/governance/ops, research ACs và advanced extensions. Coverage là **PLANNED**, không phải chứng nhận đã triển khai.

| Requirement | Yêu cầu | Nguồn | Tasks | Modules | I/O | Gate | Scope |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BUY-AC-01 | Ticket lưu aspect/sentiment/entities và model version | SRC-02 §3.1–3.3 | M4.1,M4.5,M4.7 | MOD-07 | IO-03,IO-10 | G4 | Core demo |
| BUY-AC-02 | Draft có policy ID/version phù hợp | SRC-02 §3.1–3.3 | M1.3,M3.3,M3.4 | MOD-06 | IO-07,IO-08 | G3 | Core demo |
| BUY-AC-03 | Khẳng định root cause truy ngược tới evidence | SRC-02 §3.1–3.3 | M6.3,M6.4,M6.8 | MOD-08 | IO-05,IO-12 | G6 | Core demo |
| BUY-AC-04 | Thiếu evidence/policy phải hỏi thêm hoặc review; không đoán | SRC-02 §3.1–3.3 | M2.4,M2.8,M3.7,M6.4 | MOD-03,MOD-06 | IO-02,IO-08 | G2,G3,G6 | Core demo |
| BUY-AC-05 | Resolved outcome gắn ticket/resolution | SRC-02 §3.1–3.3 | M3.6,M7.5 | MOD-06,MOD-09 | IO-09 | G3,G7 | Core demo |
| AG-AC-01 | Không hiển thị hypothesis như fact | SRC-02 §3.1–3.3 | M3.5,M6.4,M6.5 | MOD-08,MOD-11 | IO-08,IO-12 | G3,G6 | Core demo |
| AG-AC-02 | Policy có source/version/effective date | SRC-02 §3.1–3.3 | M1.3,M3.3,M6.7 | MOD-06 | IO-04,IO-07 | G1,G3,G6 | Core demo |
| AG-AC-03 | Approve/edit/reject có lý do và feedback log | SRC-02 §3.1–3.3 | M3.5,M3.6,M7.1 | MOD-11 | IO-09,IO-13 | G3,G7 | Core demo |
| AG-AC-04 | Agent xem evidence gốc trước gửi | SRC-02 §3.1–3.3 | M3.5,M3.7 | MOD-04,MOD-11 | IO-05,IO-08 | G3 | Core demo |
| AG-AC-05 | Persist state/action/final response để tính MTTR/FCR/CSAT | SRC-02 §3.1–3.3 | M3.6,M5.2,M8.7 | MOD-06,MOD-09 | IO-09,IO-11 | G3,G5,G8 | Core demo |
| AN-AC-01 | Dashboard truy ngược population và bản ghi được tính | SRC-02 §3.1–3.3 | M4.5,M5.1,M5.4 | MOD-07,MOD-09 | IO-10,IO-11 | G4,G5 | Core demo |
| AN-AC-02 | Investigation giữ nguyên filters từ dashboard | SRC-02 §3.1–3.3 | M5.3,M5.4 | MOD-04,MOD-10 | IO-11,IO-12 | G5 | Core demo |
| AN-AC-03 | Retrieval có source IDs và timestamp | SRC-02 §3.1–3.3 | M2.1,M5.3 | MOD-04 | IO-05 | G2,G5 | Core demo |
| AN-AC-04 | Annotation có version/author/time | SRC-02 §3.1–3.3 | M4.7,M6.5,M7.1 | MOD-11 | IO-13 | G4,G6,G7 | Core demo |
| AN-AC-05 | Graph update có approval/audit, không silent overwrite | SRC-02 §3.1–3.3 | M6.6,M6.7 | MOD-08,MOD-11 | IO-13,IO-15 | G6 | Core demo |
| AN-AC-06 | Corrected ABSA labels export được sang train/eval | SRC-02 §3.1–3.3 | M7.1,M7.2,M7.5 | MOD-07,MOD-11 | IO-10,IO-13 | G7 | Core demo |
| PM-AC-01 | Population size và denominator theo SKU/hardware/firmware | SRC-02 §3.4–3.5; SRC-05 §3–4 (ID PM/KS do kế hoạch đặt) | M5.1,M5.2,M5.4 | MOD-09,MOD-10 | IO-11 | G5 | Core demo |
| PM-AC-02 | Root-cause hypothesis/confirmed/rejected hiển thị rõ | SRC-02 §3.4–3.5; SRC-05 §3–4 (ID PM/KS do kế hoạch đặt) | M6.1,M6.5 | MOD-08,MOD-10 | IO-12 | G6 | Core demo |
| PM-AC-03 | Resolution success/reopen/recurrence/MTTR/FCR/CSAT/cost | SRC-02 §3.4–3.5; SRC-05 §3–4 (ID PM/KS do kế hoạch đặt) | M3.6,M5.2,M7.5,M8.7 | MOD-09 | IO-09,IO-11 | G5,G7,G8 | Core demo |
| PM-AC-04 | Mỗi issue có owner và lifecycle | SRC-02 §3.4–3.5; SRC-05 §3–4 (ID PM/KS do kế hoạch đặt) | M6.1,M6.5 | MOD-08,MOD-10 | IO-12 | G6 | Core demo |
| PM-AC-05 | Drill-down tôn trọng role và tối thiểu PII | SRC-02 §3.4–3.5; SRC-05 §3–4 (ID PM/KS do kế hoạch đặt) | M5.2,M5.4,M8.5 | MOD-10,MOD-12 | IO-11,IO-12 | G5,G8 | Core demo |
| KS-AC-01 | Approve/reject graph changes theo quyền | SRC-02 §3.4–3.5; SRC-05 §3–4 (ID PM/KS do kế hoạch đặt) | M6.6,M6.8 | MOD-08,MOD-11 | IO-13 | G6 | Core demo |
| KS-AC-02 | Retire outdated policy, invalidation và stale alerts | SRC-02 §3.4–3.5; SRC-05 §3–4 (ID PM/KS do kế hoạch đặt) | M1.3,M6.6,M6.7 | MOD-06,MOD-08 | IO-04,IO-15 | G6 | Core demo |
| KS-AC-03 | Resolve conflicting causes/annotations | SRC-02 §3.4–3.5; SRC-05 §3–4 (ID PM/KS do kế hoạch đặt) | M6.6,M7.1 | MOD-08,MOD-11 | IO-13 | G6,G7 | Core demo |
| KS-AC-04 | Publish knowledge version và rollback | SRC-02 §3.4–3.5; SRC-05 §3–4 (ID PM/KS do kế hoạch đặt) | M6.7,M8.5 | MOD-08,MOD-12 | IO-15 | G6,G8 | Core demo |
| KS-AC-05 | Retention/deletion/access policy có owner | SRC-02 §3.4–3.5; SRC-05 §3–4 (ID PM/KS do kế hoạch đặt) | M0.3,M7.4,M8.5 | MOD-12 | IO-13,IO-15 | G7,G8 | Core demo |
| KS-AC-06 | Audit lineage từ ticket đến model/policy/graph/human approval | SRC-02 §3.4–3.5; SRC-05 §3–4 (ID PM/KS do kế hoạch đặt) | M3.6,M6.7,M8.1 | MOD-12 | IO-15 | G3,G6,G8 | Core demo |
| US-BUY-01 | Buyer complaint→verified order/policy→evidence→action→outcome | SRC-03; SRC-05 §3; SRC-02 §3 | M2.8,M3.7,M4.7,M6.8,M8.6 | MOD-01,MOD-03,MOD-05,MOD-06,MOD-07,MOD-08 | IO-01,IO-08,IO-09 | G8 | Core demo |
| US-AGENT-01 | Pre-triaged card, grounded draft, evidence, review/correction/escalation | SRC-03; SRC-05 §3; SRC-02 §3 | M3.5,M4.7,M6.8,M7.5,M8.6 | MOD-07,MOD-11 | IO-08,IO-09,IO-13 | G8 | Core demo |
| US-ANALYST-01 | Quant→filtered diverse evidence→hypothesis→approved knowledge→support reuse | SRC-03; SRC-05 §3; SRC-02 §3 | M5.4,M6.8,M7.5,M8.6 | MOD-04,MOD-08,MOD-09,MOD-10,MOD-11 | IO-11,IO-12,IO-13 | G8 | Core demo |
| US-PM-01 | SKU/version defect trends, cause state, ownership và resolution effectiveness | SRC-03; SRC-05 §3; SRC-02 §3 | M5.2,M6.5,M8.6,M8.7 | MOD-08,MOD-09,MOD-10 | IO-09,IO-11,IO-12 | G8 | Core demo |
| US-STEWARD-01 | Governed graph/policy changes, versions, conflict, access/retention và audit | SRC-03; SRC-05 §3; SRC-02 §3 | M6.6,M6.7,M7.4,M8.6 | MOD-06,MOD-08,MOD-11,MOD-12 | IO-13,IO-15 | G8 | Core demo |
| ARCH-L1 | Gateway: parse/PII/rate limit/semantic routing | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M1.2,M1.3,M4.5,M4.6 | MOD-02,MOD-12 | IO-03 | G4 | Core demo |
| ARCH-L2 | Planning/FSM/bounded reflection và handoff | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M3.4,M3.7 | MOD-01,MOD-06 | IO-08 | G3 | Core demo |
| ARCH-L3 | Working context; sliding buffer; episodic recall; semantic/procedural memory | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M0.3,M2.5,M3.2,M3.3,M6.3 | MOD-01,MOD-05,MOD-06,MOD-08 | IO-01,IO-06,IO-07 | G3,G6 | Core demo |
| ARCH-L4 | Dense/BM25/RRF/BGE + metadata + operational GraphRAG | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M2.1,M2.2,M2.3,M5.3,M6.3 | MOD-04,MOD-08 | IO-05,IO-12 | G2,G6 | Core demo |
| ARCH-L5 | Typed/function tools/MCP; authorized actions và task isolation | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M3.4,M3.8 | MOD-05,MOD-06,MOD-12 | IO-06,IO-07,IO-08 | G3 | Core demo |
| ARCH-L6 | Claim/citation/schema/policy guard + output PII + abstention | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M2.4,M2.8,M3.7,M6.4,M8.5 | MOD-03,MOD-06 | IO-02,IO-08 | G2,G3,G8 | Core demo |
| ARCH-L7 | OTel traces, tokens/cost, model/data drift và operational metrics | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M2.7,M7.3,M8.3 | MOD-09,MOD-12 | IO-15 | G2,G7,G8 | Core demo |
| ARCH-PIPE-A | Ingest→mask→ABSA 100% corpus→SQL→BI, async throughput | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M4.5,M5.1 | MOD-02,MOD-07,MOD-09 | IO-03,IO-10,IO-11 | G5 | Core demo |
| ARCH-PIPE-B | Query→filters→evidence→graph/policy→generation→guardrails | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M2.8,M3.4,M6.4 | MOD-01,MOD-03,MOD-04,MOD-06,MOD-08 | IO-01,IO-05,IO-08 | G6 | Core demo |
| ARCH-BOUNDARY | ABSA != retrieval; Top-K != statistics; GraphRAG operational; policy deterministic | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M0.3,M3.3,M4.5,M5.4,M6.1 | MOD-04,MOD-06,MOD-07,MOD-08,MOD-09 | IO-07,IO-10,IO-11 | G6 | Core demo |
| API-CONTRACTS | Canonical /api/v1 ingest/investigation/resolution/feedback plus chat/ABSA/retrieval | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M0.3,M2.5,M3.4,M4.5,M4.6,M5.3,M7.1 | MOD-12 | IO-01,IO-03,IO-08,IO-10,IO-12,IO-13 | G8 | Core demo |
| DATA-SOT | CRM/raw events/predictions/policy/graph/final response/outcome source-of-truth boundaries | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M0.3,M1.1,M3.1,M3.6,M4.5,M6.7 | MOD-02,MOD-05,MOD-06,MOD-08 | IO-03,IO-04,IO-09,IO-15 | G6 | Core demo |
| DATA-QUALITY | Duplicate/missing/spam/language/date/schema/source checks; no hidden rejection | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M1.2,M4.5,M4.6 | MOD-02 | IO-03 | G4 | Core demo |
| DATA-PRIVACY | Masked vector/prompt/log; resolution access tách analytics; cross-customer filters | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M1.3,M2.5,M3.2,M8.5 | MOD-02,MOD-05,MOD-12 | IO-01,IO-06,IO-15 | G8 | Core demo |
| FEEDBACK-TYPES | ABSA/retrieval/cause/policy-stale/resolution-outcome/draft/new-issue/duplicate feedback | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M3.5,M6.5,M6.6,M7.1 | MOD-11 | IO-13 | G7 | Core demo |
| GOVERNANCE | Data ownership/license, review, retention/deletion, access and audit lineage | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M0.1,M4.1,M6.6,M7.4,M8.5 | MOD-12 | IO-13,IO-15 | G8 | Core demo |
| OPS-RELEASE | Build once; digest; staging→prod same artifact; independent model/app/knowledge rollback | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M6.7,M8.1,M8.5 | MOD-12 | IO-15 | G8 | Core demo |
| OPS-SCALING | API/ABSA/retrieval/graph/LLM/jobs separate resource boundaries and scaling targets | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M0.3,M4.5,M8.2,M8.4 | MOD-12 | IO-15 | G8 | Core bounded tests/design; sustained/live scale conditional |
| OPS-SECURITY | OIDC least privilege, per-service identity, secrets, non-root/read-only, network restrictions | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M8.2,M8.5 | MOD-12 | IO-15 | G8 | Core bounded tests/design; sustained/live scale conditional |
| OPS-RECOVERY | Backup/rebuild index/restore/rollback; incident runbooks; dependency failure paths | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M2.7,M6.7,M8.4,M8.5,M8.8 | MOD-12 | IO-15 | G8 | Core demo |
| QA-TEST-PYRAMID | Unit/contract/integration/eval/E2E/smoke/load; versioned AI gates | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M0.4,M2.8,M3.7,M4.4,M5.4,M6.8,M7.5,M8.1,M8.6 | MOD-12 | IO-14 | G8 | Core demo |
| QA-ABSA | ATE/APC/category/calibration; macro/per-aspect/slices; no hallucinated aspect | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M4.1,M4.2,M4.3,M4.4 | MOD-07 | IO-10,IO-14 | G4 | Core demo |
| QA-RETRIEVAL | BM25/dense/hybrid/rerank comparison, Recall/MRR/nDCG, filter correctness/diversity/index freshness | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M2.2,M2.3,M5.3,M6.8 | MOD-04 | IO-05,IO-14 | G6 | Core demo |
| QA-GRAPH | Schema/entity integrity, orphan/duplicates, relation correctness, evidence, stale policy, approval | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M6.1,M6.2,M6.7,M6.8 | MOD-08 | IO-12,IO-14 | G6 | Core demo |
| QA-RESOLUTION | Groundedness/citation precision/completeness, policy correctness, unsupported action, abstention | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M2.8,M3.7,M6.8,M8.6 | MOD-03,MOD-06 | IO-08,IO-14 | G8 | Core demo |
| QA-NFR | Latency/p95/p99/throughput/availability/freshness/scaling/error/reliability/cost | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M2.7,M7.3,M8.3,M8.4 | MOD-12 | IO-15 | G8 | Core bounded tests/design; sustained/live scale conditional |
| QA-BUSINESS | FRT/AHT/MTTR/FCR/CSAT/reopen/escalation/recurrence/cost/acceptance; baseline and sample size | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M0.4,M3.6,M5.2,M8.7 | MOD-09 | IO-09,IO-11 | G8 | Core instrumentation; real impact conditional |
| HANDOVER | User stories demonstrated; AI eval; knowledge/governance; release/runbooks; defense narrative | SRC-02 §5–22; SRC-05; SRC-06; SRC-07; SRC-09 | M8.6,M8.8 | MOD-12 | IO-14,IO-15 | G8 | Core demo |
| ABSA-AC-01 | Multi-aspect contrasting review correct | SRC-07 ABSA acceptance | M4.2,M4.7 | MOD-07,MOD-12 | IO-10,IO-14 | G4,G8 | Core demo |
| ABSA-AC-02 | Output schema/version/record ID | SRC-07 ABSA acceptance | M4.2,M4.5 | MOD-07,MOD-12 | IO-10,IO-14 | G4,G8 | Core demo |
| ABSA-AC-03 | Không bịa aspect; none/other behavior | SRC-07 ABSA acceptance | M4.2 | MOD-07,MOD-12 | IO-10,IO-14 | G4,G8 | Core demo |
| ABSA-AC-04 | Validation lỗi có cấu trúc | SRC-07 ABSA acceptance | M4.5 | MOD-07,MOD-12 | IO-10,IO-14 | G4,G8 | Core demo |
| ABSA-AC-05 | Macro-F1 floor theo release | SRC-07 ABSA acceptance | M4.4 | MOD-07,MOD-12 | IO-10,IO-14 | G4,G8 | Core demo |
| ABSA-AC-06 | Critical aspect F1 floor | SRC-07 ABSA acceptance | M4.4 | MOD-07,MOD-12 | IO-10,IO-14 | G4,G8 | Core demo |
| ABSA-AC-07 | Inference p95 trên hardware pin | SRC-07 ABSA acceptance | M4.4,M8.4 | MOD-07,MOD-12 | IO-10,IO-14 | G4,G8 | Core demo |
| ABSA-AC-08 | PII trong logs được mask | SRC-07 ABSA acceptance | M1.3,M8.5 | MOD-07,MOD-12 | IO-10,IO-14 | G4,G8 | Core demo |
| ABSA-AC-09 | Truy vết hai model versions | SRC-07 ABSA acceptance | M4.5,M5.1 | MOD-07,MOD-12 | IO-10,IO-14 | G4,G8 | Core demo |
| ABSA-AC-10 | Unsupported language rõ | SRC-07 ABSA acceptance | M4.2,M4.6 | MOD-07,MOD-12 | IO-10,IO-14 | G4,G8 | Core demo |
| RET-AC-01 | Ranked hits/schema/index version | SRC-07 Retrieval acceptance | M2.1 | MOD-04,MOD-12 | IO-05,IO-14 | G2,G5,G8 | Core demo |
| RET-AC-02 | Exact filter correctness | SRC-07 Retrieval acceptance | M5.3 | MOD-04,MOD-12 | IO-05,IO-14 | G2,G5,G8 | Core demo |
| RET-AC-03 | Recall@10 baseline threshold | SRC-07 Retrieval acceptance | M2.2,M5.3 | MOD-04,MOD-12 | IO-05,IO-14 | G2,G5,G8 | Core demo |
| RET-AC-04 | nDCG@10 graded relevance | SRC-07 Retrieval acceptance | M5.3 | MOD-04,MOD-12 | IO-05,IO-14 | G2,G5,G8 | Core demo |
| RET-AC-05 | Source ID resolves | SRC-07 Retrieval acceptance | M2.1,M6.8 | MOD-04,MOD-12 | IO-05,IO-14 | G2,G5,G8 | Core demo |
| RET-AC-06 | Empty evidence supported | SRC-07 Retrieval acceptance | M2.4 | MOD-04,MOD-12 | IO-05,IO-14 | G2,G5,G8 | Core demo |
| RET-AC-07 | Search p95 bounded corpus | SRC-07 Retrieval acceptance | M8.4 | MOD-04,MOD-12 | IO-05,IO-14 | G2,G5,G8 | Core demo |
| RET-AC-08 | Reranker enable only measured gain | SRC-07 Retrieval acceptance | M2.3 | MOD-04,MOD-12 | IO-05,IO-14 | G2,G5,G8 | Core demo |
| RET-AC-09 | Index/data/embedding lineage | SRC-07 Retrieval acceptance | M2.1,M6.7 | MOD-04,MOD-12 | IO-05,IO-14 | G2,G5,G8 | Core demo |
| RET-AC-10 | Regression gate before index promotion | SRC-07 Retrieval acceptance | M8.1 | MOD-04,MOD-12 | IO-05,IO-14 | G2,G5,G8 | Core demo |
| RET-AC-11 | PII/sensitive query logs redacted | SRC-07 Retrieval acceptance | M1.3,M8.5 | MOD-04,MOD-12 | IO-05,IO-14 | G2,G5,G8 | Core demo |
| RET-AC-12 | Readiness during rebuild/unavailable | SRC-07 Retrieval acceptance | M2.1,M2.7 | MOD-04,MOD-12 | IO-05,IO-14 | G2,G5,G8 | Core demo |
| EXT-01 | Global GraphRAG / DRIFT-like query | SRC-02 §7.7B,18 Phase5 | M6.9 | MOD-12 | IO-15 | G8 | Deferred sau W14 |
| EXT-02 | Autonomous multi-step actions / proactive outreach | SRC-02 §18 Phase5 | M6.9 | MOD-12 | IO-15 | G8 | Deferred sau W14 |
| EXT-03 | MicroVM isolation | SRC-05 L5; SRC-01 | M3.8,M6.9 | MOD-12 | IO-15 | G8 | Conditional extension |
| EXT-04 | ASTE/ACOS / English expansion / alternative encoder roster | SRC-02 §7.3; SRC-07 ABSA | M4.1,M6.9 | MOD-12 | IO-15 | G8 | Deferred sau W14 |
| EXT-05 | Live production EKS, HA/GPU autoscaling, availability validation | SRC-02 §14–16; SRC-07 NFR | M8.2,M8.3,M8.4,M8.5 | MOD-12 | IO-15 | G8 | Conditional resource + sau demo |
| EXT-06 | Real CRM/commerce connectors và real business pilot | SRC-02 §7.1,8.2,13.5; SRC-03 | M3.2,M8.7 | MOD-12 | IO-15 | G8 | Conditional data access |
| EXT-07 | Multimodal parsers / call transcripts / more channels | SRC-05 L1; SRC-02 §7.1 | M0.1,M6.9 | MOD-12 | IO-15 | G8 | Deferred theo data need |
| EXT-08 | Dedicated annotation platform / large-scale active learning | SRC-02 §10.5,7.10; SRC-07 | M7.1,M7.2 | MOD-12 | IO-15 | G8 | Deferred sau W14 |

## 9. Quyết định, giả định và phạm vi mở rộng

| ID | Chủ đề | Vấn đề | Quyết định | Trạng thái | Hạn chốt | Ảnh hưởng |
| --- | --- | --- | --- | --- | --- | --- |
| DEC-01 | Lịch và nhân lực | User: 14 tuần từ 26/10/2026; chỉ 1 người | 14 tuần đến 31/01/2027; làm việc cuối 29/01; 5 ngày/tuần, 1 ngày=8h; 60 ngày task + 10 slot dự phòng/nghỉ. 01/01/2027 dành 1 slot nghỉ dự kiến; còn 9 ngày dự phòng thực. | Đã xác nhận lịch/người; giờ/nghỉ là giả định | M0.G | Nếu làm part-time/nghỉ thêm: dùng dự phòng rồi rebaseline; không song song nhiều vai trò. |
| DEC-02 | Phạm vi một người | Full blueprint gồm nhiều tầng enterprise; 14 tuần không đồng nghĩa production đạt hết | Cam kết phạm vi bounded demo 5 personas; every requirement có coverage. Optional advanced được deferred; cloud/real CRM/business pilot có gate phụ thuộc. | Đề xuất kế hoạch | M0.G | Không tuyên bố toàn bộ target architecture đã production-ready; gate thất bại cần kế hoạch sửa. |
| DEC-03 | FRT 30s/60s và pipeline <2s | User story <30s; acceptance/blueprint <60s; architecture pipeline <2s | Chat MVP standard scenarios: full response <60s trên bộ test; <30s stretch. <2s tách stage budget/target cần đo, không thay nghĩa thành first-token nếu chưa có ADR. | Cần chốt tại G0 | M0.G; M2.G; M8.4 | FRT đo từ gửi ticket đến phản hồi đầu hữu ích; TTFT và full latency báo riêng, sample/hardware rõ. |
| DEC-04 | Unsupported action / citations / business KPI | Acceptance zero promises; architecture ≤1% actions, ≥95% completeness; FCR +15% chưa rõ đơn vị | Zero unsupported policy/refund commitments trên critical suite; generic unsupported-action rate báo riêng. Policy claims cần citation 100%, completeness chung ≥95%. FCR +15% tạm hiểu tương đối, chốt baseline/denominator tại G0. | Cần chốt ngưỡng/định nghĩa | M0.G; M3.7; M8.7 | Mục tiêu business AHT ≥40%, FCR ≥15%, draft accept ≥80% chưa là kết quả; real pilot mới validate. |
| DEC-05 | ABSA/Recall và latency targets | Research ghi MVP F1 .80; acceptance .85; Recall@5 .88/@10 .85; p95 250/300ms giả định | Demo floor F1 .80, production .85, critical aspect .75. Báo Recall@5 và @10 riêng cùng query set; @10 phải không thấp hơn @5 thực đo. Tất cả latency trên hardware/corpus pin. | Targets cần baseline; không sửa số đo | M0.G; M4.4; M5.3 | Ngưỡng Recall@10 thấp hơn @5 là floor yếu hơn, không phải kỳ vọng Recall giảm. Model failure không tự giảm gate. |
| DEC-06 | Ontology và trạng thái nguyên nhân | Blueprint có Issue/Firmware/Evidence/Team; schema rút gọn lấy RootCause trung tâm; status names khác | Canonical Issue-centered ontology theo blueprint; adapter cho schema rút gọn; tách issue vs root-cause states; cause hypothesis/under_review/confirmed/rejected; issue emerging/investigating/confirmed/mitigated/monitored/closed. | Đề xuất ADR | M0.3; M6.1 | Chu trình graph hợp lệ không cấm toàn cục; chỉ kiểm chu trình trái invariant. Knowledge freshness <24h là target cần đo. |
| DEC-07 | API và schemas chưa đủ chatbot | Blueprint cũ /v1/... khác README /api/v1/...; FeedbackRecord bắt product_id; Citation thiếu URL/version | Giữ /api/v1 hiện có, thêm /chat/messages, schema conversation riêng; mở rộng citation và investigation; status enum; legacy endpoints deprecated; migration tương thích. | Đề xuất chuẩn canonical | M0.3; M2.5; M5.3 | Không chặn hỏi chính sách chung do thiếu product. Ghi OpenAPI version và contract tests. |
| DEC-08 | BM25 backend, queue và scale | README BM25 ngoài/Qdrant; data spec server-side sparse; worker nhắc Redis/Kafka, README Celery | Demo một Redis Streams worker; local BM25 làm reference; dense+BM25+RRF contract ổn định. Chọn server-side sparse sau parity/filter benchmark; API modular monolith + worker. | Đề xuất đơn giản hóa triển khai | M0.3; M2.2; M4.5 | Không đưa Kafka/Celery/microservices vào cùng sprint; độc lập scale là boundary thiết kế và roadmap. |
| DEC-09 | Dữ liệu, taxonomy và router | UIT count/split minh họa; 10 aspect vs macro categories; 3-class router không có policy Q&A | Xác minh license/count/split chính thức; freeze taxonomy mapping; bổ sung domain labels; policy_query subintent thuộc service/chat branch; paired aspect-polarity payload. | Cần khóa tại G0/G4 | M0.3; M4.1; M4.6 | Synthetic không là production evidence; unsupported language rõ; dataset span không tự suy từ category labels. |
| DEC-10 | LLM/model/provider và thiếu benchmark | Docs không khóa provider; embedding dimension/model candidates khác nhau; confidence .70 chưa calibrate | Smoke chọn tại M0.3 theo tiếng Việt/schema/cost/access; config/version pin; confidence chỉ dùng khi có calibration hoặc rubric; .70 là rule thử nghiệm phải validate. | Chưa chọn model; không chặn lập kế hoạch | M0.3; M2.4; M4.4 | Thiếu key/compute chuyển resource blocker, không thay bằng response hardcoded rồi gọi hoàn thành. |
| DEC-11 | Cloud và giới hạn free tier | Docs nêu EKS/HA/GPU/scaling và quota RAM/node cụ thể nhưng chưa có deployment evidence | Compose demo bắt buộc; IaC package core M8; live EKS/CRM/prod phụ thuộc quyền/budget/reviewer; đo actual sizing, không kế thừa quota/số RAM chưa xác minh. | Resource gate | M0.3; M8.2–M8.3 | Thiếu resource: cloud gate BLOCKED/NOT_RUN; không thế bằng local pass; plan production mở rộng sau demo. |
| DEC-12 | Nguồn lịch sử và bảo vệ dữ liệu | Research còn nhắc kiosk/old docs; Final_project tham chiếu file không có; legal claims chưa kiểm chứng độc lập | Lấy user instruction + current product/architecture làm chuẩn; research dùng eval/NFR/baseline. Ghi nguồn thiếu; privacy controls triển khai; legal/licensing sign-off giao owner, không claim compliance. | Source precedence | M0.1; M7.4; M8.5 | Không đưa ASR/TTS kiosk thành requirement SenticRAG; không tự thực thi policy theo văn bản luật trích dẫn chưa rà soát. |
| DEC-13 | Human reviewer khi chỉ một developer | 5 personas gồm agent/steward; governance cần người được ủy quyền | Dev mô phỏng roles bằng accounts tách trong demo; tự review theo checklist có evidence. External UAT/production approval chỉ ghi Done khi người có thẩm quyền thực sự duyệt. | Giới hạn kiểm chứng | M0.G; M6.6; M8.6 | Không bịa nhóm 3 người từ template; không gán tên thành viên dự án khác. |
| DEC-14 | PII và policy applicability | 100% masking/context trong acceptance là target tuyệt đối; policy crawl thiếu ngày hiệu lực | Kiểm 0 leaks trên suite có scope; entity/date thiếu → unknown/review, không tự điền. 100% context availability hiểu có trạng thái known/missing/unauthorized rõ, không invent order. | Cần chốt acceptance scope | M1.3; M3.2; M8.5 | Production redaction/generalization cần audit thêm; chưa có identity liên kết thì phải xác minh. |

| ID | Hạng mục | Scope | Task xem xét | Nguồn | Điều kiện | Output tương lai | Giới hạn core |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EXT-01 | Global GraphRAG / DRIFT-like query | Deferred sau W14 | M6.9 | SRC-02 §7.7B,18 Phase5 | Cần query set global + local/warehouse baseline + token/cost budget | Implement bounded experiment; quality/cost report; chỉ promote nếu gain | Không cần cho 5 demo stories local entity-centered |
| EXT-02 | Autonomous multi-step actions / proactive outreach | Deferred sau W14 | M6.9 | SRC-02 §18 Phase5 | Đã có policy rules, authorization, rollback/idempotency và approve action matrix | Controlled action integration + verified delivery/outcome | Chatbot M3 có tools/approval; tự động hoàn tiền/liên hệ chủ động chưa triển khai |
| EXT-03 | MicroVM isolation | Conditional extension | M3.8; M6.9 | SRC-05 L5; SRC-01 | Có nhu cầu chạy code không tin cậy và hạ tầng hỗ trợ; task isolation hiện tại không đủ | MicroVM proof-of-concept và threat/resource tests | 14 tuần dùng allowlisted typed tools + task/container isolation; không gọi đây là microVM |
| EXT-04 | ASTE/ACOS / English expansion / alternative encoder roster | Deferred sau W14 | M4.1; M6.9 | SRC-02 §7.3; SRC-07 ABSA | Có labels opinion/span/category, quyền dataset và tài nguyên; core ABSA gate đã ổn | Candidate comparisons, slices và model card | MVP tiếng Việt; ATE chỉ nếu nhãn phù hợp; multi-language unsupported path vẫn có |
| EXT-05 | Live production EKS, HA/GPU autoscaling, availability validation | Conditional resource + sau demo | M8.2–M8.5 | SRC-02 §14–16; SRC-07 NFR | Cloud account/budget, qualified reviewer, secrets/backup, đủ load/monitoring window | Live deploy evidence; sustained SLO; scaling/restore; audited prod approval | IaC minimal + local demo có trong core; live target chưa có evidence không được đóng |
| EXT-06 | Real CRM/commerce connectors và real business pilot | Conditional data access | M3.2; M8.7 | SRC-02 §7.1,8.2,13.5; SRC-03 | API access/quyền dữ liệu, baseline cohort, support/product reviewers | Live connector integration, real AHT/FCR/CSAT study | 14 tuần synthetic adapters + instrumentation; KPI business NOT VALIDATED nếu thiếu pilot |
| EXT-07 | Multimodal parsers / call transcripts / more channels | Deferred theo data need | M0.1; M6.9 | SRC-05 L1; SRC-02 §7.1 | Có nguồn được phép và acceptance cho modality cụ thể; HTML/text MVP đã đạt | Connector/parser schemas, permission and extraction quality report | Không tự thêm kiosk ASR/TTS từ research lịch sử vào core |
| EXT-08 | Dedicated annotation platform / large-scale active learning | Deferred sau W14 | M7.1–M7.2 | SRC-02 §10.5,7.10; SRC-07 | Annotation volume/multiple reviewers làm UI hiện tại thiếu; core approval/export đã ổn | Argilla/alternative ADR và migration có evidence | Core giữ workspace/approval/export và một retrain cycle; không bắt cài mọi tool được tham khảo |

## 10. Tải công việc và quy tắc theo dõi

| Tuần | Từ | Đến | Người | Core | Buffer | Nghỉ | Tổng slots | Tasks | Kiểm tải |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W1 | 26/10/2026 | 30/10/2026 | Trần Đình Khương | 4.0 | 1.0 | 0 | 5 | M0.1, M0.2, M0.3, M0.4, M0.G, M0.B | PASS — không chồng lịch |
| W2 | 02/11/2026 | 06/11/2026 | Trần Đình Khương | 4.0 | 1.0 | 0 | 5 | M1.1, M1.2, M1.3, M1.4, M1.G, M1.B | PASS — không chồng lịch |
| W3 | 09/11/2026 | 13/11/2026 | Trần Đình Khương | 5.0 | 0.0 | 0 | 5 | M2.1, M2.2, M2.3, M2.4, M2.5 | PASS — không chồng lịch |
| W4 | 16/11/2026 | 20/11/2026 | Trần Đình Khương | 4.0 | 1.0 | 0 | 5 | M2.5, M2.6, M2.7, M2.8, M2.G, M2.B | PASS — không chồng lịch |
| W5 | 23/11/2026 | 27/11/2026 | Trần Đình Khương | 5.0 | 0.0 | 0 | 5 | M3.1, M3.2, M3.3, M3.4, M3.5 | PASS — không chồng lịch |
| W6 | 30/11/2026 | 04/12/2026 | Trần Đình Khương | 4.0 | 1.0 | 0 | 5 | M3.5, M3.6, M3.7, M3.8, M3.G, M3.B | PASS — không chồng lịch |
| W7 | 07/12/2026 | 11/12/2026 | Trần Đình Khương | 5.0 | 0.0 | 0 | 5 | M4.1, M4.2, M4.3, M4.4 | PASS — không chồng lịch |
| W8 | 14/12/2026 | 18/12/2026 | Trần Đình Khương | 4.0 | 1.0 | 0 | 5 | M4.5, M4.6, M4.7, M4.G, M4.B | PASS — không chồng lịch |
| W9 | 21/12/2026 | 25/12/2026 | Trần Đình Khương | 4.0 | 1.0 | 0 | 5 | M5.1, M5.2, M5.3, M5.4, M5.G, M5.B | PASS — không chồng lịch |
| W10 | 28/12/2026 | 01/01/2027 | Trần Đình Khương | 4.0 | 0.0 | 1.0 | 5 | M6.1, M6.2, M6.3, M6.4, M6.B | PASS — không chồng lịch |
| W11 | 04/01/2027 | 08/01/2027 | Trần Đình Khương | 5.0 | 0.0 | 0 | 5 | M6.5, M6.6, M6.7, M6.8, M6.9, M6.G | PASS — không chồng lịch |
| W12 | 11/01/2027 | 15/01/2027 | Trần Đình Khương | 4.0 | 1.0 | 0 | 5 | M7.1, M7.2, M7.3, M7.4, M7.5, M7.G, M7.B | PASS — không chồng lịch |
| W13 | 18/01/2027 | 22/01/2027 | Trần Đình Khương | 5.0 | 0.0 | 0 | 5 | M8.1, M8.2, M8.3, M8.4, M8.5 | PASS — không chồng lịch |
| W14 | 25/01/2027 | 29/01/2027 | Trần Đình Khương | 3.0 | 2.0 | 0 | 5 | M8.6, M8.7, M8.8, M8.G, M8.B | PASS — không chồng lịch |

| ID | Chủ đề | Quy tắc |
| --- | --- | --- |
| N01 | Cách đọc | Cover → Milestones → Milestone Details → WBS/Task Details → Module/IO → Traceability/Gates. Source Register cung cấp nguồn và hash. |
| N02 | Một người | Tất cả task owner là Trần Đình Khương. Role chỉ là loại công việc đang làm, không phải người bổ sung. Không lấy tên nhóm QPAF sang dự án này. |
| N03 | Ngày và effort | Start 26/10/2026, W14 hết 31/01/2027, ngày làm việc cuối 29/01. Đơn vị 0,5 ngày/4h; buổi bắt đầu AM/PM trong Task Details. WBS chỉ hiển thị ngày; xem slots/capacity để tránh hiểu task cùng ngày là chồng lịch. |
| N04 | Capacity và nghỉ | 60 ngày core/gate + 9 ngày buffer + 1 ngày nghỉ dự kiến 01/01 = 70 ngày T2–T6. Chưa tính mọi ngày nghỉ cá nhân/nghỉ lễ phát sinh. Rebaseline khi nghỉ vượt buffer; ngày trong workbook là baseline cố định. |
| N05 | Dependency | Task core được xếp finish-to-start nối tiếp; giai đoạn sau chờ gate trước. Buffer là ngân sách lịch, không là task triển khai bắt buộc; M6.B nằm 01/01 trước gate M6 vì là ngày nghỉ. |
| N06 | Gates | PASS có đủ evidence; FAIL cần sửa; BLOCKED thiếu prerequisite; NOT RUN chưa chạy. Mỗi gate có review report/demo/manifest. Gate report phải ghi open scope và measured metrics. |
| N07 | Trạng thái duy nhất | Chỉnh Task Status tại WBS cột J; Milestones/Task Details lấy công thức tham chiếu. Tất cả core ban đầu Not Started; buffers Contingency; không tự nhận crawler cũ làm task mới Done. |
| N08 | Done | Chỉ đặt Done khi đạt Definition of Done và điền Evidence thực tế tại Task Details. Nếu task implementation xong nhưng target fail thì báo rõ gate FAIL; không coi code tồn tại là story đã nghiệm thu. |
| N09 | Không mở rộng scope trong buffer | Buffer dùng sửa lỗi/verification/nghỉ. Nếu không dùng, có thể rà soát thêm. Không tự lấp bằng global GraphRAG, Kubernetes HA hay nhiều candidate models. |
| N10 | Chatbot-first | M0 thiết kế; M1 knowledge; M2 chatbot demo cuối W4. Không cần đợi ABSA/Neo4j. Sau M3 có order/policy decision, M4 triage, M6 confirmed issue context. |
| N11 | Ngưỡng không phải thành tích | Targets F1/Recall/FRT/AHT/FCR trong docs chưa chứng minh repo đạt. Record sample_count, hardware, timestamps và test split. Synthetic replay không xác nhận business impact thật. |
| N12 | Scope levels | Core = bounded demo; Conditional = cần tài nguyên/quyền/budget/reviewer; Deferred = sau 14 tuần. Dòng conditional/deferred vẫn được trace, không lặng lẽ loại khỏi tài liệu. |
| N13 | Cloud và production | Compose demo bắt buộc. Minimal IaC package là core M8. Live EKS/prod cần prerequisite và người duyệt thật; nếu không đủ, ghi BLOCKED/NOT_RUN và để mở gate production. |
| N14 | Reviewer | Một developer có thể test các role bằng accounts riêng. Điều đó không thay độc lập đánh giá hoặc xác nhận chính sách của doanh nghiệp. Sự chấp thuận production/live actions cần chủ thể được ủy quyền. |
| N15 | Data privacy | Không raw customer PII trong vector/prompt/log; policy effective date unknown phải duyệt. Không biến công việc kỹ thuật thành tuyên bố tuân thủ pháp lý. |
| N16 | Sử dụng mẫu | Giữ 5 sheet chính, task/start/end/responsibility/deliverable/status/Gantt. Thay lịch 16→14 tuần, owner nhóm→1 người; bổ sung 11 sheet cho I/O/module/gates/data/tech/decision/capacity. Không giữ dữ liệu/trạng thái nghiên cứu QPAF. |
| N17 | Phạm vi công việc lượt này | Chỉ tạo kế hoạch XLSX/Markdown; không triển khai chatbot, train model, chạy cloud, gọi LLM production hay sửa API. Verification hiện tại kiểm tính toàn vẹn của kế hoạch/workbook. |
| N18 | Đồng bộ tài liệu | Markdown là bản đọc tại baseline; WBS Excel là nơi theo dõi tiến độ sau bàn giao. Khi đổi scope/deadline/effort, cập nhật cả milestone details, traceability, gates và capacity; không chỉ đổi ngày trên Cover. |

## 11. Nguồn đã đối chiếu

Repo snapshot đọc: `9083135`. Nội dung tài liệu được snapshot bằng SHA-256 trong workbook. Các tài liệu lịch sử được nhắc nhưng không có file tại repo được ghi rõ ở Source Register; không suy diễn rằng đã đọc chúng.

- **SRC-01 — [README và repo layout](../../README.md)**: Executive summary; architecture; API layout; setup. Mapping: M0.1; M0.3; M8.8. Current project overview; claims production phải kiểm code/evidence.
- **SRC-02 — [Final project tiếng Việt](../architecture/Final_project_rewritten.md)**: §0–4 product/personas; §5–9 architecture/modules/data/API; §10 research; §11–12 changes/layout; §13–17 eval/governance/ops; §18–24 roadmap/scenario/risks/DoD/narrative/sources. Mapping: M0–M8; all acceptance IDs; Extensions. Nguồn bao quát nhất; old referenced Bai_Toan_Dat_Ra/Final_project(3) không tìm thấy trong repo hiện tại.
- **SRC-03 — [Product user stories](../product/user-stories.md)**: US-BUY-01, US-AGENT-01, US-ANALYST-01, US-PM-01. Mapping: M2–M8. Outcome numbers là targets; FRT khác acceptance cần DEC-03.
- **SRC-04 — [Product acceptance](../product/acceptance-criteria.md)**: Buyer/Agent/Analyst/PM readiness. Mapping: G2–G8; Q-02..18. Tiêu chí dùng nghiệm thu, không là số đo repo.
- **SRC-05 — [Architecture blueprint](../architecture/ARCHITECTURE.md)**: §0–4 purpose/story/traceability; §5 7-layer/memory/2 pipelines; §6–10 modules/security/APIs/metrics/roadmap. Mapping: ARCH-L1..L7; M0–M8. Có US-STEWARD-01 và production targets; chatbot-first đổi thứ tự, giữ coverage.
- **SRC-06 — [Production data specification](../reports/production-data-specification.md)**: §1 storage; §2 PII/router; §3 ABSA; §4 retrieval; §5 graph/policy/CRM; §6 resolution; §7 feedback; §8 data checklist. Mapping: Data Plan; IO-03..15; M1/M3/M4/M6/M7. Counts/splits/model/quota minh họa cần verify, không copy làm kết quả/thông số runtime đã đo.
- **SRC-07 — [Deep research report](../reports/deep-research-report.md)**: ABSA/Retrieval AC; baseline-first; NFR/governance; doc template/roadmap. Mapping: ABSA-AC-01..10; RET-AC-01..12; M0/M4/M8. Historical context; kiosk/old API/missing docs không override current product. Numerical thresholds marked assumptions.
- **SRC-08 — [Ontology schema](../ontology/ontology-schema.md)**: Nodes, edges, traversal pattern. Mapping: M6.1–M6.3; DEC-06. Schema rút gọn phải reconcile với Issue/Firmware/Evidence/Team trong blueprint.
- **SRC-09 — [Capability map](../product/capability-map.md)**: Quantitative/qualitative/actionable/learning; module invariants. Mapping: Module Catalog; ARCH-BOUNDARY. Giữ ranh giới ABSA/retrieval/graph/policy.
- **SRC-10 — [Crawler README](../../Data_crawling/README.md)**: Discovery/scrape exports; raw captures; isolation. Mapping: M1.1–M1.2. Chỉ raw data; navigation/footer chưa clean; adapter file boundary.
- **SRC-11 — [Crawler design](../../Data_crawling/docs/design.md)**: Scope, URL handling, workflow, limits. Mapping: M1.1; DATA-01. Không mở scope crawler trong plan này.
- **SRC-12 — [Crawler implementation plan](../../Data_crawling/docs/implementation-plan.md)**: Standalone boundaries; implementation/verification history. Mapping: M0.1; M1.1. Historical completed crawl work; không gán Done cho new ingestion pipeline.
- **SRC-13 — [Crawler verification](../../Data_crawling/docs/verification.md)**: 26/34 tests; 56 attempted/52 success/4 fail historical batch. Mapping: M0.1; M1.1; DATA-01. Evidence lịch sử 19–20/10/2026, không phải rerun của lượt lập kế hoạch này.
- **SRC-14A — [Agent workspace scope](../../apps/agent_workspace/README.md)**: Triage/context/draft/actions/feedback. Mapping: M3.5; M4.7; M6.4; M7.1. README target; app code còn khung.
- **SRC-14B — [Analyst dashboard scope](../../apps/analyst_dashboard/README.md)**: Macro BI; drill-down; graph explorer; contribution. Mapping: M5; M6.5. README target; app code còn khung.
- **SRC-14C — [Worker scope](../../apps/worker/README.md)**: Consumers/jobs/alerts/active learning. Mapping: M4.5; M5.1; M7.2–M7.3. Chốt queue tại DEC-08.
- **SRC-15 — [Artifact conventions](../../artifacts/README.md)**: Versioned S3/local artifacts; immutable manifest; no large binaries in Git. Mapping: M4.3; M8.1; M8.8. Workbook planning không phải model checkpoint; model weights/index ngoài Git.
- **SRC-16A — [Current API implementation](../../apps/api/app/main.py)**: Mock handlers; readiness static; legacy endpoints. Mapping: M0.1; M2.5; M3.4; M4.5; M8.3. Chỉ kiểm đọc mã, không claim API đáp ứng user story.
- **SRC-16B — [Current data contracts](../../packages/data_contracts/__init__.py)**: FeedbackRecord/AspectSentiment/Investigation/Resolution/Feedback schemas. Mapping: M0.3; IO Contracts. Cần chat schema, policy URL/version, rich filters, typed feedback.
- **SRC-16C — [Dependencies](../../pyproject.toml)**: Python range/dependencies/test tooling. Mapping: M0.3; Tech Stack. Chọn/pin model/library tại implementation; không claim versions mới nhất.
- **SRC-16D — [Compose infrastructure](../../infra/compose/docker-compose.yml)**: Target local services. Mapping: M0.4; M2.7; M8.3. Cấu hình hiện hữu cần smoke/review trước dùng.
- **SRC-17 — [Excel template supplied by user](https://github.com/khuonglaptri3/qpaf-visual-document-retrieval/blob/feature/m3-6-integrity-review/docs/GUILDLINE_OVERVIEWS_PROPOSAL/POAI_Milestone_Group01_Hoan_Chinh.xlsx)**: Cover Page; WBS; Milestones; Proposal Traceability; Notes; dates/status/deliverable/Gantt. Mapping: Workbook structure and traceability design. Adapt 16-week/3-member research template → 14-week/1-person SenticRAG; no borrowed completion statuses.
- **WEB-01 — [FastAPI official docs](https://fastapi.tiangolo.com/)**: API/backend reference. Mapping: TECH-01. Checked 23/10/2026; implementation versions remain pinned by project.
- **WEB-02 — [Qdrant Hybrid Queries official docs](https://qdrant.tech/documentation/search/hybrid-queries/)**: Dense/sparse fusion reference. Mapping: TECH-06; M2.2. Referenced for design; no performance or quota claims inferred.
- **WEB-03 — [Neo4j constraints official docs](https://neo4j.com/docs/cypher-manual/current/schema/constraints/)**: Graph integrity reference. Mapping: TECH-11; M6.2. Edition/version support must be checked during implementation.
- **WEB-04 — [React TypeScript official docs](https://react.dev/learn/typescript)**: Typed frontend reference. Mapping: TECH-02. Frontend choice proposed, not existing implementation.

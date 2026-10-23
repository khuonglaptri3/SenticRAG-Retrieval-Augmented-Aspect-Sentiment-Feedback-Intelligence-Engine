# Rà soát kế hoạch SenticRAG với đặc tả kiến trúc — 23/10/2026

**Kết luận:** kế hoạch phù hợp làm baseline cho một demo tích hợp trong 14 tuần, sau khi sửa các thiếu sót về thứ tự triển khai, độ tin cậy và nghiệm thu. Chưa thể kết luận “đã đáp ứng đầy đủ kiến trúc” hoặc bảo đảm đủ effort: kiến trúc có các yêu cầu ATE, chất lượng, latency, IAM và production cần bằng chứng riêng. Kế hoạch có coverage không đồng nghĩa hệ thống đã triển khai.

Nguồn chính là [ARCHITECTURE.md](../architecture/ARCHITECTURE.md), đối chiếu với [bản đặc tả chi tiết](../architecture/Final_project_rewritten.md), [user stories](../product/user-stories.md), [acceptance criteria](../product/acceptance-criteria.md), [capability map](../product/capability-map.md), [ontology](../ontology/ontology-schema.md) và [research report](deep-research-report.md). Các thay đổi được đồng bộ vào [milestone Markdown](../planning/SenticRAG_Milestone.md), [Excel](../planning/SenticRAG_Milestone.xlsx) và [HTML](../planning/SenticRAG_Milestone.html).

Phạm vi audit là thiết kế/kế hoạch, không chạy benchmark, không nghiệm thu crawler hoặc 52 file chưa được người dùng duyệt. Giữ nguyên Data Plan, toàn bộ task M1 và lịch/effort baseline. Các nguồn kỹ thuật trên web dùng để kiểm cách triển khai, không thay yêu cầu sản phẩm.

## 1. Những phần đã đúng

| Yêu cầu gốc | Kế hoạch đáp ứng ở đâu | Đánh giá |
| --- | --- | --- |
| §1, §5.2: ABSA toàn corpus tách khỏi retrieval Top-K | M4.5, M5.1, MOD-07/09; Q-10 | Đúng. Accounting accepted/processed/pending/failed cần tách khỏi tỷ lệ đã inference thành công. |
| §5.3–5.4: bảy tầng, bốn loại memory | M1/M2 gateway; M3 orchestration/tools/context; M4 triage; M6 graph; M2/M7/M8 telemetry | Có mapping. Cần triển khai từng control trước khi tính năng sử dụng nó được mở. |
| §6.3: dense + BM25 + RRF + BGE | M2.1–M2.3, M5.3 | Có benchmark và adapter. BGE tắt vì quality/latency là một deviation phải ghi, không được tuyên bố topology hoàn toàn giống kiến trúc. |
| §6.4: graph vận hành nối version/symptom/cause/policy/resolution/service center | M6.1–M6.8 | Đúng; ontology có Issue/Evidence/Team theo bản đặc tả dài. |
| §6.5: policy-grounded draft, tools và guardrails | M3.2–M3.5; IO-06..09 | Đúng hướng; policy engine quyết eligibility, LLM chỉ diễn đạt. Bổ sung tiêu chí protocol MCP và từng loại guardrail. |
| §8: bốn API sản phẩm | IO-03/08/12/13 và các task tương ứng | Giữ API canonical `/api/v1`; thêm chat riêng là mở rộng tương thích, không ép policy Q&A phải có product. |
| §3–4: năm user stories, feedback và stewardship | M2/M3/M4/M5/M6/M7/M8 | Một ứng dụng UI không làm mất vai trò; Analyst và PM có thể cùng khu vực nhưng permission khác nhau. |
| §7, §9: IAM, AI metrics, business outcomes | M8; Q-01..18; DEC-03..05/11 | Có kế hoạch. Render IaC, demo pass hoặc synthetic KPI không chứng minh production. |

LangGraph không phải công nghệ bắt buộc trong ARCHITECTURE.md; tài liệu yêu cầu lifecycle FSM, planning, reflection và tools. Giữ LangGraph là lựa chọn có điều kiện ở M0 là hợp lý. PostgreSQL driver/migration và UI hợp nhất là chi tiết triển khai phù hợp ranh giới kiến trúc.

## 2. Các phát hiện và chỉnh sửa

| ID | Mức | Trước audit | Chỉnh sửa trong kế hoạch | Nguồn |
| --- | --- | --- | --- | --- |
| F-01 | Cao | Rate limit ở M4.6 trong khi chatbot gọi LLM từ M2 | Đưa sliding-window, token/request quota, 429 và Redis failure vào M2.5/G2; M4 chỉ mở rộng theo route | ARCHITECTURE §6.1; M2.5/M4.6 |
| F-02 | Cao | M4.5 “persist rồi queue” chưa định nghĩa lỗi giữa hai hệ thống | Commit record + outbox trong một SQL transaction; dispatch retry, consumer dedup, ack sau commit, reclaim pending và fault tests | ARCHITECTURE §5.2; Final project §7.1/8/15; suy luận kỹ thuật, không phải từ nguyên văn kiến trúc |
| F-03 | Cao | “Atomic publish” chưa nêu boundary giữa PostgreSQL, Qdrant và Neo4j | Snapshot có version, integrity checks, SQL active release pointer; mỗi request pin manifest; reconcile/rollback và kiểm stale policy trước action | Final project §8.2/15/20; M6.6/M6.7 |
| F-04 | Cao | Q-09 chưa giữ rõ target ATE .85; demo .80 dễ bị hiểu là hoàn thành yêu cầu gốc | Tách demo/architecture-target; giữ .85 cho mục tiêu kiến trúc, ATE báo riêng; thiếu span labels/test = NOT VALIDATED | ARCHITECTURE §6.2/9.1; acceptance Agent readiness; research ABSA-AC-05 |
| F-05 | Cao | Cách diễn đạt “stage budget <2s” chưa rõ có đo toàn Pipeline B không | Q-16/M8.4 đo đến output đã qua guardrails, gồm mọi stage route sử dụng; TTFT/full response/chờ approval báo riêng | ARCHITECTURE §5.2; user stories <30s; acceptance <60s |
| F-06 | Vừa | M3.4 mới nêu “MCP adapter”; gọi hàm nội bộ cũng có thể bị tính là hoàn tất MCP | Thêm client/server local, transport/version pin, `tools/list` và `tools/call` cho ba tool canonical; test lỗi/permission/schema | ARCHITECTURE §6.5 |
| F-07 | Vừa | Planning engine và episodic/procedural memory có trong module mapping nhưng task chưa cụ thể | Typed plan nguồn/tool/missing fields/stop condition; customer history có quyền; versioned playbooks; Triaged nối ABSA ở M4 | ARCHITECTURE §5.4/6.5; Final project §7.9 |
| F-08 | Vừa | Citation/schema có tiêu chí nhưng từng guardrail chưa tách rõ ở M2 | Tách claim verification, schema validation, policy compliance, output PII filter; JSON valid không thay evidence entailment | ARCHITECTURE §5.3/6.5; Final project §7.9 |
| F-09 | Vừa | M8.2 có OIDC/per-service identity nhưng chưa ghi cụ thể quyền và node-role isolation | Builder chỉ push ECR, deployment roles riêng, API/training quyền S3 khác nhau, IMDS isolation, securityContext; live checks riêng | ARCHITECTURE §7.1–7.3 |
| F-10 | Vừa | Source Register trỏ một số file không có trên nhánh hiện tại; hash hai đặc tả khác working tree | Đọc lại SRC-02/05, cập nhật hash; SRC-06/10..13 ghi `git:9083135:<path>` và xác minh blob | Source Register; working tree `eb194ff` |
| F-11 | Nhỏ | IO-01 khai báo UUID nhưng ví dụ dùng `conv-demo-01`; DEC-15..17 bị tách khỏi bảng Markdown | Sửa UUID hợp lệ; gộp bảng Decisions; render HTML đầy đủ từ Markdown và kiểm đồng bộ | IO-01; artifacts planning |
| F-12 | Vừa | G0 viết như đã bảo đảm “một người/14 tuần khả thi” | Đổi thành feasibility cần kiểm bằng smoke và effort review; ghi rõ các task chặt, không tự tăng người hoặc hạ gate | Task Details; Capacity; DEC-01/02 |

Các phát hiện F-02/F-03 là bổ sung thiết kế để thực hiện các yêu cầu durability/replay/versioning, không phải khẳng định đã có lỗi runtime: repo đang ở giai đoạn scaffold.

## 3. Những khác biệt có chủ đích, không cần sửa thành giống nguyên văn

- **Roadmap:** ARCHITECTURE §10 có 12 tuần, bắt đầu từ quantitative core; kế hoạch hiện là 14 tuần, chatbot trước theo yêu cầu người dùng. Giữ thứ tự mới nhưng M2 chỉ nghiệm thu policy Q&A; Buyer story đầy đủ cần M3 context, M4 triage và M6 graph.
- **UI:** các đường dẫn `apps/analyst_dashboard`/`apps/agent_workspace` trong tài liệu nguồn là module giao diện mục tiêu. DEC-16 hợp nhất vào `apps/web`, vẫn giữ chức năng và kiểm quyền của năm personas; đây là thay đổi packaging được ghi nhận.
- **Ontology:** tài liệu rút gọn đặt RootCause ở trung tâm; bản dài bổ sung Issue/Firmware/Evidence/Team. DEC-06 chọn ontology mở rộng và tách lifecycle issue/cause. “Zero cyclic graph errors” được hiểu là không vi phạm invariant quan hệ, không phải cấm mọi chu trình của graph.
- **Hybrid/rerank:** có thực nghiệm dense-only/BM25-only/hybrid và BGE theo yêu cầu; việc chưa bật BGE có thể phù hợp demo sau benchmark, nhưng topology chuẩn của §6.3 vẫn được ghi là chưa đáp ứng trọn vẹn.
- **Cloud:** Compose demo bắt buộc; live EKS, IAM runtime, production reviewer và real CRM phụ thuộc quyền/tài nguyên. Thiếu chúng là OPEN/BLOCKED/NOT RUN cho phần tương ứng, không thành PASS từ local smoke.
- **LangGraph:** việc có hay không có framework không tự quyết định tuân thủ kiến trúc. Cần cùng bằng chứng state persistence, bounded reflection, approval/resume và idempotency; không triển khai hai orchestrator.

## 4. Khóa cách nghiệm thu để không đánh tráo mục tiêu

| Hạng mục | Demo baseline | Architecture / product target | Chưa có evidence thì ghi |
| --- | --- | --- | --- |
| ABSA classification/polarity | .80, critical aspect .75 chỉ khi profile demo khóa G0 | Macro-F1 ≥.85; định nghĩa class/aspect averaging rõ | NOT RUN hoặc FAIL theo kết quả |
| ATE | Span chỉ hiện khi model/labels hỗ trợ | F1 ≥.85 theo §9.1; khóa exact/partial span matching và averaging | Thiếu span test: NOT VALIDATED; không đạt full ABSA architecture |
| Pipeline B | Demo response <60s; <30s stretch theo DEC-03 | <2s đến guarded output, mọi stage route dùng; không đổi thành TTFT | Không đo: NOT RUN; vượt: FAIL architecture-target |
| Retrieval | M2 tập policy nhỏ, M5/M6 bổ sung review/graph | Recall@5 ≥.88, MRR ≥.82; các ngưỡng research bổ sung báo riêng | Không suy chất lượng toàn corpus từ một slice |
| Guardrails | Critical suite không có unsupported policy/refund commitment | Citation completeness ≥95%, generic unsupported-action ≤1%; critical promises vẫn zero | Không coi thêm metadata/URL hoặc schema pass là grounded |
| Business | Chứng minh event/formula/lineage | AHT giảm ≥40%, FCR cải thiện ≥15%, draft accept ≥80% cần pilot và baseline | NOT VALIDATED nếu chỉ synthetic/self-run |

§9.1 chưa định nghĩa thật rõ cách averaging F1 cho ATE; kế hoạch giữ mục tiêu .85 và yêu cầu khóa phép đo, không tự coi category classification là extraction. <2s cũng cần khóa request boundary/concurrency/cold-warm tại G0; report phải giữ cả target gốc và phép đo đã dùng.

## 5. Đánh giá lịch và rủi ro effort

Kiểm tra workbook theo slot nửa ngày cho thấy **75 task**, **55,5 ngày core + 4,5 ngày gate + 9 ngày buffer + 1 ngày nghỉ dự kiến = 70 ngày làm việc**. Không có slot trùng, end date khớp effort và không có dependency finish-to-start bị vi phạm. Đây chỉ là kiểm tra số học lịch.

Các timebox rủi ro là M0.4 (1 ngày: nền app/DB/contracts), M3.4 (1,5 ngày: orchestration + persistence + MCP), M4.5 (1,5 ngày: worker/ingestion/outbox/index), M6.7 (1 ngày: publication/recovery) và M8.2 (1 ngày: Helm/Terraform/IAM package). Một web app giảm phần việc trùng lặp nhưng chưa có số đo tiết kiệm thời gian. Bổ sung tiêu chí làm rõ khối lượng cần làm, không tự làm effort nhỏ đi.

G0 cần kiểm smoke tối thiểu và tách rõ việc có thể tái dùng. Vượt timebox thì ghi sử dụng buffer hoặc rebaseline; không bỏ lỗi, hạ metric hoặc ghi Done vì đến deadline. Giữ nguyên baseline 14 tuần trong lượt audit này, không cam kết đủ thời gian huấn luyện ATE hoặc live production nếu prerequisite chưa có.

## 6. Tính đúng của nguồn

- Kế hoạch cũ snapshot tại `9083135`; working tree audit hiện tại trên `develop`, HEAD `eb194ff`, gồm các chỉnh planning chưa commit.
- Nội dung SRC-02 (`Final_project_rewritten.md`) và SRC-05 (`ARCHITECTURE.md`) hiện có hash khác snapshot cũ; đọc bản hiện tại và cập nhật Source Register.
- SRC-06 (`production-data-specification.md`) và SRC-10..13 (README/design/implementation/verification crawler) không có trong checkout. Tất cả tìm được bằng `git show 9083135:<path>`, hash khớp Source Register cũ. SRC-06 được đọc ở bản lịch sử để kiểm nguồn; các blob crawler chỉ xác minh provenance, không đánh giá chất lượng data.
- Các đề cập SRC-06/10..13 trong plan là tham chiếu lịch sử có thể truy xuất, không là bằng chứng những file đang có trên develop. Không khôi phục hoặc sửa crawler/data trong audit này.
- 52 file vẫn **chưa được người dùng duyệt**. Output “đã duyệt” trong milestone M1 mô tả điều kiện bàn giao tương lai, không phải trạng thái hiện tại.

## 7. Đối chiếu kỹ thuật bằng nguồn chính thức

- Cách outbox xử lý dual-write giữa DB và message broker, cùng yêu cầu consumer idempotency, đối chiếu với [AWS transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html). Thiết kế SQL outbox + Redis cụ thể là đề xuất cho repo này, không yêu cầu dùng dịch vụ AWS.
- MCP là giao thức có discovery/call và schema, nên bằng chứng cần bao gồm protocol interaction; xem [MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools). SDK/protocol version khóa theo phiên bản được triển khai, không dùng nhãn “latest” làm dependency pin.
- LangGraph cần checkpointer/thread identity cho interrupt/resume và có thể chạy lại node chứa side effects; xem [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts). Vì vậy dùng framework không thay kiểm quyền hoặc action idempotency.
- Filtering trên array cần giữ điều kiện aspect/sentiment trong cùng phần tử; đối chiếu [Qdrant nested filtering](https://qdrant.tech/documentation/search/filtering/). Plan M5.3 đã có test battery-positive/delivery-negative nên không cần thêm scope riêng.
- Quyền workload riêng không đồng nghĩa tự chặn mọi đường lấy node credentials; đối chiếu [AWS EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html). Plan cần kiểm IMDS và phân biệt render manifest với runtime enforcement.
- BGE có lựa chọn reranker multilingual, nhưng model card không chứng minh gain/latency trên corpus của dự án; xem [BAAI bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3). Giữ benchmark tiếng Việt tại M2.3 và không tự khóa model từ mô tả chung.

## 8. Kiểm tra artifacts sau sửa

Kết quả kiểm tra artifacts: PASS cho 70 trường thay đổi đồng bộ MD/XLSX/HTML, 10 bảng HTML có số cột nhất quán, 21 quyết định trong cùng bảng và 15 JSON examples parse hợp lệ (IO-01 dùng UUID hợp lệ). Giữ nguyên 102 công thức Excel, lịch/effort/dependencies/owners/status/evidence của 75 task; không có overlap hoặc vi phạm thứ tự dependency. Data Plan, nội dung M1 và trạng thái gates/traceability không đổi. Các hash nguồn local/historical đều khớp; `git diff --check` không báo lỗi.

Không chạy test ứng dụng vì lượt này chỉ sửa tài liệu. Báo cáo này không phải chứng nhận đạt gate G0–G8 hoặc kết quả benchmark AI.

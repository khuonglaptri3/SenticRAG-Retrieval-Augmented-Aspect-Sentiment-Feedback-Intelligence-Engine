# Danh mục nguồn dữ liệu cần cho SenticRAG

Ngày tổng hợp: 02/10/2026. Căn cứ: [Final_project_rewritten.md](Final_project_rewritten.md) và [ARCHITECTURE.md](ARCHITECTURE.md). Phạm vi: toàn bộ target architecture, không chỉ training ABSA.

Không cần mọi nguồn ngay ở Phase 1. Dữ liệu đầu vào nghiệp vụ cần thu thập; nhãn và bộ đánh giá cần xây dựng; prediction/index/log/feedback được tạo dần trong quá trình phát triển và vận hành. Qdrant, Neo4j, PostgreSQL, Redis là nơi lưu hoặc xử lý dữ liệu, không phải nguồn tri thức độc lập.

Các trường bên dưới là checklist tối thiểu để hiện thực hóa capability, tổng hợp từ fields, ontology và user stories. Hai tài liệu chưa định nghĩa đầy đủ contract cho mọi nguồn. Những mẫu kiểm thử chi tiết là đề xuất suy ra từ yêu cầu evaluation, không phải tên dataset đã được tài liệu chỉ định.

## 1. Nguồn nghiệp vụ phải thu thập hoặc kết nối

| ID | Nguồn dữ liệu | Nội dung cần có | Nguồn gốc / đơn vị cung cấp | Capability / thời điểm cần |
| --- | --- | --- | --- | --- |
| S01 | Review và phản hồi sản phẩm | source_record_id, text, created_at, language, channel, product_id; rating và version nếu có | Marketplace, website bán hàng, nguồn review công khai hoặc doanh nghiệp | ABSA, BI, review retrieval; Phase 1 |
| S02 | Ticket/khiếu nại CSKH | ticket_id, issue_text, customer_ref, product/order references, timestamps, trạng thái, mức ưu tiên nếu có | Hệ thống helpdesk/CSKH | Triage, case retrieval, resolution; trước US-BUY/AGENT |
| S03 | Lịch sử tương tác/hội thoại | conversation/session/ticket ID, thứ tự lượt, vai trò người nói, nội dung, thời gian | Chat/support system; bản chép cuộc gọi khi có phạm vi sử dụng phù hợp | Multi-turn memory và phân tích tương tác; theo kênh được chọn. Audio/video thô không là yêu cầu bắt buộc |
| S04 | Hồ sơ khách hàng và liên kết định danh | customer_ref, liên kết tài khoản/đơn hàng, thông tin liên hệ hoặc vùng phục vụ tối thiểu theo nhiệm vụ | CRM, tài khoản commerce | Customer context, ownership verification; trước personalized resolution |
| S05 | Đơn hàng, mua hàng và bảo hành | order_id, customer/product ID, purchase_date, serial/device reference khi cần, trạng thái mua hàng/bảo hành/đổi trả | Commerce, ERP, CRM, hệ thống warranty | Eligibility và lịch sử mua hàng; trước cam kết quyền lợi |
| S06 | Danh mục sản phẩm | product_id, tên, family/category, SKU và aliases để nối review/ticket về đúng sản phẩm | Product master/ERP/catalog chính thức | Product filters, BI, entity linking; Phase 1 theo phạm vi sản phẩm |
| S07 | Registry hardware/firmware/software | version_id, hardware revision, firmware version, release_date/status, mapping về product; affected/fixed versions khi được xác nhận | Product/engineering/release registry | Version cohorts, known-issue matching; trước chức năng phân tích theo version |
| S08 | Policy và rule chính thức | văn bản gốc, policy_id, version, clause/rule ID, effective_from/to, jurisdiction, product_scope, conditions, allowed_actions, approval | Bộ phận quản lý policy/warranty/CSKH | Policy retrieval, deterministic eligibility, citations; Phase 3 |
| S09 | Manuals và tài liệu kỹ thuật | hướng dẫn sử dụng, troubleshooting, error codes, maintenance/repair guidance, phạm vi product/version và source locator | Nhà sản xuất, đội kỹ thuật/knowledge base | Grounded technical guidance, evidence; khi triển khai hỗ trợ kỹ thuật |
| S10 | Known issues, triệu chứng và root causes có bằng chứng | issue/cause/symptom IDs, status, severity, affected versions, evidence IDs, xác nhận chuyên môn và thời gian cập nhật | Incident/bug registry, đội sản phẩm/kỹ thuật, analyst findings đã duyệt | Knowledge Graph, root-cause investigation; Phase 3. Review tự nó không xác nhận quan hệ nhân quả |
| S11 | Resolution và playbook đã phê duyệt | resolution_id, instructions, action type, approval status, applicable issues/versions, policy/rule links, escalation/approval rubric | CSKH, đội kỹ thuật, vận hành | Resolution Engine, procedural memory, draft/actions; Phase 3 |
| S12 | Danh bạ trung tâm bảo hành/dịch vụ | center_id, region, địa chỉ/liên hệ cần cho routing, capabilities và phạm vi sản phẩm được phục vụ | Mạng lưới dịch vụ chính thức | Service-center routing; khi hỗ trợ booking/repair dispatch |
| S13 | Teams, ownership và tuyến escalation | team_id, responsibility, issue ownership, routing destination, quyền duyệt và vai trò | Cơ cấu CSKH/kỹ thuật và hệ thống IAM/workflow | Specialist handoff, knowledge approval, ownership; trước escalation/publishing |

Căn cứ: bản đầy đủ §§7.1–7.2, 7.6–7.9, 8.1–8.2, user stories §§3.1–3.5 và memory §5.4; bản rút gọn §§5.4, 6.4–6.5, 8.

Một record có thể phục vụ nhiều nguồn/capability: ticket vừa là input triage vừa là evidence retrieval. Không cần biến từng dòng thành một database riêng. S05 tách khỏi S04 vì dữ liệu mua hàng và identity có authority khác nhau; S08 phải tách khỏi review/LLM-generated text vì là căn cứ quyền lợi.

## 2. Dữ liệu cấu hình, nhãn và bộ đánh giá phải xây dựng

| ID | Bộ dữ liệu / cấu hình | Nội dung cần có | Cách có / vai trò |
| --- | --- | --- | --- |
| D01 | Taxonomy aspect, mapping và annotation guideline | aspect/category IDs, definitions, synonyms, hierarchy nếu dùng, mapping nguồn, taxonomy_version; polarity và quy tắc mixed/no-aspect | Chuyên gia domain chuẩn hóa từ nhãn UIT/Shopee và phạm vi sản phẩm; cần trước training/BI |
| D02 | Ontology và lifecycle schema | node/edge definitions, stable IDs, allowed relations/statuses, approval rules, schema_version | Nhóm phát triển và knowledge steward; cần trước graph ingestion; thống nhất các ontology đang khác nhau trong hai tài liệu |
| D03 | ABSA supervised train/dev/test | text và gold aspect–sentiment tuples/categories, split, source ID, label provenance, guideline/version | UIT-ViSFD, Shopee Gold, annotation bổ sung; cần Phase 1. Không cần train LLM từ đầu để dùng dữ liệu này |
| D04 | Aspect-term/opinion span labels; ASTE/ACOS nếu chọn | term/opinion spans với offsets đúng, category/sentiment và liên kết tuple | Annotate thêm nếu implement ATE/ASTE/ACOS; category-only data không đủ; ASTE/ACOS là optional trong tài liệu |
| D05 | Entity/routing labels nếu train các classifier tương ứng | product/version/error-code/symptom entities; review vs ticket vs out-of-scope, urgency nếu dùng | Curated examples để train/evaluate extractor/router; không bắt buộc một corpus train riêng nếu dùng rules/model sẵn, nhưng cần tập kiểm chứng behavior |
| D06 | Retrieval evaluation queries và relevance judgments | query_id, query, cohort/metadata filters, doc IDs, relevance grade/qrels, dev/test | Analyst/chuyên gia gán relevance cho corpus; Phase 2. Đây là dữ liệu evaluate, chỉ dùng train reranker/embedding nếu chủ động chọn fine-tuning và có train split riêng |
| D07 | Graph/knowledge validation fixtures | node/edge/path đúng, schema-invalid/duplicate/orphan cases, confirmed vs hypothesis, scope/evidence/policy links | Từ ontology và tri thức S10 đã duyệt; kiểm tra traversal, evidence và publication |
| D08 | Policy/eligibility/resolution test cases | ticket+customer/order context, policy version, allowed/blocked actions, missing fields, expected escalation | Policy owner/CSKH tạo đáp án chuẩn; trước bật draft/actions. Các boundary cases như hết hạn/đúng sai scope là đề xuất kiểm thử |
| D09 | Grounded draft/citation evaluation cases | context+evidence pack, claims/citations/actions đúng, unsupported claims, expected abstention/human review và rubric | Chuyên gia chấm draft; evaluate generation/guardrails. Không nhất thiết cần một câu trả lời duy nhất cho mỗi tình huống |
| D10 | Privacy/access-control và workflow regression fixtures | PII mẫu, masked expectations, caller roles/ownership, cross-customer cases, approval/state transition expectations | Bộ kiểm thử tự xây theo boundaries; ưu tiên dữ liệu giả lập cho tình huống kiểm thử |
| D11 | Retention, access, approval và provenance configuration | ai được đọc/sửa/duyệt, purpose, category retention, deletion/correction workflow, author/source/version records | Chủ dữ liệu và quản trị hệ thống; không phải training dataset |
| D12 | Smoke/load/failure scenarios | payload đại diện, sizes, concurrency mix, timeout/dependency-failure cases và expected behavior | Từ user stories và workload dự kiến; cần trước tuyên bố SLO/deployment readiness |

Căn cứ: §§7.3, 7.9–7.10, 13, 14.2, 16, 17, 21 và ARCHITECTURE §§6.1–6.2, 9. Đây là các tập cần để đạt/kiểm tra capability, không phải 12 bộ dữ liệu bên ngoài phải download.

## 3. Dữ liệu được hệ thống sinh và cần lưu

| ID | Dữ liệu | Thành phần sinh / nơi authoritative | Công dụng |
| --- | --- | --- | --- |
| R01 | Ingest events và quality/processing status | Connectors, durable ingestion store | Dedup, replay, source lineage, coverage/freshness |
| R02 | ABSA predictions, entity mentions, issue assignments | Versioned prediction/assignment tables | SQL aggregations, index enrichment, model comparison; gồm model/taxonomy/inference versions |
| R03 | BI aggregates và anomaly/cohort context | Aggregation/analytics engine từ toàn corpus đủ điều kiện | Count/denominator/time window/filter snapshot để truy nguyên trend |
| R04 | Retrieval corpus/chunks, embeddings, sparse index, graph projections | Pipeline từ S01/S02/S08/S09/S10/S11 và nhãn/ontology phù hợp | Qdrant/BM25/Neo4j; cần source locator, filters, index/graph version; không phải nguồn gold mới |
| R05 | Retrieval sessions/results và evidence packs | Retrieval/orchestration | Query/filters/scores/doc IDs/paths/timestamps/version; kiểm chứng và citations |
| R06 | LLM generations, draft versions, citations và final replies | Generation log; final reply thuộc support system | Claim/evidence lineage, prompt/model version, so sánh draft với lời đáp đã gửi |
| R07 | Feedback và knowledge change requests | Analyst/agent/knowledge steward | Sửa ABSA, relevance, root cause, stale policy, new/duplicate issue; proposed→reviewed→approved/rejected→published |
| R08 | Ticket actions, approvals và resolution outcomes | Support workflow và phản hồi khách hàng | Resolved/reopened, timestamps, actions, CSAT; tính FRT/AHT/MTTR/FCR/recurrence và tạo learning signals |
| R09 | Traces, metrics, token/cost và audit logs | Application/worker/observability, IAM/workflow | Ai truy cập/duyệt gì, model/index/graph/policy/prompt versions, latency/cost và drift |

Căn cứ: §§7.4, 7.10, 8, 13.5, 14.2, 15.3 và ARCHITECTURE Layer 7. R07/R08 do con người cung cấp trong quá trình dùng sản phẩm; cần thiết kế việc thu nhận từ đầu nhưng không cần đầy đủ lịch sử trước khi bắt đầu phát triển.

## 4. Đối chiếu với data hiện có

Tham chiếu dữ liệu tại `C:/Users/lanph/Downloads/data`, theo kết quả kiểm tra trong phiên này. Không coi sự có mặt của một file là bằng chứng đã đáp ứng đầy đủ protocol của dự án.

| Hiện có | Đáp ứng được | Giới hạn |
| --- | --- | --- |
| `processed/uit_visfd/{train,dev,test}.jsonl` | D03, baseline review điện thoại; nguồn review cho thử nghiệm | 7.671/1.094/2.187 reviews; không có exact aspect-term gold; thiếu master product/customer/order để làm personalized resolution |
| `gold/absa/shopee_gold/` và `model_ready/` | D03, review nhiều domain; 21 aspect/63 tuple labels | 19.237/3.520/3.359 reviews; provenance ghi human-reviewed; không tự chứng minh mọi nhãn đúng. Một số evidence non-exact, nhãn hiếm và text overlap cần quản lý |
| Aspect schemas/label mappings | Khởi điểm cho D01 | Cần chốt canonical taxonomy giữa UIT/Shopee/SenticRAG; các schema hiện có chưa là ontology full project |
| `rag_support`, `gold/rag_support`, release retrieval artifacts | Có corpus, queries và qrels để xem xét D06/R04 | Chưa audit toàn bộ tính đúng của relevance labels, filters, provenance và leakage đối với protocol SenticRAG |
| `external`/`release` Shopee silver và nguồn thô | S01, augmentation có điều kiện | Không trộn mặc định vào train: train release cũ có 1.429 IDs nằm trong Shopee Gold dev/test; silver Gemini chứa cả holdout |

Chưa xác nhận có đủ S02–S13 cho doanh nghiệp mục tiêu: ticket/CRM/orders, product/firmware registry authoritative, policies, technical manuals, confirmed root causes, approved resolutions, service centers, escalation ownership. Shopee có một số metadata sản phẩm/shop nhưng không thay thế các nguồn authoritative đó.

## 5. Thứ tự chuẩn bị

1. **Phase 1 – ABSA/BI:** S01, S06 theo phạm vi chọn, D01, D03; ingestion/prediction/aggregate lineage R01–R03. Có thể bắt đầu từ UIT/Shopee hiện có. Không cam kết BI theo SKU/firmware nếu chưa có metadata tương ứng.
2. **Phase 2 – Investigation:** review/ticket corpus tùy use case, S07 nếu lọc version, D06 và retrieval/index lineage R04–R05. Tách corpus inference khỏi labels được phép dùng trong training/evaluation.
3. **Phase 3 – Knowledge/Resolution:** S02, S04–S13 theo workflow; D02, D07–D10, access controls và policy/context linking. Chat/call S03 chỉ cần khi triển khai kênh đó.
4. **Phase 4 – Learning/Outcome:** capture và approve R07/R08, cập nhật dataset/eval có version; không dùng correction chưa duyệt làm gold.
5. **Trước production:** D10–D12, R09, workload/SLO evidence, retention/access config và tests cho capability đã implement.

ABSA corpus không cung cấp quyền lợi bảo hành, nguyên nhân kỹ thuật đã xác nhận hoặc dữ liệu mua hàng. Các phần đó phải có nguồn authoritative riêng. Chứng minh với fixture giả lập được phép cho demo, nhưng fixture không chứng minh độ đúng trên doanh nghiệp thực tế.

## 6. Contract tối thiểu xuyên nguồn

- Giữ source/source_record_id, timestamps, language, product reference và schema version cho feedback; rating/customer/order/version là các trường tùy nguồn và nhiệm vụ như bản đầy đủ §7.1.
- Stable IDs nối review/ticket↔product/version↔issue/evidence↔policy/rule↔resolution↔outcome; không tự bịa mapping khi nguồn không có.
- Giữ aspect–sentiment theo cùng tuple/object, không hai mảng rời làm mất quan hệ.
- Nhãn train, dev, test có isolation theo protocol; giữ provenance/guideline/version. Không dùng held-out labels làm prompt exemplars hay training augmentation.
- Policy/confirmed root cause/resolution phải có version, status, người có quyền phê duyệt và bằng chứng nguồn.
- Analytics/index/prompt ngoài chỉ dùng dữ liệu tối thiểu đã xử lý PII; customer/order authoritative nằm sau authorization boundary.
- Mỗi quyết định có evidence locator/citation và các version cần thiết để audit/reproduce; nhận xét người dùng phải đi qua approval theo mục đích trước khi publish/train.

Hai tài liệu chưa chốt số lượng mẫu bắt buộc cho từng nguồn. Không suy ra rằng mọi nguồn phải có hàng chục nghìn record. Quy mô training và evaluation phải dựa trên số nhãn, class support, domain, workload và kết quả baseline.

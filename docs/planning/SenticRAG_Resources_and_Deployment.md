# SenticRAG — Tài nguyên, lưu trữ, triển khai và ngân sách

Đối chiếu repo và bảng giá chính thức ngày **23/10/2026**. Đây là phương án để lựa chọn, chưa mua dịch vụ, tạo tài khoản hay deploy; không thay quyết định provider/model ở M0. Giá bằng USD trừ khi nói khác, chưa cộng thuế/phí thanh toán hoặc các dịch vụ ngoài mục được báo. Xem [milestone](SenticRAG_Milestone.md) và [audit kiến trúc](../reports/planning-architecture-audit-2026-10-23.md).

**Đề xuất cập nhật:** local Compose cho phát triển; ưu tiên thử Modal Starter cho training/inference và public API ít tải trước khi thuê VPS. VPS phù hợp khi cần compute chạy liên tục hoặc gom các DB; EKS chỉ khi cần chứng minh deployment AWS và đã có ngân sách. Miễn phí phần mềm, free quota dịch vụ và trial/credits là ba điều khác nhau. Free storage không cấp luôn compute cho API/worker/model.

## 1. Nền tảng đang có và giả định sizing

Workspace hiện báo 4 logical CPU, RAM 16.222.476 KiB (~15,47 GiB), đĩa trống ~795,9 GiB. Không có `nvidia-smi`, nên **chưa xác nhận GPU**, không kết luận máy chắc chắn không có GPU. Nếu đây là VM/môi trường từ xa thì cấu hình này không đại diện máy cá nhân khác.

Sizing dưới đây là **ước lượng khởi đầu, chưa benchmark**: demo 1–3 người dùng đồng thời, corpus giả định không quá 10.000 review và 10.000 chunks, một phiên bản model được phục vụ tại một thời điểm, LLM gọi API. Những số này không xác nhận data hiện có, không duyệt 52 file và không đảm bảo SLO <2s.

| Giai đoạn | Cấu hình bắt đầu đề xuất | Đĩa dự trù | GPU |
| --- | --- | --- | --- |
| M0–M3: API/chat/policy retrieval | 4 CPU, 8–16 GiB RAM; chưa bật Neo4j khi chưa dùng | 30–60 GB cho images, DB, model cache, logs | Không bắt buộc nếu LLM dùng API; embedding/rerank CPU phải đo latency |
| M4–M7: ABSA/BI/graph/worker | 4–8 CPU, 16 GiB RAM; 32 GiB thoải mái hơn khi nhiều model cùng load | 80–120 GB gồm cache/checkpoints/snapshots | Inference nhỏ có thể thử CPU; train PhoBERT nên có GPU riêng |
| Training candidate | 1 GPU; khởi đầu 12–16 GB VRAM, 16–32 GB system RAM; batch/sequence length điều chỉnh theo model | 20–50 GB cho dataset/checkpoints/cache | Xác minh bằng smoke run, mixed precision/gradient accumulation nếu phù hợp |
| VPS public demo | 4 vCPU/8 GiB nếu tải nhẹ và tách bớt DB/model; 8 vCPU/16 GiB nếu gom stack | 80–160 GB trở lên, backup riêng | Không cần chạy GPU 24/7 nếu inference CPU đạt demo rubric |

Giữ headroom cho OS và Docker. Không nhân nhiều API workers khi mỗi worker load lại embedding/ABSA/reranker. Chạy batch/training tách khỏi request path; giới hạn log retention và số checkpoint giữ lại. Nếu CPU latency không đạt target, báo kết quả và cân nhắc GPU inference sau đo, không hạ ngầm gate.

## 2. Cần lưu gì, ở đâu

| Thành phần | Dữ liệu/trách nhiệm | Phương án local | Khi đưa lên cloud |
| --- | --- | --- | --- |
| PostgreSQL | Conversations, messages, policy registry, reviews, predictions, outbox, approvals, outcomes | Persistent Docker volume; SQL backups | Managed Postgres hoặc persistent disk trên VPS |
| Qdrant | Embeddings + metadata/source IDs, không làm source of truth | Volume riêng; index có thể rebuild từ manifest | Qdrant Cloud hoặc self-host trên VPS |
| Redis | Rate limit, cache, Streams queue | Giới hạn memory; persistence cho queue và SQL outbox replay | Trên cùng VPS trước; managed phải kiểm Streams/consumer/retry compatibility |
| Neo4j | Versioned graph/confirmed knowledge | Community container + volume; bật từ M6 | AuraDB hoặc self-host; kiểm edition/features/APOC được hỗ trợ |
| Files/object storage | Raw/clean snapshots, model checkpoint, eval report, backup | Filesystem ngoài Git, manifest/hash/version | Private object bucket, S3 hoặc R2 |
| API/worker/web | FastAPI, job dispatcher/consumer, React build | Docker Compose, một web app | Một VPS Compose hoặc Kubernetes theo resource gate |
| LLM | Sinh draft/answer từ evidence | API provider; model local là phương án khác cần sizing riêng | Token billing/quota, không phải chi phí lưu Qdrant |
| Observability | Logs/traces/metrics/cost | Retention ngắn, sampling phù hợp | Tính riêng log ingest/storage nếu dùng managed monitoring |

Dự trù khoảng 5–20 GB cho dữ liệu demo/DB/index và 20–50 GB cho images/model cache/checkpoints, cộng backup/headroom; đây là khoản phân bổ chứ không phải số đo corpus. Ví dụ 10.000 vector × 768 chiều × 4 byte ≈ 30,72 MB chỉ là **mảng vector thô**, chưa gồm HNSW, payload, indexes, replicas hay snapshots. Không dùng số này để khẳng định free cluster chứa được bao nhiêu dữ liệu thật.

Volume trên cùng một máy không phải backup độc lập. Cần ít nhất một bản export/backup ở vị trí khác và thử restore; object bucket lưu file không thay filesystem của PostgreSQL/Neo4j đang chạy.

## 3. Các gói free đã kiểm tra

| Dịch vụ | Free/quota được công bố lúc kiểm tra | Phù hợp với SenticRAG | Giới hạn cần tính vào kế hoạch |
| --- | --- | --- | --- |
| [Neon PostgreSQL](https://neon.com/pricing) | 1 GB/project, 100 CU-hours/project/tháng | Registry/history/demo DB nhỏ | Scale-to-zero; 100 CU-hours không phải 100 giờ wall-clock. 0,25 CU liên tục 730h ≈182,5 CUh, vượt quota |
| [Qdrant Cloud](https://qdrant.tech/pricing/) | 0,5 vCPU, 1 GB RAM, 4 GB disk, single node | Policy/review vector demo nhỏ sau đo | Không HA; đừng lấy quota làm SLO. [Cloud FAQ](https://qdrant.tech/cloud/) nêu suspend sau 1 tuần không dùng và delete sau 4 tuần nếu không kích hoạt lại |
| [Neo4j AuraDB Free](https://neo4j.com/free-graph-database/) | 1 graph DB, 50.000 nodes/175.000 relationships | Graph demo M6 | Không kèm database backups; tự pause sau 3 ngày không hoạt động, cần kiểm tra trước buổi demo |
| [Cloudflare R2 Standard](https://developers.cloudflare.com/r2/pricing/) | 10 GB-month/tháng, 1 triệu Class A và 10 triệu Class B operations; internet egress free | Checkpoint đã chọn, dataset/eval artifacts, backup nhỏ | Vượt quota tính phí; Standard storage ngoài quota $0,015/GB-month; không gộp mọi checkpoint vào free quota |
| [Cloudflare Pages](https://developers.cloudflare.com/pages/platform/limits/) | Free plan 500 builds/tháng | Static React frontend | Không phải máy chạy FastAPI/PyTorch/Redis; API cần host riêng |
| [Modal Starter](https://modal.com/pricing) | $30 compute credit/tháng, phí gói $0 | FastAPI, embedding/ABSA/rerank functions và training theo đợt | Credit chung CPU/RAM/GPU; xem phương án B cho billing, state và cold start |
| [Google Colab](https://research.google.com/colaboratory/faq.html) | Có compute/GPU miễn phí với hạn mức biến động | Notebook train/thử nghiệm, lưu checkpoint thường xuyên | Không đảm bảo GPU hoặc runtime; không dùng làm backend phục vụ 24/7 |
| [Gemini API](https://ai.google.dev/gemini-api/docs/pricing) | Một số model có free input/output, rate limits theo model/account | Thử tiếng Việt/JSON/citation bằng dữ liệu synthetic hoặc công khai phù hợp | Free content được ghi là dùng cải thiện sản phẩm; raw PII không được gửi. Paid Standard nêu không dùng cải thiện sản phẩm; vẫn cần data policy của dự án |

**Không tính Hugging Face Docker Spaces là backend hoàn toàn free theo thông tin cũ.** [Tài liệu hiện tại](https://huggingface.co/docs/hub/spaces-overview) nói CPU Basic không có phí theo giờ nhưng tạo Docker/Gradio compute Space cần paid plan (có ngoại lệ ZeroGPU được mô tả riêng); Static Spaces free. Disk mặc định là ephemeral. Đây không phải chỗ đặt các DB persistent của dự án.

Để giảm vận hành, không cần dùng tất cả nhà cung cấp free cùng lúc. Chia app qua nhiều region có thể tăng round-trip latency và làm demo phụ thuộc nhiều quota/sleep policies. Cùng một VPS hoặc local Compose dễ tái lập hơn cho một người.

## 4. Bốn phương án triển khai

### A. Local, gần như không có phí dịch vụ cố định — khuyến nghị cho M0–M7

Web → FastAPI → PostgreSQL/Redis/Qdrant; thêm Neo4j ở M6. Worker chạy riêng. LLM gọi API. GPU chỉ dùng lúc train trên Colab hoặc thuê theo giờ; xuất model đã chọn về local.

Chi phí hosting tăng thêm $0 nếu đã có máy và không thuê cloud; vẫn có điện, Internet, phần cứng và token/GPU nếu dùng paid. Với workspace ~16 GB RAM, có thể bắt đầu development và đo giới hạn, không cần mua thêm máy trước smoke.

Không phải public service luôn hoạt động: máy tắt thì app dừng. Nếu demo qua mạng cần đường truy cập/TLS/auth phù hợp, không mở trực tiếp các database ports ra Internet.

### B. Modal serverless — ưu tiên thử cho public demo ít tải và GPU jobs

Modal Starter có $30 compute credit/tháng; trả phần vượt credit hoặc dịch vụ ngoài phạm vi credit. Đây là khoản dùng chung của workspace, không phải $30 cho mỗi model. Credit compute không trả hóa đơn LLM bên ngoài; Modal Shared Endpoints tính token cũng không nằm trong credit này. Đơn giá standard Functions: T4 $0,000164/s; L4 $0,000222/s; CPU $0,0000131/core/s; RAM $0,00000222/GiB/s. [Modal pricing](https://modal.com/pricing).

**Phương án tích hợp đề xuất**, chưa deploy:

| Phần của SenticRAG | Nơi chạy/lưu | Ranh giới |
| --- | --- | --- |
| Web React | Cloudflare Pages hoặc static hosting | Frontend gọi API HTTPS; không chứa secret |
| FastAPI/chat orchestration | Modal CPU Function/ASGI app | Stateless container; history, idempotency, pending approval lưu PostgreSQL |
| Embedding, PhoBERT ABSA, BGE rerank | Modal CPU/GPU Functions riêng | Chỉ cấp GPU cho function cần; API chờ LLM không giữ GPU |
| Train/retrain M4/M7 | Modal GPU job theo đợt | Save/resume checkpoint và version manifest; không giả định GPU luôn sẵn hoặc run không bị ngắt |
| PostgreSQL | Neon hoặc DB server riêng | Source of truth, outbox và durable approval; pool/connection limits khi API scale |
| Qdrant/Neo4j | Cloud free tiers đã đối chiếu, hoặc server riêng | Kết nối TLS/auth; graph bật từ M6; kiểm region/network latency |
| Model weights/checkpoints | Modal Volume, export backup ra object storage | Không đặt DB transaction trên Volume như thay thế managed PostgreSQL |
| Redis/Streams | Redis server có persistence/command support phù hợp | Đây là dependency còn phải chọn và đo giá; không tự đổi thành Modal Queue mà vẫn gọi giữ nguyên baseline |

Modal hỗ trợ phục vụ FastAPI bằng ASGI wrapper, không cần viết lại domain services. Cần thêm deployment adapter/image/secrets, pin dependencies và mount artifact; Docker Compose vẫn dùng để dev local. [HTTP applications](https://modal.com/docs/guide/webhooks). Volume phù hợp workload model weights; semantics commit/reload và concurrent writes cần được tôn trọng. [Volumes](https://modal.com/docs/guide/volumes).

Với 1 physical CPU core (khác vCPU), 8 GiB RAM và một GPU, phép tính minh họa cho **giờ container được tính phí**:

| Function | Tổng compute/giờ xấp xỉ | $30 nếu chỉ dùng function này |
| --- | --- | --- |
| CPU, không GPU | $0,1111 | 270 giờ |
| T4 + CPU/RAM trên | $0,7015 | 42,8 giờ |
| L4 + CPU/RAM trên | $0,9103 | 33,0 giờ |

Đây là phép tính theo rate đã dẫn, không phải thời gian train được bảo đảm. CPU/RAM tính theo giá trị lớn hơn giữa requested và actual, nên vượt mức giả định làm chi phí tăng; region pin/non-preemptible có thể cộng hệ số. Ví dụ cùng mức request trên, 20 giờ L4 + 50 giờ CPU ≈ $23,76 compute, còn khoảng $6,24 credit nếu workspace không có workload khác. Tổng billed time phải gồm khởi tạo/model loading, retry và khoảng chờ tính phí, không chỉ thời gian forward pass. [Resource metering](https://modal.com/docs/guide/resources).

Functions mặc định có thể scale về zero. Khởi đầu đề xuất `min_containers=0`, `max_containers=1` hoặc 2 theo function; thử `scaledown_window=30–60` giây và đo lại. Khoảng giữ container chờ vẫn dùng tài nguyên tính phí; cold start/load model có thể kéo dài request đầu. Giữ warm liên tục đổi latency lấy chi phí, không phù hợp suy luận “serverless nên miễn phí 24/7”. Tách cold/warm p95 theo Q-16; không mặc định đạt Pipeline B <2s. [Scaling](https://modal.com/docs/guide/scale), [cold starts](https://modal.com/docs/guide/cold-start).

**Worker cần điều chỉnh theo serverless:** không giữ consumer `XREAD BLOCK` chờ cả ngày nếu mục tiêu là scale-to-zero. Chọn bounded drain job/scheduled dispatcher đọc outbox, xử lý một batch rồi kết thúc; giữ event ID, retry, ack/reclaim và replay invariant của M4.5. Xác định latency do polling, pin phiên bản knowledge và kiểm quyền trước tool/action. Modal Queue là lựa chọn kiến trúc khác cần ADR, không phải thay thế Redis Streams tự động.

**Kiểm soát tiền:** billing docs hiện yêu cầu payment method; đừng dựa vào suy đoán hết $30 thì tự ngừng mọi chi phí. Đặt Workspace usage budget, ví dụ $25 trước credits, và net spend limit $0 nếu mục tiêu không trả thêm; kiểm giá trị đã lưu trong dashboard. Spend limit khác usage budget; Environment budgets thuộc Team/Enterprise. [Billing](https://modal.com/docs/guide/billing), [budgets/spend limits](https://modal.com/docs/guide/budgets).

Phương án này có thể có hóa đơn Modal $0 khi workload nằm trong credit và không phát sinh khoản ngoài credit; toàn hệ thống chỉ $0 khi các DB/Redis/storage/LLM cũng nằm trong quota hoặc chạy trên tài nguyên đã có. Chưa chọn Redis cloud và chưa đo total usage nên chưa thể cam kết full stack online miễn phí. Modal demo không chứng minh EKS/IAM runtime ở M8.

### C. Một VPS khi cần compute chạy liên tục

Deploy React build + reverse proxy/TLS + API + worker; DB/Redis/Qdrant/Neo4j cùng VPS hoặc tách managed DB nếu memory không đủ. Train GPU ở môi trường khác và tải artifact khi deploy. Dùng persistent disk và backup ngoài VPS.

Ví dụ giá **DigitalOcean Basic Regular**, không phải khẳng định rẻ nhất: 4 vCPU/8 GiB/160 GiB SSD = **$48/tháng**; 8 vCPU/16 GiB/320 GiB SSD = **$96/tháng**. Mức 8 GiB chỉ nên chọn sau smoke, đặc biệt khi load đồng thời ABSA/embedding/reranker và Neo4j. Phí backup, token, GPU, object storage vượt quota hoặc domain cộng riêng. [Bảng giá Droplets](https://www.digitalocean.com/pricing/droplets).

Nếu chỉ cần một đợt demo ngắn, tính theo thời gian tạo tài nguyên với rate nhà cung cấp; xuất backup và xóa tài nguyên tính phí sau khi không dùng. Không mặc định nút stop tương đương không tính phí.

### D. AWS EKS theo target architecture

Cần EKS control plane, worker EC2 hoặc Fargate, disk/EBS, ECR images, S3 artifacts, IAM/OIDC, secrets, networking/load balancer và logs. GPU nodes chỉ thêm nếu workload yêu cầu. Repo nhắm Singapore (`ap-southeast-1`), nên báo giá node/storage/network phải chọn region này.

EKS standard-support control plane **$0,10/giờ**, khoảng **$73 cho 730 giờ/tháng**; extended support **$0,60/giờ**, khoảng $438/tháng. Đây chưa gồm worker, disk, load balancer/NAT, log, public IP hay data transfer. Không có cơ sở gọi cả stack EKS là miễn phí. [AWS EKS pricing](https://aws.amazon.com/eks/pricing/).

AWS Free Tier hiện công bố cho khách mới tới **$200 credits** ($100 ban đầu + tối đa $100 qua hoạt động) và free plan tới 6 tháng; phụ thuộc eligibility/account/service. Không tính credits là ngân sách chắc chắn khi chưa kiểm Billing của tài khoản. [AWS Free Tier FAQ](https://aws.amazon.com/free/free-tier-faqs/).

Để minh họa tác động: chỉ control plane chạy 14 tuần liên tục đã là 14 × 7 × 24 × $0,10 = **$235,20**, chưa có worker. Nên chỉ provision giai đoạn cần nghiệm thu cloud; local/Compose pass không thay bằng chứng EKS/IAM runtime.

## 5. Dự trù token và training tách khỏi hosting

Ví dụ định lượng, **không chốt provider/model**: 5.000 lượt/tháng, mỗi lượt tổng cộng 3.000 input tokens + 400 billed output tokens. Với `gemini-3.1-flash-lite` Standard ($0,25/1M input, $1,50/1M output), phép tính là 15M × $0,25 + 2M × $1,50 = **$6,75/tháng**. Chưa có retry/reflection/tool calls thêm, search grounding hay cache storage; token thinking nếu model có dùng phải cộng vào output. Chất lượng tiếng Việt/grounding vẫn phải nghiệm thu. [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing).

Đối với GPU, trang Runpod hiện hiển thị ví dụ RTX 3090 24 GB ở **$0,50/giờ** cho Pods. Một **ngân sách giả định 20 GPU-hours** tương đương $10 compute, cộng storage/phí liên quan; đây không phải cam kết train xong trong 20h hoặc capacity luôn sẵn. Kiểm loại cloud/region/giá cuối ở console trước chạy. Modal credit hoặc Colab free là phương án đầu; GPU thuê là fallback cho deadline. [Runpod pricing](https://www.runpod.io/pricing).

| Kịch bản minh họa | Chi phí đã tính được | Khoản chưa bao gồm |
| --- | --- | --- |
| Local + free LLM/GPU trong quota | $0 dịch vụ hosting cố định | Điện/máy/Internet; quota không bảo đảm |
| Local + 5.000 chat paid theo ví dụ | $6,75/tháng | Retry và các call khác; GPU khi train |
| VPS 8 GiB + ví dụ token trên | $54,75/tháng | Backup/storage phát sinh/thuế/domain; GPU training |
| VPS 16 GiB + ví dụ token trên | $102,75/tháng | Các khoản trên; không cam kết SLA từ cấu hình |
| Modal: 20 giờ L4 + 50 giờ CPU theo phương án B | ~$23,76 compute; có thể $0 sau $30 credit | DB/Redis/LLM và usage ngoài giả định; không bảo đảm workload hoàn thành trong số giờ này |
| 20 giờ GPU thuê | $10 compute cho đợt chạy | Storage và thời gian vượt budget |
| EKS | $73/tháng control plane standard | Tất cả worker/network/storage/token/GPU; cần calculator riêng |

Budget alerts giúp theo dõi; hard quotas/token caps và cơ chế dừng job mới là cách giới hạn workload. Ghi USD/request, GPU-hours/run, disk usage và chi phí mỗi lần promote vào manifest/metrics.

## 6. Khoảng trống triển khai trong repo hiện tại

Đọc [Compose](../../infra/compose/docker-compose.yml), [API Dockerfile](../../infra/docker/Dockerfile.api), [training workflow](../../.github/workflows/train.yml) và [release workflow](../../.github/workflows/release.yml):

- Compose có PostgreSQL/Redis/Qdrant/Neo4j/API và volumes; chưa có web/worker/dispatcher. API đang depends_on Neo4j ngay từ đầu; cần profiles/optional readiness để M2 chạy không phụ thuộc graph chưa dùng.
- Mật khẩu demo đang nằm trong Compose và DB ports publish ra host; cần cấu hình secrets/env, mạng nội bộ và chỉ public web/API khi deploy.
- Redis cần chốt persistence/retention và reclaim/retry phù hợp queue; có volume chưa tự chứng minh durable delivery. SQL outbox và restore drill nằm trong milestone.
- API image cài toàn bộ main dependencies gồm torch/transformers; cần đo image size/RAM và cân nhắc tách dependency runtime/training trước chọn host nhỏ.
- `train.yml` hiện chỉ build training image; chưa thực hiện training hoặc cấp GPU runner.
- Release workflow chứa tên mẫu `project-a`/`ai-production`, tham chiếu `infra/helm/project-a` hiện không có; chưa có Helm/Terraform package trong checkout. Có workflow không đồng nghĩa đã có hạ tầng EKS hoặc deploy thành công.

Đây là danh sách việc cần triển khai theo milestone, không phải đã sửa trong lượt rà tài nguyên này.

## 7. Cách gắn tài nguyên vào milestone

| Mốc | Điều kiện tài nguyên cần chốt |
| --- | --- |
| M0 | Máy/CPU/RAM/disk thật, API key và data policy, trần chi phí, region; smoke DB + embedding + LLM; chọn local/online profile |
| M1–M2 | Disk/backup, DB migrations, Qdrant và lexical index; chạy local trước, chưa cần thuê EKS |
| M3 | Persistence/approval/outbox design, customer-data boundaries, API auth và quota |
| M4 | Xác nhận GPU/Modal credit trước sprint train; save/resume checkpoint; đo thời gian/VRAM và budget mỗi run |
| M5–M6 | Thêm Neo4j, graph/policy/index version snapshots; đo memory lúc stack đầy đủ hoạt động |
| M7 | Dự trù một retrain/eval cycle; giữ artifact/version cũ cho rollback |
| M8 | Modal/VPS/EKS theo ngân sách và acceptance profile; TLS/backup/restore/load tests, cold/warm latency; ghi riêng local/cloud/EKS evidence |

Lựa chọn đề xuất: A cho phát triển local; B ưu tiên thử cho public demo ít tải và GPU jobs; C khi cần compute liên tục hoặc gom stack; D khi cần chứng minh AWS và có ngân sách riêng. Không thay đổi lịch, phê duyệt data hoặc đánh dấu gate PASS từ việc có free tier.

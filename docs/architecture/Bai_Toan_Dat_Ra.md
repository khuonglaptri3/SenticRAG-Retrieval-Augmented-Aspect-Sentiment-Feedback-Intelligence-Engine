
# MỤC TIÊU NGHIÊN CỨU & ĐẶC TẢ KIẾN TRÚC SẢN PHẨM: SENTICRAG PLATFORM

Hãy thực hiện một nghiên cứu chuyên sâu (Deep Research) và lập bản đặc tả sản phẩm/kiến trúc chi tiết nhằm tái định hình toàn diện hệ sinh thái **SenticRAG**.

Hệ thống mới không chỉ đóng vai trò phân tích nội bộ (Business Intelligence) mà còn là nền tảng **Tự động hóa chăm sóc khách hàng & Xử lý khiếu nại chủ động (Actionable Customer Care & Resolution)** với sự kết hợp giữa ABSA, Retrieval, GraphRAG và cơ chế đóng góp tri thức hai chiều (Collaborative Feedback Loop).

---

## 1. Bài toán cốt lõi & Sự phân công nhiệm vụ (Định lượng vs. Định tính)

Hãy làm rõ vai trò chuyên biệt của từng module trong xử lý dữ liệu lớn (Big Data Reviews):

1. **ABSA giải quyết bài toán Định lượng (100% Corpus Analysis):**
   - Quét qua toàn bộ dữ liệu (ví dụ 100.000 reviews/tháng) để gán nhãn Aspect, Sentiment và trích xuất Entity có cấu trúc.
   - Không bị giới hạn bởi `top_k`. Cung cấp góc nhìn toàn cảnh (Macro view) trên Dashboard: *Tỷ lệ tiêu cực của aspect `pin` tháng này là 40%, tăng vọt 15% so với tháng trước*.
2. **Retrieval giải quyết bài toán Định tính (Root Cause Investigation qua Top-K):**
   - Đóng vai trò "kính lúp" đào sâu nguyên nhân khi chỉ số định lượng có biến động.
   - Khi người quản lý hỏi: *"Khách hàng cụ thể đang gặp vấn đề gì với pin?"*, Retrieval áp dụng bộ lọc metadata (`aspect: pin`, `sentiment: negative`) kết hợp Dense + BM25 để lấy ra `top_k` review tiêu biểu nhất, đưa vào LLM tóm tắt: *"Khách phàn nàn pin sạc không vào sau bản update v1.2, kèm hiện tượng nóng máy"*.
3. **Mở rộng sang Actionable Care (Hành động trực tiếp với khách hàng):**
   - Kết hợp kết quả phân tích với **Chính sách nội bộ & GraphRAG** để tự động tạo giải pháp phản hồi tức thì cho khách hàng (hướng dẫn đổi trả, thông tin trạm bảo hành, contact kỹ thuật).

---

## 2. Các yêu cầu nghiên cứu và đặc tả chi tiết

### Phần A: Vòng lặp đóng góp tri thức (Collaborative Data & Knowledge Feedback Loop)

Nghiên cứu cơ chế lưu trữ và cho phép các bên liên quan cùng làm giàu hệ thống:

- **Lưu trữ dữ liệu người mua & lịch sử tương tác:** Gắn kết `review_id` với hồ sơ khách hàng, mã đơn hàng, ngày mua, phiên bản sản phẩm trong Database.
- **Sự đóng góp của đội ngũ phân tích (Product Analysts / CX / CSKH):**
  - Khi nhà phân tích phát hiện nguyên nhân gốc rễ (Root cause), họ có thể gắn thẻ (tagging), thêm ghi chú (annotation), hoặc đánh dấu một lỗi mới phát sinh (New emerging bug).
  - Cơ chế cập nhật ngược lại vào **Knowledge Graph / Ontology**: Bổ sung các mối quan hệ mới (ví dụ: *Lỗi pin sạc chậm* $\rightarrow$ *Nguyên nhân: Firmware v1.2* $\rightarrow$ *Giải pháp: Hướng dẫn hạ cấp firmware hoặc gửi đổi pin*).
  - Vòng lặp cải thiện mô hình: Đội ngũ gắn nhãn đúng/sai cho các kết quả của ABSA để tái huấn luyện (Active Learning / Re-training pipeline).

### Phần B: Kiến trúc Module & Luồng dữ liệu End-to-End

Xây dựng sơ đồ kiến trúc và luồng xử lý chi tiết:

1. **Batch Processing Pipeline (Định lượng):** Ingestion $\rightarrow$ PII Masking $\rightarrow$ ABSA Inference trên toàn bộ review $\rightarrow$ Lưu vào RDBMS/Data Warehouse để phục vụ Dashboard BI & Metrics.
2. **Hybrid Retrieval & Graph Traversal Pipeline (Định tính & Giải pháp):**
   - Truy vấn kết hợp: Metadata filtering (do ABSA tạo ra) + Hybrid Search (Dense + BM25 trên Qdrant) + GraphRAG (Neo4j/Graph Index).
   - Tra cứu chéo: Từ lỗi của khách hàng $\rightarrow$ liên kết tới Chính sách đổi trả/Bảo hành $\rightarrow$ Chi nhánh hỗ trợ gần nhất $\rightarrow$ Người phụ trách.
3. **LLM Generation & Action Routing:**
   - Tạo báo cáo Root Cause có dẫn chứng (citations) cho Product Manager.
   - Tạo câu trả lời tự động hoặc bản nháp phản hồi giải pháp (Resolution draft) cho nhân viên CSKH gửi tới người mua.

### Phần C: Hệ thống User Stories & Kịch bản thực tế

Xây dựng câu chuyện người dùng cụ thể cho 4 đối tượng:

1. **Khách hàng (Buyer):** Đánh giá chê sản phẩm hỏng và nhận ngay được phản hồi hướng dẫn xử lý đúng chính sách kèm lời xin lỗi chân thành.
2. **Nhân viên CSKH (Support Agent):** Nhận ticket đã được phân loại sẵn aspect, kèm draft phản hồi đã tra sẵn quy trình bảo hành dựa trên hồ sơ mua hàng.
3. **Chuyên viên phân tích (Product/CX Analyst):** Dùng Dashboard xem tỷ lệ định lượng, dùng công cụ hỏi-đáp định tính để tìm nguyên nhân lỗi, và **đóng góp ghi chú/giải pháp mới vào hệ thống tri thức**.
4. **Giám đốc sản phẩm (CPO/PM):** Nắm bắt xu hướng lỗi của sản phẩm theo thời gian thực và đánh giá hiệu quả giải quyết khiếu nại.

### Phần D: Đánh giá Giá trị Kinh doanh, Công nghệ & Đạo đức dữ liệu

- **Chỉ số đo lường hiệu quả (Metrics):** Cả về kỹ thuật (Macro-F1 của ABSA, Recall@K của Retrieval, Groundedness của LLM) và kinh doanh (FRT, MTTR, CSAT, Cost per Ticket).
- **Tech Stack đề xuất:** Giải pháp cho Ingestion, ABSA model (PhoBERT/DeBERTa), Vector DB (Qdrant), Graph DB (Neo4j), RDBMS, Orchestration.
- **Bảo mật & Quản trị dữ liệu:** Cơ chế tuân thủ Luật Bảo vệ dữ liệu cá nhân (ẩn danh thông tin người mua, phân quyền truy cập giữa CSKH và Analyst).

---

## 3. Định dạng đầu ra mong muốn

- Báo cáo đặc tả sản phẩm hoàn chỉnh bằng tiếng Việt, rõ ràng, tính ứng dụng thực tế cao.
- Có sơ đồ luồng dữ liệu (Mermaid.js diagram).
- Có bảng so sánh, ví dụ JSON Payload cho API, cấu trúc Graph Ontology thực tế (Nodes, Edges, Properties).

# MỤC TIÊU NGHIÊN CỨU & ĐẶC TẢ KIẾN TRÚC SẢN PHẨM: SENTICRAG PLATFORM

Hãy thực hiện một nghiên cứu chuyên sâu (Deep Research) và lập bản đặc tả sản phẩm/kiến trúc chi tiết nhằm tái định hình toàn diện hệ sinh thái **SenticRAG**.

Hệ thống mới không chỉ đóng vai trò phân tích nội bộ (Business Intelligence) mà còn là nền tảng **Tự động hóa chăm sóc khách hàng & Xử lý khiếu nại chủ động (Actionable Customer Care & Resolution)** với sự kết hợp giữa ABSA, Retrieval, GraphRAG và cơ chế đóng góp tri thức hai chiều (Collaborative Feedback Loop).

---

## 1. Bài toán cốt lõi & Sự phân công nhiệm vụ (Định lượng vs. Định tính)

Hãy làm rõ vai trò chuyên biệt của từng module trong xử lý dữ liệu lớn (Big Data Reviews):

1. **ABSA giải quyết bài toán Định lượng (100% Corpus Analysis):**
   - Quét qua toàn bộ dữ liệu (ví dụ 100.000 reviews/tháng) để gán nhãn Aspect, Sentiment và trích xuất Entity có cấu trúc.
   - Không bị giới hạn bởi `top_k`. Cung cấp góc nhìn toàn cảnh (Macro view) trên Dashboard: *Tỷ lệ tiêu cực của aspect `pin` tháng này là 40%, tăng vọt 15% so với tháng trước*.
2. **Retrieval giải quyết bài toán Định tính (Root Cause Investigation qua Top-K):**
   - Đóng vai trò "kính lúp" đào sâu nguyên nhân khi chỉ số định lượng có biến động.
   - Khi người quản lý hỏi: *"Khách hàng cụ thể đang gặp vấn đề gì với pin?"*, Retrieval áp dụng bộ lọc metadata (`aspect: pin`, `sentiment: negative`) kết hợp Dense + BM25 để lấy ra `top_k` review tiêu biểu nhất, đưa vào LLM tóm tắt: *"Khách phàn nàn pin sạc không vào sau bản update v1.2, kèm hiện tượng nóng máy"*.
3. **Mở rộng sang Actionable Care (Hành động trực tiếp với khách hàng):**
   - Kết hợp kết quả phân tích với **Chính sách nội bộ & GraphRAG** để tự động tạo giải pháp phản hồi tức thì cho khách hàng (hướng dẫn đổi trả, thông tin trạm bảo hành, contact kỹ thuật).

---

## 2. Các yêu cầu nghiên cứu và đặc tả chi tiết

### Phần A: Vòng lặp đóng góp tri thức (Collaborative Data & Knowledge Feedback Loop)

Nghiên cứu cơ chế lưu trữ và cho phép các bên liên quan cùng làm giàu hệ thống:

- **Lưu trữ dữ liệu người mua & lịch sử tương tác:** Gắn kết `review_id` với hồ sơ khách hàng, mã đơn hàng, ngày mua, phiên bản sản phẩm trong Database.
- **Sự đóng góp của đội ngũ phân tích (Product Analysts / CX / CSKH):**
  - Khi nhà phân tích phát hiện nguyên nhân gốc rễ (Root cause), họ có thể gắn thẻ (tagging), thêm ghi chú (annotation), hoặc đánh dấu một lỗi mới phát sinh (New emerging bug).
  - Cơ chế cập nhật ngược lại vào **Knowledge Graph / Ontology**: Bổ sung các mối quan hệ mới (ví dụ: *Lỗi pin sạc chậm* $\rightarrow$ *Nguyên nhân: Firmware v1.2* $\rightarrow$ *Giải pháp: Hướng dẫn hạ cấp firmware hoặc gửi đổi pin*).
  - Vòng lặp cải thiện mô hình: Đội ngũ gắn nhãn đúng/sai cho các kết quả của ABSA để tái huấn luyện (Active Learning / Re-training pipeline).

### Phần B: Kiến trúc Module & Luồng dữ liệu End-to-End

Xây dựng sơ đồ kiến trúc và luồng xử lý chi tiết:

1. **Batch Processing Pipeline (Định lượng):** Ingestion $\rightarrow$ PII Masking $\rightarrow$ ABSA Inference trên toàn bộ review $\rightarrow$ Lưu vào RDBMS/Data Warehouse để phục vụ Dashboard BI & Metrics.
2. **Hybrid Retrieval & Graph Traversal Pipeline (Định tính & Giải pháp):**
   - Truy vấn kết hợp: Metadata filtering (do ABSA tạo ra) + Hybrid Search (Dense + BM25 trên Qdrant) + GraphRAG (Neo4j/Graph Index).
   - Tra cứu chéo: Từ lỗi của khách hàng $\rightarrow$ liên kết tới Chính sách đổi trả/Bảo hành $\rightarrow$ Chi nhánh hỗ trợ gần nhất $\rightarrow$ Người phụ trách.
3. **LLM Generation & Action Routing:**
   - Tạo báo cáo Root Cause có dẫn chứng (citations) cho Product Manager.
   - Tạo câu trả lời tự động hoặc bản nháp phản hồi giải pháp (Resolution draft) cho nhân viên CSKH gửi tới người mua.

### Phần C: Hệ thống User Stories & Kịch bản thực tế

Xây dựng câu chuyện người dùng cụ thể cho 4 đối tượng:

1. **Khách hàng (Buyer):** Đánh giá chê sản phẩm hỏng và nhận ngay được phản hồi hướng dẫn xử lý đúng chính sách kèm lời xin lỗi chân thành.
2. **Nhân viên CSKH (Support Agent):** Nhận ticket đã được phân loại sẵn aspect, kèm draft phản hồi đã tra sẵn quy trình bảo hành dựa trên hồ sơ mua hàng.
3. **Chuyên viên phân tích (Product/CX Analyst):** Dùng Dashboard xem tỷ lệ định lượng, dùng công cụ hỏi-đáp định tính để tìm nguyên nhân lỗi, và **đóng góp ghi chú/giải pháp mới vào hệ thống tri thức**.
4. **Giám đốc sản phẩm (CPO/PM):** Nắm bắt xu hướng lỗi của sản phẩm theo thời gian thực và đánh giá hiệu quả giải quyết khiếu nại.

### Phần D: Đánh giá Giá trị Kinh doanh, Công nghệ & Đạo đức dữ liệu

- **Chỉ số đo lường hiệu quả (Metrics):** Cả về kỹ thuật (Macro-F1 của ABSA, Recall@K của Retrieval, Groundedness của LLM) và kinh doanh (FRT, MTTR, CSAT, Cost per Ticket).
- **Tech Stack đề xuất:** Giải pháp cho Ingestion, ABSA model (PhoBERT/DeBERTa), Vector DB (Qdrant), Graph DB (Neo4j), RDBMS, Orchestration.
- **Bảo mật & Quản trị dữ liệu:** Cơ chế tuân thủ Luật Bảo vệ dữ liệu cá nhân (ẩn danh thông tin người mua, phân quyền truy cập giữa CSKH và Analyst).

---

## 3. Định dạng đầu ra mong muốn

- Báo cáo đặc tả sản phẩm hoàn chỉnh bằng tiếng Việt, rõ ràng, tính ứng dụng thực tế cao.
- Có sơ đồ luồng dữ liệu (Mermaid.js diagram).
- Có bảng so sánh, ví dụ JSON Payload cho API, cấu trúc Graph Ontology thực tế (Nodes, Edges, Properties).

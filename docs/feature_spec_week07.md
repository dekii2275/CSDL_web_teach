# Đặc Tả Tính Năng (Feature Specification) - Buổi 7
## Tính năng: Bộ lọc tùy chọn cho CourseHub API `GET /sections`

- **Tác giả**: Sinh viên thực hành CourseHub (Nhánh `week07-release-candidate`)
- **Trạng thái**: Draft / AI-OFF Specification
- **Mục tiêu**: Bổ sung hai tham số truy vấn (query parameters) tùy chọn `available_only` và `course_code` cho endpoint `GET /sections` của CourseHub, đảm bảo tương thích ngược 100% với Frontend và các bài kiểm thử hiện có.

---

### 1. Yêu cầu nghiệp vụ (Business Requirements & API Contract)

Người dùng muốn chọn "Chỉ hiện lớp còn chỗ" trên giao diện CourseHub. Về phía API, một lớp được coi là "còn chỗ" nếu trường `remaining > 0` trong kết quả hiện tại của `GET /sections`.
Endpoint tiếp tục giữ nguyên phương thức `GET /sections` (không đổi thành `/api/sections` ở tầng FastAPI). Khi không truyền tham số, API phải giữ nguyên toàn bộ dữ liệu và thứ tự ban đầu.

| Request HTTP | Tham số Query | Kỳ vọng kết quả & Mã trạng thái |
| :--- | :--- | :--- |
| `GET /sections` | Không tham số | Giữ nguyên danh sách và thứ tự như trước khi sửa; trả về **HTTP 200**. |
| `GET /sections?available_only=true` | `available_only=true` | Chỉ trả về các lớp có `remaining > 0`; trả về **HTTP 200** (có thể trả về mảng rỗng `[]` nếu tất cả lớp đã đầy). |
| `GET /sections?course_code=INT2204` | `course_code=INT2204` | Chỉ trả về các lớp của học phần `INT2204`; chấp nhận chữ hoa/thường (`int2204`) và khoảng trắng thừa (` int2204 `). Trả về **HTTP 200**. |
| `GET /sections?course_code=INT2204&available_only=true` | Kết hợp cả 2 tham số | Chỉ trả về các lớp vừa thuộc mã `INT2204` vừa có `remaining > 0`; không thay đổi tên hoặc cấu trúc các trường JSON. Trả về **HTTP 200**. |
| `GET /sections?course_code=INT9999` | Mã học phần không tồn tại | Trả về mảng rỗng `[]` kèm **HTTP 200**; tuyệt đối **không** tự đổi thành lỗi HTTP 404. |

---

### 2. Tiêu chí nghiệm thu (Acceptance Criteria)

- **AC1 – Tương thích ngược mặc định (Default Preservation)**:
  Khi không có query parameter nào được truyền vào, kết quả trả về phải giữ nguyên cấu trúc, số lượng và thứ tự hiển thị ban đầu.
- **AC2 – Lọc lớp còn chỗ (`available_only=true`)**:
  Kết quả chỉ chứa các lớp có `remaining > 0`. Không còn bất kỳ lớp nào có `remaining == 0` hoặc âm.
- **AC3 – Lọc theo mã học phần linh hoạt (`course_code`)**:
  So khớp chính xác mã học phần không phân biệt chữ hoa hay chữ thường, tự động cắt bỏ khoảng trắng (trim) ở đầu và cuối chuỗi.
- **AC4 – Tính hợp lệ của kết quả rỗng (Empty Result is Valid)**:
  Khi không tìm thấy lớp học phần phù hợp với điều kiện lọc, API phải trả về mảng rỗng `[]` cùng mã `HTTP 200`, không coi đây là lỗi tài nguyên không tìm thấy (`404`).
- **AC5 – Bất biến CSDL và các route nghiệp vụ (Scope Boundaries)**:
  Không thay đổi cấu trúc bảng, view (`v_section_summary`), dữ liệu bảng `enrollments`, `enrollment_events`. Giữ nguyên logic Transaction, Row-level Locking (`FOR UPDATE`), và mã lỗi `HTTP 409 Conflict` của `POST /enrollments` và `DELETE /enrollments`.
- **AC6 – Nối luồng Frontend (Client-Server Integration)**:
  Thao tác bấm checkbox trên giao diện React phải kích hoạt request mạng chứa query parameter tương ứng tới server, nhận dữ liệu mới lọc từ Backend thay vì chỉ lọc state cục bộ tại trình duyệt.

---

### 3. Dữ liệu mẫu dùng cho Kiểm thử độc lập (Test Matrix Input/Output)

Dữ liệu giả lập đầu vào (không phụ thuộc vào CSDL thật):

```json
[
  {"class_id": "WEB-01", "course_code": "INT2204", "remaining": 0},
  {"class_id": "WEB-02", "course_code": "INT2204", "remaining": 2},
  {"class_id": "DM-01",  "course_code": "INT2205", "remaining": 1}
]
```

| Kịch bản kiểm thử | Input Parameters | Expected Output (`class_id`) | Mục đích chứng minh |
| :--- | :--- | :--- | :--- |
| **Case 1: Default** | `available_only=False`, `course_code=None` | `["WEB-01", "WEB-02", "DM-01"]` | Đạt AC1: Giữ nguyên số lượng & thứ tự gốc. |
| **Case 2: Available Only** | `available_only=True`, `course_code=None` | `["WEB-02", "DM-01"]` | Đạt AC2: Loại bỏ lớp `WEB-01` có `remaining=0`. |
| **Case 3: Case-insensitive & Trim** | `available_only=False`, `course_code=" int2204 "` | `["WEB-01", "WEB-02"]` | Đạt AC3: Khớp chính xác dù có khoảng trắng và chữ thường. |
| **Case 4: Combined Filter** | `available_only=True`, `course_code="INT2204"` | `["WEB-02"]` | Cả 2 điều kiện cùng thỏa mãn. |
| **Case 5: Empty Result** | `available_only=False`, `course_code="INT9999"` | `[]` | Đạt AC4: Trả về mảng rỗng, không gây lỗi. |
| **Case 6: Immutability** | `available_only=True` | Danh sách gốc không bị đột biến (`mutation`) | Đảm bảo hàm lọc thuần khiết (pure function), không sửa input. |

---

### 4. Ghi chú kiến trúc & Cơ sở dữ liệu (Database Architecture Note)
- Trong bài thực hành này, việc lọc bằng hàm thuần Python ở Backend giúp luyện tập viết đặc tả, hợp đồng API và kiểm thử độc lập (Unit Test). Tuy nhiên, cách này vẫn tải toàn bộ rows từ PostgreSQL về ứng dụng.
- **Nguyên tắc kỹ thuật tối ưu**: Khi làm việc với tập dữ liệu lớn trong thực tế, cần đẩy điều kiện `WHERE` và phân trang (`LIMIT` / `OFFSET` hoặc Keyset Pagination) xuống tầng câu lệnh SQL và bắt buộc sử dụng **Parameterized Query (Biến bind)** để bảo vệ chống lỗ hổng SQL Injection.

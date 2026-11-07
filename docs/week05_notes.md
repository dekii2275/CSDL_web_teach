# CourseHub - Buổi 5: Xây dựng Frontend với React kết nối FastAPI

## 1. Tóm tắt kết quả triển khai
- **CORS Backend**: Đã cấu hình `CORSMiddleware` trong `backend/app/main.py` cho phép origin `http://localhost:5173` và `http://127.0.0.1:5173` với các phương thức `GET`, `POST`, `DELETE`.
- **Thư mục Frontend**:
  - Khởi tạo với **Vite 7** và **React 18**.
  - `frontend/src/api.js`: Hàm fetch dùng chung xử lý `AbortController`, bắt lỗi mạng, xử lý `DELETE 204`, và trích xuất thông báo lỗi từ FastAPI.
  - Các component độc lập:
    - `Notice.jsx`: Hiển thị thông báo `info`, `success`, `error`.
    - `SectionTable.jsx`: Hiển thị danh sách lớp, sức chứa, số đã đăng ký, số còn lại và nút Đăng ký (tự động khóa khi hết chỗ hoặc đã đăng ký).
    - `EnrollmentList.jsx`: Hiển thị các lớp đã đăng ký của sinh viên kèm nút Hủy đăng ký.
  - `styles.css`: Giao diện chuẩn gồm CSS Grid 2 cột, Flexbox cho form/filter, và Media Query responsive xuống 1 cột trên màn hình hẹp (< 900px, < 560px).
  - `App.jsx`: Điều phối toàn bộ trạng thái (state), tải dữ liệu song song qua `Promise.all([/courses, /sections, /students/.../enrollments])`, và đồng bộ lại với CSDL sau mỗi thao tác.

---

## 2. Kiểm thử API & Unit Test
- Chạy kiểm thử tự động `npm test` với 8 tình huống HTTP giả lập trong `frontend/tests/api.test.mjs`:
  1. GET thành công trả về dữ liệu JSON.
  2. `AbortError` được giữ nguyên khi request bị hủy bởi AbortController.
  3. Lỗi mạng/CORS ném thông báo rõ ràng.
  4. DELETE thành công status 204 trả về `null`.
  5. Phản hồi không phải JSON ném lỗi `HTTP {status}: phản hồi không phải JSON.`
  6. HTTP lỗi với `detail` dạng chuỗi (ví dụ: HTTP 409).
  7. HTTP lỗi 422 với `detail` là danh sách `item.msg`.
  8. POST kèm body được serialize JSON đúng định dạng và có header `Content-Type: application/json`.
- Kết quả: **8/8 test passed**.

---

## 3. Quy trình thực hành và đối chiếu CSDL (SQL Verify)
- Sử dụng truy vấn trong `database/13_week05_verify.sql` để đối chiếu:
  1. **Đăng ký `WEB-01` cho sinh viên `22000004`**:
     - `POST /enrollments` trả về `201 Created`.
     - `enrollments` xuất hiện bản ghi `(22000004, WEB-01)`.
     - `v_section_summary` cập nhật `remaining = 0`, `enrolled = 3`.
     - `enrollment_events` ghi nhận sự kiện `CREATED`.
  2. **Hủy đăng ký `WEB-01`**:
     - `DELETE /enrollments/22000004/WEB-01` trả về `204 No Content`.
     - `enrollments` xóa bản ghi tương ứng.
     - `v_section_summary` phục hồi `remaining = 1`.
     - `enrollment_events` ghi nhận sự kiện `CANCELLED`.
  3. **Kiểm thử Concurrency 409**:
     - Hai cửa sổ cùng xem `RACE-01` còn 1 chỗ.
     - Cửa sổ A đăng ký thành công.
     - Cửa sổ B gửi request sau nhận lỗi `HTTP 409: Lop hoc phan da het cho` và tự động cập nhật lại giao diện về trạng thái "Hết chỗ".

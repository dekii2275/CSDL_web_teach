# Buổi 6 - Đóng gói, Kiểm thử và Tự động hóa CourseHub với Docker và GitHub Actions

## 1. Môi trường thực hành
- **Hệ điều hành**: Windows 11 (Host) / Ubuntu Latest (GitHub Actions Runner) / Alpine Linux (Container)
- **Docker Engine**: Docker Desktop 28.5.1, Docker Compose v2.40.0-desktop.1
- **Python Runtime**: Python 3.12-slim (Backend Container), Python 3.14 (Host)
- **Node.js Runtime**: Node 22-alpine (Frontend Build Stage), Nginx 1.31-alpine (Frontend Runtime Stage)

---

## 2. Kết quả kiểm thử tại Local
- **pytest backend/tests -q**: `2 passed in 2.74s` (bảo vệ hợp đồng OpenAPI paths và methods).
- **npm test**: `8 passed / 0 failed` (kiểm thử 8 kịch bản HTTP mock trong `tests/api.test.mjs`).
- **npm run build**: Tạo production bundle thành công trong `1.27s` (31 modules).
- **docker compose up -d --build**:
  - `backend`: Healthy (vượt qua kiểm tra `http://127.0.0.1:8000/health`).
  - `frontend`: Khởi chạy sau khi backend healthy, mở cổng `8080:80`.

---

## 3. Luồng kiểm thử tích hợp 3 tầng (Browser -> Nginx -> FastAPI -> PostgreSQL host)
- **Kiểm thử POST đăng ký**:
  - Request: `POST http://127.0.0.1:8080/api/enrollments` với `student_id: 22000004`, `class_section_id: WEB-01`.
  - HTTP status: `201 Created`.
  - SQL xác nhận: `v_section_summary` ghi nhận `enrolled = 3, remaining = 0`; bảng `enrollment_events` ghi nhận sự kiện `CREATED`.
- **Kiểm thử DELETE hủy đăng ký**:
  - Request: `DELETE http://127.0.0.1:8080/api/enrollments/22000004/WEB-01`.
  - HTTP status: `204 No Content`.
  - SQL xác nhận: `v_section_summary` phục hồi `enrolled = 2, remaining = 1`; bảng `enrollment_events` ghi nhận sự kiện `CANCELLED`.
- **Kiểm thử tình huống biên**:
  - `POST` với sinh viên không tồn tại: `HTTP 404 Not Found` (`{"detail":"Khong tim thay sinh vien"}`).
  - `POST` vào lớp đã đầy `DM-01`: `HTTP 409 Conflict` (`{"detail":"Lop hoc phan da het cho"}`).

---

## 4. Ghi nhận Debugging & Tối ưu hóa CI
- **Vấn đề gặp phải**:
  - Khi chạy tại máy cá nhân, Backend kết nối được CSDL vì có file `.env`.
  - Khi đẩy lên GitHub Actions Runner, máy chủ GitHub là môi trường sạch không có file `.env` (vì đã bị Git ignore để bảo mật), dẫn đến `database.py` báo lỗi thiếu biến môi trường khi import vào test contract.
- **Cách khắc phục**:
  - Bổ sung bước `cp backend/.env.example backend/.env` vào job `backend` trong `.github/workflows/ci.yml` để cung cấp biến môi trường không chứa secret phục vụ kiểm thử OpenAPI contract.
  - Sau khi push bản sửa, toàn bộ 3 job trên GitHub Actions đều chuyển sang trạng thái xanh (`PASS`).

---

## 5. Bàn giao Git, Pull Request và CI Run
- **Nhánh thực hành**: `week06-docker-ci`
- **GitHub Repository**: `https://github.com/dekii2275/CSDL_web_teach`
- **GitHub Actions Run**: [Run #43617597330](https://github.com/dekii2275/CSDL_web_teach/actions/runs/43617597330) (Kết quả: **Success** cho cả 3 job `backend`, `frontend`, `docker`).
- **Liên kết tạo Pull Request**: `https://github.com/dekii2275/CSDL_web_teach/pull/new/week06-docker-ci`

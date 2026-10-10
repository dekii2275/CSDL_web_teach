# CourseHub Demo

Dự án mẫu cho học phần **Cơ sở dữ liệu Web và hệ thống thông tin**.
Giảng viên: TS. Vũ Tiến Dũng – Phạm Duy Phương

---

## Cấu Trúc Dự Án

```text
coursehub-demo/
├── .gitignore
├── README.md
├── backend/
│   ├── __init__.py
│   ├── .env.example
│   ├── requirements.txt
│   ├── week01_python_refresh.py
│   └── app/
│       ├── __init__.py
│       ├── database.py
│       ├── schemas.py
│       └── main.py
├── database/
│   ├── 01_schema.sql
│   ├── 02_seed.sql
│   ├── 03_queries.sql
│   ├── 04_views.sql
│   ├── 05_constraint_checks.sql
│   ├── 06_view_demo.sql
│   ├── 07_ai_query.sql
│   └── 90_reset_demo.sql
├── docs/
│   ├── week02_notes.md
│   └── week03_notes.md
└── postman/
    ├── CourseHub_Buoi_3.postman_collection.json
    └── CourseHub_Local.postman_environment.json
```

---

## Nội Dung Các Buổi Thực Hành

### Buổi 1: Tổng quan hệ thống thông tin Web – Ôn tập Python – Git/GitHub
- Mô phỏng dữ liệu in-memory: Sinh viên, Học phần, Đăng ký lớp học phần.
- Cài đặt các hàm nghiệp vụ:
  - Tra cứu / tìm kiếm học phần (`find_course`, `search_courses`).
  - Kiểm tra điều kiện đăng ký (`can_enroll`).
  - Đăng ký học phần (`enroll_student`).
- Xử lý ngoại lệ, cấu trúc dữ liệu list và dictionary.
- Quản lý mã nguồn với Git/GitHub.

### Buổi 2: Thiết kế CSDL quan hệ CourseHub với PostgreSQL
- Thiết kế 6 bảng quan hệ: `students`, `courses`, `semesters`, `lecturers`, `class_sections`, `enrollments`.
- Ràng buộc toàn vẹn: Primary Key, Foreign Key, Unique, Check constraint.
- Dữ liệu mẫu seed chuẩn xác nhận số lượng bản ghi.
- Các câu lệnh truy vấn SQL từ cơ bản đến nâng cao (JOIN, GROUP BY, HAVING, Subquery).
- Xây dựng View tổng hợp `v_section_summary` phục vụ tra cứu sức chứa và số lượng đăng ký.

### Buổi 3: Xây dựng Backend REST API với FastAPI & Kiểm thử bằng Postman
- Xây dựng Backend API bằng **FastAPI**, kết nối cơ sở dữ liệu **PostgreSQL** qua **SQLAlchemy Core** và driver **psycopg**.
- Không ghi mật khẩu trong mã nguồn; sử dụng biến môi trường với file `backend/.env`.
- Triển khai đầy đủ các endpoint CRUD và nghiệp vụ:
  - `GET /`: Kiểm tra hoạt động Backend.
  - `GET /health`: Kiểm tra kết nối CSDL PostgreSQL.
  - `GET /courses`: Danh sách học phần, tìm kiếm từ khóa `q`, phân trang với `skip` và `limit` (*Bài 4*).
  - `GET /courses/{course_code}`: Chi tiết một học phần (xử lý 404).
  - `GET /lecturers`: Danh sách giảng viên theo `id` tăng dần (*Bài 1*).
  - `GET /sections`: Danh sách lớp học phần qua view `v_section_summary` (lọc `available_only`).
  - `GET /sections/{section_id}`: Chi tiết lớp học phần (*Bài 2*).
  - `PATCH /sections/{section_id}/capacity`: Cập nhật sức chứa lớp học phần có kiểm tra xung đột số lượng đã đăng ký (*Bài 3*).
  - `GET /students/{student_id}/enrollments`: Danh sách đăng ký của sinh viên.
  - `POST /enrollments`: Đăng ký lớp học phần mới với Pydantic validation (xử lý 201, 404, 409, 422).
  - `DELETE /enrollments/{student_id}/{class_section_id}`: Hủy đăng ký lớp học phần (xử lý 204, 404).
- Tài liệu API tương tác tự động Swagger UI tại `http://127.0.0.1:8000/docs`.
- Bộ sưu tập kiểm thử Postman hoàn chỉnh (`postman/CourseHub_Buoi_3.postman_collection.json` và `postman/CourseHub_Local.postman_environment.json`) gồm 23 kịch bản kiểm thử có assertion tự động.

---

## Hướng Dẫn Chạy Nhanh

1. **Khởi chạy Backend:**
   ```powershell
   .venv\Scripts\Activate.ps1
   python -m uvicorn backend.app.main:app --reload
   ```
2. **Truy cập Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
3. **Kiểm thử với Postman:**
   Import hai tệp trong thư mục `postman/` vào Postman và chạy theo thứ tự từ request `01` đến `23`.

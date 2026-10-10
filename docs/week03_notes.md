# Báo Cáo Thực Hành Buổi 3 - CourseHub

## 1. Mục Tiêu & Kiến Trúc Hệ Thống
- **Mục tiêu:** Xây dựng Backend REST API bằng FastAPI, kết nối cơ sở dữ liệu PostgreSQL (CourseHub từ Buổi 2) qua SQLAlchemy Core, kiểm thử API với Swagger UI và Postman.
- **Công nghệ sử dụng:**
  - **Framework:** FastAPI (0.115+)
  - **Server ASGI:** Uvicorn
  - **Data Validation:** Pydantic (v2)
  - **Database Driver / ORM:** psycopg 3, SQLAlchemy Core (v2.0+)
  - **Database:** PostgreSQL 16
  - **Testing Client:** Swagger UI (`/docs`), Postman Collection

---

## 2. Hướng Dẫn Cài Đặt & Khởi Chạy

### 2.1. Cài đặt môi trường ảo và thư viện
Tại thư mục gốc dự án:
```powershell
# Kích hoạt môi trường ảo
.venv\Scripts\Activate.ps1

# Cài đặt thư viện phụ thuộc
python -m pip install -r backend/requirements.txt
```

### 2.2. Cấu hình biến môi trường
Tạo file `backend/.env` từ mẫu `backend/.env.example`:
```env
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=coursehub
DB_USER=coursehub_user
DB_PASSWORD=your_actual_password
```
> **Lưu ý bảo mật:** File `backend/.env` chứa thông tin nhạy cảm đã được thêm vào `.gitignore` và tuyệt đối không commit lên GitHub.

### 2.3. Khởi chạy Uvicorn Server
```powershell
python -m uvicorn backend.app.main:app --reload
```
- Base URL: `http://127.0.0.1:8000`
- Swagger UI (tài liệu tương tác): `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## 3. Danh Sách Endpoint Hoàn Chỉnh

### 3.1. Nhóm General & Health Check
| Method | Path | Mô tả | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Kiểm tra ứng dụng hoạt động | `200 OK` |
| `GET` | `/health` | Kiểm tra kết nối CSDL (`SELECT 1`) | `200 OK` hoặc `503 Service Unavailable` |

### 3.2. Nhóm Học Phần (Courses)
| Method | Path | Tham số | Mô tả | Status Code |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/courses` | `q`: từ khóa tìm kiếm<br>`skip`: số bản ghi bỏ qua (mặc định 0)<br>`limit`: số bản ghi tối đa (mặc định 10) | Danh sách, tìm kiếm và phân trang học phần (*Bài tập 4*) | `200 OK`, `400 Bad Request` |
| `GET` | `/courses/{course_code}` | `course_code` (path) | Chi tiết một học phần | `200 OK`, `404 Not Found` |

### 3.3. Nhóm Giảng Viên (Lecturers)
| Method | Path | Mô tả | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/lecturers` | Danh sách giảng viên sắp xếp theo `id` tăng dần (*Bài tập 1*) | `200 OK` |

### 3.4. Nhóm Lớp Học Phần (Sections)
| Method | Path | Tham số / Body | Mô tả | Status Code |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/sections` | `available_only: bool` (query) | Lấy danh sách lớp học phần từ view `v_section_summary` | `200 OK` |
| `GET` | `/sections/{section_id}` | `section_id` (path) | Chi tiết lớp học phần gồm học phần, học kỳ, GV, sức chứa (*Bài tập 2*) | `200 OK`, `404 Not Found` |
| `PATCH` | `/sections/{section_id}/capacity` | Body: `{"capacity": int}` | Cập nhật sức chứa của lớp; từ chối nếu nhỏ hơn số đã đăng ký (*Bài tập 3*) | `200 OK`, `404 Not Found`, `409 Conflict` |

### 3.5. Nhóm Đăng Ký (Enrollments)
| Method | Path | Tham số / Body | Mô tả | Status Code |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/students/{student_id}/enrollments` | `student_id` (path) | Danh sách các lớp sinh viên đã đăng ký | `200 OK`, `404 Not Found` |
| `POST` | `/enrollments` | Body: `{"student_id": "...", "class_section_id": "..."}` | Đăng ký lớp học phần mới (kiểm tra tồn tại SV, lớp, trùng lặp, còn chỗ) | `201 Created`, `404 Not Found`, `409 Conflict`, `422 Unprocessable` |
| `DELETE` | `/enrollments/{student_id}/{class_section_id}` | Path params | Hủy đăng ký một lớp học phần | `204 No Content`, `404 Not Found` |

---

## 4. Kiểm Thử Hệ Thống Với Postman

Bộ sưu tập kiểm thử được lưu trữ tại thư mục `postman/`:
- **Collection:** `postman/CourseHub_Buoi_3.postman_collection.json` (Gồm 23 requests với test script tự động kiểm tra status code và response body).
- **Environment:** `postman/CourseHub_Local.postman_environment.json` (Biến `base_url = http://127.0.0.1:8000`).

### Thứ tự luồng kiểm thử:
1. **01 - 07:** Kiểm tra `/health`, đọc danh sách học phần, tìm kiếm `q=web`, lỗi tìm kiếm rỗng `q=%20%20` (400), phân trang `skip/limit`, xem chi tiết và kiểm tra 404.
2. **08:** Kiểm tra danh sách giảng viên (`GET /lecturers` - Bài 1).
3. **09 - 12:** Lấy toàn bộ lớp học phần, lọc lớp còn chỗ (`available_only=true`), xem chi tiết `WEB-01` (`GET /sections/WEB-01` - Bài 2) và kiểm tra 404 khi không tồn tại.
4. **13 - 16:** Cập nhật sức chứa `WEB-01` lên 4 (200), thử giảm xuống 1 khi đã có 2 SV đăng ký (409 Conflict), khôi phục về sức chứa chuẩn 3 (200), thử mã lớp không tồn tại (404) (*Bài tập 3*).
5. **17 - 18:** Kiểm tra lớp đã đăng ký của sinh viên `22000001` (200) và sinh viên không tồn tại (404).
6. **19 - 21:** Đăng ký sinh viên `22000004` vào lớp `WEB-01` (201 Created), thử đăng ký trùng lặp (409 Conflict), thử mã SV không hợp lệ (422 Unprocessable Content).
7. **22 - 23:** Hủy đăng ký thử vừa tạo (204 No Content - khôi phục dữ liệu ban đầu), thử hủy lại lần nữa để kiểm tra 404.

> **Kết quả sau kiểm thử:** Dữ liệu cơ sở dữ liệu giữ nguyên đúng chuẩn 4 sinh viên, 3 học phần, 4 lớp học phần, 5 đăng ký và lớp `WEB-01` có sức chứa là 3.

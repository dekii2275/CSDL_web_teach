# CourseHub Week 07 - Release Candidate

## 1. Spec / Implementation
- **Branch**: `week07-release-candidate`
- **Target Branch**: `main` (hoặc `week06-docker-ci`)
- **Reviewer**: Thành viên nhóm / Giảng viên hướng dẫn
- **Feature Overview**: Bổ sung bộ lọc tùy chọn `available_only` và `course_code` cho endpoint `GET /sections` của CourseHub, chuyển việc lọc từ client sang server và giữ tương thích ngược 100%.
- **Acceptance Criteria Verification**:
  - `AC1` (Không tham số): **PASS** - Trả về đầy đủ 5 lớp, thứ tự `v_section_summary` không đổi.
  - `AC2` (`available_only=true`): **PASS** - Loại bỏ lớp `DM-01` (`remaining=0`), chỉ còn 4 lớp còn chỗ.
  - `AC3` (`course_code` case-insensitive & trim): **PASS** - Khớp chính xác `int2204` $\rightarrow$ 3 lớp học phần `INT2204`.
  - `AC4` (Kết quả rỗng `INT9999`): **PASS** - Trả về `[]` kèm HTTP 200, không đổi thành 404.
  - `AC5` (Bất biến CSDL & Nghiệp vụ): **PASS** - Giữ nguyên schema, view, transaction và row-lock `FOR UPDATE`.
  - `AC6` (React Checkbox): **PASS** - Bấm checkbox kích hoạt `GET /api/sections?available_only=true` lên Nginx/FastAPI.
- **Diff quan trọng**:
  - `backend/app/section_filters.py`: Hàm lọc thuần Python độc lập với CSDL.
  - `backend/app/main.py`: Chèn 17 dòng code bổ sung tham số cho route `GET /sections`.
  - `frontend/src/App.jsx`: Thêm `sectionsPath` động, đưa `onlyAvailable` vào useEffect dependencies, bỏ lọc local trong `rows`.

---

## 2. Testing & Verification Evidence
- **pytest backend/tests -v**: **8 passed in 2.68s**
  - 2 bài test hợp đồng OpenAPI Buổi 6 (`test_openapi_contract.py`).
  - 6 bài unit test mới không cần CSDL (`test_section_filters.py`).
- **npm test (frontend)**: **8 passed / 0 failed** (100% kịch bản mock API).
- **npm run build**: **Built in 839ms** (31 modules transformed, tạo bundle Vite production).
- **Docker Compose & Smoke script**:
  - `docker compose ps`: Cả hai service `backend` (healthy) và `frontend` (Up) trên cổng 8080.
  - `python scripts/smoke_release.py`:
    - `PASS GET /api/health (HTTP 200 + JSON object)`
    - `PASS GET /api/sections?available_only=true (4 lớp)`
- **Regression Matrix**:
  - `GET /api/sections`: HTTP 200 OK
  - `GET /api/sections?available_only=true`: HTTP 200 OK
  - `POST /api/enrollments` hợp lệ (`22000004` $\rightarrow$ `WEB-02`): **HTTP 201 Created**
  - `DELETE /api/enrollments/22000004/WEB-02`: **HTTP 204 No Content**
  - `POST` với sinh viên không tồn tại (`99999999`): **HTTP 404 Not Found**
  - `POST` vào lớp đã đầy (`DM-01`): **HTTP 409 Conflict**
- **Xác nhận SQL (PostgreSQL Host)**:
  - `v_section_summary`: Sĩ số `enrolled` và `remaining` cập nhật và hoàn tác chính xác.
  - `enrollment_events`: Ghi nhận đầy đủ sự kiện `CREATED` và `CANCELLED`.

---

## 3. AI Usage & Security Review
- **1 đề xuất AI đã sử dụng và xác minh**:
  - Đề xuất hàm `filter_sections(rows, course_code, available_only)`.
  - Cách xác minh: Viết 6 unit test độc lập bao phủ các trường hợp biên (`None`, khoảng trắng thừa, chữ hoa/thường, mảng rỗng `[]`, immutability).
- **1 đề xuất AI đã từ chối và lý do**:
  - AI từng gợi ý đổi route thành `@app.get("/api/sections")` trong FastAPI để "khớp với URL frontend".
  - Lý do từ chối: Sai kiến trúc tầng Nginx reverse proxy. Nginx đã đảm nhiệm map `/api/*` vào `backend:8000/*`; nếu sửa route trong FastAPI sẽ làm hỏng toàn bộ đường dẫn qua Nginx và gây lỗi 404.
- **An toàn bảo mật (Security Gate)**:
  - CourseHub chưa có Authentication/Authorization $\rightarrow$ Tuyệt đối không đưa dữ liệu thật lên Internet.
  - Bổ sung middleware `demo_guard.py`: Khi `DEMO_READ_ONLY=1`, mọi request ghi `POST/DELETE` đều bị chặn với **HTTP 403 Forbidden**.

---

## 4. Release Candidate & Deployment
- **URL Local**: `http://127.0.0.1:8080` (truy cập qua Nginx)
- **API Docs**: `http://127.0.0.1:8000/docs` (OpenAPI Swagger)
- **Tag ứng viên phát hành**: `v0.7.0-rc1`
- **Known issues / Giới hạn**:
  - Lọc dữ liệu bằng Python ở Backend chỉ phù hợp tập dữ liệu vừa/nhỏ. Với dữ liệu lớn cần chuyển sang SQL `WHERE` và phân trang.
  - PostgreSQL vẫn chạy trên host phục vụ môi trường thực hành phòng lab.

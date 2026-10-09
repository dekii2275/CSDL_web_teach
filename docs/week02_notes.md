# CourseHub - Buoi 2

Co so du lieu: coursehub (PostgreSQL).
Thu tu khoi tao: 01_schema.sql -> 02_seed.sql -> 04_views.sql.
03_queries.sql: chay tung truy van de xem ket qua.
05_constraint_checks.sql: chay tung lenh, loi la du kien.
06_view_demo.sql: BEGIN -> INSERT -> SELECT -> ROLLBACK -> SELECT.
Du lieu chuan: 4 sinh vien, 3 hoc phan, 4 lop, 5 dang ky.
WEB-01: 2 dang ky, con 1 cho. WEB-02: 0 dang ky, con 2 cho.

---

## Tom tat cac bang trong co so du lieu:
1. `students`: Quan ly sinh vien (id, name, major, email). Rang buoc UNIQUE email, CHECK do dai id = 8, CHECK trim(name) <> ''.
2. `courses`: Quan ly hoc phan (code, name, credits). Rang buoc CHECK credits BETWEEN 1 AND 6.
3. `semesters`: Quan ly hoc ky (code, name, start_date, end_date). Rang buoc CHECK end_date >= start_date.
4. `lecturers`: Quan ly giang vien (id, name).
5. `class_sections`: Quan ly lop hoc phan (id, course_code, semester_code, lecturer_id, capacity). Khoa ngoai tham chieu toi courses, semesters, lecturers. CHECK capacity > 0.
6. `enrollments`: Quan ly dang ky (student_id, class_section_id, registered_at). Khoa chinh phuc hop (student_id, class_section_id).

## View:
- `v_section_summary`: Tong hop ma lop, ma hoc phan, suc chua, so da dang ky (enrolled) va so cho con lai (remaining).

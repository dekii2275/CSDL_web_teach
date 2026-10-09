-- ===============================================================
-- Buoi 2: Thiet ke co so du lieu CourseHub va viet truy van SQL
-- Tep: database/02_seed.sql
-- Muc dich: Nhap bo du lieu mau thong nhat
-- ===============================================================

-- 1/6. Nhap du lieu sinh vien (students)
INSERT INTO students (id, name, major, email) VALUES
('22000001', 'Nguyen Minh Anh', 'KHDL', 'anh@example.com'),
('22000002', 'Tran Duc Long', 'KHDL', 'long@example.com'),
('22000003', 'Pham Thu Ha', 'KHDL', 'ha@example.com'),
('22000004', 'Le Hoang Nam', 'KHDL', 'nam@example.com');

-- 2/6. Nhap du lieu hoc phan (courses)
INSERT INTO courses (code, name, credits) VALUES
('INT2204', 'Co so du lieu Web va he thong thong tin', 3),
('INT2205', 'Khai pha du lieu', 3),
('INT2206', 'Lap trinh Python', 2);

-- 3/6. Nhap du lieu hoc ky (semesters)
INSERT INTO semesters (code, name, start_date, end_date) VALUES
('2026-1', 'Hoc ky I - 2026', '2026-09-01', '2027-01-31');

-- 4/6. Nhap du lieu giang vien (lecturers)
INSERT INTO lecturers (id, name) VALUES
('GV01', 'Nguyen Thu Lan'),
('GV02', 'Le Minh Son');

-- 5/6. Nhap du lieu lop hoc phan (class_sections)
INSERT INTO class_sections (id, course_code, semester_code, lecturer_id, capacity) VALUES
('WEB-01', 'INT2204', '2026-1', 'GV01', 3),
('WEB-02', 'INT2204', '2026-1', 'GV01', 2),
('DM-01', 'INT2205', '2026-1', 'GV02', 2),
('PY-01', 'INT2206', '2026-1', 'GV02', 2);

-- 6/6. Nhap du lieu dang ky lop hoc phan (enrollments)
INSERT INTO enrollments (student_id, class_section_id) VALUES
('22000001', 'WEB-01'),
('22000002', 'WEB-01'),
('22000001', 'DM-01'),
('22000003', 'DM-01'),
('22000003', 'PY-01');

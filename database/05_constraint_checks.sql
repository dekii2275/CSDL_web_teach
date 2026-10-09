-- ===============================================================
-- Buoi 2: Thiet ke co so du lieu CourseHub va viet truy van SQL
-- Tep: database/05_constraint_checks.sql
-- Muc dich: Cac lenh co y nhap sai de kiem tra rang buoc toan ven
-- Luu y: Chay tung lenh mot tren Query Tool de quan sat thong bao loi
-- ===============================================================

-- 1. Dang ky trung mot lop (Vi pham PRIMARY KEY pk_enrollments: duplicate key value)
INSERT INTO enrollments (student_id, class_section_id)
VALUES ('22000001', 'WEB-01');

-- 2. Dang ky cho sinh vien khong ton tai (Vi pham FOREIGN KEY: violates foreign key constraint)
INSERT INTO enrollments (student_id, class_section_id)
VALUES ('22999999', 'WEB-01');

-- 3. Doi suc chua lop thanh 0 (Vi pham CHECK constraint ck_sections_capacity)
UPDATE class_sections
SET capacity = 0
WHERE id = 'WEB-01';

-- 4. Bo trong so tin chi (Vi pham NOT NULL constraint: violates not-null constraint)
UPDATE courses
SET credits = NULL
WHERE code = 'INT2204';

-- 5. Dung lai email cua sinh vien khac (Vi pham UNIQUE constraint uq_students_email)
UPDATE students
SET email = 'anh@example.com'
WHERE id = '22000002';

-- 6. Nhap ho ten chi gom dau cach (Vi pham CHECK ck_students_name: trim(name) <> '')
UPDATE students
SET name = ' '
WHERE id = '22000004';

-- 7. Kiem tra du lieu sau cac lan bi tu choi (Tong so dang ky van phai la 5)
SELECT COUNT(*) AS total_enrollments
FROM enrollments;

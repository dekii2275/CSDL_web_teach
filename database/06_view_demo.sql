-- ===============================================================
-- Buoi 2: Thiet ke co so du lieu CourseHub va viet truy van SQL
-- Tep: database/06_view_demo.sql
-- Muc dich: Quan sat view khi co dang ky moi va hoan tac (Transaction Demo)
-- Luu y: Chay tung buoc tren cung mot tab Query Tool cua pgAdmin
-- ===============================================================

-- Buoc 1: Bat dau giao dich
BEGIN;

-- Buoc 2: Them thu mot dang ky moi (Hoang Nam dang ky WEB-01)
INSERT INTO enrollments (student_id, class_section_id)
VALUES ('22000004', 'WEB-01');

-- Buoc 3: Xem so luong thay doi tuc thi trong view (enrolled tang len 3, remaining ve 0)
SELECT class_id, capacity, enrolled, remaining
FROM v_section_summary
WHERE class_id = 'WEB-01';

-- Buoc 4: Huy giao dich thu nghiem de tra lai trang thai du lieu chuan
ROLLBACK;

-- Buoc 5: Kiem tra lai view sau khi rollback (enrolled tro ve 2, remaining la 1)
SELECT class_id, capacity, enrolled, remaining
FROM v_section_summary
WHERE class_id = 'WEB-01';

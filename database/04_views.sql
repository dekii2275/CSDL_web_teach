-- ===============================================================
-- Buoi 2: Thiet ke co so du lieu CourseHub va viet truy van SQL
-- Tep: database/04_views.sql
-- Muc dich: Tao va khai thac view tong hop lop (v_section_summary)
-- ===============================================================

-- 1. Tao view tong hop thong tin lop hoc phan
CREATE OR REPLACE VIEW v_section_summary AS
SELECT cs.id AS class_id,
       cs.course_code,
       cs.capacity,
       COUNT(e.student_id) AS enrolled,
       cs.capacity - COUNT(e.student_id) AS remaining
FROM class_sections AS cs
LEFT JOIN enrollments AS e ON e.class_section_id = cs.id
GROUP BY cs.id, cs.course_code, cs.capacity;

-- 2. Xem thong tin tat ca cac lop qua view
SELECT class_id, course_code, capacity, enrolled, remaining
FROM v_section_summary
ORDER BY class_id;

-- 3. Loc cac lop con cho tu view
SELECT class_id, remaining
FROM v_section_summary
WHERE remaining > 0
ORDER BY class_id;

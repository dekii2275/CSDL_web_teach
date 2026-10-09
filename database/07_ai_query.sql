-- ===============================================================
-- Buoi 2: Thiet ke co so du lieu CourseHub va viet truy van SQL
-- Tep: database/07_ai_query.sql
-- Muc dich: Doi chieu truy van AI de xuat dem sai va cach sua
-- ===============================================================

-- ---------------------------------------------------------------
-- 1. Truy van chay duoc nhung dem sai (AI de xuat dung COUNT(*))
-- Giai thich: LEFT JOIN giu lai dong lop WEB-02 du e.* deu NULL.
-- COUNT(*) dem so dong duoc giu lai, tra ve 1 (SAI nghiep vu vi chua ai dang ky).
-- ---------------------------------------------------------------
SELECT cs.id, COUNT(*) AS enrolled
FROM class_sections AS cs
LEFT JOIN enrollments AS e ON e.class_section_id = cs.id
WHERE cs.id = 'WEB-02'
GROUP BY cs.id;

-- ---------------------------------------------------------------
-- 2. Truy van da sua (Dung COUNT(e.student_id))
-- Giai thich: COUNT(cot) bo qua cac gia tri NULL, tra ve dung 0 cho WEB-02.
-- ---------------------------------------------------------------
SELECT cs.id, COUNT(e.student_id) AS enrolled
FROM class_sections AS cs
LEFT JOIN enrollments AS e ON e.class_section_id = cs.id
WHERE cs.id = 'WEB-02'
GROUP BY cs.id;

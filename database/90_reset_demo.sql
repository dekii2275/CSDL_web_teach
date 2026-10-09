-- ===============================================================
-- Buoi 2: Thiet ke co so du lieu CourseHub va viet truy van SQL
-- Tep: database/90_reset_demo.sql
-- Muc dich: Xoa sach cac bang va view khi can dung lai bo du lieu demo
-- Luu y: Chi chay khi can reset toan bo ve trang thai rong
-- ===============================================================

BEGIN;
DROP VIEW IF EXISTS v_section_summary;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS class_sections;
DROP TABLE IF EXISTS lecturers;
DROP TABLE IF EXISTS semesters;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
COMMIT;

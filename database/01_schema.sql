-- ===============================================================
-- Buoi 2: Thiet ke co so du lieu CourseHub va viet truy van SQL
-- Tep: database/01_schema.sql
-- Muc dich: Tao sau bang va cac rang buoc toan ven
-- ===============================================================

-- 1/6. Bang sinh vien (students)
CREATE TABLE students (
    id VARCHAR(8) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    major VARCHAR(20) NOT NULL,
    email VARCHAR(120) NOT NULL,
    CONSTRAINT uq_students_email UNIQUE (email),
    CONSTRAINT ck_students_id CHECK (length(id) = 8),
    CONSTRAINT ck_students_name CHECK (trim(name) <> '')
);

-- 2/6. Bang hoc phan (courses)
CREATE TABLE courses (
    code VARCHAR(10) NOT NULL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    credits INTEGER NOT NULL,
    CONSTRAINT ck_courses_credits CHECK (credits BETWEEN 1 AND 6)
);

-- 3/6. Bang hoc ky (semesters)
CREATE TABLE semesters (
    code VARCHAR(10) NOT NULL PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    CONSTRAINT ck_semesters_dates CHECK (end_date >= start_date)
);

-- 4/6. Bang giang vien (lecturers)
CREATE TABLE lecturers (
    id VARCHAR(10) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- 5/6. Bang lop hoc phan (class_sections)
CREATE TABLE class_sections (
    id VARCHAR(20) NOT NULL PRIMARY KEY,
    course_code VARCHAR(10) NOT NULL REFERENCES courses(code),
    semester_code VARCHAR(10) NOT NULL REFERENCES semesters(code),
    lecturer_id VARCHAR(10) NOT NULL REFERENCES lecturers(id),
    capacity INTEGER NOT NULL,
    CONSTRAINT ck_sections_capacity CHECK (capacity > 0)
);

-- 6/6. Bang dang ky lop hoc phan (enrollments)
CREATE TABLE enrollments (
    student_id VARCHAR(8) NOT NULL REFERENCES students(id),
    class_section_id VARCHAR(20) NOT NULL REFERENCES class_sections(id),
    registered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_enrollments PRIMARY KEY (student_id, class_section_id)
);

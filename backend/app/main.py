from __future__ import annotations

import logging
from typing import Annotated, Any

from fastapi import FastAPI, HTTPException, Query, Response, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from .database import engine
from .schemas import (
    CapacityUpdate,
    CapacityUpdateResponse,
    CourseResponse,
    EnrollmentCreate,
    EnrollmentCreateResponse,
    HealthResponse,
    LecturerResponse,
    MessageResponse,
    SectionDetailResponse,
    SectionSummaryResponse,
    StudentEnrollmentResponse,
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="CourseHub API",
    version="0.3.0",
    description="API thực hành Buổi 3 - Cơ sở dữ liệu Web và hệ thống thông tin",
    openapi_tags=[
        {"name": "General", "description": "Kiểm tra hệ thống và trạng thái kết nối"},
        {"name": "Courses", "description": "Quản lý thông tin học phần"},
        {"name": "Lecturers", "description": "Quản lý thông tin giảng viên"},
        {"name": "Sections", "description": "Quản lý lớp học phần và sức chứa"},
        {"name": "Enrollments", "description": "Đăng ký và hủy đăng ký lớp học phần"},
    ],
)


@app.get(
    "/",
    response_model=MessageResponse,
    tags=["General"],
    summary="Kiểm tra ứng dụng hoạt động",
)
def read_root() -> dict[str, str]:
    """Trả về thông báo xác nhận ứng dụng CourseHub API đang hoạt động."""
    return {"message": "CourseHub API dang hoat dong"}


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["General"],
    summary="Kiểm tra kết nối cơ sở dữ liệu",
)
def health_check() -> dict[str, str]:
    """Kiểm tra kết nối tới cơ sở dữ liệu PostgreSQL qua truy vấn SELECT 1."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        logger.exception("Khong ket noi duoc co so du lieu")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Khong ket noi duoc co so du lieu",
        ) from exc
    return {"status": "ok", "database": "connected"}


@app.get(
    "/courses",
    response_model=list[CourseResponse],
    tags=["Courses"],
    summary="Danh sách và tìm kiếm học phần (có phân trang)",
)
def list_courses(
    q: Annotated[
        str | None,
        Query(
            min_length=1,
            description="Từ khóa tìm kiếm theo mã hoặc tên học phần",
        ),
    ] = None,
    skip: Annotated[
        int,
        Query(
            ge=0,
            description="Số lượng bản ghi bỏ qua (skip >= 0)",
        ),
    ] = 0,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=100,
            description="Số lượng bản ghi tối đa lấy về (1 <= limit <= 100)",
        ),
    ] = 10,
) -> list[dict[str, Any]]:
    """Lấy danh sách học phần, hỗ trợ tìm kiếm từ khóa và phân trang bằng skip/limit."""
    sql = """
        SELECT code, name, credits
        FROM courses
    """
    parameters: dict[str, Any] = {
        "skip": skip,
        "limit": limit,
    }

    if q is not None:
        keyword = q.strip().lower()
        if not keyword:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tu khoa tim kiem khong duoc rong",
            )
        sql += """
            WHERE LOWER(code) LIKE :keyword
               OR LOWER(name) LIKE :keyword
        """
        parameters["keyword"] = f"%{keyword}%"

    sql += " ORDER BY code LIMIT :limit OFFSET :skip"

    with engine.connect() as connection:
        rows = connection.execute(text(sql), parameters).mappings().all()

    return [dict(row) for row in rows]


@app.get(
    "/courses/{course_code}",
    response_model=CourseResponse,
    tags=["Courses"],
    summary="Xem chi tiết một học phần",
)
def get_course(course_code: str) -> dict[str, Any]:
    """Xem thông tin chi tiết học phần theo mã học phần (không phân biệt hoa thường)."""
    sql = """
        SELECT code, name, credits
        FROM courses
        WHERE code = :course_code
    """

    with engine.connect() as connection:
        row = connection.execute(
            text(sql),
            {"course_code": course_code.upper()},
        ).mappings().first()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khong tim thay hoc phan",
        )

    return dict(row)


@app.get(
    "/lecturers",
    response_model=list[LecturerResponse],
    tags=["Lecturers"],
    summary="Danh sách giảng viên",
)
def list_lecturers() -> list[dict[str, Any]]:
    """Bài tập 1: Lấy danh sách giảng viên sắp xếp theo id tăng dần."""
    sql = """
        SELECT id, name
        FROM lecturers
        ORDER BY id
    """
    with engine.connect() as connection:
        rows = connection.execute(text(sql)).mappings().all()

    return [dict(row) for row in rows]


@app.get(
    "/sections",
    response_model=list[SectionSummaryResponse],
    tags=["Sections"],
    summary="Danh sách lớp học phần",
)
def list_sections(
    available_only: Annotated[
        bool,
        Query(
            description="Chỉ lấy các lớp học phần còn chỗ trống (remaining > 0)",
        ),
    ] = False,
) -> list[dict[str, Any]]:
    """Lấy danh sách các lớp học phần từ view v_section_summary."""
    sql = """
        SELECT class_id, course_code, capacity, enrolled, remaining
        FROM v_section_summary
    """

    if available_only:
        sql += " WHERE remaining > 0"

    sql += " ORDER BY class_id"

    with engine.connect() as connection:
        rows = connection.execute(text(sql)).mappings().all()

    return [dict(row) for row in rows]


@app.get(
    "/sections/{section_id}",
    response_model=SectionDetailResponse,
    tags=["Sections"],
    summary="Xem chi tiết một lớp học phần",
)
def get_section(section_id: str) -> dict[str, Any]:
    """Bài tập 2: Lấy thông tin chi tiết của một lớp học phần bao gồm học phần, học kỳ, giảng viên và sức chứa."""
    sql = """
        SELECT cs.id AS class_id,
               cs.course_code,
               c.name AS course_name,
               cs.semester_code,
               sem.name AS semester_name,
               cs.lecturer_id,
               l.name AS lecturer_name,
               cs.capacity,
               COALESCE(v.enrolled, 0) AS enrolled,
               COALESCE(v.remaining, cs.capacity) AS remaining
        FROM class_sections AS cs
        JOIN courses AS c ON c.code = cs.course_code
        JOIN semesters AS sem ON sem.code = cs.semester_code
        JOIN lecturers AS l ON l.id = cs.lecturer_id
        LEFT JOIN v_section_summary AS v ON v.class_id = cs.id
        WHERE cs.id = :section_id
    """

    with engine.connect() as connection:
        row = connection.execute(
            text(sql),
            {"section_id": section_id.upper()},
        ).mappings().first()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khong tim thay lop hoc phan",
        )

    return dict(row)


@app.patch(
    "/sections/{section_id}/capacity",
    response_model=CapacityUpdateResponse,
    tags=["Sections"],
    summary="Cập nhật sức chứa của lớp học phần",
)
def update_section_capacity(
    section_id: str,
    payload: CapacityUpdate,
) -> dict[str, Any]:
    """Bài tập 3: Cập nhật sức chứa của lớp học phần; không cho phép sức chứa nhỏ hơn số lượng đã đăng ký."""
    normalized_section_id = section_id.upper()

    section_sql = """
        SELECT cs.id,
               cs.capacity,
               COUNT(e.student_id) AS enrolled
        FROM class_sections AS cs
        LEFT JOIN enrollments AS e ON e.class_section_id = cs.id
        WHERE cs.id = :section_id
        GROUP BY cs.id, cs.capacity
    """

    update_sql = """
        UPDATE class_sections
        SET capacity = :capacity
        WHERE id = :section_id
    """

    with engine.begin() as connection:
        section = connection.execute(
            text(section_sql),
            {"section_id": normalized_section_id},
        ).mappings().first()

        if section is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Khong tim thay lop hoc phan",
            )

        enrolled = int(section["enrolled"])
        if payload.capacity < enrolled:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Suc chua moi ({payload.capacity}) khong duoc nho hon so sinh vien da dang ky ({enrolled})",
            )

        connection.execute(
            text(update_sql),
            {
                "capacity": payload.capacity,
                "section_id": normalized_section_id,
            },
        )

    return {
        "message": "Cap nhat suc chua thanh cong",
        "class_id": normalized_section_id,
        "capacity": payload.capacity,
        "enrolled": enrolled,
        "remaining": payload.capacity - enrolled,
    }


@app.get(
    "/students/{student_id}/enrollments",
    response_model=list[StudentEnrollmentResponse],
    tags=["Enrollments"],
    summary="Danh sách lớp đã đăng ký của một sinh viên",
)
def list_student_enrollments(student_id: str) -> list[dict[str, Any]]:
    """Lấy danh sách các lớp học phần mà một sinh viên đã đăng ký thành công."""
    student_sql = "SELECT id FROM students WHERE id = :student_id"
    enrollment_sql = """
        SELECT e.student_id,
               s.name AS student_name,
               cs.id AS class_section_id,
               c.code AS course_code,
               c.name AS course_name,
               e.registered_at
        FROM enrollments AS e
        JOIN students AS s ON s.id = e.student_id
        JOIN class_sections AS cs ON cs.id = e.class_section_id
        JOIN courses AS c ON c.code = cs.course_code
        WHERE e.student_id = :student_id
        ORDER BY cs.id
    """
    with engine.connect() as connection:
        student = connection.execute(
            text(student_sql),
            {"student_id": student_id},
        ).first()

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Khong tim thay sinh vien",
            )

        rows = connection.execute(
            text(enrollment_sql),
            {"student_id": student_id},
        ).mappings().all()

    return [dict(row) for row in rows]


@app.post(
    "/enrollments",
    response_model=EnrollmentCreateResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"],
    summary="Tạo đăng ký lớp học phần mới",
)
def create_enrollment(payload: EnrollmentCreate) -> dict[str, str]:
    """Tạo một đăng ký lớp học phần mới từ JSON body."""
    student_sql = "SELECT id FROM students WHERE id = :student_id"
    section_sql = """
        SELECT cs.id,
               cs.capacity,
               COUNT(e.student_id) AS enrolled
        FROM class_sections AS cs
        LEFT JOIN enrollments AS e ON e.class_section_id = cs.id
        WHERE cs.id = :class_section_id
        GROUP BY cs.id, cs.capacity
    """
    duplicate_sql = """
        SELECT 1
        FROM enrollments
        WHERE student_id = :student_id
          AND class_section_id = :class_section_id
    """
    insert_sql = """
        INSERT INTO enrollments (student_id, class_section_id)
        VALUES (:student_id, :class_section_id)
    """
    parameters = {
        "student_id": payload.student_id,
        "class_section_id": payload.class_section_id,
    }

    with engine.begin() as connection:
        student = connection.execute(
            text(student_sql),
            {"student_id": payload.student_id},
        ).first()
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Khong tim thay sinh vien",
            )

        section = connection.execute(
            text(section_sql),
            {"class_section_id": payload.class_section_id},
        ).mappings().first()
        if section is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Khong tim thay lop hoc phan",
            )

        duplicated = connection.execute(
            text(duplicate_sql),
            parameters,
        ).first()
        if duplicated is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Sinh vien da dang ky lop nay",
            )

        if int(section["enrolled"]) >= int(section["capacity"]):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Lop hoc phan da het cho",
            )

        connection.execute(text(insert_sql), parameters)

    return {
        "message": "Dang ky thanh cong",
        "student_id": payload.student_id,
        "class_section_id": payload.class_section_id,
    }


@app.delete(
    "/enrollments/{student_id}/{class_section_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Enrollments"],
    summary="Hủy đăng ký lớp học phần",
)
def delete_enrollment(student_id: str, class_section_id: str) -> Response:
    """Hủy một đăng ký lớp học phần theo mã sinh viên và mã lớp."""
    sql = """
        DELETE FROM enrollments
        WHERE student_id = :student_id
          AND class_section_id = :class_section_id
    """
    with engine.begin() as connection:
        result = connection.execute(
            text(sql),
            {
                "student_id": student_id,
                "class_section_id": class_section_id,
            },
        )
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Khong tim thay dang ky can huy",
            )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

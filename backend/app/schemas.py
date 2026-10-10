from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class EnrollmentCreate(BaseModel):
    student_id: str = Field(
        min_length=8,
        max_length=8,
        description="Mã sinh viên gồm đúng 8 ký tự",
        examples=["22000004"],
    )
    class_section_id: str = Field(
        min_length=1,
        max_length=20,
        description="Mã lớp học phần",
        examples=["WEB-01"],
    )


class CapacityUpdate(BaseModel):
    capacity: int = Field(
        gt=0,
        description="Sức chứa mới của lớp học phần (phải lớn hơn 0)",
        examples=[4],
    )


class MessageResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str
    database: str


class CourseResponse(BaseModel):
    code: str
    name: str
    credits: int


class LecturerResponse(BaseModel):
    id: str
    name: str


class SectionSummaryResponse(BaseModel):
    class_id: str
    course_code: str
    capacity: int
    enrolled: int
    remaining: int


class SectionDetailResponse(BaseModel):
    class_id: str
    course_code: str
    course_name: str
    semester_code: str
    semester_name: str
    lecturer_id: str
    lecturer_name: str
    capacity: int
    enrolled: int
    remaining: int


class CapacityUpdateResponse(BaseModel):
    message: str
    class_id: str
    capacity: int
    enrolled: int
    remaining: int


class StudentEnrollmentResponse(BaseModel):
    student_id: str
    student_name: str
    class_section_id: str
    course_code: str
    course_name: str
    registered_at: datetime | str


class EnrollmentCreateResponse(BaseModel):
    message: str
    student_id: str
    class_section_id: str

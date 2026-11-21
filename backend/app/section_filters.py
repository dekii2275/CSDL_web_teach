"""Bộ lọc thuần Python cho kết quả GET /sections của CourseHub (Buổi 7)."""
from typing import Any, Mapping


def filter_sections(
    rows: list[Mapping[str, Any]],
    *,
    course_code: str | None = None,
    available_only: bool = False,
) -> list[Mapping[str, Any]]:
    """Giữ thứ tự nguồn; không sửa dữ liệu và không ghi database."""
    code = (course_code or "").strip().upper()
    return [
        row for row in rows
        if (not code or str(row["course_code"]).upper() == code)
        and (not available_only or int(row["remaining"]) > 0)
    ]

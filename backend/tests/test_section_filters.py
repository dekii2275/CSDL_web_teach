"""Test bộ lọc không cần PostgreSQL, Docker hoặc HTTP."""
from backend.app.section_filters import filter_sections

ROWS = [
    {"class_id": "WEB-01", "course_code": "INT2204", "remaining": 0},
    {"class_id": "WEB-02", "course_code": "INT2204", "remaining": 2},
    {"class_id": "DM-01", "course_code": "INT2205", "remaining": 1},
]


def ids(rows):
    return [row["class_id"] for row in rows]


def test_default_preserves_current_response_and_order():
    assert ids(filter_sections(ROWS)) == ["WEB-01", "WEB-02", "DM-01"]


def test_available_only_excludes_full_sections():
    assert ids(filter_sections(ROWS, available_only=True)) == ["WEB-02", "DM-01"]


def test_course_code_matches_case_insensitively():
    assert ids(filter_sections(ROWS, course_code=" int2204 ")) == ["WEB-01", "WEB-02"]


def test_combined_filters():
    assert ids(filter_sections(ROWS, course_code="INT2204", available_only=True)) == ["WEB-02"]


def test_empty_result_is_valid():
    assert filter_sections(ROWS, course_code="INT9999") == []


def test_source_data_is_not_modified():
    snapshot = [row.copy() for row in ROWS]
    filter_sections(ROWS, available_only=True)
    assert ROWS == snapshot

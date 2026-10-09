"""
CourseHub - Buoi 1: Tong quan he thong thong tin Web
On tap Python - Git/GitHub va cong cu AI ho tro lap trinh
TS. Vu Tien Dung - Pham Duy Phuong
"""

import sys

# Ho tro in ky tu Unicode tren Windows console neu can
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

print("CourseHub - Buoi 1")

# ==========================================
# 1. MO PHONG DU LIEU BANG LIST VA DICTIONARY (Muc III.3)
# ==========================================

students = [
    {"id": "22000001", "name": "Nguyen Minh Anh", "major": "KHDL"},
    {"id": "22000002", "name": "Tran Duc Long", "major": "KHDL"},
]

courses = [
    {
        "code": "INT2204",
        "name": "Co so du lieu Web va he thong thong tin",
        "capacity": 3,
        "enrolled": 2,
    },
    {
        "code": "INT2205",
        "name": "Khai pha du lieu",
        "capacity": 2,
        "enrolled": 2,
    },
]

enrollments = [
    {"student_id": "22000001", "course_code": "INT2204"}
]

# ==========================================
# 2. DUYET DU LIEU VA TINH GIA TRI (Muc III.4)
# ==========================================

print("\n--- DUYET DANH SACH HOC PHAN ---")
for course in courses:
    remaining = course["capacity"] - course["enrolled"]
    print(course["code"], "- con", remaining, "cho")


# ==========================================
# 3. TACH XU LY THANH HAM (Muc III.5)
# ==========================================

def find_student(student_id):
    """Tim sinh vien theo ma sinh vien."""
    for student in students:
        if student["id"] == student_id:
            return student
    return None

def find_course(course_code):
    """Tim hoc phan theo ma hoc phan."""
    for course in courses:
        if course["code"] == course_code:
            return course
    return None

print("\n--- TIM HOC PHAN THEO MA ---")
print("find_course('INT2204'):", find_course("INT2204"))


# ==========================================
# 4. MO PHONG QUY TAC DANG KY (Muc III.6)
# ==========================================

def can_enroll(student_id, course_code):
    """
    Kiem tra cac quy tac nghiep vu khi dang ky hoc phan:
    1. Sinh vien co ton tai trong he thong khong
    2. Hoc phan co ton tai khong
    3. Lop hoc phan con cho trong khong
    4. Sinh vien da dang ky hoc phan nay truoc do chua
    """
    student = find_student(student_id)
    if student is None:
        return False, "Sinh vien khong ton tai"

    course = find_course(course_code)
    if course is None:
        return False, "Hoc phan khong ton tai"

    duplicated = any(
        item["student_id"] == student_id and item["course_code"] == course_code
        for item in enrollments
    )
    if duplicated:
        return False, "Sinh vien da dang ky hoc phan nay"

    if course["enrolled"] >= course["capacity"]:
        return False, "Lop da du so luong"

    return True, "Co the dang ky"

print("\n--- KIEM TRA DIEU KIEN DANG KY (can_enroll) ---")
print("can_enroll('22000002', 'INT2204'):", can_enroll("22000002", "INT2204"))


# ==========================================
# 5. XU LY DU LIEU NHAP SAI (Muc III.7)
# ==========================================

def demo_input_limit():
    """Minh hoa xu ly ngoai le try/except khi chuyen doi kieu du lieu."""
    print("\n--- XU LY DU LIEU NHAP SAI (TRY/EXCEPT) ---")
    if sys.stdin.isatty():
        try:
            limit = int(input("Nhap so luong hoc phan muon hien thi: "))
            print(courses[:limit])
        except ValueError:
            print("So luong phai la so nguyen")
    else:
        # Chay mo phong voi cac gia tri thu nghiem
        test_inputs = ["1", "abc"]
        for raw_val in test_inputs:
            print(f"Thu nghiem nhap gia tri '{raw_val}':")
            try:
                limit = int(raw_val)
                print(" -> Ket qua:", courses[:limit])
            except ValueError:
                print(" -> So luong phai la so nguyen")


# ==========================================
# 6. HAM TIM KIEM HOC PHAN (Muc III.8)
# ==========================================

def search_courses(keyword):
    """Tim kiem hoc phan theo ma hoac ten, khong phan biet hoa thuong."""
    normalized = keyword.strip().lower()
    results = []
    for course in courses:
        code = course["code"].lower()
        name = course["name"].lower()
        if normalized in code or normalized in name:
            results.append(course)
    return results

print("\n--- TIM KIEM HOC PHAN (search_courses) ---")
print("search_courses('web'):", search_courses("web"))


# ==========================================
# 7. BAI TAP TU LUYEN (Muc VII.1 & VII.2)
# ==========================================

def enroll_student(student_id, course_code):
    """
    Hoan thien ham dang ky hoc phan:
    - Kiem tra sinh vien ton tai, hoc phan ton tai, lop con cho, sinh vien chua dang ky trung.
    - Neu dang ky thanh cong: them ban ghi moi vao enrollments va cap nhat enrolled cua hoc phan.
    """
    eligible, message = can_enroll(student_id, course_code)
    if not eligible:
        return False, message

    # Dang ky thanh cong: them vao danh sach va cap nhat so luong
    enrollments.append({
        "student_id": student_id,
        "course_code": course_code
    })

    course = find_course(course_code)
    course["enrolled"] += 1

    return True, f"Dang ky thanh cong hoc phan {course_code} cho sinh vien {student_id}"


def run_tests():
    """Kiem tra chuong trinh voi toi thieu 05 tinh huong chay thu (Muc VII.2)."""
    print("\n==========================================")
    print("CHAY KIEM THU 05 TINH HUONG (VII.2)")
    print("==========================================")

    # Tinh huong 1: Dang ky thanh cong
    # SV 22000002 dang ky INT2204 (dang co enrolled=2, capacity=3 => con 1 cho)
    res1, msg1 = enroll_student("22000002", "INT2204")
    print(f"Test 1 [Dang ky thanh cong]       : Result = {res1} | Thong bao: {msg1}")

    # Tinh huong 2: Dang ky trung
    # SV 22000002 tiep tuc thu dang ky lai INT2204
    res2, msg2 = enroll_student("22000002", "INT2204")
    print(f"Test 2 [Dang ky trung]             : Result = {res2} | Thong bao: {msg2}")

    # Tinh huong 3: Lop day
    # Lop INT2205 co enrolled=2, capacity=2 (het cho)
    res3, msg3 = enroll_student("22000002", "INT2205")
    print(f"Test 3 [Lop da day]               : Result = {res3} | Thong bao: {msg3}")

    # Tinh huong 4: Ma hoc phan khong ton tai
    res4, msg4 = enroll_student("22000001", "INT9999")
    print(f"Test 4 [Hoc phan khong ton tai]   : Result = {res4} | Thong bao: {msg4}")

    # Tinh huong 5: Ma sinh vien khong ton tai
    res5, msg5 = enroll_student("99999999", "INT2204")
    print(f"Test 5 [Sinh vien khong ton tai]  : Result = {res5} | Thong bao: {msg5}")

    print("\n--- TRANG THAI DU LIEU SAU KHI CHAY TEST ---")
    print("Danh sach enrollments hien tai:")
    for enr in enrollments:
        print("  -", enr)
    print("Thong tin hoc phan INT2204 sau cap nhat:")
    print("  -", find_course("INT2204"))


if __name__ == "__main__":
    demo_input_limit()
    run_tests()

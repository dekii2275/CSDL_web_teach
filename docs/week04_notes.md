# CourseHub - Buoi 4: Transaction, Locking, Migration & Index

## 1. Tóm tắt kết quả triển khai
- **Migration 001**: Bổ sung bảng theo dõi phiên bản `schema_migrations` và bảng nhật ký kiểm toán `enrollment_events`.
- **Demo class**: `RACE-01` (`INT2204`, `capacity = 1`, `semester_code = '2026-1'`).
- **Row Locking**: `POST /enrollments` và `DELETE /enrollments/{student_id}/{class_section_id}` sử dụng `SELECT ... FOR UPDATE` trên bảng `class_sections` trong cùng khối transaction `with engine.begin()`.
- **Concurrency Test**: Đạt kết quả chuẩn xác với 2 request đồng thời:
  - 1 request thành công `201 Created`
  - 1 request xung đột `409 Conflict` ("Lop hoc phan da het cho")
  - Trạng thái CSDL cuối: `enrolled = 1`, `remaining = 0`.
- **Performance Data**: 100.000 bản ghi sinh tự động với `dataset = 'performance'`.

---

## 2. So sánh Kế hoạch thực thi (EXPLAIN ANALYZE) trước và sau Composite Index

### Truy vấn kiểm thử:
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, student_id, class_section_id, event_type, occurred_at
FROM enrollment_events
WHERE dataset = 'performance'
  AND student_id = '22000001'
  AND occurred_at >= TIMESTAMP '2025-12-20 00:00:00'
ORDER BY occurred_at DESC
LIMIT 50;
```

### Chỉ mục khởi tạo:
```sql
CREATE INDEX idx_enrollment_events_dataset_student_time
ON enrollment_events (dataset, student_id, occurred_at DESC);
```

### Bảng đối sánh hiệu năng:

| Tiêu chí | Trước khi tạo Index (Seq Scan) | Sau khi tạo Index (Index Scan) | Mức cải thiện |
| :--- | :--- | :--- | :--- |
| **Kiểu quét (Scan Type)** | `Seq Scan on enrollment_events` | `Index Scan using idx_enrollment_events_...` | Trực tiếp nhảy đến vùng index phù hợp |
| **Số dòng bị loại (Removed by Filter)**| `99.183 rows` | `0 rows` | Không phải quét toàn bộ bảng |
| **Thao tác sắp xếp (Sorting)** | `Top-N heapsort (Memory: 31kB)` | Không cần (đã được sắp xếp sẵn theo `occurred_at DESC`) | Tiết kiệm CPU/RAM sắp xếp |
| **Số khối I/O đệm (Buffers)** | `1.140 blocks` (`shared hit=1140`) | `53 blocks` (`shared hit=50 read=3`) | **Giảm ~21.5 lần I/O** |
| **Thời gian thực thi (Execution Time)**| `6.686 ms` | `0.459 ms` | **Nhanh hơn ~14.5 lần** |

---

## 3. Lưu ý bảo mật
- Tuyệt đối không commit file `backend/.env` lên repository (đã có trong `.gitignore`).
- Các câu truy vấn trong Backend đều dùng tham số hóa (bind parameters `text("... :keyword")`) chống SQL Injection.

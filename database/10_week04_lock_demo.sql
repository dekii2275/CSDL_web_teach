-- Tab A - khóa dòng và giữ 8 giây
BEGIN;
SELECT id, capacity
FROM class_sections
WHERE id = 'RACE-01'
FOR UPDATE;

SELECT pg_sleep(8);

COMMIT;

-- Tab B - chạy khi Tab A đang chờ
BEGIN;
SELECT id, capacity
FROM class_sections
WHERE id = 'RACE-01'
FOR UPDATE;

ROLLBACK;

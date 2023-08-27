
-- Знайти, які курси читає певний викладач.

SELECT sub.subject, l.lecturer
FROM subjects sub
	RIGHT JOIN lecturers l ON sub.lecturer_id = l.id
WHERE l.id = 4
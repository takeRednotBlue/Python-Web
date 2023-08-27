-- Середній бал, який певний викладач ставить певному студентові.

SELECT st.student, l.lecturer, avg(s.score)
FROM scores s 
	RIGHT JOIN students st ON st.id = s.student_id 
	LEFT JOIN subjects sub ON sub.id = s.subject_id
	RIGHT JOIN lecturers l ON l.id = sub.lecturer_id
WHERE st.id = 24 AND sub.id in (SELECT id FROM subjects sub WHERE sub.lecturer_id = 4)
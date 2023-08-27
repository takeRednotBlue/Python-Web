
-- Список курсів, які певному студенту читає певний викладач.

SELECT st.student, sub.subject, l.lecturer
FROM scores s
	LEFT JOIN students st ON st.id = s.student_id
	LEFT  JOIN subjects sub ON sub.id = s.subject_id
	LEFT  JOIN lecturers l ON l.id = sub.lecturer_id 
WHERE st.id = 34 AND l.id = 4
GROUP BY sub.subject 
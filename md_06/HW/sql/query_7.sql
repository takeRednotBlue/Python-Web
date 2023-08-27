
-- Знайти оцінки студентів в окремій групі з певного предмета.

SELECT g.group_name, st.student, sub.subject, s.score, s.date_of 
FROM scores s 
	LEFT JOIN students st ON st.id = s.student_id
	LEFT JOIN subjects sub ON sub.id = s.subject_id
	RIGHT JOIN groups g ON g.id = st.group_id 
WHERE g.id = 2 AND sub.id = 3
ORDER BY st.student
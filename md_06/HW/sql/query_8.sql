
-- Знайти середній бал, який ставить певний викладач зі своїх предметів.

SELECT l.lecturer, sub.subject, AVG(s.score) as avgScore
FROM scores s 
	RIGHT JOIN subjects sub ON sub.id = s.subject_id
	RIGHT JOIN lecturers l ON l.id = sub.lecturer_id 
WHERE l.id = 4 
GROUP BY sub.subject
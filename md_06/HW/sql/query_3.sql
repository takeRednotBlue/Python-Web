
-- Знайти середній бал у групах з певного предмета.

SELECT g.group_name, sub.subject, ROUND(AVG(s.score), 2) as avgScore
FROM scores s 
    RIGHT JOIN students st ON s.student_id = st.id
    RIGHT JOIN subjects sub ON s.subject_id = sub.id
    RIGHT JOIN groups g ON st.group_id = g.id
WHERE sub.id = 3
GROUP BY g.group_name 
ORDER BY avgScore DESC
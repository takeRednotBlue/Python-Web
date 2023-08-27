
-- Знайти студента із найвищим середнім балом з певного предмета.

SELECT st.student, sub.subject, AVG(s.score) as avgScore
FROM scores s 
    RIGHT JOIN students st ON s.student_id = st.id
    RIGHT JOIN subjects sub ON s.subject_id = sub.id
WHERE sub.id = 3
GROUP BY st.student
ORDER BY avgScore DESC
LIMIT 1
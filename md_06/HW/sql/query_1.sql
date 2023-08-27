-- Знайти 5 студентів із найбільшим середнім балом з усіх предметів.

SELECT st.student, AVG(s.score) as avgScore
FROM scores s 
    RIGHT JOIN students st ON s.student_id = st.id
GROUP BY st.student
ORDER BY avgScore DESC
LIMIT 5
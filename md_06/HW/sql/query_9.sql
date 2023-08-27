
-- Знайти список курсів, які відвідує студент

SELECT st.student, sub.subject
FROM scores s
    LEFT JOIN students st ON st.id = s.student_id 
    LEFT JOIN subjects sub ON sub.id = s.subject_id 
WHERE st.id = 34
GROUP BY sub.subject 
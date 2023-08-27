
-- Знайти список студентів у певній групі.

SELECT g.group_name, st.student
FROM groups g 
	LEFT JOIN students st ON st.group_id = g.id 
WHERE g.id = 2
-- Table: groups
DROP TABLE IF EXISTS groups;
CREATE TABLE groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name VARCHAR(10) UNIQUE NOT NULL
);

-- Table: students
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student VARCHAR(255) UNIQUE NOT NULL,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES groups (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

-- Table: lecturers
DROP TABLE IF EXISTS lecturers;
CREATE TABLE lecturers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lecturer VARCHAR(255) UNIQUE NOT NULL
);

-- Table: subjects
DROP TABLE IF EXISTS subjects;
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject VARCHAR(255) NOT NULL,
    lecturer_id INTEGER NOT NULL,
    FOREIGN KEY (lecturer_id) REFERENCES lecturers (id)
      ON DELETE SET NULL
      ON UPDATE CASCADE
);



-- Table: scores
DROP TABLE IF EXISTS scores;
CREATE TABLE scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_id INTEGER,
    date_of DATE NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);
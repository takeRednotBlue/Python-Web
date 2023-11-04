from faker import Faker
from random import randint, choice
from datetime import datetime, timedelta
import sqlite3

NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_LECTURERS = 5
NUMBER_SUBJECTS = 8
NUMBER_SCORES = 5 # number of scores each student have for each subject

MIN_SCORE = 60
MAX_SCORE = 100

START_DATE = datetime(2023, 9, 1)
END_DATE = datetime(2023, 12, 26)

CS_SUBJECTS = [
    "Introduction to Computer Science",
    "Data Structures and Algorithms",
    "Database Systems",
    "Operating Systems",
    "Computer Networks",
    "Software Engineering",
    "Artificial Intelligence",
    "Machine Learning",
]

GROUPS = [
    'CS-111',
    'CS-112',
    'CS-113'
]

TABLES_MAPPING = {
    'groups': ['group_name', '?'],
    'lecturers': ['lecturer', '?'],
    'students': ['student, group_id', '?,?'],
    'subjects': ['subject, lecturer_id', '?,?'],
    'scores': ['student_id, subject_id, score, date_of', '?,?,?,?'],
}

database = 'university.db'

fake_data = Faker(locale=['en_GB', 'en_US'])

def random_date(start_date: datetime, end_date: datetime) -> datetime:
    '''Generates random date from interval'''
    time_delta = end_date - start_date
    random_date = start_date + timedelta(days=randint(0, time_delta.days))
    return random_date.date()


def generate_fake_data(number_students: int, number_lecturers: int) -> tuple[list]:
    '''Generate fake names for students and lecturers. Returns tuple which contain
    lists of names respectively.'''
    students_names = []
    lecturers_names = []
    for _ in range(number_students):
        students_names.append(fake_data.name())
    for _ in range(number_lecturers):
        lecturers_names.append(fake_data.name())
    return students_names, lecturers_names


def prepare_data_students(students_names: list[str]) -> list[tuple]:
    '''Prepare data for inserting into DB using sqlite3 module by executemany() method'''
    for_table = []
    for name in students_names:
        for_table.append(
            (name, randint(1, NUMBER_GROUPS))
        )
    return for_table


def prepare_data_lecturers(lecturers_names: list[str]) -> list[tuple]:
    '''Prepare data for inserting into DB using sqlite3 module by executemany() method'''
    for_table = []
    for name in lecturers_names:
        for_table.append((name,))
    return for_table


def prepare_data_groups(groups_list: list[str]) -> list[tuple]:
    '''Prepare data for inserting into DB using sqlite3 module by executemany() method'''
    for_table = []
    for group in groups_list:
        for_table.append((group,))
    return for_table


def prepare_data_subjects(subjects_list: list[str]) -> list[tuple]:
    '''Prepare data for inserting into DB using sqlite3 module by executemany() method'''
    for_table = []
    for subject in subjects_list:
        for_table.append(
            (subject, randint(1, NUMBER_LECTURERS))
        )
    return for_table


def prepare_data_scores(min_score: int, max_score: int) -> list[tuple]:
    for_table = []
    for student_id in range(1, NUMBER_STUDENTS+1):
        for subject_id in range(1, NUMBER_SUBJECTS+1):
            for _ in range(NUMBER_SCORES):
                for_table.append(
                    (student_id, subject_id, randint(min_score, max_score), random_date(START_DATE, END_DATE)) 
                )
    return for_table
    

def populate_db(db: str) -> None:
    students_names, lecturers_names = generate_fake_data(NUMBER_STUDENTS, NUMBER_LECTURERS)
    data = {
        'students': prepare_data_students(students_names),
        'lecturers': prepare_data_lecturers(lecturers_names),
        'groups': prepare_data_groups(GROUPS),
        'subjects': prepare_data_subjects(CS_SUBJECTS),
        'scores': prepare_data_scores(MIN_SCORE, MAX_SCORE),
    }
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        for table, values in TABLES_MAPPING.items():
            sql = f'''
            INSERT INTO {table}({values[0]}) VALUES({values[1]});
            '''
            cur.executemany(sql, data[table])
            print(data[table])

    

if __name__ == '__main__':
    populate_db(database)
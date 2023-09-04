from faker import Faker
from random import randint, choice
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.connect_db import session
from src.models import Student, Tutor, Group, Grade, Subject


NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_TUTORS= 5
NUMBER_SUBJECTS = 8
NUMBER_GRADES = 5 # number of scores each student have for each subject

MIN_GRADE = 60
MAX_GRADE = 100

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


fake_data = Faker(locale=['en_GB', 'en_US'])


def populate_students(fake_engine: Faker, session: Session) -> None:
    for _ in range(NUMBER_STUDENTS):
        name = fake_engine.name()
        student = Student(fullname=name, group_id=randint(1,NUMBER_GROUPS))
        session.add(student)
    session.commit()
    
def populate_groups(groups_list: list[str], session: Session) -> None:
    if len(groups_list) != NUMBER_GROUPS:
        raise ValueError("List length doesn't match NUMER_GROUPS constant.")
    
    for item in groups_list:
        group = Group(name=item)
        session.add(group)
    session.commit()

def populate_tutors(fake_engine: Faker, session: Session) -> None:
    tutors_list = []
    for _ in range(NUMBER_TUTORS):
        name = fake_engine.name()
        tutor = Tutor(fullname=name)
        tutors_list.append(tutor)
        session.add(tutor)
    session.commit()
    return tutors_list

def populate_subjects(subjects_list: list[str],  tutors_list: list[Tutor],  session: Session) -> None:
    if len(subjects_list) != NUMBER_SUBJECTS:
        raise ValueError("List length doesn't match NUMER_SUBJECTS constant.")

    for item in subjects_list:
        subject = Subject(name=item, tutors=[choice(tutors_list)])
        session.add(subject)
    session.commit()  

def populate_grades(fake_engine: Faker, session: Session) -> None:
    for student_id in range(1,NUMBER_STUDENTS+1):
        for subject_id in range(1, NUMBER_SUBJECTS+1):
            for _ in range(NUMBER_GRADES):
                grade = Grade(
                    student_id=student_id, 
                    subject_id=subject_id,
                    grade=randint(MIN_GRADE, MAX_GRADE),
                    date_of=fake_engine.date_between(START_DATE, END_DATE)
                    )
                session.add(grade)
    session.commit()

def random_date(start_date: datetime, end_date: datetime) -> datetime:
    '''Generates random date from interval'''
    time_delta = end_date - start_date
    random_date = start_date + timedelta(days=randint(0, time_delta.days))
    return random_date.date()

    

if __name__ == '__main__':
    try:
        populate_groups(GROUPS, session)
        populate_students(fake_data, session)
        tutors = populate_tutors(fake_data, session)
        populate_subjects(CS_SUBJECTS, tutors, session)
        populate_grades(fake_data, session)
    except Exception as err:
        print(err)
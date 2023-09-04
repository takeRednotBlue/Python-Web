'''
Зробити наступні вибірки з отриманої бази даних:

    1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    2. Знайти студента із найвищим середнім балом з певного предмета.
    3. Знайти середній бал у групах з певного предмета.
    4. Знайти середній бал на потоці (по всій таблиці оцінок).
    5. Знайти, які курси читає певний викладач.
    6. Знайти список студентів у певній групі.
    7. Знайти оцінки студентів в окремій групі з певного предмета.
    8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
    9. Знайти список курсів, які відвідує певний студент.
    10. Список курсів, які певному студенту читає певний викладач.

Для запитів оформити окремий файл my_select.py, де будуть 10 функцій від select_1 
до select_10. Виконання функцій повинно повертати результат аналогічний 
попередньої домашньої роботи. При запитах використовуємо механізм сесій SQLAlchemy.

Для додаткового завдання зробіть наступні запити підвищеної складності:

    11. Середній бал, який певний викладач ставить певному студентові.
    12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
'''
from tabulate import tabulate

from typing import Sequence, Tuple, Any
from sqlalchemy import select, func, desc, Row
from sqlalchemy.orm import Session

from src.models import Student, Tutor, Group, Grade, Subject, tutor_to_subject
from src.connect_db import session

# Custom typing for value that is returned by sqlalchemy.Result.all()
MySelectResult = Sequence[Row[Tuple[str, Any]]]


def print_table(result: MySelectResult) -> None:
    '''Takes result from select_xx() function as argument and print it
      in table format.'''
    if not result:
        print('No data found.')
        return
    
    headers = list(result[0]._mapping.keys())
    # Pretty prints when single value is returned
    if len(result) == 1 and len(result[0]) == 1:
        print(f'{headers[0]} - {str(result[0][0])}')
        return
    else:
        data = []
        for row in result:
            data.append(list(row))
    
        table = tabulate(data, headers, tablefmt='psql')
        print(table)


def select_1(session: Session) -> MySelectResult:
    '''Знайти 5 студентів із найбільшим середнім балом з усіх предметів.'''
    stmt = select(Student.fullname, 
                  func.round(func.avg(Grade.grade), 2).label('avgrade'))\
    .select_from(Grade)\
    .join(Student)\
    .group_by(Student.fullname)\
    .order_by(desc('avgrade'))\
    .limit(5)
    result = session.execute(stmt).all()
    return result


def select_2(session: Session) -> MySelectResult:
    '''Знайти студента із найвищим середнім балом з певного предмета.'''
    target_subject_id = 3
    stmt = select(Student.fullname, Subject.name, 
                  func.round(func.avg(Grade.grade), 2).label('avgrade'))\
    .select_from(Grade)\
    .join(Student)\
    .join(Subject)\
    .filter(Subject.id == target_subject_id)\
    .group_by(Subject.name, Student.fullname)\
    .order_by(desc('avgrade'))\
    .limit(1)
    result = session.execute(stmt).all()
    return result


def select_3(session: Session) -> MySelectResult:
    '''Знайти середній бал у групах з певного предмета.'''
    target_subject_id = 3
    stmt = select(Group.name,
                  Subject.name,
                  func.round(func.avg(Grade.grade), 2).label('avgrade'))\
    .select_from(Grade)\
    .join(Student)\
    .join(Group)\
    .join(Subject)\
    .filter(Subject.id == target_subject_id)\
    .group_by(Group.name, Subject.name)
    result = session.execute(stmt).all()
    return result


def select_4(session: Session) -> MySelectResult:
    '''Знайти середній бал на потоці (по всій таблиці оцінок).'''
    stmt = select(func.round(func.avg(Grade.grade), 2).label('general_avgrade'))\
    .select_from(Grade)
    result = session.execute(stmt).all()
    return result


def select_5(session: Session) -> MySelectResult:
    '''Знайти, які курси читає певний викладач'''
    target_tutor_id = 5
    stmt = select(Tutor.fullname,
                  Subject.name)\
    .select_from(Subject)\
    .join(Subject.tutors)\
    .where(Tutor.id == target_tutor_id)
    result = session.execute(stmt).all()
    return result


def select_6(session: Session) -> MySelectResult:
    '''Знайти список студентів у певній групі'''
    target_group_id = 1
    stmt = select(Group.name,
                  Student.fullname)\
    .select_from(Student)\
    .join(Group)\
    .where(Group.id == target_group_id)
    result = session.execute(stmt).all()
    return result


def select_7(session: Session) -> MySelectResult:
    '''Знайти оцінки студентів в окремій групі з певного предмета.'''
    target_group_id = 2
    target_subject_id = 5
    stmt = select(Group.name,
                  Subject.name,
                  Student.fullname,
                  Grade.grade)\
    .select_from(Grade)\
    .join(Student)\
    .join(Subject)\
    .join(Group)\
    .filter(Group.id == target_group_id and Subject.id == target_subject_id)
    result = session.execute(stmt).all()
    return result


def select_8(session: Session) -> MySelectResult:
    '''Знайти середній бал, який ставить певний викладач зі своїх предметів.'''
    target_tutor_id = 1
    stmt = select(Tutor.fullname, 
                  Subject.name,
                  func.round(func.avg(Grade.grade), 2).label('avgrade'))\
    .select_from(Grade)\
    .join(Subject)\
    .join(tutor_to_subject, Subject.id == tutor_to_subject.c.subject_id)\
    .join(Tutor, Tutor.id == tutor_to_subject.c.tutor_id)\
    .filter(Tutor.id == target_tutor_id)\
    .group_by(Subject.id, Tutor.fullname)
    result = session.execute(stmt).all()
    return result


def select_9(session: Session) -> MySelectResult:
    '''Знайти список курсів, які відвідує певний студент.'''
    target_student_id = 2
    stmt = select(Student.fullname,
                  Subject.name)\
    .select_from(Grade)\
    .join(Student)\
    .join(Subject)\
    .filter(Student.id == target_student_id)\
    .group_by(Subject.name, Student.fullname)
    print(stmt)
    result = session.execute(stmt).all()
    return result


def select_10(session: Session) -> MySelectResult:
    '''Список курсів, які певному студенту читає певний викладач.'''
    target_student_id = 2
    target_tutor_id = 1
    stmt = select(Student.fullname.label('student_name'),
                  Tutor.fullname.label('tutor_name'),
                  Subject.name)\
    .select_from(Grade)\
    .join(Subject)\
    .join(tutor_to_subject, Subject.id == tutor_to_subject.c.subject_id)\
    .join(Tutor, Tutor.id == tutor_to_subject.c.tutor_id)\
    .join(Student)\
    .filter(Student.id == target_student_id,
            Tutor.id == target_tutor_id)\
    .group_by(Subject.name, Student.fullname, Tutor.fullname)
    result = session.execute(stmt).all()
    return result


if __name__ == '__main__':
    result = select_1(session)
    print_table(result)


''' 
Домашнє завдання #6
Основне завдання

Реалізуйте базу даних, схема якої містить:

    Таблицю студентів; id student group_id
    Таблицю груп; id group
    Таблицю викладачів; id lacturer
    Таблицю предметів із зазначенням викладача, який читає предмет; id subject lecturer_id
    Таблицю, де у кожного студента є оцінки з предметів із зазначенням, коли оцінку отримано; id student_id subject_id score date_of

Заповніть отриману базу даних випадковими даними (~30-50 студентів, 3 групи, 5-8 предметів, 3-5 викладачів, до 20 оцінок у кожного студента з 
усіх предметів). Використовуйте пакет Faker для наповнення.

Зробити такі вибірки з отриманої бази даних:

    Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    Знайти студента із найвищим середнім балом з певного предмета.
    Знайти середній бал у групах з певного предмета.
    Знайти середній бал на потоці (по всій таблиці оцінок).
    Знайти, які курси читає певний викладач.
    Знайти список студентів у певній групі.
    Знайти оцінки студентів в окремій групі з певного предмета.
    Знайти середній бал, який ставить певний викладач зі своїх предметів.
    Знайти список курсів, які відвідує студент.
    Список курсів, які певному студенту читає певний викладач.

Для кожного запиту оформити окремий файл query_number.sql, де замість number підставити номер запиту. Файл містить SQL інструкцію, яку можна 
виконати як у терміналі бази даних, так і через cursor.execute(sql)
Додаткове завдання

Для додаткового завдання зробіть наступні запити підвищеної складності:

    Середній бал, який певний викладач ставить певному студентові.
    Оцінки студентів у певній групі з певного предмета на останньому занятті.
'''
from faker import Faker
from random import randint, choice
import sqlite3

computer_science_subjects = [
    "Introduction to Computer Science",
    "Data Structures and Algorithms",
    "Database Systems",
    "Operating Systems",
    "Computer Networks",
    "Software Engineering",
    "Artificial Intelligence",
    "Machine Learning",
]

database = 'university.db'

fake_data = Faker()


def create_db(db: str) -> None:
    with open(db, 'r') as fd:
        sql = fd.read()
    with sqlite3.connect(database) as conn:
        cur = conn.cursor()
        cur.executescript(sql)

def fill_students(db):
    names = []
    for _ in range(50):
        names.append(fake_data.name())
    group_id = []


if __name__ == '__main__':
    create_db(database)
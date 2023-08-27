import sqlite3

def create_db():
    with open('salary.sql', 'r') as f:
        sql = f.read()

    # створюємо з'єднання з БД (якщо файлу з БД немає, він буде створений)
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        cur.executescript(sql)


if __name__ == '__main__':
    create_db()
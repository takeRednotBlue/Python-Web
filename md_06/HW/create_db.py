import sqlite3


database = 'university.db'
script_file = 'sql/create_db.sql'


def create_db(scrip_file: str, db: str = 'unknown.db',) -> None:
    '''Creates DB
    :param db: optional
    :param script_file: is a string tha contains path to sql file
    with table creation script
    '''
    with open(scrip_file, 'r') as fd:
        sql = fd.read()
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.executescript(sql)


if __name__ == '__main__':
    create_db(script_file, database)
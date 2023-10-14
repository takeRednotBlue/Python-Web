import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

username = os.environ.get('DB_USER')
password = os.environ.get('PASSWORD')
db_name = os.environ.get('DB_NAME')
domain = os.environ.get('DOMAIN')

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{username}:{password}@{domain}:5432/{db_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

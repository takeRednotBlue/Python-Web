import dotenv
import os
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

username = os.environ.get('DB_USER')
password = os.environ.get('PASSWORD')
db_name = os.environ.get('DB_NAME')
domain = os.environ.get('DOMAIN')

url = f'postgresql+psycopg2://{username}:{password}@{domain}:5432/{db_name}'

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase

engine = create_engine('sqlite:///sqlalchemy_example.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('persons.id'))
    person = relationship(Person)

Base.metadata.create_all(engine)
Base.metadata.bind = engine

new_person = Person(name='John')
session.add(new_person)

# session.commit()

# new_address = Address(post_code='00000', person=new_person)
# session.add(new_address)
# session.commit()

with session:
    statement = select(Person)
    user_obj = session.scalars(statement).all()
    for num, person in enumerate(user_obj):
        print(f'{num}. - {person.name}')

    # for person in session.query(Person).all():
    #     print(person.name)
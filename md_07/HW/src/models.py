from datetime import date

from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey, Table

class Base(DeclarativeBase):
    pass


tutor_to_subject = Table(
    'tutor_to_subject', 
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('tutor_id', Integer, ForeignKey('tutors.id', ondelete='CASCADE')),
    Column('subject_id', Integer, ForeignKey('subjects.id', ondelete='CASCADE')),
)

class Person:
    # Parent class for models that contain personal data
    fullname: Mapped[str] = mapped_column(String(255))

class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10))


class Tutor(Base, Person):
    __tablename__ = 'tutors'
    id: Mapped[int] = mapped_column(primary_key=True)


class Student(Base, Person):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    groups: Mapped[int] = relationship('Group', backref='students')
    

class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(70))
    # tutor_id: Mapped[int] = mapped_column(ForeignKey('tutors.id'))
    tutors: Mapped[list[Tutor]] = relationship('Tutor', secondary=tutor_to_subject, backref='subjects')


class Grade(Base):
    __tablename__ = 'grades'
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id', ondelete='CASCADE'))
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id', ondelete='CASCADE'))
    students = relationship('Student', backref='grades')
    subjects = relationship('Subject', backref='grades')
    grade: Mapped[int]
    date_of: Mapped[date]
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from faker import Faker
import random

fake = Faker()
Base = declarative_base()

# Створення моделей таблиць
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship("Group")

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher")

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    grade = Column(Integer)
    date = Column(Date)

# Створення та налаштування бази даних
engine = create_engine('sqlite:///database.db', echo=True)
Base.metadata.create_all(engine)

# Створення сесії для взаємодії з базою даних
Session = sessionmaker(bind=engine)
session = Session()

# Заповнення таблиць
groups = [Group(name=f'Group {group_id}') for group_id in range(1, 4)]
session.add_all(groups)

teachers = [Teacher(name=fake.name()) for _ in range(5)]
session.add_all(teachers)

for _ in range(50):
    student = Student(name=fake.name(), group_id=random.randint(1, 3))
    session.add(student)

subjects = [Subject(name=fake.job(), teacher_id=random.randint(1, 5)) for _ in range(8)]
session.add_all(subjects)

for student_id in range(1, 51):
    for subject_id in range(1, 9):
        grade = Grade(student_id=student_id, subject_id=subject_id, grade=random.randint(60, 100), date=fake.date_between(start_date='-1y', end_date='today'))
        session.add(grade)

session.commit()

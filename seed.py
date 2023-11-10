from faker import Faker
from sqlalchemy.orm import Session
from models import Base, Group, Teacher, Student, Subject, Grade
from sqlalchemy import create_engine
import random

fake = Faker()

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

session = Session(engine)

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
        grade = Grade(
            student_id=student_id,
            subject_id=subject_id,
            grade=random.randint(60, 100),
            date=fake.date_between(start_date='-1y', end_date='today')
        )
        session.add(grade)

session.commit()
session.close()
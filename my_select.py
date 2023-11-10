from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Subject, Group

engine = create_engine('sqlite:///C:\\Users\\katya\\Documents\\GitHub\\PyWebDZ7\\database.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    result = (
        session.query(Student.name, func.avg(Grade.grade).label('avg_grade'))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.desc('avg_grade'))
        .limit(5)
        .all()
    )
    print("Запит 1:")
    for row in result:
        print(row)

def select_2(subject_id):
    result = (
        session.query(Student.name, func.avg(Grade.grade).label('avg_grade'))
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.desc('avg_grade'))
        .limit(1)
        .all()
    )
    print("Запит 2:")
    for row in result:
        print(row)

# Додайте аналогічні функції для інших запитів (select_3, select_4, і так далі)

if __name__ == "__main__":
    select_1()
    select_2(subject_id=1)
    # Викликайте інші функції тут, якщо потрібно

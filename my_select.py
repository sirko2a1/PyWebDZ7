from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from models import Base, Group, Teacher, Student, Subject, Grade

def select_1():
    DATABASE_URL = "sqlite:///database.db"
    engine = create_engine(DATABASE_URL)
    session = Session(engine)

    avg_grade_subquery = (
        session.query(
            Grade.student_id,
            func.avg(Grade.grade).label("average_grade")
        )
        .group_by(Grade.student_id)
        .subquery()
    )

    top_students_info = (
        session.query(
            Student.name.label("student_name"),
            Student.id.label("student_id"),
            avg_grade_subquery.c.average_grade.label("average_grade")
        )
        .join(avg_grade_subquery, Student.id == avg_grade_subquery.c.student_id)
        .order_by(avg_grade_subquery.c.average_grade.desc())
        .limit(5)
        .all()
    )

    session.close()

    print("Запит №1")
    print("-" * 40)
    
    for student_info in top_students_info:
        print("{:<15} {:<10} {:<10.2f}".format(
            student_info.student_name,
            student_info.student_id,
            student_info.average_grade
        ))



def select_2(subject_id):
    DATABASE_URL = "sqlite:///database.db"
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    
    session = Session(engine)

    avg_grade_subquery = (
        session.query(
            Grade.student_id,
            func.avg(Grade.grade).label("average_grade")
        )
        .filter(Grade.subject_id == subject_id)
        .group_by(Grade.student_id)
        .subquery()
    )

    top_student_info = (
        session.query(
            Student.name.label("student_name"),
            Student.id.label("student_id"),
            avg_grade_subquery.c.average_grade.label("average_grade")
        )
        .join(avg_grade_subquery, Student.id == avg_grade_subquery.c.student_id)
        .order_by(avg_grade_subquery.c.average_grade.desc())
        .first()
    )

    session.close()

    if top_student_info:
        print("Запит №2")
        print("-" * 40)
        print(f"Знайдено студента з найвищим середнім балом для предмета {subject_id}:")
        print(f"Ім'я студента: {top_student_info.student_name}")
        print(f"Айді студента: {top_student_info.student_id}")
        print(f"Середній бал: {top_student_info.average_grade:.2f}")
    else:
        print(f"Студентів не знайдено для предмета з id {subject_id}.")


def select_3(subject_id):
    DATABASE_URL = "sqlite:///database.db"
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    
    session = Session(engine)

    avg_grade_by_group = (
        session.query(
            Group.name.label("group_name"),
            func.avg(Grade.grade).label("average_grade")
        )
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )

    session.close()

    if avg_grade_by_group:
        print("Запит №3")
        print("-" * 40)
        print(f"Середній бал у групах для предмета {subject_id}:")
        print("{:<15} {:<10}".format("Назва групи", "Середній бал"))
        print("_" * 30)
        for avg_grade in avg_grade_by_group:
            print("{:<15} {:<10.2f}".format(
                avg_grade.group_name,
                avg_grade.average_grade
            ))
    else:
        print(f"Немає даних для предмета з id {subject_id}.")


def select_4():
    DATABASE_URL = "sqlite:///database.db"
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    
    session = Session(engine)

    avg_grade_overall = (
        session.query(
            func.avg(Grade.grade).label("average_grade")
        )
        .first()
    )

    session.close()

    if avg_grade_overall.average_grade:
        print("Запит №4")
        print("-" * 40)
        print(f"Середній бал по всій таблиці оцінок: {avg_grade_overall.average_grade:.2f}")
    else:
        print("Немає даних у таблиці оцінок.")



def select_5(teacher_id):
    DATABASE_URL = "sqlite:///database.db"
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

    session = Session(engine)

    courses_by_teacher = (
        session.query(Subject.name)
        .filter(Subject.teacher_id == teacher_id)
        .all()
    )

    session.close()

    if courses_by_teacher:
        print("Запит №5")
        print("-" * 40)
        print(f"Курси, які читає викладач з id {teacher_id}:")
        for course in courses_by_teacher:
            print(course.name)
    else:
        print(f"Викладача з id {teacher_id} не знайдено або він не читає жодного курсу.")


def select_6(group_id):
    DATABASE_URL = "sqlite:///database.db"
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

    session = Session(engine)

    students_by_group = (
        session.query(Student.name)
        .filter(Student.group_id == group_id)
        .all()
    )

    session.close()

    if students_by_group:
        print("Запит №6")
        print("-" * 40)
        print(f"Список студентів у групі з id {group_id}:")
        for student in students_by_group:
            print(student.name)
    else:
        print(f"Групи з id {group_id} не знайдено або в ній немає студентів.")


def select_7(group_id, subject_id):
    DATABASE_URL = "sqlite:///database.db"
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

    session = Session(engine)

    grades_by_group_and_subject = (
        session.query(Grade.grade, Student.name)
        .join(Student, Student.id == Grade.student_id)
        .join(Group, Group.id == Student.group_id)
        .filter(Group.id == group_id, Grade.subject_id == subject_id)
        .all()
    )

    session.close()

    if grades_by_group_and_subject:
        print("Запит №7")
        print("-" * 40)
        print(f"Оцінки студентів у групі з id {group_id} за предметом з id {subject_id}:")
        for grade, student_name in grades_by_group_and_subject:
            print(f"Студент: {student_name}, Оцінка: {grade}")
    else:
        print(f"Не знайдено оцінок для групи з id {group_id} та предмету з id {subject_id}.")


def select_8(teacher_id):
    DATABASE_URL = "sqlite:///database.db"
    engine = create_engine(DATABASE_URL)
    session = Session(engine)

    average_grade = (
        session.query(func.avg(Grade.grade))
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )

    session.close()

    if average_grade is not None:
        print("Запит №8")
        print("-" * 40)
        print(f"Середній бал, який ставить викладач з id {teacher_id}: {average_grade:.2f}")
    else:
        print(f"Викладача з id {teacher_id} не знайдено або він ще не має оцінок.")


def select_9(student_id):
    DATABASE_URL = "sqlite:///database.db"
    engine = create_engine(DATABASE_URL)
    session = Session(engine)

    courses_attended = (
        session.query(Subject.name)
        .join(Grade, Grade.subject_id == Subject.id)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )

    session.close()

    if courses_attended:
        print("Запит №9")
        print("-" * 40)
        print(f"Список курсів, які відвідує студент з id {student_id}:")
        for course in courses_attended:
            print(course.name)
    else:
        print(f"Студента з id {student_id} не знайдено або він ще не відвідав жодного курсу.")


def select_10(teacher_id, student_id):
    DATABASE_URL = "sqlite:///database.db"
    engine = create_engine(DATABASE_URL)
    session = Session(engine)

    courses_taught = (
        session.query(Subject.name)
        .join(Grade, Grade.subject_id == Subject.id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .join(Student, Student.id == Grade.student_id)
        .filter(Teacher.id == teacher_id, Student.id == student_id)
        .distinct()
        .all()
    )

    session.close()

    if courses_taught:
        print("Запит №10")
        print("-" * 40)
        print(f"Список курсів, які читає викладач з id {teacher_id} для студента з id {student_id}:")
        for course in courses_taught:
            print(course.name)
    else:
        print(f"Викладача з id {teacher_id} або студента з id {student_id} не знайдено, або вони не мають спільних курсів.")



select_1()
select_2(2)
select_3(1)
select_4()
select_5(1)
select_6(1)
select_7(1, 1)
select_8(1)
select_9(1)
select_10(1, 1)
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from models import Student, Grade

def my_select1():
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

    print("Запит 1")
    print("-" * 40)
    
    for student_info in top_students_info:
        print("{:<15} {:<10} {:<10.2f}".format(
            student_info.student_name,
            student_info.student_id,
            student_info.average_grade
        ))

my_select1()

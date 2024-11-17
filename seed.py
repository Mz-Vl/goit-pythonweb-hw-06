from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from faker import Faker
import random
from models import Base, Group, Student, Teacher, Subject, Grade
from datetime import datetime, timedelta

fake = Faker()
engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')
Session = sessionmaker(bind=engine)

def seed_data():
    session = Session()
    if session.query(Group).count() == 0:
        groups = [Group(name=f"Group {i + 1}") for i in range(3)]
        session.bulk_save_objects(groups)
        print("Групи додані.")
    else:
        print("Групи вже існують.")

    if session.query(Teacher).count() == 0:
        teachers = [Teacher(name=fake.name()) for _ in range(5)]
        session.bulk_save_objects(teachers)
        print("Викладачі додані.")
    else:
        print("Викладачі вже існують.")

    if session.query(Subject).count() == 0:
        teachers = session.query(Teacher).all()
        subjects = [
            Subject(name=f"Subject {i + 1}", teacher=random.choice(teachers))
            for i in range(8)
        ]
        session.bulk_save_objects(subjects)
        print("Предмети додані.")
    else:
        print("Предмети вже існують.")

    if session.query(Student).count() == 0:
        groups = session.query(Group).all()
        students = [
            Student(name=fake.name(), group=random.choice(groups))
            for _ in range(30)
        ]
        session.bulk_save_objects(students)
        print("Студенти додані.")
    else:
        print("Студенти вже існують.")

    if session.query(Grade).count() == 0:
        students = session.query(Student).all()
        subjects = session.query(Subject).all()
        grades = []
        for student in students:
            for subject in subjects:
                for _ in range(random.randint(5, 10)):
                    grade = Grade(
                        student=student,
                        subject=subject,
                        grade=random.randint(60, 100),
                        date_received=fake.date_between(
                            start_date="-6m", end_date="today"
                        ),
                    )
                    grades.append(grade)
        session.bulk_save_objects(grades)
        print("Оцінки додані.")
    else:
        print("Оцінки вже існують.")

    session.commit()
    print("База даних заповнена.")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    seed_data()

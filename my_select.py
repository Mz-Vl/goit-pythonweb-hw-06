from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, desc
from models import Student, Teacher, Subject, Group, Grade

engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()

# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_1():
    result = session.query(
        Student.name,
        func.avg(Grade.grade).label('average_grade')
    ).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result

# 2. Знайти студента із найвищим середнім балом з певного предмета
def select_2(subject_id):
    result = session.query(
        Student.name,
        func.avg(Grade.grade).label('average_grade')
    ).join(Grade).filter(Grade.subject_id == subject_id).group_by(Student.id).order_by(desc('average_grade')).first()
    return result

# 3. Середній бал у групах з певного предмета
def select_3(subject_id):
    result = session.query(
        Group.name,
        func.avg(Grade.grade).label('average_grade')
    ).select_from(Group) \
     .join(Student, Group.id == Student.group_id) \
     .join(Grade, Student.id == Grade.student_id) \
     .filter(Grade.subject_id == subject_id) \
     .group_by(Group.id) \
     .all()
    return result

# 4. Середній бал на потоці
def select_4():
    result = session.query(func.avg(Grade.grade).label('average_grade')).scalar()
    return result

# 5. Курси, які читає певний викладач
def select_5(teacher_id):
    result = session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()
    return result

# 6. Список студентів у певній групі
def select_6(group_id):
    result = session.query(Student.name).filter(Student.group_id == group_id).all()
    return result

# 7. Оцінки студентів у групі з певного предмета
def select_7(group_id, subject_id):
    result = session.query(
        Student.name,
        Grade.grade
    ).join(Student).filter(Student.group_id == group_id, Grade.subject_id == subject_id).all()
    return result

# 8. Середній бал, який ставить певний викладач зі своїх предметів
def select_8(teacher_id):
    result = session.query(
        func.avg(Grade.grade).label('average_grade')
    ).join(Subject).filter(Subject.teacher_id == teacher_id).scalar()
    return result

# 9. Курси, які відвідує певний студент
def select_9(student_id):
    result = session.query(
        Subject.name
    ).join(Grade).filter(Grade.student_id == student_id).distinct().all()
    return result

# 10. Курси, які певному студенту читає певний викладач
def select_10(student_id, teacher_id):
    result = session.query(
        Subject.name
    ).join(Grade).filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id).distinct().all()
    return result


if __name__ == "__main__":
    print("\n1. Топ 5 студентів:")
    print(select_1())

    print("\n2. Кращий студент з предмету 1:")
    print(select_2(1))

    print("\n3. Середній бал по групам з предмету 2:")
    print(select_3(1))

    print("\n4. Середній бал на потоці:")
    print(select_4())

    print("\n5. Курси викладача 3:")
    print(select_5(3))

    print("\n6. Студенти групи 1:")
    print(select_6(1))

    print("\n7. Оцінки групи 1 з предмету 1:")
    print(select_7(1, 1))

    print("\n8. Середній бал, який ставить викладач 3:")
    print(select_8(3))

    print("\n9. Курси студента 1:")
    print(select_9(1))

    print("\n10. Курси студента 1 у викладача 1:")
    print(select_10(1, 3))

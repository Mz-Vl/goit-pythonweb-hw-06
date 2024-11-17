import argparse
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Student, Teacher, Subject, Group
from seed import seed_data

engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()

def create_record(model, **kwargs):
    record = model(**kwargs)
    session.add(record)
    session.commit()
    print(f"Створено запис: {record.name}")

def list_records(model):
    records = session.query(model).all()
    for record in records:
        if hasattr(record, "id") and hasattr(record, "name"):
            print(f"ID: {record.id}, Name: {record.name}")
        else:
            print(record)

def update_record(model, record_id, **kwargs):
    record = session.get(model, record_id)
    if record:
        for key, value in kwargs.items():
            setattr(record, key, value)
        session.commit()
        print(f"Оновлено запис: ID={record.id}, Name={record.name}")
    else:
        print(f"Запис із ID {record_id} не знайдено.")

def delete_record(model, record_id):
    record = session.get(model, record_id)
    if record:
        session.delete(record)
        session.commit()
        print(f"Видалено запис із ID {record_id}.")
    else:
        print(f"Запис із ID {record_id} не знайдено.")

parser = argparse.ArgumentParser(description="CLI для роботи з базою даних.")
parser.add_argument('-a', '--action', required=True, help="Дія: create, list, update, remove, seed")
parser.add_argument('-m', '--model', help="Модель: Student, Teacher, Subject, Group")
parser.add_argument('--id', type=int, help="ID запису (для оновлення чи видалення)")
parser.add_argument('--name', help="Ім'я (для створення чи оновлення запису)")
args = parser.parse_args()

if args.action == 'seed':
    seed_data()
elif args.action == 'create' and args.model and args.name:
    models = {'Student': Student, 'Teacher': Teacher, 'Group': Group, 'Subject': Subject}
    model = models.get(args.model)
    if model:
        create_record(model, name=args.name)
elif args.action == 'list' and args.model:
    models = {'Student': Student, 'Teacher': Teacher, 'Group': Group, 'Subject': Subject}
    model = models.get(args.model)
    if model:
        list_records(model)
elif args.action == 'update' and args.model and args.id and args.name:
    models = {'Student': Student, 'Teacher': Teacher, 'Group': Group, 'Subject': Subject}
    model = models.get(args.model)
    if model:
        update_record(model, args.id, name=args.name)
elif args.action == 'remove' and args.model and args.id:
    models = {'Student': Student, 'Teacher': Teacher, 'Group': Group, 'Subject': Subject}
    model = models.get(args.model)
    if model:
        delete_record(model, args.id)
else:
    print("Неправильні аргументи. Використовуйте --help для перегляду доступних опцій.")

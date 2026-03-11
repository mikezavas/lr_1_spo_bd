from main import SQLTable
import json


db_config = {
    'host': 'srv221-h-st.jino.ru',
    'user': 'j30084097_13418',
    'password': 'pPS090207/()',
    'database': 'j30084097_13418',
    'port': 3306
}

if __name__ == "__main__":

    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            db_config = json.load(f)
    except:
        db_config = db_config

    db = SQLTable(db_config, 'students')

    db.create_table('id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), grade INT')

    db.insert({'name': 'Napoleon', 'grade': 85})
    db.insert({'name': 'Putin', 'grade': 90})
    db.insert({'name': 'Trump', 'grade': 78})

    print("\nВсе студенты:")
    for student in db.select():
        print(student)

    print("\nСортировка по grade DESC:")
    for student in db.select_ordered("grade", "DESC"):
        print(student)

    print("\nДиапазон id 1-2:")
    for student in db.select_id_range(1, 2):
        print(student)

    print("\nПоиск по имени Napoleon:")
    print(db.find_by_value("name", "Napoleon"))

    print("\nСтруктура таблицы:")
    db.show_structure()

    print("\nДобавляем столбец age")
    db.add_column("age INT")

    print("\nУдаляем столбец age")
    db.drop_column("age")

    print("\nЭкспорт CSV")
    db.export_csv("students.csv")

    print("\nУдаляем записи id 2-3")
    db.delete_id_range(2, 3)

    print("\nИмпорт CSV")
    db.import_csv("students.csv")

    print("\nУдаляем таблицу")
    db.drop_table()

    db.disconnect()

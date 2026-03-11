import mysql.connector
import csv


class SQLTable:
    def __init__(self, db_config, table_name):
        self.db_config = db_config
        self.table_name = table_name
        self.connection = None
        self.cursor = None
        self.columns = []

        self.connect()

        if not self._check_table_exists():
            print(f"Таблица '{self.table_name}' не существует.")
        else:
            self._update_column_names()

    def connect(self):
        """
        подключение к бд
        """
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            self.cursor = self.connection.cursor()
            print("Подключено")
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False

    def disconnect(self):
        """
        отключение от бд
        """
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Соединение закрыто")

    def _check_table_exists(self):
        """
        проверка существования таблицы
        """
        try:
            query = "SHOW TABLES LIKE %s"
            self.cursor.execute(query, (self.table_name,))
            return bool(self.cursor.fetchone())
        except:
            return False

    def _update_column_names(self):
        """
        Получение имён колонок таблицы
        """
        try:
            query = f"DESCRIBE {self.table_name}"
            self.cursor.execute(query)
            self.columns = [row[0] for row in self.cursor.fetchall()]
        except:
            self.columns = []

    # операции crud
    def insert(self, data):
        cursor = self.connection.cursor()
        try:
            columns = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
            cursor.execute(query, list(data.values()))
            self.connection.commit()
            print(f"INSERT: Добавлено в {self.table_name}")
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
        finally:
            cursor.close()

    def update(self, data, condition):
        cursor = self.connection.cursor()
        try:
            set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
            query = f"UPDATE {self.table_name} SET {set_clause} WHERE {condition}"
            cursor.execute(query, list(data.values()))
            self.connection.commit()
            print(f"UPDATE: Обновлено в {self.table_name}")
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
        finally:
            cursor.close()

    def delete(self, condition):
        cursor = self.connection.cursor()
        try:
            query = f"DELETE FROM {self.table_name} WHERE {condition}"
            cursor.execute(query)
            self.connection.commit()
            print(f"DELETE: Удалено из {self.table_name}")
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
        finally:
            cursor.close()

    def select(self, columns='*', condition=None):
        """
        получение данных с выбором колонок
        """
        cursor = self.connection.cursor(dictionary=True)
        try:
            query = f"SELECT {columns} FROM {self.table_name}"
            if condition:
                query += f" WHERE {condition}"
            cursor.execute(query)
            result = cursor.fetchall()
            print(f"SELECT: Получено {len(result)} записей")
            return result
        except Exception as e:
            print(f"Ошибка: {e}")
            return []
        finally:
            cursor.close()

    def drop_table(self):
        """
        удаление таблицы
        """
        cursor = self.connection.cursor()
        try:
            query = f"DROP TABLE IF EXISTS {self.table_name}"
            cursor.execute(query)
            self.connection.commit()
            print(f"DROP TABLE: Таблица {self.table_name} удалена")
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
        finally:
            cursor.close()

    def create_table(self, columns):
        cursor = self.connection.cursor()
        try:
            query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns})"
            cursor.execute(query)
            self.connection.commit()
            print(f"CREATE TABLE: Таблица {self.table_name} создана")
            self._update_column_names()
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
        finally:
            cursor.close()

    def select_ordered(self, column, order="ASC"):
        '''
        Вывод конкретного столбца по возрастанию/убыванию
        :param column: столбец для сортировки
        :param order: порядок сортировки
        :return: список строк таблицы
        '''
        cursor = self.connection.cursor(dictionary=True)
        try:
            query = f"SELECT * FROM {self.table_name} ORDER BY {column} {order}"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка: {e}")
            return []
        finally:
            cursor.close()

    def select_id_range(self, start_id, end_id):
        '''
        Вывод диапазона строк по id
        :param start_id: начальный id диапазона
        :param end_id: конечный id диапазона
        :return: список строк таблицы
        '''
        cursor = self.connection.cursor(dictionary=True)
        try:
            query = f"SELECT * FROM {self.table_name} WHERE id BETWEEN %s AND %s"
            cursor.execute(query, (start_id, end_id))
            return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка: {e}")
            return []
        finally:
            cursor.close()

    def delete_id_range(self, start_id, end_id):
        '''
        Удаление диапазона строк по id
        :param start_id: начальный id диапазона
        :param end_id: конечный id диапазона
        '''
        cursor = self.connection.cursor()
        try:
            query = f"DELETE FROM {self.table_name} WHERE id BETWEEN %s AND %s"
            cursor.execute(query, (start_id, end_id))
            self.connection.commit()
            print("Диапазон строк удалён")
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            cursor.close()

    def show_structure(self):
        '''
        Вывод структуры таблицы
        :return: список строк со структурой таблицы
        '''
        cursor = self.connection.cursor()
        try:
            query = f"DESCRIBE {self.table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            print("Структура таблицы:")
            for row in result:
                print(row)
            return result
        except Exception as e:
            print(f"Ошибка: {e}")
            return []
        finally:
            cursor.close()

    def find_by_value(self, column, value):
        '''
        Вывод строки содержащей значение в конкретном столбце
        :param column: столбец для поиска
        :param value: значение, которое необходимо найти
        :return:
        '''
        cursor = self.connection.cursor(dictionary=True)
        try:
            query = f"SELECT * FROM {self.table_name} WHERE {column} = %s"
            cursor.execute(query, (value,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка: {e}")
            return []
        finally:
            cursor.close()

    def add_column(self, column_definition):
        '''
        Добавление нового столбца
        :param column_definition: описание столбца
        '''
        cursor = self.connection.cursor()
        try:
            query = f"ALTER TABLE {self.table_name} ADD COLUMN {column_definition}"
            cursor.execute(query)
            self.connection.commit()
            print("Столбец добавлен")
            self._update_column_names()
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            cursor.close()

    def drop_column(self, column_name):
        '''
        удаление столбца
        :param column_name: столбец для удаления
        '''
        cursor = self.connection.cursor()
        try:
            query = f"ALTER TABLE {self.table_name} DROP COLUMN {column_name}"
            cursor.execute(query)
            self.connection.commit()
            print("Столбец удалён")
            self._update_column_names()
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            cursor.close()

    def export_csv(self, filename):
        '''
        экспорт в CSV
        :param filename: имя файла
        :return:
        '''
        data = self.select()

        if not data:
            print("Нет данных для экспорта")
            return

        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

            print("Экспорт в CSV выполнен")
        except Exception as e:
            print(f"Ошибка: {e}")

    def import_csv(self, filename):
        '''
        импорт из CSV
        :param filename: имя файла
        '''
        try:
            with open(filename, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    self.insert(row)

            print("Импорт из CSV выполнен")
        except Exception as e:
            print(f"Ошибка: {e}")

import json
import os
from psycopg2 import sql, connect, errors
from settings import DATABASESSETTINGS

BASE_DIR = os.path.dirname(__file__)


class DataBaseManager:
    """Базовый класс для работы с базой"""
    conn = connect(
        dbname=DATABASESSETTINGS['name'],
        user=DATABASESSETTINGS['user'],
        password=DATABASESSETTINGS['password'],
        host=DATABASESSETTINGS['host'],
        )

    def get_all_value_from_table(self, table_name, limit=100):
        """
        Получение всех записей из таблицы.
        params:
            table_name(название таблицы)
            limit(ограничение выборки)
        """
        cursor = self.conn.cursor()
        sql_str = 'SELECT * FROM %s LIMIT %s' % (table_name, limit)
        try:
            cursor.execute(sql_str)
        except errors.UndefinedTable as e:
            print(e)
        else:
            records = cursor.fetchall()
            return records

    def create_persons_table(self):
        """
        Создание таблицы для персонала
        """
        sql_str = '''
            CREATE TABLE Persons (
                Id SERIAL PRIMARY KEY,
                ParentId INTEGER references Persons(Id),
                Name CHARACTER VARYING(100) NOT NULL,
                Type INTEGER NOT NULL
            );
            '''
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        self.conn.commit()

    def create_persons(self, values):
        """
        Создание записи в таблицы персонала
        params:
            values(значения)
        """
        insert = sql.SQL(
                'INSERT INTO Persons (ParentId, Name, Type) VALUES {}'
                ).format(sql.SQL(',').join(map(sql.Literal, values)))
        cursor = self.conn.cursor()
        cursor.execute(insert)
        self.conn.commit()

    def get_data_from_json(self):
        """
        Получение данных из json файла
        """
        path_to_json_file = os.path.join(BASE_DIR, 'json_data.json')
        with open(path_to_json_file, "r") as read_file:
            data = json.load(read_file)
        return data

    def get_data_for_insert_person(self):
        """
        Преобразование данных из json файла в
        список для создания записей в таблице Persons
        """
        data_from_json = self.get_data_from_json()
        data = list()
        for instance in data_from_json:
            data.append(
                (instance['ParentId'], instance['Name'], instance['Type'])
                )
        return data

    def set_data_from_json(self):
        """
        Запись данных в таблицу Persons из json файла
        """
        data_from_json = self.get_data_for_insert_person()
        self.create_persons(data_from_json)

    def get_main_parent_id_and_name(self, persons_id):
        """
        Получение id и имени города, к которому пренадлежит
        persons
        """
        sql_str = """
            WITH recursive r AS (
                SELECT
                    Id,
                    Name,
                    ParentId,
                    1 AS level
                FROM Persons
                WHERE id = %s
            UNION
                SELECT
                    Persons.Id,
                    Persons.Name,
                    Persons.ParentId,
                    r.level + 1 AS level
                FROM Persons
                INNER JOIN r ON r.ParentId=Persons.id
            )
            SELECT Id, Name, level  FROM r
        """ % (persons_id)
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        records = sorted(
            cursor.fetchall(), key=lambda x: x[2], reverse=True
            )
        main_parent = records[0]
        result = {'id': main_parent[0], 'name': main_parent[1]}
        return result

    def get_all_persons_in_city(self, city_id):
        """
        Получение всего персонала из переданного города
        """
        sql_str = """
            WITH RECURSIVE r AS (
                SELECT
                    Id,
                    ParentId,
                    Name,
                    Type
                FROM Persons
                WHERE ParentId = %s
            UNION ALL
                SELECT
                    Persons.Id,
                    Persons.ParentId,
                    Persons.Name,
                    Persons.Type
                FROM Persons
                JOIN r ON Persons.ParentId = r.Id
            )
            SELECT * FROM r where Type=3;
        """ % (city_id)
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        records = cursor.fetchall()
        return records

    def get_draw_data_all_persons_in_city(self, persons_id):
        """
        Получение словаря в котором
        city_name - название города
        persons_list - список всех сотрудников в городе
        params:
            persons_id(id записи в таблице persons)
        """
        main_parent_id_and_name = self.get_main_parent_id_and_name(persons_id)
        all_persons_in_city = self.get_all_persons_in_city(
            main_parent_id_and_name['id']
            )
        data = {
            'city_name': main_parent_id_and_name['name'],
            'persons_list': all_persons_in_city
            }
        return data

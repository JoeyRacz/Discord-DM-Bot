import sqlite3
from sqlite3 import Error
import random

database = r"C:\Users\Joey PC\Documents\PY Projects\Discord-DM-Bot\Random Bot.db"


class MetaDatabase(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaDatabase, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=MetaDatabase):
    connection = None
    cursor_object = None

    def connect(self):
        if self.connection is None:
            try:
                self.connection = sqlite3.connect(database)
                self.cursor_object = self.connection.cursor()
            except Error as e:
                print(e)
        return self.cursor_object

    def random_query(self, cursor, roll, description, table, a=-1):
        cursor.execute(f"SELECT COUNT(*) from {table}")
        roll_limit = cursor.fetchone()[0]
        if a == -1:
            a = random.randint(1, roll_limit)
        cursor.execute(f"SELECT {description} FROM {table} WHERE {roll}=?", (a,))
        row = cursor.fetchone()[0]
        return row, a

    def weighted_query(self, cursor, connection, roll, description, table, a=-1):
        connection.row_factory = lambda cursor, row: row[0]
        new_cursor = connection.cursor()
        contents_rolls = new_cursor.execute(f'SELECT {roll} FROM {table}').fetchall()
        contents_weights = new_cursor.execute(f'SELECT weight FROM {table}').fetchall()
        if a == -1:
            a = random.choices(contents_rolls, weights=contents_weights, k=1)[0]
        connection.row_factory = sqlite3.Row
        cursor.execute(f"SELECT {description} FROM {table} WHERE {roll}=?",
                       (a,))
        row = cursor.fetchone()[0]
        return row, a

    def create_dungeon_table(self, cursor, table_id):
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS D{table_id}(
                                id text PRIMARY KEY,
                                description text NOT NULL
                        );""")

    def insert_into_dungeon(self, object, cursor, connection, dungeon_id):
        sql = f"""INSERT INTO D{dungeon_id}(id, description)
                    VALUES(?, ?)"""
        cursor.execute(sql, object)
        connection.commit()

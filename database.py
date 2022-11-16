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
        print(row)
        return a
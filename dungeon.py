import random
import json
import sqlite3
from sqlite3 import Error
from dungeon_generator import dungeonGenerator
from main import database_connection
from abc import ABC, abstractmethod


def load_json(file):
    with open(file) as dungeon_size:
        return json.load(dungeon_size)


dungeon_data = load_json("dungeon.json")
map_height = dungeon_data["small"]["map height"]
map_width = dungeon_data["small"]["map width"]

dm = dungeonGenerator(91, 91)
dm.placeRoom(1, 1, 3, 3)
dm.placeRandomRooms(5, 15, 1, 1, 30000)
dm.generateCorridors('l')
dm.connectAllRooms(0)
dm.pruneDeadends(50)

# join unconnected areas
unconnected = dm.findUnconnectedAreas()
dm.joinUnconnectedAreas(unconnected)
dm.placeWalls()
passages = []
corridor_list_length = len(dm.corridors)
for i, v in enumerate(dm.corridors):
    if i+1 == corridor_list_length:
        break
    t1 = dm.corridors[i]
    t2 = dm.corridors[i+1]
    if t1[0] == t2[0] or t1[1] == t2[1]:
        continue
    passages.append(i)
dungeon_id = random.randint(1, 99999)
create_dungeon_table = f""" CREATE TABLE IF NOT EXISTS D{dungeon_id}(
                                id text PRIMARY KEY,
                                description text NOT NULL
                        );"""

try:
    c = database_connection.cursor()
    c.execute(create_dungeon_table)
except Error as e:
    print(e)


def insert_into_dungeon(object):
    sql = f"""INSERT INTO D{dungeon_id}(id, description)
                VALUES(?, ?)"""
    cur = database_connection.cursor()
    cur.execute(sql, object)
    database_connection.commit()


def roll_no_weight(roll, table, description):
    with database_connection:
        cursor = database_connection.cursor()
        cursor.execute(f"SELECT COUNT(*) from {table}")
        roll_limit = cursor.fetchone()[0]
        a = random.randint(1, roll_limit)
        cursor.execute(f"SELECT {description} FROM {table} WHERE {roll}=?", (a,))
        row = cursor.fetchone()[0]
        return row


def roll_weighted(roll, table, description):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        contents_rolls = cursor.execute(f'SELECT {roll} FROM {table}').fetchall()
        contents_weights = cursor.execute(f'SELECT weight FROM {table}').fetchall()
        random_roll = random.choices(contents_rolls, weights=contents_weights, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute(f"SELECT {description} FROM {table} WHERE {roll}=?",
                       (random_roll,))
        row = cursor.fetchone()[0]
        return row


class Strategy(ABC):
    @abstractmethod
    def save_dungeon_part(self):
        pass


class Context():
    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def save_dungeon(self) -> None:
        self._strategy.save_dungeon_part()


class Door(Strategy):
    def save_dungeon_part(self) -> None:
        y = 0
        for i in dm.doors:
            x = (f"D{y}", roll_weighted("dungeon_door_roll", "dungeon_door", "dungeon_door_description"))
            insert_into_dungeon(x)
            y += 1


class Passage(Strategy):
    def save_dungeon_part(self) -> None:
        y = 0
        for i in passages:
            x = (f"P{y}", roll_weighted("dungeon_door_roll", "dungeon_door", "dungeon_door_description"))
            insert_into_dungeon(x)
            y += 1


class Room(Strategy):
    def save_dungeon_part(self) -> None:
        y = 0
        for i in dm.rooms:
            x = (f"R{y}", roll_weighted("dungeon_door_roll", "dungeon_door", "dungeon_door_description"))
            insert_into_dungeon(x)
            y += 1


context = Context(Door())
context.save_dungeon()

import random
import json
import sqlite3
from sqlite3 import Error
from dungeon_generator import dungeonGenerator
import database
from abc import ABC, abstractmethod


test_database = database.Database()
test_database.connect()
test_cursor = test_database.cursor_object
test_connection = test_database.connection

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
player_map = dm
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

test_database.create_dungeon_table(test_cursor, dungeon_id)

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
            x = (f"D{y}", test_database.weighted_query(test_cursor, test_connection, "dungeon_door_roll",
                                                       "dungeon_door_description", "dungeon_door"))
            test_database.insert_into_dungeon(x, test_cursor, test_connection, dungeon_id)
            y += 1


class Passage(Strategy):
    def save_dungeon_part(self) -> None:
        y = 0
        for i in passages:
            x = (f"P{y}", test_database.weighted_query(test_cursor, test_connection, "passage_contents_roll",
                                                       "passage_contents", "dungeon_passage_contents"))
            test_database.insert_into_dungeon(x, test_cursor, test_connection, dungeon_id)
            y += 1


class Room(Strategy):
    def save_dungeon_part(self) -> None:
        y = 0
        for i in dm.rooms:
            x = (f"R{y}", test_database.weighted_query(test_cursor, test_connection, "room_contents_roll",
                                                       "room_contents", "dungeon_room_contents"))
            test_database.insert_into_dungeon(x, test_cursor, test_connection, dungeon_id)
            y += 1


context = Context(Door())
context.save_dungeon()

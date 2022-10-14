import os
import random
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return connection


database = r"C:\Users\Joey PC\Documents\PY Projects\Discord-DM-Bot\Random Bot.db"
database_connection = create_connection(database)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id}'
    )


@bot.command(name='clue')
async def clue(ctx):
    with database_connection:
        cursor = database_connection.cursor()
        cursor.execute("SELECT COUNT(*) from dungeon_clue")
        roll_limit = cursor.fetchone()[0]
        a = random.randint(1, roll_limit)
        cursor.execute("SELECT clue_description FROM dungeon_clue WHERE dungeon_clue_roll=?", (a,))
        row = cursor.fetchone()[0]
        await ctx.send(row)


@bot.command(name='passage_contents')
async def passage_contents(ctx):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        contents_rolls = cursor.execute('SELECT passage_contents_roll FROM dungeon_passage_contents').fetchall()
        contents_weights = cursor.execute('SELECT weight FROM dungeon_passage_contents').fetchall()
        random_roll = random.choices(contents_rolls, weights=contents_weights, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT passage_contents FROM dungeon_passage_contents WHERE passage_contents_roll=?",
                       (random_roll,))
        row = cursor.fetchone()[0]
        await ctx.send(row)


@bot.command(name='oracle')
async def oracle(ctx):
    await ctx.send(f"How Likely?\n1. Impossible\n2. Highly Unlikely\n3. Unlikely\n4. Possible\n5. Likely\n"
                   f"6. Highly Likely\n7. A Certainty\n")

    async def check(msg):
        if msg.content not in ['1', '2', '3', '4', '5','6', '7']:
            await ctx.send('Not a valid choice!')

        return msg.author == ctx.author and msg.channel == ctx.channel and \
            msg.content in ['1', '2', '3', '4', '5', '6', '7']
    try:
        msg = await bot.wait_for("message", check=check, timeout=5)
    except asyncio.TimeoutError:
        await ctx.send("Didn't reply in time!")
        return
    modifier = 1
    match msg.content:
        case '1':
            modifier = -6
        case '2':
            modifier = -4
        case '3':
            modifier = -2
        case '4':
            modifier = 0
        case '5':
            modifier = 2
        case '6':
            modifier = 4
        case '7':
            modifier = 6
    oracle_roll = random.randint(1, 20) + modifier
    if modifier == 1:
        await ctx.send('Not a valid choice!')
    elif oracle_roll < 7:
        await ctx.send('No')
    elif oracle_roll > 12:
        await ctx.send('Yes')
    else:
        await ctx.send('Maybe')


@bot.command(name='bane')
async def bane(ctx):
    with database_connection:
        cursor = database_connection.cursor()
        cursor.execute("SELECT COUNT(*) from banes")
        roll_limit = cursor.fetchone()[0]
        a = random.randint(1, roll_limit)
        cursor.execute("SELECT banes_result, banes_descriptions FROM banes WHERE banes_roll=?", (a,))
        result, description = cursor.fetchone()
        await ctx.send(result)
        await ctx.send(description)


@bot.command(name='boon')
async def boon(ctx):
    with database_connection:
        cursor = database_connection.cursor()
        cursor.execute("SELECT COUNT(*) from boons")
        roll_limit = cursor.fetchone()[0]
        a = random.randint(1, roll_limit)
        cursor.execute("SELECT boons_result, boons_descriptions FROM boons WHERE boons_roll=?", (a,))
        result, description = cursor.fetchone()
        await ctx.send(result)
        await ctx.send(description)


@bot.command(name='encounter1')
async def encounter1(ctx):
    with database_connection:
        cursor = database_connection.cursor()
        cursor.execute("SELECT COUNT(*) from dungeon_encounters")
        roll_limit = cursor.fetchone()[0]
        a = random.randint(1, roll_limit)
        cursor.execute("SELECT encounter_description FROM dungeon_encounters WHERE encounters_roll=?", (a,))
        row = cursor.fetchone()[0]
        await ctx.send(row)


@bot.command(name='encounter2')
async def encounter2(ctx):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        dungeon_encounters_roll = cursor.execute('SELECT dungeon_encounters_roll FROM dungeon_encounters_2').fetchall()
        weight = cursor.execute('SELECT weight FROM dungeon_encounters_2').fetchall()
        random_roll = random.choices(dungeon_encounters_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT dungeon_encounters_description FROM dungeon_encounters_2"
                       " WHERE dungeon_encounters_roll=?", (random_roll,))
        dungeon_encounters = cursor.fetchone()[0]
        await ctx.send(dungeon_encounters)


@bot.command(name='room_feature')
async def room_feature(ctx):
    with database_connection:
        cursor = database_connection.cursor()
        cursor.execute("SELECT COUNT(*) from dungeon_room_feature")
        roll_limit = cursor.fetchone()[0]
        a = random.randint(1, roll_limit)
        cursor.execute("SELECT room_feature FROM dungeon_room_feature WHERE room_feature_roll=?", (a,))
        row = cursor.fetchone()[0]
        await ctx.send(row)


@bot.command(name='items')
async def items(ctx):
    with database_connection:
        cursor = database_connection.cursor()
        cursor.execute("SELECT COUNT(*) from items")
        roll_limit = cursor.fetchone()[0]
        a = random.randint(1, roll_limit)
        cursor.execute("SELECT items_result FROM items WHERE items_roll=?", (a,))
        row = cursor.fetchone()[0]
        await ctx.send(row)


@bot.command(name='keywords')
async def keywords(ctx):
    with database_connection:
        cursor = database_connection.cursor()
        cursor.execute("SELECT COUNT(*) from keywords")
        roll_limit = cursor.fetchone()[0]
        a = random.randint(1, roll_limit)
        cursor.execute("SELECT keywords_result FROM keywords WHERE keywords_roll=?", (a,))
        row = cursor.fetchone()[0]
        await ctx.send(row)


@bot.command(name='verbs')
async def verbs(ctx):
    with database_connection:
        cursor = database_connection.cursor()
        cursor.execute("SELECT COUNT(*) from situations_verbs")
        roll_limit = cursor.fetchone()[0]
        a = random.randint(1, roll_limit)
        cursor.execute("SELECT verbs_description FROM situations_verbs WHERE verbs_roll=?", (a,))
        row = cursor.fetchone()[0]
        await ctx.send(row)


@bot.command(name='skill_challenge')
async def skill_challenge(ctx):
    with database_connection:
        cursor = database_connection.cursor()
        cursor.execute("SELECT COUNT(*) from skill_challenges")
        roll_limit = cursor.fetchone()[0]
        a = random.randint(1, roll_limit)
        cursor.execute("SELECT skill_challenges_result FROM skill_challenges WHERE skill_challenges_roll=?", (a,))
        row = cursor.fetchone()[0]
        await ctx.send(row)


@bot.command(name='combat_events')
async def combat_events(ctx):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        combat_events_roll = cursor.execute('SELECT combat_events_roll FROM combat_events').fetchall()
        weight = cursor.execute('SELECT weight FROM combat_events').fetchall()
        random_roll = random.choices(combat_events_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT combat_events_result, combat_events_description FROM combat_events"
                       " WHERE combat_events_roll=?", (random_roll,))
        event, description = cursor.fetchone()
        await ctx.send(event)
        await ctx.send(description)


@bot.command(name='door')
async def door(ctx):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        dungeon_door_roll = cursor.execute('SELECT dungeon_door_roll FROM dungeon_door').fetchall()
        weight = cursor.execute('SELECT weight FROM dungeon_door').fetchall()
        random_roll = random.choices(dungeon_door_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT dungeon_door_description FROM dungeon_door"
                       " WHERE dungeon_door_roll=?", (random_roll,))
        dungeon_door = cursor.fetchone()[0]
        await ctx.send(dungeon_door)


@bot.command(name='dungeon_feature')
async def door(ctx):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        dungeon_feature_roll = cursor.execute('SELECT dungeon_feature_roll FROM dungeon_feature').fetchall()
        weight = cursor.execute('SELECT weight FROM dungeon_feature').fetchall()
        random_roll = random.choices(dungeon_feature_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT dungeon_feature_description FROM dungeon_feature"
                       " WHERE dungeon_feature_roll=?", (random_roll,))
        dungeon_feature = cursor.fetchone()[0]
        await ctx.send(dungeon_feature)


@bot.command(name='room_contents')
async def room_contents(ctx):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        room_contents_roll = cursor.execute('SELECT room_contents_roll FROM dungeon_room_contents').fetchall()
        weight = cursor.execute('SELECT weight FROM dungeon_room_contents').fetchall()
        random_roll = random.choices(room_contents_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT room_contents FROM dungeon_room_contents"
                       " WHERE room_contents_roll=?", (random_roll,))
        room_contents = cursor.fetchone()[0]
        await ctx.send(room_contents)


@bot.command(name='trap')
async def dungeon_trap(ctx):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        dungeon_trap_roll = cursor.execute('SELECT dungeon_trap_roll FROM dungeon_trap').fetchall()
        weight = cursor.execute('SELECT weight FROM dungeon_trap').fetchall()
        random_roll = random.choices(dungeon_trap_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT kind_of_trap FROM dungeon_trap"
                       " WHERE dungeon_trap_roll=?", (random_roll,))
        kind_of_trap = cursor.fetchone()[0]
        random_roll = random.choices(dungeon_trap_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT trap_notice_dc FROM dungeon_trap"
                       " WHERE dungeon_trap_roll=?", (random_roll,))
        trap_notice_dc = cursor.fetchone()[0]
        random_roll = random.choices(dungeon_trap_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT trap_save_dc FROM dungeon_trap"
                       " WHERE dungeon_trap_roll=?", (random_roll,))
        trap_save_dc = cursor.fetchone()[0]
        random_roll = random.choices(dungeon_trap_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT trap_damage FROM dungeon_trap"
                       " WHERE dungeon_trap_roll=?", (random_roll,))
        trap_damage = cursor.fetchone()[0]
        await ctx.send(kind_of_trap)
        await ctx.send(f"Notice DC: " + str(trap_notice_dc))
        await ctx.send(f"Save DC: " + str(trap_save_dc))
        await ctx.send(f"Damage: " + str(trap_damage))


@bot.command(name='difficulty')
async def encounter_difficulty(ctx):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        difficulty_roll = cursor.execute('SELECT difficulty_roll FROM encounter_difficulty').fetchall()
        weight = cursor.execute('SELECT weight FROM encounter_difficulty').fetchall()
        random_roll = random.choices(difficulty_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT difficulty_description FROM encounter_difficulty"
                       " WHERE difficulty_roll=?", (random_roll,))
        encounter_difficulty = cursor.fetchone()[0]
        await ctx.send(encounter_difficulty)


@bot.command(name='something_found')
async def something_found(ctx):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        something_found_roll = cursor.execute('SELECT something_found_roll FROM event_something_found').fetchall()
        weight = cursor.execute('SELECT weight FROM event_something_found').fetchall()
        random_roll = random.choices(something_found_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT something_found_result FROM event_something_found"
                       " WHERE something_found_roll=?", (random_roll,))
        something_found = cursor.fetchone()[0]
        await ctx.send(something_found)


@bot.command(name='monster_intentions')
async def monster_intentions(ctx):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        monster_intentions_roll = cursor.execute('SELECT monster_intentions_roll FROM monster_intentions').fetchall()
        weight = cursor.execute('SELECT weight FROM monster_intentions').fetchall()
        random_roll = random.choices(monster_intentions_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT monster_intentions_description FROM monster_intentions"
                       " WHERE monster_intentions_roll=?", (random_roll,))
        monster_intentions = cursor.fetchone()[0]
        await ctx.send(monster_intentions)


@bot.command(name='monster_reactions')
async def monster_reactions(ctx):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        monster_reactions_roll = cursor.execute('SELECT monster_reactions_roll FROM monster_reactions').fetchall()
        weight = cursor.execute('SELECT weight FROM monster_reactions').fetchall()
        random_roll = random.choices(monster_reactions_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT monster_reactions_description FROM monster_reactions"
                       " WHERE monster_reactions_roll=?", (random_roll,))
        monster_reactions = cursor.fetchone()[0]
        await ctx.send(monster_reactions)


@bot.command(name='move_events')
async def move_events(ctx):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        move_event_roll = cursor.execute('SELECT move_event_roll FROM move_events').fetchall()
        weight = cursor.execute('SELECT weight FROM move_events').fetchall()
        random_roll = random.choices(move_event_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT move_event_result FROM move_events"
                       " WHERE move_event_roll=?", (random_roll,))
        move_events = cursor.fetchone()[0]
        await ctx.send(move_events)


@bot.command(name='notice')
async def notice_something(ctx):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        notice_something_roll = cursor.execute('SELECT notice_something_roll FROM notice_something').fetchall()
        weight = cursor.execute('SELECT weight FROM notice_something').fetchall()
        random_roll = random.choices(notice_something_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT notice_something_title FROM notice_something"
                       " WHERE notice_something_roll=?", (random_roll,))
        notice_something = cursor.fetchone()[0]
        await ctx.send(notice_something)


@bot.command(name='contents')
async def contents(ctx):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        contents_roll = cursor.execute('SELECT room_contents_roll FROM room_contents').fetchall()
        weight = cursor.execute('SELECT weight FROM room_contents').fetchall()
        random_roll = random.choices(contents_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT room_contents, room_contents_notes FROM room_contents"
                       " WHERE room_contents_roll=?", (random_roll,))
        contents, description = cursor.fetchone()
        await ctx.send(contents)
        await ctx.send(description)


@bot.command(name='story')
async def story(ctx):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        story_points_roll = cursor.execute('SELECT story_points_roll FROM story_points').fetchall()
        weight = cursor.execute('SELECT weight FROM story_points').fetchall()
        random_roll = random.choices(story_points_roll, weights=weight, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("SELECT story_points_result, story_points_description FROM story_points"
                       " WHERE story_points_roll=?", (random_roll,))
        story_points, description = cursor.fetchone()
        await ctx.send(story_points)
        await ctx.send(description)

bot.run(TOKEN)

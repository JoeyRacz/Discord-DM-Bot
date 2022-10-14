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
        contents_weights = cursor.execute('SELECT passage_contents_weight FROM dungeon_passage_contents').fetchall()
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

        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content in ['1', '2', '3', '4', '5',
                                                                                           '6', '7']
    try:
        msg = await bot.wait_for("message", check=check, timeout=5)
    except asyncio.TimeoutError:
        await ctx.send("Didn't reply in time!")
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

bot.run(TOKEN)

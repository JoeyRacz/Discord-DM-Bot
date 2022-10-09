import os
import random

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

bot.run(TOKEN)

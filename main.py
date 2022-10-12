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


@bot.command(name='oracle')
async def oracle(ctx):
    await ctx.send(f"How Likely?\n1. Impossible\n2. Highly Unlikely\n3. Unlikely\n4. Possible\n5. Likely\n"
                   f"6. Highly Likely\n7. A Certainty\n")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content in ['1', '2', '3', '4', '5',
                                                                                           '6', '7']
    msg = await bot.wait_for("message", check=check)
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
        case _:
            await ctx.send('Not a valid choice!\n')
            return
    oracle_roll = random.randint(1, 20) + modifier
    if oracle_roll < 7:
        await ctx.send('No')
    elif oracle_roll > 12:
        await ctx.send('Yes')
    else:
        await ctx.send('Maybe')

bot.run(TOKEN)

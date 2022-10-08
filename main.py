import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

#def clue_select(conn, priority):


database = r"C:\Users\Joey PC\Documents\PY Projects\Discord-DM-Bot\Random Bot.db"
conn = create_connection(database)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user.name} is connected to the following guild: \n'
        f'{guild.name}(id: {guild.id}'
    )


@bot.command(name='clue')
async def clue(ctx):
    with conn:
        cur = conn.cursor()
        a = random.randint(1, 104)
        cur.execute("SELECT clue_description FROM dungeon_clue WHERE dungeon_clue_roll=?", (a,))
        row = cur.fetchone()[0]
        await ctx.send(row)


bot.run(TOKEN)

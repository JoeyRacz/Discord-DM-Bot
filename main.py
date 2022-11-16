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


async def roll_no_weight(ctx, roll, description, table, a=-1):
    with database_connection:
        cursor = database_connection.cursor()
        cursor.execute(f"SELECT COUNT(*) from {table}")
        roll_limit = cursor.fetchone()[0]
        if a == -1:
            a = random.randint(1, roll_limit)
        cursor.execute(f"SELECT {description} FROM {table} WHERE {roll}=?", (a,))
        row = cursor.fetchone()[0]
        await ctx.send(row)
        return a


async def roll_weighted(ctx, roll, description, table, random_roll=-1):
    with database_connection:
        database_connection.row_factory = lambda cursor, row: row[0]
        cursor = database_connection.cursor()
        contents_rolls = cursor.execute(f'SELECT {roll} FROM {table}').fetchall()
        contents_weights = cursor.execute(f'SELECT weight FROM {table}').fetchall()
        if random_roll == -1:
            random_roll = random.choices(contents_rolls, weights=contents_weights, k=1)[0]
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute(f"SELECT {description} FROM {table} WHERE {roll}=?",
                       (random_roll,))
        row = cursor.fetchone()[0]
        await ctx.send(row)
        return random_roll


@bot.command(name='clue')
async def clue(ctx):
    await roll_no_weight(ctx, "dungeon_clue_roll", "clue_description", "dungeon_clue")


@bot.command(name='passage_contents')
async def passage_contents(ctx):
    await roll_weighted(ctx, "passage_contents_roll", "passage_contents", "dungeon_passage_contents")


@bot.command(name='oracle')
async def oracle(ctx):
    await ctx.send(f"How Likely?\n1. Impossible\n2. Highly Unlikely\n3. Unlikely\n4. Possible\n5. Likely\n"
                   f"6. Highly Likely\n7. A Certainty\n")
    try:
        msg = await bot.wait_for("message", timeout=30)
    except asyncio.TimeoutError:
        await ctx.send("Didn't reply in time!")
        return
    try:
        modifier = int(msg.content) * 2 - 8
    except ValueError:
        await ctx.send("Not a valid choice!")
        return
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
    roll = await roll_no_weight(ctx, "banes_roll", "banes_result", "banes")
    await roll_no_weight(ctx, "banes_roll", "banes_descriptions", "banes", roll)


@bot.command(name='boon')
async def boon(ctx):
    roll = await roll_no_weight(ctx, "boons_roll", "boons_result", "boons")
    await roll_no_weight(ctx, "boons_roll", "boons_descriptions", "boons", roll)


@bot.command(name='encounter1')
async def encounter1(ctx):
    await roll_no_weight(ctx, "encounters_roll", "encounter_description", "dungeon_encounters")


@bot.command(name='encounter2')
async def encounter2(ctx):
    await roll_weighted(ctx, "dungeon_encounters_roll", "dungeon_encounters_description", "dungeon_encounters_2")


@bot.command(name='room_feature')
async def room_feature(ctx):
    await roll_no_weight(ctx, "room_feature_roll", "room_feature", "dungeon_room_feature")


@bot.command(name='items')
async def items(ctx):
    await roll_no_weight(ctx, "items_roll", "items_result", "items")


@bot.command(name='keywords')
async def keywords(ctx):
    await roll_no_weight(ctx, "keywords_roll", "keywords_result", "keywords")


@bot.command(name='verbs')
async def verbs(ctx):
    await roll_no_weight(ctx, "verbs_roll", "verbs_description", "situations_verbs")


@bot.command(name='skill_challenge')
async def skill_challenge(ctx):
    await roll_no_weight(ctx, "skill_challenges_roll", "skill_challenges_result", "skill_challenges")


@bot.command(name='combat_events')
async def combat_events(ctx):
    roll = await roll_weighted(ctx, "combat_events_roll", "combat_events_result", "combat_events")
    await roll_weighted(ctx, "combat_events_roll", "combat_events_description", "combat_events", roll)


@bot.command(name='door')
async def door(ctx):
    await roll_weighted(ctx, "dungeon_door_roll", "dungeon_door_description", "dungeon_door")


@bot.command(name='dungeon_feature')
async def door(ctx):
    await roll_weighted(ctx, "dungeon_feature_roll", "dungeon_feature_description", "dungeon_feature")


@bot.command(name='room_contents')
async def room_contents(ctx):
    await roll_weighted(ctx, "room_contents_roll", "room_contents", "dungeon_room_contents")


@bot.command(name='trap')
async def dungeon_trap(ctx):
    await roll_weighted(ctx, "dungeon_trap_roll", "kind_of_trap", "dungeon_trap")
    await ctx.send(f"Notice DC: ")
    await roll_weighted(ctx, "dungeon_trap_roll", "trap_notice_dc", "dungeon_trap")
    await ctx.send(f"Save DC: ")
    await roll_weighted(ctx, "dungeon_trap_roll", "trap_save_dc", "dungeon_trap")
    await ctx.send(f"Damage: ")
    await roll_weighted(ctx, "dungeon_trap_roll", "trap_damage", "dungeon_trap")


@bot.command(name='difficulty')
async def encounter_difficulty(ctx):
    await roll_weighted(ctx, "difficulty_roll", "difficulty_description", "encounter_difficulty")


@bot.command(name='something_found')
async def something_found(ctx):
    await roll_weighted(ctx, "something_found_roll", "something_found_result", "event_something_found")


@bot.command(name='monster_intentions')
async def monster_intentions(ctx):
    await roll_weighted(ctx, "monster_intentions_roll", "monster_intentions_description", "monster_intentions")


@bot.command(name='monster_reactions')
async def monster_reactions(ctx):
    await roll_weighted(ctx, "monster_reactions_roll", "monster_reactions_description", "monster_reactions")


@bot.command(name='move_events')
async def move_events(ctx):
    await roll_weighted(ctx, "move_event_roll", "move_event_result", "move_events")


@bot.command(name='notice')
async def notice_something(ctx):
    await roll_weighted(ctx, "notice_something_roll", "notice_something_title", "notice_something")


@bot.command(name='contents')
async def contents(ctx):
    roll = await roll_weighted(ctx, "room_contents_roll", "room_contents", "room_contents")
    await roll_weighted(ctx, "room_contents_roll", "room_contents_notes", "room_contents", roll)


@bot.command(name='story')
async def story(ctx):
    roll = await roll_weighted(ctx, "story_points_roll", "story_points_result", "story_points")
    await roll_weighted(ctx, "story_points_roll", "story_points_description", "story_points", roll)

bot.run(TOKEN)

import os
import random
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

import database

test_database = database.Database()
test_database.connect()
test_cursor = test_database.cursor_object
test_connection = test_database.connection

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
    row, roll = test_database.random_query(test_cursor, "dungeon_clue_roll", "clue_description", "dungeon_clue")
    await ctx.send(row)


@bot.command(name='passage_contents')
async def passage_contents(ctx):
    row, roll = test_database.weighted_query(test_cursor, test_connection, "passage_contents_roll", "passage_contents",
                                             "dungeon_passage_contents")
    await ctx.send(row)


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
    row, roll = test_database.random_query(test_cursor, "banes_roll", "banes_result", "banes")
    await ctx.send(row)
    row, roll = test_database.random_query(test_cursor, "banes_roll", "banes_descriptions", "banes", roll)
    await ctx.send(row)


@bot.command(name='boon')
async def boon(ctx):
    row, roll = test_database.random_query(test_cursor, "boons_roll", "boons_result", "boons")
    await ctx.send(row)
    row, roll = test_database.random_query(test_cursor, "boons_roll", "boons_descriptions", "boons", roll)
    await ctx.send(row)


@bot.command(name='encounter1')
async def encounter1(ctx):
    row, roll = test_database.random_query(test_cursor, "encounters_roll", "encounter_description",
                                           "dungeon_encounters")
    await ctx.send(row)


@bot.command(name='encounter2')
async def encounter2(ctx):
    row, roll = test_database.weighted_query(test_cursor, test_connection, "dungeon_encounters_roll",
                                             "dungeon_encounters_description", "dungeon_encounters_2")
    await ctx.send(row)


@bot.command(name='room_feature')
async def room_feature(ctx):
    row, roll = test_database.random_query(test_cursor, "room_feature_roll", "room_feature", "dungeon_room_feature")
    await ctx.send(row)


@bot.command(name='items')
async def items(ctx):
    row, roll = test_database.random_query(test_cursor, "items_roll", "items_result", "items")
    await ctx.send(row)


@bot.command(name='keywords')
async def keywords(ctx):
    row, roll = test_database.random_query(test_cursor, "keywords_roll", "keywords_result", "keywords")
    await ctx.send(row)


@bot.command(name='verbs')
async def verbs(ctx):
    row, roll = test_database.random_query(test_cursor, "verbs_roll", "verbs_description", "situations_verbs")
    await ctx.send(row)


@bot.command(name='skill_challenge')
async def skill_challenge(ctx):
    row, roll = test_database.random_query(test_cursor, "skill_challenges_roll", "skill_challenges_result",
                                           "skill_challenges")
    await ctx.send(row)


@bot.command(name='combat_events')
async def combat_events(ctx):
    row, roll = test_database.weighted_query(test_cursor, test_connection, "combat_events_roll", "combat_events_result",
                                             "combat_events")
    await ctx.send(row)
    row, roll = test_database.weighted_query(test_cursor, test_connection, "combat_events_roll",
                                             "combat_events_description",
                                             "combat_events", roll)
    await ctx.send(row)


@bot.command(name='door')
async def door(ctx):
    row, roll = test_database.weighted_query(test_cursor, test_connection, "dungeon_door_roll",
                                             "dungeon_door_description",
                                             "dungeon_door")
    await ctx.send(row)


@bot.command(name='dungeon_feature')
async def door(ctx):
    row, roll = test_database.weighted_query(test_cursor, test_connection, "dungeon_feature_roll",
                                             "dungeon_feature_description",
                                             "dungeon_feature")
    await ctx.send(row)


@bot.command(name='room_contents')
async def room_contents(ctx):
    row, roll = test_database.weighted_query(test_cursor, test_connection, "room_contents_roll", "room_contents",
                                             "dungeon_room_contents")
    await ctx.send(row)


@bot.command(name='trap')
async def dungeon_trap(ctx):
    row, roll = test_database.weighted_query(test_cursor, test_connection, "dungeon_trap_roll", "kind_of_trap",
                                             "dungeon_trap")
    await ctx.send(row)
    await ctx.send(f"Notice DC: ")
    row, roll = test_database.weighted_query(test_cursor, test_connection, "dungeon_trap_roll", "trap_notice_dc",
                                             "dungeon_trap")
    await ctx.send(row)
    await ctx.send(f"Save DC: ")
    row, roll = test_database.weighted_query(test_cursor, test_connection, "dungeon_trap_roll", "trap_save_dc",
                                             "dungeon_trap")
    await ctx.send(row)
    await ctx.send(f"Damage: ")
    row, roll = test_database.weighted_query(test_cursor, test_connection, "dungeon_trap_roll", "trap_damage",
                                             "dungeon_trap")
    await ctx.send(row)


@bot.command(name='difficulty')
async def encounter_difficulty(ctx):
    row, roll = test_database.weighted_query(test_cursor, test_connection, "difficulty_roll", "difficulty_description",
                                             "encounter_difficulty")
    await ctx.send(row)


@bot.command(name='something_found')
async def something_found(ctx):
    row, roll = test_database.weighted_query(test_cursor, test_connection, "something_found_roll",
                                             "something_found_result",
                                             "event_something_found")
    await ctx.send(row)


@bot.command(name='monster_intentions')
async def monster_intentions(ctx):
    row, roll = test_database.weighted_query(test_cursor, test_connection, "monster_intentions_roll",
                                             "monster_intentions_description", "monster_intentions")
    await ctx.send(row)


@bot.command(name='monster_reactions')
async def monster_reactions(ctx):
    row, roll = test_database.weighted_query(test_cursor, test_connection, "monster_reactions_roll",
                                             "monster_reactions_description", "monster_reactions")
    await ctx.send(row)


@bot.command(name='move_events')
async def move_events(ctx):
    row, roll = test_database.weighted_query(test_cursor, test_connection, "move_event_roll", "move_event_result",
                                             "move_events")
    await ctx.send(row)


@bot.command(name='notice')
async def notice_something(ctx):
    row, roll = test_database.weighted_query(test_cursor, test_connection, "notice_something_roll",
                                             "notice_something_title",
                                             "notice_something")
    await ctx.send(row)


@bot.command(name='contents')
async def contents(ctx):
    row, roll = test_database.weighted_query(test_cursor, test_connection, "room_contents_roll", "room_contents",
                                             "room_contents")
    await ctx.send(row)
    row, roll = test_database.weighted_query(test_cursor, test_connection, "room_contents_roll", "room_contents_notes",
                                             "room_contents", roll)
    await ctx.send(row)


@bot.command(name='story')
async def story(ctx):
    row, roll = test_database.weighted_query(test_cursor, test_connection, "story_points_roll", "story_points_result",
                                             "story_points")
    await ctx.send(row)
    row, roll = test_database.weighted_query(test_cursor, test_connection, "story_points_roll",
                                             "story_points_description",
                                             "story_points", roll)
    await ctx.send(row)


bot.run(TOKEN)

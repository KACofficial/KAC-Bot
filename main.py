# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import os
import json
from utils.utils import init

# boilerplate junk
description = "Request movies!"
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

with open("config.json") as f:
    config = json.load(f)

loaded_ext = []


# end boilerplate junk


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


async def setup_hook():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            ext_name = filename[:-3]
            try:
                if ext_name not in loaded_ext:
                    await bot.load_extension(f'commands.{ext_name}')
                    loaded_ext.append(ext_name)
            except Exception as e:
                print(f'Failed to load extension {ext_name}: {e}')


@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        await message.reply(f"Don't mention me! Use `!help` to see a list of valid commands.")
    await bot.process_commands(message)


init(config["tmdb_key"])

# asyncio.run(setup_hook())
bot.setup_hook = setup_hook

bot.run(config["bot_token"])

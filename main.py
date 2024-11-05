import discord
from discord.ext import commands
import os
import json
from utils.utils import init  # use the function init() from utils/utils.py in this file
from utils.webui import setup_global_api_key, run_flask # import the webui's core functions
from utils.help_command import CustomHelpCommand
import threading

# setup the configuration and bot
description = "the official KillAllChickens discord bot!"
intents = discord.Intents.all()

#intents.message_content = True

activity = discord.Activity(type=discord.ActivityType.listening, name="SRV | !help")

bot = commands.Bot(command_prefix='!', description=description, intents=intents, activity=activity, help_command=CustomHelpCommand()) # commands.Bot(command_prefix='!', description=description, intents=intents, activity=activity, help_command=CustomHelpCommand())

with open("config.json") as f:
    config = json.load(f)

loaded_ext = []


@bot.event  # Run this code when the bot is ready to start listining to commands
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')  # print the bots username
    print('------')  # print a little break to seperate this from debugging stuff


async def setup_hook():  # this function searches the "commands" directory for python files
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            ext_name = filename[:-3]
            try:
                if ext_name not in loaded_ext:
                    await bot.load_extension(f'commands.{ext_name}')  # load the python files in "commands"
                    loaded_ext.append(ext_name)
            except Exception as e:
                print(f'Failed to load extension {ext_name}: {e}')

@bot.event
async def on_message(message: discord.Message):
    if bot.user.mentioned_in(message):  # if the bot is mentioned like `@KAC Bot`
        await message.reply(f"Don't mention me! Use `!help` to see a list of valid commands.")  # reply to the message
        return
    
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx: commands.Context, error):
    """This runs on command errors"""
    command = ctx.message.content.split(" ")[0]
    if isinstance(error, commands.CommandNotFound): # is the error is a command not found error
        await ctx.reply(f"Command `{command}` not found. Use `!help` to get a list of commands.")
    elif isinstance(error, commands.MissingAnyRole): # is the error is a missing any role error
        await ctx.reply(f"You do not have permission to use the `{command}` command.")
    elif isinstance(error, commands.NoPrivateMessage): # is the error is a no private message error
        await ctx.reply("This command cannot be used in private messages.")
    else:
        raise error

if __name__ == '__main__':  # if statement makes sure that this is ran first
    setup_global_api_key(config["webui_key"])
    webui_thread = threading.Thread(target=run_flask)
    webui_thread.start()  # create a webui thread

    init(config["tmdb_key"])

    bot.setup_hook = setup_hook # this line runs the setup_hook() function when the bot is ready to load commands

    bot.run(config["bot_token"])  # start the bot
    webui_thread.join()

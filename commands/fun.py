import random
from typing import Optional
from time import sleep

import requests
from discord.ext import commands

from utils.rps_utils import RockPaperScissors


class Fun(commands.Cog):
    """\"Fun\" commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):  # replies with pong
        """Replies with pong"""
        await ctx.reply('Pong.')

    @commands.command()
    async def coin(self, ctx):  # flips a coin
        """Flip a coin"""
        await ctx.reply(random.choice(["Heads!", "Tails!"]))

    @commands.command(name="8ball")
    async def eight_ball(self, ctx: commands.Context, *, question: Optional[str]):  # ask the 8ball a question to answer
        """Ask the 8ball a question"""
        if question is None:  # if there is no question provided
            await ctx.reply("A question is required!")
            return
        responses = [  # a list of responses the 8ball can give
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes, definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]
        answer = random.choice(responses)
        await ctx.reply(f"I respond to `{question}` with, `{answer}`")  # reply with an answer from the 8ball

    @commands.command()
    async def joke(self, ctx: commands.Context):  # returns a joke
        """Say a joke(can be offensive)"""
        try:
            api_url = "https://v2.jokeapi.dev/joke/Any"  # the api for jokes
            response = requests.get(api_url)
            joke_data = response.json()
        except Exception as e:
            await ctx.reply(f"An error accured while grabbing the joke: {e}")
            return
        try:
            if joke_data["type"] == "twopart":  # if there is a setup and punchline send post on two different messages
                await ctx.send(joke_data["setup"])
                sleep(1)
                await ctx.send(joke_data["delivery"])
            elif joke_data["type"] == "single":  # if its a one liner say that one line
                await ctx.send(joke_data["joke"])
        except Exception as e:
            await ctx.reply(f"An error accured while parsing the joke: {e}")
            return
        
    @commands.command(name="quote")  # the command will be !quote
    async def random_quote(self, ctx: commands.Context):  # returns a random quote
        """Get a random quote"""
        try:
            api_url = "https://api.quotable.io/random"
            response = requests.get(api_url)
            quote_data = response.json()
        except Exception as e:
            await ctx.reply(f"An error accured while grabbing the quote: {e}")
            return
        await ctx.reply(f"\"{quote_data['content']}\" - *{quote_data['author']}*")

    @commands.command()
    async def source_code(self, ctx: commands.Context):  # provides a link to the github page
        """Get a link to my source code"""
        await ctx.reply("View my source code here: [KAC-Bot](https://github.com/KACofficial/KAC-Bot)")

    @commands.command()
    async def dice(self, ctx, die: str):
        """Roll a die, use NdN format"""
        try:
            count, sides = map(int, die.split("d"))
        except ValueError:
            await ctx.reply("Invalid format! Use `NdN` format, ex. `1d6` for 1 6-sided die.")
            return

        msg = str(random.randint(1, sides))
        if count > 1:
            for _ in range(count - 1):
                msg += "\n" + str(random.randint(1, sides))

        await ctx.reply(msg)

    @commands.command()
    async def rps(self, ctx: commands.Context):
        """Play rock paper scissors against the bot"""
        
        # Call the view class
        view = RockPaperScissors(ctx)
        
        # Send an message with the view attached to it
        view.message = await ctx.send(f"{ctx.author.mention}\nChoose an option by using the buttons below!", view=view)


async def setup(bot):
    await bot.add_cog(Fun(bot))

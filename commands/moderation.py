from discord.ext import commands
import discord
import sys
from asyncio import TimeoutError

class Moderation(commands.Cog):
    """Commands for neckbeards"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str = "No reason provided"):
        """Kick a user from the server"""
        try:
            # Attempt to send a DM to the user
            try:
                await member.send(f"You have been kicked from `{ctx.guild.name}` for the following reason: `{reason}`")
            except discord.Forbidden:
                await ctx.send(f"Could not send a DM to `{member.name}`, but they will be kicked from the server.")

            # Kick the member
            await member.kick(reason=reason)
            await ctx.send(f"`{member.name}` has been kicked for: `{reason}`")

        except discord.Forbidden:
            await ctx.reply(f"I do not have permission to kick `{member.name}`.")
        except discord.HTTPException as e:
            await ctx.reply(f"Failed to kick `{member.name}`: {e}")
        except Exception as e:
            await ctx.reply(f"An error occurred: {e}")
        
    @commands.command()
    async def kill_bot(self, ctx: commands.Context):
        """Kill the bot (owner only)"""
        if any(role.name == "Owner" for role in ctx.author.roles):
            conf_message: discord.Message = await ctx.reply("Are you sure?")
            await conf_message.add_reaction('✅')
            await conf_message.add_reaction('❌')

            def check(reaction, user):
                return user == ctx.author and reaction.message.id == conf_message.id

            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)

                if reaction.emoji == '✅':
                    await ctx.send("Shutting down...")
                    await self.bot.close()
                elif reaction.emoji == '❌':
                    await ctx.send("Shutdown cancelled.")
                else:
                    await ctx.send("Invalid reaction. Shutdown cancelled.")

            except TimeoutError:
                await ctx.send("No reaction received. Shutdown cancelled.")
        else:
            await ctx.message.add_reaction('❌')
            await ctx.reply("You do not have permission to shut the bot down!")
            

    


async def setup(bot):
    await bot.add_cog(Moderation(bot))

from discord.ext import commands
import discord


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *args):
        """Kick a user from the server"""
        reason = " ".join(args) if args else "No reason provided"
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


async def setup(bot):
    await bot.add_cog(Moderation(bot))

from discord.ext import commands
import discord
import datetime

class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Commands",
            colour=0xff0000,
            timestamp=datetime.datetime.now()
        )

        for cog, commands_list in mapping.items():
            if cog is None:
                cog_name = "No Category"
            else:
                cog_name = cog.qualified_name

            # Create a string to hold all commands for this category
            command_list = ""
            for command in commands_list:
                if command.name in self.context.bot.all_commands:
                    # Only include commands that are registered
                    command_list += f"`{self.context.prefix}{command.name}` | {command.help or 'No description'}\n"
            
            if command_list:  # Only add a field if there are commands to show
                embed.add_field(
                    name=f"**{cog_name}**",
                    value=command_list,
                    inline=False
                )

        channel = self.get_destination()
        await channel.send(embed=embed)

    
    async def command_not_found(self, string: str):
        # Customize what happens when a command is not found
        await self.get_destination().send(f"Command `{string}` not found.")

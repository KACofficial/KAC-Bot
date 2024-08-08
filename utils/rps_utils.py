import random
from discord import Interaction, ButtonStyle
from discord.ext import commands
from discord.ui import View, button, Button


class RockPaperScissors(View):
    def __init__(self, ctx: commands.Context) -> None:
        super().__init__(timeout=120)
        self.ai = random.choice(["Rock", "Paper", "Scissors"])
        self.ctx = ctx

    async def on_timeout(self) -> None:
        """This function will be called when this view expires. In this case, this view will expire in 120 seconds."""

        # Iterate over each button attached to this view and disable it
        for button in self.children:
            button.disabled = True
        await self.message.edit(view=self)

    async def interaction_check(self, interaction: Interaction) -> bool:
        """Checks if the user who is interacting with the buttons is the same as the author who invoked the command."""

        # If the user who interacted with the buttons is not the command invoker
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Hey! Those buttons ain't for you buddy", ephemeral=True)
            return False

        # If the user is the same as the command invoker, just disable all the buttons because it means the user has played their chance
        else:
            for button in self.children:
                button.disabled = True
            await self.message.edit(view=self)
            return True

    @button(label="Rock", emoji="🪨", style=ButtonStyle.secondary)
    async def rock_callback(self, interaction: Interaction, button: Button) -> None:
        if self.ai == "Rock":
            await interaction.response.send_message(
                f"You chose: **Rock**\nAI chose: **{self.ai}**\n\nResult: **IT'S A TIE!**")

        elif self.ai == "Paper":
            await interaction.response.send_message(
                f"You chose: **Rock**\nAI chose: **{self.ai}**\n\nResult: **AI WON!**")

        else:
            await interaction.response.send_message(
                f"You chose: **Rock**\nAI chose: **{self.ai}**\n\nResult: **YOU WON!**")

        # We need to explicitly stop this view using the 'stop' method
        # Otherwise, the 'on_timeout' function won't stop running even though the buttons might be disabled
        self.stop()

    @button(label="Paper", emoji="📰", style=ButtonStyle.secondary)
    async def paper_callback(self, interaction: Interaction, button: Button) -> None:
        if self.ai == "Rock":
            await interaction.response.send_message(
                f"You chose: **Paper**\nAI chose: **{self.ai}**\n\nResult: **YOU WON!**")

        elif self.ai == "Paper":
            await interaction.response.send_message(
                f"You chose: **Paper**\nAI chose: **{self.ai}**\n\nResult: **IT'S A TIE!**")

        else:
            await interaction.response.send_message(
                f"You chose: **Paper**\nAI chose: **{self.ai}**\n\nResult: **AI WON!**")

        self.stop()

    @button(label="Scissors", emoji="✂️", style=ButtonStyle.secondary)
    async def scissors_callback(self, interaction: Interaction, button: Button) -> None:
        if self.ai == "Rock":
            await interaction.response.send_message(
                f"You chose: **Scissors**\nAI chose: **{self.ai}**\n\nResult: **AI WON!**")

        elif self.ai == "Paper":
            await interaction.response.send_message(
                f"You chose: **Scissors**\nAI chose: **{self.ai}**\n\nResult: **YOU WON!**")

        else:
            await interaction.response.send_message(
                f"You chose: **Scissors**\nAI chose: **{self.ai}**\n\nResult: **IT'S A TIE!!**")

        self.stop()
import sys

import discord
from discord.ext import commands

from utils.bot import AdvancedBot
from utils.logger import CustomLogger


class ShutdownView(discord.ui.View):
    def __init__(self, logger: CustomLogger):
        super().__init__(disable_on_timeout=True)
        self.logger = logger

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message("Shutting down!", ephemeral=True)
        self.disable_all_items()
        await interaction.edit(view=self)
        self.stop()
        self.logger.warning(f"Shutdown by {interaction.user.name} ({interaction.user.id})")
        exit(0)

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send("Cancelled shutdown!", ephemeral=True)
        self.disable_all_items()
        await interaction.edit(view=self)
        self.stop()


class Shutdown(commands.Cog):
    def __init__(self, client):
        self.client: AdvancedBot = client
        self.logger = CustomLogger(self.client.start_stamp, name = "Shutdown Cog")

    @commands.slash_command(name = "shutdown", description="Initiate a shutdown of the bot")
    async def shutdown(self, ctx: discord.ApplicationContext) -> None:
        if await ctx.bot.is_owner(ctx.author):
            await ctx.respond("Confirm shutdown", view=ShutdownView(logger=self.logger), ephemeral=True)
        else:
            await ctx.followup.send("You are not allowed to shut down the bot.", ephemeral=True)


def setup(client):
    client.add_cog(Shutdown(client))

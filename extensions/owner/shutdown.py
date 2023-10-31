import sys

import discord
from discord.ext import commands

from utils.bot import AdvancedBot
from utils.logger import CustomLogger


class Shutdown(commands.Cog):
    def __init__(self, client):
        self.client: AdvancedBot = client
        self.logger = CustomLogger(self.client.start_stamp, name = "Shutdown Cog")

    @commands.slash_command(name = "shutdown", description="Initiate a shutdown of the bot")
    async def shutdown(self, ctx: discord.ApplicationContext) -> None:
        await ctx.defer()
        if await ctx.bot.is_owner(ctx.author):
            self.logger.warning(f"Shutting down due to {ctx.author.name}")
            await ctx.followup.send("Shutting down", ephemeral=True)
            exit(1)
        await ctx.followup.send("You are not allowed to shut down the bot.", ephemeral=True)


def setup(client):
    client.add_cog(Shutdown(client))

import discord
from discord.ext import commands

from utils.bot import AdvancedBot
from utils.logger import CustomLogger


modmail = discord.SlashCommandGroup("modmail")


def populate_autocomplete(ctx: discord.ApplicationContext) -> [str]:
    bot: AdvancedBot = ctx.bot
    bot.db.get_setting()


class ModMail(commands.Cog):
    def __init__(self, client):
        self.client: AdvancedBot = client

    @modmail.command(name = "create", description = "Create a new modmail to any server you and the bot are sharing.")
    async def create_communication(
            self,
            ctx: discord.ApplicationContext,
            server: discord.Option(autocomplete=populate_autocomplete)
    ) -> None:
        pass



def setup(client):
    client.add_cog(ModMail(client))

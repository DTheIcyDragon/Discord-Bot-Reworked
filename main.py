import discord
from discord.ext import commands

from utils.classes import AdvancedBot
import config

bot = AdvancedBot(
    command_prefix="?",
    intents=discord.Intents.all()
)


if __name__ == '__main__':
    bot.setup()
    bot.run(config.DISCORD_TOKEN)

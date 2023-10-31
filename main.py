import discord

from utils.bot import AdvancedBot
import config

bot = AdvancedBot(
    command_prefix="?",
    intents=discord.Intents.all()
)


@bot.listen("on_ready")
async def bot_ready_log() -> None:
    bot.logger.info(f"Logged in as \"{bot.user.name}\" ({bot.user.id})")
    bot.logger.info(f"On {len(bot.guilds)} guilds with {len(bot.users)} users")
    await bot.db.create_tables()


if __name__ == '__main__':
    bot.setup()
    bot.run(config.DISCORD_TOKEN)

import discord

import config
from utils.bot import AdvancedBot

bot = AdvancedBot(command_prefix="?", intents=discord.Intents.all())


@bot.listen("on_ready")
async def bot_ready_log() -> None:
    bot.logger.info(f'Logged in as "{bot.user.name}" ({bot.user.id})')
    bot.logger.info(f"On {len(bot.guilds)} guilds with {len(bot.users)} users")
    await bot.db.create_tables()


@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, exception: discord.DiscordException):
    if not ctx.command.has_error_handler():
        await ctx.response.send_message(
            embed=discord.Embed(
                title="Error",
                description=exception,
                colour=discord.Colour.brand_red(),
            ),
            ephemeral=True,
        )


if __name__ == "__main__":
    bot.setup()
    bot.run(config.DISCORD_TOKEN)

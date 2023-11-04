from typing import List

import discord
from discord.ext import commands

from utils.bot import AdvancedBot
from utils.logger import CustomLogger


async def populate_autocomplete(ctx: discord.ApplicationContext) -> [str]:
    answer: list[str] = []
    bot: AdvancedBot = ctx.bot
    resp = await bot.db.get_setting("modmail")
    for guild in resp:
        g = bot.get_guild(int(guild))
        answer.append(f"{g.name} ({g.id})")
    return answer


class ModMail(commands.Cog):
    def __init__(self, client):
        self.client: AdvancedBot = client

    modmail = discord.SlashCommandGroup("modmail")

    @modmail.command(
        name="open", description="Open a new modmail to any server you and the bot share and the feature is enabled."
    )
    @commands.dm_only()
    async def open_communication(
        self, ctx: discord.ApplicationContext, server: discord.Option(autocomplete=populate_autocomplete)
    ):
        gid = server[::-1].split("(")[0].removeprefix(")")
        guild = self.client.get_guild(int(gid[::-1]))
        resp = self.client.db.get_modmail(user=ctx.author, guild=guild)
        if resp is not None:
            return await ctx.response.send_message("You already have an open modmail", ephemeral=True)
        resp = await self.client.db.get_setting("modmail", guild)
        channel = guild.get_channel_or_thread(int(resp["value"]))
        msg = await channel.send(f"Modmail Thread for {ctx.author.name}")
        thread = await msg.create_thread(
            name=f"Modmail Thread for {ctx.author.name}"
        )
        self.client.db.add_modmail()
        await ctx.respond(
            "A modmail channel has been created for you! To stop the modmail with this server you may use "
            "`/modmail close` Please note that server moderators may also reopen communication to you."
        )


def setup(client):
    client.add_cog(ModMail(client))

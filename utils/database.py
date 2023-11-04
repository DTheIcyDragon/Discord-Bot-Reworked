from datetime import datetime as dt
from pathlib import Path
import sys
import typing

import aiosqlite
from discord import Guild

from utils.logger import CustomLogger


class DB:
    def __init__(self, file: str | Path, log_stamp: dt) -> None:
        self.file: Path = None
        self.logger = CustomLogger(log_stamp, name="DB Start")
        self.validate_file(file)
        self.logger = CustomLogger(log_stamp, name=self.file.name)
        self.logger.info(f"{self.file.name} is validated and ready")

    def validate_file(self, file):
        if type(file) is str:
            file = Path(file)
            if file.exists() and file.is_file():
                self.file = file
            else:
                file.touch()
                self.file = file
                self.logger.info(f"Created {file} as database")
        elif type(file) is Path and file.exists() and file.is_file():
            self.file = file
        else:
            self.logger.critical(f"{file} is an invalid database file")
            sys.exit(1)

    async def create_tables(self):
        conn = await aiosqlite.connect(self.file)
        cursor: aiosqlite.Cursor = await conn.cursor()
        try:
            await cursor.execute("CREATE TABLE IF NOT EXISTS settings (setting TEXT, value TEXT, guild INTEGER)")
        except BaseException as e:
            self.logger.critical(f"{e}")

    async def get_setting(self, setting: typing.Literal["join2create", "modmail"], guild: Guild) -> None | dict:
        conn = await aiosqlite.connect(self.file)
        cursor: aiosqlite.Cursor = await conn.cursor()
        await cursor.execute("SELECT * from settings WHERE setting = ? and guild = ?",
                                  (setting, guild.id))
        resp = await cursor.fetchone()
        if resp is None:
            return None
        else:
            return {
                "setting": resp[0],
                "value": resp[1],
                "guild_id": resp[2]
            }

    async def set_setting(self, setting: typing.Literal["join2create", "modmail"], value: str, guild: Guild) -> None:
        conn = await aiosqlite.connect(self.file)
        cursor: aiosqlite.Cursor = await conn.cursor()
        resp = await self.get_setting(setting=setting, guild = guild)
        if resp is None:
            await cursor.execute("INSERT INTO settings (setting, value, guild) VALUES (?, ?, ?)",
                                      (setting, value, guild.id))
        else:
            await cursor.execute("UPDATE settings SET value = ? WHERE setting = ? AND guild = ?",
                                      (setting, value, guild.id))
        cursor.connection.commit()

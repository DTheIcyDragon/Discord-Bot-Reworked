from utils.database import DB
from utils.logger import CustomLogger

from discord.ext.commands import Bot

from datetime import datetime as dt
import logging
import os
from pathlib import Path
import sys


class AdvancedBot(Bot):
    """The basic bot class to communicate with discord"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_stamp = dt.now()
        self.first_start = True
        self.logger: CustomLogger = None
        self.db = DB("data/main.sqlite", log_stamp=self.start_stamp)
        logging.getLogger("discord").setLevel(logging.DEBUG)

    def setup(self) -> None:
        """This function setups infrastructure the bot requires to operate"""
        if not Path("logs").exists():
            os.mkdir("logs")
            self.logger = CustomLogger(start_stamp=self.start_stamp,name="AdvancedBot")
            self.logger.info(f"Created logs directory")
        if self.logger is None:     # needed to create a logger in case the log directory exists
            self.logger = CustomLogger(start_stamp=self.start_stamp, name="AdvancedBot")
        if len(os.listdir("logs")) > 7:
            for file in os.listdir("logs"):
                os.remove("logs/" + file)
                self.logger.warning(f"Removed /logs/{file} to save some space!")
                break
        extensions = self.load_extensions(
            "extensions",
            recursive=True,
            store=True
        )
        for ext, value in extensions.items():
            if value is True:
                self.logger.info(f"Loaded {ext} successfully!")
            else:
                self.logger.critical(f"Failed to load {ext} due to {value}")
                sys.exit(1)

import sys

from discord.ext.commands import Bot

from datetime import datetime as dt
import logging
import os
from pathlib import Path


FMT = "[{levelname:^9}] [{asctime}] [{name}] [{module}:{lineno}] : {message}"
FORMATS = {
    logging.DEBUG: f"\33[37m{FMT}\33[0m",
    logging.INFO: f"\33[36m{FMT}\33[0m",
    logging.WARNING: f"\33[33m{FMT}\33[0m",
    logging.ERROR: f"\33[31m{FMT}\33[0m",
    logging.CRITICAL: f"\33[1m\33[31m{FMT}\33[0m",
}


class CustomFormatter(logging.Formatter):
    """A custom formatter for the console logger"""
    def format(self, record):
        log_fmt = FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt, style="{", datefmt="%d-%m-%y %H:%M:%S")
        return formatter.format(record)


class CustomLogger(logging.Logger):
    """A custom file and console logger"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_stamp = dt.now().strftime('%Y-%m-%d_%H+%M')
        file_handler = logging.FileHandler(f"logs/{self.start_stamp}.log", "a")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(FMT, style="{", datefmt="%d-%m-%y %H:%M:%S"))
        self.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(CustomFormatter())
        self.addHandler(console_handler)


class AdvancedBot(Bot):
    """The basic bot class to communicate with discord"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_start = True
        self.logger: CustomLogger = None
        logging.getLogger("discord").setLevel(logging.DEBUG)

    def setup(self) -> None:
        """This function setups infrastructure the bot requires to operate"""
        if not Path("logs").exists():
            os.mkdir("logs")
            self.logger = CustomLogger("AdvancedBot")
            self.logger.info(f"Created logs directory")
        if self.logger is None:     # needed to create a logger in case the log directory exists
            self.logger = CustomLogger("AdvancedBot")
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

# dict[str, Exception | bool] | list[str]
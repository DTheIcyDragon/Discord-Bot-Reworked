import logging
from datetime import datetime as dt


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
    def __init__(self, start_stamp: dt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_stamp = start_stamp
        file_handler = logging.FileHandler(f"logs/{self.start_stamp.strftime('%Y-%m-%d_%H+%M')}.log", "a")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(FMT, style="{", datefmt="%d-%m-%y %H:%M:%S"))
        self.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(CustomFormatter())
        self.addHandler(console_handler)
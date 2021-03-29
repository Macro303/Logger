#!/usr/bin/env python3
import logging
from logging import Formatter
from pathlib import Path

from colorama import init, Fore, Style

TOP_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = TOP_DIR.joinpath('logs')


class ColouredFormatter(Formatter):
    MAPPING = {
        logging.DEBUG: Fore.GREEN,
        logging.INFO: Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA
    }
    # PREFIX = '\033['
    # SUFFIX = '\033[0m'
    FORMAT = '[%(asctime)s] [%(levelname)-8s] {%(name)s} | %(message)s'

    def format(self, record):
        seq = self.MAPPING.get(record.levelno, Style.RESET_ALL)  # Default INFO
        # log_fmt = '{0}{1}m{2}{3}'.format(self.PREFIX, seq, self.FORMAT, self.SUFFIX)
        log_fmt = f"{seq}{self.FORMAT}"
        formatter = logging.Formatter(fmt=log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)


def init_logger(project: str, file_level=logging.DEBUG, console_level=logging.INFO, show_console: bool = True) -> None:
    root = logging.getLogger()
    logger = logging.getLogger(__name__)

    if show_console:
        init(autoreset=True)
        stream_logger = logging.StreamHandler()
        stream_logger.setLevel(console_level)
        stream_logger.setFormatter(ColouredFormatter())
        root.addHandler(stream_logger)

    LOG_DIR.mkdir(exist_ok=True)
    file_logger = logging.FileHandler(filename=LOG_DIR.joinpath(f"{project}.log"), encoding='UTF-8')
    file_logger.setLevel(file_level)
    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(levelname)-8s] {%(name)s:%(filename)s:%(lineno)d} | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_logger.setFormatter(formatter)
    root.addHandler(file_logger)

    root.setLevel(logging.NOTSET)
    logger.log(logging.DEBUG, 'DEBUG is Visible')
    logger.log(logging.INFO, 'INFO is Visible')
    logger.log(logging.WARNING, 'WARNING is Visible')
    logger.log(logging.ERROR, 'ERROR is Visible')
    logger.log(logging.CRITICAL, 'CRITICAL is Visible')

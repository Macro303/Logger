#!/usr/bin/env python3
import logging
from logging import Formatter
from pathlib import Path
from colorama import init

TOP_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = TOP_DIR.joinpath('logs')


class ColouredFormatter(Formatter):
    MAPPING = {
        logging.DEBUG: 32,  # Green
        logging.INFO: 37,  # White
        logging.WARNING: 33,  # Yellow
        logging.ERROR: 31,  # Red
        logging.CRITICAL: 35,  # Magenta
    }
    PREFIX = '\033['
    SUFFIX = '\033[0m'
    FORMAT = '[%(asctime)s] [%(levelname)-8s] {%(name)s} | %(message)s'

    def format(self, record):
        seq = self.MAPPING.get(record.levelno, 37)  # Default INFO
        log_fmt = '{0}{1}m{2}{3}'.format(self.PREFIX, seq, self.FORMAT, self.SUFFIX)
        formatter = logging.Formatter(fmt=log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)


def init_logger(project: str, file_level=logging.DEBUG, console_level=logging.INFO, show_console: bool = True) -> None:
    root = logging.getLogger()
    logger = logging.getLogger(__name__)

    if show_console:
        init()
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

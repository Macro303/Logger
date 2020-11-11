#!/usr/bin/env python3
import logging
from pathlib import Path

from .coloured_formatter import ColouredFormatter

TOP_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = TOP_DIR.joinpath('logs')


def init_logger(project: str, file_level = logging.DEBUG, console_level = logging.INFO, show_console: bool = True) -> None:
    root = logging.getLogger()
    logger = logging.getLogger(__name__)

    if show_console:
        stream_logger = logging.StreamHandler()
        stream_logger.setLevel(console_level)
        coloured_formatter = ColouredFormatter(
            fmt='[%(asctime)s] [%(levelname)-8s] {%(name)s:%(filename)s} | %(message)s'
        )
        stream_logger.setFormatter(coloured_formatter)
        root.addHandler(stream_logger)

    LOG_DIR.mkdir(exist_ok=True)
    file_logger = logging.FileHandler(filename=LOG_DIR.joinpath(f"{project}.log"), encoding='UTF-8')
    file_logger.setLevel(file_level)
    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(levelname)-8s] {%(name)s:%(filename)s:%(lineno)d} | %(message)s'
    )
    file_logger.setFormatter(formatter)
    root.addHandler(file_logger)

    root.setLevel(logging.NOTSET)
    logger.log(logging.NOTSET, 'NOTSET is Visible')
    logger.log(logging.DEBUG, 'DEBUG is Visible')
    logger.log(logging.INFO, 'INFO is Visible')
    logger.log(logging.WARNING, 'WARNING is Visible')
    logger.log(logging.ERROR, 'ERROR is Visible')
    logger.log(logging.CRITICAL, 'CRITICAL is Visible')

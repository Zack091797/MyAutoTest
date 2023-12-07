import sys
from pathlib import *

from loguru import logger


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


@singleton
class LoguruHelper:

    def __init__(self, log_file=False):
        self.__logger = logger
        self.__logger.remove()

        stderr_fmt = '[<cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan>]' \
                     '[<level>{level:<5}</level>]' \
                     '[<blue>{module}</blue>:<cyan>{line}</cyan>] - ' \
                     '<level>{message}</level>'
        self.__logger.add(sink=sys.stderr, level="TRACE", format=stderr_fmt,
                          backtrace=True, catch=True, diagnose=True,
                          enqueue=True)

        if log_file is True:
            logfile_fmt = '<light-green>{time:YYYY-MM-DD HH:mm:ss,SSS}</light-green>' \
                          '[<level>{level:<5}</level>]' \
                          '<cyan>{process.name}({process.id})</cyan>:' \
                          '<cyan>{thread.name:<10}({thread.id:<5})</cyan> | ' \
                          '<blue>{module}</blue>.<blue>{function}</blue>:' \
                          '<blue>{line}</blue> - <level>{message}</level>'
            self.__logger.add(sink=Path(Path.cwd(), "Log\\LoguruLog\\{time}.log"),
                              level="DEBUG", format=logfile_fmt, rotation="00:00",
                              retention="3 days", backtrace=True, catch=True,
                              diagnose=True, enqueue=True, encoding="utf-8")

    @property
    def logger(self):
        return self.__logger


loguHelper = LoguruHelper(log_file=True).logger

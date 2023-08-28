import logging


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


@singleton
class LogHelper:

    def __init__(self):
        self.__logger = logging.getLogger("Native")

    @property
    def logger(self):
        return self.__logger


logHelper = LogHelper().logger

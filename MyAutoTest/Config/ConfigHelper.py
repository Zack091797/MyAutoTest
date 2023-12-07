import configparser
from pathlib import Path


class ConfigHelper:
    """
    读取配置文件的封装类，简单封装，还需完善

    """

    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.read(Path(Path.cwd(), config_path))

    def get_str(self, section, option):
        return self.config.get(section, option)

    def get_int(self, section, option):
        return self.config.getint(section, option)

    def get_items(self, section, option):
        return self.config.items(section, option)

    def set(self):
        pass

    def add_section(self, sec):
        self.config.add_section(section=sec)

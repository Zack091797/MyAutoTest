from string import Template

import yaml
from pathlib import *


class YamlHelper:

    def __init__(self):
        pass

    def get_yaml_data(self, yaml_path) -> object:
        with open(Path(Path.cwd(), yaml_path), mode="r", encoding="utf-8") as f:
            value = yaml.safe_load(stream=f)
            return value

    def set_yaml_data(self, yaml_path, value):
        with open(Path(Path.cwd(), yaml_path), mode="a", encoding="utf-8") as f:
            yaml.safe_dump(value, stream=f, allow_unicode=True)

    def clear_yaml_data(self, yaml_path):
        with open(Path(Path.cwd(), yaml_path), mode="w", encoding="utf-8") as f:
            f.truncate()

    def template_yaml_data(self, yaml_path, value):
        with open(Path(Path.cwd(), yaml_path), mode="w", encoding="utf-8") as f:
            res = Template(f.read()).safe_substitute(value)
            return yaml.safe_load(res)


yamlHelper = YamlHelper()
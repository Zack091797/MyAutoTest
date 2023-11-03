from string import Template
from typing import Optional, Union

import yaml
from pathlib import *


class YamlHelper:

    def __init__(self):
        pass

    def get_yaml_data(self, yaml_path, key: Union[str, int] = None) -> object:
        """
        读取yaml文件的内容, 需设置一个key值，读取对应key值的value，默认值All读取全部yaml值

        :param key: key值或列表下标，默认None取全部yaml内容
        :param yaml_path: yaml文件路径
        :return:
        """
        with open(Path(Path.cwd(), yaml_path), mode="r", encoding="utf-8") as f:
            if key is None:
                value = yaml.safe_load(stream=f)
                return value
            elif isinstance(key, str):
                values = yaml.safe_load(stream=f)
                value = values.get(key, f"对应key-{key}的value不存在, 请检查key值!")
                return value
            elif isinstance(key, int):
                values = yaml.safe_load(stream=f)
                value = values[key]
                return value

    def set_yaml_data(self, yaml_path, value: Union[list, dict] = None):
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

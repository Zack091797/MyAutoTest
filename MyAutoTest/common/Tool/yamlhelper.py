from string import Template
from typing import Optional, Union

import yaml
from pathlib import *


class YamlHelper:

    def __init__(self):
        pass

    def get_yaml_data(self, yaml_path: str, key: Union[str] = None, index: Union[int] = None,
                      isOutsideDict=True) -> object:
        """
        读取yaml文件

        :param isOutsideDict: 判断yaml内容最外层数据类型，List或Dict，List取False，Dict取True，默认True
        :param index: 列表下标，默认None
        :param key: key值，默认None
        :param yaml_path: yaml文件路径
        :return:
        """
        with open(Path(Path.cwd(), yaml_path), mode="r", encoding="utf-8") as f:
            if key is None and index is None:
                value = yaml.safe_load(stream=f)
                return value
            elif key is not None and index is not None and isOutsideDict is False:
                values = yaml.safe_load(stream=f)
                value = values.get(index, "index对应的value不存在, 请检查index值!").get(key, "对应key的value不存在, 请检查key值!")
                return value
            elif key is not None and index is not None and isOutsideDict is True:
                values = yaml.safe_load(stream=f)
                value = values.get(key, "key对应的value不存在, 请检查key值!").get(index)
                return value
            elif key is not None:
                try:
                    values = yaml.safe_load(stream=f)
                    value = values.get(key, "key对应的value不存在, 请检查key值!")
                    return value
                except Exception as err:
                    print(err)
            elif index is not None:
                try:
                    values = yaml.safe_load(stream=f)
                    value = values.get(index, "index对应的value不存在, 请检查index值!")
                    return value
                except Exception as err:
                    print(err)

    def set_yaml_data(self, yaml_path: str, value: Union[list, dict] = None):
        with open(Path(Path.cwd(), yaml_path), mode="a", encoding="utf-8") as f:
            yaml.safe_dump(value, stream=f, allow_unicode=True)

    def clear_yaml_data(self, yaml_path):
        with open(Path(Path.cwd(), yaml_path), mode="w", encoding="utf-8") as f:
            f.truncate()

    def template_yaml_data(self, yaml_path, value):
        """弃用"""
        with open(Path(Path.cwd(), yaml_path), mode="w", encoding="utf-8") as f:
            res = Template(f.read()).safe_substitute(value)
            return yaml.safe_load(res)


yamlHelper = YamlHelper()

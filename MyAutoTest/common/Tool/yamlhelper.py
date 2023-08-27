import yaml


class YamlHelper:

    def __init__(self):
        pass

    def get_yaml_data(self, yaml_path) -> object:
        with open(yaml_path, mode="r") as f:
            value = yaml.safe_load(stream=f)
            return value

    def set_yaml_data(self, yaml_path, value):
        with open(yaml_path, mode="a", encoding="utf-8") as f:
            yaml.safe_dump(value, stream=f, allow_unicode=True)

    def clear_yaml_data(self, yaml_path):
        with open(yaml_path, mode="w", encoding="utf-8") as f:
            f.truncate()
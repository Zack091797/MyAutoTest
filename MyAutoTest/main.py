import importlib
import inspect
import json
from pathlib import Path

from Utils.LogConfig.LogConfig import logHelper
from Utils.Tool.render_template_jinja2 import render_template_by_jinja2
from Utils.Tool.yamlhelper import yamlHelper


def all_functions():
    """
    读取 debugtalk 模块下的所有function，return一个内置function对象的dict

    :return:
    """
    debug_module = importlib.import_module("debugtalk")
    all_function = inspect.getmembers(debug_module, inspect.isfunction)
    result = dict(all_function)
    return result


if __name__ == '__main__':
    pass
    # data = yamlHelper.get_yml_data(Path(Path.cwd(), r"testdata/yaml_data/test_swhy_corp.yml"))
    # data_json = json.dumps(data)
    # print(data_json)
    # data = {"test": [[1, 3, 5], [2, 4, 6]]}
    # yamlHelper.set_yml_data(r"testdata/yaml_data/test_swhy_corp.yml", data)
    # data = yamlHelper.get_yml_data(Path(Path.cwd(), r"testdata/yaml_data/test_swhy_corp.yml"))
    # print(data)
    print(None)


    # 1.yaml定义用例模板，test用例需要有校验必填字段的方法 -- jsonschma定义，入参和出参

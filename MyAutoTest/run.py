import importlib
import inspect
import os
from time import sleep

import jinja2
import pytest


def render(yml_path, **kwargs):
    path, filename = os.path.split(yml_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or './')).get_template(filename).render(**kwargs)


def all_functions():
    """
    运行此函数，将自动加载debug.py模块，并将方法调用结果统一存放入dict

    :return:
    """
    debug_module = importlib.import_module("debug")
    all_function = inspect.getmembers(debug_module, inspect.isfunction)
    result = dict(all_function)
    return result


if __name__ == "__main__":
    pytest.main(["./testcases/test_api/TestApiDemo.py"])

    # sleep(3)
    # os.system("allure generate ./allure_result -o ./allure_reports --clean")

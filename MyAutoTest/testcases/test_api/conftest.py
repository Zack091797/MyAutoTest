import copy
import importlib
import inspect

import pytest

from Utils.API.requesthelper import RequestHelper
from Utils.Tool.datahelper import dataHelper
from Utils.Tool.render_template_jinja2 import render_template_by_jinja2
from Utils.Tool.yamlhelper import yamlHelper

# pytest_plugins = ["case_plugins"]


req = None


@pytest.fixture(scope="function")
def get_case_data(request, debug_talk):
    csv_data = request.param
    csv_data.update(debug_talk)
    api_name = request.node.originalname
    yml_model = yamlHelper.get_yml_data(f"./testdata/yaml_model/{api_name}.yaml", index=0)
    test_data = render_template_by_jinja2(yml_model, csv_data)
    return test_data


@pytest.fixture(scope="class")
def get_class_data(request):
    module_name = request.module.__name__.rsplit(".", 1)[-1]


@pytest.fixture(scope="session")
def debug_talk():
    """
    读取 debugtalk 模块下的所有function，return一个内置function对象的dict

    :return:
    """
    debug_module = importlib.import_module("debugtalk")
    all_function = inspect.getmembers(debug_module, inspect.isfunction)
    result = dict(all_function)
    return result


@pytest.fixture(scope="session", name="req")
def initRequest():
    global req
    req = RequestHelper()
    return req

import copy

import pytest

from Utils.API.requesthelper import RequestHelper
from Utils.Tool.datahelper import dataHelper
from Utils.Tool.yamlhelper import yamlHelper

req = None


@pytest.fixture(scope="session", name="req")
def initRequest():
    global req
    req = RequestHelper()
    return req


@pytest.fixture(scope="function")
def get_case_data(request):
    csv_data = request.param
    api_name = request.node.originalname
    yml_model = yamlHelper.get_yml_data(f"./testdata/{api_name}.yaml", index=0)
    test_data = dataHelper.parse_yml(yml_model, csv_data)
    return test_data


@pytest.fixture(scope="class")
def get_class_data(request):
    module_name = request.module.__name__.rsplit(".", 1)[-1]
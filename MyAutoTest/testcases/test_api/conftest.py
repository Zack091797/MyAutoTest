import copy

import pytest

from common.API.requesthelper import RequestHelper
from common.Tool.datahelper import dataHelper
from common.Tool.yamlhelper import yamlHelper

req = None


@pytest.fixture(scope="session", name="req")
def initRequest():
    global req
    req = RequestHelper()
    return req


@pytest.fixture(scope="function")
def get_data(request):
    api_name = request.node.originalname
    csv_data = request.param
    yml_model = yamlHelper.get_yaml_data(f"./testdata/{api_name}.yaml")[0]
    test_data = dataHelper.parse_yml(yml_model, csv_data)
    return test_data


@pytest.fixture(scope="class")
def get_data_class(request):
    module_name = request.module.__name__.rsplit(".", 1)[-1]
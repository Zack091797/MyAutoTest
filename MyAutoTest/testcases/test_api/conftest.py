import pytest

from typing import Any
from Utils.API.requesthelper import RequestHelper
from Utils.LogConfig.LogConfig import logHelper
from Utils.Tool.render_template_jinja2 import render_template_by_jinja2
from Utils.Tool.yamlhelper import yamlHelper

# pytest_plugins = ["case_plugins"]


req = None


@pytest.fixture(scope="class")
def get_test_data(request, debug_talk):
    """
    fixture工厂方法, 通过传入的模板名称, 生成测试数据

    :param request:
    :param debug_talk:
    :return:
    """
    csv_data = request.param

    def _render_template(yamlTemplate: Any):
        debug_talk.update({"get_cache": getattr(request.config.cache, "get", None)})
        return render_template_by_jinja2(yamlTemplate, csv_data, **debug_talk)

    return _render_template


@pytest.fixture(scope="function")
def get_yaml_template(request) -> dict:
    template_name = request.node.originalname
    logHelper.info(f"提取路径->testdata/yaml_template/{template_name}.yaml用例模板...")
    yaml_template = yamlHelper.get_yml_data(f"./testdata/yaml_template/{template_name}.yaml", index=0)
    return yaml_template


@pytest.fixture(scope="session", name="req")
def initRequest():
    global req
    req = RequestHelper()
    return req

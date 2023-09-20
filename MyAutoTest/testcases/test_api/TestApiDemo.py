import re
import pytest

from MyAutoTest.common.API.apicase import ApiCase
from MyAutoTest.common.LogConfig.LogConfig import logHelper
from MyAutoTest.common.Tool.yamlhelper import yamlHelper


class TestApi(ApiCase):

    @pytest.mark.parametrize("get_data", yamlHelper.get_yaml_data("./testdata/test_api_demo.yaml"))
    def test_api_demo(self, req, get_data):
        req_name = get_data.get("name")
        req_method = get_data.get("request").get("method")
        req_url = get_data.get("request").get("url")
        req_data = get_data.get("request").get("data")
        req_validate = get_data.get("request").get("validate")
        logHelper.info(f"本次请求的用例名称: {req_name}")
        logHelper.info(f"请求使用的方法: {req_method}")
        logHelper.info(f"请求使用的路径: {req_url}")
        logHelper.info(f"请求使用的数据： {req_data}")
        # loguHelper.info(f"请求断言: {req_validate}")
        result = req.request(req_method, req_url, req_data)
        access_token = re.findall('"access_token":"(.*?)"', result.text)
        logHelper.info(f"获取的token： {access_token}")





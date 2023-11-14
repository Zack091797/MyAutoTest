import re
import pytest

from common.API.apicase import ApiCase
from common.LogConfig.LogConfig import logHelper
from common.Tool.yamlhelper import yamlHelper


class TestApi(ApiCase):

    @pytest.mark.parametrize("get_data", yamlHelper.get_yaml_data("./testdata/test_api_demo.yaml"))
    def test_api_get_token(self, req, get_data, cache):
        req_name = get_data.get("name")
        req_method = get_data.get("request").get("method")
        req_url = get_data.get("request").get("url")
        req_data = get_data.get("request").get("data")
        req_validate = get_data.get("request").get("validate")

        req_headers = {"content-type": "application/json"}

        logHelper.info(f"本次请求的用例名称: {req_name}")
        logHelper.info(f"请求使用的方法: {req_method}")
        logHelper.info(f"请求使用的路径: {req_url}")
        logHelper.info(f"请求header: {req_headers}")
        logHelper.info(f"请求使用的数据： {req_data}")
        logHelper.info(f"请求断言: {req_validate}")

        result = req.request(req_method, req_url, req_data, headers=req_headers)

        access_token = re.findall('"access_token":"(.*?)"', result.text)[0]
        logHelper.info(f"获取的token： {access_token}")

        yamlHelper.set_yaml_data("./testdata/tmpdata.yaml", {"access_token": access_token})
        cache.set("token", access_token)
        cache.set("default_token", "")

    def test_api_show_token(self, cache):
        logHelper.info(f"cache取出的token: {cache.get('token', None)}")
        logHelper.info(f"yaml取出的token: {yamlHelper.get_yaml_data('./testdata/tmpdata.yaml', key='access_token')}")

import json
import re

import jsonpath
import pytest
import pytest_check as check

from Utils.API.apicase import ApiCase
from Utils.LogConfig.LogConfig import logHelper
from Utils.Tool.datahelper import dataHelper
from Utils.Tool.yamlhelper import yamlHelper


@pytest.mark.parametrize("get_test_data", dataHelper.fromCsv2List("./testdata/csv_data/test_demo_api.csv"),
                         indirect=True)
class TestApi(ApiCase):
    """

    """

    def test_api_get_token(self, req, base_url, get_test_data, get_yaml_template, cache):
        request_data = self.create_request_data(base_url, get_test_data, get_yaml_template)
        # test_data = get_test_data(get_yaml_template)
        # req_name = test_data.get("step")
        # req_method = test_data.get("request").get("method")
        # req_url = base_url + test_data.get("request").get("url")
        # req_data = test_data.get("request").get("data")
        # req_validate = test_data.get("request").get("validate")
        # req_headers = {"content-type": "application/json"}
        #
        # logHelper.info(f"请求名称: {req_name}\n"
        #                f"请求方法: {req_method}\n"
        #                f"请求路径: {req_url}\n"
        #                f"请求header: {req_headers}\n"
        #                f"请求数据： {req_data}\n"
        #                f"请求断言: {req_validate}")

        resp = req.request(**request_data)
        logHelper.info(f"响应信息:{resp.text}")

        expires = None
        try:
            # jsonpath提取响应体expires_in
            resp_dict = json.loads(resp.text)
            expires = jsonpath.jsonpath(resp_dict, "$.expires_in")[0]
        except TypeError:
            logHelper.error(f"jsonpath未提取到目标值, 请检查响应详情!")
        except IndexError:
            logHelper.error(f"正则表达式未匹配到目标值, 请检查响应详情!")
        finally:
            pass

        access_token = None
        try:
            # 正则表达式提取响应体Token
            access_token = re.findall('"access_token":"(.*?)"', resp.text)[0]
            logHelper.info(f"获取的token： {access_token}")
            yamlHelper.set_yml_data("./testdata/tmpdata.yaml", {"access_token": access_token})
            cache.set("token", access_token)
            cache.set("default_token", "")
        except IndexError:
            logHelper.error(f"正则表达式未匹配到目标值, 请检查响应详情!")
        finally:
            pass
        # check.equal(req_validate, expires)
        # check.is_not_none(access_token)

    def test_api_show_token(self, get_test_data, cache):
        logHelper.info(f"cache取出的token: {cache.get('token', None)}")
        logHelper.info(f"yaml取出的token: {yamlHelper.get_yml_data('./testdata/tmpdata.yaml', key='access_token')}")

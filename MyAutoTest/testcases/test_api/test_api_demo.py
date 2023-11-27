import json
import re

import jsonpath
import pytest
import pytest_check as check
from Utils.API.apicase import ApiCase
from Utils.LogConfig.LogConfig import logHelper
from Utils.Tool.yamlhelper import yamlHelper
from Utils.Tool.datahelper import dataHelper


class TestApi(ApiCase):
    """

    """
    @pytest.mark.parametrize("get_case_data", dataHelper.fromCsv2List("./testdata/test_api_get_token.csv"), indirect=True)
    def test_api_get_token(self, req, set_testing_env, get_case_data, cache):
        req_name = get_case_data.get("name")
        req_method = get_case_data.get("request").get("method")
        req_url = set_testing_env + get_case_data.get("request").get("url")
        req_data = get_case_data.get("request").get("data")
        req_validate = get_case_data.get("request").get("validate")

        req_headers = {"content-type": "application/json"}

        logHelper.info(f"本次请求的用例名称: {req_name}")
        logHelper.info(f"请求使用的方法: {req_method}")
        logHelper.info(f"请求使用的路径: {req_url}")
        logHelper.info(f"请求header: {req_headers}")
        logHelper.info(f"请求使用的数据： {req_data}")
        logHelper.info(f"请求断言: {req_validate}")

        resp = req.request(method=req_method, url=req_url, params=req_data, headers=req_headers)

        logHelper.info(f"响应信息:{resp.text}")

        expires = None
        try:
            # jsonpath提取响应体expires_in
            resp_dict = json.loads(resp.text)
            expires = str(jsonpath.jsonpath(resp_dict, "$.expires_in")[0])
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
            yamlHelper.set_yaml_data("./testdata/tmpdata.yaml", {"access_token": access_token})
            cache.set("token", access_token)
            cache.set("default_token", "")
        except IndexError:
            logHelper.error(f"正则表达式未匹配到目标值, 请检查响应详情!")
        finally:
            pass

        check.equal(req_validate, expires)
        check.is_not_none(access_token)

    def test_api_show_token(self, cache):
        logHelper.info(f"cache取出的token: {cache.get('token', None)}")
        logHelper.info(f"yaml取出的token: {yamlHelper.get_yaml_data('./testdata/tmpdata.yaml', key='access_token')}")

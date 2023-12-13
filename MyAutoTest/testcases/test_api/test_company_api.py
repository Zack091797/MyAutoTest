import json
import re

import jsonpath
import pytest

from Utils.API.apicase import ApiCase
from Utils.LogConfig.LogConfig import logHelper
from Utils.Tool.datahelper import dataHelper


@pytest.mark.parametrize("get_test_data", dataHelper.fromCsv2List("./testdata/csv_data/test_company_api.csv"),
                         indirect=True)
class TestCompanyApi(ApiCase):

    def test_user_login(self, req, get_test_data, get_yaml_template, cache):
        test_data = get_test_data(get_yaml_template, cache)
        step = test_data.get("step")
        url = test_data.get("request").get("url")
        method = test_data.get("request").get("method")
        data = test_data.get("request").get("data")
        validate = test_data.get("request").get("validate")
        header = test_data.get("request").get("header")
        logHelper.info(f"请求名称: {step}\n"
                       f"请求方法: {method}\n"
                       f"请求路径: {url}\n"
                       f"请求header: {header}\n"
                       f"请求数据： {data}\n"
                       f"请求断言: {validate}")
        data_json = json.dumps(data)
        result = req.request(url=url, method=method, data=data_json, headers=header)
        access_token = re.compile('"accessToken":"(.*?)"').findall(result.text)[0]
        logHelper.info(f"提取的token:{access_token}")
        cache.set("access_token", access_token)

    def test_account_debenture(self, req, get_test_data, get_yaml_template, cache):
        test_data = get_test_data(get_yaml_template, cache)
        step = test_data.get("step")
        url = test_data.get("request").get("url")
        method = test_data.get("request").get("method")
        data = test_data.get("request").get("data")
        header = test_data.get("request").get("header")
        header.update({"access_token": cache.get("access_token", None)})
        logHelper.info(f"请求名称: {step}\n"
                       f"请求方法: {method}\n"
                       f"请求路径: {url}\n"
                       f"请求header: {header}\n"
                       f"请求数据： {data}\n")
        request_params = {"url": url, "method": method, "params": data, "headers": header}
        result = req.request(**request_params)
        stockholderAcct = jsonpath.jsonpath(result.json(), "$..data[?(@.mktCode=='05')].stockholderAcct")[0]
        logHelper.info(f"提取的stockholderAcct:{stockholderAcct}")
        cache.set("stockholderAcct", stockholderAcct)

    def test_account_debenture_open(self, req, get_test_data, get_yaml_template, cache):
        test_data = get_test_data(get_yaml_template, cache)
        step = test_data.get("step")
        url = test_data.get("request").get("url")
        method = test_data.get("request").get("method")
        data = test_data.get("request").get("data")
        header = test_data.get("request").get("header")
        data.get("stockHolderInfoDTOS")[0].update({"stockholderAcct": cache.get("stockholderAcct", None)})
        header.update({"access_token": cache.get("access_token", None)})
        data_json = json.dumps(data)
        logHelper.info(f"请求名称: {step}\n"
                       f"请求方法: {method}\n"
                       f"请求路径: {url}\n"
                       f"请求header: {header}\n"
                       f"请求数据： {data}\n")
        request_params = {"url": url, "method": method, "data": data_json, "headers": header}
        result = req.request(**request_params)
        print(result.text)
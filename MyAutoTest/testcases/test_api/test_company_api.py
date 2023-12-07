import json
import re
import pytest

from Utils.LogConfig.LogConfig import logHelper
from Utils.Tool.datahelper import dataHelper


@pytest.mark.parametrize("get_test_data", dataHelper.fromCsv2List("./testdata/csv_data/test_company_api.csv"),
                         indirect=True)
class TestCompanyApi:

    def test_user_login(self, req, get_test_data, cache):
        test_data = get_test_data(self.test_user_login.__name__)
        step = test_data.get("step")
        url = test_data.get("request").get("url")
        method = test_data.get("request").get("method")
        data = test_data.get("request").get("data")
        validate = test_data.get("request").get("validate")
        header = {"Content-Type": "application/json"}
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

    def test_customer_adaptability(self, req, get_test_data, cache):
        test_data = get_test_data(self.test_customer_adaptability.__name__)
        step = test_data.get("step")
        url = test_data.get("request").get("url")
        method = test_data.get("request").get("method")
        data = test_data.get("request").get("data")
        validate = test_data.get("request").get("validate")
        header = {"Content-Type": "application/json", "x-demeter-systemid": "001",
                  "access_token": cache.get("access_token", "")}
        logHelper.info(f"请求名称: {step}\n"
                       f"请求方法: {method}\n"
                       f"请求路径: {url}\n"
                       f"请求header: {header}\n"
                       f"请求数据： {data}\n"
                       f"请求断言: {validate}")
        data_json = json.dumps(data)
        result = req.request(url=url, method=method, data=data_json, headers=header)
        print(result.request.headers)
        print(result.text)

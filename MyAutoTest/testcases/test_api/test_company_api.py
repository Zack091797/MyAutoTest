import json
import re

import requests
from requests import Request

from Utils.API.requesthelper import RequestHelper


class TestCompanyApi:

    request = requests.session()

    def test_user_login(self, req, cache):
        url = "http://192.168.27.43:98/user/v1/login"
        method = "POST"
        header = {"Content-Type": "application/json"}
        data = {
            # 用户名
            "userName": "1633002554",
            # 用户密码
            "passWord": "135246",
            # 备注
            "verifyInfo": "",
            # 登录类型
            "loginType": "2"}
        data_json = json.dumps(data)

        result = req.request(url=url, method=method, data=data_json, headers=header)

        access_token = re.compile('"accessToken":"(.*?)"').findall(result.text)[0]
        print(f"提取的token:{access_token}")
        cache.set("access_token", access_token)

    def test_customer_adaptability(self, req, cache):
        url = "http://192.168.25.210:8006/business/v1/product/suitable/check"
        method = "POST"
        header = {"Content-Type": "application/json", "x-demeter-systemid": "001", "access_token": cache.get("access_token", "")}
        data = {
            # "fundAcc": "1633000091",
            "taCode": "99",
            "ofCode": "970191"}
        data_json = json.dumps(data)

        result = req.request(url=url, method=method, data=data_json, headers=header)
        print(result.request.headers)
        print(result.headers)
        print(result.text)



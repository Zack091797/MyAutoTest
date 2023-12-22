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
    def test_user_login(self, req, base_url, get_test_data, get_yaml_template, cache):
        request_data = self.create_request_data(base_url, get_test_data, get_yaml_template)
        data = json.dumps(request_data.get("data"))
        request_data.update({"data": data})
        resp = req.request(**request_data)
        print(resp.text)
        code = self.extract_resp(r"$.code", resp.json())
        msg = self.extract_resp(r'"msg":"(.*?)"', resp.text, ex_type="regular")
        accessToken = self.extract_resp(r"$..accessToken", resp.json())
        # self.check_validate()
        # self.check_validate()
        # self.check_validate()
        cache.set("access_token", accessToken)

    def test_use_token(self, get_test_data, cache):
        access_token = cache.get("access_token", None)
        logHelper.info(f"取得token: {access_token}")




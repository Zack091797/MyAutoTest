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

    def test_api_get_token(self, req, base_url, get_test_data, get_yaml_template, cache):
        request_data = self.create_request_data(base_url, get_test_data, get_yaml_template)
        resp = req.request(**request_data)
        logHelper.info(f"响应信息:{resp.text}")

        errcode = self.extract_resp(r'"errcode":(\d+)', resp.text, ex_type="regular")
        errmsg = self.extract_resp(r'$..errmsg', resp.json())
        print(errcode)
        print(errmsg)

        # check.equal(req_validate, expires)
        # check.is_not_none(access_token)

    def test_api_show_token(self, get_test_data, cache):
        logHelper.info(f"cache取出的token: {cache.get('token', None)}")
        logHelper.info(f"yaml取出的token: {yamlHelper.get_yml_data('./testdata/tmpdata.yaml', key='access_token')}")

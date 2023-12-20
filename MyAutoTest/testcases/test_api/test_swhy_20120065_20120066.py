import json

from Utils.API.apicase import ApiCase
from Utils.LogConfig.LogConfig import logHelper
from Utils.Tool.yamlhelper import yamlHelper


class TestCustModify(ApiCase):

    def test_ficc_corp_modify(self, req):
        header = {"Content-Type": "application/json"}
        method = "PUT"
        url = "http://192.168.25.210:8002/account/v1/org/cust/ficc/corp/modify"
        data = yamlHelper.get_yml_data()
        data_json = json.dumps(data)
        reqeust_data = {"url": url, "method": method, "data": data_json, "headers": header}
        result = req.request(**reqeust_data)
        logHelper.info(result.text)

    def test_ficc_prod_modify(self, req):
        pass

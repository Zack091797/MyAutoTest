import json

from Utils.API.apicase import ApiCase
from Utils.LogConfig.LogConfig import logHelper


class TestSwhyMsg(ApiCase):

    def test_batch_send_wechatcorp(self, req, cache):
        url = "http://192.168.27.31:34044/message/v1/wechatcorp/batch/send"
        header = {"Content-Type": "application/json"}
        method = "POST"
        data = {
            "type": "1",
            "namespace": "default",
            "targets": {"18800000010": {"name": "测试10", "verification_code": 100},
                        "18800000001": {"name": "测试20", "verification_code": 200}
                        },
            "templateType": "2",
            "content": "${name} 您好,您的验证码是: ${verification_code}",
            "templateId": "4E7557DDE727EFE436B53CA7D67CDD95",
            "param": {"name": "zh", "verification_code": 300},
            "mentionedList": [],
            "mentionedMobileList": []
        }
        data_json = json.dumps(data)
        request_data = {"url": url, "method": method, "data": data_json, "headers": header}
        result = req.request(**request_data)
        logHelper.info(result.text)
        print(result.request.headers)

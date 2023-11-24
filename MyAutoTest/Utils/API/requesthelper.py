import requests


class RequestHelper:

    def __init__(self):
        self.session = requests.session()

    def request(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        res = None
        method = method.upper()
        res = self.session.request(method=method, url=url, params=params, data=data, json=json, headers=headers, **kwargs)
        return res
from Utils.API.requesthelper import RequestHelper


class BaseApi:

    def __init__(self):
        self.request = RequestHelper()

import pytest

from MyAutoTest.common.API.requesthelper import RequestHelper

req = None


@pytest.fixture(scope="session", name="req")
def initRequest():
    global req
    req = RequestHelper()
    return req

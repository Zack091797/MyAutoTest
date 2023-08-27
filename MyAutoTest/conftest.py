import pytest

from common.Tool.mysqlhelper import MySqlHelper

sqlHelper = None


@pytest.fixture(scope="session", autouse=False)
def connect_sql():
    sqlHelper = MySqlHelper()


@pytest.fixture(scope="session", autouse=False)
def close_sql():
    yield
    pass
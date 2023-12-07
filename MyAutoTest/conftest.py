import pytest

from _pytest.config.argparsing import Parser

from Utils.LogConfig.LogConfig import logHelper
from Utils.Tool.datahelper import dataHelper
from Utils.Tool.mysqlhelper import MySqlHelper
from Config.ConfigHelper import ConfigHelper
from Utils.Tool.yamlhelper import yamlHelper

pytest_plugins = ["config_plugins"]

# 测试类实例化的数据库连接对象存入此列表，在测试类运行结束后断开连接
db_list = []


@pytest.fixture(scope="class")
def get_conn_database():
    """
    fixture工厂模式，建立数据库连接

    :return:
    """
    global db_list

    def _get_mysql_conn(database_info):
        db = MySqlHelper()
        db.connectDB(database_info)
        db_list.append(db)
        logHelper.info(f"成功连接数据库{db._database_info.get('database')}...")
        return db

    return _get_mysql_conn


@pytest.fixture(scope="class")
def disconn_database():
    """
    关闭测试类连接的数据库

    :return:
    """
    yield
    global db_list
    for index, db in enumerate(db_list):
        db.close()
        logHelper.info(f"关闭连接数据库{db._database_info.get('database')}...")


@pytest.fixture(scope="session")
def base_url(request):
    envCode = request.config.getoption("--envCode")
    configHelper = ConfigHelper("Config/env_config.ini")
    if envCode == "dev":
        base_url = configHelper.get_str("url settings", "dev_url")
    elif envCode == "test":
        base_url = configHelper.get_str("url settings", "test_url")
    else:
        base_url = configHelper.get_str("url settings", "uat_url")
    return base_url


@pytest.hookimpl
def pytest_addoption(parser: Parser):
    parser.addoption("--envCode",
                     action="store",
                     default="test",
                     type=str,
                     choices=["dev", "test", "uat"],
                     help="代码环境参数，-dev开发环境，-test测试环境，-uat用户环境")
    # parser.addoption("--testType",
    #                  action="store",
    #                  default="api",
    #                  type=str,
    #                  choices=["api", "ui"],
    #                  help="判断测试类型")

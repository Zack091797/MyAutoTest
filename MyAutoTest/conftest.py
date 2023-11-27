from time import sleep

import pytest
import datetime

from _pytest.config import Config
from _pytest.config.argparsing import Parser

from Utils.LogConfig.LogConfig import logHelper
from Utils.Tool.mysqlhelper import MySqlHelper
from Config.ConfigHelper import ConfigHelper

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
def set_testing_env(get_envCode, get_sslCode):
    configHelper = ConfigHelper("Config/env_config.ini")
    if get_envCode == "dev":
        base_host = configHelper.get_str("url settings", "dev_host")
        base_port = configHelper.get_str("url settings", "dev_port")
    elif get_envCode == "test":
        base_host = configHelper.get_str("url settings", "test_host")
        base_port = configHelper.get_str("url settings", "test_port")
    else:
        base_host = configHelper.get_str("url settings", "uat_host")
        base_port = configHelper.get_str("url settings", "uat_port")
    s = "" if get_sslCode == "False" else "s"
    base_url = f"http{s}://{base_host}:{base_port}" if base_port != "" else f"http{s}://{base_host}"
    return base_url



@pytest.fixture(scope="session")
def get_envCode(request):
    envCode = request.config.getoption("--envCode")
    logHelper.info(f"当前测试环境 ---> {envCode}")
    return envCode


@pytest.fixture(scope="session")
def get_sslCode(request):
    sslCode = request.config.getoption("--sslCode")
    logHelper.info(f"是否是ssl请求 ---> {sslCode}")
    return sslCode


@pytest.hookimpl
def pytest_addoption(parser: Parser):
    parser.addoption("--envCode",
                     action="store",
                     default="test",
                     type=str,
                     choices=["dev", "test", "uat"],
                     help="代码环境参数，-dev开发环境，-test测试环境，-uat用户环境")
    parser.addoption("--sslCode",
                     action="store",
                     default="False",
                     type=str,
                     choices=["True", "False"],
                     help="是否作为https请求?默认为否False")
    # parser.addoption("--testType",
    #                  action="store",
    #                  default="api",
    #                  type=str,
    #                  choices=["api", "ui"],
    #                  help="判断测试类型")


@pytest.hookimpl
def pytest_configure(config: Config):
    # -- 为 pytest.ini配置 中的log_file日志文件命名添加日期
    # hook读取配置的顺序，加载插件的顺序？
    log_file = config.inicfg.get("log_file", None)
    if log_file is not None:
        now = datetime.datetime.now()
        now_time = now.strftime("%Y-%m-%d")
        log_file_tmp = log_file.split(".")
        new_log_file = log_file_tmp[0] + "_" + now_time + "." + log_file_tmp[1]
        config.inicfg.update({"log_file": new_log_file})


@pytest.hookimpl
def pytest_collection_modifyitems(session, config, items):
    """
    测试用例收集完成后，将收集的用例的item属性 name 和 nodeid 转换为中文输出到控制台

    :param session:
    :param config:
    :param items:
    :return:
    """
    for index, item in enumerate(items):
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode_escape")

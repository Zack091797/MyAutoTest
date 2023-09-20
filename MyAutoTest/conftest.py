import pytest
import datetime

from _pytest.config import Config

from common.LogConfig.LogConfig import logHelper
from common.Tool.mysqlhelper import MySqlHelper

sqlHelper = None

database_info = [{"host": "", "port": "", "user": "", "password": "", "database": "", "charset": ""}]


@pytest.fixture(scope="session", params=database_info, autouse=False)
def connectSql(request):
    global sqlHelper
    sqlHelper = MySqlHelper(request.param)
    sqlHelper.connectDB()
    logHelper.info(f"数据库连接已打开...")
    return sqlHelper


@pytest.fixture(scope="session", autouse=False)
def closeSql():
    yield
    global sqlHelper
    if sqlHelper is not None:
        sqlHelper.close()
        sqlHelper = None
        logHelper.info("数据库连接已断开...")


def pytest_configure(config: Config):
    # -- 为 pytest.ini配置 中的log_file日志文件命名添加日期
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
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode_escape")

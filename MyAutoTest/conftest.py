from time import sleep

import pytest
import datetime

from _pytest.config import Config

from common.LogConfig.LogConfig import logHelper
from common.Tool.mysqlhelper import MySqlHelper

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


@pytest.fixture(scope="function")
def disconn_database():
    yield
    global db_list
    db = db_list[-1]
    db.close()
    logHelper.info(f"关闭连接数据库{db._database_info.get('database')}...")


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

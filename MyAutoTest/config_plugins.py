import datetime
from pathlib import Path

import pytest
from _pytest.config import Config


@pytest.hookimpl
def pytest_configure(config: Config):
    # -- 为 pytest.ini配置 中的log_file日志文件命名添加日期
    # hook读取配置的顺序，加载插件的顺序？
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    new_log_path = Path(config.rootdir, "Log/NativeLog/", f"native_{today}.log")
    print(f"本次执行日志记录于:{new_log_path}")
    config.option.log_file = new_log_path


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

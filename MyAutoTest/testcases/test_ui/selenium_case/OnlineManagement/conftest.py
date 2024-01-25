from time import sleep

import pytest

from UI_Objects.OnlineManagement.ProcessView import ProcessView_Page
from Utils.LogConfig.LogConfig import logHelper


@pytest.fixture()
def reset_side_bar(get_page_dict, init_page):
    yield
    processView = get_page_dict.get("processView", init_page(ProcessView_Page, "processView"))
    processView.js_scroll_into_view(f"//*[@id='ztree']/li[1]")
    text = processView.get_text(f"//*[@id='ztree']/li[1]/a/span[2]")
    logHelper.info(f"重定位至...{text}")





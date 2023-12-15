from time import sleep

import pytest

from UI_Objects.OnlineManagement.OnlineManagement_Home import Management_Home_Page
from UI_Objects.OnlineManagement.ProcessView import ProcessView_Page
import pytest_check as check

from Utils.LogConfig.LogConfig import logHelper


class TestOnlineManagement:

    @pytest.mark.dependency()
    def test_log_in(self, init_page, base_url):
        """用户登录系统"""
        home = init_page(Management_Home_Page, "home")
        home.open_url(base_url)
        logHelper.info(f"打开页面:{base_url}")
        home.login_account("liuyk", "admin")
        logHelper.info(f"输入账号:liuyk, 密码:admin")
        page_title = home.get_title()
        check.is_not_in("登录", page_title)
        if home.is_element_exist("//*[@id='jbox-state-state0']/div[2]/button"):
            #  处理密码过期弹框场景
            home.click_element("//*[@id='jbox-state-state0']/div[2]/button")
        else:
            pass
        sleep(1)

    @pytest.mark.usefixtures("reset_side_bar")
    @pytest.mark.dependency(depends=["test_log_in"], scope="class")
    def test_loopViewPage(self, init_page, base_url, cache):
        """循环查看业务页面加载是否报错"""
        processView = init_page(ProcessView_Page, "processView")
        processView.choose_top_menu("流程查看")
        processView.switch_iframe("//*[@id='mainFrame']")
        firstMenuLen = len(processView.locates("//*[@id='ztree']/li"))
        for i in range(firstMenuLen):
            processView.click_element(f"//*[@id='ztree']/li[{i + 1}]")
            firstMenuText = processView.get_text(f"//*[@id='ztree']/li[{i + 1}]/a/span[2]")
            secondMenuLen = len(processView.locates(f"//*[@id='ztree']/li[{i + 1}]/ul/li"))
            for j in range(int(secondMenuLen / secondMenuLen)):
                processView.click_element(f"//*[@id='ztree']/li[{i + 1}]/ul/li[{j + 1}]")
                secondMenuText = processView.get_text(f"//*[@id='ztree']/li[{i + 1}]/ul/li[{j + 1}]/a/span[2]")
                logHelper.info(f"打开菜单 {firstMenuText}->{secondMenuText}")
                processView.switch_iframe("//*[@id='officeContent']")
                processView.wait_condition(ConditionType=6, loc="/html/body/ul/li/a", value="流程列表")
                form_topic = processView.get_text("/html/body/ul/li/a")
                check.is_in("流程列表", form_topic)
                processView.switch_parent_frame()
                sleep(1)

    @pytest.mark.skip
    def test_multi_conditions_search(self, get_page_dict, init_page):
        processView = get_page_dict.get("processView", init_page(ProcessView_Page, "processView"))
        processView.click_element(("xpath", "//*[@id='ztree_2_span']"))

    @pytest.mark.skip
    def test_TripartiteDepositoryBank_View(self, init_page, base_url):
        """时间控件搜索"""
        processView = init_page(ProcessView_Page)
        processView.choose_top_menu("流程查看")
        processView.choose_left_menu("证券账户开立", "三方存管银行管理")
        processView.switch_iframe(("xpath", "//*[@id='officeContent']"))

        processView.click_element(("xpath", "//*[@id='startTime']"))
        processView.switch_default_content()
        processView.switch_iframe(("xpath", "/html/body/div[2]/iframe"))
        processView.click_element(("xpath", "//*[@id='dpTitle']/div[4]/input"))  # 点击年份框
        processView.action_send_keys("delete")
        processView.input_element(("xpath", "//*[@id='dpTitle']/div[4]/input"), 2022)
        processView.perform_actions()
        processView.click_element(("xpath", "//*[@id='dpTitle']/div[3]/input"))  # 点击月份框
        processView.click_element(("xpath", "//*[@id='dpTitle']/div[3]/div/table/tbody//tr/td[text()='一月']"))
        processView.click_element(
            ("xpath", "/html/body/div/div[3]/table/tbody//tr/td[text()='30' and  @class!= 'WotherDay']"))

        processView.switch_default_content()
        processView.switch_iframe(("xpath", "//*[@id='mainFrame']"))
        processView.switch_iframe(("xpath", "//*[@id='officeContent']"))

        processView.click_element(("xpath", "//*[@id='endTime']"))
        processView.switch_default_content()
        processView.switch_iframe(("xpath", "/html/body/div[2]/iframe"))
        processView.click_element(("xpath", "//*[@id='dpTitle']/div[4]/input"))  # 点击年份框
        processView.action_send_keys("delete")
        processView.input_element(("xpath", "//*[@id='dpTitle']/div[4]/input"), 2023)
        processView.perform_actions()
        processView.click_element(("xpath", "//*[@id='dpTitle']/div[3]/input"))  # 点击月份框
        processView.click_element(("xpath", "//*[@id='dpTitle']/div[3]/div/table/tbody//tr/td[text()='十二']"))
        processView.click_element(
            ("xpath", "/html/body/div/div[3]/table/tbody//tr/td[text()='10' and  @class!= 'WotherDay']"))

        processView.switch_default_content()
        processView.switch_iframe(("xpath", "//*[@id='mainFrame']"))
        processView.switch_iframe(("xpath", "//*[@id='officeContent']"))
        processView.click_element(("xpath", "//*[@id='btnSubmit']"))
        sleep(5)

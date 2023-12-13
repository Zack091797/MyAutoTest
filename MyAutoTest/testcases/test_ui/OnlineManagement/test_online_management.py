from time import sleep

import pytest

from UI_Objects.OnlineManagement.OnlineManagement_Home import Management_Home_Page
from UI_Objects.OnlineManagement.ProcessView import ProcessView_Page
import pytest_check as check


class TestOnlineManagement:

    @pytest.mark.usefixtures("slide_side_bar")
    @pytest.mark.dependency()
    def test_log_in(self, driver, base_url):
        """用户登录系统"""
        home = Management_Home_Page(driver)
        home.open_url(base_url)
        home.login_account("wy", "admin")
        page_title = home.get_title()
        check.is_not_in("登录", page_title)
        home.save_png_to_allure("首页")
        sleep(1)

    @pytest.mark.skip
    def test_TripartiteDepositoryBank_View(self, driver, base_url):
        """时间控件搜索"""
        processView = ProcessView_Page(driver)
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
        processView.click_element(("xpath", "/html/body/div/div[3]/table/tbody//tr/td[text()='30' and  @class!= 'WotherDay']"))

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
        processView.click_element(("xpath", "/html/body/div/div[3]/table/tbody//tr/td[text()='10' and  @class!= 'WotherDay']"))

        processView.switch_default_content()
        processView.switch_iframe(("xpath", "//*[@id='mainFrame']"))
        processView.switch_iframe(("xpath", "//*[@id='officeContent']"))
        processView.click_element(("xpath", "//*[@id='btnSubmit']"))
        sleep(5)

    @pytest.mark.skip
    @pytest.mark.dependency(depends=["test_log_in"], scope="class")
    def test_loopViewPage(self, driver, base_url):
        """循环查看业务页面加载是否报错"""
        processView = ProcessView_Page(driver)
        processView.choose_top_menu("流程查看")
        processView.switch_iframe(("xpath", "//*[@id='mainFrame']"))
        firstMenuLen = len(processView.locates(("xpath", "//*[@id='ztree']/li")))
        for i in range(firstMenuLen):
            processView.click_element(("xpath", f"//*[@id='ztree']/li[{i+1}]"))
            secondMenuLen = len(processView.locates(("xpath", f"//*[@id='ztree']/li[{i+1}]/ul/li")))
            for j in range(secondMenuLen):
                processView.click_element(("xpath", f"//*[@id='ztree']/li[{i+1}]/ul/li[{j+1}]"))
                processView.switch_iframe(("xpath", "//*[@id='officeContent']"))
                processView.wait_condition(6, loc=("xpath", "/html/body/ul/li/a"), value="流程列表")
                form_topic = processView.get_text(("xpath", "/html/body/ul/li/a"))
                check.is_in("流程列表", form_topic)
                processView.switch_parent_frame()
                sleep(1)


    # def test_

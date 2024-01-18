import re
import time

from Utils.LogConfig.LogConfig import logHelper
from Utils.UI.basepage import BasePage


class ProcessView_Page(BasePage):

    def choose_top_menu(self, menuTxt):
        self.switch_default_content()
        self.click_element(f"//*[@id='menu']//li/a/span[text()='{menuTxt}']")
        self.iframe_into_Main()

    def choose_left_menu(self, firstMenu, secondMenu):
        self.click_element(f"//*[@id='ztree']//li/a/span[text()='{firstMenu}']")
        self.click_element(
            f"//*[@id='ztree']//li/a/span[text()='{firstMenu}']/parent::a/following-sibling::ul//li/a/span[contains(text(), "
            f"'{secondMenu}')]")
        self.iframe_into_Content()

    def iframe_into_Main(self):
        self.switch_iframe("//*[@id='mainFrame']")

    def iframe_into_Content(self):
        self.switch_iframe("//*[@id='officeContent']")

    def input_custMobile(self, newMobile: str):
        """搜索条件-手机号"""
        self.input_element("//*[@id='newMobile']", newMobile)

    def input_custName(self, custName: str):
        """搜索条件-客户名称"""
        self.input_element("//*[@id='custName']", custName)

    def input_fundAcct(self, newFundAcct: str):
        """搜索条件-资金账号"""
        self.input_element("//*[@id='newFundAcct']", newFundAcct)

    def input_sysChannel(self, sysChannel: str):
        """搜索条件-渠道"""
        self.select_ComboBox("//*[@id='channel']", text=sysChannel)

    def input_certType(self, certType: str):
        """搜索条件-证件类型"""
        self.select_ComboBox("//*[@id='certType']", text=certType)

    def input_timeInterval(self, *timeInterval):
        """搜索条件-时间区间"""
        timeType = ("startTime", "endTime")
        for index, interval in enumerate(timeInterval):
            self.click_element(f"//*[@id='{timeType[index]}']")
            self.switch_default_content()
            self.switch_iframe("/html/body/div[2]/iframe")

            self.click_element("//*[@id='dpTitle']/div[4]/input")  # 点击年份框
            self.action_send_keys("delete")
            self.input_element("//*[@id='dpTitle']/div[4]/input", interval[0])  # 输入年份
            self.click_element("//*[@id='dpTitle']/div[3]/input")  # 点击月份框
            self.click_element(f"//*[@id='dpTitle']/div[3]/div/table/tbody//tr/td[text()='{interval[1]}']")  # 选择月份
            self.js_click_element(
                f"/html/body/div/div[3]/table/tbody//tr/td[text()='{interval[2]}' and  @class!= 'WotherDay']")  # 选择日期

            self.switch_default_content()
            self.iframe_into_Main()
            self.iframe_into_Content()

    def click_btnSubmit(self):
        """点击按钮-高级搜索"""
        self.click_element("//*[@id='btnSubmit']")

    def click_btnReset(self):
        """点击按钮-重置"""
        self.click_element("//*[@id='btnButton']")

    def click_btnProcessStatus(self, processStatus):
        """点击按钮-流程状态"""
        self.click_element(f"//*[@id='searchForm']/p/a[contains(text(), '{processStatus}')]")

    def getLen_processStatus(self, processStatus):
        """获取各流程状态的单据数量"""
        statusTxt = self.get_text(f"//*[@id='searchForm']/p/a[contains(text(), '{processStatus}')]")
        statusTxtLen = re.compile(r"[0-9]+").findall(statusTxt)[0]
        return statusTxtLen

    def getLen_tableInstance(self):
        "获取"
        tableTxt = self.get_text("/html/body/div/ul/li[last()]/a")
        tableLen = re.compile(r"[0-9]+").findall(tableTxt)[0]
        return tableLen


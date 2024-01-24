from time import sleep

from Utils.UI.basepage import BasePage


class ProcessCheck_Page(BasePage):

    def choose_top_menu(self, menuTxt):
        self.switch_default_content()
        self.click_element(f"//*[@id='menu']//li/a/span[text()='{menuTxt}']")

    def choose_left_menu(self, firstMenu, secondMenu):
        self.click_element(f"//*[@id='left']/div//div/div/a[contains(text(), '{firstMenu}')]")
        self.click_element(
            f"//*[@id='left']/div//div/div/a[contains(text(), '{firstMenu}')]/parent::div/following-sibling::div//a[contains(text(), '{secondMenu}')]")
        self.iframe_into_Main()

    def iframe_into_Main(self):
        self.switch_iframe("//*[@id='mainFrame']")

    def manual_Refresh(self):
        """手动刷新"""
        self.click_element("/html/body/div[6]/button")

    def getNum_PendingProcess(self, pendingNum):
        """获取各待办流程个数"""
        return self.get_text(f"/html/body//div/p[contains(text(), '{pendingNum}')]/span")

    def goto_PendingProcess(self, pendingTxt):
        """进入各待办流程"""
        self.click_element(f"/html/body//div/p/a[text()='{pendingTxt}']")

    def input_custOrgName(self, custOrgName):
        """搜索条件-营业部"""
        self.click_element("//*[@id='custOrgName']")
        self.switch_default_content()
        self.switch_iframe("//*[@id='jbox-iframe']")
        self.set_obviously_wait(3, until_or_not=False, loc="//*[@id='jbox-content-loading']")
        sleep(2)
        self.input_element("//*[@id='key']", custOrgName)
        self.click_element("//*[@id='tree']/li[@style='']/ul/li[@style='']/ul/li[@style='']/ul/li[@style='']/a[1]")
        self.switch_default_content()
        self.click_element("//*[@id='jbox-state-state0']/div[2]/button[1]")
        self.iframe_into_Main()

    def input_custName(self, custName: str):
        """搜索条件-客户姓名"""
        self.input_element("//*[@id='custName']", custName)

    def input_custMobile(self, custMobile):
        """搜索条件-手机号"""
        self.input_element("//*[@id='mobile']", custMobile)

    def input_fundAcct(self, fundAcct):
        """搜索条件-资金账号"""
        self.input_element("//*[@id='fundAcct']", fundAcct)

    def input_businessNum(self, businessNum: str):
        """搜索条件-业务类型"""
        self.select_ComboBox("//*[@id='businessNum']", text=businessNum)

    def input_businessStatus(self, businessStatus):
        """搜索条件-业务状态"""
        self.select_ComboBox("//*[@id='processStatus']", text=businessStatus)

    def input_sysChannel(self, sysChannel):
        """搜索条件-渠道"""
        self.select_ComboBox("//*[@id='channel']", text=sysChannel)

    def input_timeInterval(self, *timeInterval):
        """搜索条件-时间区间"""
        timeType = ("startTime", "finishTime")
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

    def input_staffId(self, staffId):
        """搜索条件-审核人工号"""
        self.input_element("//*[@id='staffId']", staffId)

    def input_checkStatus(self, checkStatus):
        """搜索条件-审核结果"""
        self.select_ComboBox("//*[@id='status']", text=checkStatus)

    def input_auditStatus(self, auditStatus):
        """搜索条件-见证结果"""
        self.select_ComboBox("//*[@id='auditStatus']", text=auditStatus)

    def input_auditTimeInterval(self, *timeInterval):
        """搜索条件-见证时间区间"""
        timeType = ("auditStartTime", "auditEndTime")
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

    def click_btnSubmit(self):
        """点击按钮-高级搜索"""
        self.click_element("//*[@id='btnSubmit']")



















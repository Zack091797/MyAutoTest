from Utils.UI.basepage import BasePage


class ProcessCheck_Page(BasePage):

    def choose_top_menu(self, menuTxt):
        self.switch_default_content()
        self.click_element(f"//*[@id='menu']//li/a/span[text()='{menuTxt}']")

    def choose_left_menu(self, firstMenu, secondMenu):
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

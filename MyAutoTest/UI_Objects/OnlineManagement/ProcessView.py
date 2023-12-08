from Utils.UI.basepage import BasePage


class ProcessView_Page(BasePage):

    def choose_top_menu(self, menuTxt):
        self.click_element(("xpath", f"//*[@id='menu']//li/a/span[text()='{menuTxt}']"))

    def choose_left_menu(self, firstMenu, secondMenu):
        self.switch_iframe(("xpath", "//*[@id='mainFrame']"))
        self.click_element(("xpath", f"//*[@id='ztree']//li/a/span[text()='{firstMenu}']"))
        self.click_element(("xpath",
                            f"//*[@id='ztree']//li/a/span[text()='{firstMenu}']/parent::a/following-sibling::ul//li/a/span[contains(text(), '{secondMenu}')]"))

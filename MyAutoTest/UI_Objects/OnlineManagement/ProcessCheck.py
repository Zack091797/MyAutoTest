from Utils.UI.basepage import BasePage


class ProcessCheck_Page(BasePage):

    def choose_top_menu(self, menuTxt):
        self.switch_default_content()
        self.click_element(f"//*[@id='menu']//li/a/span[text()='{menuTxt}']")

    def choose_left_menu(self, firstMenu, secondMenu):
        self.click_element(f"//*[@id='left']/div//div/div/a[contains(text(), '{firstMenu}')]/parent::div/following-sibling::div//a[contains(text(), '{secondMenu}')]")
        self.iframe_into_Main()

    def iframe_into_Main(self):
        self.switch_iframe("//*[@id='mainFrame']")
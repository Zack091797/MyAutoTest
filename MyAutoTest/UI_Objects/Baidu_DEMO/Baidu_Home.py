from Utils.UI.basepage import BasePage


class BaiDu_Home_Page(BasePage):

    def search_input(self, search_key):
        self.input_element(loc="//*[@id='kw']", content=search_key)

    def search_button(self):
        self.click_element(loc="//*[@id='su']")

from Utils.UI.basepage import BasePage


class Management_Home_Page(BasePage):

    def login_account(self, userAcc, userPass):
        self.input_element("//*[@id='username']", userAcc)
        self.input_element("//*[@id='password']", userPass)
        self.click_element("//*[@id='loginForm']/input[3]")




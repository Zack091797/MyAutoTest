from time import sleep

from UI_Objects.Baidu_DEMO.Baidu_Home import BaiDu_Home_Page


class Test_BaiDu_Demo:
    """

    """

    def test_baidu_search(self, base_url, driver):
        home = BaiDu_Home_Page(driver)
        home.open_url(base_url)
        home.search_input("UI自动化")
        home.search_button()
        sleep(5)

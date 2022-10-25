from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.action = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 20)

    def locate(self, loc):
        """
        定位元素

        :param loc: 列表或元组，包含定位方式和定位元素
        :return:
        """
        return self.driver.find_element(*loc)

    def locates(self, loc, index=None):
        """
        定位组元素组，若index为None，则返回一组元素对象list；否则返回对应下标的单个元素对象

        :param loc: 列表或元组，包含定位方式和定位元素
        :param index: 定位组元素对象的子元素对象，默认为None
        :return:
        """
        if index is None:
            return self.driver.find_elements(*loc)
        else:
            return self.driver.find_elements(*loc)[index]

    def move_above_element(self, loc):
        pass
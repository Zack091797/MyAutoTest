import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    """
    基于Selenium的POM模式页面基类，封装各Selenium及自定义操作及方法，页面类继承此类。
    业务用例中实例化各页面对象，调用组装页面实例对象的属性方法，实现业务场景操作。
    """
    def __init__(self, driver):
        self.driver = driver
        self.action = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 20)

    def locate(self, loc: iter):
        """
        定位元素，返回WebElement对象

        :param loc: 列表或元组，包含定位方式和定位元素
        :return:
        """
        return self.driver.find_element(*loc)

    def locates(self, loc: iter, index=None):
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

    def open_url(self, url):
        """
        浏览器跳转url

        :param url: 目标url
        :return:
        """
        self.driver.get(url)

    def click_element(self, loc: iter):
        """
        点击元素

        :param loc: 列表或元组，包含定位方式和定位元素
        :return:
        """
        self.locate(loc).click()

    def input_element(self, loc, content):
        """
        在元素上输入文本内容content

        :param loc: 目标元素对象xpath
        :param content: 输入内容
        :return:
        """
        self.locate(loc).send_keys(content)

    def wait_condition(self, until_or_not, EC, *args, **kwargs):
        """
        显示等待条件

        :param until_or_not:
        :param EC:
        :param args:
        :param kwargs:
        :return:
        """
        if until_or_not == "until":
            self.wait.until()
        elif until_or_not == "until_not":
            self.wait.until_not()

    def set_implicitly_wait(self, wait_time=10):
        """
        设置隐式等待，默认10s

        :param wait_time:
        :return:
        """
        self.driver.implicitly_wait(wait_time)

    def move_above_element(self, loc):
        """
        鼠标悬停元素之上

        :param loc:
        :return:
        """
        self.action.move_to_element(self.locate(loc))

    def perform_actions(self):
        """
        鼠标执行链式操作

        :return:
        """
        self.action.perform()

    def reset_actions(self):
        """
        重置鼠标链式操作

        :return:
        """
        self.action.reset_actions()

    def get_title(self):
        return self.driver.title

    def get_text(self, loc):
        return self.locate(loc).text

    def do_js(self, script):
        """
        driver执行js脚本

        :param script:
        :return:
        """
        self.driver.excute_script(*script)

    def js_click_element(self, loc):
        """
        js点击元素，解决遮挡导致误点击问题

        :return:
        """
        self.driver.do_js(("arguments[0].click()", self.locate(loc)))

    def js_input_element(self, loc, content):
        """
        js输入文本

        :param loc:
        :param content:
        :return:
        """
        self.driver.do_js((f"arguments[0].value={content}", self.locate(loc)))

    def js_remove_attribute(self, loc, attr):
        """
        js去除元素属性

        :param loc:
        :param attr:
        :return:
        """
        self.driver.do_js((f"arguments[0].removeAttribute({attr})", self.locate(loc)))

    def js_scroll_into_view(self, loc):
        """
        js定位滚动至元素

        :param loc:
        :return:
        """
        self.driver.do_js(("arguments[0].scrollIntoView()", self.locate(loc)))

    def set_maximize_window(self):
        """
        窗口最大化

        :return:
        """
        self.driver.maximize_window()

    def set_custom_window_size(self, width, height):
        """
        自定义窗口尺寸

        :param width:
        :param height:
        :return:
        """
        self.driver.set_window_size(width, height)

    def get_now_window_handle(self):
        """
        获取浏览器当前窗口句柄

        :return:
        """
        return self.driver.current_window_handle

    def get_all_window_handles(self):
        """
        获取浏览器所有窗口句柄

        :return:
        """
        return self.driver.window_handles

    def switch_window_to_new(self, index=-1):
        """
        切换窗口句柄

        :param index:
        :return:
        """
        handles = self.get_window_handles()
        self.driver.switch_to.window(handles[index])

    def switch_iframe(self, loc):
        """
        切换子iframe

        :param loc:
        :return:
        """
        self.driver.switch_to.frame(self.locate(loc))

    def switch_parent_frame(self):
        """
        切换至上一层frame

        :return:
        """
        self.driver.switch_to.parent_frame()

    def switch_default_content(self):
        """
        切换出frame

        :return:
        """
        self.driver.switch_to.default_content()

    def switch_alert(self):
        """
        切换至告警框
        alert.accept()-确认
        alert.dismiss()-取消
        alert.send_keys()-告警输入
        alert.text-获取告警文本

        :return:
        """
        return self.driver.switch_to.alert

    def get_screenshot_as_png(self):
        """
        浏览器截取当前屏幕画面存为png格式图片

        :return:
        """
        return self.driver.get_screenshot_as_png()

    def save_png_to_allure(self, png_name):
        """
        将当前浏览器页面截图存入allure报告

        :param png_name:
        :return:
        """
        allure.attach(self.get_screenshot_as_png(), png_name, allure.attachment_type.PNG)

    # 下拉选择封装...








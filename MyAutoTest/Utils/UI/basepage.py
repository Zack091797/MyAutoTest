from time import sleep
from typing import Union, Literal

import allure
import pyautogui
from selenium.common import WebDriverException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from Utils.LogConfig.LogConfig import logHelper


class BasePage:
    """
    基于Selenium的POM模式页面基类，封装各Selenium及自定义操作及方法，页面类继承此类。
    业务用例中实例化各页面对象，调用组装页面实例对象的属性方法，实现业务场景操作。
    """

    def __init__(self, driver):
        self.driver = driver
        self.action = ActionChains(self.driver)
        self.wait = None
        self.select = None

    def locate(self, loc: str, by="xpath"):
        """
        定位元素，返回WebElement对象

        :param by:
        :param loc: 列表或元组，包含定位方式和定位元素
        :return:
        """
        loc = (by, loc)
        return self.driver.find_element(*loc)

    def locates(self, loc: str, by="xpath", index=None):
        """
        定位组元素，若index为None，则返回一组元素对象list；否则返回对应下标的单个元素对象

        :param by:
        :param loc: 列表或元组，包含定位方式和定位元素
        :param index: 定位组元素对象的子元素对象，默认为None
        :return:
        """
        loc = (by, loc)
        if index is None:
            return self.driver.find_elements(*loc)
        else:
            return self.driver.find_elements(*loc)[index]

    def is_element_exist(self, loc: str):
        try:
            self.locate(loc)
            return True
        except NoSuchElementException:
            return False
        except WebDriverException:
            return False

    def open_url(self, url):
        """
        浏览器跳转url

        :param url: 目标url
        :return:
        """
        self.driver.get(url)

    def goto_next(self):
        """浏览器前进一页"""
        self.driver.forward()

    def back_previous(self):
        """浏览器后退一页"""
        # js执行后退
        # self.do_js("window.history.back()")
        self.driver.back()

    def refresh_page(self):
        """浏览器页面刷新"""
        self.driver.refresh()

    def windows_PropScale(self, prop: int, model: Literal["down", "up"] = "down"):
        """页面比例缩放, webdriver控制不了ctrl+-缩放页面，这里引入pyautogui库"""
        if model == "down":
            for i in range(0, prop):
                pyautogui.hotkey("ctrl", "-")
            logHelper.info(f"页面缩小...")
        else:
            for i in range(0, prop):
                pyautogui.hotkey("ctrl", "+")
            logHelper.info(f"页面放大...")

    def click_element(self, loc: str, index: Union[int | None] = None):
        """
        点击元素

        :param index:
        :param loc: 列表或元组，包含定位方式和定位元素
        :return:
        """
        if index is None:
            self.locate(loc).click()
        else:
            self.locates(loc, index=index).click()

    def input_element(self, loc: str, content: str):
        """
        在元素上输入文本内容content

        :param loc: 目标元素对象xpath
        :param content: 输入内容
        :return:
        """
        self.locate(loc).send_keys(content)

    def wait_condition(self, ConditionType: int, *args, by="xpath", **kwargs):
        """
        显示等待条件, 不应该用数字代表条件，应改成条件简称

        0 判断 title 是否等于预期 value

        1 判断 title 是否包含预期 value

        2 判断元素是否被加载到 dom 树，传入locator， 不代表元素一定可见

        3 判断元素是否可见，传入 locator，可见代表元素非隐藏，宽高都不等于0

        4 判断元素是否可见，传入 webelement

        5 判断元素是否不存在于 dom 树或不可见

        6 判断元素的 text 是否包含预期 value

        7 判断元素的 value 属性是否包含预期 value

        8 判断 frame 是否可以 switch 切换进入，True 则切换进入，反之 False

        9 判断元素可见且可点击

        10 判断元素不可点击

        11 判断元素
        :param by:
        :param ConditionType:
        :param args:
        :param kwargs:
        :return:
        """
        loc: str = (by, kwargs.get("loc", ""))
        value: str = kwargs.get("value", "")
        until_or_not: bool = kwargs.get("until_or_not", True)
        obviously_method = getattr(self.wait, "until") if until_or_not is True else getattr(self.wait, "until_not")
        obviously_result = None
        match ConditionType:
            case 0:
                assert_msg = f"页面title与{value}不匹配!!!" if until_or_not is True else f"页面title仍是{value}!!!"
                obviously_result = obviously_method(EC.title_is(value), assert_msg)
            case 1:
                assert_msg = f"页面title不包含{value}!!!" if until_or_not is True else f"页面title不包含{value}!!!"
                obviously_result = obviously_method(EC.title_contains(value), assert_msg)
            case 2:
                assert_msg = f"页面不存在预期元素!!!" if until_or_not is True else f"页面仍存在预期元素!!!"
                obviously_result = obviously_method(EC.presence_of_element_located(loc), assert_msg)
            case 3:
                assert_msg = f"预期元素在页面不可见!!!" if until_or_not is True else f"预期元素在页面仍可见!!!"
                obviously_result = obviously_method(EC.visibility_of_element_located(loc), assert_msg)
            case 4:
                assert_msg = f"预期元素在页面未出现!!!" if until_or_not is True else f"预期元素在页面未消失!!!"
                obviously_result = obviously_method(EC.visibility_of(self.locate(loc)), assert_msg)
            case 5:
                if until_or_not is True:
                    self.wait.until()
                else:
                    self.wait.until_not()
            case 6:
                assert_msg = f"元素未包含文本{value}!!!" if until_or_not is True else f"元素仍包含文本{value}!!!"
                obviously_result = obviously_method(EC.text_to_be_present_in_element(loc, value), assert_msg)
        return obviously_result

    def set_obviously_wait(self, ConditionType, *args, implicitly_time: float = 10.0, obviously_time: float = 20.0, **kwargs):
        """
        设置显示等待之前需要关闭全局隐式等待，完成之后再重新设置隐式等待
        显示等待条件, 不应该用数字代表条件，应改成条件简称

        0 判断 title 是否等于预期 value

        1 判断 title 是否包含预期 value

        2 判断元素是否被加载到 dom 树，不代表元素一定可见

        3 判断元素是否可见，传入 locator，可见代表元素非隐藏，宽高都不等于0

        4 判断元素是否可见，传入 webelement

        5 判断元素是否不存在于 dom 树或不可见

        6 判断元素的 text 是否包含预期 value

        7 判断元素的 value 属性是否包含预期 value

        8 判断 frame 是否可以 switch 切换进入，True 则切换进入，反之 False

        9 判断元素可见且可点击

        10 判断元素不可点击

        11 判断元素
        :return:
        """
        self.wait = WebDriverWait(self.driver, obviously_time)
        try:
            self.set_implicitly_wait(0)
            self.wait_condition(ConditionType, *args, **kwargs)
        except WebDriverException as err:
            raise err
        finally:
            self.wait = None
            self.set_implicitly_wait(implicitly_time)

    def set_implicitly_wait(self, implicitly_time=10):
        """
        设置隐式等待，默认10s

        :param implicitly_time:
        :return:
        """
        self.driver.implicitly_wait(implicitly_time)

    def set_scripts_timeout(self, timeout=15):
        """
        设置异步脚本等待超时时间

        :param timeout:
        :return:
        """
        self.driver.set_script_timeout(timeout)

    def set_pages_load_timeout(self, timeout=20):
        """
        设置页面加载超时时间

        :param timeout:
        :return:
        """
        self.driver.set_page_load_timeout(timeout)

    def move_above_element(self, loc: str):
        """
        鼠标悬停元素之上

        :param loc:
        :return:
        """
        self.action.move_to_element(self.locate(loc))

    def action_send_keys(self, keyBoard):
        match keyBoard:
            case "SELECTALL":
                self.action.send_keys(Keys.CONTROL, "a")
            case "COPY":
                self.action.send_keys(Keys.CONTROL, "c")
            case "PASTE":
                self.action.send_keys(Keys.CONTROL, "v")
            case "DELETE":
                self.action.send_keys(Keys.DELETE)
            case "ENTER":
                self.action.send_keys(Keys.ENTER)
            case _:
                pass
        self.perform_actions()

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
        """
        获取当前页面标题

        :return:
        """
        return self.driver.title

    def get_current_url(self):
        """
        获取当前页面url

        :return:
        """
        return self.driver.current_url

    def get_browser_name(self):
        """
        获取当前浏览器名称

        :return:
        """
        return self.driver.name

    def get_page_source(self):
        """
        获取当前页面源码

        :return:
        """
        return self.driver.page_source

    def get_text(self, loc: str):
        """
        获取指定元素文本

        :param loc:
        :return:
        """
        return self.locate(loc).text.strip()

    def get_element_attribute(self, loc: str, attr: str):
        """
        返回指定元素的指定属性

        :param loc:
        :param attr:
        :return:
        """
        return self.locate(loc).get_attribute(attr)

    def do_js(self, script: iter):
        """
        driver执行js脚本

        :param script:
        :return:
        """
        self.driver.execute_script(*script)

    def js_click_element(self, loc: str):
        """
        js点击元素，解决遮挡导致误点击问题

        :return:
        """
        self.do_js(("arguments[0].click()", self.locate(loc)))

    def js_input_element(self, loc: str, content: str):
        """
        js输入文本

        :param loc:
        :param content:
        :return:
        """
        self.do_js((f"arguments[0].value={content}", self.locate(loc)))

    def js_remove_attribute(self, loc: str, attr: str):
        """
        js去除元素属性

        :param loc:
        :param attr:
        :return:
        """
        self.do_js((f"arguments[0].removeAttribute({attr})", self.locate(loc)))

    def js_change_attribute(self, loc: str, attr: str, new_value: str):
        """
        js修改元素属性

        :param loc:
        :param attr:
        :param new_value:
        :return:
        """
        self.do_js(f"arguments[0].{attr}={new_value}", self.locate(loc))

    def js_scroll_into_view(self, loc: str):
        """
        js定位滚动至元素

        :param loc:
        :return:
        """
        self.do_js(("arguments[0].scrollIntoView()", self.locate(loc)))

    def js_scroll_side_bar(self, loc: str):
        "未完"
        self.do_js("window.scrollTo")

    def js_body_style_transform(self, prop: float):
        """js调整页面缩放-会偏移，暂时不用"""
        # self.do_js((f"document.body.style.transform='scale({prop})'",))
        self.do_js((f"chrome.settingsPrivate.setDefaultZoom({prop});"))
        sleep(1)

    def set_maximize_window(self):
        """
        窗口最大化

        :return:
        """
        self.driver.maximize_window()

    def set_customer_window_size(self, width, height):
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
        handles = self.get_all_window_handles()
        self.driver.switch_to.window(handles[index])

    def switch_iframe(self, loc: str):
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

    def get_screenshots_as_png(self):
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
        sleep(1)
        allure.attach(self.get_screenshots_as_png(), png_name, allure.attachment_type.PNG)

    def select_ComboBox(self, loc: str, index: int=None, value: str=None, text: str=None):
        """
        下拉框选择

        :param loc: select定位xpath
        :param index: 下拉选项option下标
        :param value: 下拉选项option的value
        :param text: 下拉选项option的text
        :return:
        """
        self.select = Select(self.locate(loc))
        if index:
            self.select.select_by_index(index)
        if value:
            self.select.select_by_value(value)
        if text:
            self.select.select_by_visible_text(text)

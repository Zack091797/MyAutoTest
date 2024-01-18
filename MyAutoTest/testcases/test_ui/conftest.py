from typing import Type
from time import sleep

import allure
import pytest
from selenium import webdriver

from Utils.LogConfig.LogConfig import logHelper
from Utils.UI.basepage import BasePage

browser_driver = None
page_dict = {}


@pytest.fixture(scope="session", name="driver")
def initDriver():
    global browser_driver
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'C:\\Users\\Public\\Downloads'}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("detach", True)  # 案例正常运行完成，不调用 quit() 浏览器则不自动关闭
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 去掉受自动化控制抬头
    options.add_experimental_option("useAutomationExtension", False)  # 去掉受自动化控制抬头
    options.add_argument("ignore-certificate-errors")  # 忽略证书错误
    browser_driver = webdriver.Chrome(options=options)
    browser_driver.maximize_window()
    browser_driver.implicitly_wait(10)  # 全局隐式等待
    logHelper.info(f"浏览器初始化完毕...")
    return browser_driver


@pytest.fixture(scope="session")
def init_page(driver):
    """
    fixture工厂模式，初始化page对象
    :param driver:
    :return:
    """
    global page_dict

    def _init_ui_page(PageObj: Type[BasePage], key: str):
        page = PageObj(driver)
        page_dict.update({key: page})
        return page

    return _init_ui_page


@pytest.fixture()
def get_page_dict():
    global page_dict
    return page_dict


@pytest.fixture(scope="session", autouse=False)
def destroy_page(closeBrowser):
    yield
    global page_dict
    if page_dict:
        page_dict.clear()
        logHelper.info("page对象字典已销毁...")


@pytest.fixture(scope="session")
def closeBrowser():
    yield
    global browser_driver
    if browser_driver is not None:
        sleep(5)
        browser_driver.quit()
        browser_driver = None
        logHelper.info("浏览器已关闭...")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "setup" and report.failed:
        if hasattr(browser_driver, "get_screenshot_as_png"):
            allure.attach(browser_driver.get_screenshot_as_png(), "前置操作错误", allure.attachment_type.PNG)
    elif report.when == "call" and report.failed:
        if hasattr(browser_driver, "get_screenshot_as_png"):
            allure.attach(browser_driver.get_screenshot_as_png(), "页面操作错误", allure.attachment_type.PNG)

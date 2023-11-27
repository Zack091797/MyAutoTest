from time import sleep

import allure
import pytest

from selenium import webdriver
from Utils.LogConfig.LogConfig import logHelper

browser_driver = None


@pytest.fixture(scope="session", name="driver")
def initDriver():
    global browser_driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  # 案例正常运行完成，不调用 quit() 浏览器则不自动关闭
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) # 去掉受自动化控制抬头
    options.add_experimental_option("useAutomationExtension", False) # 去掉受自动化控制抬头
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'C:\\Users\\Public\\Downloads'}
    options.add_experimental_option("prefs", prefs)
    browser_driver = webdriver.Chrome(options=options)
    browser_driver.maximize_window()
    browser_driver.implicitly_wait(10)  # 全局隐式等待
    logHelper.info(f"浏览器初始化完毕...")
    return browser_driver


@pytest.fixture(scope="session", autouse=True)
def closeBrowser():
    yield
    global browser_driver
    if browser_driver is not None:
        browser_driver.quit()
        browser_driver = None
        logHelper.info("浏览器已关闭...")
    sleep(5)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "setup" and report.failed:
        if hasattr(browser_driver, "get_screenshot_as_png"):
            allure.attach(browser_driver.get_screen_as_png(), "前置页面操作错误", allure.attachment_type.PNG)
    elif report.when == "call" and report.failed:
        if hasattr(browser_driver, "get_screenshot_as_png"):
            allure.attach(browser_driver.get_screen_as_png(), "页面操作错误", allure.attachment_type.PNG)


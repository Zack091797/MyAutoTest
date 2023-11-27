import importlib
import inspect
import json
import os
from time import sleep

import jinja2
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def render(yml_path, **kwargs):
    path, filename = os.path.split(yml_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or './')).get_template(filename).render(**kwargs)


def all_functions():
    """

    :return:
    """
    debug_module = importlib.import_module("debug")
    all_function = inspect.getmembers(debug_module, inspect.isfunction)
    result = dict(all_function)
    return result


if __name__ == '__main__':
    # r = render("./testdata/tmpdata.yaml", **all_functions())
    # res = yaml.safe_load(r)
    # print(res)
    pass
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.get("https://baidu.com")
    driver.implicitly_wait(0)
    wait = WebDriverWait(driver, 10)
    print(driver.timeouts.implicit_wait)
    hs = driver.find_element("xpath", "//*[@id='s-user-setting-menu']/div/a[2]/span")
    wait.until(EC.visibility_of, ("xpath", "//*[@id='s-user-setting-menu']/div/a[2]/span"))
    # high_search = driver.find_element(("xpath", "//*[@id='s-user-setting-menu']/div/a[2]/span"))
    sleep(20)

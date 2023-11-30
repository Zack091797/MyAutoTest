import importlib
import inspect
import json
import os
from time import sleep

import jinja2
import yaml
from jinja2 import Template
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Utils.Tool.render_template_jinja2 import render_template_by_jinja2
from Utils.Tool.yamlhelper import yamlHelper


def all_functions():
    """
    读取 debug 模块下的所有function

    :return:
    """
    debug_module = importlib.import_module("debug")
    all_function = inspect.getmembers(debug_module, inspect.isfunction)
    result = dict(all_function)
    return result


if __name__ == '__main__':

    fun = all_functions()
    fun.update({"name": "Customer"})

    t_temp = yamlHelper.get_yml_data("./testdata/tmpdata.yaml")
    t = render_template_by_jinja2(t_temp, **fun)
    # t = render_template_by_jinja2(t_temp, fun.get("get_random"))
    # t = render_template_by_jinja2(t_temp, fun.get("get_name_and_age"))
    print(t)


    # 1.yaml定义用例模板，test用例需要有校验必填字段的方法 -- jsonschma定义，入参和出参
    # 2.yaml利用模板调用python方法
    # 3.yaml文件直接作为测试用例

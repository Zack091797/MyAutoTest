import importlib
import inspect
from pathlib import Path

from Utils.Tool.datahelper import dataHelper
from Utils.Tool.render_template_jinja2 import render_template_by_jinja2
from Utils.Tool.yamlhelper import yamlHelper


def all_functions():
    """
    读取 debugtalk 模块下的所有function，return一个内置function对象的dict

    :return:
    """
    debug_module = importlib.import_module("debugtalk")
    all_function = inspect.getmembers(debug_module, inspect.isfunction)
    result = dict(all_function)
    return result

if __name__ == '__main__':
    pass
    debug_talk = all_functions()
    # t_template = [{"name": "正例"}, {"name": "反例"}]
    # t_str = "获取微信小程序token-${name}, 获取随机数-${get_random()}"
    # for index, template in enumerate(t_template):
    #     template.update(debug_talk)
    #     t = render_template_by_jinja2(t_str, **template)
    #     print(t)
    t_str = "${get_random()}"
    t_temp = {"a": 1, "b": 2}
    t_temp.update(debug_talk)
    t = render_template_by_jinja2(t_str, t_temp)
    print(t)





    # prefix = random.choice(['6227', '6222', "6228", '6216'])
    # check_code = random.randint(0, 9)
    # digits = random.randint(10000000000000, 99999999999999)
    # card_number = prefix+str(check_code)+str(digits)
    # if prefix == "6227":
    #     print(f"建设银行:{card_number}")
    # elif prefix == "6228":
    #     print(f"农业银行:{card_number}")
    # elif prefix == "6222":
    #     print(f"工商银行:{card_number}")
    # else:
    #     print(f"中国银行:{card_number}")


    # 1.yaml定义用例模板，test用例需要有校验必填字段的方法 -- jsonschma定义，入参和出参
    # 2.yaml利用模板调用python方法
    # 3.yaml文件直接作为测试用例

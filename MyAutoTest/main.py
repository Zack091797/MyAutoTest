import importlib
import inspect
from pathlib import Path

from Utils.Tool.datahelper import dataHelper
from Utils.Tool.render_template_jinja2 import render_template_by_jinja2
from Utils.Tool.yamlhelper import yamlHelper


if __name__ == '__main__':
    pass
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

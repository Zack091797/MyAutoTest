import base64
import importlib
import inspect
import io
import json
import random
import re
import math
from pathlib import Path
from time import sleep


import pyautogui

from Utils.LogConfig.LogConfig import logHelper
from Utils.Tool.render_template_jinja2 import render_template_by_jinja2
from Utils.Tool.yamlhelper import yamlHelper
from selenium import webdriver
from PIL import Image


def all_functions():
    """
    读取 debugtalk 模块下的所有function，return一个内置function对象的dict

    :return:
    """
    debug_module = importlib.import_module("debugtalk")
    all_function = inspect.getmembers(debug_module, inspect.isfunction)
    result = dict(all_function)
    return result


def image_to_base64_native(image_path):
    with open(image_path, mode='rb') as image_file:
        encoded = base64.b64encode(image_file.read())
    return encoded.decode('utf-8')


def image_to_base64_PIL(imagePath, save_format='png'):
    # with Image.open(imagePath) as image_file:
    #     image_data = io.BytesIO()
    #     image_file.save(image_data, format=save_format)
    #     image_data_bytes = image_data.getvalue()
    #     image_encoded = base64.b64encode(image_data_bytes).decode('utf-8')
    # return image_encoded
    with Image.open(imagePath) as img:
        output_buffer = io.BytesIO()
        img.save(output_buffer, format=save_format)
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data).decode('utf-8')
    return base64_str


def base64_to_image_PIL(base64_str, img_path=None):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = io.BytesIO(byte_data)
    with Image.open(image_data) as img:
        if img_path:
            img.save(img_path)
    return img


def get_check_num(idCard: str):
    a = [int(i) for i in list(idCard)]  # 17位本体
    b = [int(math.pow(2, i - 1) % 11) for i in range(0, 17)]  # 加权因子
    c = [a[i] * b[i] for i in range(0, 17)]
    sum = 0
    for index, i in enumerate(c):
        sum += i
    check_num = sum % 11
    if check_num == 10:
        check_num = "X"
        return f"{idCard+check_num}"
    # elif check_num == 10:
    #     check_num = "0"
    #     return f"{idCard + check_num}"
    else:
        check_num = str(check_num)
        return f"{idCard + check_num}"



if __name__ == '__main__':
    pass
    # image_path = r"C:\Users\EDY\Desktop\外国人永居证反面2.jpg"
    # image_base64 = image_to_base64_PIL(image_path)
    # print(image_base64)

    # new_base64 = "data:image/jpg;base64," + image_base64
    # base64_to_image_PIL(new_base64, r"C:\Users\EDY\Desktop\test_pic_2.png")
    print(get_check_num("94376019980305667"))

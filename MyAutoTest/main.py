import base64
import importlib
import inspect
import io
import json
import re
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
    with Image.open(image_path) as img:
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


if __name__ == '__main__':
    pass
    image_path = r"C:\Users\EDY\Desktop\外国人永居证反面2.jpg"
    image_base64 = image_to_base64_PIL(image_path)
    print(image_base64)

    # new_base64 = "data:image/jpg;base64," + image_base64
    # base64_to_image_PIL(new_base64, r"C:\Users\EDY\Desktop\test_pic_2.png")


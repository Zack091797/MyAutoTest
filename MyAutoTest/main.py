import configparser
import copy
import csv
import importlib
import inspect
import json
import os
import re
from pathlib import Path
from typing import Union
import jinja2
import jsonpath
import yaml


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

    config = configparser.ConfigParser()
    config.read(Path(Path.cwd(), "./config/env_config.ini"))
    dev_url = config.get("url settings", "dev_url")
    dev_port = config.getint("url settings", "dev_port")
    print(type(dev_url), type(dev_port))







import importlib
import inspect
import json
import os
import jinja2




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

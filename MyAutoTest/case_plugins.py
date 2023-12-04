import re
import sys
import types
from inspect import Parameter, Signature
from pathlib import Path
from typing import Iterable, Union, Callable, Mapping, Any, Sequence
import pytest_check as check_assert

import jmespath
import jsonpath
import pytest
import yaml
from _pytest import config
from _pytest.config import Config
from _pytest.python import Module, path_matches_patterns
from pytest_check import check_functions
from requests import Response

from MyException import ExtractExpressError, ParserError
from Utils.LogConfig.LogConfig import logHelper
from Utils.Tool.render_template_jinja2 import render_template_by_jinja2
from dynamic_create_function import create_function_from_parameters

"""
pytest中将 session、package、module、class、instance、function包装成了
<Session>、<Package>、<Module>、<Class>、<Instance>、<Function>各个包，
在<Session>还有一个<Config>包，用于初始化运行环境的各种配置。
这个包各层存在层级关系，由上层包可以构建下层包,
pytest会自动创建 Config Session Package层级的包
"""


#
# def extract_by_object(response: Response, extract_expression: str):
#     """
#        从response 对象属性取值 [status_code, url, ok, headers, cookies, text, json, encoding]
#     :param response: Response Obj
#     :param extract_expression: 取值表达式
#     :return: 返回取值后的结果
#     """
#     if not isinstance(extract_expression, str):
#         return extract_expression
#     res = {
#         "headers": response.headers,
#         "cookies": dict(response.cookies)
#     }
#     if extract_expression in ["status_code", "url", "ok", "encoding"]:
#         return getattr(response, extract_expression)
#     elif extract_expression.startswith('headers') or extract_expression.startswith('cookies'):
#         return extract_by_jmespath(res, extract_expression)
#     elif extract_expression.startswith('body') or extract_expression.startswith('content'):
#         try:
#             response_parse_dict = response.json()
#             return extract_by_jmespath({"body": response_parse_dict}, extract_expression)
#         except Exception as msg:
#             raise ExtractExpressError(f'expression:<{extract_expression}>, error: {msg}')
#     elif extract_expression.startswith('$.'):
#         try:
#             response_parse_dict = response.json()
#             return extract_by_jsonpath(response_parse_dict, extract_expression)
#         except Exception as msg:
#             raise ExtractExpressError(f'expression:<{extract_expression}>, error: {msg}')
#     elif '.+?' in extract_expression or '.*?' in extract_expression:
#         # 正则匹配
#         return extract_by_regex(response.text, extract_expression)
#     else:
#         # 其它非取值表达式，直接返回
#         return extract_expression
#
#
# def extract_by_jsonpath(extract_value: dict, extract_expression: str):  # noqa
#     """
#         json path 取值
#     :param extract_value: response.json()
#     :param extract_expression: eg: '$.code'
#     :return: None或 提取的第一个值 或全部
#     """
#     if not isinstance(extract_expression, str):
#         return extract_expression
#     extract_value = jsonpath.jsonpath(extract_value, extract_expression)
#     if not extract_value:
#         return
#     elif len(extract_value) == 1:
#         return extract_value[0]
#     else:
#         return extract_value
#
#
# def extract_by_jmespath(extract_obj: dict, extract_expression: str):  # noqa
#     """
#         jmes path 取值
#     :param extract_obj: {
#         "body": response.json(),
#         "cookies": dict(response.cookies),
#         "headers": response.headers,
#     }
#     :param extract_expression: eg: 'body.code'
#     :return: 未提取到返回None, 提取到返回结果
#     """  # noqa
#     if not isinstance(extract_expression, str):
#         return extract_expression
#     try:
#         extract_value = jmespath.search(extract_expression, extract_obj)
#         return extract_value
#     except Exception as msg:
#         raise ExtractExpressError(f'expression:<{extract_expression}>, error: {msg}')
#
#
# def extract_by_regex(extract_obj: str, extract_expression: str):
#     """
#        正则表达式提取返回结果
#     :param extract_obj: response.text
#     :param extract_expression:
#     :return:
#     """
#     if not isinstance(extract_expression, str):
#         return extract_expression
#     extract_value = re.findall(extract_expression, extract_obj, flags=re.S)
#     if not extract_value:
#         return ''
#     elif len(extract_value) == 1:
#         return extract_value[0]
#     else:
#         return extract_value
#
#
@pytest.hookimpl
def pytest_collect_file(file_path: Path, parent):
    if file_path.suffix in [".yaml", ".yml"] and path_matches_patterns(file_path, parent.config.getini("python_files")):
        # 动态创建 pytest 的 <Module>包, 其parent为 <Package>
        yaml_Module = Module.from_parent(parent, path=file_path)
        # 动态创建 python 的 module 对象，通常python将 .py文件视为 module，import即可; 此处将 .yml文件创建为一个 module对象
        module = types.ModuleType(file_path.stem)

        raw_data = yaml.safe_load(file_path.open(encoding='utf-8'))
        print("原始数据", raw_data)
        runner = RunYaml(raw_data, module)
        runner.run()

        # 重写 Module 的 _getobj属性, _getobj()方法将返回动态创建的 module 对象
        yaml_Module._getobj = lambda: module
        return yaml_Module
#
#
# class RunYaml:
#     def __init__(self, raw_data: dict, module: types.ModuleType):
#         self.raw_data = raw_data
#         self.module = module
#         self.module_var = {}  # 模块变量
#         self.context = {}
#
#     def run(self):
#         # config 获取用例名称 name 和 base_url
#         case_name = self.raw_data.get('config').get('name', '')
#         base_url = self.raw_data.get('config').get('base_url', None)
#         config_var = self.raw_data.get('config').get('variables', {})
#         # 模块变量渲染
#         self.context.update(__builtins__)  # 加载内置函数
#         # self.context.update(my_builtins.__dict__)  # 自定义函数对象
#         self.module_var = render_template_by_jinja2(config_var, **self.context)
#         teststeps = self.raw_data.get('teststeps', [])
#
#         def execute_yml_case(args):
#             for index, step in enumerate(teststeps):
#                 print(index)
#                 response = None
#                 for item, value in step.items():
#                     if item == "name":
#                         pass
#                     elif item == "request":
#                         request_session = args.get('request_session')
#                         if isinstance(self.module_var, dict):
#                             self.context.update(self.module_var)  # 加载模块变量
#                         request_value = render_template_by_jinja2(value, **self.context)
#                         response = request_session.send_request(
#                             method=str(request_value.pop("method")).upper(),
#                             base_url=base_url,
#                             url=request_value.pop("url"),
#                             **request_value
#                         )
#                     elif item == "extract":
#                         # 提取变量
#                         extract_value = render_template_by_jinja2(value, **self.context)
#                         extract_result = extract_response(response, extract_value)
#                         # 添加到模块变量
#                         self.module_var.update(extract_result)
#                         if isinstance(self.module_var, dict):
#                             self.context.update(self.module_var)  # 加载模块变量
#                     elif item == "validate":
#                         validate_value = render_template_by_jinja2(value, **self.context)
#                         validate_response(response, validate_value)
#                     else:
#                         try:
#                             eval(item)(value)
#                         except Exception as err:
#                             raise ParserError(f"Parsers error: {err}")
#         # 将每个yaml文件实例化为一个module对象，为每个module对象创建一个执行方法
#         f = create_function_from_parameters(
#             func=execute_yml_case,
#             parameters=[
#                 Parameter('request', Parameter.POSITIONAL_OR_KEYWORD),
#                 Parameter('request_session', Parameter.POSITIONAL_OR_KEYWORD)
#             ],
#             documentation=case_name,
#             func_name=str(self.module.__name__),
#             func_filename=f"{self.module.__name__}.py"
#         )
#         setattr(self.module, str(self.module.__name__), f)
#
#         @staticmethod
#         def extract_response(response, extract_obj: dict):
#             """提取返回结果，添加到 module_var ，模块变量"""
#             extract_result = {}
#             if isinstance(extract_obj, dict):
#                 for extract_var, extract_expression in extract_obj.items():
#                     extract_var_value = extract_by_object(response, extract_expression)  # 实际结果
#                     extract_result[extract_var] = extract_var_value
#                 return extract_result
#             else:
#                 return extract_result
#
#         @staticmethod
#         def validate_response(response, validate_check: list) -> None:
#             """校验结果"""
#             for check in validate_check:
#                 for check_type, check_value in check.items():
#                     actual_value = extract_by_object(response, check_value[0])  # 实际结果
#                     expect_value = check_value[1]
#                     if check_type in ["eq", "equals", "equal"]:
#                         check_assert.equal(actual_value, expect_value)
#                     elif check_type in ["lt", "less_than"]:
#                         check_assert.less(actual_value, expect_value)
#                     elif check_type in ["le", "less_or_equal"]:
#                         check_assert.less_equal(actual_value, expect_value)
#                     elif check_type in ["gt", "greater_than"]:
#                         check_assert.greater(actual_value, expect_value)
#                     elif check_type in ["ge", "greater_or_equal"]:
#                         check_assert.greater_equal(actual_value, expect_value)
#                     elif check_type in ["ne", "not_equal"]:
#                         check_assert.not_equal(actual_value, expect_value)
#                     elif check_type in ["str_eq", "string_equals"]:
#                         check_assert.string_equal(actual_value, expect_value)
#                     elif check_type in ["len_eq", "length_equal"]:
#                         check_assert.length_equal(actual_value, expect_value)
#                     elif check_type in ["contains"]:
#                         check_assert.is_in(actual_value, expect_value)
#                     else:
#                         if hasattr(check_assert, check_type):
#                             getattr(check_assert, check_type)(actual_value, expect_value)
#                         else:
#                             print(f"{check_type} not valid check type, please add type!")


@pytest.hookimpl
def pytest_collect_file(file_path: Path, parent):
    if file_path.suffix in [".yaml", ".yml"] and path_matches_patterns(file_path, parent.config.getini("python_files")):
        yaml_Module = YamlFile.from_parent(parent, path=file_path)
        # module = types.ModuleType(file_path.stem)
        # yaml_Module._getobj = lambda: module
        return yaml_Module


class YamlFile(pytest.File):
    def collect(self):
        raw = yaml.safe_load(self.path.open(encoding='utf-8'))
        for name, spec in sorted(raw.items()):
            if name == "teststeps":
                for index, step in enumerate(spec):
                    step_name = step.get("name", f"testcase{index+1}")
                    case_name = step_name if step_name else f"testcase{index+1}"
                    yield YamlItem.from_parent(self, name=case_name, spec=step)


class YamlItem(pytest.Item):
    def __init__(self, *, spec, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec

    def runtest(self):
        for key, value in self.spec.items():
            logHelper.info(f"{key}: {value}")

        pass

    def repr_failure(self, excinfo):
        return super().repr_failure(excinfo)

    def reportinfo(self):
        return self.path, 0, f"usecase: {self.name}"


class YamlException(Exception):
    pass

import re
from typing import Union, Callable

import jsonpath

from Utils.LogConfig.LogConfig import logHelper


class ApiCase:

    @staticmethod
    def create_request_data(base_url: str, callback: callable, callback_param: Union[dict, list]) -> dict:
        """封装请求的各项数据"""
        real_data = callback(callback_param)
        api_name = real_data.get("step", None)
        method = real_data.get("request", None).get("method", None)
        url = base_url + real_data.get("request", None).get("url", None)
        header = real_data.get("request", None).get("header", None)
        param = real_data.get("request", None).get("param", None)
        json = real_data.get("request", None).get("json", None)
        data = real_data.get("request", None).get("data", None)
        file = real_data.get("request", None).get("file", None)
        cookie = real_data.get("request", None).get("cookie", None)
        hook = real_data.get("request", None).get("hook", None)
        auth = real_data.get("request", None).get("auth", None)
        validate = real_data.get("request", None).get("validate", None)
        request_data_print = lambda v: f"{v}\n"
        logHelper.info(f"{'' if api_name is None else f'请求用例名: {request_data_print(api_name)}'}"
                       f"{'' if method is None else f'请求类型: {request_data_print(method)}'}"
                       f"{'' if url is None else f'请求路径: {request_data_print(url)}'}"
                       f"{'' if header is None else f'请求headers: {request_data_print(header)}'}"
                       f"{'' if param is None else f'请求数据param: {request_data_print(param)}'}"
                       f"{'' if json is None else f'请求数据json: {request_data_print(json)}'}"
                       f"{'' if data is None else f'请求数据data: {request_data_print(data)}'}"
                       f"{'' if file is None else f'请求数据file: {request_data_print(file)}'}"
                       f"请求断言: {validate}")
        request_data = {}
        if url:
            request_data.update({"url": url})
        if method:
            request_data.update({"method": method})
        if header:
            request_data.update({"headers": header})
        if param:
            request_data.update({"params": param})
        if json:
            request_data.update({"json": json})
        if data:
            request_data.update({"data": data})
        if file:
            request_data.update({"files": file})
        if cookie:
            request_data.update({"cookies": cookie})
        if hook:
            request_data.update({"hooks": hook})
        if auth:
            request_data.update({"auth": auth})
        return request_data

    @staticmethod
    def extract_resp(expr: str, src: [dict, str], ex_type: str = "jsonpath"):
        """处理提取响应body"""
        value = None
        try:
            match ex_type:
                case "jsonpath":
                    value = jsonpath.jsonpath(src, expr)
                case "regular":
                    value = re.compile(expr).findall(src)
                case _:
                    logHelper.error(f"未定义的提取方式->{ex_type}, 请检查...")
        except IndexError as err:
            logHelper.error(f"提取表达式数组下标越界, 请检查... -> {err}")
        except TypeError as err:
            logHelper.error(f"提取表达式数据类型错误, 请检查... -> {err}")
        except ValueError as err:
            logHelper.error(f"提取表达式数据错误, 请检查... -> {err}")
        finally:
            if value is False:
                value = None
            return value





from typing import Union, Any, Callable

from Utils.LogConfig.LogConfig import logHelper


class ApiCase:
    pass

    @staticmethod
    def create_request_data(base_url: str, csv_data: Callable, yaml_template: Union[dict, list]) -> dict:
        request_data = {}
        real_data = csv_data(yaml_template)
        api_name = real_data.get("step")
        method = real_data.get("request").get("method")
        url = base_url + real_data.get("request").get("url")
        header = real_data.get("request").get("header")
        data = real_data.get("request").get("data")
        validate = real_data.get("request").get("validate")
        logHelper.info(f"请求名称: {api_name}\n"
                       f"请求方法: {method}\n"
                       f"请求路径: {url}\n"
                       f"请求header: {header}\n"
                       f"请求数据： {data}\n"
                       f"请求断言: {validate}")
        return request_data

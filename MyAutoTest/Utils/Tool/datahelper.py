import csv
import re
from pathlib import Path
from typing import Union


class DataHelper:

    def __init__(self):
        pass

    def fromCsv2List(self, csv_path):
        """
        读取csv文件，每行返回一个dict，dict存入list

        :param csv_path:
        :return:
        """
        path = Path(Path.cwd(), csv_path)
        csv_data = []
        with open(path, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, skipinitialspace=True)
            for row in reader:
                csv_data.append(row)
        return csv_data

    def parse_yml(self, yml_data: Union[list, dict], csv_data: dict):
        """
        解析yml模板，替换占位符，返回替换之后的yml数据

        :param yml_data:
        :param csv_data:
        :return:
        """
        if isinstance(yml_data, list):
            for index_, element in enumerate(yml_data):
                if isinstance(element, (str, int)):
                    if re.compile(r"\$\{(.*?)\}").findall(str(element)):
                        yml_data[index_] = self.replace_yml_params(element, csv_data)
                    else:
                        pass
                else:
                    self.parse_yml(element, csv_data)
        elif isinstance(yml_data, dict):
            for key, value in yml_data.items():
                if isinstance(value, (str, int)):
                    if re.compile(r"\$\{(.*?)\}").findall(str(value)):
                        yml_data.update({key: self.replace_yml_params(value, csv_data)})
                    else:
                        pass
                else:
                    self.parse_yml(value, csv_data)
        else:
            pass
        return yml_data

    def replace_yml_params(self, template_value, replace_dict):
        """
        替换yml模板的占位符

        :param template_value:
        :param replace_dict:
        :return:
        """
        temp_value = re.compile(r"\$\{(.*?)\}").findall(template_value)[0]
        replace_value = replace_dict.get(temp_value, None)
        if replace_value is not None:
            return replace_value
        else:
            return "未匹配到该占位符, 请检查!"


dataHelper = DataHelper()
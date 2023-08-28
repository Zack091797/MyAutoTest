import csv
import re
from contextlib import ExitStack
from pathlib import *


class FileHelper:

    def __init__(self):
        pass

    def fromCsv2Json(self, csv_path):
        json_list = []
        with open(Path(Path.cwd(), csv_path), mode="r", encoding="utf-8") as csv_data:
            reader = csv.DictReader(csv_data)
            for row in reader:
                json_list.append(dict(row))
        return json_list

    def EnvReplaceYaml(self, yaml_model_file, yaml_real_file, real_dict):
        try:
            self.create_folder_if_unexist(Path(Path.cwd(), yaml_real_file))
            with ExitStack() as stack:
                yml_model = stack.enter_context(open(Path(Path.cwd(), yaml_model_file), mode="r+", encoding="utf-8"))
                yml_real = stack.enter_context(open(Path(Path.cwd(), yaml_real_file), mode="a+", encoding="utf-8"))
                yml_model_lines = yml_model.readlines()
                for line in yml_model_lines:
                    new_line = line
                    if new_line.find("$csv{") > 0:
                        env_list = new_line.split(":")
                        # env_value = env_list[1].strip().split("{", 1)[1].split("}", 1)[0]
                        env_value = re.findall("\\{(.*?)\\}", env_list[1])[0]
                        if env_value in real_dict.keys():
                            replacement = real_dict.get(env_value)
                            new_line = new_line.replace(env_list[1].strip(), replacement)
                    yml_real.write(new_line)
                yml_real.write("\n\n")
        except IOError as err:
            print(err)
            raise

    def create_folder_if_unexist(self, folder_path):
        try:
            if Path(folder_path).parent.exists():
                pass
            else:
                Path.mkdir(Path(folder_path).parent)
        except IOError as err:
            print(err)

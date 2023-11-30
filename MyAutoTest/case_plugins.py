import types
from pathlib import Path
from typing import Iterable, Union

import pytest
import yaml
from _pytest import config
from _pytest.config import Config
from _pytest.python import Module, path_matches_patterns


# _ptest/python.py 207行 中的pytest_collect_file 定义了原始收集策略
@pytest.hookimpl
def pytest_collect_file(file_path: Path, parent):
    if file_path.suffix in (".yaml", ".yml"):
        if path_matches_patterns(file_path, parent.config.getini("python_files")):
            return YamlFile.from_parent(parent, path=file_path)


class YamlFile(pytest.File):
    def collect(self):
        raw = yaml.safe_load(self.path.open(encoding='utf-8'))
        for name, spec in sorted(raw.items()):
            yield YamlItem.from_parent(self, name=name, spec=spec)


class YamlItem(pytest.Item):
    def __init__(self, *, spec, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec

    def runtest(self):
        for name, value in sorted(self.spec.items()):
            if name != value:
                raise YamlException(self, name, value)

    def repr_failure(self, excinfo):
        if isinstance(excinfo.value, YamlException):
            return "\n".join([
                "usecase execution failed",
                " spec failed: {1!r}: {2!r}".format(*excinfo.value.args),
                "no further details known at this point.",
            ])
        return super().repr_failure(excinfo)

    def reportinfo(self):
        return self.path, 0, f"usecase: {self.name}"


class YamlException(Exception):
    pass


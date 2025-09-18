import importlib
import os
import pathlib

import loguru

dirs = os.path.dirname(__file__)
paths = os.listdir(dirs)
parent_dir = f"src.api.{os.path.split(dirs)[-1]}"
modules = []
modules_py = []
for p in paths:
    abs_path = os.path.join(dirs, p)

    if not p.startswith("__"):
        modules.append(f"{parent_dir}.{os.path.splitext(p)[0]}")
        if os.path.isdir(abs_path):
            # src.api.routers.xxxx
            py_files = pathlib.Path(abs_path).glob("**/*.py")
            for file_abs_path in py_files:
                _, file_name = os.path.split(str(file_abs_path))
                if file_name.startswith("__"):
                    continue
                modules_py.append(f"{parent_dir}.{p}.{os.path.splitext(file_name)[0]}")


def init_modules():
    for x in modules + modules_py:
        loguru.logger.info(f"import {x}")
        importlib.import_module(x)

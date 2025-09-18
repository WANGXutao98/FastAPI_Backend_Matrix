# -*- coding: utf-8 -*-
import os
from collections import defaultdict

import toml
from loguru import logger
from src.config.settings.base import ROOT_DIR

print("import business toml settings")


def load_business_setttings():
    try:
        settings = defaultdict(dict)
        print(".toml file loading...")
        # 自动扫描config目录下的toml文件
        for file in os.listdir(os.path.join(ROOT_DIR, "config")):
            if file.endswith(".toml"):
                try:
                    file_name = os.path.basename(file).split(".")[0]
                    file_path = os.path.join(ROOT_DIR, "config", file)
                    settings[file_name] = toml.loads(open(file_path).read())
                except Exception as e:
                    print(f"{file_name}配置文件加载错误")
                    raise
    except Exception as e:
        logger.exception((str(e)))

    print(f".toml file loaded.{settings}")
    return settings

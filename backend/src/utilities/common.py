import asyncio
import io
import os
import time

import chardet
import pandas as pd
from loguru import logger


def get_encoding_with_bytes(content: bytes) -> str:
    result = chardet.detect(content)
    return result["encoding"]


def __count_text_blank_lines(content: str) -> int:
    lines = content.split("\n")
    non_blank_lines = [line for line in lines if line.strip() != ""]
    return len(non_blank_lines)


def count_non_blank_lines(filename: str, content: bytes) -> int:
    _, file_extension = os.path.splitext(filename)
    if file_extension == ".xls":
        engine = "xlrd"
    elif file_extension == ".xlsx":
        engine = "openpyxl"
    else:
        return __count_text_blank_lines(content.decode(get_encoding_with_bytes(content), errors="ignore"))

    # 读取Excel文件
    df = pd.read_excel(io.BytesIO(content), engine=engine)

    # 去除所有空白行
    df = df.dropna(how="all")

    # 返回非空白行的数量
    return len(df)


def async_timing_decorator(func):
    async def wrapper(*args, **kwargs):
        start_time = asyncio.get_event_loop().time()
        result = await func(*args, **kwargs)
        end_time = asyncio.get_event_loop().time()
        logger.info(
            f"*****[async timing decorator]***** [Func: {func.__name__}] [Time_cost: {end_time - start_time:.2f} seconds]"
        )
        return result

    return wrapper


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds to run.")
        logger.info(
            f"*****[timing_decorator]***** [Func: {func.__name__}] [Cost_time: {end_time - start_time:.2f} seconds]"
        )
        return result

    return wrapper

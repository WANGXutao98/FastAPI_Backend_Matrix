import os
from typing import TYPE_CHECKING, Any, Dict

from asgi_correlation_id.context import correlation_id
from loguru import logger
from src.config import path_conf

if TYPE_CHECKING:
    import loguru


class MyLogger:
    def __init__(self):
        self.log_path = path_conf.LogPath

    def configure_logger(self) -> Any:  # type: ignore
        def correlation_id_filter(record):
            record["correlation_id"] = correlation_id.get()
            return record["correlation_id"]

        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)

        # 日志文件
        log_stdout_file = os.path.join(self.log_path, "access.log")
        log_stderr_file = os.path.join(self.log_path, "error.log")
        log_scheduler_file = os.path.join(self.log_path, "scheduler.log")

        # loguru 日志: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add
        log_config: Dict[str, Any] = dict(rotation="500 MB", retention="15 days", compression="tar.gz", enqueue=True)

        fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <cyan>{correlation_id}</cyan> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

        # stdout
        logger.add(
            log_stdout_file,
            format=fmt,
            level="INFO",
            filter=lambda record: correlation_id_filter(record)
            or (record["level"].name == "INFO" or record["level"].no <= 25),
            **log_config,
            backtrace=False,
            diagnose=False,
        )
        # stderr
        logger.add(
            log_stderr_file,
            format=fmt,
            level="ERROR",
            filter=lambda record: correlation_id_filter(record)
            or (record["level"].name == "ERROR" or record["level"].no >= 30),
            **log_config,
            backtrace=True,
            diagnose=True,
        )

        # stderr
        logger.add(
            log_scheduler_file,
            format=fmt,
            filter=lambda record: "SCHEDULER" in record["message"],
            **log_config,
            backtrace=True,
            diagnose=True,
        )

        return logger


"""
TRACE (5): 用于记录程序执行路径的细节信息，以进行诊断。
DEBUG (10): 开发人员使用该工具记录调试信息。
INFO (20): 用于记录描述程序正常操作的信息消息。
SUCCESS (25): 类似于INFO，用于指示操作成功的情况。
WARNING (30): 警告类型，用于指示可能需要进一步调查的不寻常事件。
ERROR (40): 错误类型，用于记录影响特定操作的错误条件。
CRITICAL (50): 严重类型，用于记录阻止核心功能正常工作的错误条件。

logger.debug('调试消息')
logger.info('普通消息')
logger.warning('警告消息')
logger.error('错误消息')
logger.exception('异常消息')
logger.critical('严重错误消息')
logger.success('成功调用')
"""

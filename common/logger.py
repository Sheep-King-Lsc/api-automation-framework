"""
日志工具类
封装logging，支持控制台输出和文件输出
"""
import logging
import os
from datetime import datetime


class Logger:
    """日志工具类（单例模式）"""

    _instance = None
    _logger = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, log_dir="logs"):
        if self._logger is not None:
            return

        # 创建日志目录
        os.makedirs(log_dir, exist_ok=True)

        # 创建logger
        self._logger = logging.getLogger("api_test")
        self._logger.setLevel(logging.DEBUG)
        self._logger.handlers.clear()

        # 日志格式
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

        # 文件输出
        log_file = os.path.join(log_dir, f"test_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

    def get_logger(self):
        """获取logger实例"""
        return self._logger

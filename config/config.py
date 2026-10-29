"""
配置文件
管理环境配置、基础URL、超时时间等
"""
import os


class Config:
    """配置类"""

    # 项目根目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 测试环境配置
    ENV = "test"  # dev / test / prod

    # 各环境基础URL
    BASE_URLS = {
        "dev": "https://jsonplaceholder.typicode.com",
        "test": "https://jsonplaceholder.typicode.com",
        "prod": "https://jsonplaceholder.typicode.com"
    }

    # 当前环境基础URL（根据ENV自动选择）
    BASE_URL = BASE_URLS.get(ENV, BASE_URLS["test"])

    # 请求超时时间（秒）
    TIMEOUT = 10

    # 测试数据目录
    DATA_DIR = os.path.join(BASE_DIR, "data")

    # 报告目录
    REPORT_DIR = os.path.join(BASE_DIR, "reports")

    # 日志目录
    LOG_DIR = os.path.join(BASE_DIR, "logs")

    # 失败重跑次数
    RERUN_TIMES = 2
    RERUN_DELAY = 1  # 重跑间隔（秒）

    # 性能阈值
    MAX_RESPONSE_TIME = 3  # 秒

    # 测试账号
    TEST_USER = {
        "username": "test_user",
        "password": "test_pass"
    }

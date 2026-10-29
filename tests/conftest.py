"""
pytest配置文件
包含fixture：请求工具实例、测试数据加载等
"""
import pytest
import os
from common.request_util import RequestUtil
from common.assert_util import AssertUtil
from common.logger import Logger
from config.config import Config
from utils.yaml_util import YamlUtil

logger = Logger().get_logger()


@pytest.fixture(scope="session")
def req():
    """
    请求工具fixture（整个测试会话共享一个实例）
    自动设置基础URL
    """
    request_util = RequestUtil()
    request_util.set_base_url(Config.BASE_URL)
    logger.info(f"🚀 测试开始，基础URL: {Config.BASE_URL}")
    yield request_util
    logger.info("🏁 测试结束")


@pytest.fixture(scope="session")
def assert_util():
    """断言工具fixture"""
    return AssertUtil()


@pytest.fixture(scope="function")
def user_test_data():
    """加载用户模块测试数据"""
    data_file = os.path.join(Config.DATA_DIR, "test_user_api.yaml")
    return YamlUtil.read_yaml_test_data(data_file)


@pytest.fixture(scope="function")
def product_test_data():
    """加载商品模块测试数据"""
    data_file = os.path.join(Config.DATA_DIR, "test_product_api.yaml")
    return YamlUtil.read_yaml_test_data(data_file)


def pytest_collection_modifyitems(config, items):
    """
    测试用例收集完成后，修改用例名称（支持中文显示）
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

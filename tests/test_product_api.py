"""
商品模块接口测试用例
数据驱动：从YAML文件读取测试数据
"""
import pytest
import os
from config.config import Config
from utils.yaml_util import YamlUtil

# 加载测试数据
data_file = os.path.join(Config.DATA_DIR, "test_product_api.yaml")
test_cases = YamlUtil.read_yaml_test_data(data_file)


class TestProductApi:
    """商品模块接口测试"""

    @pytest.mark.parametrize("case_name, request_data, expected", test_cases,
                             ids=[case[0] for case in test_cases])
    def test_product_api(self, req, assert_util, case_name, request_data, expected):
        """
        数据驱动的商品接口测试
        """
        # 1. 发送请求
        method = request_data.get("method", "GET")
        url = request_data.get("url", "/")
        params = request_data.get("params")
        json_data = request_data.get("json")

        response = req.request(method, url, params=params, json=json_data)

        # 2. 执行断言
        if "status_code" in expected:
            assert_util.assert_status_code(response, expected["status_code"])

        if "response_time" in expected:
            assert_util.assert_response_time(response, expected["response_time"])

        if "json_contains" in expected:
            assert_util.assert_json_contains(response, expected["json_contains"])

        if expected.get("list_not_empty"):
            assert_util.assert_json_list_not_empty(response)

        if "list_length" in expected:
            assert_util.assert_json_list_length(response, None, expected["list_length"])

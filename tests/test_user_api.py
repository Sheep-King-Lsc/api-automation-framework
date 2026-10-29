"""
用户模块接口测试用例
数据驱动：从YAML文件读取测试数据
"""
import pytest
import os
from config.config import Config
from utils.yaml_util import YamlUtil

# 加载测试数据
data_file = os.path.join(Config.DATA_DIR, "test_user_api.yaml")
test_cases = YamlUtil.read_yaml_test_data(data_file)


class TestUserApi:
    """用户模块接口测试"""

    @pytest.mark.parametrize("case_name, request_data, expected", test_cases,
                             ids=[case[0] for case in test_cases])
    def test_user_api(self, req, assert_util, case_name, request_data, expected):
        """
        数据驱动的用户接口测试
        每个用例从YAML读取请求和预期结果
        """
        # 1. 发送请求
        method = request_data.get("method", "GET")
        url = request_data.get("url", "/")
        params = request_data.get("params")
        json_data = request_data.get("json")
        data = request_data.get("data")

        response = req.request(method, url, params=params, json=json_data, data=data)

        # 2. 执行断言
        # 状态码断言
        if "status_code" in expected:
            assert_util.assert_status_code(response, expected["status_code"])

        # 响应时间断言
        if "response_time" in expected:
            assert_util.assert_response_time(response, expected["response_time"])

        # JSON包含断言
        if "json_contains" in expected:
            assert_util.assert_json_contains(response, expected["json_contains"])

        # 列表非空断言
        if expected.get("list_not_empty"):
            assert_util.assert_json_list_not_empty(response)

        # 列表长度断言
        if "list_length" in expected:
            assert_util.assert_json_list_length(response, None, expected["list_length"])

        # 响应头断言
        if "header_exists" in expected:
            assert_util.assert_header_exists(response, expected["header_exists"])

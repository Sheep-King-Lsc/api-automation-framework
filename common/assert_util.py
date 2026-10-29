"""
断言工具类
封装常用断言方法，支持状态码、响应体、响应时间等多种断言
"""
import json
import logging
from common.logger import Logger

logger = Logger().get_logger()


class AssertUtil:
    """断言工具类"""

    @staticmethod
    def assert_status_code(response, expected_code):
        """
        断言响应状态码
        :param response: Response对象
        :param expected_code: 预期状态码（int或list）
        """
        actual = response.status_code
        if isinstance(expected_code, list):
            assert actual in expected_code, \
                f"状态码断言失败: 预期{expected_code}, 实际{actual}"
        else:
            assert actual == expected_code, \
                f"状态码断言失败: 预期{expected_code}, 实际{actual}"
        logger.info(f"✅ 状态码断言通过: {actual} == {expected_code}")

    @staticmethod
    def assert_json_key(response, key):
        """
        断言响应JSON包含指定key
        """
        resp_json = response.json()
        assert key in resp_json, f"响应中不包含key: {key}"
        logger.info(f"✅ Key存在断言通过: {key}")

    @staticmethod
    def assert_json_value(response, key, expected_value):
        """
        断言响应JSON中指定key的值
        支持嵌套key: "data.user.name"
        """
        resp_json = response.json()
        keys = key.split(".")
        actual = resp_json
        for k in keys:
            assert k in actual, f"响应中不包含key: {k}"
            actual = actual[k]

        assert actual == expected_value, \
            f"值断言失败: key={key}, 预期={expected_value}, 实际={actual}"
        logger.info(f"✅ 值断言通过: {key} = {expected_value}")

    @staticmethod
    def assert_json_contains(response, expected_dict):
        """
        断言响应JSON包含预期的键值对（部分匹配）
        :param expected_dict: 预期的键值对字典
        """
        resp_json = response.json()
        for key, value in expected_dict.items():
            assert key in resp_json, f"响应中不包含key: {key}"
            assert resp_json[key] == value, \
                f"值断言失败: key={key}, 预期={value}, 实际={resp_json[key]}"
        logger.info(f"✅ 包含断言通过: {expected_dict}")

    @staticmethod
    def assert_response_time(response, max_seconds):
        """
        断言响应时间不超过最大值
        """
        elapsed = response.elapsed.total_seconds()
        assert elapsed <= max_seconds, \
            f"响应时间断言失败: 预期<={max_seconds}s, 实际={elapsed:.3f}s"
        logger.info(f"✅ 响应时间断言通过: {elapsed:.3f}s <= {max_seconds}s")

    @staticmethod
    def assert_json_list_length(response, key, expected_length):
        """
        断言响应中列表长度
        """
        resp_json = response.json()
        if isinstance(resp_json, list):
            actual_length = len(resp_json)
        else:
            assert key in resp_json, f"响应中不包含key: {key}"
            actual_length = len(resp_json[key])

        assert actual_length == expected_length, \
            f"列表长度断言失败: 预期={expected_length}, 实际={actual_length}"
        logger.info(f"✅ 列表长度断言通过: {actual_length}")

    @staticmethod
    def assert_json_list_not_empty(response, key=None):
        """
        断言响应列表不为空
        """
        resp_json = response.json()
        if key:
            assert key in resp_json, f"响应中不包含key: {key}"
            data = resp_json[key]
        else:
            data = resp_json

        assert isinstance(data, list) and len(data) > 0, "列表为空"
        logger.info(f"✅ 列表非空断言通过: 长度={len(data)}")

    @staticmethod
    def assert_text_contains(response, expected_text):
        """
        断言响应文本包含指定内容
        """
        assert expected_text in response.text, \
            f"文本包含断言失败: 响应中不包含'{expected_text}'"
        logger.info(f"✅ 文本包含断言通过: '{expected_text}'")

    @staticmethod
    def assert_header_exists(response, header_name):
        """
        断言响应头包含指定字段
        """
        assert header_name in response.headers, \
            f"响应头中不包含: {header_name}"
        logger.info(f"✅ 响应头断言通过: {header_name}")

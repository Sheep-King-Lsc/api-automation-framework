"""
YAML文件读取工具
"""
import yaml
import os


class YamlUtil:
    """YAML工具类"""

    @staticmethod
    def read_yaml(file_path):
        """
        读取YAML文件
        :param file_path: YAML文件路径
        :return: 解析后的数据（dict/list）
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"YAML文件不存在: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data

    @staticmethod
    def read_yaml_test_data(file_path):
        """
        读取测试数据YAML，返回pytest参数化数据格式
        YAML格式要求：
        test_cases:
          - name: 用例名称
            request: {...}
            expected: {...}
        """
        data = YamlUtil.read_yaml(file_path)
        test_cases = data.get("test_cases", [])

        # 转换为pytest参数化格式：(用例名称, 请求数据, 预期结果)
        result = []
        for case in test_cases:
            result.append((
                case.get("name", "未命名用例"),
                case.get("request", {}),
                case.get("expected", {})
            ))
        return result

    @staticmethod
    def write_yaml(file_path, data):
        """写入YAML文件"""
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

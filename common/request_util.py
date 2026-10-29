"""
HTTP请求工具类
对requests进行二次封装，统一处理请求、响应、日志、异常
"""
import requests
import json
import logging
from common.logger import Logger

logger = Logger().get_logger()


class RequestUtil:
    """请求工具类"""

    def __init__(self):
        self.session = requests.Session()
        self.base_url = ""
        self.headers = {}
        self.timeout = 10

    def set_base_url(self, url):
        """设置基础URL"""
        self.base_url = url

    def set_headers(self, headers):
        """设置请求头"""
        self.headers.update(headers)

    def set_token(self, token):
        """设置Token（自动加到Header）"""
        self.headers["Authorization"] = f"Bearer {token}"

    def _build_url(self, url):
        """构建完整URL"""
        if url.startswith("http"):
            return url
        return self.base_url.rstrip("/") + "/" + url.lstrip("/")

    def _log_request(self, method, url, **kwargs):
        """记录请求日志"""
        logger.info(f"📤 请求: {method.upper()} {url}")
        if kwargs.get("params"):
            logger.info(f"   参数: {kwargs['params']}")
        if kwargs.get("json"):
            logger.info(f"   请求体: {json.dumps(kwargs['json'], ensure_ascii=False)}")
        if kwargs.get("data"):
            logger.info(f"   表单数据: {kwargs['data']}")

    def _log_response(self, response):
        """记录响应日志"""
        logger.info(f"📥 响应: 状态码={response.status_code}, 耗时={response.elapsed.total_seconds():.3f}s")
        try:
            resp_json = response.json()
            logger.info(f"   响应体: {json.dumps(resp_json, ensure_ascii=False)[:500]}")
        except:
            logger.info(f"   响应体: {response.text[:500]}")

    def request(self, method, url, **kwargs):
        """
        统一请求方法
        :param method: GET/POST/PUT/DELETE/PATCH
        :param url: 接口地址
        :param kwargs: 其他参数（params/json/data/headers等）
        :return: Response对象
        """
        full_url = self._build_url(url)
        kwargs.setdefault("headers", self.headers)
        kwargs.setdefault("timeout", self.timeout)

        self._log_request(method, full_url, **kwargs)

        try:
            response = self.session.request(method.upper(), full_url, **kwargs)
            self._log_response(response)
            return response
        except requests.exceptions.Timeout:
            logger.error(f"❌ 请求超时: {full_url}")
            raise
        except requests.exceptions.ConnectionError:
            logger.error(f"❌ 连接失败: {full_url}")
            raise
        except Exception as e:
            logger.error(f"❌ 请求异常: {full_url}, 错误: {str(e)}")
            raise

    def get(self, url, params=None, **kwargs):
        """GET请求"""
        return self.request("GET", url, params=params, **kwargs)

    def post(self, url, json=None, data=None, **kwargs):
        """POST请求"""
        return self.request("POST", url, json=json, data=data, **kwargs)

    def put(self, url, json=None, **kwargs):
        """PUT请求"""
        return self.request("PUT", url, json=json, **kwargs)

    def patch(self, url, json=None, **kwargs):
        """PATCH请求"""
        return self.request("PATCH", url, json=json, **kwargs)

    def delete(self, url, **kwargs):
        """DELETE请求"""
        return self.request("DELETE", url, **kwargs)

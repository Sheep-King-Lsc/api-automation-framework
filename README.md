# 接口自动化测试框架

## 项目简介

基于 Python + requests + pytest 搭建的**接口自动化测试框架**，采用数据驱动设计模式，支持 YAML 测试数据、自动断言、日志记录、Allure 报告、失败重跑等功能，用于 RESTful API 的接口自动化回归测试。

> 测试对象：https://jsonplaceholder.typicode.com（公开 REST API），可直接运行验证。

## 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.8+ | 开发语言 |
| requests | HTTP 请求库 |
| pytest | 测试框架 |
| PyYAML | 测试数据管理 |
| Allure | 测试报告 |
| logging | 日志记录 |
| pytest-rerunfailures | 失败重跑 |

## 框架特点

1. **数据驱动**：测试数据与代码分离，YAML 文件管理，新增用例只需改数据
2. **统一请求封装**：requests 二次封装，支持 GET/POST/PUT/PATCH/DELETE，预留 Header/Token 扩展接口（当前公开 API 无需鉴权）
3. **智能断言**：支持状态码、响应体字段、响应时间、Content-Type 多种断言方式
4. **日志系统**：每个请求和响应自动记录日志，便于排查问题
5. **Allure 报告**：可视化测试报告，支持用例分级、步骤展示
6. **失败重跑**：网络波动导致的失败自动重跑，提高稳定性
7. **配置管理**：多环境配置（dev/test/prod），一套代码多环境运行

## 项目结构

```
project2-api-automation/
├── README.md
├── run.py                    # 运行入口
├── requirements.txt
├── pytest.ini
├── common/
│   ├── __init__.py
│   ├── request_util.py       # 请求封装
│   ├── assert_util.py        # 断言封装
│   └── logger.py             # 日志封装
├── config/
│   ├── __init__.py
│   ├── config.py             # 配置类
│   └── settings.yaml         # 环境配置
├── data/
│   ├── __init__.py
│   ├── test_user_api.yaml    # 用户接口测试数据（17条用例）
│   └── test_product_api.yaml # 商品接口测试数据（16条用例）
├── utils/
│   ├── __init__.py
│   └── yaml_util.py          # YAML 读取工具
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # pytest fixture
│   ├── test_user_api.py      # 用户接口测试
│   └── test_product_api.py   # 商品接口测试
├── logs/                     # 运行日志
└── reports/                  # 测试报告输出目录（Allure 结果）
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行测试

```bash
# 运行所有测试
python run.py

# 或使用 pytest
pytest tests/ -v --alluredir=reports/allure-results

# 生成 Allure 报告
allure serve reports/allure-results
```

### 3. 运行指定用例

```bash
pytest tests/test_user_api.py -v
pytest tests/ -k "get_user" -v
```

## 测试成果

- 搭建接口自动化框架，覆盖用户、商品 **2 个模块 33条**接口测试用例（用户17条 + 商品16条）
- 数据驱动设计：新增用例零代码改动，只需在 YAML 中追加配置
- 覆盖正常 / 异常 / 边界 / 参数校验 / 响应时间等场景，支持状态码、响应字段、响应时间多维断言
- 已接入 Allure 报告与失败重跑机制，历史运行结果见 `reports/` 目录

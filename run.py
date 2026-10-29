"""
测试运行入口
支持命令行参数指定环境、用例、报告等
"""
import pytest
import sys
import os

# 将项目根目录加入path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config import Config


def run_tests():
    """运行测试"""
    # 报告目录
    report_dir = os.path.join(Config.REPORT_DIR, "allure-results")
    html_report = os.path.join(Config.REPORT_DIR, "report.html")
    os.makedirs(Config.REPORT_DIR, exist_ok=True)

    # pytest参数
    args = [
        "tests/",
        "-v",
        "--tb=short",
        f"--html={html_report}",
        "--self-contained-html",
        f"--alluredir={report_dir}",
        f"--reruns={Config.RERUN_TIMES}",
        f"--reruns-delay={Config.RERUN_DELAY}",
    ]

    # 运行pytest
    exit_code = pytest.main(args)
    return exit_code


if __name__ == "__main__":
    code = run_tests()
    print(f"\n{'='*50}")
    print(f"测试执行完成，退出码: {code}")
    print(f"HTML报告: {os.path.join(Config.REPORT_DIR, 'report.html')}")
    print(f"Allure结果: {os.path.join(Config.REPORT_DIR, 'allure-results')}")
    print(f"查看Allure报告: allure serve {os.path.join(Config.REPORT_DIR, 'allure-results')}")
    print(f"{'='*50}")
    sys.exit(code)

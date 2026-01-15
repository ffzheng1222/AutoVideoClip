#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
灵活的测试运行器
允许自由选择和调整要运行的具体测试模块
"""

import os
import sys
from utils import clear_outputs_directory

# 添加当前目录和tests目录到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
tests_dir = os.path.join(current_dir, 'tests')
sys.path.append(current_dir)
sys.path.append(tests_dir)

# 从tests目录导入测试运行器
from tests.test_runner import main as run_tests

def main():
    """简化的主函数"""
    # 定义outputs目录路径
    outputs_path = os.path.join(current_dir, 'outputs')

    # 清空outputs目录
    clear_outputs_directory(outputs_path)

    # 运行测试
    run_tests()


if __name__ == "__main__":
    main()
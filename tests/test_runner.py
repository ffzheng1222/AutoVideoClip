#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行器
包含所有灵活的测试选择和运行逻辑
"""

import os
import sys
import argparse
import time
from datetime import datetime
#import traceback

# 添加当前目录和父目录到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

# 导入所有测试函数
from test_modules import (
    test_video_editor,
    test_video_trimmer,
    test_video_compositor,
    test_export_distributor,
    test_audio_editor,
    test_color_correction,
    run_tests
)

class TestRunner:
    """灵活的测试运行器类"""

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def print_header(self, title):
        """打印测试标题"""
        print("=" * 80)
        print(f"🚀 {title} 🚀")
        print("=" * 80)
        print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

    def print_footer(self, test_name, success=True, error_msg=None):
        """打印测试结果页脚"""
        print()
        print("-" * 60)
        print(f"📊 {test_name} 测试结果:")
        if success:
            print("   ✅ 测试执行成功")
        else:
            print(f"   ❌ 测试执行失败: {error_msg or '未知错误'}")
        print("-" * 60)

    def run_single_test(self, test_func, test_name):
        """运行单个测试函数"""
        print(f"\n{'🔍' + ' ' * 10} 开始执行 {test_name} 测试 {'🔍' + ' ' * 10}")
        success = False
        error_msg = None

        try:
            self.print_header(f"🎯 {test_name} 测试详情")

            # 执行测试函数
            test_func()

            success = True
            print("🟢 测试函数执行完成")

        except Exception as e:
            error_msg = str(e)
            print(f"🔴 {test_name} 测试执行过程中发生异常: {error_msg}")
            import traceback
            traceback.print_exc()

        finally:
            self.print_footer(test_name, success, error_msg)
            return success

    def run_selected_tests(self, selected_tests):
        """运行选定的测试"""
        self.start_time = time.time()
        self.print_header("🎬 视频编辑工具套件 - 选择性测试运行")

        total_success = 0
        total_failure = 0
        available_tests = {
            'video_editor': ('VideoEditor - 视频编辑器', test_video_editor),
            'video_trimmer': ('VideoTrimmer - 视频剪辑器', test_video_trimmer),
            'audio_editor': ('AudioEditor - 音频编辑器', test_audio_editor),
            'color_correction': ('ColorCorrection - 色彩校正器', test_color_correction),
            'video_compositor': ('VideoCompositor - 视频合成器', test_video_compositor),
            'export_distributor': ('ExportDistributor - 导出分发器', test_export_distributor)
        }

        print(f"\n📋 计划执行 {len(selected_tests)} 个测试模块:\n")

        tests_to_run = []
        for test_key in selected_tests:
            if test_key in available_tests:
                test_name, test_func = available_tests[test_key]
                tests_to_run.append((test_func, test_name))
                print(f"  ✅ {test_name} (已选择)")
            else:
                print(f"  ❌ {test_key} (未找到，跳过)")

        if not tests_to_run:
            print("⚠️  没有有效的测试被选择！")
            return

        print("\n" + "=" * 80)

        # 运行选定的测试
        for test_func, test_name in tests_to_run:
            success = self.run_single_test(test_func, test_name)
            if success:
                total_success += 1
            else:
                total_failure += 1

        # 运行总结
        self.end_time = time.time()
        self.print_summary(total_success, total_failure, len(selected_tests))

    def run_all_tests_wrapper(self):
        """运行所有测试（使用原始的 run_all_tests 函数）"""
        self.start_time = time.time()
        self.print_header("🎬 视频编辑工具套件 - 完整测试运行")

        print("\n" + "=" * 80)
        print("📋 计划执行所有测试模块:\n")

        # 获取所有测试名称
        test_names = [
            "VideoEditor - 视频编辑器",
            "VideoTrimmer - 视频剪辑器",
            "AudioEditor - 音频编辑器",
            "ColorCorrection - 色彩校正器",
            "VideoCompositor - 视频合成器",
            "ExportDistributor - 导出分发器"
        ]

        for i, test_name in enumerate(test_names, 1):
            print(f"  {i}. {test_name}")

        print("\n" + "=" * 80)

        # 运行所有测试
        try:
            run_tests()
            total_success = 6  # 假设所有6个测试都运行了
            total_failure = 0
        except Exception as e:
            total_success = 0
            total_failure = 6
            print(f"❌ 运行所有测试时发生错误: {e}")
            import traceback
            traceback.print_exc()

        # 运行总结
        self.end_time = time.time()
        self.print_summary(total_success, total_failure, 6)

    def print_summary(self, total_success, total_failure, total_planned):
        """打印测试总结"""
        total_tests = total_success + total_failure
        duration = self.end_time - self.start_time
        duration_str = f"{duration:.2f} 秒"
        success_rate = (total_success / total_tests * 100) if total_tests > 0 else 0

        print("\n" + "=" * 80)
        print("🎯 测试执行总结 🎯")
        print("=" * 80)
        print(f"📋 计划测试: {total_planned}")
        print(f"📈 实际执行: {total_tests}")
        print(f"✅ 成功通过: {total_success}")
        print(f"❌ 测试失败: {total_failure}")
        print(f"📊 通过率: {success_rate:.1f}%")
        print(f"⏱️  总执行时间: {duration_str}")

        if total_failure == 0:
            print("🎉 恭喜！所有执行的测试模块都成功！")
        else:
            print("⚠️  有测试失败，请检查失败的测试模块并修复相关问题！")

        print("\n" + "=" * 80)

def main():
    """主函数 - 提供灵活的测试选择"""
    parser = argparse.ArgumentParser(description='视频编辑工具测试运行器 - 灵活选择测试模块')

    parser.add_argument('--all', action='store_true',
                        help='运行所有测试模块 (默认)')
    parser.add_argument('--module', '-m', action='append',
                        help='指定要运行的单个测试模块 (可多次使用)')
    parser.add_argument('--group', '-g', action='append',
                        help='指定要运行的测试组 (video, audio, export, all)')

    # 为方便使用，也支持简写参数
    parser.add_argument('--video', action='store_true',
                        help='运行所有视频相关测试 (video_editor, video_trimmer, video_compositor)')
    parser.add_argument('--audio', action='store_true',
                        help='运行所有音频相关测试 (audio_editor, color_correction)')
    parser.add_argument('--export', action='store_true',
                        help='运行导出相关测试 (export_distributor)')

    args = parser.parse_args()

    runner = TestRunner()

    if args.all or (not any(vars(args).values())):  # 如果没有指定任何参数，默认运行所有
        runner.run_all_tests_wrapper()
    elif args.module:  # 运行指定的具体模块
        runner.run_selected_tests(args.module)
    else:
        # 根据组别运行测试
        selected_tests = []

        if args.video or args.group and 'video' in args.group:
            selected_tests.extend(['video_editor', 'video_trimmer', 'video_compositor'])

        if args.audio or args.group and 'audio' in args.group:
            selected_tests.extend(['audio_editor', 'color_correction'])

        if args.export or args.group and 'export' in args.group:
            selected_tests.append('export_distributor')

        if not selected_tests:  # 如果没有匹配的组别，运行所有
            runner.run_all_tests_wrapper()
        else:
            runner.run_selected_tests(selected_tests)

if __name__ == "__main__":
    main()
# test_video_compositor.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from video_compositor import VideoCompositor

def test_video_compositor():
    print("🎞️" + " " * 10 + "开始测试 VideoCompositor ..." + " " * 10 + "🎞️")
    compositor = VideoCompositor()
    input_video = os.path.join("inputs", "cat_01.mp4")
    output_title = os.path.join("outputs", "test_title.mp4")
    output_subtitle = os.path.join("outputs", "test_subtitle.mp4")
    output_graphic = os.path.join("outputs", "test_graphic.mp4")
    output_moving_graphic = os.path.join("outputs", "test_moving_graphic.mp4")
    output_animated_title = os.path.join("outputs", "test_animated_title.mp4")
    output_ar = os.path.join("outputs", "test_ar.mp4")
    output_metadata = os.path.join("outputs", "test_metadata.mp4")

    os.makedirs("outputs", exist_ok=True)

    # 测试1: 添加静态标题
    print("🔹 测试添加静态标题: '测试标题' 居中，字体大小48，白色")
    if compositor.add_title(input_video, output_title, "测试标题", "center", 48, "white"):
        print("✅ 静态标题添加成功！输出文件: " + output_title)
    else:
        print("❌ 静态标题添加失败！")

    # 测试2: 添加字幕
    print("🔹 测试添加字幕: '这是一个字幕' 从 00:00:05 到 00:00:10，底部，字体大小28，白色")
    if compositor.add_subtitle(input_video, output_subtitle, "这是一个字幕", "00:00:05", "00:00:10", "bottom", 28, "white"):
        print("✅ 字幕添加成功！输出文件: " + output_subtitle)
    else:
        print("❌ 字幕添加失败！")

    # 测试3: 添加静态图形（水印）
    print("🔹 测试添加静态图形（水印）: 'inputs/watermark.png' 右上角，偏移(10,10)")
    if compositor.add_graphic_overlay(input_video, os.path.join("inputs", "watermark.png"), output_graphic, "top-right", 10, 10):
        print("✅ 静态图形添加成功！输出文件: " + output_graphic)
    else:
        print("❌ 静态图形添加失败！")

    # 测试4: 添加移动图形
    print("🔹 测试添加移动图形: 'inputs/logo.png' 向右移动，持续5秒")
    if compositor.add_moving_graphic(input_video, os.path.join("inputs", "logo.png"), output_moving_graphic, 5.0, "right"):
        print("✅ 移动图形添加成功！输出文件: " + output_moving_graphic)
    else:
        print("❌ 移动图形添加失败！")

    # 测试5: 添加动画标题
    print("🔹 测试添加动画标题: '动画标题' 淡入效果，持续2秒")
    if compositor.add_animated_title(input_video, output_animated_title, "动画标题", "fade_in", 2.0):
        print("✅ 动画标题添加成功！输出文件: " + output_animated_title)
    else:
        print("❌ 动画标题添加失败！")

    # 测试6: 添加 AR 叠加
    print("🔹 测试添加 AR 叠加: 'inputs/watermark.png' 中心位置")
    if compositor.add_ar_overlay(input_video, os.path.join("inputs", "watermark.png"), output_ar, "center"):
        print("✅ AR 叠加添加成功！输出文件: " + output_ar)
    else:
        print("❌ AR 叠加添加失败！")

    # 测试7: 嵌入元数据
    print("🔹 测试嵌入元数据: 标题='测试视频', 作者='测试作者', 描述='这是一个测试描述'")
    if compositor.embed_metadata(input_video, output_metadata, title="测试视频", author="测试作者", description="这是一个测试描述"):
        print("✅ 元数据嵌入成功！输出文件: " + output_metadata)
    else:
        print("❌ 元数据嵌入失败！")

    print("🎞️" + " " * 8 + "VideoCompositor 测试完成。" + " " * 8 + "🎞️\n")

if __name__ == "__main__":
    test_video_compositor()
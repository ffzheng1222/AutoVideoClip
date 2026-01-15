# test_video_trimmer.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from video_trimmer import VideoTrimmer

def test_video_trimmer():
    print("✂️" + " " * 10 + "开始测试 VideoTrimmer ..." + " " * 10 + "✂️")
    trimmer = VideoTrimmer()
    input_video = os.path.join("inputs", "cat_01.mp4")
    output_segments = os.path.join("outputs", "test_segments.mp4")
    output_fade = os.path.join("outputs", "test_fade.mp4")
    output_zoom = os.path.join("outputs", "test_zoom.mp4")
    output_blur = os.path.join("outputs", "test_blur.mp4")
    output_vintage = os.path.join("outputs", "test_vintage.mp4")

    os.makedirs("outputs", exist_ok=True)

    # 测试1: 多段剪辑
    #print("🔹 测试多段剪辑: [(00:00:05, 00:00:10), (00:00:15, 00:00:20)]")
    #segments = [("00:00:05", "00:00:10"), ("00:00:15", "00:00:20")]
    print("🔹 测试多段剪辑: [(5, 10), (15, 20)]")
    segments = [("5", "10"), ("15", "20")]
    if trimmer.trim_by_segments(input_video, output_segments, segments):
        print("✅ 多段剪辑成功！输出文件: " + output_segments)
    else:
        print("❌ 多段剪辑失败！")

    # 测试2: 淡入淡出转场
    print("🔹 测试淡入淡出转场")
    if trimmer.apply_fade_transition(input_video, output_fade, "10.0"):
        print("✅ 淡入淡出转场成功！输出文件: " + output_fade)
    else:
        print("❌ 淡入淡出转场失败！")

    # 测试3: 缩放效果
    print("🔹 测试缩放效果 (1.2倍)")
    if trimmer.apply_zoom_effect(input_video, output_zoom, 1.2):
        print("✅ 缩放效果成功！输出文件: " + output_zoom)
    else:
        print("❌ 缩放效果失败！")

    # 测试4: 模糊效果
    print("🔹 测试模糊效果 (强度5)")
    if trimmer.apply_blur_effect(input_video, output_blur, 5):
        print("✅ 模糊效果成功！输出文件: " + output_blur)
    else:
        print("❌ 模糊效果失败！")

    # 测试5: 复古色调
    print("🔹 测试复古色调")
    if trimmer.apply_vintage_effect(input_video, output_vintage):
        print("✅ 复古色调成功！输出文件: " + output_vintage)
    else:
        print("❌ 复古色调失败！")

    print("✂️" + " " * 8 + "VideoTrimmer 测试完成。" + " " * 8 + "✂️\n")

if __name__ == "__main__":
    test_video_trimmer()
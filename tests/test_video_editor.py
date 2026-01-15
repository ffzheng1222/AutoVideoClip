# test_video_editor.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from video_editor import VideoEditor

def test_video_editor():
    print("🎬" + " " * 10 + "开始测试 VideoEditor ..." + " " * 10 + "🎬")
    editor = VideoEditor()
    input_video = os.path.join("inputs", "cat_01.mp4")
    output_cut = os.path.join("outputs", "test_cut.mp4")
    output_extract_audio = os.path.join("outputs", "test_extract_audio.mp3")
    output_speed = os.path.join("outputs", "test_speed.mp4")
    output_watermark = os.path.join("outputs", "test_watermark.mp4")

    # 确保输出目录存在
    os.makedirs("outputs", exist_ok=True)

    # 测试1: 视频剪辑
    print("🔹 测试视频剪辑: 从 00:00:05 到 00:00:10")
    if editor.cut_video(input_video, output_cut, "00:00:05", "00:00:10"):
        print("✅ 视频剪辑成功！输出文件: " + output_cut)
    else:
        print("❌ 视频剪辑失败！")

    # 测试2: 提取音频
    print("🔹 测试提取音频")
    if editor.extract_audio(input_video, output_extract_audio):
        print("✅ 音频提取成功！输出文件: " + output_extract_audio)
    else:
        print("❌ 音频提取失败！")

    # 测试3: 加速视频
    print("🔹 测试视频加速 (2倍速)")
    if editor.speed_up_video(input_video, output_speed, 2.0):
        print("✅ 视频加速成功！输出文件: " + output_speed)
    else:
        print("❌ 视频加速失败！")

    # 测试4: 添加水印
    print("🔹 测试添加水印")
    if editor.add_watermark(input_video, os.path.join("inputs", "watermark.png"), output_watermark, "top-right"):
        print("✅ 水印添加成功！输出文件: " + output_watermark)
    else:
        print("❌ 水印添加失败！")

    print("🎬" + " " * 8 + "VideoEditor 测试完成。" + " " * 8 + "🎬\n")

if __name__ == "__main__":
    test_video_editor()
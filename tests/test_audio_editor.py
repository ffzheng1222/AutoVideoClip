# test_audio_editor.py
import os
import sys

# 添加当前目录到系统路径，以便导入 audio_editor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from audio_editor import AudioEditor

def test_audio_editor():
    print("🎵" + " " * 10 + "开始测试 AudioEditor ..." + " " * 10 + "🎵")
    editor = AudioEditor()
    bgm_path = os.path.join("inputs", "bgm.mp3")
    video_path = os.path.join("inputs", "cat_01.mp4")
    output_adjust_volume = os.path.join("outputs", "test_adjust_volume.mp3")
    output_add_bgm = os.path.join("outputs", "test_add_bgm.mp4")
    output_apply_fade = os.path.join("outputs", "test_apply_fade.mp3")
    output_trim_audio = os.path.join("outputs", "test_trim_audio.mp3")
    output_extract_audio = os.path.join("outputs", "test_extract_audio.mp3")
    output_sync_audio = os.path.join("outputs", "test_sync_audio.mp4")
    output_mix_multiple = os.path.join("outputs", "test_mix_multiple.mp3")
    output_equalizer = os.path.join("outputs", "test_equalizer.mp3")
    output_echo = os.path.join("outputs", "test_echo.mp3")
    output_highpass = os.path.join("outputs", "test_highpass.mp3")
    output_lowpass = os.path.join("outputs", "test_lowpass.mp3")

    # 确保输出目录存在
    os.makedirs("outputs", exist_ok=True)

    # -------------------------------
    # 【1】音量控制
    # -------------------------------
    print("🔹 测试调整音量 (音量倍数: 2.0)")
    if editor.adjust_volume(bgm_path, output_adjust_volume, volume_factor=2.0):
        print("✅ 音量调整成功！输出文件: " + output_adjust_volume)
    else:
        print("❌ 音量调整失败！")

    # -------------------------------
    # 【2】背景音乐混合（BGM）+ 淡入淡出
    # -------------------------------
    print("🔹 测试为视频添加背景音乐，并设置音量与淡入淡出")
    if editor.add_background_music(video_path, bgm_path, output_add_bgm, bgm_volume=1.0, fade_duration=60.0):
        print("✅ 背景音乐混合成功！输出文件: " + output_add_bgm)
    else:
        print("❌ 背景音乐混合失败！")

    # -------------------------------
    # 【3】音频淡入淡出
    # -------------------------------
    print("🔹 测试为音频添加淡入淡出效果")
    if editor.apply_audio_fade(output_adjust_volume, output_apply_fade, fade_in_duration=10.0, fade_out_duration=10.0):
        print("✅ 音频淡入淡出成功！输出文件: " + output_apply_fade)
    else:
        print("❌ 音频淡入淡出失败！")

    # -------------------------------
    # 【4】音频剪辑（按时间段裁剪）
    # -------------------------------
    print("🔹 测试按时间段裁剪音频 (从 20 到 60)")
    if editor.trim_audio_by_time(bgm_path, output_trim_audio, start_time="20", end_time="60"):
        print("✅ 音频剪辑成功！输出文件: " + output_trim_audio)
    else:
        print("❌ 音频剪辑失败！")

    # -------------------------------
    # 【5】音频提取（从视频中提取音频）
    # -------------------------------
    print("🔹 测试从视频中提取音频")
    if editor.extract_audio_from_video(video_path, output_extract_audio):
        print("✅ 音频提取成功！输出文件: " + output_extract_audio)
    else:
        print("❌ 音频提取失败！")

    # -------------------------------
    # 【6】音频与视频同步（简单对齐，可通过剪辑或延迟实现）
    # -------------------------------
    print("🔹 测试将音频与视频同步 (音频延迟 10.0 秒)")
    if editor.sync_audio_with_video(video_path, output_adjust_volume, output_sync_audio, audio_start_offset=10.0):
        print("✅ 音频同步成功！输出文件: " + output_sync_audio)
    else:
        print("❌ 音频同步失败！")

    # -------------------------------
    # 【7】多音轨处理：混合多个音频输入，可控制各自音量
    # -------------------------------
    print("🔹 测试混合多个音频轨道")
    audio_paths = [bgm_path, output_extract_audio]  # 示例：混合原BGM和调整音量后的BGM
    volumes = [0.1, 1.0]  # 第一个音轨原音量，第二个音轨音量减半
    if editor.mix_multiple_audio_tracks(audio_paths, output_mix_multiple, volumes=volumes):
        print("✅ 多音轨混合成功！输出文件: " + output_mix_multiple)
    else:
        print("❌ 多音轨混合失败！")

    # -------------------------------
    # 【8】基础音效
    # -------------------------------

    # 【8.1】应用均衡器
    print("🔹 测试应用均衡器 (低频 +2.0dB, 中频 +1.0dB, 高频 +0.5dB)")
    if editor.apply_equalizer(output_adjust_volume, output_equalizer, low_gain=2.0, mid_gain=1.0, high_gain=0.5):
        print("✅ 均衡器应用成功！输出文件: " + output_equalizer)
    else:
        print("❌ 均衡器应用失败！")

    # 【8.2】应用回声效果
    print("🔹 测试应用回声效果 (延迟 0.8s, 衰减 0.3)")
    if editor.apply_echo_effect(output_adjust_volume, output_echo, delay_ms=800, decay=0.3):
        print("✅ 回声效果应用成功！输出文件: " + output_echo)
    else:
        print("❌ 回声效果应用失败！")

    # 【8.3】应用高通滤波器
    print("🔹 测试应用高通滤波器 (截止频率 200 Hz)")
    if editor.apply_highpass_filter(output_adjust_volume, output_highpass, cutoff_freq=200.0):
        print("✅ 高通滤波器应用成功！输出文件: " + output_highpass)
    else:
        print("❌ 高通滤波器应用失败！")

    # 【8.4】应用低通滤波器
    print("🔹 测试应用低通滤波器 (截止频率 2000 Hz)")
    if editor.apply_lowpass_filter(output_adjust_volume, output_lowpass, cutoff_freq=2000.0):
        print("✅ 低通滤波器应用成功！输出文件: " + output_lowpass)
    else:
        print("❌ 低通滤波器应用失败！")

    print("🎵" + " " * 8 + "AudioEditor 测试完成。" + " " * 8 + "🎵\n")

if __name__ == "__main__":
    test_audio_editor()
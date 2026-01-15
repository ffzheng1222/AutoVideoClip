# utils.py
import os
#import subprocess
import shutil
#from typing import List
import subprocess
from typing import Optional


def check_ffmpeg_installed() -> bool:
    """
    检查当前系统中是否安装了 ffmpeg，并且可以在命令行中运行。
    返回 True 表示 ffmpeg 可用，False 表示未安装或不在 PATH 中。
    """
    try:
        # 尝试运行 ffmpeg -version，如果成功说明已安装
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        # 捕获找不到命令或执行失败的异常
        return False


def ensure_dir_exists(directory: str):
    """
    检查输出目录是否存在，如果不存在则创建该目录。
    :param directory: 要确保存在的目录路径
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_output_filepath(output_dir: str, filename: str) -> str:
    """
    根据输出目录和文件名，生成安全的完整输出路径，并确保目录存在。
    :param output_dir: 输出目录，如 "outputs/"
    :param filename: 输出文件名，如 "cut_video.mp4"
    :return: 完整的输出文件路径，如 "/project/outputs/cut_video.mp4"
    """
    ensure_dir_exists(output_dir)
    return os.path.join(output_dir, filename)

def clear_outputs_directory(outputs_dir: str) -> None:
    """
    清空 outputs 目录中的所有文件和子文件夹（谨慎操作：不可恢复）
    :param outputs_dir: outputs 文件夹路径，比如 "outputs/"
    """

    if not os.path.exists(outputs_dir):
        print(f"[ℹ️] outputs 目录不存在：{outputs_dir}，无需清理。")
        return

    print(f"[🧹] 开始清理 outputs 目录：{outputs_dir} 中的所有文件和文件夹...")

    try:
        for item in os.listdir(outputs_dir):
            item_path = os.path.join(outputs_dir, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.remove(item_path)
                    print(f"[✅] 已删除文件：{item_path}")
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    print(f"[✅] 已删除文件夹及内容：{item_path}")
            except Exception as e:
                print(f"[❌ 删除失败：{item_path}，原因：{e}]")
        print(f"[🧹] ✅ outputs 目录清理完成。")
    except Exception as e:
        print(f"[❌ 清理 outputs 目录时发生错误：{e}]")

    # 确保目录存在
    os.makedirs(outputs_dir, exist_ok=True)

# 获取视频总时长（秒）
def get_video_duration(video_path: str) -> Optional[float]:
    """
    获取视频时长（秒），严谨可靠版
    :param video_path: 视频文件路径
    :return: 时长（秒）或None（失败时）
    """
    cmd = [
        'ffprobe',
        '-v', 'error',  # 只显示错误信息
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]

    try:
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        return float(result.stdout.strip())
    except Exception as e:
        print(f"获取视频时长失败: {e}")
        return None

# ==================== 获取时间基准 ====================
def get_start_pts(media_path: str, is_video: bool) -> float:
    """获取音视频的起始时间戳（秒）"""
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0' if is_video else 'a:0',
        '-show_entries', 'packet=pts_time',
        '-of', 'csv=p=0',
        media_path
    ]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        first_pts = float(result.stdout.split('\n')[0])
        return first_pts
    except Exception as e:
        print(f"获取PTS失败: {e}")
        return 0.0

# 检查视频是否包含音频轨道
def has_audio(video_path: str) -> bool:
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'a',
        '-show_entries', 'stream=codec_type',
        '-of', 'csv=p=0',
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return bool(result.stdout.strip())
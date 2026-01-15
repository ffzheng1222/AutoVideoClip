# video_editor.py
import os
import subprocess
#from typing import List
from utils import get_output_filepath
#from utils import get_output_filepath, ensure_dir_exists


class VideoEditor:
    def __init__(self, ffmpeg_cmd: str = "ffmpeg"):
        """
        初始化视频编辑器。
        :param ffmpeg_cmd: ffmpeg 命令的名称，默认为 'ffmpeg'（需已在系统 PATH 中）
        """
        self.ffmpeg = ffmpeg_cmd

    def _run_ffmpeg(self, cmd_args: list[str]) -> bool:
        """
        执行 ffmpeg 命令的核心方法。
        :param cmd_args: ffmpeg 的参数列表，例如 ['-i', 'input.mp4', 'output.mp4']
        :return: True 表示执行成功，False 表示执行失败（会打印详细的错误日志）
        """
        global full_cmd
        try:
            # 构造完整的 ffmpeg 命令列表，例如：['ffmpeg', '-i', 'input.mp4', 'output.mp4']
            full_cmd = [self.ffmpeg] + cmd_args  # type: list[str]

            # 执行 ffmpeg 命令
            # stdout=subprocess.PIPE 捕获标准输出（一般不需要打印）
            # stderr=subprocess.PIPE 捕获错误输出（调试时很重要）
            # check=True 表示如果 ffmpeg 返回非零状态码，就抛出 CalledProcessError 异常
            result = subprocess.run(
                full_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )

            # 如果执行到这里，说明 ffmpeg 命令成功了
            return True

        except subprocess.CalledProcessError as e:
            # 捕获 ffmpeg 命令执行错误（比如参数错误、输入文件不存在、编码问题等）
            # e.stderr 是字节串，需要用 decode 转成人可读的消息
            print(f"[❌ FFmpeg 命令执行失败，命令：{' '.join(full_cmd)}]")  # ✅ full_cmd 已定义，安全访问
            print(f"[错误输出]: {e.stderr.decode('utf-8', errors='ignore')}")  # 打印 ffmpeg 的错误详情
            return False

        except Exception as e:
            # 捕获其它可能的异常，比如：权限不足、系统调用失败、内存问题等
            print(f"[❌ 发生未知错误: {e}]")
            return False

    def cut_video(self, input_path: str, output_path: str, start_time: str, end_time: str) -> bool:
        """
        裁剪视频：从 start_time 到 end_time（支持格式：HH:MM:SS 或 MM:SS）
        使用 copy 模式，不重新编码，速度最快。
        :param input_path: 输入视频路径，如 "inputs/input1.mp4"
        :param output_path: 输出视频路径，如 "outputs/cut.mp4"
        :param start_time: 开始时间，如 "00:00:05"
        :param end_time: 结束时间，如 "00:00:10"
        :return: 成功返回 True，失败返回 False
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-ss', start_time,     # 开始时间
            '-to', end_time,       # 结束时间
            '-c:v', 'copy',        # 视频流直接复制，不重新编码
            '-c:a', 'copy',        # 音频流直接复制，不重新编码
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    def extract_audio(self, input_path: str, output_path: str) -> bool:
        """
        从视频中提取音频，保存为 mp3 格式。
        :param input_path: 输入的视频文件路径
        :param output_path: 输出的音频文件路径，如 "outputs/audio.mp3"
        :return: 成功返回 True，失败返回 False
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-q:a', '0',           # 最高质量
            '-map', 'a',           # 只提取音频流
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    def speed_up_video(self, input_path: str, output_path: str, speed: float) -> bool:
        """
        改变视频播放速度（加速或减速）
        :param speed: 倍速，如 2.0 表示 2 倍速（加速），0.5 表示慢动作
        :return: 成功返回 True，失败返回 False
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        pts_factor = 1.0 / speed      # 视频时间轴缩放因子
        atempo_factor = speed         # 音频速度调整因子

        cmd = [
            '-i', input_path,
            '-filter:v', f'setpts={pts_factor:.3f}*PTS',  # 视频速度
            '-filter:a', f'atempo={atempo_factor:.3f}',   # 音频速度
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    def add_watermark(self, input_path: str, watermark_path: str, output_path: str, position: str = "top-right") -> bool:
        """
        给视频添加图片水印
        :param position: 水印位置，支持：top-right（默认）、top-left、bottom-right、bottom-left、center
        :return: 成功返回 True，失败返回 False
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))

        # 根据位置设置水印的 X Y 坐标表达式
        if position == "top-right":
            x_expr, y_expr = "main_w-overlay_w-10", "10"
        elif position == "top-left":
            x_expr, y_expr = "10", "10"
        elif position == "bottom-right":
            x_expr, y_expr = "main_w-overlay_w-10", "main_h-overlay_h-10"
        elif position == "bottom-left":
            x_expr, y_expr = "10", "main_h-overlay_h-10"
        elif position == "center":
            x_expr, y_expr = "(main_w-overlay_w)/2", "(main_h-overlay_h)/2"
        else:
            x_expr, y_expr = "10", "10"  # 默认：左上角

        cmd = [
            '-i', input_path,
            '-i', watermark_path,
            '-filter_complex', f'[1][0]overlay={x_expr}:{y_expr}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

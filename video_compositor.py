# video_compositor.py
import os
import subprocess
from typing import Optional
from utils import get_output_filepath


class VideoCompositor:
    def __init__(self, ffmpeg_cmd: str = "ffmpeg"):
        """
        初始化视频合成器
        :param ffmpeg_cmd: ffmpeg 命令名称，默认为 'ffmpeg'
        """
        self.ffmpeg = ffmpeg_cmd

    def _run_ffmpeg(self, cmd_args: list) -> bool:
        """
        执行 ffmpeg 命令
        :param cmd_args: 参数列表，如 ['-i', 'input.mp4', '-vf', 'drawtext=...', 'output.mp4']
        :return: True 表示成功，False 表示失败
        """
        global full_cmd
        try:
            full_cmd = [self.ffmpeg] + cmd_args
            result = subprocess.run(
                full_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"[❌ 视频合成失败，命令：{' '.join(full_cmd)}]")
            print(f"[错误详情]: {e.stderr.decode('utf-8', errors='ignore')}")
            return False
        except Exception as e:
            print(f"[❌ 未知错误: {e}]")
            return False

    # ----------------------------------------------------------------------
    # 【1】添加文字标题（静态）
    # ----------------------------------------------------------------------
    def add_title(self, input_path: str, output_path: str, title_text: str, position: str = "center", fontsize: int = 48, fontcolor: str = "white") -> bool:
        """
        在视频上添加一个静态文字标题
        :param position: 标题位置，如 "center", "top", "bottom-left" 等（简单实现，可扩展为 x:y）
        :param fontsize: 字体大小
        :param fontcolor: 字体颜色，如 white, red, #FFFFFF
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        x, y = self._get_position(position, "title")
        drawtext_filter = f"drawtext=text='{title_text}':fontsize={fontsize}:fontcolor={fontcolor}:x={x}:y={y}"
        cmd = [
            '-i', input_path,
            '-vf', drawtext_filter,
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【2】添加字幕（可设置时间范围、位置、样式）
    # ----------------------------------------------------------------------
    def add_subtitle(self, input_path: str, output_path: str, subtitle_text: str, start_time: str, end_time: str, position: str = "bottom", fontsize: int = 28, fontcolor: str = "white") -> bool:
        """
        在视频的指定时间段添加字幕
        :param start_time: 开始时间，如 "00:00:05"
        :param end_time: 结束时间，如 "00:00:10"
        :param position: 字幕位置，如 "bottom", "top", "center"
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        x, y = self._get_position(position, "subtitle")
        drawtext_filter = (
            f"drawtext=text='{subtitle_text}':fontsize={fontsize}:fontcolor={fontcolor}:"
            f"x={x}:y={y}:enable='between(t,{self._time_to_sec(start_time)},{self._time_to_sec(end_time)})'"
        )
        cmd = [
            '-i', input_path,
            '-vf', drawtext_filter,
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【3】添加图形元素（如 logo、水印，通过 overlay 图片实现）
    # ----------------------------------------------------------------------
    def add_graphic_overlay(self, input_path: str, graphic_path: str, output_path: str, position: str = "top-right", offset_x: int = 10, offset_y: int = 10) -> bool:
        """
        在视频上叠加一个图片（如 logo、水印）
        :param graphic_path: 图片路径，如 logo.png
        :param position: 位置，如 "top-right", "bottom-left"
        :param offset_x: X偏移
        :param offset_y: Y偏移
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        x_expr, y_expr = self._get_graphic_position(position, offset_x, offset_y)
        cmd = [
            '-i', input_path,
            '-i', graphic_path,
            '-filter_complex', f'[1:v]scale=100:-1[scaled];[0:v][scaled]overlay={x_expr}:{y_expr}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【4】动态图形（如移动的 logo，使用 x/y 表达式）
    # ----------------------------------------------------------------------
    def add_moving_graphic(self, input_path: str, graphic_path: str, output_path: str, duration: float = 5.0, direction: str = "right") -> bool:
        """
        添加一个从左到右（或自定义方向）移动的图形（如 logo）
        :param duration: 移动持续时间（秒）
        :param direction: 移动方向，如 "right", "left"
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        if direction == "right":
            x_expr = f"t*50"  # 每秒向右移动 50 像素
        elif direction == "left":
            x_expr = f"-t*50"
        else:
            x_expr = "100"  # 默认固定位置
        y_expr = "100"  # 固定 Y
        cmd = [
            '-i', input_path,
            '-i', graphic_path,
            '-filter_complex', f'[1:v]scale=100:-1[scaled];[0:v][scaled]overlay=x=\'{x_expr}\':y={y_expr}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【5】标题动画（如淡入、滑入）
    # ----------------------------------------------------------------------
    def add_animated_title(self, input_path: str, output_path: str, title_text: str, animation_type: str = "fade_in", duration: float = 2.0) -> bool:
        """
        添加一个带动画的标题（如淡入、从下方滑入）
        :param animation_type: 动画类型，如 "fade_in", "slide_up"
        :param duration: 动画持续时间
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        if animation_type == "fade_in":
            vf = f"drawtext=text='{title_text}':fontsize=50:fontcolor=white:alpha='if(lt(t,1),t/1,1)':x=(w-text_w)/2:y=(h-text_h)/2"
        elif animation_type == "slide_up":
            vf = f"drawtext=text='{title_text}':fontsize=50:fontcolor=white:y='h-(h-text_h)-t*50':x=(w-text_w)/2:alpha=1"
        else:
            vf = f"drawtext=text='{title_text}':fontsize=50:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2"
        cmd = [
            '-i', input_path,
            '-vf', vf,
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【6】AR 叠加（模拟，如静态贴图，可扩展为动态跟踪）
    # ----------------------------------------------------------------------
    def add_ar_overlay(self, input_path: str, ar_path: str, output_path: str, position: str = "center") -> bool:
        """
        模拟 AR 叠加效果（如人脸贴纸、虚拟元素），使用静态图片
        :param ar_path: AR 图片路径，如 "face_sticker.png"
        :param position: 位置，如 "center"
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        x, y = self._get_position(position, "ar")
        cmd = [
            '-i', input_path,
            '-i', ar_path,
            '-filter_complex', f'[1:v]scale=200:-1[scaled];[0:v][scaled]overlay={x}:{y}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【7】元数据嵌入（如标题、作者等）
    # ----------------------------------------------------------------------
    def embed_metadata(self, input_path: str, output_path: str, title: Optional[str] = None, author: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        向视频文件嵌入元数据（如标题、作者、描述）
        :param title: 视频标题
        :param author: 作者
        :param description: 描述
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        metadata_args = []
        if title:
            metadata_args.extend(['-metadata', f'title={title}'])
        if author:
            metadata_args.extend(['-metadata', f'artist={author}'])
        if description:
            metadata_args.extend(['-metadata', f'description={description}'])
        cmd = ['-i', input_path] + metadata_args + [safe_output]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【辅助函数】根据位置返回 x:y 坐标表达式
    # ----------------------------------------------------------------------
    def _get_position(self, position: str, element: str) -> tuple[str, str]:
        # 简化实现，返回 ffmpeg drawtext / overlay 可用的 x:y 表达式或固定值
        if position == "center":
            return "(w-text_w)/2", "(h-text_h)/2"
        elif position == "top":
            return "(w-text_w)/2", "20"
        elif position == "bottom":
            return "(w-text_w)/2", f"h-text_h-20"
        elif position == "top-left":
            return "20", "20"
        elif position == "bottom-left":
            return "20", f"h-text_h-20"
        elif position == "top-right":
            return f"w-text_w-20", "20"
        elif position == "bottom-right":
            return f"w-text_w-20", f"h-text_h-20"
        else:
            return "(w-text_w)/2", "(h-text_h)/2"  # 默认居中

    def _get_graphic_position(self, position: str, offset_x: int, offset_y: int) -> tuple[str, str]:
        if position == "top-right":
            return f"w-offset_x-100", f"{offset_y}"
        elif position == "bottom-left":
            return f"{offset_x}", f"h-offset_y-100"
        elif position == "center":
            return f"(w-100)/2", f"(h-100)/2"
        else:  # top-right 作为默认
            return f"w-100-10", f"{offset_y}"

    # ----------------------------------------------------------------------
    # 【辅助函数】时间字符串转秒数
    # ----------------------------------------------------------------------
    def _time_to_sec(self, time_str: str) -> float:
        h, m, s = map(float, time_str.split(':'))
        return h * 3600 + m * 60 + s
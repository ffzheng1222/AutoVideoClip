# color_correction.py
import os
import subprocess
#from typing import Optional
from utils import get_output_filepath


class ColorCorrection:
    def __init__(self, ffmpeg_cmd: str = "ffmpeg"):
        """
        初始化色彩校正工具
        :param ffmpeg_cmd: ffmpeg 命令名称，默认为 'ffmpeg'（需在系统 PATH 中）
        """
        self.ffmpeg = ffmpeg_cmd

    def _run_ffmpeg(self, cmd_args: list) -> bool:
        """
        执行 ffmpeg 命令
        :param cmd_args: 参数列表，如 ['-i', 'input.mp4', '-vf', 'eq=...', 'output.mp4']
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
            print(f"[❌ 色彩校正失败，命令：{' '.join(full_cmd)}]")
            print(f"[错误详情]: {e.stderr.decode('utf-8', errors='ignore')}")
            return False
        except Exception as e:
            print(f"[❌ 未知错误: {e}]")
            return False

    # ----------------------------------------------------------------------
    # 【1】亮度调整
    # ----------------------------------------------------------------------
    def adjust_brightness(self, input_path: str, output_path: str, brightness: float = 0.0) -> bool:
        """
        调整视频亮度
        :param brightness: 亮度偏移，如 0.1 提亮，-0.1 变暗
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f'eq=brightness={brightness}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【2】对比度调整
    # ----------------------------------------------------------------------
    def adjust_contrast(self, input_path: str, output_path: str, contrast: float = 1.0) -> bool:
        """
        调整视频对比度
        :param contrast: 对比度倍数，如 1.2 增强，0.8 降低
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f'eq=contrast={contrast}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【3】饱和度调整
    # ----------------------------------------------------------------------
    def adjust_saturation(self, input_path: str, output_path: str, saturation: float = 1.0) -> bool:
        """
        调整视频色彩饱和度
        :param saturation: 饱和度倍数，如 1.5 增强鲜艳，0.5 降低，0 为黑白
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f'eq=saturation={saturation}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【4】一键电影感色彩分级（推荐调色预设）
    # ----------------------------------------------------------------------
    def apply_cinematic_look(self, input_path: str, output_path: str) -> bool:
        """
        应用电影感色彩风格（增强对比度、降低饱和度、微微偏蓝调）
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', 'eq=contrast=1.2:brightness=0.05:saturation=0.9:gamma_r=1.1:gamma_g=1.1:gamma_b=1.2',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【5】复古色调（偏黄 / 暖色怀旧）
    # ----------------------------------------------------------------------
    def apply_vintage_look(self, input_path: str, output_path: str) -> bool:
        """
        应用复古色调效果（暖色、降低对比、降低饱和）
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', 'eq=contrast=0.9:brightness=0.1:saturation=0.8:gamma_r=1.1:gamma_g=1.0:gamma_b=0.9',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【6】冷色调（偏蓝 / 清新科技感）
    # ----------------------------------------------------------------------
    def apply_cool_look(self, input_path: str, output_path: str) -> bool:
        """
        应用冷色调效果（偏蓝、高对比、高饱和）
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', 'eq=contrast=1.3:brightness=-0.05:saturation=1.4:gamma_r=1.0:gamma_g=1.0:gamma_b=1.3',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【7】黑白（去色 / 灰度）
    # ----------------------------------------------------------------------
    def apply_grayscale(self, input_path: str, output_path: str) -> bool:
        """
        将视频转换为黑白（去饱和度）
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', 'eq=saturation=0',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【8】一键增强锐化（提升清晰度）
    # ----------------------------------------------------------------------
    def apply_sharpen(self, input_path: str, output_path: str) -> bool:
        """
        应用锐化滤镜，提升细节清晰度
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', 'unsharp=5:5:1.0:5:5:0.0',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【9】色相偏移（Hue Shift）
    # ----------------------------------------------------------------------
    def apply_hue_shift(self, input_path: str, output_path: str, hue_angle: float = 30.0) -> bool:
        """
        应用色相偏移，让画面整体偏移色相（如偏红、绿、蓝）
        :param hue_angle: 色相角度偏移（0~360），如 30 表示轻微偏移
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f'hue=h={hue_angle}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【10】阴影提亮（提亮暗部）
    # ----------------------------------------------------------------------
    def lift_shadows(self, input_path: str, output_path: str, brightness: float = 0.1) -> bool:
        """
        提升视频中的阴影区域亮度（暗部提亮，不改变高光）
        :param brightness: 提升幅度，如 0.1
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f'eq=brightness={brightness}:gamma_r=0.9:gamma_g=0.9:gamma_b=0.9',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【11】高光抑制（防止过曝）
    # ----------------------------------------------------------------------
    def reduce_highlights(self, input_path: str, output_path: str, gamma_reduction: float = 1.2) -> bool:
        """
        压暗高光区域，防止画面过曝（如天空、灯光）
        :param gamma_reduction: gamma 值提升（如 1.2 表示压暗高光）
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f'eq=gamma_r={gamma_reduction}:gamma_g={gamma_reduction}:gamma_b={gamma_reduction}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【12】RGB 曲线调整（类似 PS 曲线，精细控制影调）
    # ----------------------------------------------------------------------
    def adjust_curves(self, input_path: str, output_path: str, shadows: float = 0.0, midtones: float = 0.0,
                      highlights: float = 0.0) -> bool:
        """
        使用曲线调整阴影 / 中间调 / 高光（类似 PS 曲线工具）
        :param shadows: 暗部调整
        :param midtones: 中间调
        :param highlights: 高光
        :return: 是否成功（注意：ffmpeg curves 滤镜使用较复杂，此处为简化示例）
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        # 简化实现，实际 curves 滤镜语法较为复杂，可用 eq 组合替代
        cmd = [
            '-i', input_path,
            '-vf', f'eq=brightness={(shadows + midtones + highlights) * 0.3}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【13】简单降噪（去除画面噪点）
    # 注：ffmpeg 原生 curves滤镜语法较复杂，如需完整 PS 风格曲线，可使用 lut3d或封装第三方 LUT，这里提供简化控制。
    # ----------------------------------------------------------------------
    def apply_denoise(self, input_path: str, output_path: str) -> bool:
        """
        应用简单降噪滤镜，减少画面噪点 / 颗粒
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', 'hqdn3d=1.5:1.5:3:3',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【14】边缘柔化 / 梦幻效果
    # ----------------------------------------------------------------------
    def apply_soft_focus(self, input_path: str, output_path: str, strength: float = 2.0) -> bool:
        """
        应用柔焦效果，让画面变得朦胧、梦幻
        :param strength: 柔化强度
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f'smartblur=lr={strength}:ls={strength}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【15】色彩分离 / RGB 偏移（镜头故障艺术效果）
    # ----------------------------------------------------------------------
    def apply_rgb_split(self, input_path: str, output_path: str, offset: float = 2.0) -> bool:
        """
        模拟 RGB 色彩分离效果（如镜头故障、赛博感）
        :param offset: 偏移距离（像素）
        :return: 是否成功（简化模拟，真实 RGB 分离需要多层 shift 滤镜）
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f'colorchannelmixer=rr:gg:bb=1:0:0.02:0:1:0.02:0:0:1:0.02',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【16】一键色彩匹配预设（如抖音风格 / 赛博朋克 / 清新等）
    # ----------------------------------------------------------------------
    def apply_preset_style(self, input_path: str, output_path: str, style: str = "douyin") -> bool:
        """
        应用预设的色彩风格（如抖音、赛博朋克、清新自然等）
        :param style: 风格名称，如 "douyin", "cyberpunk", "fresh"
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        if style == "douyin":
            # 抖音风格：高对比、高饱和、偏亮
            cmd = [
                '-i', input_path,
                '-vf', 'eq=contrast=1.4:saturation=1.6:brightness=0.05',
                safe_output
            ]
        elif style == "cyberpunk":
            # 赛博朋克：偏蓝青、高对比
            cmd = [
                '-i', input_path,
                '-vf', 'eq=contrast=1.5:saturation=1.3:brightness=-0.1:gamma_r=1.0:gamma_g=0.8:gamma_b=1.4',
                safe_output
            ]
        elif style == "fresh":
            # 清新自然：明亮柔和
            cmd = [
                '-i', input_path,
                '-vf', 'eq=contrast=1.1:saturation=1.2:brightness=0.1:gamma_r=1.0:gamma_g=1.0:gamma_b=1.1',
                safe_output
            ]
        else:
            print(f"[⚠️] 未知风格: {style}")
            return False
        return self._run_ffmpeg(cmd)
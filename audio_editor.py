# audio_editor.py
import os
import subprocess
from typing import Optional
import utils


class AudioEditor:
    def __init__(self, ffmpeg_cmd: str = "ffmpeg"):
        """
        初始化音频编辑器
        :param ffmpeg_cmd: ffmpeg 命令名称，默认为 'ffmpeg'（需在系统 PATH 中）
        """
        self.ffmpeg = ffmpeg_cmd

    def _run_ffmpeg(self, cmd_args: list) -> bool:
        """
        执行 ffmpeg 命令
        :param cmd_args: ffmpeg 参数列表，如 ['-i', 'input.mp3', 'output.mp3']
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
            print(f"[❌ 音频处理失败，命令：{' '.join(full_cmd)}]")
            print(f"[错误详情]: {e.stderr.decode('utf-8', errors='ignore')}")
            return False
        except Exception as e:
            print(f"[❌ 未知错误: {e}]")
            return False

    # ----------------------------------------------------------------------
    # 【1】音量控制
    # ----------------------------------------------------------------------

    def adjust_volume(self, input_path: str, output_path: str, volume_factor: float = 1.0) -> bool:
        """
        调整音频音量
        :param volume_factor: 倍数，如 0.5（降低一半）、2.0（加倍）
        :return: 是否成功
        """
        safe_output = utils.get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-af', f'volume={volume_factor}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【2】背景音乐混合（BGM）+ 淡入淡出
    # ----------------------------------------------------------------------

    def add_background_music(self, video_path: str, bgm_path: str, output_path: str, bgm_volume: float = 0.3, fade_duration: float = 2.0) -> bool:
        """
        为视频添加背景音乐，并设置背景音乐音量与淡入淡出
        :param bgm_volume: 背景音乐音量倍数，如 0.3
        :param fade_duration: 淡入淡出时间（秒）
        :return: 是否成功
        """
        safe_output = utils.get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', video_path,
            '-i', bgm_path,
            '-filter_complex',
            f'[1:a]volume={bgm_volume},afade=t=in:st=0:d={fade_duration},afade=t=out:st={fade_duration}:d={fade_duration}[bgm];'
            '[0:a][bgm]amix=inputs=2:duration=longest[a]',
            '-map', '0:v',
            '-map', '[a]',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【3】音频淡入淡出
    # ----------------------------------------------------------------------

    def apply_audio_fade(self, input_path: str, output_path: str, fade_in_duration: float = 1.0, fade_out_duration: float = 1.0) -> bool:
        """
        为音频添加淡入淡出效果
        :param fade_in_duration: 淡入时间（秒）
        :param fade_out_duration: 淡出时间（秒）
        :return: 是否成功
        """
        duration = utils.get_video_duration(input_path)
        fade_out_duration_st = duration - float(fade_out_duration)

        safe_output = utils.get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-af', f'afade=t=in:st=0:d={fade_in_duration},afade=t=out:st={fade_out_duration_st}:d={fade_out_duration}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【4】音频剪辑（按时间段裁剪）
    # ----------------------------------------------------------------------

    def trim_audio_by_time(self, input_path: str, output_path: str, start_time: str, end_time: str) -> bool:
        """
        按开始和结束时间裁剪音频
        :param start_time: 开始时间，如 "00:00:05"
        :param end_time: 结束时间，如 "00:00:10"
        :return: 是否成功
        """
        safe_output = utils.get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-ss', start_time,
            '-to', end_time,
            '-c', 'copy',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【5】音频提取（从视频中提取音频）
    # ----------------------------------------------------------------------

    def extract_audio_from_video(self, video_path: str, output_audio_path: str) -> bool:
        """
        从视频中提取音频（默认 mp3 格式）
        :return: 是否成功
        """
        safe_output = utils.get_output_filepath(os.path.dirname(output_audio_path), os.path.basename(output_audio_path))
        cmd = [
            '-i', video_path,
            '-q:a', '0',
            '-map', 'a',
            '-c:a', 'libmp3lame',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【6】音频与视频同步（简单对齐，可通过剪辑或延迟实现）
    # ----------------------------------------------------------------------
    def sync_audio_with_video(self, video_path: str, audio_path: str, output_path: str,
                              audio_start_offset: float = 0.0) -> bool:
        """
        严谨的音频视频同步方法（动态计算PTS偏移）

        功能：
        1. 自动检测音视频的起始时间差
        2. 支持手动指定的额外偏移量
        3. 智能处理无音频/无视频的情况

        参数：
        :param video_path: 视频文件路径
        :param audio_path: 音频文件路径
        :param output_path: 输出文件路径
        :param audio_start_offset: 额外延迟补偿（秒）
        :return: 是否成功
        """
        # 获取视频和音频的起始PTS
        video_start = utils.get_start_pts(video_path, is_video=True)
        audio_start = utils.get_start_pts(audio_path, is_video=False)

        # ==================== 计算动态延迟 ====================
        # 计算PTS差异（秒）并加上用户指定的偏移量
        total_delay_sec = float(max(0.0, video_start - audio_start + audio_start_offset))
        total_delay_ms = int(round(total_delay_sec * 1000))  # 毫秒需为整数

        print(f"同步参数：视频起始 {video_start:.3f}s, 音频起始 {audio_start:.3f}s, "
              f"最终延迟 {total_delay_ms}ms (含补偿 {audio_start_offset}s)")

        # 根据视频是否包含音频自动调整滤镜链
        video_has_audio = utils.has_audio(video_path)

        # ==================== 构建FFmpeg命令 ====================
        safe_output = utils.get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))

        cmd = [
            '-y',
            '-i', video_path,
            '-i', audio_path,
            '-filter_complex',
            f"[1:a]adelay=delays={total_delay_ms}|{total_delay_ms}[delayed];"
            f"[0:a][delayed]amix=inputs=2:duration=first,volume=2.0[aout]" if video_has_audio else
            f"[1:a]adelay=delays={total_delay_ms}|{total_delay_ms}[aout]",
            '-map', '0:v',
            '-map', '[aout]',
            '-c:v', 'copy',
            '-c:a', 'aac', '-b:a', '192k',
            '-movflags', '+faststart',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 多音轨处理
    # 【7】多音轨处理：混合多个音频输入，可控制各自音量
    # ----------------------------------------------------------------------

    def mix_multiple_audio_tracks(self, audio_paths: list[str], output_path: str,
                                  volumes: Optional[list[float]] = None) -> bool:
        """
        混合多个音频轨道为一个音频文件
        :param audio_paths: 多个音频文件路径列表，如 ["bgm.mp3", "voice.mp3", "effect.mp3"]
        :param output_path: 输出的混合后音频路径
        :param volumes: 可选，每个音频轨道的音量倍数，如 [1.0, 0.8, 0.5]，长度需与 audio_paths 一致
        :return: 是否成功
        """
        if not audio_paths:
            print("[❌] 错误：没有提供音频文件路径")
            return False

        safe_output = utils.get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))

        # 默认所有音轨音量为 1.0
        if volumes is None:
            volumes = [1.0] * len(audio_paths)

        if len(volumes) != len(audio_paths):
            print("[❌] 错误：volumes 长度必须与 audio_paths 一致")
            return False

        # 构建滤镜链：每个音频先调整音量，然后混合
        inputs = []
        filter_parts = []
        for i, (audio_path, vol) in enumerate(zip(audio_paths, volumes)):
            inputs.extend(['-i', audio_path])
            filter_parts.append(f"[{i}:a]volume={vol}[a{i}];")

        # 拼接所有音轨：[a0][a1][a2]...amix=inputs=N
        filter_inputs = "".join([f"[a{i}]" for i in range(len(audio_paths))])
        filter_complex = "".join(filter_parts) + f"{filter_inputs}amix=inputs={len(audio_paths)}:duration=longest[aout]"

        cmd = inputs + ['-filter_complex', filter_complex, '-map', '[aout]', safe_output]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 基础音效
    # 【8】基础音效：使用 ffmpeg 滤镜实现
    # ----------------------------------------------------------------------

    def apply_equalizer(self, input_path: str, output_path: str, low_gain: float = 0.0, mid_gain: float = 0.0,
                        high_gain: float = 0.0) -> bool:
        """
        应用简单的均衡器效果，调整低中高频
        :param low_gain: 低频增益（如 +2.0dB 提升低音）
        :param mid_gain: 中频增益
        :param high_gain: 高频增益
        :return: 是否成功
        """
        safe_output = utils.get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        eq_expr = f"equalizer=f={32}:width_type=h:width=1:g={low_gain},equalizer=f={1000}:width_type=h:width=1:g={mid_gain},equalizer=f={5000}:width_type=h:width=1:g={high_gain}"
        cmd = [
            '-i', input_path,
            '-af', eq_expr,
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    def apply_echo_effect(self, input_path: str, output_path: str, delay_ms: int = 800, decay: float = 0.3, in_gain: float = 0.8, out_gain: float = 0.8) -> bool:
        """
        添加回声效果
        :param delay_ms: 回声延迟（毫秒）
        :param decay: 衰减系数（0.1-0.9）
        :param in_gain: 输入增益（0.0-1.0）
        :param out_gain: 输出增益（0.0-1.0）
        """
        safe_output = utils.get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-af', f'aecho=in_gain={in_gain}:out_gain={out_gain}:delays={delay_ms}:decays={decay}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    def apply_highpass_filter(self, input_path: str, output_path: str, cutoff_freq: float = 300.0) -> bool:
        """
        应用高通滤波器，去掉低频噪音
        :param cutoff_freq: 截止频率（Hz），如 300
        :return: 是否成功
        """
        safe_output = utils.get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-af', f'highpass=f={cutoff_freq}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    def apply_lowpass_filter(self, input_path: str, output_path: str, cutoff_freq: float = 3000.0) -> bool:
        """
        应用低通滤波器，去掉高频噪音
        :param cutoff_freq: 截止频率（Hz），如 3000
        :return: 是否成功
        """
        safe_output = utils.get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-af', f'lowpass=f={cutoff_freq}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

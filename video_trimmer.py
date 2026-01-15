# video_trimmer.py
import os
import subprocess
from typing import List, Tuple
from utils import get_output_filepath,get_video_duration


class VideoTrimmer:
    def __init__(self, ffmpeg_cmd: str = "ffmpeg"):
        """
        初始化精剪工具类
        :param ffmpeg_cmd: ffmpeg 命令名称，默认为 'ffmpeg'（需在系统 PATH 中）
        """
        self.ffmpeg = ffmpeg_cmd

    def _run_ffmpeg(self, cmd_args: List[str]) -> bool:
        """
        执行 ffmpeg 命令的核心方法
        :param cmd_args: ffmpeg 参数列表，如 ['-i', 'input.mp4', 'output.mp4']
        :return: True 表示成功，False 表示失败（会打印错误日志）
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
            print(f"[❌ 精剪操作失败，命令：{' '.join(full_cmd)}]")
            print(f"[错误详情]: {e.stderr.decode('utf-8', errors='ignore')}")
            return False
        except Exception as e:
            print(f"[❌ 未知错误: {e}]")
            return False

    # ======================================================================
    # 【1】调整剪辑点：精准多段剪辑（按时间段裁剪并拼接）
    # ======================================================================

    def trim_by_segments(self, input_path: str, output_path: str, segments: List[Tuple[str, str]]) -> bool:
        """
        按多个时间段精准裁剪视频并拼接（多段剪辑）
        :param input_path: 输入视频路径，如 "inputs/cat_01.mp4"
        :param output_path: 输出视频路径，如 "outputs/trimmed_output.mp4"
        :param segments: 剪辑时间段列表，每个元素为 (开始时间, 结束时间)，如 [("00:00:05", "00:00:10"), ("00:00:15", "00:00:20")]
        :return: 成功返回 True，失败返回 False
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        filter_parts = []

        for i, (start, end) in enumerate(segments):
            # 对每一时间段，截取视频和音频，分别设置 PTS 起始点
            filter_parts.append(f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS[v{i}];")
            filter_parts.append(f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[a{i}];")

        # 拼接所有视频段和音频段
        video_inputs = "".join([f"[v{i}]" for i in range(len(segments))])
        audio_inputs = "".join([f"[a{i}]" for i in range(len(segments))])
        concat_video = f"{video_inputs}concat=n={len(segments)}:v=1:a=0[outv]"
        concat_audio = f"{audio_inputs}concat=n={len(segments)}:v=0:a=1[outa]"

        filter_complex = "".join(filter_parts) + concat_video + ";" + concat_audio

        cmd = [
            '-i', input_path,
            '-filter_complex', filter_complex,
            '-map', '[outv]',
            '-map', '[outa]',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ======================================================================
    # 【2】节奏控制：分段变速（可扩展，暂未完整实现复杂逻辑）
    # ======================================================================

    def adjust_speed_segments(self, input_path: str, output_path: str, speed_map: List[Tuple[str, str, float]]) -> bool:
        """
        对视频的不同时间段设置不同的播放速度（分段变速 / 慢动作 / 快进）
        :param speed_map: 列表，每个元素为 (开始时间, 结束时间, 倍速)，如 [("00:00:05", "00:00:10", 2.0)]
        :return: 成功返回 True，失败返回 False（复杂逻辑，留作扩展）
        """
        print("[⚠️] 分段变速功能（adjust_speed_segments）需要复杂的滤镜链，暂未实现，预留接口。")
        return False

    # ======================================================================
    # 【3】转场效果：淡入淡出（开头和结尾）
    # ======================================================================

    def apply_fade_transition(self, input_path: str, output_path: str, fade_duration: str = "1.0") -> bool:
        """
        为视频添加淡入（开头）和淡出（结尾）转场效果
        :param fade_duration: 淡入淡出持续时间，单位秒，如 "1.0"
        :return: 成功返回 True，失败返回 False
        """

        """带时长检查的版本"""
        # 获取视频时长（秒）
        duration = get_video_duration(input_path)
        if duration is None:
            return False

        fade_out_duration = duration - float(fade_duration)

        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f"fade=t=in:st=0:d={fade_duration},fade=t=out:st={fade_out_duration}:d={fade_duration}",
            '-af', f"afade=t=in:st=0:d={fade_duration},afade=t=out:st={fade_out_duration}:d={fade_duration}",
            safe_output
        ]
        #print(f"cmd: {cmd}")
        return self._run_ffmpeg(cmd)

    # ======================================================================
    # 【4】动态效果：缩放（放大/缩小画面）
    # ======================================================================

    def apply_zoom_effect(self, input_path: str, output_path: str, zoom_ratio: float = 1.2) -> bool:
        """
        为视频添加整体缩放效果（放大或缩小）
        :param zoom_ratio: 缩放倍数，如 1.2 表示放大到 120%
        :return: 成功返回 True，失败返回 False
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f"scale=ceil(iw*{zoom_ratio}):ceil(ih*{zoom_ratio})",
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ======================================================================
    # 【5】特效：模糊效果
    # ======================================================================

    def apply_blur_effect(self, input_path: str, output_path: str, blur_strength: int = 5) -> bool:
        """
        为视频添加模糊特效
        :param blur_strength: 模糊强度（如 5 表示适度模糊）
        :return: 成功返回 True，失败返回 False
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f"boxblur={blur_strength}:{blur_strength}",
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ======================================================================
    # 【6】特效：复古色调（简单色彩调整）
    # ======================================================================

    def apply_vintage_effect(self, input_path: str, output_path: str) -> bool:
        """
        为视频添加复古色调效果（简单 LUT / 色调调整）
        :return: 成功返回 True，失败返回 False
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', 'eq=brightness=0.1:saturation=1.3:contrast=1.1',
            safe_output
        ]
        return self._run_ffmpeg(cmd)


    # ======================================================================
    #  高级功能
    # 【7】更多转场效果（滑动、叠化、擦除等）—— 使用 xfade 滤镜
    # ======================================================================
    def apply_advanced_transition(self, video1_path: str, video2_path: str, output_path: str, transition_type: str = "fade", duration: float = 1.0) -> bool:
        """
        应用高级视频转场效果，如滑动、叠化、擦除等
        :param video1_path: 第一个视频路径
        :param video2_path: 第二个视频路径
        :param transition_type: 转场类型，如 'fade', 'slideleft', 'wipeleft', 'smoothleft', 'distance' 等
        :param duration: 转场持续时间（秒）
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', video1_path,
            '-i', video2_path,
            '-filter_complex', f'[0:v][1:v]xfade=transition={transition_type}:duration={duration}:offset=4[v];[0:a][1:a]acrossfade=d={duration}[a]',
            '-map', '[v]',
            '-map', '[a]',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ======================================================================
    #  高级功能
    # 【8】关键帧精确控制（按时间段启用滤镜）—— 使用 enable='between(t,start,end)'
    # ======================================================================
    def apply_effect_during_time_range(self, input_path: str, output_path: str, effect_expr: str, start_time: str,
                                       end_time: str) -> bool:
        """
        仅在指定的时间段内应用某个滤镜效果
        :param input_path: 输入视频路径
        :param output_path: 输出视频路径
        :param effect_expr: 滤镜表达式，如 "blur=5:5"、"eq=brightness=0.2"
        :param start_time: 开始时间，如 "00:00:05"
        :param end_time: 结束时间，如 "00:00:10"
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))

        # 将时间转为秒，用于 enable 条件
        def to_sec(t: str) -> float:
            h, m, s = map(float, t.split(':'))
            return h * 3600 + m * 60 + s

        enable_cond = f"between(t,{to_sec(start_time)},{to_sec(end_time)})"
        vf = f"{effect_expr},enable='{enable_cond}'"
        cmd = [
            '-i', input_path,
            '-vf', vf,
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ======================================================================
    #  高级功能
    # 【9】LUT 色彩查找表效果（模拟专业预设）—— 使用 eq / colorchannelmixer
    # ======================================================================
    def apply_lut_color_effect(self, input_path: str, output_path: str, brightness: float = 0.0,
                               saturation: float = 1.0, contrast: float = 1.0) -> bool:
        """
        模拟 LUT 色彩查找表效果，调整亮度、饱和度、对比度
        :param brightness: 亮度调整，如 0.1 提亮
        :param saturation: 饱和度，如 1.5 增强
        :param contrast: 对比度，如 1.2 增强
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f'eq=brightness={brightness}:saturation={saturation}:contrast={contrast}',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ======================================================================
    #  高级功能
    # 【10】画中画 / 双视频合成 —— 使用 overlay 滤镜
    # ======================================================================
    def apply_picture_in_picture(self, main_video_path: str, pip_video_path: str, output_path: str,
                                 position: str = "bottom-right") -> bool:
        """
        将第二个视频作为画中画叠加在主视频的指定位置
        :param position: 位置，如 'bottom-right'（默认）、'top-left'、'center' 等
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        # 将画中画视频缩小为 1/4
        x_expr, y_expr = "main_w-overlay_w-10", "main_h-overlay_h-10"  # 右下角
        if position == "top-left":
            x_expr, y_expr = "10", "10"
        elif position == "top-right":
            x_expr, y_expr = "main_w-overlay_w-10", "10"
        elif position == "center":
            x_expr, y_expr = "(main_w-overlay_w)/2", "(main_h-overlay_h)/2"
        cmd = [
            '-i', main_video_path,
            '-i', pip_video_path,
            '-filter_complex', f'[1:v]scale=iw/4:ih/4[scaled];[0:v][scaled]overlay={x_expr}:{y_expr}',
            '-map', '[0:v]',
            '-map', '0:a',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ======================================================================
    #  高级功能
    # 【11】多轨道音频混音 / 延迟 / 淡入淡出 —— 使用 adelay / amix / afade
    # ======================================================================
    def mix_audio_with_delay(self, audio1_path: str, audio2_path: str, output_path: str,
                             delay_seconds: float = 0.0) -> bool:
        """
        混合两个音频轨道，第二个音频可设置延迟（秒）
        :param delay_seconds: 第二个音频延迟时间（如 1.0 秒）
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        delay_ms = int(delay_seconds * 1000)
        adelay_filter = f"adelay={delay_ms}|{delay_ms}"
        cmd = [
            '-i', audio1_path,
            '-i', audio2_path,
            '-filter_complex', f'{adelay_filter}[delayed];[0:a][delayed]amix=inputs=2:duration=longest[a]',
            '-map', '0:v',  # 保留主视频（如果有）
            '-map', '[a]',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ======================================================================
    #  动画效果扩展
    # 【12】平移动画（从左到右 / 从上到下移动）
    # ======================================================================
    def apply_horizontal_slide_animation(self, input_path: str, output_path: str, direction: str = "right",
                                         duration: float = 5.0) -> bool:
        """
        应用水平方向平移动画效果（如从左到右移动）
        :param direction: 移动方向，如 "right"（向右）、"left"（向左）
        :param duration: 动画持续时长（秒）
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        if direction == "right":
            x_expr = f"t*100"  # 每秒向右移动 100 像素
        elif direction == "left":
            x_expr = f"-t*100"
        else:
            x_expr = "0"
        cmd = [
            '-i', input_path,
            '-vf', f"crop=iw-200:ih:100:0, x='{x_expr}':y=0",  # 从左侧开始移动
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ======================================================================
    #  旋转动画（缓慢 360° 旋转）
    # 【13】多轨道音频混音 / 延迟 / 淡入淡出 —— 使用 adelay / amix / afade
    # 📌 提示：更精确的旋转可以使用 rotate=PI*2*t/{duration}，需要 ffmpeg 支持表达式。
    # ======================================================================
    def apply_rotation_animation(self, input_path: str, output_path: str, duration: float = 5.0,
                                 degrees: float = 360.0) -> bool:
        """
        应用旋转动画效果（如 360° 旋转）
        :param degrees: 总旋转角度，如 360
        :param duration: 持续时间（秒）
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f"rotate=2*PI*t/{duration}:ow=hypot(iw,ih):oh=ow",
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ======================================================================
    #  动画效果扩展
    # 【14】缩放 + 平移动画（放大并移动）
    # ======================================================================
    def apply_scale_and_move_animation(self, input_path: str, output_path: str,
                                       scale_range: Tuple[float, float] = (1.0, 1.5), duration: float = 5.0) -> bool:
        """
        缩放并移动动画（如放大同时从中心往右移动）
        :param scale_range: 缩放范围，如 (1.0, 1.5)
        :param duration: 持续时间
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        scale_end = scale_range[1]
        x_expr = f"(iw/2)-(iw*{scale_end}/2)+t*50"  # 向右移动
        cmd = [
            '-i', input_path,
            '-vf',
            f"scale=iw*{scale_range[0]}:ih*{scale_range[0]}:x='(iw/2)-(iw*{scale_range[1]}/2)+t*30':y='(ih/2)-(ih*{scale_range[1]}/2)'",
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ======================================================================
    #  动画效果扩展
    # 【15】淡入动画（透明度渐显）
    # ======================================================================
    def apply_fade_in_animation(self, input_path: str, output_path: str, fade_duration: float = 2.0) -> bool:
        """
        视频从透明逐渐显现（淡入）
        :param fade_duration: 淡入时间（秒）
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f"fade=t=in:st=0:d={fade_duration}",
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ======================================================================
    #  动画效果扩展
    # 【16】画中画动态移动（小窗从左到右移动）
    # ======================================================================
    def apply_moving_pip_animation(self, main_video_path: str, pip_video_path: str, output_path: str,
                                   duration: float = 5.0) -> bool:
        """
        画中画小窗口从左到右动态移动
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', main_video_path,
            '-i', pip_video_path,
            '-filter_complex',
            f'[1:v]scale=iw/4:ih/4[scaled];[0:v][scaled]overlay=x=\'t*100\':y=\'ih/2-(ih/4/2)\':enable=\'between(t,0,{duration})\'',
            '-map', '[0:v]',
            '-map', '0:a',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ======================================================================
    #  动画效果扩展
    # 【17】摇摆 / 震动效果
    # ======================================================================
    def apply_shake_effect(self, input_path: str, output_path: str, intensity: int = 5, duration: float = 3.0) -> bool:
        """
        应用轻微震动 / 摇摆效果，模拟不稳定拍摄
        :param intensity: 摇摆强度（像素偏移量）
        :param duration: 持续时间（秒）
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f"x='iw/2+W*sin(t*10)*{intensity}':y='ih/2+H*sin(t*8)*{intensity}'",
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ======================================================================
    #  动画效果扩展
    # 【18】缩放呼吸效果（周期性放大缩小）
    # ======================================================================
    def apply_breathing_scale_effect(self, input_path: str, output_path: str, duration: float = 4.0,
                                     scale_range: Tuple[float, float] = (1.0, 1.3)) -> bool:
        """
        视频周期性放大缩小，产生呼吸感
        :param scale_range: 最小/最大缩放比，如 (1.0, 1.3)
        :param duration: 周期时间（秒）
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf',
            f"scale=iw*{scale_range[0]}:ih*{scale_range[0]}:enable='between(t,0,{duration})',scale=iw*{scale_range[1]}:ih*{scale_range[1]}:enable='between(t,{duration / 2},{duration})'",
            safe_output
        ]
        return self._run_ffmpeg(cmd)


    # ======================================================================
    #  补充方法
    # 【19】merge_videos() → 合并多个视频
    # =====================================================================
    def merge_videos(self, video_paths: list, output_path: str) -> bool:
        """
        合并多个视频为一个视频（按顺序拼接，适用于相同分辨率/编码格式的视频）
        :param video_paths: 视频路径列表，如 [cat_01.mp4, cat_02.mp4]
        :param output_path: 合并后的输出路径，如 outputs/merged.mp4
        :return: 是否成功
        """
        if not video_paths or len(video_paths) < 2:
            print("[⚠️] 至少需要提供两个视频文件用于合并")
            return False

        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))

        # 创建临时文本文件，用于 ffmpeg concat 分离器（适用于相同编码视频）
        list_file = os.path.join(os.path.dirname(safe_output), "file_list.txt")
        try:
            with open(list_file, 'w', encoding='utf-8') as f:
                for path in video_paths:
                    f.write(f"file '{os.path.abspath(path)}'\n")
        except Exception as e:
            print(f"[❌ 创建视频列表文件失败：{e}]")
            return False

        # 使用 concat 分离器进行视频合并（最快最稳定，要求视频参数一致）
        cmd = [
            '-f', 'concat',
            '-safe', '0',
            '-i', list_file,
            '-c', 'copy',  # 直接拷贝流，不重新编码，速度最快
            safe_output
        ]

        success = self._run_ffmpeg(cmd)

        # 清理临时文件
        if os.path.exists(list_file):
            try:
                os.remove(list_file)
            except:
                pass

        return success

    # ======================================================================
    #  补充方法
    # 【20】apply_dynamic_effect() → 对视频应用动态效果（如平移、缩放、动画）
    # =====================================================================
    def apply_dynamic_effect(self, input_path: str, output_path: str, effect_type: str = "translate",
                             direction: str = "right", duration: float = 2.0) -> bool:
        """
        对视频应用某种动态效果，如平移、缩放、旋转等（简单动画效果）
        :param input_path: 输入视频路径
        :param output_path: 输出视频路径
        :param effect_type: 效果类型，如 "translate"（平移）、"scale"（缩放）、"rotate"（旋转）
        :param direction: 方向，如 "right"（右）、"left"、"up"、"down"（部分效果支持）
        :param duration: 动画持续时间（秒）。注意：本实现为简单演示，不控制精确时长，而是整体滤镜效果
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))

        if effect_type == "translate":
            # 简单平移动画：从左到右移动（可通过 x 表达式控制）
            x_expr = "t*50"  # 每秒向右移动 50 像素
            filter_str = f"overlay=x='{x_expr}':y=0"  # 在原始画面上叠加移动图层
            # 注意：为了实现“自身平移”，我们复制原视频流并移动其中一个
            cmd = [
                '-i', input_path,
                '-filter_complex', f'[0:v]setpts=PTS-STARTPTS,split=2[v1][v2];'
                                   f'[v1]copy[v1copy];'
                                   f'[v2]crop=iw:ih:0:0,setsar=1,translate=x=t*50[v2move];'
                                   f'[v1copy][v2move]overlay=shortest=1',
                safe_output
            ]
        elif effect_type == "scale":
            # 简单缩放动画：放大或缩小（示例：从 1.0 到 1.2 倍）
            filter_str = "scale=iw*1.2:ih*1.2"  # 固定放大
            cmd = [
                '-i', input_path,
                '-vf', filter_str,
                safe_output
            ]
        elif effect_type == "rotate":
            # 简单旋转（顺时针 5 度）
            filter_str = "rotate=5*PI/180"  # 5度
            cmd = [
                '-i', input_path,
                '-vf', filter_str,
                safe_output
            ]
        else:
            # 默认无效果
            cmd = [
                '-i', input_path,
                safe_output
            ]

        return self._run_ffmpeg(cmd)
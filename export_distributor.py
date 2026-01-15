# export_distributor.py
import os
import subprocess
from typing import Optional, Dict
from utils import get_output_filepath


class ExportDistributor:
    def __init__(self, ffmpeg_cmd: str = "ffmpeg"):
        """
        初始化导出分发器
        :param ffmpeg_cmd: ffmpeg 命令名称，默认为 'ffmpeg'
        """
        self.ffmpeg = ffmpeg_cmd

    def _run_ffmpeg(self, cmd_args: list) -> bool:
        """
        执行 ffmpeg 命令
        :param cmd_args: 参数列表，如 ['-i', 'input.mp4', '-vf', ..., 'output.mp4']
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
            print(f"[❌ 导出失败，命令：{' '.join(full_cmd)}]")
            print(f"[错误详情]: {e.stderr.decode('utf-8', errors='ignore')}")
            return False
        except Exception as e:
            print(f"[❌ 未知错误: {e}]")
            return False

    # ----------------------------------------------------------------------
    # 【1】导出为通用高质量 MP4（适合大部分平台）
    # ----------------------------------------------------------------------
    def export_for_general_use(self, input_path: str, output_path: str, resolution: str = "1080:1920", bitrate: str = "5M") -> bool:
        """
        导出为通用高质量的 MP4 视频，适用于大多数平台
        :param resolution: 分辨率，格式为 "宽:高"，如 "1080:1920"（竖屏）、"1920:1080"（横屏）
        :param bitrate: 视频码率，如 "5M"（5 Mbps）
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f'scale={resolution.replace(":", ":")}',  # 注意传入的是 "宽:高"
            '-c:v', 'libx264',
            '-b:v', bitrate,
            '-preset', 'slow',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-movflags', '+faststart',  # 适合网络流式播放
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【2】导出为抖音推荐格式
    # ----------------------------------------------------------------------
    def export_for_douyin(self, input_path: str, output_path: str) -> bool:
        """
        导出为抖音推荐的视频格式：竖屏 1080x1920，高画质
        :return: 是否成功
        """
        return self.export_for_platform(input_path, output_path, resolution="1080:1920", bitrate="8M", fps=30)

    # ----------------------------------------------------------------------
    # 【3】导出为小红书推荐格式
    # ----------------------------------------------------------------------
    def export_for_xiaohongshu(self, input_path: str, output_path: str) -> bool:
        """
        导出为小红书推荐的视频格式：竖屏 1080x1920，高画质，适合种草与展示
        :return: 是否成功
        """
        return self.export_for_platform(input_path, output_path, resolution="1080:1920", bitrate="6M", fps=30)

    # ----------------------------------------------------------------------
    # 【4】导出为视频号（微信视频号）推荐格式
    # ----------------------------------------------------------------------
    def export_for_wechat_video(self, input_path: str, output_path: str) -> bool:
        """
        导出为微信视频号推荐格式：竖屏或横屏 1080x1920 或 1920x1080，高画质
        :return: 是否成功
        """
        return self.export_for_platform(input_path, output_path, resolution="1080:1920", bitrate="6M", fps=30)

    # ----------------------------------------------------------------------
    # 【5】导出为 B 站推荐格式
    # ----------------------------------------------------------------------
    def export_for_bilibili(self, input_path: str, output_path: str) -> bool:
        """
        导出为 B 站推荐格式：横屏 1920x1080，高码率，适合高清观看
        :return: 是否成功
        """
        return self.export_for_platform(input_path, output_path, resolution="1920:1080", bitrate="8M", fps=30)

    # ----------------------------------------------------------------------
    # 【6】导出为 YouTube 推荐格式
    # ----------------------------------------------------------------------
    def export_for_youtube(self, input_path: str, output_path: str) -> bool:
        """
        导出为 YouTube 推荐格式：横屏 1920x1080 或 3840x2160，高码率，适合 1080p / 4K 上传
        :return: 是否成功
        """
        return self.export_for_platform(input_path, output_path, resolution="1920:1080", bitrate="12M", fps=30)

    # ----------------------------------------------------------------------
    # 【内部方法】通用平台导出（可扩展）
    # ----------------------------------------------------------------------
    def export_for_platform(self, input_path: str, output_path: str, resolution: str, bitrate: str, fps: int = 30) -> bool:
        """
        通用导出方法，用于各平台定制
        :param resolution: 如 "1920:1080"
        :param bitrate: 如 "8M"
        :param fps: 帧率，如 30
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f'scale={resolution}',
            '-r', str(fps),
            '-c:v', 'libx264',
            '-b:v', bitrate,
            '-preset', 'slow',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-movflags', '+faststart',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【7】自定义导出（用户手动控制所有导出参数）
    # ----------------------------------------------------------------------
    def export_custom(self, input_path: str, output_path: str,
                      video_codec: str = 'libx264',
                      video_bitrate: str = '5M',
                      audio_codec: str = 'aac',
                      audio_bitrate: str = '192k',
                      resolution: Optional[str] = None,
                      fps: Optional[int] = None,
                      optimize: bool = True) -> bool:
        """
        完全自定义导出参数，用户可控制分辨率、码率、帧率、编码器等
        :param input_path: 输入视频路径
        :param output_path: 输出视频路径
        :param video_codec: 视频编码器，如 libx264（H.264）、libx265（H.265）
        :param video_bitrate: 视频码率，如 '5M', '8M'
        :param audio_codec: 音频编码器，如 aac
        :param audio_bitrate: 音频码率，如 '192k'
        :param resolution: 分辨率，如 '1920:1080' 或 '1080:1920'（宽:高）
        :param fps: 帧率，如 30、60
        :param optimize: 是否优化（添加 -movflags +faststart，适合网络播放）
        :return: 是否成功
        """
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = ['-i', input_path, '-c:v', video_codec, '-b:v', video_bitrate, '-c:a', audio_codec, '-b:a', audio_bitrate]

        if resolution:
            cmd.extend(['-vf', f'scale={resolution}'])  # 缩放至指定分辨率
        if fps:
            cmd.extend(['-r', str(fps)])  # 设置帧率

        if optimize:
            cmd.append('-movflags')
            cmd.append('+faststart')  # 优化网络加载

        cmd.append(safe_output)
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【8】自动调整视频参数（根据目标平台或内容类型智能选择）
    # ----------------------------------------------------------------------
    def auto_adjust_parameters(self, target_platform: Optional[str] = None, video_type: Optional[str] = None) -> Dict[
        str, str]:
        """
        根据目标平台或视频类型，自动返回推荐的分辨率、码率、帧率等参数
        :param target_platform: 目标平台，如 "douyin", "xiaohongshu", "bilibili", "youtube"
        :param video_type: 视频类型，如 "vertical"（竖屏）、"horizontal"（横屏）、"square"（方屏）
        :return: 参数字典，包含 resolution, bitrate, fps
        """
        # 默认参数（通用竖屏短视频）
        params = {
            "resolution": "1080:1920",  # 竖屏 1080x1920
            "bitrate": "6M",  # 视频码率
            "fps": 30  # 帧率
        }

        if target_platform:
            target_platform = target_platform.lower()
            if target_platform == "douyin":
                params = {"resolution": "1080:1920", "bitrate": "8M", "fps": 30}
            elif target_platform == "xiaohongshu":
                params = {"resolution": "1080:1920", "bitrate": "6M", "fps": 30}
            elif target_platform == "bilibili":
                params = {"resolution": "1920:1080", "bitrate": "8M", "fps": 30}
            elif target_platform == "youtube":
                params = {"resolution": "1920:1080", "bitrate": "12M", "fps": 30}

        if video_type == "horizontal":
            params["resolution"] = "1920:1080"
        elif video_type == "square":
            params["resolution"] = "1080:1080"

        return params

    # ----------------------------------------------------------------------
    # 【9】导出视频（使用自动调整的分辨率、码率、帧率）
    # ----------------------------------------------------------------------
    def export_with_auto_settings(self, input_path: str, output_path: str, target_platform: Optional[str] = None,
                                  video_type: Optional[str] = None) -> bool:
        """
        自动根据目标平台或视频类型调整参数并导出视频
        :param target_platform: 如 "douyin", "youtube"
        :param video_type: 如 "vertical", "horizontal"
        :return: 是否成功
        """
        params = self.auto_adjust_parameters(target_platform, video_type)
        safe_output = get_output_filepath(os.path.dirname(output_path), os.path.basename(output_path))
        cmd = [
            '-i', input_path,
            '-vf', f'scale={params["resolution"]}',
            '-r', str(params["fps"]),
            '-c:v', 'libx264',
            '-b:v', params["bitrate"],
            '-preset', 'slow',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-movflags', '+faststart',
            safe_output
        ]
        return self._run_ffmpeg(cmd)

    # ----------------------------------------------------------------------
    # 【10】获取指定平台的完整预设配置（可扩展为 JSON / 配置文件）
    # ----------------------------------------------------------------------
    def get_platform_preset(self, platform: str) -> Optional[Dict[str, str]]:
        """
        获取某个平台的完整推荐导出参数（字典形式，可被 UI 或高级逻辑使用）
        :param platform: 平台名称，如 "douyin", "bilibili"
        :return: dict 如 {"resolution": "1080:1920", "bitrate": "8M", "fps": 30} 或 None
        """
        platform = platform.lower()
        presets = {
            "douyin": {"resolution": "1080:1920", "bitrate": "8M", "fps": 30},
            "xiaohongshu": {"resolution": "1080:1920", "bitrate": "6M", "fps": 30},
            "wechat_video": {"resolution": "1080:1920", "bitrate": "6M", "fps": 30},
            "bilibili": {"resolution": "1920:1080", "bitrate": "8M", "fps": 30},
            "youtube": {"resolution": "1920:1080", "bitrate": "12M", "fps": 30},
        }
        return presets.get(platform)


    # ----------------------------------------------------------------------
    # 【11】输出优化建议（辅助函数，提供专业导出参数推荐）
    # ----------------------------------------------------------------------
    def get_export_optimization_guide(self) -> str:
        """
        返回一份详细的「视频导出优化建议」，供用户参考如何选择最佳导出参数，
        适配不同平台与用途，提升视频质量与上传兼容性。
        :return: 格式化文本，包含分辨率、码率、帧率、编码器等推荐
        """
        guide = """
    🎬 【视频导出优化建议指南】🎬

    🔧 一、通用推荐（适用于大多数短视频平台，如抖音、小红书、B站、YouTube 等）

        • 📽️ 格式：MP4（H.264 视频编码 + AAC 音频编码）
                  → 兼容性最好，文件较小，加载快

        • 🎞️ 视频编码器：libx264（H.264）
                  → 平衡兼容性与压缩效率，推荐绝大多数场景使用
                  → 如需更高压缩率且不急，可尝试 libx265（H.265），但编码慢且兼容略差

        • 🔊 音频编码器：aac
                  → 标准音频编码，推荐码率 192k，音质与体积兼顾

        • 📐 分辨率推荐：
              – 竖屏（适合抖音、小红书、快手等）：1080x1920（宽x高）
              – 横屏（适合 B站、YouTube、影视类）：1920x1080
              – 方屏（Instagram 正方形等）：1080x1080

        • 🎥 帧率（FPS）推荐：
              – 一般内容：30fps（足够流畅，文件小）
              – 高动态 / 游戏 / 运动：60fps（更流畅，但文件更大）

        • 📦 码率推荐（视频）：
              – 竖屏 1080x1920：5M ~ 8M（高清，推荐 6M~8M）
              – 横屏 1920x1080：6M ~ 10M
              – 4K（3840x2160）：12M ~ 20M

        • 🎵 音频码率：192k（平衡清晰与体积）

        • ✅ 优化提示：添加 -movflags +faststart，可使 MP4 支持流式加载（适合网页/上传）

    🔧 二、按平台推荐（简要）

        • 抖音：竖屏 1080x1920，码率 8M，30fps，MP4 + H.264 + AAC
        • 小红书：竖屏 1080x1920，码率 6M~8M，30fps
        • 视频号（微信）：竖屏/横屏 1080x1920 或 1920x1080，码率 6M~8M
        • B站：横屏 1920x1080，推荐 8M~12M，支持 4K
        • YouTube：横屏 1920x1080 或 3840x2160，推荐 12M~20M（4K）

    🔧 三、其他建议
        • 导出前检查视频是否有黑边、音画是否同步
        • 适当压缩体积以提升加载速度，但不要过度牺牲清晰度
        • 使用 -crf 23（默认平衡质量与体积，值越小质量越高，文件越大）
        • 推荐使用 slow preset（编码质量更好，速度稍慢）

    ——————————————————————————————
    💡 提示：以上参数可根据实际内容类型（如 vlog、教程、带货、动画）微调。
        """
        return guide

    # ----------------------------------------------------------------------
    # 【12】一键校验视频是否符合平台技术要求（分辨率、码率、帧率、格式等）
    # ----------------------------------------------------------------------
    def validate_for_platform(self, input_path: str, platform: str) -> dict:
        """
        校验给定视频文件是否符合某个短视频平台的推荐技术参数
        （基于平台官方推荐，校验分辨率、帧率、格式等，返回详细报告）
        :param input_path: 待校验的视频文件路径
        :param platform: 平台名称，如 "douyin", "xiaohongshu", "bilibili", "youtube"
        :return: dict，包含是否通过、详细参数与提示信息
        """
        import subprocess

        # 平台推荐配置（简化校验维度：分辨率、帧率、格式）
        platform_standards = {
            "douyin": {
                "expected_resolution": "1080:1920",  # 竖屏
                "expected_fps": 30,
                "expected_format": "mp4",
                "max_video_bitrate": "8M",
                "tips": "抖音推荐竖屏 1080x1920，30fps，码率 8M 内，MP4 格式"
            },
            "xiaohongshu": {
                "expected_resolution": "1080:1920",
                "expected_fps": 30,
                "expected_format": "mp4",
                "max_video_bitrate": "6M",
                "tips": "小红书推荐竖屏 1080x1920，30fps，码率 6M 左右，MP4"
            },
            "bilibili": {
                "expected_resolution": "1920:1080",
                "expected_fps": 30,
                "expected_format": "mp4",
                "max_video_bitrate": "10M",
                "tips": "B站推荐横屏 1920x1080，30fps，码率建议 8M~10M，支持 4K"
            },
            "youtube": {
                "expected_resolution": "1920:1080",
                "expected_fps": 30,
                "expected_format": "mp4",
                "max_video_bitrate": "12M",
                "tips": "YouTube 推荐横屏 1920x1080 或 3840x2160，30fps~60fps，码率 12M+（4K需更高）"
            }
        }

        # 默认返回结构
        result = {
            "platform": platform,
            "passed": False,
            "details": {},
            "message": "",
            "recommendation": ""
        }

        # 检查平台是否存在
        platform = platform.lower()
        if platform not in platform_standards:
            result["message"] = f"未找到平台 '{platform}' 的校验标准"
            return result

        standard = platform_standards[platform]
        expected_res = standard["expected_resolution"]
        expected_fps = standard["expected_fps"]
        expected_fmt = standard["expected_format"]
        max_bitrate = standard["max_video_bitrate"]
        tips = standard["tips"]

        # ---- Step 1: 获取视频信息（通过 ffprobe，解析分辨率 / 帧率 / 格式等）
        try:
            # 获取视频基本信息
            cmd_probe = [
                'ffprobe', '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height,r_frame_rate,codec_name',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                input_path
            ]
            probe_output = subprocess.check_output(cmd_probe, stderr=subprocess.STDOUT, text=True).strip().split('\n')

            if len(probe_output) < 4:
                result["message"] = "无法解析视频信息，请检查文件是否为有效视频"
                return result

            width = int(probe_output[0])
            height = int(probe_output[1])
            framerate_str = probe_output[2]  # 如 "30/1"
            codec = probe_output[3].lower()

            # 计算实际帧率（处理 r_frame_rate = "30/1" -> 30.0）
            try:
                num, den = map(int, framerate_str.split('/'))
                actual_fps = round(num / den)
            except:
                actual_fps = 30  # 默认假设

            resolution = f"{width}:{height}"
            actual_format = os.path.splitext(input_path)[1][1:].lower()  # .mp4 -> mp4

            # 构造结果详情
            result["details"] = {
                "实际分辨率": resolution,
                "预期分辨率": expected_res,
                "实际帧率": actual_fps,
                "预期帧率": expected_fps,
                "实际格式": actual_format,
                "预期格式": expected_fmt,
                "视频编码器": codec,
                "平台推荐": tips
            }

            # 校验逻辑
            passed = True
            messages = []

            if resolution != expected_res:
                passed = False
                messages.append(f"⚠️ 分辨率不符：当前 {resolution}，推荐 {expected_res}")

            if actual_fps != expected_fps:
                passed = False
                messages.append(f"⚠️ 帧率不符：当前 {actual_fps}，推荐 {expected_fps}")

            if actual_format != expected_fmt:
                passed = False
                messages.append(f"⚠️ 格式不符：当前 {actual_format}，推荐 {expected_fmt}（建议导出为 MP4）")

            # 注：码率校验需要 ffprobe 视频流 bit_rate，这里暂未实现（可后续扩展）

            result["passed"] = passed
            result["message"] = "✅ 通过" if passed else "❌ 未通过"
            result["recommendation"] = tips if not passed else "请根据上述提示调整参数后重新导出"

            if messages:
                result["details"]["不匹配项"] = messages

        except Exception as e:
            result["message"] = f"校验失败：{str(e)}"
            result["details"]["错误"] = str(e)

        return result
# test_export_distributor.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from export_distributor import ExportDistributor

def test_export_distributor():
    print("📤" + " " * 10 + "开始测试 ExportDistributor ..." + " " * 10 + "📤")
    distributor = ExportDistributor()
    input_video = os.path.join("inputs", "cat_01.mp4")
    output_general = os.path.join("outputs", "test_general.mp4")
    output_douyin = os.path.join("outputs", "test_douyin.mp4")
    output_xiaohongshu = os.path.join("outputs", "test_xiaohongshu.mp4")
    output_wechat = os.path.join("outputs", "test_wechat.mp4")
    output_bilibili = os.path.join("outputs", "test_bilibili.mp4")
    output_youtube = os.path.join("outputs", "test_youtube.mp4")
    output_custom = os.path.join("outputs", "test_custom.mp4")

    os.makedirs("outputs", exist_ok=True)

    # 测试1: 导出为通用高质量 MP4
    print("🔹 测试导出为通用高质量 MP4 (1080:1920, 5M)")
    if distributor.export_for_general_use(input_video, output_general, resolution="1080:1920", bitrate="5M"):
        print("✅ 通用导出成功！输出文件: " + output_general)
    else:
        print("❌ 通用导出失败！")

    # 测试2: 导出为抖音推荐格式
    print("🔹 测试导出为抖音推荐格式 (1080:1920, 8M)")
    if distributor.export_for_douyin(input_video, output_douyin):
        print("✅ 抖音导出成功！输出文件: " + output_douyin)
    else:
        print("❌ 抖音导出失败！")

    # 测试3: 导出为小红书推荐格式
    print("🔹 测试导出为小红书推荐格式 (1080:1920, 6M)")
    if distributor.export_for_xiaohongshu(input_video, output_xiaohongshu):
        print("✅ 小红书导出成功！输出文件: " + output_xiaohongshu)
    else:
        print("❌ 小红书导出失败！")

    # 测试4: 导出为微信视频号推荐格式
    print("🔹 测试导出为微信视频号推荐格式 (1080:1920, 6M)")
    if distributor.export_for_wechat_video(input_video, output_wechat):
        print("✅ 微信视频号导出成功！输出文件: " + output_wechat)
    else:
        print("❌ 微信视频号导出失败！")

    # 测试5: 导出为 B 站推荐格式
    print("🔹 测试导出为 B 站推荐格式 (1920:1080, 8M)")
    if distributor.export_for_bilibili(input_video, output_bilibili):
        print("✅ B站导出成功！输出文件: " + output_bilibili)
    else:
        print("❌ B站导出失败！")

    # 测试6: 导出为 YouTube 推荐格式
    print("🔹 测试导出为 YouTube 推荐格式 (1920:1080, 12M)")
    if distributor.export_for_youtube(input_video, output_youtube):
        print("✅ YouTube导出成功！输出文件: " + output_youtube)
    else:
        print("❌ YouTube导出失败！")

    # 测试7: 自定义导出
    print("🔹 测试自定义导出: 视频编码器=libx264, 码率=6M, 音频编码器=aac, 码率=192k, 分辨率=1920:1080, 帧率=30")
    if distributor.export_custom(
        input_video,
        output_custom,
        video_codec='libx264',
        video_bitrate='6M',
        audio_codec='aac',
        audio_bitrate='192k',
        resolution='1920:1080',
        fps=30
    ):
        print("✅ 自定义导出成功！输出文件: " + output_custom)
    else:
        print("❌ 自定义导出失败！")

    print("📤" + " " * 8 + "ExportDistributor 测试完成。" + " " * 8 + "📤\n")

if __name__ == "__main__":
    test_export_distributor()
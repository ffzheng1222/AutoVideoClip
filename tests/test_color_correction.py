# test_color_correction.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from color_correction import ColorCorrection

def test_color_correction():
    print("🎨" + " " * 10 + "开始测试 ColorCorrection ..." + " " * 10 + "🎨")
    corrector = ColorCorrection()
    input_video = os.path.join("inputs", "cat_01.mp4")
    output_brightness = os.path.join("outputs", "test_brightness.mp4")
    output_contrast = os.path.join("outputs", "test_contrast.mp4")
    output_saturation = os.path.join("outputs", "test_saturation.mp4")
    output_cinematic = os.path.join("outputs", "test_cinematic.mp4")
    output_vintage = os.path.join("outputs", "test_vintage.mp4")
    output_cool = os.path.join("outputs", "test_cool.mp4")
    output_grayscale = os.path.join("outputs", "test_grayscale.mp4")
    output_sharpen = os.path.join("outputs", "test_sharpen.mp4")
    output_hue_shift = os.path.join("outputs", "test_hue_shift.mp4")
    output_lift_shadows = os.path.join("outputs", "test_lift_shadows.mp4")
    output_reduce_highlights = os.path.join("outputs", "test_reduce_highlights.mp4")
    output_denoise = os.path.join("outputs", "test_denoise.mp4")
    output_soft_focus = os.path.join("outputs", "test_soft_focus.mp4")
    output_rgb_split = os.path.join("outputs", "test_rgb_split.mp4")
    output_preset_douyin = os.path.join("outputs", "test_preset_douyin.mp4")
    output_preset_cyberpunk = os.path.join("outputs", "test_preset_cyberpunk.mp4")
    output_preset_fresh = os.path.join("outputs", "test_preset_fresh.mp4")

    os.makedirs("outputs", exist_ok=True)

    # 测试1: 调整亮度
    print("🔹 测试调整亮度 (偏移 +0.1)")
    if corrector.adjust_brightness(input_video, output_brightness, brightness=0.1):
        print("✅ 亮度调整成功！输出文件: " + output_brightness)
    else:
        print("❌ 亮度调整失败！")

    # 测试2: 调整对比度
    print("🔹 测试调整对比度 (倍数 1.2)")
    if corrector.adjust_contrast(input_video, output_contrast, contrast=1.2):
        print("✅ 对比度调整成功！输出文件: " + output_contrast)
    else:
        print("❌ 对比度调整失败！")

    # 测试3: 调整饱和度
    print("🔹 测试调整饱和度 (倍数 1.5)")
    if corrector.adjust_saturation(input_video, output_saturation, saturation=1.5):
        print("✅ 饱和度调整成功！输出文件: " + output_saturation)
    else:
        print("❌ 饱和度调整失败！")

    # 测试4: 应用电影感色彩分级
    print("🔹 测试应用电影感色彩分级")
    if corrector.apply_cinematic_look(input_video, output_cinematic):
        print("✅ 电影感色彩分级成功！输出文件: " + output_cinematic)
    else:
        print("❌ 电影感色彩分级失败！")

    # # 测试5: 应用复古色调
    # print("🔹 测试应用复古色调")
    # if corrector.apply_vintage_look(input_video, output_vintage):
    #     print("✅ 复古色调成功！输出文件: " + output_vintage)
    # else:
    #     print("❌ 复古色调失败！")

    # 测试6: 应用冷色调
    print("🔹 测试应用冷色调")
    if corrector.apply_cool_look(input_video, output_cool):
        print("✅ 冷色调成功！输出文件: " + output_cool)
    else:
        print("❌ 冷色调失败！")

    # 测试7: 应用黑白（去饱和度）
    print("🔹 测试应用黑白（去饱和度）")
    if corrector.apply_grayscale(input_video, output_grayscale):
        print("✅ 黑白效果成功！输出文件: " + output_grayscale)
    else:
        print("❌ 黑白效果失败！")

    # 测试8: 应用锐化
    print("🔹 测试应用锐化")
    if corrector.apply_sharpen(input_video, output_sharpen):
        print("✅ 锐化成功！输出文件: " + output_sharpen)
    else:
        print("❌ 锐化失败！")

    # 测试9: 应用色相偏移
    print("🔹 测试应用色相偏移 (偏移角度 30.0)")
    if corrector.apply_hue_shift(input_video, output_hue_shift, hue_angle=30.0):
        print("✅ 色相偏移成功！输出文件: " + output_hue_shift)
    else:
        print("❌ 色相偏移失败！")

    # 测试10: 提升阴影区域亮度
    print("🔹 测试提升阴影区域亮度 (偏移 +0.1)")
    if corrector.lift_shadows(input_video, output_lift_shadows, brightness=0.1):
        print("✅ 阴影提亮成功！输出文件: " + output_lift_shadows)
    else:
        print("❌ 阴影提亮失败！")

    # 测试11: 压暗高光区域
    print("🔹 测试压暗高光区域 (gamma 提升 1.2)")
    if corrector.reduce_highlights(input_video, output_reduce_highlights, gamma_reduction=1.2):
        print("✅ 高光抑制成功！输出文件: " + output_reduce_highlights)
    else:
        print("❌ 高光抑制失败！")

    # 测试12: 应用简单降噪
    print("🔹 测试应用简单降噪")
    if corrector.apply_denoise(input_video, output_denoise):
        print("✅ 降噪成功！输出文件: " + output_denoise)
    else:
        print("❌ 降噪失败！")

    # 测试13: 应用柔焦效果
    print("🔹 测试应用柔焦效果 (强度 2.0)")
    if corrector.apply_soft_focus(input_video, output_soft_focus, strength=2.0):
        print("✅ 柔焦效果成功！输出文件: " + output_soft_focus)
    else:
        print("❌ 柔焦效果失败！")

    # 测试14: 应用 RGB 色彩分离效果
    print("🔹 测试应用 RGB 色彩分离效果 (偏移 2.0)")
    if corrector.apply_rgb_split(input_video, output_rgb_split, offset=2.0):
        print("✅ RGB 分离效果成功！输出文件: " + output_rgb_split)
    else:
        print("❌ RGB 分离效果失败！")

    # 测试15: 应用预设风格 - 抖音
    print("🔹 测试应用预设风格 - 抖音")
    if corrector.apply_preset_style(input_video, output_preset_douyin, style="douyin"):
        print("✅ 抖音预设风格成功！输出文件: " + output_preset_douyin)
    else:
        print("❌ 抖音预设风格失败！")

    # 测试16: 应用预设风格 - 赛博朋克
    print("🔹 测试应用预设风格 - 赛博朋克")
    if corrector.apply_preset_style(input_video, output_preset_cyberpunk, style="cyberpunk"):
        print("✅ 赛博朋克预设风格成功！输出文件: " + output_preset_cyberpunk)
    else:
        print("❌ 赛博朋克预设风格失败！")

    # 测试17: 应用预设风格 - 清新
    print("🔹 测试应用预设风格 - 清新")
    if corrector.apply_preset_style(input_video, output_preset_fresh, style="fresh"):
        print("✅ 清新预设风格成功！输出文件: " + output_preset_fresh)
    else:
        print("❌ 清新预设风格失败！")

    print("🎨" + " " * 8 + "ColorCorrection 测试完成。" + " " * 8 + "🎨\n")

if __name__ == "__main__":
    test_color_correction()
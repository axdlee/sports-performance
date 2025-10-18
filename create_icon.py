#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成应用图标脚本
使用 Pillow 生成一个现代化的体育主题图标
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_base_icon(size=1024):
    """创建基础图标"""
    # 创建画布
    img = Image.new('RGB', (size, size), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # 绘制渐变背景
    for i in range(size):
        # 从深蓝到浅蓝的渐变
        r = int(46 + (135 - 46) * i / size)
        g = int(134 + (206 - 134) * i / size)
        b = int(171 + (235 - 171) * i / size)
        draw.rectangle([0, i, size, i+1], fill=(r, g, b))
    
    # 绘制圆形边框
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 outline='#FFFFFF', width=size//40)
    
    # 绘制跑步人物轮廓（简化版）
    center_x = size // 2
    center_y = size // 2
    
    # 头部
    head_size = size // 8
    draw.ellipse([center_x - head_size//2, center_y - size//4 - head_size//2,
                  center_x + head_size//2, center_y - size//4 + head_size//2],
                 fill='#FFFFFF')
    
    # 身体（使用多边形绘制跑步姿势）
    body_points = [
        (center_x, center_y - size//6),  # 颈部
        (center_x - size//10, center_y),  # 左肩
        (center_x - size//6, center_y + size//8),  # 左手
        (center_x, center_y + size//12),  # 腰部
        (center_x + size//8, center_y + size//6),  # 右腿
        (center_x, center_y + size//5),  # 右脚
        (center_x - size//12, center_y + size//8),  # 左腿起点
        (center_x - size//6, center_y + size//4),  # 左脚
    ]
    
    # 绘制身体轮廓
    draw.line([(center_x, center_y - size//6), (center_x, center_y + size//12)], 
              fill='#FFFFFF', width=size//35)  # 躯干
    
    # 左臂
    draw.line([(center_x, center_y - size//8), (center_x - size//6, center_y + size//12)], 
              fill='#FFFFFF', width=size//40)
    
    # 右臂
    draw.line([(center_x, center_y - size//8), (center_x + size//8, center_y)], 
              fill='#FFFFFF', width=size//40)
    
    # 左腿
    draw.line([(center_x, center_y + size//12), (center_x - size//10, center_y + size//4)], 
              fill='#FFFFFF', width=size//40)
    
    # 右腿
    draw.line([(center_x, center_y + size//12), (center_x + size//8, center_y + size//5)], 
              fill='#FFFFFF', width=size//40)
    
    # 绘制速度线条
    for i in range(3):
        y_offset = center_y - size//6 + i * size//12
        draw.line([(center_x + size//4, y_offset), (center_x + size//3, y_offset)], 
                  fill='#FFFFFF', width=size//60)
    
    # 添加底部文字 "PE" (Physical Education)
    try:
        # 尝试使用系统字体
        font_size = size // 6
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            try:
                font = ImageFont.truetype("/Library/Fonts/Arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        text = "PE"
        # 使用 textbbox 代替 textsize
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        text_x = (size - text_width) // 2
        text_y = size - margin - text_height - size//20
        
        # 绘制文字阴影
        draw.text((text_x+3, text_y+3), text, fill='#1E5F8C', font=font)
        # 绘制文字
        draw.text((text_x, text_y), text, fill='#FFFFFF', font=font)
    except Exception as e:
        print(f"绘制文字时出错: {e}")
    
    return img


def save_icon_sizes(base_img, base_path, sizes):
    """保存不同尺寸的图标"""
    for size in sizes:
        img = base_img.resize((size, size), Image.Resampling.LANCZOS)
        filename = f"{base_path}_{size}x{size}.png"
        img.save(filename, 'PNG')
        print(f"✓ 生成 {filename}")
    return True


def create_macos_iconset():
    """创建 macOS iconset"""
    print("\n生成 macOS 图标...")
    
    # 创建基础图标
    base_img = create_base_icon(1024)
    
    # iconset 目录
    iconset_dir = "assets/AppIcon.iconset"
    os.makedirs(iconset_dir, exist_ok=True)
    
    # macOS 需要的尺寸
    sizes = [
        (16, "icon_16x16"),
        (32, "icon_16x16@2x"),
        (32, "icon_32x32"),
        (64, "icon_32x32@2x"),
        (128, "icon_128x128"),
        (256, "icon_128x128@2x"),
        (256, "icon_256x256"),
        (512, "icon_256x256@2x"),
        (512, "icon_512x512"),
        (1024, "icon_512x512@2x"),
    ]
    
    for size, name in sizes:
        img = base_img.resize((size, size), Image.Resampling.LANCZOS)
        img.save(f"{iconset_dir}/{name}.png", 'PNG')
        print(f"✓ 生成 {name}.png")
    
    # 尝试创建 .icns 文件
    print("\n尝试创建 .icns 文件...")
    try:
        import subprocess
        result = subprocess.run(
            ["iconutil", "-c", "icns", iconset_dir, "-o", "assets/icon.icns"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓ 成功创建 icon.icns")
        else:
            print(f"✗ iconutil 失败: {result.stderr}")
            print("  提示: 手动运行: iconutil -c icns assets/AppIcon.iconset -o assets/icon.icns")
    except FileNotFoundError:
        print("✗ iconutil 未找到（仅在 macOS 上可用）")
        print("  提示: 手动运行: iconutil -c icns assets/AppIcon.iconset -o assets/icon.icns")


def create_windows_icon():
    """创建 Windows 图标"""
    print("\n生成 Windows 图标...")
    
    base_img = create_base_icon(1024)
    
    # Windows ICO 需要多个尺寸
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    for size in sizes:
        img = base_img.resize((size, size), Image.Resampling.LANCZOS)
        images.append(img)
        print(f"✓ 准备 {size}x{size} 图标")
    
    # 保存为 ICO
    try:
        images[0].save(
            'assets/icon.ico',
            format='ICO',
            sizes=[(img.width, img.height) for img in images],
            append_images=images[1:]
        )
        print("✓ 成功创建 icon.ico")
    except Exception as e:
        print(f"✗ 创建 ICO 失败: {e}")
        print("  回退: 保存为 256x256 PNG")
        base_img.resize((256, 256), Image.Resampling.LANCZOS).save('assets/icon.png', 'PNG')


def create_general_icons():
    """创建通用图标（PNG格式）"""
    print("\n生成通用图标...")
    
    base_img = create_base_icon(1024)
    
    # 保存多个常用尺寸
    sizes = [16, 32, 48, 64, 128, 256, 512, 1024]
    for size in sizes:
        img = base_img.resize((size, size), Image.Resampling.LANCZOS)
        img.save(f'assets/icon_{size}x{size}.png', 'PNG')
        print(f"✓ 生成 icon_{size}x{size}.png")


def main():
    """主函数"""
    print("=" * 60)
    print("  体育成绩评估系统 - 图标生成工具")
    print("=" * 60)
    
    # 确保 assets 目录存在
    os.makedirs("assets", exist_ok=True)
    
    # 生成各平台图标
    create_macos_iconset()
    create_windows_icon()
    create_general_icons()
    
    print("\n" + "=" * 60)
    print("✓ 图标生成完成！")
    print("=" * 60)
    print("\n生成的文件:")
    print("  - assets/AppIcon.iconset/  (macOS iconset)")
    print("  - assets/icon.icns         (macOS 图标)")
    print("  - assets/icon.ico          (Windows 图标)")
    print("  - assets/icon_*.png        (通用 PNG 图标)")
    
    print("\n使用说明:")
    print("  macOS: 已在 sports_performance.spec 中配置")
    print("  Windows: 已在 sports_performance.spec 中配置")
    print("\n提示:")
    print("  如果 icon.icns 创建失败，请在 macOS 上手动运行:")
    print("  iconutil -c icns assets/AppIcon.iconset -o assets/icon.icns")


if __name__ == "__main__":
    main()

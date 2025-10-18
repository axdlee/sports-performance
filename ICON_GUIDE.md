# 应用图标使用指南

## 🎨 图标设计

### 设计理念
- **主题**: 体育运动 - 跑步人物剪影
- **配色**: 蓝色渐变（#2E86AB → #87CEEB）
- **风格**: 现代、简洁、动感
- **元素**: 
  - 跑步人物轮廓
  - 速度线条
  - 圆形边框
  - "PE" 字样（Physical Education）

### 设计特点
- ✅ 在各种尺寸下清晰可辨
- ✅ 符合现代应用设计规范
- ✅ 体现体育评估主题
- ✅ 跨平台统一视觉风格

## 📁 图标文件

### 目录结构
```
assets/
├── icon.icns                 # macOS 应用图标
├── icon.ico                  # Windows 应用图标
├── AppIcon.iconset/          # macOS iconset 源文件
│   ├── icon_16x16.png
│   ├── icon_16x16@2x.png
│   ├── icon_32x32.png
│   ├── icon_32x32@2x.png
│   ├── icon_128x128.png
│   ├── icon_128x128@2x.png
│   ├── icon_256x256.png
│   ├── icon_256x256@2x.png
│   ├── icon_512x512.png
│   └── icon_512x512@2x.png
└── icon_*.png                # 通用 PNG 图标（多尺寸）
```

### 文件说明

#### macOS 图标 (.icns)
- **文件**: `assets/icon.icns`
- **格式**: Apple Icon Image format
- **尺寸**: 包含 16x16 到 1024x1024 的所有标准尺寸
- **用途**: macOS .app bundle 图标

#### Windows 图标 (.ico)
- **文件**: `assets/icon.ico`
- **格式**: Windows Icon format
- **尺寸**: 包含 16x16 到 256x256 的标准尺寸
- **用途**: Windows .exe 应用程序图标

#### PNG 图标
- **文件**: `assets/icon_{size}x{size}.png`
- **尺寸**: 16, 32, 48, 64, 128, 256, 512, 1024
- **用途**: 
  - 通用图标文件
  - 文档、网站使用
  - 自定义尺寸需求

## 🔧 如何使用

### 自动使用（推荐）

图标已集成到打包配置中，使用 `build.py` 构建时会自动应用：

```bash
python build.py
```

### 手动配置

#### 在 PyInstaller spec 文件中
图标路径已在 `sports_performance.spec` 中配置：

```python
# EXE 阶段
exe = EXE(
    ...
    icon='assets/icon.icns' if is_macos else 'assets/icon.ico',
)

# macOS BUNDLE
if is_macos:
    app = BUNDLE(
        ...
        icon='assets/icon.icns',
    )
```

#### 直接使用 PyInstaller
```bash
# macOS
pyinstaller --icon=assets/icon.icns main.py

# Windows
pyinstaller --icon=assets/icon.ico main.py
```

## 🎨 重新生成图标

### 使用自动脚本

运行图标生成脚本：
```bash
python create_icon.py
```

脚本会自动生成所有平台所需的图标文件。

### 自定义图标

#### 修改设计
编辑 `create_icon.py` 文件，修改以下部分：

1. **颜色方案**：
```python
# 修改渐变色
r = int(46 + (135 - 46) * i / size)   # 红色分量
g = int(134 + (206 - 134) * i / size) # 绿色分量
b = int(171 + (235 - 171) * i / size) # 蓝色分量
```

2. **图形元素**：
```python
# 修改人物轮廓、速度线条等
# 参考代码中的绘制逻辑
```

3. **文字内容**：
```python
text = "PE"  # 修改为其他文字
```

#### 使用自定义图片

如果你有设计好的图标图片：

1. 准备 1024x1024 的 PNG 图片
2. 替换生成逻辑：

```python
# 在 create_icon.py 中
def create_base_icon(size=1024):
    img = Image.open("your_icon.png")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    return img
```

### 转换现有图标

#### PNG 转 ICNS (macOS)
```bash
# 创建 iconset
mkdir MyIcon.iconset
sips -z 16 16     icon.png --out MyIcon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out MyIcon.iconset/icon_16x16@2x.png
# ... 其他尺寸

# 转换为 .icns
iconutil -c icns MyIcon.iconset -o assets/icon.icns
```

#### PNG 转 ICO (Windows)
使用在线工具或 ImageMagick：
```bash
convert icon.png -define icon:auto-resize=256,128,96,64,48,32,16 assets/icon.ico
```

或使用 Python Pillow（已在脚本中实现）。

## 📐 图标规范

### 尺寸要求

#### macOS
- **最小**: 16x16 px
- **标准**: 512x512 px
- **高分辨率**: 1024x1024 px (Retina)
- **格式**: ICNS（包含多个尺寸）

#### Windows
- **最小**: 16x16 px
- **标准**: 256x256 px
- **推荐**: 包含 16, 32, 48, 256 尺寸
- **格式**: ICO

### 设计建议

1. **清晰度**: 确保在 16x16 像素时仍可识别
2. **对比度**: 使用高对比度以提高可见性
3. **简洁性**: 避免过多细节，保持简洁
4. **一致性**: 各尺寸保持视觉一致
5. **背景**: 考虑不同背景下的显示效果

### 文件大小

- **ICNS**: 通常 < 500KB
- **ICO**: 通常 < 100KB
- **PNG**: 根据尺寸和压缩而定

## 🧪 测试图标

### macOS
```bash
# 查看应用图标
open dist/体育成绩评估系统.app

# 在 Finder 中查看
open dist/installer_macos/

# 使用 Preview 查看 .icns
open -a Preview assets/icon.icns
```

### Windows
```cmd
# 在资源管理器中查看
explorer dist\installer_windows\

# 查看 .ico
start assets\icon.ico
```

### 验证清单

- [ ] 图标在 Finder/资源管理器中正确显示
- [ ] 应用启动时 Dock/任务栏图标正确
- [ ] 16x16 尺寸仍清晰可辨
- [ ] 高分辨率显示（Retina）效果良好
- [ ] 不同背景（深色/浅色）下都清晰

## 🐛 常见问题

### Q: 图标未显示
**A**: 
1. 检查图标文件是否存在
2. 重新构建应用
3. macOS: 清除图标缓存
   ```bash
   sudo rm -rf /Library/Caches/com.apple.iconservices.store
   killall Dock
   ```

### Q: 图标模糊
**A**: 
1. 确保提供高分辨率版本（至少 512x512）
2. 使用矢量图形或高质量位图
3. 检查 @2x Retina 版本

### Q: Windows 图标颜色失真
**A**: 
1. ICO 格式限制，使用 32-bit 色深
2. 测试不同尺寸
3. 考虑简化配色方案

### Q: macOS 提示图标损坏
**A**: 
1. 重新生成 .icns 文件
2. 使用 `iconutil` 验证：
   ```bash
   iconutil -c iconset assets/icon.icns
   ```

## 🔄 版本历史

### v1.3.1 (2024-10-18)
- ✅ 初始图标设计
- ✅ 蓝色渐变体育主题
- ✅ 跨平台支持
- ✅ 自动化生成脚本

## 📚 相关资源

- [Apple Human Interface Guidelines - App Icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)
- [Windows App Icon Design](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-design)
- [PyInstaller Icons Documentation](https://pyinstaller.org/en/stable/usage.html#icon-resources)
- [Pillow Documentation](https://pillow.readthedocs.io/)

## 💡 设计灵感

如需更换图标设计，可参考：
- 运动主题：篮球、足球、跑道等
- 图表主题：柱状图、曲线图等
- 成绩主题：奖杯、奖牌、证书等
- 抽象主题：几何图形、渐变等

---

**创建日期**: 2025-10-18  
**版本**: 1.0  
**维护**: Sports Performance Assessment Team

# 打包构建指南

## 概述

本项目提供了统一的跨平台打包机制，支持 macOS 和 Windows 平台。

## 打包文件说明

- **`sports_performance.spec`** - PyInstaller 统一配置文件（支持 macOS 和 Windows）
- **`build.py`** - 自动化打包脚本

## 快速开始

### 1. 安装依赖

```bash
# 确保使用项目虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 安装依赖（如未安装）
pip install -r requirements.txt
```

### 2. 运行打包脚本

```bash
# 自动检测平台并打包
python build.py
```

打包脚本会自动：

- 检查依赖是否安装
- 清理旧的构建文件
- 使用 PyInstaller 构建应用
- 根据平台创建对应的安装包

## macOS 打包

### 基本打包

运行 `python build.py` 后会生成：

```shell
dist/
├── 体育成绩评估系统.app          # macOS 应用包
└── installer_macos/              # 安装包目录
    ├── 体育成绩评估系统.app      # 应用程序（副本）
    └── README.txt                # 安装说明
```

### 创建 DMG 安装包（可选）

如需创建专业的 DMG 安装包：

```bash
# 安装 create-dmg 工具
brew install create-dmg

# 运行打包（会自动创建 DMG）
python build.py
```

生成的 DMG：`dist/体育成绩评估系统-v1.0.0-macOS.dmg`

### 代码签名（可选）

如需发布到 App Store 或通过 Gatekeeper：

```bash
# 签名应用
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: Your Name" \
  "dist/体育成绩评估系统.app"

# 公证（需要 Apple 开发者账号）
xcrun notarytool submit "dist/体育成绩评估系统-v1.0.0-macOS.dmg" \
  --apple-id "your@email.com" \
  --team-id "YOUR_TEAM_ID" \
  --password "app-specific-password"
```

## Windows 打包

### 基本打包

运行 `python build.py` 后会生成：

```
dist/
├── 体育成绩评估系统/              # Windows 应用目录
│   ├── 体育成绩评估系统.exe      # 可执行文件
│   ├── data/                     # 数据文件
│   └── ...                       # 依赖库
└── installer_windows/            # 安装包目录
    ├── 体育成绩评估系统/         # 应用程序（副本）
    ├── README.txt                # 安装说明
    ├── 启动程序.bat              # 快速启动脚本
    └── installer.iss             # Inno Setup 脚本
```

### 创建安装程序（可选）

使用 Inno Setup 创建 Windows 安装程序：

1. 下载并安装 [Inno Setup](https://jrsoftware.org/isdl.php)
2. 打开 `dist/installer_windows/installer.iss`
3. 点击 "Compile" 编译安装程序
4. 生成的安装程序位于 `dist/installer_windows/体育成绩评估系统-v1.0.0-Windows-Setup.exe`

### 数字签名（可选）

如需对 exe 进行数字签名：

```cmd
# 使用 signtool（需要代码签名证书）
signtool sign /f "certificate.pfx" /p "password" /t "http://timestamp.digicert.com" ^
  "dist\体育成绩评估系统\体育成绩评估系统.exe"
```

## 手动打包（高级）

### 仅使用 PyInstaller

```bash
# 使用统一的 spec 文件
pyinstaller --clean sports_performance.spec
```

### 自定义打包参数

编辑 `sports_performance.spec` 文件，修改以下内容：

```python
# 添加额外的数据文件
datas = [
    ('data', 'data'),
    ('config', 'config'),
    ('your_folder', 'your_folder'),  # 添加新文件夹
]

# 添加额外的隐藏导入
hiddenimports = [
    'matplotlib',
    'your_module',  # 添加新模块
]

# 修改图标
icon='assets/icon.icns' if is_macos else 'assets/icon.ico'
```

## 添加应用图标

### macOS 图标（.icns）

1. 准备 1024x1024 的 PNG 图片
2. 使用以下命令创建 .icns：

```bash
# 创建临时图标集
mkdir MyIcon.iconset
sips -z 16 16     icon.png --out MyIcon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out MyIcon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out MyIcon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out MyIcon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out MyIcon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out MyIcon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out MyIcon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out MyIcon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out MyIcon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out MyIcon.iconset/icon_512x512@2x.png

# 转换为 .icns
iconutil -c icns MyIcon.iconset

# 移动到 assets 目录
mv MyIcon.icns assets/icon.icns
```

### Windows 图标（.ico）

1. 准备 256x256 的 PNG 图片
2. 使用在线工具或 ImageMagick 转换：

```bash
# 使用 ImageMagick
convert icon.png -define icon:auto-resize=256,128,96,64,48,32,16 assets/icon.ico
```

## 数据存储

打包后的应用将用户数据存储在系统标准位置，而不是应用程序包内部：

- **macOS**: `~/Library/Application Support/SportsPerformance/`
- **Windows**: `%APPDATA%\SportsPerformance\`
- **Linux**: `~/.local/share/SportsPerformance/`

这确保了：

- ✅ 应用包保持只读状态
- ✅ 数据在应用更新后保留
- ✅ 符合各平台的标准实践
- ✅ 多用户环境下数据隔离

详细说明请参考 [DATA_STORAGE.md](DATA_STORAGE.md)

## 常见问题

### Q: PyInstaller 构建失败

**A:** 检查以下内容：

- 确保所有依赖已安装：`pip install -r requirements.txt`
- 更新 PyInstaller：`pip install --upgrade pyinstaller`
- 清理缓存：删除 `build/` 和 `dist/` 目录后重试

### Q: macOS 提示"无法打开，因为来自身份不明的开发者"

**A:** 有两种解决方法：

1. 右键点击应用 → 选择"打开"
2. 在"系统偏好设置 > 安全性与隐私"中允许运行
3. 对应用进行代码签名（推荐用于发布）

### Q: Windows Defender 报毒

**A:** PyInstaller 打包的程序常被误报：

1. 点击"更多信息" → "仍要运行"
2. 将程序添加到信任列表
3. 对 exe 进行数字签名（推荐用于发布）

### Q: 应用体积过大

**A:** 优化建议：

- 使用虚拟环境，只安装必要的依赖
- 在 spec 文件中排除不需要的模块
- 使用 UPX 压缩（已在 spec 中启用）

### Q: 找不到 data 文件

**A:** 确保：

- data 目录存在于项目根目录
- spec 文件中正确配置了 datas
- 代码中使用正确的路径（参考下方）

### 在打包后正确访问资源文件

```python
import sys
import os

def get_resource_path(relative_path):
    """获取资源文件的绝对路径（支持打包后）"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后
        return os.path.join(sys._MEIPASS, relative_path)
    # 开发环境
    return os.path.join(os.path.abspath("."), relative_path)

# 使用示例
data_file = get_resource_path("data/users.json")
```

## 分发清单

### macOS 分发

分发以下内容：

- `dist/installer_macos/` 整个目录，或
- `dist/体育成绩评估系统-v1.0.0-macOS.dmg`（如果已创建）

### Windows 分发

分发以下内容之一：

- `dist/installer_windows/` 整个目录（压缩为 ZIP）
- `dist/installer_windows/体育成绩评估系统-v1.0.0-Windows-Setup.exe`（如果已创建）

## 版本更新

更新版本号时，修改以下文件：

1. `sports_performance.spec` - Bundle 信息
2. `build.py` - DMG/安装程序文件名
3. `README.md` - 项目文档

## 自动化构建（CI/CD）

### GitHub Actions 示例

```yaml
name: Build Installers

on:
  push:
    tags:
      - 'v*'

jobs:
  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python build.py
      - uses: actions/upload-artifact@v2
        with:
          name: macos-installer
          path: dist/installer_macos/

  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python build.py
      - uses: actions/upload-artifact@v2
        with:
          name: windows-installer
          path: dist/installer_windows/
```

## 支持

如有打包相关问题，请检查：

1. Python 版本（建议 3.8-3.11）
2. PyInstaller 版本（建议 5.0+）
3. 操作系统版本
4. 构建日志中的错误信息

---

**最后更新:** 2025-10
**版本:** 1.0.0

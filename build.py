# -*- coding: utf-8 -*-
"""
体育成绩评估系统 - 统一打包脚本
支持 macOS 和 Windows 平台的自动化打包
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def check_requirements():
    """检查打包必要的依赖"""
    print_section("检查依赖")
    
    # 检查 PyInstaller
    try:
        import PyInstaller
        print(f"✓ PyInstaller 已安装 (版本: {PyInstaller.__version__})")
    except ImportError:
        print("✗ PyInstaller 未安装")
        return False
    
    # 检查其他依赖
    required_modules = ['tkinter', 'matplotlib', 'PIL']
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module} 已安装")
        except ImportError:
            print(f"✗ {module} 未安装")
            return False
    
    return True


def install_dependencies():
    """安装依赖包"""
    print_section("安装依赖")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 依赖包安装失败: {e}")
        return False


def clean_build_dirs():
    """清理旧的构建目录"""
    print_section("清理旧构建文件")
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"清理 {dir_name}/ ...")
            shutil.rmtree(dir_name)
    print("✓ 清理完成")


def create_assets_dir():
    """创建 assets 目录（用于存放图标等资源）"""
    assets_dir = Path("assets")
    if not assets_dir.exists():
        assets_dir.mkdir()
        print("✓ 创建 assets 目录")


def build_with_pyinstaller():
    """使用 PyInstaller 构建应用"""
    print_section("使用 PyInstaller 构建应用")
    
    try:
        # 使用统一的 spec 文件，确保使用当前 Python 环境的 PyInstaller
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "sports_performance.spec"]
        
        print("执行命令:", " ".join(cmd))
        subprocess.check_call(cmd)
        print("✓ PyInstaller 构建完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ PyInstaller 构建失败: {e}")
        return False


def create_macos_installer():
    """创建 macOS 安装包"""
    print_section("创建 macOS 安装包")
    
    try:
        app_path = Path("dist/体育成绩评估系统.app")
        
        if not app_path.exists():
            print("✗ .app 文件未找到")
            return False
        
        print(f"✓ 找到应用程序: {app_path}")
        
        # 创建 DMG 安装包（可选，需要 create-dmg 工具）
        installer_dir = Path("dist/installer_macos")
        installer_dir.mkdir(exist_ok=True)
        
        # 复制 .app 到安装包目录
        app_dest = installer_dir / "体育成绩评估系统.app"
        if app_dest.exists():
            shutil.rmtree(app_dest)
        shutil.copytree(app_path, app_dest)
        
        # 创建安装说明
        readme_content = """# 体育成绩评估系统 - macOS 安装包

## 安装说明

1. 将"体育成绩评估系统.app"拖拽到"应用程序"文件夹
2. 双击运行应用程序
3. 如果遇到"无法打开，因为来自身份不明的开发者"：
   - 右键点击应用程序，选择"打开"
   - 或在"系统偏好设置 > 安全性与隐私"中允许运行

## 系统要求

- macOS 10.13 或更高版本
- 无需额外安装 Python 环境

## 使用说明

1. 首次运行需要注册用户（输入姓名和性别）
2. 登录后可以录入体育成绩
3. 系统会自动计算得分并生成分析报告
4. 支持查看历史数据和趋势分析

## 数据存储

应用数据存储在系统标准位置：
  ~/Library/Application Support/SportsPerformance/

这确保：
- 数据在应用更新后保留
- 应用程序包保持只读状态
- 符合 macOS 标准实践

查看数据目录：
1. 打开 Finder，按 Command + Shift + G
2. 输入：~/Library/Application Support/SportsPerformance
3. 点击"前往"

## 数据备份

建议定期备份数据文件：
1. 找到数据目录（见上方说明）
2. 复制整个 SportsPerformance 文件夹
3. 保存到安全位置

## 卸载说明

1. 删除应用：将 .app 拖到废纸篓
2. 删除数据（可选）：
   在终端执行：rm -rf ~/Library/Application\ Support/SportsPerformance

## 技术支持

如有问题，请检查：
1. 系统版本是否满足要求
2. 应用程序权限设置
3. 数据文件完整性

版本: 1.3.1
"""
        
        readme_file = installer_dir / "README.txt"
        readme_file.write_text(readme_content, encoding="utf-8")
        
        print(f"✓ macOS 安装包创建成功: {installer_dir}")
        print(f"  - 应用程序: {app_dest}")
        print(f"  - 说明文档: {readme_file}")
        
        # 尝试创建 DMG（可选）
        try_create_dmg(installer_dir, app_dest)
        
        return True
        
    except Exception as e:
        print(f"✗ macOS 安装包创建失败: {e}")
        return False


def try_create_dmg(installer_dir, app_path):
    """尝试创建 DMG 安装包（需要 create-dmg 工具）"""
    try:
        # 检查是否安装了 create-dmg
        result = subprocess.run(["which", "create-dmg"], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print("\n提示: 未找到 create-dmg 工具")
            print("如需创建 DMG 安装包，请运行: brew install create-dmg")
            return False
        
        print("\n创建 DMG 安装包...")
        dmg_name = "体育成绩评估系统-v1.0.0-macOS.dmg"
        dmg_path = Path("dist") / dmg_name
        
        if dmg_path.exists():
            dmg_path.unlink()
        
        cmd = [
            "create-dmg",
            "--volname", "体育成绩评估系统",
            "--window-pos", "200", "120",
            "--window-size", "600", "400",
            "--icon-size", "100",
            "--app-drop-link", "450", "180",
            str(dmg_path),
            str(installer_dir)
        ]
        
        subprocess.check_call(cmd)
        print(f"✓ DMG 安装包创建成功: {dmg_path}")
        return True
        
    except Exception as e:
        print(f"  DMG 创建跳过: {e}")
        return False


def create_windows_installer():
    """创建 Windows 安装包"""
    print_section("创建 Windows 安装包")
    
    try:
        app_dir = Path("dist/体育成绩评估系统")
        exe_path = app_dir / "体育成绩评估系统.exe"
        
        if not exe_path.exists():
            print("✗ .exe 文件未找到")
            print(f"  查找路径: {exe_path.absolute()}")
            print(f"  dist 目录内容: {list(Path('dist').iterdir()) if Path('dist').exists() else '不存在'}")
            return False
        
        print(f"✓ 找到应用程序: {exe_path}")
        
        # 创建安装包目录
        installer_dir = Path("dist/installer_windows")
        installer_dir.mkdir(parents=True, exist_ok=True)
        
        # 复制整个应用目录到安装包
        app_dest = installer_dir / "体育成绩评估系统"
        if app_dest.exists():
            print(f"清理旧的安装包目录...")
            shutil.rmtree(app_dest)
        
        print(f"复制应用程序到安装包目录...")
        shutil.copytree(app_dir, app_dest)
        
        # 创建安装说明
        readme_content = """# 体育成绩评估系统 - Windows 安装包

## 安装说明

1. 将整个"体育成绩评估系统"文件夹复制到您想安装的位置
   （例如：C:\\Program Files\\体育成绩评估系统）
2. 进入文件夹，双击"体育成绩评估系统.exe"运行程序
3. 可选：创建桌面快捷方式
   - 右键点击"体育成绩评估系统.exe"
   - 选择"发送到" > "桌面快捷方式"

## 系统要求

- Windows 10 或更高版本（建议 Windows 10 1809 或更高）
- 无需额外安装 Python 环境
- 需要约 100MB 磁盘空间

## 使用说明

1. 首次运行需要注册用户（输入姓名和性别）
2. 登录后可以录入体育成绩
3. 系统会自动计算得分并生成分析报告
4. 支持查看历史数据和趋势分析

## 数据存储

应用数据存储在系统标准位置：
  %APPDATA%\\SportsPerformance\\
  
通常为：C:\\Users\\[用户名]\\AppData\\Roaming\\SportsPerformance\\

这确保：
- 数据在应用更新后保留
- 程序目录保持只读状态
- 符合 Windows 标准实践

查看数据目录：
1. 打开文件资源管理器
2. 在地址栏输入：%APPDATA%\\SportsPerformance
3. 按回车

## 数据备份

建议定期备份数据文件：
1. 找到数据目录（见上方说明）
2. 复制整个 SportsPerformance 文件夹
3. 保存到安全位置

## 注意事项

- 首次运行可能被 Windows Defender 拦截：
  * 点击"更多信息"
  * 选择"仍要运行"
- 如被杀毒软件误报，请添加到信任列表

## 卸载说明

1. 删除程序：删除整个程序文件夹
2. 删除数据（可选）：删除 %APPDATA%\\SportsPerformance 文件夹

## 技术支持

如有问题，请检查：
1. 系统版本是否满足要求
2. 杀毒软件/防火墙设置
3. 数据文件完整性
4. 是否有足够的磁盘空间

版本: 1.3.1
"""
        
        readme_file = installer_dir / "README.txt"
        print(f"创建安装说明文档...")
        readme_file.write_text(readme_content, encoding="utf-8")
        
        # 创建快速启动批处理文件
        batch_content = """@echo off
chcp 65001 >nul
cd /d "%~dp0体育成绩评估系统"
start "" "体育成绩评估系统.exe"
"""
        batch_file = installer_dir / "启动程序.bat"
        print(f"创建启动脚本...")
        # Windows 批处理文件使用 GBK 编码
        try:
            batch_file.write_text(batch_content, encoding="utf-8")
        except Exception as e:
            print(f"  使用 UTF-8 编码失败，尝试 GBK: {e}")
            batch_file.write_text(batch_content, encoding="gbk")
        
        print(f"✓ Windows 安装包创建成功: {installer_dir}")
        print(f"  - 应用程序: {app_dest}")
        print(f"  - 说明文档: {readme_file}")
        print(f"  - 启动脚本: {batch_file}")
        
        # 尝试创建 Inno Setup 安装程序（可选）
        try_create_inno_installer(app_dest, installer_dir)
        
        return True
        
    except Exception as e:
        import traceback
        print(f"✗ Windows 安装包创建失败: {e}")
        print(f"详细错误信息:")
        traceback.print_exc()
        return False


def try_create_inno_installer(app_dir, installer_dir):
    """尝试创建 Inno Setup 安装程序（需要 Inno Setup）"""
    try:
        # 创建 Inno Setup 脚本
        iss_content = f"""[Setup]
AppName=体育成绩评估系统
AppVersion=1.0.0
AppPublisher=Sports Performance Assessment
DefaultDirName={{autopf}}\\体育成绩评估系统
DefaultGroupName=体育成绩评估系统
OutputDir={installer_dir.absolute()}
OutputBaseFilename=体育成绩评估系统-v1.0.0-Windows-Setup
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "{app_dir.absolute()}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\体育成绩评估系统"; Filename: "{{app}}\\体育成绩评估系统.exe"
Name: "{{group}}\\卸载体育成绩评估系统"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\体育成绩评估系统"; Filename: "{{app}}\\体育成绩评估系统.exe"

[Run]
Filename: "{{app}}\\体育成绩评估系统.exe"; Description: "启动体育成绩评估系统"; Flags: nowait postinstall skipifsilent
"""
        
        iss_file = installer_dir / "installer.iss"
        iss_file.write_text(iss_content, encoding="utf-8")
        
        print(f"\n✓ Inno Setup 脚本已创建: {iss_file}")
        print("  如需创建安装程序，请：")
        print("  1. 安装 Inno Setup (https://jrsoftware.org/isdl.php)")
        print("  2. 用 Inno Setup 编译 installer.iss 脚本")
        
        return True
        
    except Exception as e:
        print(f"  Inno Setup 脚本创建失败: {e}")
        return False


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("  体育成绩评估系统 - 统一打包工具")
    print("  Physical Education Performance Assessment System")
    print("=" * 60)
    
    # 检查当前平台
    current_platform = platform.system()
    print(f"\n当前平台: {current_platform}")
    
    # 检查依赖
    if not check_requirements():
        print("\n✗ 依赖检查失败，尝试安装依赖...")
        if not install_dependencies():
            print("\n✗ 打包失败：依赖安装失败")
            return 1
    
    # 清理旧的构建文件
    clean_build_dirs()
    
    # 创建 assets 目录
    create_assets_dir()
    
    # 使用 PyInstaller 构建
    if not build_with_pyinstaller():
        print("\n✗ 打包失败：PyInstaller 构建失败")
        return 1
    
    # 根据平台创建安装包
    success = False
    if current_platform == "Darwin":  # macOS
        success = create_macos_installer()
    elif current_platform == "Windows":  # Windows
        success = create_windows_installer()
    else:
        print(f"\n✗ 不支持的平台: {current_platform}")
        print("  支持的平台: macOS (Darwin), Windows")
        return 1
    
    # 打印结果
    print_section("打包完成")
    if success:
        print("✓ 安装包创建成功！")
        print("\n生成的文件:")
        if current_platform == "Darwin":
            print("  - dist/installer_macos/体育成绩评估系统.app")
            print("  - dist/installer_macos/README.txt")
            print("  - dist/体育成绩评估系统-v1.0.0-macOS.dmg (如果 create-dmg 已安装)")
        else:
            print("  - dist/installer_windows/体育成绩评估系统/")
            print("  - dist/installer_windows/README.txt")
            print("  - dist/installer_windows/启动程序.bat")
            print("  - dist/installer_windows/installer.iss (Inno Setup 脚本)")
        
        print("\n分发说明:")
        print("  1. 将安装包目录整体分发给用户")
        print("  2. 用户按照 README.txt 说明安装和使用")
        print("  3. 无需额外安装 Python 环境")
        
        print("\n提示:")
        if current_platform == "Darwin":
            print("  - 如需创建 DMG，请安装: brew install create-dmg")
            print("  - 如需代码签名，请使用: codesign 命令")
        else:
            print("  - 如需创建安装程序，请使用 Inno Setup 编译 installer.iss")
            print("  - 建议在 Windows 机器上进行最终测试")
        
        return 0
    else:
        print("✗ 安装包创建失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())

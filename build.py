# -*- coding: utf-8 -*-
"""
打包脚本 - 生成macOS和Windows安装包
"""

import os
import sys
import subprocess
import platform


def install_dependencies():
    """安装依赖包"""
    print("正在安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依赖包安装完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖包安装失败: {e}")
        return False


def create_macos_app():
    """创建macOS应用程序包"""
    print("正在创建macOS应用程序包...")
    
    try:
        # PyInstaller命令
        cmd = [
            "pyinstaller",
            "--windowed",  # 无控制台窗口
            "--onefile",   # 单文件
            "--name", "体育成绩评估系统",
            "--icon", "icon.ico" if os.path.exists("icon.ico") else None,
            "--add-data", "data:data",  # 包含数据目录
            "--hidden-import", "matplotlib.backends.backend_tkagg",
            "--hidden-import", "matplotlib.figure",
            "--hidden-import", "matplotlib.backends._backend_tk",
            "main.py"
        ]
        
        # 移除None值
        cmd = [arg for arg in cmd if arg is not None]
        
        subprocess.check_call(cmd)
        
        # 创建.app包
        app_name = "体育成绩评估系统.app"
        if os.path.exists("dist/体育成绩评估系统"):
            os.rename("dist/体育成绩评估系统", f"dist/{app_name}")
            print(f"macOS应用程序包创建成功: dist/{app_name}")
        else:
            print("macOS应用程序包创建失败")
            return False
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"macOS应用程序包创建失败: {e}")
        return False


def create_windows_exe():
    """创建Windows可执行文件"""
    print("正在创建Windows可执行文件...")
    
    try:
        # PyInstaller命令
        cmd = [
            "pyinstaller",
            "--windowed",  # 无控制台窗口
            "--onefile",   # 单文件
            "--name", "体育成绩评估系统",
            "--icon", "icon.ico" if os.path.exists("icon.ico") else None,
            "--add-data", "data;data",  # 包含数据目录（Windows使用分号）
            "--hidden-import", "matplotlib.backends.backend_tkagg",
            "--hidden-import", "matplotlib.figure",
            "--hidden-import", "matplotlib.backends._backend_tk",
            "main.py"
        ]
        
        # 移除None值
        cmd = [arg for arg in cmd if arg is not None]
        
        subprocess.check_call(cmd)
        
        exe_name = "体育成绩评估系统.exe"
        if os.path.exists("dist/体育成绩评估系统.exe"):
            print(f"Windows可执行文件创建成功: dist/{exe_name}")
        else:
            print("Windows可执行文件创建失败")
            return False
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Windows可执行文件创建失败: {e}")
        return False


def create_installer_script():
    """创建安装脚本"""
    print("正在创建安装脚本...")
    
    # macOS安装脚本
    macos_installer = """#!/bin/bash
# macOS安装脚本

echo "正在安装体育成绩评估系统..."

# 检查Python版本
python3 --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 安装依赖
echo "安装依赖包..."
pip3 install matplotlib>=3.5.0 Pillow>=9.0.0

# 复制应用程序
if [ -f "dist/体育成绩评估系统.app" ]; then
    cp -r "dist/体育成绩评估系统.app" "/Applications/"
    echo "安装完成！应用程序已安装到 /Applications/"
else
    echo "错误: 未找到应用程序包"
    exit 1
fi

echo "安装完成！"
"""
    
    # Windows安装脚本
    windows_installer = """@echo off
REM Windows安装脚本

echo 正在安装体育成绩评估系统...

REM 检查Python版本
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 安装依赖
echo 安装依赖包...
pip install matplotlib>=3.5.0 Pillow>=9.0.0

REM 复制可执行文件
if exist "dist\\体育成绩评估系统.exe" (
    copy "dist\\体育成绩评估系统.exe" "%USERPROFILE%\\Desktop\\"
    echo 安装完成！可执行文件已复制到桌面
) else (
    echo 错误: 未找到可执行文件
    pause
    exit /b 1
)

echo 安装完成！
pause
"""
    
    # 保存脚本
    with open("install_macos.sh", "w", encoding="utf-8") as f:
        f.write(macos_installer)
    
    with open("install_windows.bat", "w", encoding="utf-8") as f:
        f.write(windows_installer)
    
    # 设置macOS脚本执行权限
    if platform.system() == "Darwin":
        os.chmod("install_macos.sh", 0o755)
    
    print("安装脚本创建完成！")


def main():
    """主函数"""
    print("体育成绩评估系统 - 打包工具")
    print("=" * 50)
    
    # 检查当前平台
    current_platform = platform.system()
    print(f"当前平台: {current_platform}")
    
    # 安装依赖
    if not install_dependencies():
        return
    
    # 创建dist目录
    if not os.path.exists("dist"):
        os.makedirs("dist")
    
    success = False
    
    # 根据平台创建相应的安装包
    if current_platform == "Darwin":  # macOS
        success = create_macos_app()
    elif current_platform == "Windows":  # Windows
        success = create_windows_exe()
    else:
        print(f"不支持的平台: {current_platform}")
        return
    
    if success:
        # 创建安装脚本
        create_installer_script()
        
        print("\n" + "=" * 50)
        print("打包完成！")
        print("生成的文件:")
        print("- dist/ 目录下的应用程序")
        print("- install_macos.sh (macOS安装脚本)")
        print("- install_windows.bat (Windows安装脚本)")
        print("\n使用说明:")
        print("1. 将dist目录下的应用程序分发给用户")
        print("2. 用户运行相应的安装脚本即可安装")
    else:
        print("打包失败！")


if __name__ == "__main__":
    main()

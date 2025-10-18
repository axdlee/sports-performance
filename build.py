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


def create_macos_installer():
    """创建macOS安装包"""
    print("正在创建macOS安装包...")
    
    try:
        # 创建应用程序包
        cmd = [
            "pyinstaller",
            "--windowed",  # 无控制台窗口
            "--onedir",    # 目录模式，便于安装
            "--name", "体育成绩评估系统",
            "--add-data", "data:data",  # 包含数据目录
            "--hidden-import", "matplotlib.backends.backend_tkagg",
            "--hidden-import", "matplotlib.figure",
            "--hidden-import", "matplotlib.backends._backend_tk",
            "main.py"
        ]
        
        subprocess.check_call(cmd)
        
        # 创建安装包目录结构
        installer_dir = "dist/体育成绩评估系统_安装包"
        os.makedirs(installer_dir, exist_ok=True)
        
        # 复制应用程序
        app_source = "dist/体育成绩评估系统"
        app_dest = f"{installer_dir}/体育成绩评估系统.app"
        
        if os.path.exists(app_source):
            subprocess.run(["cp", "-r", app_source, app_dest])
            
            # 创建安装说明
            readme_content = """# 体育成绩评估系统 - macOS安装包

## 安装说明

1. 双击"体育成绩评估系统.app"即可运行
2. 如需安装到应用程序文件夹：
   - 将"体育成绩评估系统.app"拖拽到"应用程序"文件夹
   - 或右键点击选择"移动到应用程序文件夹"

## 系统要求

- macOS 10.14 或更高版本
- 无需额外安装Python环境

## 使用说明

1. 首次运行需要输入姓名和性别进行注册
2. 登录后可以录入体育成绩
3. 系统会自动计算得分并生成分析报告

## 注意事项

- 数据文件保存在应用程序目录下的data文件夹
- 建议定期备份数据文件
- 如遇问题，请检查系统权限设置

## 技术支持

如有问题，请检查：
1. 系统版本是否满足要求
2. 应用程序权限设置
3. 数据文件完整性
"""
            
            with open(f"{installer_dir}/安装说明.txt", "w", encoding="utf-8") as f:
                f.write(readme_content)
            
            print(f"macOS安装包创建成功: {installer_dir}")
            return True
        else:
            print("macOS安装包创建失败")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"macOS安装包创建失败: {e}")
        return False


def create_windows_installer():
    """创建Windows安装包"""
    print("正在创建Windows安装包...")
    
    try:
        # 创建可执行文件
        cmd = [
            "pyinstaller",
            "--windowed",  # 无控制台窗口
            "--onedir",    # 目录模式，便于安装
            "--name", "体育成绩评估系统",
            "--add-data", "data;data",  # 包含数据目录（Windows使用分号）
            "--hidden-import", "matplotlib.backends.backend_tkagg",
            "--hidden-import", "matplotlib.figure",
            "--hidden-import", "matplotlib.backends._backend_tk",
            "main.py"
        ]
        
        subprocess.check_call(cmd)
        
        # 创建安装包目录结构
        installer_dir = "dist/体育成绩评估系统_安装包"
        os.makedirs(installer_dir, exist_ok=True)
        
        # 复制应用程序
        app_source = "dist/体育成绩评估系统"
        app_dest = f"{installer_dir}/体育成绩评估系统"
        
        if os.path.exists(app_source):
            subprocess.run(["xcopy", app_source, app_dest, "/E", "/I"], shell=True)
            
            # 创建安装说明
            readme_content = """# 体育成绩评估系统 - Windows安装包

## 安装说明

1. 双击"体育成绩评估系统.exe"即可运行
2. 如需创建桌面快捷方式：
   - 右键点击"体育成绩评估系统.exe"
   - 选择"发送到" -> "桌面快捷方式"

## 系统要求

- Windows 10 或更高版本
- 无需额外安装Python环境

## 使用说明

1. 首次运行需要输入姓名和性别进行注册
2. 登录后可以录入体育成绩
3. 系统会自动计算得分并生成分析报告

## 注意事项

- 数据文件保存在应用程序目录下的data文件夹
- 建议定期备份数据文件
- 如遇杀毒软件拦截，请添加信任

## 技术支持

如有问题，请检查：
1. 系统版本是否满足要求
2. 杀毒软件设置
3. 数据文件完整性
"""
            
            with open(f"{installer_dir}/安装说明.txt", "w", encoding="utf-8") as f:
                f.write(readme_content)
            
            print(f"Windows安装包创建成功: {installer_dir}")
            return True
        else:
            print("Windows安装包创建失败")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Windows安装包创建失败: {e}")
        return False


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
        success = create_macos_installer()
    elif current_platform == "Windows":  # Windows
        success = create_windows_installer()
    else:
        print(f"不支持的平台: {current_platform}")
        return
    
    if success:
        print("\n" + "=" * 50)
        print("安装包创建完成！")
        print("生成的文件:")
        print("- dist/体育成绩评估系统_安装包/ 目录")
        print("- 包含完整的应用程序和安装说明")
        print("\n使用说明:")
        print("1. 将整个安装包目录分发给用户")
        print("2. 用户直接运行应用程序即可使用")
        print("3. 无需额外安装Python环境")
    else:
        print("安装包创建失败！")


if __name__ == "__main__":
    main()

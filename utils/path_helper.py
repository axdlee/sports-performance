# -*- coding: utf-8 -*-
"""
路径辅助工具 - 处理打包后的资源和数据路径
"""

import sys
import os
from pathlib import Path


def get_resource_path(relative_path):
    """
    获取资源文件的绝对路径（支持打包后的环境）
    
    Args:
        relative_path: 相对于项目根目录的路径
        
    Returns:
        资源文件的绝对路径
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后，资源文件在临时目录
        return os.path.join(sys._MEIPASS, relative_path)
    # 开发环境，资源文件在项目目录
    return os.path.join(os.path.abspath("."), relative_path)


def get_user_data_dir():
    """
    获取用户数据目录（可写目录）
    
    macOS: ~/Library/Application Support/SportsPerformance/
    Windows: %APPDATA%/SportsPerformance/
    Linux: ~/.local/share/SportsPerformance/
    
    Returns:
        用户数据目录的绝对路径
    """
    app_name = "SportsPerformance"
    
    if sys.platform == 'darwin':  # macOS
        base_dir = Path.home() / "Library" / "Application Support"
    elif sys.platform == 'win32':  # Windows
        base_dir = Path(os.environ.get('APPDATA', Path.home() / "AppData" / "Roaming"))
    else:  # Linux 和其他
        base_dir = Path.home() / ".local" / "share"
    
    data_dir = base_dir / app_name
    
    # 确保目录存在
    data_dir.mkdir(parents=True, exist_ok=True)
    
    return str(data_dir)


def get_data_file_path(filename):
    """
    获取数据文件的完整路径
    
    Args:
        filename: 文件名（如 "users.json"）
        
    Returns:
        数据文件的完整路径
    """
    return os.path.join(get_user_data_dir(), filename)


def is_packaged():
    """
    检查应用是否已打包
    
    Returns:
        如果是打包后的应用返回 True，否则返回 False
    """
    return hasattr(sys, '_MEIPASS')


def get_app_version():
    """获取应用版本号"""
    return "1.3.0"

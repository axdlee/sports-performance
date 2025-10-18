#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试路径配置是否正确
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("路径配置测试")
print("=" * 60)

# 测试 path_helper
print("\n1. 测试 path_helper 模块:")
try:
    from utils.path_helper import (
        get_user_data_dir, 
        get_data_file_path, 
        is_packaged,
        get_resource_path
    )
    
    print(f"✓ path_helper 导入成功")
    print(f"  - 是否打包: {is_packaged()}")
    print(f"  - 用户数据目录: {get_user_data_dir()}")
    print(f"  - 用户数据文件: {get_data_file_path('users.json')}")
    print(f"  - 资源路径示例: {get_resource_path('config')}")
    
    # 检查目录是否可写
    data_dir = get_user_data_dir()
    test_file = os.path.join(data_dir, ".test_write")
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print(f"✓ 数据目录可写")
    except Exception as e:
        print(f"✗ 数据目录不可写: {e}")
        
except Exception as e:
    print(f"✗ path_helper 导入失败: {e}")
    import traceback
    traceback.print_exc()

# 测试 constants
print("\n2. 测试 constants 配置:")
try:
    from config.constants import DATA_FILE
    print(f"✓ DATA_FILE 导入成功")
    print(f"  - DATA_FILE 路径: {DATA_FILE}")
    
    # 检查目录
    data_dir = os.path.dirname(DATA_FILE)
    if os.path.exists(data_dir):
        print(f"✓ 数据目录存在")
    else:
        print(f"  创建数据目录: {data_dir}")
        os.makedirs(data_dir, exist_ok=True)
        
except Exception as e:
    print(f"✗ constants 导入失败: {e}")
    import traceback
    traceback.print_exc()

# 测试 DataManager
print("\n3. 测试 DataManager:")
try:
    from services.data_manager import DataManager
    dm = DataManager()
    print(f"✓ DataManager 初始化成功")
    print(f"  - 数据文件路径: {dm.data_file}")
    print(f"  - 当前用户数: {len(dm.users)}")
    
except Exception as e:
    print(f"✗ DataManager 初始化失败: {e}")
    import traceback
    traceback.print_exc()

# 测试 MainWindow 配置
print("\n4. 测试 MainWindow 配置:")
try:
    from ui.main_window import MainWindow
    print(f"✓ MainWindow 导入成功")
    print(f"  - LAST_USER_FILE: {MainWindow.LAST_USER_FILE}")
    
except Exception as e:
    print(f"✗ MainWindow 导入失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)

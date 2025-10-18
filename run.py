# -*- coding: utf-8 -*-
"""
快速启动脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """快速启动主程序"""
    try:
        from main import main as run_main
        run_main()
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保已安装所有依赖包:")
        print("pip install -r requirements.txt")
    except Exception as e:
        print(f"启动失败: {e}")


if __name__ == "__main__":
    main()

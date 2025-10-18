# -*- coding: utf-8 -*-
"""
体育成绩评估系统 - 主程序入口
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow


def main():
    """主函数"""
    try:
        # 创建主窗口并运行
        app = MainWindow()
        app.run()
    except Exception as e:
        # 错误处理
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        messagebox.showerror("程序错误", f"程序启动时发生错误：\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

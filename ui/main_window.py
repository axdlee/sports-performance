# -*- coding: utf-8 -*-
"""
主窗口
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from models.user import User
from ui.login_window import LoginWindow
from ui.input_window import InputWindow
from ui.report_window import ReportWindow
from services.data_manager import DataManager


class MainWindow:
    """主窗口类"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.current_user: Optional[User] = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主窗口
        self.window = tk.Tk()
        self.window.title("体育成绩评估系统")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        # 设置窗口居中
        self.center_window()
        
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="体育成绩评估系统", 
                               font=("Arial", 20, "bold"))
        title_label.pack(pady=(0, 30))
        
        # 用户信息显示
        self.user_info_frame = ttk.LabelFrame(main_frame, text="当前用户", padding="15")
        self.user_info_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.user_info_var = tk.StringVar(value="未登录")
        self.user_info_label = ttk.Label(self.user_info_frame, textvariable=self.user_info_var, 
                                        font=("Arial", 12))
        self.user_info_label.pack()
        
        # 功能按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 登录按钮
        self.login_button = ttk.Button(button_frame, text="用户登录", 
                                     command=self.show_login_window, width=20)
        self.login_button.pack(pady=5)
        
        # 成绩录入按钮
        self.input_button = ttk.Button(button_frame, text="成绩录入", 
                                     command=self.show_input_window, width=20, state=tk.DISABLED)
        self.input_button.pack(pady=5)
        
        # 成绩报告按钮
        self.report_button = ttk.Button(button_frame, text="成绩报告", 
                                      command=self.show_report_window, width=20, state=tk.DISABLED)
        self.report_button.pack(pady=5)
        
        # 退出按钮
        self.exit_button = ttk.Button(button_frame, text="退出程序", 
                                     command=self.exit_application, width=20)
        self.exit_button.pack(pady=5)
        
        # 状态栏
        self.status_var = tk.StringVar(value="欢迎使用体育成绩评估系统")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                               foreground="gray", font=("Arial", 10))
        status_label.pack(pady=(20, 0))
    
    def center_window(self):
        """窗口居中显示"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def show_login_window(self):
        """显示登录窗口"""
        login_window = LoginWindow(self.window)
        login_window.set_login_callback(self.on_login_success)
        login_window.show()
    
    def on_login_success(self, user: User):
        """登录成功回调"""
        self.current_user = user
        self.update_ui_after_login()
        self.status_var.set(f"欢迎，{user.name}！")
    
    def update_ui_after_login(self):
        """登录后更新界面"""
        if self.current_user:
            gender_text = "男" if self.current_user.gender == "male" else "女"
            student_id = self.current_user.student_id or "未设置"
            record_count = len(self.current_user.records)
            
            user_info = f"{self.current_user.name} ({gender_text}) - 学号: {student_id} - 记录: {record_count}条"
            self.user_info_var.set(user_info)
            
            # 启用功能按钮
            self.input_button.config(state=tk.NORMAL)
            self.report_button.config(state=tk.NORMAL)
            
            # 禁用登录按钮
            self.login_button.config(state=tk.DISABLED)
    
    def show_input_window(self):
        """显示成绩录入窗口"""
        if not self.current_user:
            messagebox.showerror("错误", "请先登录")
            return
        
        input_window = InputWindow(self.current_user, self.window)
        input_window.set_save_callback(self.on_score_saved)
        input_window.show()
    
    def on_score_saved(self, record_data):
        """成绩保存成功回调"""
        # 更新用户信息显示
        self.update_ui_after_login()
        
        # 更新状态
        total_score = record_data["total_score"]
        self.status_var.set(f"成绩已保存！总分: {total_score:.1f}")
        
        # 询问是否查看报告
        if messagebox.askyesno("保存成功", f"成绩已保存！总分: {total_score:.1f}\n\n是否查看成绩报告？"):
            self.show_report_window()
    
    def show_report_window(self):
        """显示成绩报告窗口"""
        if not self.current_user:
            messagebox.showerror("错误", "请先登录")
            return
        
        if not self.current_user.records:
            messagebox.showwarning("无数据", "暂无成绩记录，请先录入成绩")
            return
        
        report_window = ReportWindow(self.current_user, self.window)
        report_window.show()
    
    def exit_application(self):
        """退出应用程序"""
        if messagebox.askyesno("确认退出", "确定要退出程序吗？"):
            self.window.quit()
    
    def run(self):
        """运行主窗口"""
        self.window.mainloop()

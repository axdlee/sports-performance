# -*- coding: utf-8 -*-
"""
主窗口
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from typing import Optional
from models.user import User
from ui.login_window import LoginWindow
from ui.input_window import InputWindow
from ui.report_window import ReportWindow
from ui.custom_button import CustomButton
from services.data_manager import DataManager


class MainWindow:
    """主窗口类"""
    
    # 上次登录用户配置文件路径
    LAST_USER_FILE = "data/last_user.json"
    
    def __init__(self):
        self.data_manager = DataManager()
        self.current_user: Optional[User] = None
        
        self.setup_ui()
        self.load_last_user()  # 启动时自动加载上次登录的用户
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主窗口
        self.window = tk.Tk()
        self.window.title("体育成绩评估系统")
        self.window.geometry("500x550")
        self.window.resizable(False, False)
        
        # 设置窗口背景色
        self.window.configure(bg="#ecf0f1")
        
        # 设置窗口居中
        self.center_window()
        
        # 创建主框架
        main_frame = tk.Frame(self.window, bg="#ecf0f1", padx=30, pady=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题框架
        title_frame = tk.Frame(main_frame, bg="#16a085", pady=25)
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        # 标题
        title_label = tk.Label(title_frame, text="🏃 体育成绩评估系统", 
                               font=("Microsoft YaHei", 22, "bold"),
                               bg="#16a085", fg="white")
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Physical Education Performance Assessment System",
                                 font=("Arial", 9),
                                 bg="#16a085", fg="#ecf0f1")
        subtitle_label.pack(pady=(5, 0))
        
        # 用户信息显示
        self.user_info_frame = tk.LabelFrame(main_frame, text=" 👤 当前用户 ", 
                                            font=("Microsoft YaHei", 11, "bold"),
                                            bg="#ffffff", fg="#2c3e50",
                                            padx=20, pady=15, relief=tk.FLAT, bd=0)
        self.user_info_frame.pack(fill=tk.X, pady=(0, 25))
        
        self.user_info_var = tk.StringVar(value="未登录")
        self.user_info_label = tk.Label(self.user_info_frame, textvariable=self.user_info_var, 
                                        font=("Microsoft YaHei", 12),
                                        bg="#ffffff", fg="#34495e")
        self.user_info_label.pack()
        
        # 功能按钮框架
        button_frame = tk.Frame(main_frame, bg="#ecf0f1")
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 登录按钮
        self.login_button = CustomButton(button_frame, text="🔑 用户登录", 
                                        command=self.show_login_window,
                                        font=("Microsoft YaHei", 12, "bold"),
                                        bg="#3498db", fg="white",
                                        width=8, height=1,
                                        activebackground="#2980b9",
                                        activeforeground="white")
        self.login_button.pack(pady=8, fill=tk.X)
        
        # 成绩录入按钮
        self.input_button = CustomButton(button_frame, text="📝 成绩录入", 
                                        command=self.show_input_window,
                                        font=("Microsoft YaHei", 12, "bold"),
                                        bg="#2ecc71", fg="white",
                                        width=8, height=1,
                                        state=tk.DISABLED,
                                        activebackground="#27ae60",
                                        activeforeground="white")
        self.input_button.pack(pady=8, fill=tk.X)
        self.input_button_enabled_bg = "#2ecc71"
        self.input_button_disabled_bg = "#bdc3c7"
        
        # 成绩报告按钮
        self.report_button = CustomButton(button_frame, text="📊 成绩报告", 
                                         command=self.show_report_window,
                                         font=("Microsoft YaHei", 12, "bold"),
                                         bg="#e67e22", fg="white",
                                         width=8, height=1,
                                         state=tk.DISABLED,
                                         activebackground="#d35400",
                                         activeforeground="white")
        self.report_button.pack(pady=8, fill=tk.X)
        self.report_button_enabled_bg = "#e67e22"
        self.report_button_disabled_bg = "#bdc3c7"
        
        # 退出按钮
        self.exit_button = CustomButton(button_frame, text="❌ 退出程序", 
                                        command=self.exit_application,
                                        font=("Microsoft YaHei", 12, "bold"),
                                        bg="#95a5a6", fg="white",
                                        width=8, height=1,
                                        activebackground="#7f8c8d",
                                        activeforeground="white")
        self.exit_button.pack(pady=8, fill=tk.X)
        
        # 状态栏
        self.status_var = tk.StringVar(value="💡 欢迎使用体育成绩评估系统")
        status_label = tk.Label(main_frame, textvariable=self.status_var,
                               font=("Microsoft YaHei", 10),
                               bg="#ecf0f1", fg="#7f8c8d")
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
        self.save_last_user(user.id)  # 保存用户ID
        self.update_ui_after_login()
        self.status_var.set(f"✅ 欢迎，{user.name}！")
    
    def reload_current_user(self):
        """重新加载当前用户数据（从文件读取最新数据）"""
        if self.current_user:
            # 从DataManager重新加载用户
            updated_user = self.data_manager.find_user_by_id(self.current_user.id)
            if updated_user:
                self.current_user = updated_user
    
    def update_ui_after_login(self):
        """登录后更新界面"""
        if self.current_user:
            gender_text = "男" if self.current_user.gender == "male" else "女"
            record_count = len(self.current_user.records)
            
            user_info = f"✅ {self.current_user.name} ({gender_text}) - 记录: {record_count}条"
            self.user_info_var.set(user_info)
            
            # 启用功能按钮并更新样式
            self.input_button.config(state=tk.NORMAL, bg=self.input_button_enabled_bg, 
                                    fg="white", cursor="hand2")
            self.report_button.config(state=tk.NORMAL, bg=self.report_button_enabled_bg,
                                     fg="white", cursor="hand2")
            
            # 将登录按钮改为"切换用户"
            self.login_button.config(state=tk.NORMAL, bg="#9b59b6", fg="white", 
                                    cursor="hand2", text="🔄 切换用户")
    
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
        # 重新加载用户数据以获取最新记录
        self.reload_current_user()
        
        # 更新用户信息显示
        self.update_ui_after_login()
        
        # 更新状态
        total_score = record_data["total_score"]
        self.status_var.set(f"✅ 成绩已保存！总分: {total_score:.1f}")
        
        # 询问是否查看报告
        if messagebox.askyesno("保存成功", f"成绩已保存！总分: {total_score:.1f}\n\n是否查看成绩报告？"):
            self.show_report_window()
    
    def show_report_window(self):
        """显示成绩报告窗口"""
        if not self.current_user:
            messagebox.showerror("错误", "请先登录")
            return
        
        # 重新加载用户数据以确保显示最新记录
        self.reload_current_user()
        
        if not self.current_user.records:
            messagebox.showwarning("无数据", "暂无成绩记录，请先录入成绩")
            return
        
        report_window = ReportWindow(self.current_user, self.window)
        report_window.show()
    
    def save_last_user(self, user_id: str):
        """保存上次登录的用户ID到配置文件"""
        try:
            # 确保data目录存在
            os.makedirs(os.path.dirname(self.LAST_USER_FILE), exist_ok=True)
            
            config = {"last_user_id": user_id}
            with open(self.LAST_USER_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存上次登录用户失败: {e}")
    
    def load_last_user(self):
        """加载上次登录的用户"""
        try:
            if os.path.exists(self.LAST_USER_FILE):
                with open(self.LAST_USER_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    last_user_id = config.get("last_user_id")
                    
                    if last_user_id:
                        # 尝试从DataManager加载用户
                        user = self.data_manager.find_user_by_id(last_user_id)
                        if user:
                            self.current_user = user
                            self.update_ui_after_login()
                            self.status_var.set(f"✅ 自动登录: {user.name}")
                            return
            
            # 如果没有上次用户或加载失败，显示默认状态
            self.status_var.set("💡 欢迎使用体育成绩评估系统")
        except Exception as e:
            print(f"加载上次登录用户失败: {e}")
            self.status_var.set("💡 欢迎使用体育成绩评估系统")
    
    def exit_application(self):
        """退出应用程序"""
        if messagebox.askyesno("确认退出", "确定要退出程序吗？"):
            # 退出时保存当前用户（如果已登录）
            if self.current_user:
                self.save_last_user(self.current_user.id)
            self.window.destroy()
    
    def run(self):
        """运行主窗口"""
        self.window.mainloop()

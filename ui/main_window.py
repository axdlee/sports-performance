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
from config.constants import (
    MAIN_WINDOW_CONFIG, WINDOW_SIZES, WINDOW_TITLES,
    BUTTON_TEXTS, LABEL_FRAME_TITLES, UI_TEXTS
)


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
        self.window.title(WINDOW_TITLES["main"])
        self.window.geometry(WINDOW_SIZES["main"])
        self.window.resizable(False, False)
        
        # 设置窗口背景色
        self.window.configure(bg=MAIN_WINDOW_CONFIG["bg_color"])
        
        # 设置窗口居中
        self.center_window()
        
        # 创建主框架
        main_frame = tk.Frame(self.window, bg=MAIN_WINDOW_CONFIG["bg_color"], padx=30, pady=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题框架
        title_frame = tk.Frame(main_frame, bg=MAIN_WINDOW_CONFIG["title_bg"], pady=25)
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        # 标题
        title_label = tk.Label(title_frame, text="🏃 体育成绩评估系统", 
                               font=MAIN_WINDOW_CONFIG["title_font"],
                               bg=MAIN_WINDOW_CONFIG["title_bg"], fg=MAIN_WINDOW_CONFIG["title_fg"])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Physical Education Performance Assessment System",
                                 font=MAIN_WINDOW_CONFIG["subtitle_font"],
                                 bg=MAIN_WINDOW_CONFIG["title_bg"], fg=MAIN_WINDOW_CONFIG["bg_color"])
        subtitle_label.pack(pady=(5, 0))
        
        # 用户信息显示
        self.user_info_frame = tk.LabelFrame(main_frame, text=LABEL_FRAME_TITLES["current_user"], 
                                            font=MAIN_WINDOW_CONFIG["label_font_bold"],
                                            bg=MAIN_WINDOW_CONFIG["frame_bg"], fg=MAIN_WINDOW_CONFIG["frame_fg"],
                                            padx=20, pady=15, relief=tk.FLAT, bd=0)
        self.user_info_frame.pack(fill=tk.X, pady=(0, 25))
        
        self.user_info_var = tk.StringVar(value=UI_TEXTS["not_logged_in"])
        self.user_info_label = tk.Label(self.user_info_frame, textvariable=self.user_info_var, 
                                        font=MAIN_WINDOW_CONFIG["label_font_normal"],
                                        bg=MAIN_WINDOW_CONFIG["frame_bg"], fg=MAIN_WINDOW_CONFIG["user_info_text_color"])
        self.user_info_label.pack()
        
        # 功能按钮框架
        button_frame = tk.Frame(main_frame, bg=MAIN_WINDOW_CONFIG["bg_color"])
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 登录按钮
        self.login_button = CustomButton(button_frame, text=BUTTON_TEXTS["user_login"], 
                                        command=self.show_login_window,
                                        font=MAIN_WINDOW_CONFIG["button_font"],
                                        bg=MAIN_WINDOW_CONFIG["login_button_bg"], fg="white",
                                        width=8, height=1)
        self.login_button.pack(pady=8, fill=tk.X)
        
        # 成绩录入按钮
        self.input_button = CustomButton(button_frame, text=BUTTON_TEXTS["input_score"], 
                                        command=self.show_input_window,
                                        font=MAIN_WINDOW_CONFIG["button_font"],
                                        bg=MAIN_WINDOW_CONFIG["input_button_bg"], fg="white",
                                        width=8, height=1,
                                        state=tk.DISABLED)
        self.input_button.pack(pady=8, fill=tk.X)
        self.input_button_enabled_bg = MAIN_WINDOW_CONFIG["input_button_bg"]
        self.input_button_disabled_bg = MAIN_WINDOW_CONFIG["disabled_button_bg"]
        
        # 成绩报告按钮
        self.report_button = CustomButton(button_frame, text=BUTTON_TEXTS["view_report"], 
                                         command=self.show_report_window,
                                         font=MAIN_WINDOW_CONFIG["button_font"],
                                         bg=MAIN_WINDOW_CONFIG["report_button_bg"], fg="white",
                                         width=8, height=1,
                                         state=tk.DISABLED)
        self.report_button.pack(pady=8, fill=tk.X)
        self.report_button_enabled_bg = MAIN_WINDOW_CONFIG["report_button_bg"]
        self.report_button_disabled_bg = MAIN_WINDOW_CONFIG["disabled_button_bg"]
        
        # 退出按钮
        self.exit_button = CustomButton(button_frame, text=BUTTON_TEXTS["exit"], 
                                        command=self.exit_application,
                                        font=MAIN_WINDOW_CONFIG["button_font"],
                                        bg=MAIN_WINDOW_CONFIG["exit_button_bg"], fg="white",
                                        width=8, height=1)
        self.exit_button.pack(pady=8, fill=tk.X)
        
        # 状态栏
        self.status_var = tk.StringVar(value=UI_TEXTS["welcome"])
        status_label = tk.Label(main_frame, textvariable=self.status_var,
                               font=MAIN_WINDOW_CONFIG["status_font"],
                               bg=MAIN_WINDOW_CONFIG["bg_color"], fg=MAIN_WINDOW_CONFIG["label_hint_color"])
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
        self.status_var.set(UI_TEXTS["login_success"].format(user.name))
    
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
            from config.constants import GENDER_CONFIG
            gender_text = GENDER_CONFIG[self.current_user.gender]["text"]
            record_count = len(self.current_user.records)
            
            user_info = UI_TEXTS["user_info_format"].format(self.current_user.name, gender_text, record_count)
            self.user_info_var.set(user_info)
            
            # 启用功能按钮并更新样式
            self.input_button.config(state=tk.NORMAL, bg=self.input_button_enabled_bg, 
                                    fg="white", cursor="hand2")
            self.report_button.config(state=tk.NORMAL, bg=self.report_button_enabled_bg,
                                     fg="white", cursor="hand2")
            
            # 将登录按钮改为"切换用户"
            self.login_button.config(state=tk.NORMAL, bg=MAIN_WINDOW_CONFIG["switch_user_button_bg"], fg="white", 
                                    cursor="hand2", text=BUTTON_TEXTS["switch_user"])
    
    def show_input_window(self):
        """显示成绩录入窗口"""
        if not self.current_user:
            messagebox.showerror(UI_TEXTS["input_error"], UI_TEXTS["please_login"])
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
        self.status_var.set(UI_TEXTS["save_success"] + f"总分: {total_score:.1f}")
        
        # 询问是否查看报告
        if messagebox.askyesno(UI_TEXTS["save_success"], UI_TEXTS["view_report_prompt"].format(total_score)):
            self.show_report_window()
    
    def show_report_window(self):
        """显示成绩报告窗口"""
        if not self.current_user:
            messagebox.showerror(UI_TEXTS["input_error"], UI_TEXTS["please_login"])
            return
        
        # 重新加载用户数据以确保显示最新记录
        self.reload_current_user()
        
        if not self.current_user.records:
            messagebox.showwarning(UI_TEXTS["input_error"], UI_TEXTS["no_records"])
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
                            self.status_var.set(UI_TEXTS["auto_login"].format(user.name))
                            return
            
            # 如果没有上次用户或加载失败，显示默认状态
            self.status_var.set(UI_TEXTS["welcome"])
        except Exception as e:
            print(f"加载上次登录用户失败: {e}")
            self.status_var.set(UI_TEXTS["welcome"])
    
    def exit_application(self):
        """退出应用程序"""
        if messagebox.askyesno(UI_TEXTS["confirm_exit"], UI_TEXTS["exit_message"]):
            # 退出时保存当前用户（如果已登录）
            if self.current_user:
                self.save_last_user(self.current_user.id)
            self.window.destroy()
    
    def run(self):
        """运行主窗口"""
        self.window.mainloop()

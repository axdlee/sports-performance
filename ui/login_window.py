# -*- coding: utf-8 -*-
"""
登录/用户选择界面
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from models.user import User
from services.data_manager import DataManager
from utils.validator import DataValidator
from config.constants import (
    GENDER_MALE, GENDER_FEMALE,
    LOGIN_WINDOW_CONFIG, WINDOW_SIZES, WINDOW_TITLES,
    BUTTON_TEXTS, LABEL_FRAME_TITLES, UI_TEXTS, GENDER_CONFIG
)
from ui.custom_button import CustomButton


class LoginWindow:
    """登录窗口类"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.data_manager = DataManager()
        self.current_user: Optional[User] = None
        self.on_login_success: Optional[Callable] = None
        
        self.setup_ui()
        self.load_existing_users()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主窗口
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.window.title(WINDOW_TITLES["login"])
        self.window.geometry(WINDOW_SIZES["login"])
        self.window.resizable(False, False)
        
        # 设置窗口背景色
        self.window.configure(bg=LOGIN_WINDOW_CONFIG["bg_color"])
        
        # 设置窗口居中
        self.center_window()
        
        # 创建主框架
        main_frame = tk.Frame(self.window, bg=LOGIN_WINDOW_CONFIG["bg_color"], padx=35, pady=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题框架
        title_frame = tk.Frame(main_frame, bg=LOGIN_WINDOW_CONFIG["title_bg"], pady=25)
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        # 标题
        title_label = tk.Label(title_frame, text="🏃 体育成绩评估系统", 
                              font=LOGIN_WINDOW_CONFIG["title_font"],
                              bg=LOGIN_WINDOW_CONFIG["title_bg"], fg=LOGIN_WINDOW_CONFIG["title_fg"])
        title_label.pack()
        
        # 副标题
        subtitle_label = tk.Label(title_frame, text="用户登录 / User Login",
                                 font=LOGIN_WINDOW_CONFIG["subtitle_font"],
                                 bg=LOGIN_WINDOW_CONFIG["title_bg"], fg=LOGIN_WINDOW_CONFIG["bg_color"])
        subtitle_label.pack(pady=(5, 0))
        
        # 用户信息输入框架
        info_frame = tk.LabelFrame(main_frame, text=LABEL_FRAME_TITLES["user_info"], 
                                   font=LOGIN_WINDOW_CONFIG["section_font"],
                                   bg=LOGIN_WINDOW_CONFIG["frame_bg"], fg=LOGIN_WINDOW_CONFIG["frame_fg"],
                                   padx=25, pady=20, relief=tk.FLAT, bd=2)
        info_frame.pack(fill=tk.X, pady=(0, 25))
        
        # 姓名输入区域
        name_container = tk.Frame(info_frame, bg=LOGIN_WINDOW_CONFIG["frame_bg"])
        name_container.pack(fill=tk.X, pady=(0, 15))
        
        name_label = tk.Label(name_container, text="姓名", 
                             font=LOGIN_WINDOW_CONFIG["label_font_bold"],
                             bg=LOGIN_WINDOW_CONFIG["frame_bg"], fg=LOGIN_WINDOW_CONFIG["label_primary_color"])
        name_label.pack(anchor=tk.W)
        
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(name_container, textvariable=self.name_var, 
                                   font=LOGIN_WINDOW_CONFIG["entry_font"],
                                   relief=tk.SOLID, bd=1, 
                                   highlightthickness=1, highlightcolor=LOGIN_WINDOW_CONFIG["label_primary_color"])
        self.name_entry.pack(fill=tk.X, pady=(5, 0), ipady=5)
        
        # 性别选择区域
        gender_container = tk.Frame(info_frame, bg=LOGIN_WINDOW_CONFIG["frame_bg"])
        gender_container.pack(fill=tk.X)
        
        gender_label = tk.Label(gender_container, text="性别", 
                               font=LOGIN_WINDOW_CONFIG["label_font_bold"],
                               bg=LOGIN_WINDOW_CONFIG["frame_bg"], fg=LOGIN_WINDOW_CONFIG["label_primary_color"])
        gender_label.pack(anchor=tk.W)
        
        self.gender_var = tk.StringVar(value=GENDER_MALE)
        gender_frame = tk.Frame(gender_container, bg=LOGIN_WINDOW_CONFIG["frame_bg"])
        gender_frame.pack(anchor=tk.W, pady=(8, 0))
        
        male_radio = tk.Radiobutton(gender_frame, text=GENDER_CONFIG["male"]["text"], variable=self.gender_var, 
                                   value=GENDER_MALE, font=LOGIN_WINDOW_CONFIG["label_font_normal"],
                                   bg=LOGIN_WINDOW_CONFIG["frame_bg"], fg=LOGIN_WINDOW_CONFIG["label_secondary_color"], 
                                   selectcolor=LOGIN_WINDOW_CONFIG["male_color"],
                                   activebackground=LOGIN_WINDOW_CONFIG["frame_bg"],
                                   indicatoron=True)
        male_radio.pack(side=tk.LEFT, padx=(0, 30))
        
        female_radio = tk.Radiobutton(gender_frame, text=GENDER_CONFIG["female"]["text"], variable=self.gender_var, 
                                     value=GENDER_FEMALE, font=LOGIN_WINDOW_CONFIG["label_font_normal"],
                                     bg=LOGIN_WINDOW_CONFIG["frame_bg"], fg=LOGIN_WINDOW_CONFIG["label_secondary_color"], 
                                     selectcolor=LOGIN_WINDOW_CONFIG["female_color"],
                                     activebackground=LOGIN_WINDOW_CONFIG["frame_bg"],
                                     indicatoron=True)
        female_radio.pack(side=tk.LEFT)
        
        # 按钮框架
        button_frame = tk.Frame(main_frame, bg=LOGIN_WINDOW_CONFIG["bg_color"])
        button_frame.pack(fill=tk.X, pady=(0, 25))
        
        # 登录按钮
        self.login_button = CustomButton(button_frame, text=BUTTON_TEXTS["login"], 
                                         command=self.handle_login,
                                         font=LOGIN_WINDOW_CONFIG["section_font"],
                                         bg=LOGIN_WINDOW_CONFIG["login_button_bg"], fg="white",
                                         width=12, height=2)
        self.login_button.pack(side=tk.LEFT, padx=(0, 15), fill=tk.X, expand=True)
        
        # 注册按钮
        self.register_button = CustomButton(button_frame, text=BUTTON_TEXTS["register"], 
                                            command=self.handle_register,
                                            font=LOGIN_WINDOW_CONFIG["section_font"],
                                            bg=LOGIN_WINDOW_CONFIG["register_button_bg"], fg="white",
                                            width=12, height=2)
        self.register_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 已有用户列表
        users_frame = tk.LabelFrame(main_frame, text=LABEL_FRAME_TITLES["existing_users"], 
                                    font=LOGIN_WINDOW_CONFIG["section_font"],
                                    bg=LOGIN_WINDOW_CONFIG["frame_bg"], fg=LOGIN_WINDOW_CONFIG["frame_fg"],
                                    padx=20, pady=15, relief=tk.FLAT, bd=2)
        users_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建滚动区域
        canvas = tk.Canvas(users_frame, bg=LOGIN_WINDOW_CONFIG["frame_bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(users_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.users_cards_frame = tk.Frame(canvas, bg=LOGIN_WINDOW_CONFIG["frame_bg"])
        
        self.users_cards_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.users_cards_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 存储用户卡片
        self.user_cards = []
        
        # 状态栏
        self.status_var = tk.StringVar(value="💡 请输入用户信息或点击选择已有用户")
        status_label = tk.Label(main_frame, textvariable=self.status_var,
                               font=LOGIN_WINDOW_CONFIG["label_font_small"],
                               bg=LOGIN_WINDOW_CONFIG["bg_color"], fg=LOGIN_WINDOW_CONFIG["label_hint_color"])
        status_label.pack(pady=(15, 0))
    
    def center_window(self):
        """窗口居中显示"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def load_existing_users(self):
        """加载已有用户列表"""
        # 清空现有卡片
        for card in self.user_cards:
            card.destroy()
        self.user_cards.clear()
        
        # 加载用户数据
        users = self.data_manager.get_all_users()
        
        if not users:
            # 没有用户时显示提示
            no_user_label = tk.Label(self.users_cards_frame, 
                                     text=UI_TEXTS["no_users"],
                                     font=LOGIN_WINDOW_CONFIG["label_font_normal"],
                                     bg=LOGIN_WINDOW_CONFIG["frame_bg"], fg=LOGIN_WINDOW_CONFIG["label_hint_color"])
            no_user_label.pack(pady=20)
            self.user_cards.append(no_user_label)
            return
        
        for user in users:
            self._create_user_card(user)
    
    def _create_user_card(self, user: User):
        """创建用户卡片"""
        gender_config = GENDER_CONFIG[user.gender]
        gender_text = gender_config["text"]
        gender_icon = gender_config["icon"]
        gender_color = gender_config["color"]
        record_count = len(user.records)
        
        # 创建卡片容器
        card = tk.Frame(self.users_cards_frame, bg=LOGIN_WINDOW_CONFIG["card_bg"], 
                       relief=tk.SOLID, bd=1, cursor="hand2")
        card.pack(fill=tk.X, pady=5, padx=5)
        
        # 内容框架
        content_frame = tk.Frame(card, bg=LOGIN_WINDOW_CONFIG["card_bg"])
        content_frame.pack(fill=tk.X, padx=15, pady=12)
        
        # 左侧：用户信息
        left_frame = tk.Frame(content_frame, bg=LOGIN_WINDOW_CONFIG["card_bg"])
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 用户名和性别
        name_frame = tk.Frame(left_frame, bg=LOGIN_WINDOW_CONFIG["card_bg"])
        name_frame.pack(anchor=tk.W)
        
        name_label = tk.Label(name_frame, text=f"{gender_icon} {user.name}", 
                             font=LOGIN_WINDOW_CONFIG["label_font_normal"],
                             bg=LOGIN_WINDOW_CONFIG["card_bg"], fg=LOGIN_WINDOW_CONFIG["card_text_color"])
        name_label.config(font=(LOGIN_WINDOW_CONFIG["label_font_normal"][0], 12, "bold"))
        name_label.pack(side=tk.LEFT)
        
        gender_badge = tk.Label(name_frame, text=gender_text, 
                               font=LOGIN_WINDOW_CONFIG["label_font_tiny"],
                               bg=gender_color, fg="white",
                               padx=6, pady=2)
        gender_badge.pack(side=tk.LEFT, padx=(8, 0))
        
        # 记录数
        record_label = tk.Label(left_frame, 
                               text=f"📊 已有 {record_count} 条记录",
                               font=LOGIN_WINDOW_CONFIG["label_font_small"],
                               bg=LOGIN_WINDOW_CONFIG["card_bg"], fg=LOGIN_WINDOW_CONFIG["card_hint_color"])
        record_label.pack(anchor=tk.W, pady=(3, 0))
        
        # 右侧：选择按钮
        select_icon = tk.Label(content_frame, text="→", 
                              font=("Arial", 16, "bold"),
                              bg=LOGIN_WINDOW_CONFIG["card_bg"], fg=LOGIN_WINDOW_CONFIG["label_primary_color"])
        select_icon.pack(side=tk.RIGHT)
        
        # 绑定点击事件
        def on_click(event=None):
            self.on_user_card_click(user)
        
        # 悬停效果处理
        def on_enter(event=None):
            hover_bg = LOGIN_WINDOW_CONFIG["card_hover_bg"]
            card.config(bg=hover_bg)
            content_frame.config(bg=hover_bg)
            left_frame.config(bg=hover_bg)
            name_frame.config(bg=hover_bg)
            name_label.config(bg=hover_bg)
            record_label.config(bg=hover_bg)
            select_icon.config(bg=hover_bg)
        
        def on_leave(event=None):
            card_bg = LOGIN_WINDOW_CONFIG["card_bg"]
            card.config(bg=card_bg)
            content_frame.config(bg=card_bg)
            left_frame.config(bg=card_bg)
            name_frame.config(bg=card_bg)
            name_label.config(bg=card_bg)
            record_label.config(bg=card_bg)
            select_icon.config(bg=card_bg)
        
        # 所有组件都绑定事件
        for widget in [card, content_frame, left_frame, name_frame, 
                      name_label, gender_badge, record_label, select_icon]:
            widget.bind("<Button-1>", on_click)
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
        
        self.user_cards.append(card)
    
    def on_user_card_click(self, user: User):
        """点击用户卡片"""
        self.current_user = user
        # 填充表单
        self.name_var.set(user.name)
        self.gender_var.set(user.gender)
        self.status_var.set(UI_TEXTS["selected_user"].format(user.name))
    
    def validate_input(self) -> bool:
        """验证输入数据"""
        # 验证姓名
        is_valid, error_msg = DataValidator.validate_name(self.name_var.get())
        if not is_valid:
            messagebox.showerror(UI_TEXTS["input_error"], error_msg)
            self.name_entry.focus()
            return False
        
        # 验证性别
        is_valid, error_msg = DataValidator.validate_gender(self.gender_var.get())
        if not is_valid:
            messagebox.showerror(UI_TEXTS["input_error"], error_msg)
            return False
        
        return True
    
    def handle_login(self):
        """处理登录"""
        if not self.validate_input():
            return
        
        name = self.name_var.get().strip()
        gender = self.gender_var.get()
        
        # 查找用户
        user = self.data_manager.find_user_by_name(name)
        
        if user:
            # 用户存在，检查信息是否匹配
            if user.gender != gender:
                messagebox.showerror(UI_TEXTS["login_failed"], UI_TEXTS["gender_mismatch"])
                return
            
            self.current_user = user
            self.status_var.set(UI_TEXTS["welcome_back"].format(name))
            
        else:
            # 用户不存在，询问是否注册
            if messagebox.askyesno(UI_TEXTS["user_not_found"], UI_TEXTS["register_prompt"].format(name)):
                self.handle_register()
                return
        
        # 登录成功
        if self.current_user and self.on_login_success:
            self.on_login_success(self.current_user)
            # 关闭登录窗口
            self.window.destroy()
    
    def handle_register(self):
        """处理注册"""
        if not self.validate_input():
            return
        
        name = self.name_var.get().strip()
        gender = self.gender_var.get()
        
        # 检查用户是否已存在
        if self.data_manager.find_user_by_name(name):
            messagebox.showerror(UI_TEXTS["register_failed"], UI_TEXTS["user_exists"].format(name))
            return
        
        # 创建新用户
        user = User(name, gender)
        
        if self.data_manager.add_user(user):
            self.current_user = user
            self.status_var.set(UI_TEXTS["register_success"].format(name))
            self.load_existing_users()  # 刷新用户列表
            
            if self.on_login_success:
                self.on_login_success(self.current_user)
                # 关闭登录窗口
                self.window.destroy()
        else:
            messagebox.showerror(UI_TEXTS["register_failed"], UI_TEXTS["register_error"])
    
    def set_login_callback(self, callback: Callable):
        """设置登录成功回调函数"""
        self.on_login_success = callback
    
    def show(self):
        """显示窗口"""
        self.window.mainloop()
    
    def destroy(self):
        """销毁窗口"""
        if self.window:
            self.window.destroy()

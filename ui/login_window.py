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
from config.constants import GENDER_MALE, GENDER_FEMALE


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
        self.window.title("用户登录 - 体育成绩评估系统")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        
        # 设置窗口居中
        self.center_window()
        
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="体育成绩评估系统", 
                              font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 用户信息输入框架
        info_frame = ttk.LabelFrame(main_frame, text="用户信息", padding="15")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 姓名输入
        ttk.Label(info_frame, text="姓名:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(info_frame, textvariable=self.name_var, width=25)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # 性别选择
        ttk.Label(info_frame, text="性别:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.gender_var = tk.StringVar(value=GENDER_MALE)
        gender_frame = ttk.Frame(info_frame)
        gender_frame.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Radiobutton(gender_frame, text="男", variable=self.gender_var, 
                       value=GENDER_MALE).pack(side=tk.LEFT)
        ttk.Radiobutton(gender_frame, text="女", variable=self.gender_var, 
                       value=GENDER_FEMALE).pack(side=tk.LEFT, padx=(20, 0))
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 登录按钮
        self.login_button = ttk.Button(button_frame, text="登录", 
                                      command=self.handle_login, width=15)
        self.login_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 注册按钮
        self.register_button = ttk.Button(button_frame, text="注册新用户", 
                                        command=self.handle_register, width=15)
        self.register_button.pack(side=tk.LEFT)
        
        # 已有用户列表
        users_frame = ttk.LabelFrame(main_frame, text="已有用户", padding="10")
        users_frame.pack(fill=tk.BOTH, expand=True)
        
        # 用户列表
        columns = ("姓名", "性别", "记录数")
        self.users_tree = ttk.Treeview(users_frame, columns=columns, show="headings", height=8)
        
        # 设置列标题
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=100)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(users_frame, orient=tk.VERTICAL, command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 双击选择用户
        self.users_tree.bind("<Double-1>", self.on_user_double_click)
        
        # 状态栏
        self.status_var = tk.StringVar(value="请输入用户信息或选择已有用户")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                               foreground="gray")
        status_label.pack(pady=(10, 0))
    
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
        # 清空现有数据
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # 加载用户数据
        users = self.data_manager.get_all_users()
        for user in users:
            gender_text = "男" if user.gender == GENDER_MALE else "女"
            record_count = len(user.records)
            
            self.users_tree.insert("", tk.END, values=(
                user.name, gender_text, record_count
            ))
    
    def validate_input(self) -> bool:
        """验证输入数据"""
        # 验证姓名
        is_valid, error_msg = DataValidator.validate_name(self.name_var.get())
        if not is_valid:
            messagebox.showerror("输入错误", error_msg)
            self.name_entry.focus()
            return False
        
        # 验证性别
        is_valid, error_msg = DataValidator.validate_gender(self.gender_var.get())
        if not is_valid:
            messagebox.showerror("输入错误", error_msg)
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
                messagebox.showerror("登录失败", "性别信息不匹配")
                return
            
            self.current_user = user
            self.status_var.set(f"欢迎回来，{name}！")
            
        else:
            # 用户不存在，询问是否注册
            if messagebox.askyesno("用户不存在", f"用户 '{name}' 不存在，是否注册新用户？"):
                self.handle_register()
                return
        
        # 登录成功
        if self.current_user and self.on_login_success:
            self.on_login_success(self.current_user)
    
    def handle_register(self):
        """处理注册"""
        if not self.validate_input():
            return
        
        name = self.name_var.get().strip()
        gender = self.gender_var.get()
        
        # 检查用户是否已存在
        if self.data_manager.find_user_by_name(name):
            messagebox.showerror("注册失败", f"用户 '{name}' 已存在")
            return
        
        # 创建新用户
        user = User(name, gender)
        
        if self.data_manager.add_user(user):
            self.current_user = user
            self.status_var.set(f"注册成功，欢迎 {name}！")
            self.load_existing_users()  # 刷新用户列表
            
            if self.on_login_success:
                self.on_login_success(self.current_user)
        else:
            messagebox.showerror("注册失败", "用户注册失败，请重试")
    
    def on_user_double_click(self, event):
        """双击用户列表项"""
        selection = self.users_tree.selection()
        if not selection:
            return
        
        item = self.users_tree.item(selection[0])
        name = item['values'][0]
        
        # 查找用户
        user = self.data_manager.find_user_by_name(name)
        if user:
            self.current_user = user
            # 填充表单
            self.name_var.set(user.name)
            self.gender_var.set(user.gender)
            self.status_var.set(f"已选择用户: {name}")
    
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

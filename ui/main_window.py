# -*- coding: utf-8 -*-
"""
主窗口
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from typing import Optional
from models.user import User
from ui.login_window import LoginWindow
from ui.input_window import InputWindow
from ui.report_window import ReportWindow
from ui.custom_button import CustomButton
from services.data_manager import DataManager
from utils.data_exporter import DataExporter
from utils.backup_manager import BackupManager
from utils.logger import get_logger
from config.constants import (
    MAIN_WINDOW_CONFIG, WINDOW_SIZES, WINDOW_TITLES,
    BUTTON_TEXTS, LABEL_FRAME_TITLES, UI_TEXTS, DATA_FILE
)

logger = get_logger()


class MainWindow:
    """主窗口类"""
    
    # 上次登录用户配置文件路径（动态获取以支持打包）
    @staticmethod
    def _get_last_user_file():
        """获取上次登录用户配置文件路径"""
        try:
            from utils.path_helper import get_data_file_path
            return get_data_file_path("last_user.json")
        except ImportError:
            return "data/last_user.json"
    
    LAST_USER_FILE = _get_last_user_file.__func__()
    
    def __init__(self):
        logger.info('初始化主窗口')
        self.data_manager = DataManager()
        self.data_exporter = DataExporter()
        self.backup_manager = BackupManager(DATA_FILE)
        self.current_user: Optional[User] = None
        self.report_window_instance = None  # 追踪报告窗口实例
        
        self.setup_ui()
        self.load_last_user()  # 启动时自动加载上次登录的用户
        self.backup_manager.auto_backup()  # 自动备份
    
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
        
        # 导出数据按钮
        self.export_button = CustomButton(button_frame, text="💾 导出数据", 
                                         command=self.show_export_menu,
                                         font=MAIN_WINDOW_CONFIG["button_font"],
                                         bg="#9b59b6", fg="white",
                                         width=8, height=1,
                                         state=tk.DISABLED)
        self.export_button.pack(pady=8, fill=tk.X)
        
        # 备份管理按钮
        self.backup_button = CustomButton(button_frame, text="💾 备份管理", 
                                         command=self.show_backup_menu,
                                         font=MAIN_WINDOW_CONFIG["button_font"],
                                         bg="#34495e", fg="white",
                                         width=8, height=1)
        self.backup_button.pack(pady=8, fill=tk.X)
        
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
            # 强制从文件重新加载所有数据（解决缓存问题）
            self.data_manager.load_data()
            
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
            self.export_button.config(state=tk.NORMAL, bg="#9b59b6",
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
        
        # 检查报告窗口是否已存在
        if self.report_window_instance and hasattr(self.report_window_instance, 'window'):
            try:
                # 检查窗口是否还存在
                if self.report_window_instance.window.winfo_exists():
                    # 窗口存在，刷新数据并置顶
                    self.report_window_instance.refresh_data(self.current_user)
                    self.report_window_instance.window.lift()
                    self.report_window_instance.window.focus_force()
                    return
            except Exception as e:
                # 窗口已销毁，清除引用
                self.report_window_instance = None
        
        # 创建新的报告窗口
        self.report_window_instance = ReportWindow(self.current_user, self.window)
        
        # 绑定窗口关闭事件，清除引用
        def on_close():
            self.report_window_instance.destroy()
            self.report_window_instance = None
        
        self.report_window_instance.window.protocol("WM_DELETE_WINDOW", on_close)
    
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
    
    def show_export_menu(self):
        """显示导出菜单"""
        if not self.current_user:
            messagebox.showerror("错误", "请先登录")
            return
        
        if not self.current_user.records:
            messagebox.showwarning("警告", "暂无成绩记录可导出")
            return
        
        logger.info(f'用户 {self.current_user.name} 准备导出数据')
        
        # 创建菜单窗口
        menu_window = tk.Toplevel(self.window)
        menu_window.title("选择导出格式")
        menu_window.geometry("300x200")
        menu_window.resizable(False, False)
        menu_window.configure(bg=MAIN_WINDOW_CONFIG["bg_color"])
        
        # 居中显示
        menu_window.update_idletasks()
        x = (menu_window.winfo_screenwidth() // 2) - 150
        y = (menu_window.winfo_screenheight() // 2) - 100
        menu_window.geometry(f"300x200+{x}+{y}")
        
        frame = tk.Frame(menu_window, bg=MAIN_WINDOW_CONFIG["bg_color"], padx=30, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="选择导出格式", 
                font=MAIN_WINDOW_CONFIG["section_font"],
                bg=MAIN_WINDOW_CONFIG["bg_color"]).pack(pady=(0, 20))
        
        # CSV导出按钮
        csv_btn = CustomButton(frame, text="📄 导出为 CSV", 
                              command=lambda: self.export_data('csv', menu_window),
                              font=MAIN_WINDOW_CONFIG["button_font"],
                              bg="#3498db", fg="white")
        csv_btn.pack(pady=10, fill=tk.X)
        
        # Excel导出按钮
        excel_btn = CustomButton(frame, text="📊 导出为 Excel", 
                                command=lambda: self.export_data('excel', menu_window),
                                font=MAIN_WINDOW_CONFIG["button_font"],
                                bg="#2ecc71", fg="white")
        excel_btn.pack(pady=10, fill=tk.X)
    
    def export_data(self, format_type: str, menu_window):
        """执行数据导出
        
        Args:
            format_type: 'csv' 或 'excel'
            menu_window: 菜单窗口实例
        """
        try:
            records = self.current_user.get_all_records()
            
            # 选择保存目录
            output_dir = filedialog.askdirectory(title="选择导出目录")
            if not output_dir:
                return
            
            logger.info(f'导出{format_type.upper()}到: {output_dir}')
            
            # 执行导出
            if format_type == 'csv':
                filepath = self.data_exporter.export_to_csv(records, self.current_user.name, output_dir)
            else:  # excel
                filepath = self.data_exporter.export_to_excel(records, self.current_user.name, output_dir)
            
            if filepath:
                menu_window.destroy()
                messagebox.showinfo("导出成功", f"成绩已导出到:\n{filepath}")
                self.status_var.set(f"✅ 数据已导出: {os.path.basename(filepath)}")
            else:
                messagebox.showerror("导出失败", "导出数据时发生错误")
                
        except Exception as e:
            logger.error(f'导出数据失败: {e}', exc_info=True)
            messagebox.showerror("导出失败", f"导出数据时发生错误:\n{str(e)}")
    
    def show_backup_menu(self):
        """显示备份管理菜单"""
        logger.info('打开备份管理界面')
        
        # 创建备份管理窗口
        backup_window = tk.Toplevel(self.window)
        backup_window.title("备份管理")
        backup_window.geometry("500x400")
        backup_window.configure(bg=MAIN_WINDOW_CONFIG["bg_color"])
        
        # 居中显示
        backup_window.update_idletasks()
        x = (backup_window.winfo_screenwidth() // 2) - 250
        y = (backup_window.winfo_screenheight() // 2) - 200
        backup_window.geometry(f"500x400+{x}+{y}")
        
        main_frame = tk.Frame(backup_window, bg=MAIN_WINDOW_CONFIG["bg_color"], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        tk.Label(main_frame, text="💾 备份管理", 
                font=MAIN_WINDOW_CONFIG["title_font"],
                bg=MAIN_WINDOW_CONFIG["bg_color"]).pack(pady=(0, 15))
        
        # 按钮框架
        button_frame = tk.Frame(main_frame, bg=MAIN_WINDOW_CONFIG["bg_color"])
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 创建备份按钮
        create_btn = CustomButton(button_frame, text="➕ 创建新备份", 
                                  command=lambda: self.create_new_backup(backup_window),
                                  font=MAIN_WINDOW_CONFIG["label_font_bold"],
                                  bg="#2ecc71", fg="white", width=12)
        create_btn.pack(side=tk.LEFT, padx=5)
        
        # 刷新按钮
        refresh_btn = CustomButton(button_frame, text="🔄 刷新列表", 
                                   command=lambda: self.refresh_backup_list(backup_window),
                                   font=MAIN_WINDOW_CONFIG["label_font_bold"],
                                   bg="#3498db", fg="white", width=12)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # 备份列表框架
        list_frame = tk.LabelFrame(main_frame, text=" 📋 现有备份 ", 
                                  font=MAIN_WINDOW_CONFIG["label_font_bold"],
                                  bg=MAIN_WINDOW_CONFIG["frame_bg"], 
                                  fg=MAIN_WINDOW_CONFIG["frame_fg"],
                                  padx=10, pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建备份列表（使用Treeview）
        columns = ('文件名', '大小', '创建时间')
        tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=10)
        tree.heading('#0', text='')
        tree.column('#0', width=0, stretch=False)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == '文件名':
                tree.column(col, width=200)
            elif col == '大小':
                tree.column(col, width=80, anchor='center')
            else:
                tree.column(col, width=150, anchor='center')
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 保存tree引用以便刷新
        backup_window.backup_tree = tree
        
        # 加载备份列表
        self.refresh_backup_list(backup_window)
        
        # 操作按钮框架
        action_frame = tk.Frame(main_frame, bg=MAIN_WINDOW_CONFIG["bg_color"])
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 恢复备份按钮
        restore_btn = CustomButton(action_frame, text="⏮ 恢复选中备份", 
                                   command=lambda: self.restore_selected_backup(backup_window),
                                   font=MAIN_WINDOW_CONFIG["label_font_bold"],
                                   bg="#e67e22", fg="white", width=15)
        restore_btn.pack(side=tk.LEFT, padx=5)
        
        # 删除备份按钮
        delete_btn = CustomButton(action_frame, text="🗑 删除选中备份", 
                                  command=lambda: self.delete_selected_backup(backup_window),
                                  font=MAIN_WINDOW_CONFIG["label_font_bold"],
                                  bg="#e74c3c", fg="white", width=15)
        delete_btn.pack(side=tk.LEFT, padx=5)
    
    def create_new_backup(self, backup_window):
        """创建新备份"""
        try:
            backup_path = self.backup_manager.create_backup()
            if backup_path:
                messagebox.showinfo("成功", f"备份创建成功!\n{os.path.basename(backup_path)}")
                self.refresh_backup_list(backup_window)
                self.status_var.set("✅ 备份创建成功")
            else:
                messagebox.showerror("失败", "创建备份失败")
        except Exception as e:
            logger.error(f'创建备份失败: {e}', exc_info=True)
            messagebox.showerror("错误", f"创建备份时发生错误:\n{str(e)}")
    
    def refresh_backup_list(self, backup_window):
        """刷新备份列表"""
        try:
            tree = backup_window.backup_tree
            
            # 清空现有项
            for item in tree.get_children():
                tree.delete(item)
            
            # 获取备份列表
            backups = self.backup_manager.list_backups()
            
            # 添加到树形视图
            for backup in backups:
                tree.insert('', tk.END, values=(
                    backup['name'],
                    backup['formatted_size'],
                    backup['formatted_time']
                ), tags=(backup['path'],))
            
            logger.debug(f'刷新备份列表，共 {len(backups)} 个备份')
            
        except Exception as e:
            logger.error(f'刷新备份列表失败: {e}', exc_info=True)
    
    def restore_selected_backup(self, backup_window):
        """恢复选中的备份"""
        try:
            tree = backup_window.backup_tree
            selection = tree.selection()
            
            if not selection:
                messagebox.showwarning("提示", "请先选择要恢复的备份")
                return
            
            # 获取选中项的路径
            item = selection[0]
            backup_path = tree.item(item)['tags'][0]
            
            # 确认对话框
            if not messagebox.askyesno("确认恢复", 
                                      "恢复备份将覆盖当前数据!\n当前数据会自动备份到'pre_restore_backup'\n\n确定要继续吗?"):
                return
            
            logger.info(f'恢复备份: {backup_path}')
            
            # 执行恢复
            if self.backup_manager.restore_backup(backup_path):
                messagebox.showinfo("成功", "备份恢复成功!\n请重新登录以查看恢复的数据")
                self.status_var.set("✅ 备份已恢复")
                backup_window.destroy()
                
                # 重新加载数据
                self.data_manager.load_data()
                if self.current_user:
                    self.reload_current_user()
                    self.update_ui_after_login()
            else:
                messagebox.showerror("失败", "恢复备份失败")
                
        except Exception as e:
            logger.error(f'恢复备份失败: {e}', exc_info=True)
            messagebox.showerror("错误", f"恢复备份时发生错误:\n{str(e)}")
    
    def delete_selected_backup(self, backup_window):
        """删除选中的备份"""
        try:
            tree = backup_window.backup_tree
            selection = tree.selection()
            
            if not selection:
                messagebox.showwarning("提示", "请先选择要删除的备份")
                return
            
            # 获取选中项的路径
            item = selection[0]
            backup_path = tree.item(item)['tags'][0]
            backup_name = os.path.basename(backup_path)
            
            # 确认对话框
            if not messagebox.askyesno("确认删除", f"确定要删除备份吗?\n{backup_name}"):
                return
            
            logger.info(f'删除备份: {backup_path}')
            
            # 执行删除
            if self.backup_manager.delete_backup(backup_path):
                messagebox.showinfo("成功", "备份已删除")
                self.refresh_backup_list(backup_window)
                self.status_var.set("✅ 备份已删除")
            else:
                messagebox.showerror("失败", "删除备份失败")
                
        except Exception as e:
            logger.error(f'删除备份失败: {e}', exc_info=True)
            messagebox.showerror("错误", f"删除备份时发生错误:\n{str(e)}")
    

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

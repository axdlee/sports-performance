# -*- coding: utf-8 -*-
"""
成绩报告与曲线图界面 - 重构版（标签页架构）
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional
from models.user import User
from services.score_calculator import ScoreCalculator
from utils.chart_generator import ChartGenerator
from config.constants import THEME_COLORS, FONTS, REPORT_WINDOW_SIZE
from ui.tabs import CurrentScoreTab, AnalysisTab, TrendTab, SuggestionsTab


class ReportWindow:
    """成绩报告窗口类 - 重构版（标签页架构）"""
    
    THEME_PRIMARY = THEME_COLORS["primary"]
    THEME_PRIMARY_DARK = THEME_COLORS["primary_dark"]  # 新增
    THEME_BG = THEME_COLORS["bg"]
    THEME_COLORS = THEME_COLORS  # 新增：保存完整的颜色配置供样式使用
    
    def __init__(self, user: User, parent=None):
        self.user = user
        self.parent = parent
        self.score_calculator = ScoreCalculator()
        self.chart_generator = ChartGenerator()
        
        # 标签页实例
        self.current_score_tab = None
        self.analysis_tab = None
        self.trend_tab = None
        self.suggestions_tab = None
        
        self.setup_ui()
        self.load_user_data()
    
    def setup_ui(self):
        """设置用户界面"""
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.window.title(f"📊 成绩报告 - {self.user.name}")
        self.window.geometry(REPORT_WINDOW_SIZE)
        self.window.resizable(True, True)
        self.window.configure(bg=self.THEME_BG)
        
        self.center_window()
        
        # 主容器 - 使用 Canvas 实现背景色
        main_canvas = tk.Canvas(self.window, bg=self.THEME_BG, highlightthickness=0)
        main_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 标题区域 - 使用深色主色调
        title_frame = tk.Frame(main_canvas, bg=self.THEME_PRIMARY, pady=25)
        title_frame.pack(fill=tk.X)
        
        # 标题内容容器
        title_content = tk.Frame(title_frame, bg=self.THEME_PRIMARY)
        title_content.pack()
        
        title_label = tk.Label(title_content, text=f"📊 成绩报告 - {self.user.name}", 
                               font=FONTS["title"],
                               bg=self.THEME_PRIMARY, fg="white")
        title_label.pack()
        
        gender_text = "男生" if self.user.gender == "male" else "女生"
        subtitle_label = tk.Label(title_content, text=f"{gender_text} | Performance Report",
                                 font=FONTS["subtitle"],
                                 bg=self.THEME_PRIMARY, fg="#e0f2f1")
        subtitle_label.pack(pady=(5, 0))
        
        # 内容区域 - 增加内边距
        content_frame = tk.Frame(main_canvas, bg=self.THEME_BG, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 自定义 Notebook 样式
        style = ttk.Style()
        style.theme_use('clam')  # 使用 clam 主题以支持更多自定义
        
        # Notebook 整体样式
        style.configure('Report.TNotebook', background=self.THEME_BG, borderwidth=0)
        style.layout('Report.TNotebook.Tab', [
            ('Notebook.tab', {
                'sticky': 'nswe', 
                'children': [
                    ('Notebook.padding', {
                        'side': 'top', 
                        'sticky': 'nswe',
                        'children': [
                            ('Notebook.label', {'side': 'top', 'sticky': ''})
                        ]
                    })
                ]
            })
        ])
        
        # 标签样式
        style.configure('Report.TNotebook.Tab', 
                       padding=[25, 12], 
                       font=FONTS["section_title"],
                       background=self.THEME_BG,
                       foreground=self.THEME_COLORS["text_light"],
                       borderwidth=0)
                       
        style.map('Report.TNotebook.Tab',
                 background=[('selected', self.THEME_COLORS["card"]), ('active', "#e0f2f1")],
                 foreground=[('selected', self.THEME_PRIMARY), ('active', self.THEME_PRIMARY_DARK)],
                 expand=[('selected', [0, 0, 0, 0])])  # 移除选中时的位移
        
        # 创建 Notebook
        notebook = ttk.Notebook(content_frame, style='Report.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 初始化各标签页
        self.current_score_tab = CurrentScoreTab(notebook, self.user, self.score_calculator)
        notebook.add(self.current_score_tab.frame, text="📈 当前成绩")
        
        self.analysis_tab = AnalysisTab(notebook, self.user, self.score_calculator)
        notebook.add(self.analysis_tab.frame, text="📊 数据分析")
        
        self.trend_tab = TrendTab(notebook, self.user, self.score_calculator)
        notebook.add(self.trend_tab.frame, text="📉 历史趋势")
        
        self.suggestions_tab = SuggestionsTab(notebook, self.user, self.score_calculator)
        notebook.add(self.suggestions_tab.frame, text="💡 训练建议")
    
    def center_window(self):
        """窗口居中显示"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def load_user_data(self):
        """加载用户数据"""
        records = self.user.get_all_records()
        
        if not records:
            self.show_no_data_message()
            return
        
        # 分析数据
        self.analysis_tab.analyze_all_data(records)
        
        # 显示最新成绩
        latest_record = records[-1]
        self.current_score_tab.display_current_score(latest_record)
        
        # 显示数据分析
        self.analysis_tab.display_analysis()
        
        # 显示历史记录
        self.trend_tab.display_history_records(records)
        
        # 渲染趋势图表
        self.trend_tab.render_chart_in_window()
        
        # 生成训练建议
        self.suggestions_tab.display_suggestions(latest_record)
    
    def show_no_data_message(self):
        """显示无数据消息"""
        self.current_score_tab.show_no_data()
        self.analysis_tab.show_no_data()
    
    def refresh_data(self, updated_user: User = None):
        """刷新数据 - 使用最新的用户数据更新报告"""
        if updated_user:
            self.user = updated_user
        
        # 重新加载所有数据
        self.load_user_data()
    
    def show(self):
        """显示窗口"""
        self.window.mainloop()
    
    def destroy(self):
        """销毁窗口"""
        if self.window:
            self.window.destroy()

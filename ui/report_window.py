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
    THEME_BG = THEME_COLORS["bg"]
    
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
        
        main_frame = tk.Frame(self.window, bg=self.THEME_BG, padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题框架
        title_frame = tk.Frame(main_frame, bg=self.THEME_PRIMARY, pady=20)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame, text=f"📊 成绩报告 - {self.user.name}", 
                               font=FONTS["title"],
                               bg=self.THEME_PRIMARY, fg="white")
        title_label.pack()
        
        gender_text = "男生" if self.user.gender == "male" else "女生"
        subtitle_label = tk.Label(title_frame, text=f"{gender_text} | Performance Report",
                                 font=FONTS["subtitle"],
                                 bg=self.THEME_PRIMARY, fg="#ecf0f1")
        subtitle_label.pack(pady=(5, 0))
        
        # 创建笔记本控件（标签页）
        style = ttk.Style()
        style.configure('Report.TNotebook', background=self.THEME_BG)
        style.configure('Report.TNotebook.Tab', padding=[20, 10], font=FONTS["section_title"])
        
        notebook = ttk.Notebook(main_frame, style='Report.TNotebook')
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
        self.suggestions_tab.generate_training_suggestions(latest_record)
    
    def show_no_data_message(self):
        """显示无数据消息"""
        self.current_score_tab.show_no_data()
        self.analysis_tab.show_no_data()
    
    def show(self):
        """显示窗口"""
        self.window.mainloop()
    
    def destroy(self):
        """销毁窗口"""
        if self.window:
            self.window.destroy()

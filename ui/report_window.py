# -*- coding: utf-8 -*-
"""
成绩报告与曲线图界面 - 优化版
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Dict, List
from models.user import User
from services.score_calculator import ScoreCalculator
from utils.chart_generator import ChartGenerator
from config.constants import PROJECT_NAMES
from ui.custom_button import CustomButton
from datetime import datetime
import statistics
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.font_manager as fm


class ReportWindow:
    """成绩报告窗口类 - 优化版"""
    
    # 颜色主题
    THEME_PRIMARY = "#16a085"  # 青绿色主题
    THEME_BG = "#ecf0f1"
    THEME_CARD = "#ffffff"
    THEME_SUCCESS = "#2ecc71"
    THEME_WARNING = "#f39c12"
    THEME_DANGER = "#e74c3c"
    THEME_INFO = "#3498db"
    THEME_TEXT_DARK = "#2c3e50"
    THEME_TEXT_LIGHT = "#7f8c8d"
    
    def __init__(self, user: User, parent=None):
        self.user = user
        self.parent = parent
        self.score_calculator = ScoreCalculator()
        self.chart_generator = ChartGenerator()
        
        # 分析数据缓存
        self.analysis_data = None
        
        self.setup_ui()
        self.load_user_data()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主窗口
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.window.title(f"📊 成绩报告 - {self.user.name}")
        self.window.geometry("1100x800")
        self.window.resizable(True, True)
        self.window.configure(bg=self.THEME_BG)
        
        # 设置窗口居中
        self.center_window()
        
        # 创建主框架
        main_frame = tk.Frame(self.window, bg=self.THEME_BG, padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题框架
        title_frame = tk.Frame(main_frame, bg=self.THEME_PRIMARY, pady=20)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 标题
        title_label = tk.Label(title_frame, text=f"📊 成绩报告 - {self.user.name}", 
                               font=("Microsoft YaHei", 20, "bold"),
                               bg=self.THEME_PRIMARY, fg="white")
        title_label.pack()
        
        gender_text = "男生" if self.user.gender == "male" else "女生"
        subtitle_label = tk.Label(title_frame, text=f"{gender_text} | Performance Report",
                                 font=("Arial", 10),
                                 bg=self.THEME_PRIMARY, fg="#ecf0f1")
        subtitle_label.pack(pady=(5, 0))
        
        # 创建笔记本控件（标签页）
        style = ttk.Style()
        style.configure('Report.TNotebook', background=self.THEME_BG)
        style.configure('Report.TNotebook.Tab', padding=[20, 10], font=("Microsoft YaHei", 11, "bold"))
        
        notebook = ttk.Notebook(main_frame, style='Report.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 📈 当前成绩标签页
        self.setup_current_score_tab(notebook)
        
        # 📊 数据分析标签页
        self.setup_analysis_tab(notebook)
        
        # 📉 历史趋势标签页
        self.setup_trend_tab(notebook)
        
        # 💡 训练建议标签页
        self.setup_suggestions_tab(notebook)
    
    def center_window(self):
        """窗口居中显示"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_card_frame(self, parent, title, title_color=None):
        """创建卡片框架"""
        card = tk.Frame(parent, bg=self.THEME_CARD, relief=tk.FLAT, bd=0)
        
        # 卡片标题
        if title_color is None:
            title_color = self.THEME_PRIMARY
        
        title_frame = tk.Frame(card, bg=title_color, height=40)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text=title, 
                              font=("Microsoft YaHei", 12, "bold"),
                              bg=title_color, fg="white", anchor="w", padx=15)
        title_label.pack(fill=tk.BOTH, expand=True)
        
        # 卡片内容区域
        content = tk.Frame(card, bg=self.THEME_CARD, padx=15, pady=15)
        content.pack(fill=tk.BOTH, expand=True)
        
        return card, content
    
    def setup_current_score_tab(self, notebook):
        """设置当前成绩标签页"""
        # 创建滚动框架
        current_frame = tk.Frame(notebook, bg=self.THEME_BG)
        notebook.add(current_frame, text="📈 当前成绩")
        
        # 创建Canvas和Scrollbar
        canvas = tk.Canvas(current_frame, bg=self.THEME_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(current_frame, orient="vertical", command=canvas.yview)
        
        # 创建可滚动框架 - 使用居中布局但不限制高度
        scrollable_frame = tk.Frame(canvas, bg=self.THEME_BG, padx=180, pady=15)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 绑定鼠标滚轮事件
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 成绩概览卡片
        overview_card, overview_content = self.create_card_frame(scrollable_frame, "🎯 成绩概览")
        overview_card.pack(fill=tk.X, pady=(0, 15))
        
        # 分数显示框架（横向）
        scores_frame = tk.Frame(overview_content, bg=self.THEME_CARD)
        scores_frame.pack(fill=tk.X)
        
        # 总分
        total_frame = tk.Frame(scores_frame, bg=self.THEME_PRIMARY, padx=20, pady=15)
        total_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(total_frame, text="总分 Total Score", 
                font=("Microsoft YaHei", 10), bg=self.THEME_PRIMARY, fg="white").pack()
        self.total_score_var = tk.StringVar(value="--")
        tk.Label(total_frame, textvariable=self.total_score_var, 
                font=("Arial", 32, "bold"), bg=self.THEME_PRIMARY, fg="white").pack(pady=(5, 0))
        
        # 等级
        grade_frame = tk.Frame(scores_frame, bg=self.THEME_INFO, padx=20, pady=15)
        grade_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(grade_frame, text="等级 Grade", 
                font=("Microsoft YaHei", 10), bg=self.THEME_INFO, fg="white").pack()
        self.grade_var = tk.StringVar(value="--")
        tk.Label(grade_frame, textvariable=self.grade_var, 
                font=("Microsoft YaHei", 24, "bold"), bg=self.THEME_INFO, fg="white").pack(pady=(5, 0))
        
        # 测试日期
        date_frame = tk.Frame(overview_content, bg=self.THEME_CARD, )
        date_frame.pack(fill=tk.X, pady=(10, 0))
        self.test_date_var = tk.StringVar(value="测试日期: --")
        tk.Label(date_frame, textvariable=self.test_date_var, 
                font=("Microsoft YaHei", 10), bg=self.THEME_CARD, 
                fg=self.THEME_TEXT_LIGHT).pack(anchor="w")
        
        # 详细成绩卡片
        details_card, details_content = self.create_card_frame(scrollable_frame, "📋 详细成绩")
        details_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 成绩列表容器
        self.score_items_frame = tk.Frame(details_content, bg=self.THEME_CARD)
        self.score_items_frame.pack(fill=tk.BOTH, expand=True)
        
        # 快速分析卡片
        quick_analysis_card, quick_analysis_content = self.create_card_frame(
            scrollable_frame, "⚡ 快速分析", self.THEME_WARNING)
        quick_analysis_card.pack(fill=tk.X, pady=(0, 15))
        
        # 最强项和最弱项
        analysis_frame = tk.Frame(quick_analysis_content, bg=self.THEME_CARD)
        analysis_frame.pack(fill=tk.X)
        
        # 最强项
        strong_frame = tk.Frame(analysis_frame, bg="#d5f4e6", padx=15, pady=10, relief=tk.FLAT, bd=1)
        strong_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(strong_frame, text="💪 最强项", font=("Microsoft YaHei", 10, "bold"),
                bg="#d5f4e6", fg=self.THEME_SUCCESS).pack(anchor="w")
        self.strongest_var = tk.StringVar(value="--")
        tk.Label(strong_frame, textvariable=self.strongest_var, 
                font=("Microsoft YaHei", 12), bg="#d5f4e6", 
                fg=self.THEME_TEXT_DARK).pack(anchor="w", pady=(5, 0))
        
        # 最弱项
        weak_frame = tk.Frame(analysis_frame, bg="#fadbd8", padx=15, pady=10, relief=tk.FLAT, bd=1)
        weak_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(weak_frame, text="⚠️ 最弱项", font=("Microsoft YaHei", 10, "bold"),
                bg="#fadbd8", fg=self.THEME_DANGER).pack(anchor="w")
        self.weakest_var = tk.StringVar(value="--")
        tk.Label(weak_frame, textvariable=self.weakest_var, 
                font=("Microsoft YaHei", 12), bg="#fadbd8", 
                fg=self.THEME_TEXT_DARK).pack(anchor="w", pady=(5, 0))
    
    def setup_analysis_tab(self, notebook):
        """设置数据分析标签页"""
        analysis_frame = tk.Frame(notebook, bg=self.THEME_BG)
        notebook.add(analysis_frame, text="📊 数据分析")
        
        # 创建Canvas和Scrollbar
        canvas = tk.Canvas(analysis_frame, bg=self.THEME_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(analysis_frame, orient="vertical", command=canvas.yview)
        
        # 创建可滚动框架 - 使用居中布局但不限制高度
        scrollable_frame = tk.Frame(canvas, bg=self.THEME_BG, padx=180, pady=15)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 绑定鼠标滚轮
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 统计概览卡片
        stats_card, stats_content = self.create_card_frame(scrollable_frame, "📈 统计概览")
        stats_card.pack(fill=tk.X, pady=(0, 15))
        
        # 统计数据网格
        stats_grid = tk.Frame(stats_content, bg=self.THEME_CARD)
        stats_grid.pack(fill=tk.X)
        
        self.stats_vars = {}
        stats_items = [
            ("record_count", "测试次数", self.THEME_INFO),
            ("avg_score", "平均分", self.THEME_PRIMARY),
            ("best_score", "最高分", self.THEME_SUCCESS),
            ("worst_score", "最低分", self.THEME_DANGER),
            ("improvement", "进步幅度", self.THEME_WARNING),
            ("trend", "成绩趋势", self.THEME_INFO)
        ]
        
        for i, (key, label, color) in enumerate(stats_items):
            row = i // 3
            col = i % 3
            
            stat_frame = tk.Frame(stats_grid, bg=color, padx=15, pady=12)
            stat_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            tk.Label(stat_frame, text=label, font=("Microsoft YaHei", 9),
                    bg=color, fg="white").pack()
            
            var = tk.StringVar(value="--")
            self.stats_vars[key] = var
            tk.Label(stat_frame, textvariable=var, font=("Microsoft YaHei", 16, "bold"),
                    bg=color, fg="white").pack(pady=(3, 0))
        
        # 配置网格权重
        for i in range(3):
            stats_grid.columnconfigure(i, weight=1)
        
        # 历史记录对比卡片
        compare_card, compare_content = self.create_card_frame(scrollable_frame, "📊 最佳与最差记录对比")
        compare_card.pack(fill=tk.X, pady=(0, 15))
        
        self.compare_frame = tk.Frame(compare_content, bg=self.THEME_CARD)
        self.compare_frame.pack(fill=tk.BOTH, expand=True)
        
        # 各项目分析卡片
        projects_card, projects_content = self.create_card_frame(scrollable_frame, "🎯 各项目成绩分析")
        projects_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.projects_analysis_frame = tk.Frame(projects_content, bg=self.THEME_CARD)
        self.projects_analysis_frame.pack(fill=tk.BOTH, expand=True)
    
    def setup_trend_tab(self, notebook):
        """设置历史趋势标签页"""
        trend_frame = tk.Frame(notebook, bg=self.THEME_BG, padx=15, pady=15)
        notebook.add(trend_frame, text="📉 历史趋势")
        
        # 趋势图表卡片
        chart_card, chart_content = self.create_card_frame(trend_frame, "📈 成绩趋势图")
        chart_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 图表容器
        self.chart_frame = tk.Frame(chart_content, bg=self.THEME_CARD, height=400)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        self.chart_frame.pack_propagate(False)
        
        # 提示标签（图表未生成时显示）
        self.chart_placeholder = tk.Label(
            self.chart_frame, 
            text="加载中...",
            font=("Microsoft YaHei", 12),
            bg=self.THEME_CARD,
            fg=self.THEME_TEXT_LIGHT
        )
        self.chart_placeholder.place(relx=0.5, rely=0.5, anchor="center")
        
        # 控制按钮框架
        button_frame = tk.Frame(chart_content, bg=self.THEME_CARD)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 刷新图表按钮
        refresh_btn = CustomButton(button_frame, text="🔄 刷新图表", 
                                   command=self.refresh_chart,
                                   font=("Microsoft YaHei", 10, "bold"),
                                   bg=self.THEME_PRIMARY, fg="white",
                                   width=10, height=1,
                                   activebackground="#138d75")
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 导出图表按钮
        export_btn = CustomButton(button_frame, text="💾 导出图表", 
                                 command=self.export_chart,
                                 font=("Microsoft YaHei", 10, "bold"),
                                 bg=self.THEME_INFO, fg="white",
                                 width=10, height=1,
                                 activebackground="#2874a6")
        export_btn.pack(side=tk.LEFT)
        
        # 历史记录卡片
        history_card, history_content = self.create_card_frame(trend_frame, "📜 历史记录列表")
        history_card.pack(fill=tk.BOTH, expand=True)
        
        # 历史记录表格
        columns = ("序号", "日期", "必选项", "第一类", "第二类", "总分", "等级")
        self.history_tree = ttk.Treeview(history_content, columns=columns, show="headings", height=15)
        
        # 设置列
        self.history_tree.heading("序号", text="序号")
        self.history_tree.heading("日期", text="日期")
        self.history_tree.heading("必选项", text="必选项")
        self.history_tree.heading("第一类", text="第一类选考")
        self.history_tree.heading("第二类", text="第二类选考")
        self.history_tree.heading("总分", text="总分")
        self.history_tree.heading("等级", text="等级")
        
        self.history_tree.column("序号", width=50, anchor="center")
        self.history_tree.column("日期", width=120, anchor="center")
        self.history_tree.column("必选项", width=80, anchor="center")
        self.history_tree.column("第一类", width=80, anchor="center")
        self.history_tree.column("第二类", width=80, anchor="center")
        self.history_tree.column("总分", width=80, anchor="center")
        self.history_tree.column("等级", width=100, anchor="center")
        
        # 滚动条
        history_scrollbar = ttk.Scrollbar(history_content, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_suggestions_tab(self, notebook):
        """设置训练建议标签页"""
        suggestions_frame = tk.Frame(notebook, bg=self.THEME_BG)
        notebook.add(suggestions_frame, text="💡 训练建议")
        
        # 创建Canvas和Scrollbar
        canvas = tk.Canvas(suggestions_frame, bg=self.THEME_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(suggestions_frame, orient="vertical", command=canvas.yview)
        
        # 创建可滚动框架 - 使用居中布局但不限制高度
        scrollable_frame = tk.Frame(canvas, bg=self.THEME_BG, padx=130, pady=15)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 绑定鼠标滚轮
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 总体评价卡片
        overall_card, overall_content = self.create_card_frame(scrollable_frame, "🎯 总体评价")
        overall_card.pack(fill=tk.X, pady=(0, 15))
        
        self.overall_text = tk.Text(overall_content, wrap=tk.WORD, height=4, 
                                   font=("Microsoft YaHei", 11), bg=self.THEME_CARD, 
                                   fg=self.THEME_TEXT_DARK, relief=tk.FLAT, state=tk.DISABLED)
        self.overall_text.pack(fill=tk.X)
        
        # 弱项针对性建议卡片
        weakness_card, weakness_content = self.create_card_frame(
            scrollable_frame, "⚠️ 弱项针对性建议", self.THEME_DANGER)
        weakness_card.pack(fill=tk.X, pady=(0, 15))
        
        self.weakness_text = tk.Text(weakness_content, wrap=tk.WORD, height=6, 
                                    font=("Microsoft YaHei", 10), bg=self.THEME_CARD, 
                                    fg=self.THEME_TEXT_DARK, relief=tk.FLAT, state=tk.DISABLED)
        self.weakness_text.pack(fill=tk.BOTH, expand=True)
        
        # 各项目训练计划卡片
        training_card, training_content = self.create_card_frame(scrollable_frame, "📋 分项训练计划")
        training_card.pack(fill=tk.X, pady=(0, 15))
        
        self.training_frame = tk.Frame(training_content, bg=self.THEME_CARD)
        self.training_frame.pack(fill=tk.BOTH, expand=True)
        
        # 生活建议卡片
        life_card, life_content = self.create_card_frame(
            scrollable_frame, "🌟 生活与训练建议", self.THEME_SUCCESS)
        life_card.pack(fill=tk.X, pady=(0, 15))
        
        self.life_text = tk.Text(life_content, wrap=tk.WORD, height=8, 
                                font=("Microsoft YaHei", 10), bg=self.THEME_CARD, 
                                fg=self.THEME_TEXT_DARK, relief=tk.FLAT, state=tk.DISABLED)
        self.life_text.pack(fill=tk.BOTH, expand=True)
    
    def load_user_data(self):
        """加载用户数据"""
        records = self.user.get_all_records()
        
        if not records:
            self.show_no_data_message()
            return
        
        # 分析数据
        self.analyze_all_data(records)
        
        # 显示最新成绩
        latest_record = records[-1]
        self.display_current_score(latest_record)
        
        # 显示数据分析
        self.display_analysis()
        
        # 显示历史记录
        self.display_history_records(records)
        
        # 渲染趋势图表
        self.render_chart_in_window()
        
        # 生成训练建议
        self.generate_training_suggestions(latest_record)
    
    def show_no_data_message(self):
        """显示无数据消息"""
        self.total_score_var.set("--")
        self.grade_var.set("暂无数据")
        self.test_date_var.set("测试日期: --")
        self.strongest_var.set("暂无数据")
        self.weakest_var.set("暂无数据")
        
        for var in self.stats_vars.values():
            var.set("--")
    
    def analyze_all_data(self, records: List[Dict]):
        """分析所有历史数据"""
        if not records:
            self.analysis_data = None
            return
        
        analysis = {
            "record_count": len(records),
            "scores": [r["scores"]["total"] for r in records],
            "dates": [r["date"] for r in records]
        }
        
        # 统计数据
        analysis["avg_score"] = statistics.mean(analysis["scores"])
        analysis["best_score"] = max(analysis["scores"])
        analysis["worst_score"] = min(analysis["scores"])
        analysis["best_record"] = max(records, key=lambda r: r["scores"]["total"])
        analysis["worst_record"] = min(records, key=lambda r: r["scores"]["total"])
        
        # 进步幅度
        if len(records) >= 2:
            first_score = records[0]["scores"]["total"]
            latest_score = records[-1]["scores"]["total"]
            analysis["improvement"] = latest_score - first_score
            analysis["improvement_percent"] = (analysis["improvement"] / first_score * 100) if first_score > 0 else 0
            
            # 趋势分析
            if analysis["improvement"] > 1:
                analysis["trend"] = "上升"
                analysis["trend_emoji"] = "📈"
            elif analysis["improvement"] < -1:
                analysis["trend"] = "下降"
                analysis["trend_emoji"] = "📉"
            else:
                analysis["trend"] = "稳定"
                analysis["trend_emoji"] = "➡️"
        else:
            analysis["improvement"] = 0
            analysis["improvement_percent"] = 0
            analysis["trend"] = "首次"
            analysis["trend_emoji"] = "🎯"
        
        # 各项目分析
        analysis["projects"] = self.analyze_projects(records)
        
        self.analysis_data = analysis
    
    def analyze_projects(self, records: List[Dict]) -> Dict:
        """分析各项目成绩"""
        projects = {}
        
        for record in records:
            # 必选项
            req_key = list(record["required"].keys())[0]
            if req_key not in projects:
                projects[req_key] = {"scores": [], "performances": []}
            projects[req_key]["scores"].append(record["scores"]["required"])
            projects[req_key]["performances"].append(record["required"][req_key])
            
            # 第一类选考
            cat1_key = list(record["category1"].keys())[0]
            if cat1_key not in projects:
                projects[cat1_key] = {"scores": [], "performances": []}
            projects[cat1_key]["scores"].append(record["scores"]["category1"])
            projects[cat1_key]["performances"].append(record["category1"][cat1_key])
            
            # 第二类选考
            cat2_key = list(record["category2"].keys())[0]
            if cat2_key not in projects:
                projects[cat2_key] = {"scores": [], "performances": []}
            projects[cat2_key]["scores"].append(record["scores"]["category2"])
            projects[cat2_key]["performances"].append(record["category2"][cat2_key])
        
        # 计算每个项目的统计数据
        for key, data in projects.items():
            data["avg_score"] = statistics.mean(data["scores"])
            data["best_score"] = max(data["scores"])
            data["best_performance"] = data["performances"][data["scores"].index(data["best_score"])]
            
            if len(data["scores"]) >= 2:
                data["improvement"] = data["scores"][-1] - data["scores"][0]
            else:
                data["improvement"] = 0
        
        return projects
    
    def display_current_score(self, record: Dict):
        """显示当前成绩"""
        scores = record["scores"]
        total_score = scores["total"]
        
        # 更新总分和等级
        self.total_score_var.set(f"{total_score:.1f}")
        grade = self.score_calculator.get_grade_level(total_score)
        self.grade_var.set(grade)
        
        # 更新测试日期
        self.test_date_var.set(f"测试日期: {record['date']}")
        
        # 清空现有成绩项
        for widget in self.score_items_frame.winfo_children():
            widget.destroy()
        
        # 显示各项成绩
        items = [
            ("必选项", record["required"], scores["required"]),
            ("第一类选考", record["category1"], scores["category1"]),
            ("第二类选考", record["category2"], scores["category2"])
        ]
        
        for category, performance, score in items:
            self.create_score_item(category, performance, score)
        
        # 更新最强项和最弱项
        weakest = self.score_calculator.get_weakest_item(scores)
        strongest = self.score_calculator.get_strongest_item(scores)
        
        if weakest:
            weakest_name = self.get_item_display_name(weakest)
            weakest_score = scores[weakest]
            self.weakest_var.set(f"{weakest_name} ({weakest_score:.1f}分)")
        
        if strongest:
            strongest_name = self.get_item_display_name(strongest)
            strongest_score = scores[strongest]
            self.strongest_var.set(f"{strongest_name} ({strongest_score:.1f}分)")
    
    def create_score_item(self, category: str, performance: Dict, score: float):
        """创建成绩项显示"""
        project_key = list(performance.keys())[0]
        project_name = PROJECT_NAMES.get(project_key, project_key)
        performance_value = list(performance.values())[0]
        
        # 格式化成绩显示
        formatted_value = self.format_performance(project_key, performance_value)
        
        # 确定颜色
        if score >= 9:
            color = self.THEME_SUCCESS
            status = "优秀"
        elif score >= 7:
            color = self.THEME_INFO
            status = "良好"
        elif score >= 5:
            color = self.THEME_WARNING
            status = "中等"
        else:
            color = self.THEME_DANGER
            status = "需改进"
        
        # 创建项目框架
        item_frame = tk.Frame(self.score_items_frame, bg=self.THEME_CARD, pady=5)
        item_frame.pack(fill=tk.X, pady=3)
        
        # 左侧：项目信息
        left_frame = tk.Frame(item_frame, bg=self.THEME_CARD)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left_frame, text=f"{category} - {project_name}", 
                font=("Microsoft YaHei", 11, "bold"), 
                bg=self.THEME_CARD, fg=self.THEME_TEXT_DARK, anchor="w").pack(anchor="w")
        
        tk.Label(left_frame, text=f"成绩: {formatted_value}", 
                font=("Microsoft YaHei", 9), 
                bg=self.THEME_CARD, fg=self.THEME_TEXT_LIGHT, anchor="w").pack(anchor="w")
        
        # 右侧：分数和状态
        right_frame = tk.Frame(item_frame, bg=color, padx=15, pady=5)
        right_frame.pack(side=tk.RIGHT)
        
        tk.Label(right_frame, text=f"{score:.1f}分", 
                font=("Microsoft YaHei", 14, "bold"), 
                bg=color, fg="white").pack()
        
        tk.Label(right_frame, text=status, 
                font=("Microsoft YaHei", 9), 
                bg=color, fg="white").pack()
        
        # 分隔线
        tk.Frame(self.score_items_frame, bg=self.THEME_BG, height=1).pack(fill=tk.X, pady=2)
    
    def format_performance(self, project_key: str, performance_value: float) -> str:
        """格式化成绩显示"""
        if project_key in ["1000m", "800m", "50m", "basketball", "football"]:
            if project_key in ["1000m", "800m"]:
                # 长跑：显示分:秒格式
                minutes = int(performance_value // 60)
                seconds = int(performance_value % 60)
                return f"{minutes}'{seconds}\""
            elif project_key == "50m":
                return f"{performance_value:.1f}秒"
            else:
                return f"{performance_value:.1f}秒"
        elif project_key in ["sit_reach", "standing_jump"]:
            return f"{performance_value:.1f}厘米"
        else:
            return f"{int(performance_value)}次"
    
    def display_analysis(self):
        """显示数据分析"""
        if not self.analysis_data:
            return
        
        data = self.analysis_data
        
        # 更新统计数据
        self.stats_vars["record_count"].set(f"{data['record_count']}次")
        self.stats_vars["avg_score"].set(f"{data['avg_score']:.1f}")
        self.stats_vars["best_score"].set(f"{data['best_score']:.1f}")
        self.stats_vars["worst_score"].set(f"{data['worst_score']:.1f}")
        
        if data["improvement"] >= 0:
            self.stats_vars["improvement"].set(f"+{data['improvement']:.1f}")
        else:
            self.stats_vars["improvement"].set(f"{data['improvement']:.1f}")
        
        self.stats_vars["trend"].set(f"{data['trend_emoji']} {data['trend']}")
        
        # 显示最佳与最差记录对比
        self.display_record_comparison()
        
        # 显示各项目分析
        self.display_projects_analysis()
    
    def display_record_comparison(self):
        """显示最佳与最差记录对比"""
        if not self.analysis_data:
            return
        
        # 清空现有内容
        for widget in self.compare_frame.winfo_children():
            widget.destroy()
        
        best = self.analysis_data["best_record"]
        worst = self.analysis_data["worst_record"]
        
        # 最佳记录
        best_frame = tk.Frame(self.compare_frame, bg="#d5f4e6", padx=15, pady=10, relief=tk.FLAT, bd=1)
        best_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(best_frame, text="🏆 最佳记录", font=("Microsoft YaHei", 11, "bold"),
                bg="#d5f4e6", fg=self.THEME_SUCCESS).pack(anchor="w")
        
        tk.Label(best_frame, text=f"日期: {best['date']}", font=("Microsoft YaHei", 9),
                bg="#d5f4e6", fg=self.THEME_TEXT_DARK).pack(anchor="w", pady=(5, 0))
        
        tk.Label(best_frame, text=f"总分: {best['scores']['total']:.1f}", 
                font=("Microsoft YaHei", 14, "bold"),
                bg="#d5f4e6", fg=self.THEME_SUCCESS).pack(anchor="w", pady=(2, 0))
        
        # 最差记录
        worst_frame = tk.Frame(self.compare_frame, bg="#fadbd8", padx=15, pady=10, relief=tk.FLAT, bd=1)
        worst_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(worst_frame, text="📉 最低记录", font=("Microsoft YaHei", 11, "bold"),
                bg="#fadbd8", fg=self.THEME_DANGER).pack(anchor="w")
        
        tk.Label(worst_frame, text=f"日期: {worst['date']}", font=("Microsoft YaHei", 9),
                bg="#fadbd8", fg=self.THEME_TEXT_DARK).pack(anchor="w", pady=(5, 0))
        
        tk.Label(worst_frame, text=f"总分: {worst['scores']['total']:.1f}", 
                font=("Microsoft YaHei", 14, "bold"),
                bg="#fadbd8", fg=self.THEME_DANGER).pack(anchor="w", pady=(2, 0))
    
    def display_projects_analysis(self):
        """显示各项目分析"""
        if not self.analysis_data or "projects" not in self.analysis_data:
            return
        
        # 清空现有内容
        for widget in self.projects_analysis_frame.winfo_children():
            widget.destroy()
        
        projects = self.analysis_data["projects"]
        
        for project_key, data in projects.items():
            project_name = PROJECT_NAMES.get(project_key, project_key)
            
            # 项目框架
            project_frame = tk.Frame(self.projects_analysis_frame, bg="#f8f9fa", 
                                    padx=12, pady=10, relief=tk.FLAT, bd=1)
            project_frame.pack(fill=tk.X, pady=5)
            
            # 项目名称和平均分
            header_frame = tk.Frame(project_frame, bg="#f8f9fa")
            header_frame.pack(fill=tk.X)
            
            tk.Label(header_frame, text=project_name, font=("Microsoft YaHei", 11, "bold"),
                    bg="#f8f9fa", fg=self.THEME_TEXT_DARK).pack(side=tk.LEFT)
            
            tk.Label(header_frame, text=f"平均: {data['avg_score']:.1f}分", 
                    font=("Microsoft YaHei", 10),
                    bg="#f8f9fa", fg=self.THEME_PRIMARY).pack(side=tk.RIGHT)
            
            # 详细信息
            info_frame = tk.Frame(project_frame, bg="#f8f9fa")
            info_frame.pack(fill=tk.X, pady=(5, 0))
            
            best_perf = self.format_performance(project_key, data['best_performance'])
            tk.Label(info_frame, text=f"最佳: {data['best_score']:.1f}分 ({best_perf})", 
                    font=("Microsoft YaHei", 9),
                    bg="#f8f9fa", fg=self.THEME_TEXT_LIGHT).pack(side=tk.LEFT)
            
            if data['improvement'] > 0:
                improvement_text = f"进步: +{data['improvement']:.1f}分 📈"
                color = self.THEME_SUCCESS
            elif data['improvement'] < 0:
                improvement_text = f"退步: {data['improvement']:.1f}分 📉"
                color = self.THEME_DANGER
            else:
                improvement_text = "稳定 ➡️"
                color = self.THEME_INFO
            
            tk.Label(info_frame, text=improvement_text, font=("Microsoft YaHei", 9),
                    bg="#f8f9fa", fg=color).pack(side=tk.RIGHT)
    
    def display_history_records(self, records: List[Dict]):
        """显示历史记录"""
        # 清空现有数据
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # 按日期排序（最新的在前）
        sorted_records = sorted(records, key=lambda x: x["date"], reverse=True)
        
        for idx, record in enumerate(sorted_records, 1):
            date = record["date"]
            required_score = record["scores"]["required"]
            category1_score = record["scores"]["category1"]
            category2_score = record["scores"]["category2"]
            total_score = record["scores"]["total"]
            grade = self.score_calculator.get_grade_level(total_score)
            
            self.history_tree.insert("", tk.END, values=(
                idx, date, f"{required_score:.1f}", f"{category1_score:.1f}", 
                f"{category2_score:.1f}", f"{total_score:.1f}", grade
            ))
    
    def generate_training_suggestions(self, record: Dict):
        """生成训练建议"""
        scores = record["scores"]
        total_score = scores["total"]
        
        # 总体评价
        self.overall_text.config(state=tk.NORMAL)
        self.overall_text.delete(1.0, tk.END)
        
        overall_text = self.get_overall_evaluation(total_score)
        self.overall_text.insert(1.0, overall_text)
        self.overall_text.config(state=tk.DISABLED)
        
        # 弱项建议
        weakest = self.score_calculator.get_weakest_item(scores)
        
        self.weakness_text.config(state=tk.NORMAL)
        self.weakness_text.delete(1.0, tk.END)
        
        if weakest:
            weakness_suggestions = self.get_weakness_suggestions(weakest, scores[weakest])
            self.weakness_text.insert(1.0, weakness_suggestions)
        else:
            self.weakness_text.insert(1.0, "各项成绩均衡，继续保持！")
        
        self.weakness_text.config(state=tk.DISABLED)
        
        # 分项训练计划
        self.display_training_plan(scores)
        
        # 生活建议
        self.life_text.config(state=tk.NORMAL)
        self.life_text.delete(1.0, tk.END)
        
        life_suggestions = self.get_life_suggestions(total_score)
        self.life_text.insert(1.0, life_suggestions)
        self.life_text.config(state=tk.DISABLED)
    
    def get_overall_evaluation(self, total_score: float) -> str:
        """获取总体评价"""
        if total_score >= 27:
            return ("🎉 恭喜！您的体育成绩非常优秀！您已经达到了很高的运动水平，各项指标都很出色。"
                   "建议继续保持当前的训练强度，并可以尝试挑战更高的目标。保持良好的运动习惯，"
                   "注意预防运动损伤，您可以成为同学们的榜样！")
        elif total_score >= 24:
            return ("👍 您的体育成绩良好！整体表现不错，但还有进步的空间。通过针对性训练，"
                   "您完全有能力达到优秀水平。建议重点提升得分较低的项目，同时保持强项的训练。"
                   "坚持科学训练，相信您很快就能突破到更高层次！")
        elif total_score >= 18:
            return ("📈 您的体育成绩处于中等水平。这说明您具备基本的运动能力，但需要加强系统训练。"
                   "建议制定详细的训练计划，每周至少进行3-4次针对性练习。提高成绩的关键在于持之以恒，"
                   "注意训练的科学性和规律性。加油，您一定能够取得明显进步！")
        elif total_score >= 15:
            return ("⚠️ 您的体育成绩刚达到及格线，需要重点加强训练。建议从最弱的项目入手，"
                   "制定循序渐进的训练计划。不要急于求成，先打好基础，逐步提高。可以寻求体育老师或教练的指导，"
                   "采用更科学的训练方法。相信通过努力，您的成绩会有显著提升！")
        else:
            return ("🚨 您的体育成绩目前不及格，需要系统性的改进和提升。建议立即开始规律的体育锻炼，"
                   "从基础训练做起。可以先设定小目标，比如每周进步一点点。强烈建议咨询专业教练，"
                   "制定个性化的训练方案。记住，万事开头难，只要开始行动并坚持下去，一定会看到成效！")
    
    def get_weakness_suggestions(self, weakest_item: str, score: float) -> str:
        """获取弱项针对性建议"""
        item_name = self.get_item_display_name(weakest_item)
        base_suggestion = self.score_calculator.get_improvement_suggestions(weakest_item, self.user.gender)
        
        # 根据得分程度给出更详细的建议
        if score < 3:
            intensity = "您在该项目上的得分很低，需要从基础开始系统训练。\n\n"
            frequency = "建议每周训练4-5次，每次30-40分钟。"
        elif score < 5:
            intensity = "您在该项目上还有较大提升空间，需要加强专项训练。\n\n"
            frequency = "建议每周训练3-4次，每次25-35分钟。"
        elif score < 7:
            intensity = "您在该项目上已有一定基础，需要针对性提高。\n\n"
            frequency = "建议每周训练2-3次，每次20-30分钟。"
        else:
            intensity = "您在该项目上表现尚可，可以进一步优化。\n\n"
            frequency = "建议每周训练2次，每次15-25分钟。"
        
        detailed_training = self.get_detailed_training_plan(weakest_item)
        
        return f"【{item_name}】当前得分: {score:.1f}/10.0\n\n{intensity}{base_suggestion}\n\n{frequency}\n\n{detailed_training}"
    
    def get_detailed_training_plan(self, project_key: str) -> str:
        """获取详细训练计划"""
        plans = {
            "1000m": "训练计划:\n• 第1-2周: 慢跑800米 x 3组,间歇3分钟\n• 第3-4周: 慢跑1000米 x 2组,间歇5分钟\n• 第5-6周: 节奏跑1000米 x 2组,提升配速\n• 第7-8周: 全力跑1000米,争取突破",
            "800m": "训练计划:\n• 第1-2周: 慢跑600米 x 3组,间歇3分钟\n• 第3-4周: 慢跑800米 x 2组,间歇4分钟\n• 第5-6周: 节奏跑800米 x 2组,提升配速\n• 第7-8周: 全力跑800米,争取突破",
            "50m": "训练计划:\n• 起跑练习: 蹲踞式起跑30次/天\n• 加速跑: 30米冲刺 x 10组\n• 高抬腿: 30米 x 5组\n• 后蹬跑: 30米 x 5组\n• 腿部力量: 深蹲、跳跃训练",
            "sit_reach": "训练计划:\n• 坐位体前屈静态拉伸: 3组 x 30秒\n• 站立体前屈: 3组 x 15次\n• 腿部后侧拉伸: 每腿3组 x 20秒\n• 腰部拉伸: 瑜伽猫式等动作\n• 每天拉伸,循序渐进增加幅度",
            "standing_jump": "训练计划:\n• 深蹲跳: 4组 x 15次\n• 蛙跳: 20米 x 4组\n• 单腿跳: 每腿3组 x 10次\n• 台阶跳: 4组 x 20次\n• 摆臂练习配合腿部发力",
            "pull_ups": "训练计划:\n• 辅助引体(弹力带): 3组 x 8次\n• 反向划船: 4组 x 12次\n• 悬吊静止: 3组 x 最大时间\n• 背阔肌下拉: 4组 x 10次\n• 逐步减少辅助,增加次数",
            "sit_ups": "训练计划:\n• 标准仰卧起坐: 4组 x 80%最大次数\n• 卷腹: 4组 x 20次\n• 平板支撑: 3组 x 60秒\n• 俄罗斯转体: 4组 x 30次\n• 每周增加5-10次目标",
            "basketball": "训练计划:\n• 原地运球: 左右手各5分钟\n• 行进间运球: 往返10次\n• 变向运球: Z字形 x 10次\n• 双球运球: 5分钟提高协调\n• 障碍物运球: 提高控球能力",
            "football": "训练计划:\n• 脚内侧运球: 往返10次\n• 脚外侧运球: 往返10次\n• 变向运球: 8字形 x 10次\n• 障碍物绕桩: 连续练习\n• 提高触球频率和灵活性",
            "volleyball": "训练计划:\n• 对墙垫球: 连续100次 x 3组\n• 自垫球: 连续50次 x 3组\n• 移动垫球: 前后左右各方向\n• 双人对垫: 提高稳定性\n• 注意手型和击球部位"
        }
        
        # 如果是类别项,返回通用建议
        if project_key in ["required", "category1", "category2"]:
            return "请参考各单项的详细训练计划。"
        
        return plans.get(project_key, "请咨询专业教练制定个性化训练计划。")
    
    def display_training_plan(self, scores: Dict[str, float]):
        """显示分项训练计划"""
        # 清空现有内容
        for widget in self.training_frame.winfo_children():
            widget.destroy()
        
        # 按得分排序，优先显示得分低的项目
        items = [(k, v) for k, v in scores.items() if k != "total"]
        items.sort(key=lambda x: x[1])
        
        for item_key, score in items:
            item_name = self.get_item_display_name(item_key)
            
            # 确定优先级
            if score < 5:
                priority = "🔴 高优先级"
                bg_color = "#fadbd8"
            elif score < 7:
                priority = "🟡 中优先级"
                bg_color = "#fff3cd"
            else:
                priority = "🟢 低优先级"
                bg_color = "#d5f4e6"
            
            # 项目框架
            project_frame = tk.Frame(self.training_frame, bg=bg_color, 
                                    padx=12, pady=10, relief=tk.FLAT, bd=1)
            project_frame.pack(fill=tk.X, pady=5)
            
            # 标题行
            header_frame = tk.Frame(project_frame, bg=bg_color)
            header_frame.pack(fill=tk.X)
            
            tk.Label(header_frame, text=f"{item_name} - {score:.1f}分", 
                    font=("Microsoft YaHei", 11, "bold"),
                    bg=bg_color, fg=self.THEME_TEXT_DARK).pack(side=tk.LEFT)
            
            tk.Label(header_frame, text=priority, font=("Microsoft YaHei", 9),
                    bg=bg_color, fg=self.THEME_TEXT_DARK).pack(side=tk.RIGHT)
            
            # 训练建议
            if item_key not in ["required", "category1", "category2"]:
                plan = self.get_detailed_training_plan(item_key)
                tk.Label(project_frame, text=plan, font=("Microsoft YaHei", 9),
                        bg=bg_color, fg=self.THEME_TEXT_DARK, 
                        justify=tk.LEFT, anchor="w").pack(anchor="w", pady=(5, 0))
    
    def get_life_suggestions(self, total_score: float) -> str:
        """获取生活建议"""
        suggestions = """💪 训练建议:
• 制定合理的训练计划,循序渐进,避免过度训练
• 训练前充分热身(10-15分钟),激活肌肉,预防损伤
• 训练后做好拉伸放松(10-15分钟),促进恢复
• 记录训练日志,跟踪进步情况,及时调整方案
• 每周至少休息1-2天,让身体充分恢复

🍎 饮食建议:
• 保证充足的蛋白质摄入(鸡蛋、牛奶、瘦肉、豆类)
• 多吃新鲜蔬菜水果,补充维生素和矿物质
• 训练前1-2小时进食,避免空腹或过饱运动
• 训练后及时补充水分和能量(香蕉、运动饮料)
• 减少油炸食品和高糖食物,控制体重

😴 作息建议:
• 保证每天7-9小时的充足睡眠
• 尽量在晚上11点前入睡,确保深度睡眠
• 午休20-30分钟可以提高下午训练效果
• 避免熬夜和长时间使用电子设备
• 规律作息有助于提高运动表现

🎯 心理建议:
• 设定合理的短期和长期目标,保持动力
• 不要和别人比较,专注于自己的进步
• 遇到困难时保持积极心态,寻求帮助
• 庆祝每一个小进步,建立自信心
• 把运动当作生活习惯而非任务

⚠️ 安全提示:
• 身体不适时及时停止训练,不要勉强
• 使用正确的动作技术,避免受伤
• 注意训练场地安全,穿着合适的运动装备
• 如有慢性疾病,训练前咨询医生
• 运动损伤后要充分休息和治疗"""
        
        return suggestions
    
    def get_item_display_name(self, item_key: str) -> str:
        """获取项目显示名称"""
        if item_key == "required":
            return "必选项"
        elif item_key == "category1":
            return "第一类选考"
        elif item_key == "category2":
            return "第二类选考"
        else:
            return PROJECT_NAMES.get(item_key, item_key)
    
    def render_chart_in_window(self):
        """在窗口中渲染趋势图"""
        records = self.user.get_all_records()
        
        # 清空chart_frame
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        if len(records) < 2:
            # 显示提示信息
            label = tk.Label(
                self.chart_frame,
                text="📊 需要至少2条记录才能生成趋势图\n\n请先录入更多成绩数据",
                font=("Microsoft YaHei", 12),
                bg=self.THEME_CARD,
                fg=self.THEME_TEXT_LIGHT
            )
            label.place(relx=0.5, rely=0.5, anchor="center")
            return
        
        try:
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'Microsoft YaHei']
            plt.rcParams['axes.unicode_minus'] = False
            
            # 创建图表
            fig = Figure(figsize=(9, 4), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            # 准备数据
            dates = [r['date'] for r in records]
            total_scores = [r['scores']['total'] for r in records]
            required_scores = [r['scores']['required'] for r in records]
            category1_scores = [r['scores']['category1'] for r in records]
            category2_scores = [r['scores']['category2'] for r in records]
            
            # 绘制折线图
            ax.plot(range(len(dates)), total_scores, marker='o', linewidth=2.5, 
                   markersize=8, label='总分', color='#16a085', zorder=3)
            ax.plot(range(len(dates)), required_scores, marker='s', linewidth=1.5, 
                   markersize=6, label='必选项', color='#3498db', alpha=0.7)
            ax.plot(range(len(dates)), category1_scores, marker='^', linewidth=1.5, 
                   markersize=6, label='第一类选考', color='#2ecc71', alpha=0.7)
            ax.plot(range(len(dates)), category2_scores, marker='d', linewidth=1.5, 
                   markersize=6, label='第二类选考', color='#f39c12', alpha=0.7)
            
            # 设置标题和标签
            ax.set_title(f'{self.user.name} - 成绩趋势分析', 
                        fontsize=14, fontweight='bold', pad=15)
            ax.set_xlabel('测试日期', fontsize=11)
            ax.set_ylabel('得分', fontsize=11)
            
            # 设置x轴刻度
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(dates, rotation=30, ha='right', fontsize=9)
            
            # 设置y轴范围
            ax.set_ylim(0, 10.5)
            ax.set_yticks(range(0, 11, 2))
            
            # 添加网格
            ax.grid(True, linestyle='--', alpha=0.3, zorder=0)
            
            # 添加图例
            ax.legend(loc='best', fontsize=10, framealpha=0.9)
            
            # 调整布局
            fig.tight_layout()
            
            # 嵌入到tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            print(f"渲染图表错误: {e}")
            import traceback
            traceback.print_exc()
            
            label = tk.Label(
                self.chart_frame,
                text=f"❌ 图表渲染失败\n\n{str(e)}",
                font=("Microsoft YaHei", 11),
                bg=self.THEME_CARD,
                fg=self.THEME_DANGER
            )
            label.place(relx=0.5, rely=0.5, anchor="center")
    
    def refresh_chart(self):
        """刷新图表"""
        self.render_chart_in_window()
    
    def generate_trend_chart(self):
        """生成趋势图（已废弃，保留兼容性）"""
        # 图表现在直接在窗口中显示，无需单独生成
        messagebox.showinfo("提示", "图表已在上方显示\n\n如需导出，请点击\"导出图表\"按钮")
    
    def export_chart(self):
        """导出图表"""
        records = self.user.get_all_records()
        
        if len(records) < 2:
            messagebox.showwarning("数据不足", "需要至少2条记录才能导出图表")
            return
        
        # 选择保存路径
        file_path = filedialog.asksaveasfilename(
            title="保存图表",
            defaultextension=".png",
            filetypes=[("PNG图片", "*.png"), ("JPEG图片", "*.jpg"), ("所有文件", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # 使用matplotlib直接生成并保存
            plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'Microsoft YaHei']
            plt.rcParams['axes.unicode_minus'] = False
            
            fig, ax = plt.subplots(figsize=(12, 6), dpi=150)
            
            # 准备数据
            dates = [r['date'] for r in records]
            total_scores = [r['scores']['total'] for r in records]
            required_scores = [r['scores']['required'] for r in records]
            category1_scores = [r['scores']['category1'] for r in records]
            category2_scores = [r['scores']['category2'] for r in records]
            
            # 绘制折线图
            ax.plot(range(len(dates)), total_scores, marker='o', linewidth=3, 
                   markersize=10, label='总分', color='#16a085', zorder=3)
            ax.plot(range(len(dates)), required_scores, marker='s', linewidth=2, 
                   markersize=8, label='必选项', color='#3498db', alpha=0.7)
            ax.plot(range(len(dates)), category1_scores, marker='^', linewidth=2, 
                   markersize=8, label='第一类选考', color='#2ecc71', alpha=0.7)
            ax.plot(range(len(dates)), category2_scores, marker='d', linewidth=2, 
                   markersize=8, label='第二类选考', color='#f39c12', alpha=0.7)
            
            # 设置标题和标签
            ax.set_title(f'{self.user.name} - 成绩趋势分析', 
                        fontsize=18, fontweight='bold', pad=20)
            ax.set_xlabel('测试日期', fontsize=14)
            ax.set_ylabel('得分', fontsize=14)
            
            # 设置x轴刻度
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(dates, rotation=30, ha='right', fontsize=12)
            
            # 设置y轴范围
            ax.set_ylim(0, 10.5)
            ax.set_yticks(range(0, 11, 2))
            
            # 添加网格
            ax.grid(True, linestyle='--', alpha=0.3, zorder=0)
            
            # 添加图例
            ax.legend(loc='best', fontsize=12, framealpha=0.9)
            
            # 调整布局
            fig.tight_layout()
            
            # 保存
            fig.savefig(file_path, dpi=150, bbox_inches='tight')
            plt.close(fig)
            
            messagebox.showinfo("导出成功", f"图表已导出到:\n{file_path}")
        except Exception as e:
            messagebox.showerror("导出失败", f"导出图表时发生错误:\n{str(e)}")
    
    def show(self):
        """显示窗口"""
        self.window.mainloop()
    
    def destroy(self):
        """销毁窗口"""
        if self.window:
            self.window.destroy()

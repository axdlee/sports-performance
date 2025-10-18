# -*- coding: utf-8 -*-
"""
当前成绩标签页
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Optional
from config.constants import (
    PROJECT_NAMES, THEME_COLORS, FONTS
)


class CurrentScoreTab:
    """当前成绩标签页"""
    
    # 颜色主题
    THEME_PRIMARY = THEME_COLORS["primary"]
    THEME_BG = THEME_COLORS["bg"]
    THEME_CARD = THEME_COLORS["card"]
    THEME_SUCCESS = THEME_COLORS["success"]
    THEME_WARNING = THEME_COLORS["warning"]
    THEME_DANGER = THEME_COLORS["danger"]
    THEME_INFO = THEME_COLORS["info"]
    THEME_TEXT_DARK = THEME_COLORS["text_dark"]
    THEME_TEXT_LIGHT = THEME_COLORS["text_light"]
    
    def __init__(self, parent, user, score_calculator):
        self.parent = parent
        self.user = user
        self.score_calculator = score_calculator
        self.setup_ui()
    
    def create_card_frame(self, parent, title, title_color=None):
        """创建卡片框架"""
        card = tk.Frame(parent, bg=self.THEME_CARD, relief=tk.FLAT, bd=0)
        
        if title_color is None:
            title_color = self.THEME_PRIMARY
        
        title_frame = tk.Frame(card, bg=title_color, height=40)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text=title, 
                              font=FONTS["card_title"],
                              bg=title_color, fg="white", anchor="w", padx=15)
        title_label.pack(fill=tk.BOTH, expand=True)
        
        content = tk.Frame(card, bg=self.THEME_CARD, padx=15, pady=15)
        content.pack(fill=tk.BOTH, expand=True)
        
        return card, content
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建滚动框架
        current_frame = tk.Frame(self.parent, bg=self.THEME_BG)
        
        # 创建Canvas和Scrollbar
        canvas = tk.Canvas(current_frame, bg=self.THEME_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(current_frame, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg=self.THEME_BG, pady=15)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        def center_window(event=None):
            canvas.update_idletasks()
            canvas_width = canvas.winfo_width()
            scrollable_width = scrollable_frame.winfo_reqwidth()
            x = (canvas_width - scrollable_width) // 2
            canvas.coords(canvas_window, x, 0)
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.bind('<Configure>', center_window)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 成绩概览卡片
        overview_card, overview_content = self.create_card_frame(scrollable_frame, "🎯 成绩概览")
        overview_card.pack(fill=tk.X, pady=(0, 15))
        
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
        date_frame = tk.Frame(overview_content, bg=self.THEME_CARD)
        date_frame.pack(fill=tk.X, pady=(10, 0))
        self.test_date_var = tk.StringVar(value="测试日期: --")
        tk.Label(date_frame, textvariable=self.test_date_var, 
                font=("Microsoft YaHei", 10), bg=self.THEME_CARD, 
                fg=self.THEME_TEXT_LIGHT).pack(anchor="w")
        
        # 详细成绩卡片
        details_card, details_content = self.create_card_frame(scrollable_frame, "📋 详细成绩")
        details_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.score_items_frame = tk.Frame(details_content, bg=self.THEME_CARD)
        self.score_items_frame.pack(fill=tk.BOTH, expand=True)
        
        # 快速分析卡片
        quick_analysis_card, quick_analysis_content = self.create_card_frame(
            scrollable_frame, "⚡ 快速分析", self.THEME_WARNING)
        quick_analysis_card.pack(fill=tk.X, pady=(0, 15))
        
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
        
        self.frame = current_frame
    
    def display_current_score(self, record: Dict):
        """显示当前成绩"""
        scores = record["scores"]
        total_score = scores["total"]
        
        self.total_score_var.set(f"{total_score:.1f}")
        grade = self.score_calculator.get_grade_level(total_score)
        self.grade_var.set(grade)
        
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
        
        formatted_value = self.format_performance(project_key, performance_value)
        
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
        
        item_frame = tk.Frame(self.score_items_frame, bg=self.THEME_CARD, pady=5)
        item_frame.pack(fill=tk.X, pady=3)
        
        left_frame = tk.Frame(item_frame, bg=self.THEME_CARD)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left_frame, text=f"{category} - {project_name}", 
                font=("Microsoft YaHei", 11, "bold"), 
                bg=self.THEME_CARD, fg=self.THEME_TEXT_DARK, anchor="w").pack(anchor="w")
        
        tk.Label(left_frame, text=f"成绩: {formatted_value}", 
                font=("Microsoft YaHei", 9), 
                bg=self.THEME_CARD, fg=self.THEME_TEXT_LIGHT, anchor="w").pack(anchor="w")
        
        right_frame = tk.Frame(item_frame, bg=color, padx=15, pady=5)
        right_frame.pack(side=tk.RIGHT)
        
        tk.Label(right_frame, text=f"{score:.1f}分", 
                font=("Microsoft YaHei", 14, "bold"), 
                bg=color, fg="white").pack()
        
        tk.Label(right_frame, text=status, 
                font=("Microsoft YaHei", 9), 
                bg=color, fg="white").pack()
        
        tk.Frame(self.score_items_frame, bg=self.THEME_BG, height=1).pack(fill=tk.X, pady=2)
    
    def format_performance(self, project_key: str, performance_value: float) -> str:
        """格式化成绩显示"""
        if project_key in ["1000m", "800m", "50m", "basketball", "football"]:
            if project_key in ["1000m", "800m"]:
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
    
    def show_no_data(self):
        """显示无数据消息"""
        self.total_score_var.set("--")
        self.grade_var.set("暂无数据")
        self.test_date_var.set("测试日期: --")
        self.strongest_var.set("暂无数据")
        self.weakest_var.set("暂无数据")

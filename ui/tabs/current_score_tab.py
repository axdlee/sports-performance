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
    THEME_PRIMARY_DARK = THEME_COLORS["primary_dark"]
    THEME_PRIMARY_LIGHT = THEME_COLORS["primary_light"]
    THEME_BG = THEME_COLORS["bg"]
    THEME_CARD = THEME_COLORS["card"]
    THEME_TEXT_DARK = THEME_COLORS["text_dark"]
    THEME_TEXT_LIGHT = THEME_COLORS["text_light"]
    THEME_SUCCESS = THEME_COLORS["success"]
    THEME_WARNING = THEME_COLORS["warning"]
    THEME_DANGER = THEME_COLORS["danger"]
    THEME_INFO = THEME_COLORS["info"]
    
    def __init__(self, parent, user, score_calculator):
        self.parent = parent
        self.user = user
        self.score_calculator = score_calculator
        self.setup_ui()
    
    def create_card_frame(self, parent, title, title_color=None):
        """创建卡片框架"""
        # 外层容器，用于模拟阴影或边距
        container = tk.Frame(parent, bg=self.THEME_BG, padx=2, pady=2)
        
        # 卡片主体
        card = tk.Frame(container, bg=self.THEME_CARD, relief=tk.FLAT, bd=0)
        card.pack(fill=tk.BOTH, expand=True)
        
        # 标题栏（可选）
        if title:
            if title_color is None:
                title_color = self.THEME_PRIMARY
            
            # 标题容器
            header = tk.Frame(card, bg="white", height=45)
            header.pack(fill=tk.X)
            header.pack_propagate(False)
            
            # 左侧装饰条
            tk.Frame(header, bg=title_color, width=4).pack(side=tk.LEFT, fill=tk.Y)
            
            # 标题文本
            tk.Label(header, text=title, 
                    font=FONTS["card_title"],
                    bg="white", fg=self.THEME_TEXT_DARK, 
                    anchor="w", padx=10).pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # 分割线
            tk.Frame(card, bg=THEME_COLORS["border"], height=1).pack(fill=tk.X)
        
        content = tk.Frame(card, bg=self.THEME_CARD, padx=20, pady=20)
        content.pack(fill=tk.BOTH, expand=True)
        
        return container, content
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建滚动框架
        current_frame = tk.Frame(self.parent, bg=self.THEME_BG)
        
        # 创建Canvas和Scrollbar
        canvas = tk.Canvas(current_frame, bg=self.THEME_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(current_frame, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg=self.THEME_BG, pady=10, padx=10)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        def center_window(event=None):
            canvas.update_idletasks()
            canvas_width = canvas.winfo_width()
            scrollable_width = scrollable_frame.winfo_reqwidth()
            if canvas_width > scrollable_width:
                x = (canvas_width - scrollable_width) // 2
                canvas.coords(canvas_window, x, 0)
            else:
                canvas.coords(canvas_window, 0, 0)
        
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
        
        # 总分展示区
        total_container = tk.Frame(scores_frame, bg=self.THEME_PRIMARY_LIGHT, padx=1) # 边框色
        total_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        total_frame = tk.Frame(total_container, bg="white", padx=25, pady=20)
        total_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(total_frame, text="总分 Total Score", 
                font=FONTS["text_small"], bg="white", fg=self.THEME_TEXT_LIGHT).pack(anchor="w")
        
        score_row = tk.Frame(total_frame, bg="white")
        score_row.pack(fill=tk.X, pady=(5, 0))
        
        self.total_score_var = tk.StringVar(value="--")
        tk.Label(score_row, textvariable=self.total_score_var, 
                font=FONTS["score_large"], bg="white", fg=self.THEME_PRIMARY).pack(side=tk.LEFT)
        
        tk.Label(score_row, text="/ 120", 
                font=FONTS["text_normal"], bg="white", fg=self.THEME_TEXT_LIGHT).pack(side=tk.LEFT, padx=(5, 0), pady=(15, 0))

        # 等级展示区
        grade_container = tk.Frame(scores_frame, bg=THEME_COLORS["info"], padx=1)
        grade_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        grade_frame = tk.Frame(grade_container, bg="white", padx=25, pady=20)
        grade_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(grade_frame, text="等级 Grade", 
                font=FONTS["text_small"], bg="white", fg=self.THEME_TEXT_LIGHT).pack(anchor="w")
        
        self.grade_var = tk.StringVar(value="--")
        tk.Label(grade_frame, textvariable=self.grade_var, 
                font=FONTS["score_medium"], bg="white", fg=THEME_COLORS["info"]).pack(anchor="w", pady=(5, 0))
        
        # 测试日期
        date_frame = tk.Frame(overview_content, bg=self.THEME_CARD)
        date_frame.pack(fill=tk.X, pady=(15, 0))
        self.test_date_var = tk.StringVar(value="测试日期: --")
        tk.Label(date_frame, textvariable=self.test_date_var, 
                font=FONTS["text_small"], bg=self.THEME_CARD, 
                fg=self.THEME_TEXT_LIGHT).pack(anchor="w")
        
        # 详细成绩卡片
        details_card, details_content = self.create_card_frame(scrollable_frame, "📋 详细成绩")
        details_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 表头
        header_frame = tk.Frame(details_content, bg=self.THEME_CARD)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(header_frame, text="项目", font=FONTS["text_small"], 
                bg=self.THEME_CARD, fg=self.THEME_TEXT_LIGHT, width=20, anchor="w").pack(side=tk.LEFT)
        tk.Label(header_frame, text="得分", font=FONTS["text_small"], 
                bg=self.THEME_CARD, fg=self.THEME_TEXT_LIGHT, width=10, anchor="e").pack(side=tk.RIGHT, padx=20)
        tk.Label(header_frame, text="成绩", font=FONTS["text_small"], 
                bg=self.THEME_CARD, fg=self.THEME_TEXT_LIGHT, width=15, anchor="e").pack(side=tk.RIGHT)
        
        tk.Frame(details_content, bg=THEME_COLORS["border"], height=1).pack(fill=tk.X, pady=(0, 10))
        
        self.score_items_frame = tk.Frame(details_content, bg=self.THEME_CARD)
        self.score_items_frame.pack(fill=tk.BOTH, expand=True)
        
        # 快速分析卡片
        quick_analysis_card, quick_analysis_content = self.create_card_frame(
            scrollable_frame, "⚡ 快速分析", self.THEME_WARNING)
        quick_analysis_card.pack(fill=tk.X, pady=(0, 15))
        
        analysis_frame = tk.Frame(quick_analysis_content, bg=self.THEME_CARD)
        analysis_frame.pack(fill=tk.X)
        
        # 最强项
        strong_frame = tk.Frame(analysis_frame, bg=THEME_COLORS["strong_bg"], padx=20, pady=15, relief=tk.FLAT)
        strong_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        tk.Label(strong_frame, text="💪 最强项", font=FONTS["label_font_bold"],
                bg=THEME_COLORS["strong_bg"], fg=self.THEME_SUCCESS).pack(anchor="w")
        self.strongest_var = tk.StringVar(value="--")
        tk.Label(strong_frame, textvariable=self.strongest_var, 
                font=FONTS["text_normal"], bg=THEME_COLORS["strong_bg"], 
                fg=self.THEME_TEXT_DARK).pack(anchor="w", pady=(5, 0))
        
        # 最弱项
        weak_frame = tk.Frame(analysis_frame, bg=THEME_COLORS["weak_bg"], padx=20, pady=15, relief=tk.FLAT)
        weak_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(weak_frame, text="⚠️ 最弱项", font=FONTS["label_font_bold"],
                bg=THEME_COLORS["weak_bg"], fg=self.THEME_DANGER).pack(anchor="w")
        self.weakest_var = tk.StringVar(value="--")
        tk.Label(weak_frame, textvariable=self.weakest_var, 
                font=FONTS["text_normal"], bg=THEME_COLORS["weak_bg"], 
                fg=self.THEME_TEXT_DARK).pack(anchor="w", pady=(5, 0))
        
        self.frame = current_frame

    # ... (display_current_score 方法保持不变，或者根据需要微调) ...

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
        
        item_frame = tk.Frame(self.score_items_frame, bg=self.THEME_CARD, pady=8)
        item_frame.pack(fill=tk.X)
        
        # 左侧：类别和项目名
        left_frame = tk.Frame(item_frame, bg=self.THEME_CARD)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left_frame, text=project_name, 
                font=FONTS["text_normal"], 
                bg=self.THEME_CARD, fg=self.THEME_TEXT_DARK, anchor="w").pack(anchor="w")
        
        tk.Label(left_frame, text=category, 
                font=FONTS["text_tiny"], 
                bg=self.THEME_CARD, fg=self.THEME_TEXT_LIGHT, anchor="w").pack(anchor="w")
        
        # 右侧：得分和状态
        right_frame = tk.Frame(item_frame, bg=self.THEME_CARD)
        right_frame.pack(side=tk.RIGHT)
        
        # 成绩值
        tk.Label(right_frame, text=formatted_value, 
                font=FONTS["text_normal"], 
                bg=self.THEME_CARD, fg=self.THEME_TEXT_DARK, width=15, anchor="e").pack(side=tk.LEFT)
        
        # 得分
        score_frame = tk.Frame(right_frame, bg=self.THEME_CARD, width=80)
        score_frame.pack(side=tk.LEFT, padx=(10, 0))
        
        tk.Label(score_frame, text=f"{score:.1f}", 
                font=FONTS["score_detail"], 
                bg=self.THEME_CARD, fg=color, width=5, anchor="e").pack(side=tk.RIGHT)
        
        # 底部增加分割线（除了最后一个）
        tk.Frame(self.score_items_frame, bg=THEME_COLORS["bg"], height=1).pack(fill=tk.X, pady=(5, 5))
    
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
        
        # 清空之前的成绩项
        for widget in self.score_items_frame.winfo_children():
            widget.destroy()
        
        # 显示各项成绩
        self.create_score_item("required", record["required"], scores["required"])
        self.create_score_item("category1", record["category1"], scores["category1"])
        self.create_score_item("category2", record["category2"], scores["category2"])
        
        # 更新最强项和最弱项
        strongest = self.score_calculator.get_strongest_item(scores)
        weakest = self.score_calculator.get_weakest_item(scores)
        
        if strongest:
            # 获取实际项目名称
            if strongest in ["required", "category1", "category2"]:
                actual_project = list(record[strongest].keys())[0]
                strongest_name = PROJECT_NAMES.get(actual_project, actual_project)
            else:
                strongest_name = PROJECT_NAMES.get(strongest, strongest)
                
            self.strongest_var.set(f"{strongest_name} ({scores[strongest]:.1f}分)")
        else:
            self.strongest_var.set("--")
        
        if weakest:
            # 获取实际项目名称
            if weakest in ["required", "category1", "category2"]:
                actual_project = list(record[weakest].keys())[0]
                weakest_name = PROJECT_NAMES.get(actual_project, actual_project)
            else:
                weakest_name = PROJECT_NAMES.get(weakest, weakest)
                
            self.weakest_var.set(f"{weakest_name} ({scores[weakest]:.1f}分)")
        else:
            self.weakest_var.set("--")
    
    def show_no_data(self):
        """显示无数据消息"""
        self.total_score_var.set("--")
        self.grade_var.set("暂无数据")
        self.test_date_var.set("测试日期: --")
        self.strongest_var.set("暂无数据")
        self.weakest_var.set("暂无数据")

# -*- coding: utf-8 -*-
"""
数据分析标签页
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Optional
import statistics
from config.constants import PROJECT_NAMES, THEME_COLORS, FONTS


class AnalysisTab:
    """数据分析标签页"""
    
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
        self.analysis_data = None
        self.setup_ui()
    
    def create_card_frame(self, parent, title, title_color=None):
        """创建卡片框架"""
        # 外层容器
        container = tk.Frame(parent, bg=self.THEME_BG, padx=2, pady=2)
        
        # 卡片主体
        card = tk.Frame(container, bg=self.THEME_CARD, relief=tk.FLAT, bd=0)
        card.pack(fill=tk.BOTH, expand=True)
        
        # 标题栏
        if title:
            if title_color is None:
                title_color = self.THEME_PRIMARY
            
            header = tk.Frame(card, bg="white", height=45)
            header.pack(fill=tk.X)
            header.pack_propagate(False)
            
            tk.Frame(header, bg=title_color, width=4).pack(side=tk.LEFT, fill=tk.Y)
            
            tk.Label(header, text=title, 
                    font=FONTS["card_title"],
                    bg="white", fg=self.THEME_TEXT_DARK, 
                    anchor="w", padx=10).pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            tk.Frame(card, bg=THEME_COLORS["border"], height=1).pack(fill=tk.X)
        
        content = tk.Frame(card, bg=self.THEME_CARD, padx=20, pady=20)
        content.pack(fill=tk.BOTH, expand=True)
        
        return container, content
    
    def setup_ui(self):
        """设置用户界面"""
        analysis_frame = tk.Frame(self.parent, bg=self.THEME_BG)
        
        canvas = tk.Canvas(analysis_frame, bg=self.THEME_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(analysis_frame, orient="vertical", command=canvas.yview)
        
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
        
        # 统计概览卡片
        stats_card, stats_content = self.create_card_frame(scrollable_frame, "📈 统计概览")
        stats_card.pack(fill=tk.X, pady=(0, 15))
        
        stats_grid = tk.Frame(stats_content, bg=self.THEME_CARD)
        stats_grid.pack(fill=tk.X)
        
        self.stats_vars = {}
        stats_items = [
            ("total_records", "测试次数", self.THEME_INFO, "📝"),
            ("avg_score", "平均分", self.THEME_PRIMARY, "📊"),
            ("highest_score", "最高分", self.THEME_SUCCESS, "🏆"),
            ("lowest_score", "最低分", self.THEME_DANGER, "📉")
        ]
        
        for i, (key, label, color, icon) in enumerate(stats_items):
            row = i // 2
            col = i % 2
            
            # 统计项容器
            item_container = tk.Frame(stats_grid, bg=THEME_COLORS["stats_bg"], padx=1, pady=1)
            item_container.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            stat_frame = tk.Frame(item_container, bg="white", padx=15, pady=15)
            stat_frame.pack(fill=tk.BOTH, expand=True)
            
            # 顶部：图标和标签
            top_frame = tk.Frame(stat_frame, bg="white")
            top_frame.pack(fill=tk.X)
            
            tk.Label(top_frame, text=icon, font=("Segoe UI Emoji", 12), 
                    bg="white", fg=color).pack(side=tk.LEFT, padx=(0, 5))
            
            tk.Label(top_frame, text=label, font=FONTS["text_small"],
                    bg="white", fg=self.THEME_TEXT_LIGHT).pack(side=tk.LEFT)
            
            # 底部：数值
            var = tk.StringVar(value="--")
            self.stats_vars[key] = var
            tk.Label(stat_frame, textvariable=var, font=FONTS["score_medium"],
                    bg="white", fg=self.THEME_TEXT_DARK).pack(pady=(10, 0), anchor="w")
        
        for i in range(2):
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
        
        self.frame = analysis_frame

    # ... (analyze_all_data, analyze_projects, display_analysis 方法保持不变) ...

    def display_record_comparison(self):
        """显示最佳与最差记录对比"""
        if not self.analysis_data:
            return
        
        for widget in self.compare_frame.winfo_children():
            widget.destroy()
        
        best = self.analysis_data["best_record"]
        worst = self.analysis_data["worst_record"]
        
        # 最佳记录
        best_frame = tk.Frame(self.compare_frame, bg=THEME_COLORS["strong_bg"], padx=20, pady=15, relief=tk.FLAT)
        best_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        tk.Label(best_frame, text="🏆 最佳记录", font=FONTS["label_font_bold"],
                bg=THEME_COLORS["strong_bg"], fg=self.THEME_SUCCESS).pack(anchor="w")
        
        tk.Label(best_frame, text=f"日期: {best['date']}", font=FONTS["text_small"],
                bg=THEME_COLORS["strong_bg"], fg=self.THEME_TEXT_DARK).pack(anchor="w", pady=(5, 0))
        
        tk.Label(best_frame, text=f"总分: {best['scores']['total']:.1f}", 
                font=FONTS["score_medium"],
                bg=THEME_COLORS["strong_bg"], fg=self.THEME_SUCCESS).pack(anchor="w", pady=(5, 0))
        
        # 最差记录
        worst_frame = tk.Frame(self.compare_frame, bg=THEME_COLORS["weak_bg"], padx=20, pady=15, relief=tk.FLAT)
        worst_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(worst_frame, text="📉 最低记录", font=FONTS["label_font_bold"],
                bg=THEME_COLORS["weak_bg"], fg=self.THEME_DANGER).pack(anchor="w")
        
        tk.Label(worst_frame, text=f"日期: {worst['date']}", font=FONTS["text_small"],
                bg=THEME_COLORS["weak_bg"], fg=self.THEME_TEXT_DARK).pack(anchor="w", pady=(5, 0))
        
        tk.Label(worst_frame, text=f"总分: {worst['scores']['total']:.1f}", 
                font=FONTS["score_medium"],
                bg=THEME_COLORS["weak_bg"], fg=self.THEME_DANGER).pack(anchor="w", pady=(5, 0))
    
    def display_projects_analysis(self):
        """显示各项目分析"""
        if not self.analysis_data or "projects" not in self.analysis_data:
            return
        
        for widget in self.projects_analysis_frame.winfo_children():
            widget.destroy()
        
        projects = self.analysis_data["projects"]
        
        # 表头
        header_frame = tk.Frame(self.projects_analysis_frame, bg=self.THEME_CARD)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(header_frame, text="项目", font=FONTS["text_small"], 
                bg=self.THEME_CARD, fg=self.THEME_TEXT_LIGHT, width=15, anchor="w").pack(side=tk.LEFT)
        tk.Label(header_frame, text="趋势", font=FONTS["text_small"], 
                bg=self.THEME_CARD, fg=self.THEME_TEXT_LIGHT, width=10, anchor="e").pack(side=tk.RIGHT)
        tk.Label(header_frame, text="最佳", font=FONTS["text_small"], 
                bg=self.THEME_CARD, fg=self.THEME_TEXT_LIGHT, width=15, anchor="e").pack(side=tk.RIGHT)
        tk.Label(header_frame, text="平均分", font=FONTS["text_small"], 
                bg=self.THEME_CARD, fg=self.THEME_TEXT_LIGHT, width=10, anchor="e").pack(side=tk.RIGHT)
        
        tk.Frame(self.projects_analysis_frame, bg=THEME_COLORS["border"], height=1).pack(fill=tk.X, pady=(0, 5))
        
        for i, (project_key, data) in enumerate(projects.items()):
            project_name = PROJECT_NAMES.get(project_key, project_key)
            
            # 斑马纹背景
            bg_color = self.THEME_CARD if i % 2 == 0 else THEME_COLORS["bg"]
            
            project_frame = tk.Frame(self.projects_analysis_frame, bg=bg_color, padx=10, pady=8)
            project_frame.pack(fill=tk.X)
            
            # 项目名
            tk.Label(project_frame, text=project_name, font=FONTS["text_normal"],
                    bg=bg_color, fg=self.THEME_TEXT_DARK, width=15, anchor="w").pack(side=tk.LEFT)
            
            # 趋势
            if data['trend'] == 'improving':
                improvement_text = "📈 上升"
                color = self.THEME_SUCCESS
            elif data['trend'] == 'declining':
                improvement_text = "📉 下降"
                color = self.THEME_DANGER
            else:
                improvement_text = "➡️ 稳定"
                color = self.THEME_INFO
            
            tk.Label(project_frame, text=improvement_text, font=FONTS["text_small"],
                    bg=bg_color, fg=color, width=10, anchor="e").pack(side=tk.RIGHT)
            
            # 最佳成绩
            best_perf = self.format_performance(project_key, data['best_performance'])
            tk.Label(project_frame, text=f"{best_perf}", 
                    font=FONTS["text_small"],
                    bg=bg_color, fg=self.THEME_TEXT_LIGHT, width=15, anchor="e").pack(side=tk.RIGHT)
            
            # 平均分
            tk.Label(project_frame, text=f"{data['avg_score']:.1f}", 
                    font=FONTS["score_detail"],
                    bg=bg_color, fg=self.THEME_PRIMARY, width=10, anchor="e").pack(side=tk.RIGHT)
    
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
    
    
    def analyze_all_data(self, records):
        """分析所有数据"""
        if not records:
            self.analysis_data = None
            return
        
        # 找出最佳和最差记录
        best_record = max(records, key=lambda x: x["scores"]["total"])
        worst_record = min(records, key=lambda x: x["scores"]["total"])
        
        # 统计数据
        total_records = len(records)
        total_scores = [r["scores"]["total"] for r in records]
        avg_score = statistics.mean(total_scores)
        highest_score = max(total_scores)
        lowest_score = min(total_scores)
        
        # 分析各项目
        projects_data = {}
        all_projects = set()
        for record in records:
            for category in ["required", "category1", "category2"]:
                project_key = list(record[category].keys())[0]
                all_projects.add(project_key)
        
        for project_key in all_projects:
            project_scores = []
            project_performances = []
            
            for record in records:
                for category in ["required", "category1", "category2"]:
                    if project_key in record[category]:
                        project_scores.append(record["scores"][category])
                        project_performances.append(record[category][project_key])
            
            if project_scores:
                projects_data[project_key] = {
                    "avg_score": statistics.mean(project_scores),
                    "best_score": max(project_scores),
                    "worst_score": min(project_scores),
                    "best_performance": max(project_performances),
                    "worst_performance": min(project_performances),
                    "trend": "improving" if len(project_scores) >= 2 and project_scores[-1] > project_scores[0] else "declining" if len(project_scores) >= 2 and project_scores[-1] < project_scores[0] else "stable"
                }
        
        self.analysis_data = {
            "total_records": total_records,
            "avg_score": avg_score,
            "highest_score": highest_score,
            "lowest_score": lowest_score,
            "best_record": best_record,
            "worst_record": worst_record,
            "projects": projects_data
        }
    
    def display_analysis(self):
        """显示分析结果"""
        if not self.analysis_data:
            self.show_no_data()
            return
        
        # 更新统计概览
        self.stats_vars["total_records"].set(str(self.analysis_data["total_records"]))
        self.stats_vars["avg_score"].set(f"{self.analysis_data['avg_score']:.1f}")
        self.stats_vars["highest_score"].set(f"{self.analysis_data['highest_score']:.1f}")
        self.stats_vars["lowest_score"].set(f"{self.analysis_data['lowest_score']:.1f}")
        
        # 显示最佳与最差记录对比
        self.display_record_comparison()
        
        # 显示各项目分析
        self.display_projects_analysis()
    
    def show_no_data(self):
        """显示无数据消息"""
        for var in self.stats_vars.values():
            var.set("--")
    
    def refresh_data(self, updated_user):
        """刷新数据 - 使用最新的用户数据更新分析"""
        self.user = updated_user
        records = self.user.get_all_records()
        
        if not records:
            self.show_no_data()
            return
        
        # 重新分析数据
        self.analyze_all_data(records)
        
        # 更新显示
        self.display_analysis()
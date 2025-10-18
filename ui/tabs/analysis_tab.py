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
        self.analysis_data = None
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
        analysis_frame = tk.Frame(self.parent, bg=self.THEME_BG)
        
        canvas = tk.Canvas(analysis_frame, bg=self.THEME_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(analysis_frame, orient="vertical", command=canvas.yview)
        
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
        
        # 统计概览卡片
        stats_card, stats_content = self.create_card_frame(scrollable_frame, "📈 统计概览")
        stats_card.pack(fill=tk.X, pady=(0, 15))
        
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
        
        self.frame = analysis_frame
    
    def analyze_all_data(self, records):
        """分析所有历史数据"""
        if not records:
            self.analysis_data = None
            return
        
        analysis = {
            "record_count": len(records),
            "scores": [r["scores"]["total"] for r in records],
            "dates": [r["date"] for r in records]
        }
        
        analysis["avg_score"] = statistics.mean(analysis["scores"])
        analysis["best_score"] = max(analysis["scores"])
        analysis["worst_score"] = min(analysis["scores"])
        analysis["best_record"] = max(records, key=lambda r: r["scores"]["total"])
        analysis["worst_record"] = min(records, key=lambda r: r["scores"]["total"])
        
        if len(records) >= 2:
            first_score = records[0]["scores"]["total"]
            latest_score = records[-1]["scores"]["total"]
            analysis["improvement"] = latest_score - first_score
            analysis["improvement_percent"] = (analysis["improvement"] / first_score * 100) if first_score > 0 else 0
            
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
        
        analysis["projects"] = self.analyze_projects(records)
        
        self.analysis_data = analysis
    
    def analyze_projects(self, records):
        """分析各项目成绩"""
        projects = {}
        
        for record in records:
            req_key = list(record["required"].keys())[0]
            if req_key not in projects:
                projects[req_key] = {"scores": [], "performances": []}
            projects[req_key]["scores"].append(record["scores"]["required"])
            projects[req_key]["performances"].append(record["required"][req_key])
            
            cat1_key = list(record["category1"].keys())[0]
            if cat1_key not in projects:
                projects[cat1_key] = {"scores": [], "performances": []}
            projects[cat1_key]["scores"].append(record["scores"]["category1"])
            projects[cat1_key]["performances"].append(record["category1"][cat1_key])
            
            cat2_key = list(record["category2"].keys())[0]
            if cat2_key not in projects:
                projects[cat2_key] = {"scores": [], "performances": []}
            projects[cat2_key]["scores"].append(record["scores"]["category2"])
            projects[cat2_key]["performances"].append(record["category2"][cat2_key])
        
        for key, data in projects.items():
            data["avg_score"] = statistics.mean(data["scores"])
            data["best_score"] = max(data["scores"])
            data["best_performance"] = data["performances"][data["scores"].index(data["best_score"])]
            
            if len(data["scores"]) >= 2:
                data["improvement"] = data["scores"][-1] - data["scores"][0]
            else:
                data["improvement"] = 0
        
        return projects
    
    def display_analysis(self):
        """显示数据分析"""
        if not self.analysis_data:
            return
        
        data = self.analysis_data
        
        self.stats_vars["record_count"].set(f"{data['record_count']}次")
        self.stats_vars["avg_score"].set(f"{data['avg_score']:.1f}")
        self.stats_vars["best_score"].set(f"{data['best_score']:.1f}")
        self.stats_vars["worst_score"].set(f"{data['worst_score']:.1f}")
        
        if data["improvement"] >= 0:
            self.stats_vars["improvement"].set(f"+{data['improvement']:.1f}")
        else:
            self.stats_vars["improvement"].set(f"{data['improvement']:.1f}")
        
        self.stats_vars["trend"].set(f"{data['trend_emoji']} {data['trend']}")
        
        self.display_record_comparison()
        self.display_projects_analysis()
    
    def display_record_comparison(self):
        """显示最佳与最差记录对比"""
        if not self.analysis_data:
            return
        
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
        
        for widget in self.projects_analysis_frame.winfo_children():
            widget.destroy()
        
        projects = self.analysis_data["projects"]
        
        for project_key, data in projects.items():
            project_name = PROJECT_NAMES.get(project_key, project_key)
            
            project_frame = tk.Frame(self.projects_analysis_frame, bg="#f8f9fa", 
                                    padx=12, pady=10, relief=tk.FLAT, bd=1)
            project_frame.pack(fill=tk.X, pady=5)
            
            header_frame = tk.Frame(project_frame, bg="#f8f9fa")
            header_frame.pack(fill=tk.X)
            
            tk.Label(header_frame, text=project_name, font=("Microsoft YaHei", 11, "bold"),
                    bg="#f8f9fa", fg=self.THEME_TEXT_DARK).pack(side=tk.LEFT)
            
            tk.Label(header_frame, text=f"平均: {data['avg_score']:.1f}分", 
                    font=("Microsoft YaHei", 10),
                    bg="#f8f9fa", fg=self.THEME_PRIMARY).pack(side=tk.RIGHT)
            
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
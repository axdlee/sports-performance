# -*- coding: utf-8 -*-
"""
历史趋势标签页
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from config.constants import THEME_COLORS, FONTS
from ui.custom_button import CustomButton


class TrendTab:
    """历史趋势标签页"""
    
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
        trend_frame = tk.Frame(self.parent, bg=self.THEME_BG)
        
        canvas = tk.Canvas(trend_frame, bg=self.THEME_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(trend_frame, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg=self.THEME_BG, pady=10, padx=10)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 趋势图表卡片
        chart_card, chart_content = self.create_card_frame(scrollable_frame, "📈 成绩趋势图")
        chart_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.chart_frame = tk.Frame(chart_content, bg=self.THEME_CARD, height=400)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        self.chart_frame.pack_propagate(False)
        
        self.chart_placeholder = tk.Label(
            self.chart_frame, 
            text="加载中...",
            font=FONTS["text_normal"],
            bg=self.THEME_CARD,
            fg=self.THEME_TEXT_LIGHT
        )
        self.chart_placeholder.place(relx=0.5, rely=0.5, anchor="center")
        
        # 控制按钮框架
        button_frame = tk.Frame(chart_content, bg=self.THEME_CARD)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        refresh_btn = CustomButton(button_frame, text="🔄 刷新图表", 
                                   command=self.render_chart_in_window,
                                   font=FONTS["text_small"],
                                   bg=self.THEME_PRIMARY, fg="white",
                                   width=12, height=1,
                                   activebackground=THEME_COLORS["primary_dark"])
        refresh_btn.pack(side=tk.LEFT)
        
        # 历史记录卡片
        history_card, history_content = self.create_card_frame(scrollable_frame, "📜 历史记录列表")
        history_card.pack(fill=tk.BOTH, expand=True)
        
        # 自定义 Treeview 样式
        style = ttk.Style()
        style.configure("History.Treeview", 
                       font=FONTS["text_small"],
                       rowheight=30,
                       background="white",
                       fieldbackground="white",
                       borderwidth=0)
        style.configure("History.Treeview.Heading", 
                       font=FONTS["section_title"],
                       background=THEME_COLORS["bg"],
                       foreground=self.THEME_TEXT_DARK,
                       relief="flat")
        style.map("History.Treeview", 
                 background=[('selected', self.THEME_PRIMARY_LIGHT)],
                 foreground=[('selected', self.THEME_TEXT_DARK)])
        
        columns = ("序号", "日期", "必选项", "第一类", "第二类", "总分", "等级")
        self.history_tree = ttk.Treeview(history_content, columns=columns, show="headings", height=10, style="History.Treeview")
        
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
        
        history_scrollbar = ttk.Scrollbar(history_content, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.frame = trend_frame
    
    def render_chart_in_window(self):
        """在窗口中渲染趋势图"""
        records = self.user.get_all_records()
        
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        if len(records) < 2:
            label = tk.Label(
                self.chart_frame,
                text="📊 需要至少2条记录才能生成趋势图\n\n请先录入更多成绩数据",
                font=FONTS["text_normal"],
                bg=self.THEME_CARD,
                fg=self.THEME_TEXT_LIGHT
            )
            label.place(relx=0.5, rely=0.5, anchor="center")
            return
        
        try:
            plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'Microsoft YaHei']
            plt.rcParams['axes.unicode_minus'] = False
            
            # 使用更现代的图表样式
            fig = Figure(figsize=(9, 4), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            # 移除顶部和右侧边框
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color(THEME_COLORS["text_light"])
            ax.spines['bottom'].set_color(THEME_COLORS["text_light"])
            
            dates = [r['date'] for r in records]
            total_scores = [r['scores']['total'] for r in records]
            required_scores = [r['scores']['required'] for r in records]
            category1_scores = [r['scores']['category1'] for r in records]
            category2_scores = [r['scores']['category2'] for r in records]
            
            # 绘制线条
            ax.plot(range(len(dates)), total_scores, marker='o', linewidth=3, 
                   markersize=8, label='总分', color=THEME_COLORS["primary"], zorder=3)
            ax.plot(range(len(dates)), required_scores, marker='s', linewidth=2, 
                   markersize=6, label='必选项', color=THEME_COLORS["info"], alpha=0.6)
            ax.plot(range(len(dates)), category1_scores, marker='^', linewidth=2, 
                   markersize=6, label='第一类选考', color=THEME_COLORS["success"], alpha=0.6)
            ax.plot(range(len(dates)), category2_scores, marker='d', linewidth=2, 
                   markersize=6, label='第二类选考', color=THEME_COLORS["warning"], alpha=0.6)
            
            # 设置标题和标签
            ax.set_title(f'{self.user.name} - 成绩趋势分析', 
                        fontsize=14, fontweight='bold', pad=20, color=THEME_COLORS["text_dark"])
            ax.set_xlabel('测试日期', fontsize=10, color=THEME_COLORS["text_light"])
            ax.set_ylabel('得分', fontsize=10, color=THEME_COLORS["text_light"])
            
            # 设置坐标轴
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(dates, rotation=30, ha='right', fontsize=9, color=THEME_COLORS["text_normal"])
            ax.tick_params(axis='y', colors=THEME_COLORS["text_normal"])
            
            ax.set_ylim(0, 10.5)
            ax.set_yticks(range(0, 11, 2))
            
            # 网格线
            ax.grid(True, linestyle='--', alpha=0.2, zorder=0, color=THEME_COLORS["text_light"])
            
            # 图例
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                     ncol=4, frameon=False, fontsize=9)
            
            fig.tight_layout()
            
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
                font=FONTS["text_normal"],
                bg=self.THEME_CARD,
                fg=self.THEME_DANGER
            )
            label.place(relx=0.5, rely=0.5, anchor="center")

    # ... (refresh_chart, export_chart 方法保持不变) ...

    def display_history_records(self, records):
        """显示历史记录"""
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
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
    
    def refresh_data(self, updated_user):
        """刷新数据 - 使用最新的用户数据更新趋势"""
        self.user = updated_user
        records = self.user.get_all_records()
        
        # 重新渲染图表
        self.render_chart_in_window()
        
        # 更新历史记录
        self.display_history_records(records)
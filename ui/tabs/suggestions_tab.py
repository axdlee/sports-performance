# -*- coding: utf-8 -*-
"""
训练建议标签页
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict
from config.constants import (
    PROJECT_NAMES, THEME_COLORS, FONTS,
    SCORE_EVALUATION_TEXTS, WEAKNESS_INTENSITY_TEXTS,
    PROJECT_IMPROVEMENT_SUGGESTIONS, DETAILED_TRAINING_PLANS,
    LIFE_SUGGESTIONS_TEXT, SCORE_PRIORITY
)


class SuggestionsTab:
    """训练建议标签页"""
    
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
        suggestions_frame = tk.Frame(self.parent, bg=self.THEME_BG)
        
        canvas = tk.Canvas(suggestions_frame, bg=self.THEME_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(suggestions_frame, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg=self.THEME_BG, padx=130, pady=15)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
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
        
        self.life_text = tk.Text(life_content, wrap=tk.WORD, height=28, 
                                font=("Microsoft YaHei", 10), bg=self.THEME_CARD, 
                                fg=self.THEME_TEXT_DARK, relief=tk.FLAT, state=tk.DISABLED)
        self.life_text.pack(fill=tk.BOTH, expand=True)
        
        self.frame = suggestions_frame
    
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
        if total_score >= SCORE_EVALUATION_TEXTS["excellent"]["threshold"]:
            return SCORE_EVALUATION_TEXTS["excellent"]["text"]
        elif total_score >= SCORE_EVALUATION_TEXTS["good"]["threshold"]:
            return SCORE_EVALUATION_TEXTS["good"]["text"]
        elif total_score >= SCORE_EVALUATION_TEXTS["medium"]["threshold"]:
            return SCORE_EVALUATION_TEXTS["medium"]["text"]
        elif total_score >= SCORE_EVALUATION_TEXTS["pass"]["threshold"]:
            return SCORE_EVALUATION_TEXTS["pass"]["text"]
        else:
            return SCORE_EVALUATION_TEXTS["fail"]["text"]
    
    def get_weakness_suggestions(self, weakest_item: str, score: float) -> str:
        """获取弱项针对性建议"""
        item_name = self.get_item_display_name(weakest_item)
        
        if weakest_item in PROJECT_IMPROVEMENT_SUGGESTIONS:
            base_suggestion = PROJECT_IMPROVEMENT_SUGGESTIONS[weakest_item].get(self.user.gender, "")
        else:
            base_suggestion = "建议加强该项训练，提高技术水平。"
        
        if score < 3:
            intensity_data = WEAKNESS_INTENSITY_TEXTS["very_low"]
        elif score < 5:
            intensity_data = WEAKNESS_INTENSITY_TEXTS["low"]
        elif score < 7:
            intensity_data = WEAKNESS_INTENSITY_TEXTS["medium"]
        else:
            intensity_data = WEAKNESS_INTENSITY_TEXTS["high"]
        
        intensity = intensity_data["text"] + "\n\n"
        frequency = intensity_data["frequency"]
        
        detailed_training = self.get_detailed_training_plan(weakest_item)
        
        return f"【{item_name}】当前得分: {score:.1f}/10.0\n\n{intensity}{base_suggestion}\n\n{frequency}\n\n{detailed_training}"
    
    def get_detailed_training_plan(self, project_key: str) -> str:
        """获取详细训练计划"""
        if project_key in ["required", "category1", "category2"]:
            return "请参考各单项的详细训练计划。"
        
        return DETAILED_TRAINING_PLANS.get(project_key, "请咨询专业教练制定个性化训练计划。")
    
    def display_training_plan(self, scores: Dict[str, float]):
        """显示分项训练计划"""
        for widget in self.training_frame.winfo_children():
            widget.destroy()
        
        items = [(k, v) for k, v in scores.items() if k != "total"]
        items.sort(key=lambda x: x[1])
        
        for item_key, score in items:
            item_name = self.get_item_display_name(item_key)
            
            if score < SCORE_PRIORITY["high"]["threshold"]:
                priority = SCORE_PRIORITY["high"]["label"]
                bg_color = SCORE_PRIORITY["high"]["bg_color"]
            elif score < SCORE_PRIORITY["medium"]["threshold"]:
                priority = SCORE_PRIORITY["medium"]["label"]
                bg_color = SCORE_PRIORITY["medium"]["bg_color"]
            else:
                priority = SCORE_PRIORITY["low"]["label"]
                bg_color = SCORE_PRIORITY["low"]["bg_color"]
            
            project_frame = tk.Frame(self.training_frame, bg=bg_color, 
                                    padx=12, pady=10, relief=tk.FLAT, bd=1)
            project_frame.pack(fill=tk.X, pady=5)
            
            header_frame = tk.Frame(project_frame, bg=bg_color)
            header_frame.pack(fill=tk.X)
            
            tk.Label(header_frame, text=f"{item_name} - {score:.1f}分", 
                    font=("Microsoft YaHei", 11, "bold"),
                    bg=bg_color, fg=self.THEME_TEXT_DARK).pack(side=tk.LEFT)
            
            tk.Label(header_frame, text=priority, font=("Microsoft YaHei", 9),
                    bg=bg_color, fg=self.THEME_TEXT_DARK).pack(side=tk.RIGHT)
            
            if item_key not in ["required", "category1", "category2"]:
                plan = self.get_detailed_training_plan(item_key)
                tk.Label(project_frame, text=plan, font=("Microsoft YaHei", 9),
                        bg=bg_color, fg=self.THEME_TEXT_DARK, 
                        justify=tk.LEFT, anchor="w").pack(anchor="w", pady=(5, 0))
    
    def get_life_suggestions(self, total_score: float) -> str:
        """获取生活建议"""
        return LIFE_SUGGESTIONS_TEXT
    
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
    
    def refresh_data(self, updated_user):
        """刷新数据 - 使用最新的用户数据更新建议"""
        self.user = updated_user
        records = self.user.get_all_records()
        
        if not records:
            return
        
        # 重新生成训练建议
        latest_record = records[-1]
        self.generate_training_suggestions(latest_record)
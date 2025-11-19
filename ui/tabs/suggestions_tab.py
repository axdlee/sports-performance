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
        suggestions_frame = tk.Frame(self.parent, bg=self.THEME_BG)
        
        canvas = tk.Canvas(suggestions_frame, bg=self.THEME_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(suggestions_frame, orient="vertical", command=canvas.yview)
        
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
        
        # 总体评价卡片
        overall_card, overall_content = self.create_card_frame(scrollable_frame, "📝 总体评价")
        overall_card.pack(fill=tk.X, pady=(0, 15))
        
        self.overall_text = tk.Text(overall_content, height=4, font=FONTS["text_normal"],
                                   bg=self.THEME_CARD, fg=self.THEME_TEXT_DARK,
                                   relief=tk.FLAT, wrap=tk.WORD)
        self.overall_text.pack(fill=tk.X)
        self.overall_text.config(state=tk.DISABLED)
        
        # 弱项针对性建议卡片
        weakness_card, weakness_content = self.create_card_frame(scrollable_frame, "⚠️ 弱项针对性建议", self.THEME_DANGER)
        weakness_card.pack(fill=tk.X, pady=(0, 15))
        
        self.weakness_frame = tk.Frame(weakness_content, bg=self.THEME_CARD)
        self.weakness_frame.pack(fill=tk.BOTH, expand=True)
        
        # 分项训练计划卡片
        plan_card, plan_content = self.create_card_frame(scrollable_frame, "🏋️ 分项训练计划")
        plan_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.plan_frame = tk.Frame(plan_content, bg=self.THEME_CARD)
        self.plan_frame.pack(fill=tk.BOTH, expand=True)
        
        # 生活与训练建议卡片
        lifestyle_card, lifestyle_content = self.create_card_frame(scrollable_frame, "🥗 生活与训练建议", self.THEME_SUCCESS)
        lifestyle_card.pack(fill=tk.X, pady=(0, 15))
        
        self.lifestyle_text = tk.Text(lifestyle_content, height=8, font=FONTS["text_normal"],
                                     bg=self.THEME_CARD, fg=self.THEME_TEXT_DARK,
                                     relief=tk.FLAT, wrap=tk.WORD)
        self.lifestyle_text.pack(fill=tk.X)
        self.lifestyle_text.config(state=tk.DISABLED)
        
        self.frame = suggestions_frame
    
    def display_suggestions(self, record: Dict):
        """显示建议"""
        scores = record["scores"]
        total_score = scores["total"]
        
        # 1. 总体评价
        grade = self.score_calculator.get_grade_level(total_score)
        
        if total_score >= 100:
            evaluation = f"🎉 恭喜！你的总成绩为 {total_score:.1f} 分，达到【{grade}】水平。你的体能状况非常优秀，请继续保持！"
        elif total_score >= 90:
            evaluation = f"👏 很好！你的总成绩为 {total_score:.1f} 分，达到【{grade}】水平。你的体能状况良好，仍有提升空间。"
        elif total_score >= 70:
            evaluation = f"💪 加油！你的总成绩为 {total_score:.1f} 分，达到【{grade}】水平。你的体能状况中等，需要加强训练。"
        else:
            evaluation = f"⚠️ 注意！你的总成绩为 {total_score:.1f} 分，达到【{grade}】水平。建议制定详细的训练计划并严格执行。"
            
        self.overall_text.config(state=tk.NORMAL)
        self.overall_text.delete(1.0, tk.END)
        self.overall_text.insert(tk.END, evaluation)
        self.overall_text.config(state=tk.DISABLED)
        
        # 2. 弱项建议
        for widget in self.weakness_frame.winfo_children():
            widget.destroy()
            
        weakest_item = self.score_calculator.get_weakest_item(scores)
        if weakest_item:
            # 获取类别的中文名称
            if weakest_item == "required":
                weakest_name = "必选项"
            elif weakest_item == "category1":
                weakest_name = "第一类选考"
            elif weakest_item == "category2":
                weakest_name = "第二类选考"
            else:
                weakest_name = PROJECT_NAMES.get(weakest_item, weakest_item)
            
            score = scores[weakest_item]
            
            # 弱项标题
            header_frame = tk.Frame(self.weakness_frame, bg=self.THEME_CARD)
            header_frame.pack(fill=tk.X, pady=(0, 10))
            
            tk.Label(header_frame, text=f"主要弱项: {weakest_name}", 
                    font=FONTS["label_font_bold"],
                    bg=self.THEME_CARD, fg=self.THEME_DANGER).pack(side=tk.LEFT)
            
            tk.Label(header_frame, text=f"得分: {score:.1f}", 
                    font=FONTS["text_normal"],
                    bg=self.THEME_CARD, fg=self.THEME_TEXT_LIGHT).pack(side=tk.LEFT, padx=10)
            
            # 建议内容
            suggestions = self.score_calculator.get_improvement_suggestions(weakest_item, score)
            
            for suggestion in suggestions:
                s_frame = tk.Frame(self.weakness_frame, bg=THEME_COLORS["weak_bg"], padx=15, pady=10, relief=tk.FLAT)
                s_frame.pack(fill=tk.X, pady=2)
                
                # 使用 Text widget 避免竖排问题
                text_widget = tk.Text(s_frame, height=3, font=FONTS["text_normal"],
                        bg=THEME_COLORS["weak_bg"], fg=self.THEME_TEXT_DARK,
                        wrap=tk.WORD, relief=tk.FLAT, bd=0)
                text_widget.insert("1.0", f"• {suggestion}")
                text_widget.config(state=tk.DISABLED)  # 设置为只读
                text_widget.pack(fill=tk.X)
        else:
            tk.Label(self.weakness_frame, text="暂无明显弱项，请继续保持全面发展！",
                    font=FONTS["text_normal"],
                    bg=self.THEME_CARD, fg=self.THEME_SUCCESS).pack(anchor="w")
            
        # 3. 分项训练计划
        for widget in self.plan_frame.winfo_children():
            widget.destroy()
            
        # 获取所有项目及其得分
        project_items = [
            ("required", list(record["required"].keys())[0], scores["required"]),
            ("category1", list(record["category1"].keys())[0], scores["category1"]),
            ("category2", list(record["category2"].keys())[0], scores["category2"])
        ]
        
        for category, project, score in project_items:
            project_name = PROJECT_NAMES.get(project, project)
            
            # 项目容器
            p_frame = tk.Frame(self.plan_frame, bg=self.THEME_CARD, pady=10)
            p_frame.pack(fill=tk.X)
            
            # 项目标题
            title_frame = tk.Frame(p_frame, bg=self.THEME_CARD)
            title_frame.pack(fill=tk.X, pady=(0, 5))
            
            tk.Label(title_frame, text=project_name, font=FONTS["label_font_bold"],
                    bg=self.THEME_CARD, fg=self.THEME_PRIMARY).pack(side=tk.LEFT)
            
            if score < 60:
                status = "重点加强"
                color = self.THEME_DANGER
            elif score < 80:
                status = "巩固提升"
                color = self.THEME_WARNING
            else:
                status = "保持优势"
                color = self.THEME_SUCCESS
                
            tk.Label(title_frame, text=status, font=FONTS["text_tiny"],
                    bg=color, fg="white", padx=5).pack(side=tk.LEFT, padx=10)
            
            # 训练计划内容
            plan_text = self.get_detailed_training_plan(project)
            
            content_frame = tk.Frame(p_frame, bg=THEME_COLORS["bg"], padx=15, pady=10)
            content_frame.pack(fill=tk.X)
            
            tk.Label(content_frame, text=plan_text, font=FONTS["text_small"],
                    bg=THEME_COLORS["bg"], fg=self.THEME_TEXT_DARK,
                    justify=tk.LEFT, wraplength=700).pack(anchor="w", fill=tk.X)
            
            # 分割线
            tk.Frame(self.plan_frame, bg=THEME_COLORS["border"], height=1).pack(fill=tk.X, pady=5)

        # 4. 生活建议
        lifestyle_tips = [
            "• 保证充足睡眠：每天建议睡眠时间7-8小时，利于体能恢复。",
            "• 科学饮食：注意蛋白质和碳水化合物的摄入，运动后及时补充水分。",
            "• 规律作息：保持良好的作息习惯，避免熬夜。",
            "• 心理调节：保持积极乐观的心态，适当进行放松训练。"
        ]
        
        self.lifestyle_text.config(state=tk.NORMAL)
        self.lifestyle_text.delete(1.0, tk.END)
        self.lifestyle_text.insert(tk.END, "\n\n".join(lifestyle_tips))
        self.lifestyle_text.config(state=tk.DISABLED)
    
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
        self.display_suggestions(latest_record)
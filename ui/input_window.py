# -*- coding: utf-8 -*-
"""
成绩录入界面
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable, Dict
from config.scoring_standards import parse_time_to_seconds, get_scoring_data
from models.user import User
from models.score import ScoreRecord
from services.score_calculator import ScoreCalculator
from services.data_manager import DataManager
from utils.validator import DataValidator
from config.constants import (
    GENDER_MALE, GENDER_FEMALE, PROJECT_NAMES,
    INPUT_WINDOW_CONFIG, WINDOW_SIZES, WINDOW_TITLES,
    BUTTON_TEXTS, LABEL_FRAME_TITLES, INPUT_HINTS, PROJECT_LABELS, UI_TEXTS
)
from ui.custom_button import CustomButton


class InputWindow:
    """成绩录入窗口类"""
    
    def __init__(self, user: User, parent=None):
        self.user = user
        self.parent = parent
        self.score_calculator = ScoreCalculator()
        self.data_manager = DataManager()
        self.on_save_success: Optional[Callable] = None
        
        self.setup_ui()
        self.update_ui_for_gender()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主窗口
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.window.title(WINDOW_TITLES["input"].format(self.user.name))
        self.window.geometry(WINDOW_SIZES["input"])
        self.window.resizable(False, False)
        
        # 设置窗口背景色
        self.window.configure(bg=INPUT_WINDOW_CONFIG["bg_color"])
        
        # 设置窗口居中
        self.center_window()
        
        # 创建外层容器
        outer_frame = tk.Frame(self.window, bg=INPUT_WINDOW_CONFIG["bg_color"])
        outer_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建Canvas和滚动条
        canvas = tk.Canvas(outer_frame, bg=INPUT_WINDOW_CONFIG["bg_color"], highlightthickness=0)
        scrollbar = tk.Scrollbar(outer_frame, orient=tk.VERTICAL, command=canvas.yview)
        
        # 创建可滚动的主框架
        main_frame = tk.Frame(canvas, bg=INPUT_WINDOW_CONFIG["bg_color"], padx=30, pady=25)
        
        # 配置Canvas
        main_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=main_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 布局Canvas和滚动条
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定鼠标滚轮事件
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self._mousewheel_handler = _on_mousewheel
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # 窗口关闭时解绑事件
        def _on_closing():
            canvas.unbind_all("<MouseWheel>")
            self.window.destroy()
        
        self.window.protocol("WM_DELETE_WINDOW", _on_closing)
        
        # 确保Canvas宽度自适应
        def _configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", _configure_canvas)
        
        # 保存引用以便后续使用
        self.canvas = canvas
        self.scrollbar = scrollbar
        
        # 标题框架
        title_frame = tk.Frame(main_frame, bg=INPUT_WINDOW_CONFIG["title_bg"], pady=25)
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        # 标题
        title_label = tk.Label(title_frame, text=f"📝 成绩录入 - {self.user.name}", 
                               font=INPUT_WINDOW_CONFIG["title_font"],
                               bg=INPUT_WINDOW_CONFIG["title_bg"], fg=INPUT_WINDOW_CONFIG["title_fg"])
        title_label.pack()
        
        # 副标题
        subtitle_label = tk.Label(title_frame, text="Score Entry System",
                                 font=INPUT_WINDOW_CONFIG["subtitle_font"],
                                 bg=INPUT_WINDOW_CONFIG["title_bg"], fg=INPUT_WINDOW_CONFIG["bg_color"])
        subtitle_label.pack(pady=(5, 0))
        
        # 必选项框架
        required_frame = tk.LabelFrame(main_frame, text=LABEL_FRAME_TITLES["required"], 
                                       font=INPUT_WINDOW_CONFIG["section_font"],
                                       bg=INPUT_WINDOW_CONFIG["frame_bg"], fg=INPUT_WINDOW_CONFIG["required_color"],
                                       padx=25, pady=20, relief=tk.FLAT, bd=2)
        required_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 必选项标签
        self.required_label = tk.Label(required_frame, text="", 
                                      font=INPUT_WINDOW_CONFIG["label_font_bold"],
                                      bg=INPUT_WINDOW_CONFIG["frame_bg"], fg=INPUT_WINDOW_CONFIG["label_primary_color"])
        self.required_label.pack(anchor=tk.W, pady=(0, 8))
        
        # 时间输入框架（分钟和秒钟）
        time_input_frame = tk.Frame(required_frame, bg=INPUT_WINDOW_CONFIG["frame_bg"])
        time_input_frame.pack(anchor=tk.W, pady=(0, 10))
        
        # 分钟输入
        tk.Label(time_input_frame, text="分钟:", 
                font=INPUT_WINDOW_CONFIG["label_font_small"],
                bg=INPUT_WINDOW_CONFIG["frame_bg"], fg=INPUT_WINDOW_CONFIG["label_secondary_color"]).pack(side=tk.LEFT)
        
        self.required_minutes_var = tk.IntVar(value=0)
        self.required_minutes_spinbox = tk.Spinbox(time_input_frame, 
                                                   from_=0, to=10,
                                                   textvariable=self.required_minutes_var,
                                                   width=5, font=INPUT_WINDOW_CONFIG["entry_font"],
                                                   justify=tk.CENTER,
                                                   relief=tk.SOLID, bd=1)
        self.required_minutes_spinbox.pack(side=tk.LEFT, padx=(5, 15))
        
        # 秒钟输入
        tk.Label(time_input_frame, text="秒钟:", 
                font=INPUT_WINDOW_CONFIG["label_font_small"],
                bg=INPUT_WINDOW_CONFIG["frame_bg"], fg=INPUT_WINDOW_CONFIG["label_secondary_color"]).pack(side=tk.LEFT)
        
        self.required_seconds_var = tk.IntVar(value=0)
        self.required_seconds_spinbox = tk.Spinbox(time_input_frame, 
                                                   from_=0, to=59,
                                                   textvariable=self.required_seconds_var,
                                                   width=5, font=INPUT_WINDOW_CONFIG["entry_font"],
                                                   justify=tk.CENTER,
                                                   relief=tk.SOLID, bd=1)
        self.required_seconds_spinbox.pack(side=tk.LEFT, padx=5)
        
        # 提示文本
        hint_label = tk.Label(required_frame, text=INPUT_HINTS["spinbox_hint"],
                            font=INPUT_WINDOW_CONFIG["label_font_tiny"],
                            bg=INPUT_WINDOW_CONFIG["frame_bg"], fg=INPUT_WINDOW_CONFIG["label_hint_color"])
        hint_label.pack(anchor=tk.W, pady=(0, 8))
        
        # 得分显示
        self.required_score_var = tk.StringVar(value="得分: --")
        self.required_score_label = tk.Label(required_frame, textvariable=self.required_score_var, 
                                           font=INPUT_WINDOW_CONFIG["label_font_bold"],
                                           bg=INPUT_WINDOW_CONFIG["frame_bg"], fg=INPUT_WINDOW_CONFIG["score_display_color"])
        self.required_score_label.pack(anchor=tk.W)
        
        # 第一类选考框架
        category1_frame = tk.LabelFrame(main_frame, text=LABEL_FRAME_TITLES["category1"], 
                                        font=INPUT_WINDOW_CONFIG["section_font"],
                                        bg=INPUT_WINDOW_CONFIG["frame_bg"], fg=INPUT_WINDOW_CONFIG["category1_color"],
                                        padx=25, pady=20, relief=tk.FLAT, bd=2)
        category1_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 项目选择
        tk.Label(category1_frame, text="选择项目",
                font=INPUT_WINDOW_CONFIG["label_font_bold"],
                bg=INPUT_WINDOW_CONFIG["frame_bg"], fg=INPUT_WINDOW_CONFIG["label_primary_color"]).pack(anchor=tk.W, pady=(0, 5))
        self.category1_var = tk.StringVar()
        self.category1_combo = ttk.Combobox(category1_frame, textvariable=self.category1_var, 
                                          state="readonly", width=25, font=INPUT_WINDOW_CONFIG["label_font_small"])
        self.category1_combo.pack(anchor=tk.W, pady=(0, 12))
        
        # 成绩输入
        self.category1_label = tk.Label(category1_frame, text="",
                                       font=INPUT_WINDOW_CONFIG["label_font_bold"],
                                       bg=INPUT_WINDOW_CONFIG["frame_bg"], fg=INPUT_WINDOW_CONFIG["label_primary_color"])
        self.category1_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.category1_var_value = tk.StringVar()
        self.category1_entry = tk.Entry(category1_frame, textvariable=self.category1_var_value, 
                                        width=15, font=INPUT_WINDOW_CONFIG["entry_font"],
                                        relief=tk.SOLID, bd=1,
                                        highlightthickness=1, highlightcolor=INPUT_WINDOW_CONFIG["label_primary_color"])
        self.category1_entry.pack(anchor=tk.W, pady=(0, 8), ipady=3)
        
        self.category1_score_var = tk.StringVar(value="得分: --")
        self.category1_score_label = tk.Label(category1_frame, textvariable=self.category1_score_var, 
                                            font=INPUT_WINDOW_CONFIG["label_font_bold"],
                                            bg=INPUT_WINDOW_CONFIG["frame_bg"], fg=INPUT_WINDOW_CONFIG["score_display_color"])
        self.category1_score_label.pack(anchor=tk.W)
        
        # 第二类选考框架
        category2_frame = tk.LabelFrame(main_frame, text=LABEL_FRAME_TITLES["category2"], 
                                        font=INPUT_WINDOW_CONFIG["section_font"],
                                        bg=INPUT_WINDOW_CONFIG["frame_bg"], fg=INPUT_WINDOW_CONFIG["category2_color"],
                                        padx=25, pady=20, relief=tk.FLAT, bd=2)
        category2_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 项目选择
        tk.Label(category2_frame, text="选择项目",
                font=INPUT_WINDOW_CONFIG["label_font_bold"],
                bg=INPUT_WINDOW_CONFIG["frame_bg"], fg=INPUT_WINDOW_CONFIG["label_primary_color"]).pack(anchor=tk.W, pady=(0, 5))
        self.category2_var = tk.StringVar()
        self.category2_combo = ttk.Combobox(category2_frame, textvariable=self.category2_var, 
                                          state="readonly", width=25, font=INPUT_WINDOW_CONFIG["label_font_small"])
        self.category2_combo.pack(anchor=tk.W, pady=(0, 12))
        
        # 成绩输入
        self.category2_label = tk.Label(category2_frame, text="",
                                       font=INPUT_WINDOW_CONFIG["label_font_bold"],
                                       bg=INPUT_WINDOW_CONFIG["frame_bg"], fg=INPUT_WINDOW_CONFIG["label_primary_color"])
        self.category2_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.category2_var_value = tk.StringVar()
        self.category2_entry = tk.Entry(category2_frame, textvariable=self.category2_var_value, 
                                        width=15, font=INPUT_WINDOW_CONFIG["entry_font"],
                                        relief=tk.SOLID, bd=1,
                                        highlightthickness=1, highlightcolor=INPUT_WINDOW_CONFIG["label_primary_color"])
        self.category2_entry.pack(anchor=tk.W, pady=(0, 8), ipady=3)
        
        self.category2_score_var = tk.StringVar(value="得分: --")
        self.category2_score_label = tk.Label(category2_frame, textvariable=self.category2_score_var, 
                                            font=INPUT_WINDOW_CONFIG["label_font_bold"],
                                            bg=INPUT_WINDOW_CONFIG["frame_bg"], fg=INPUT_WINDOW_CONFIG["score_display_color"])
        self.category2_score_label.pack(anchor=tk.W)
        
        # 总分显示框架
        total_frame = tk.LabelFrame(main_frame, text=" 📊 总分计算 ", 
                                    font=INPUT_WINDOW_CONFIG["section_font"],
                                    bg=INPUT_WINDOW_CONFIG["frame_bg"], fg=INPUT_WINDOW_CONFIG["label_primary_color"],
                                    padx=25, pady=20, relief=tk.FLAT, bd=2)
        total_frame.pack(fill=tk.X, pady=(0, 25))
        
        self.total_score_var = tk.StringVar(value="总分: --")
        self.total_score_label = tk.Label(total_frame, textvariable=self.total_score_var, 
                                         font=INPUT_WINDOW_CONFIG["score_font"],
                                         bg=INPUT_WINDOW_CONFIG["frame_bg"], fg=INPUT_WINDOW_CONFIG["score_total_color"])
        self.total_score_label.pack()
        
        # 按钮框架
        button_frame = tk.Frame(main_frame, bg=INPUT_WINDOW_CONFIG["bg_color"])
        button_frame.pack(fill=tk.X)
        
        # 保存按钮
        self.save_button = CustomButton(button_frame, text=BUTTON_TEXTS["save"], 
                                        command=self.handle_save,
                                        font=INPUT_WINDOW_CONFIG["section_font"],
                                        bg=INPUT_WINDOW_CONFIG["save_button_bg"], fg="white",
                                        width=12, height=2)
        self.save_button.pack(side=tk.LEFT, padx=(0, 15), fill=tk.X, expand=True)
        
        # 重置按钮
        self.reset_button = CustomButton(button_frame, text=BUTTON_TEXTS["reset"], 
                                         command=self.handle_reset,
                                         font=INPUT_WINDOW_CONFIG["section_font"],
                                         bg=INPUT_WINDOW_CONFIG["reset_button_bg"], fg="white",
                                         width=12, height=2)
        self.reset_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 绑定事件
        self.bind_events()
    
    def center_window(self):
        """窗口居中显示"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def update_ui_for_gender(self):
        """根据性别更新界面"""
        if self.user.gender == GENDER_MALE:
            # 男生必选项
            self.required_label.config(text="1000米跑")
            self.required_project = "1000m"
            
            # 第一类选考项目
            category1_options = [
                ("50m", "50米跑"),
                ("sit_reach", "坐位体前屈"),
                ("standing_jump", "立定跳远"),
                ("pull_ups", "引体向上")
            ]
        else:
            # 女生必选项
            self.required_label.config(text="800米跑")
            self.required_project = "800m"
            
            # 第一类选考项目
            category1_options = [
                ("50m", "50米跑"),
                ("sit_reach", "坐位体前屈"),
                ("standing_jump", "立定跳远"),
                ("sit_ups", "仰卧起坐")
            ]
        
        # 设置第一类选考选项
        self.category1_combo['values'] = [option[1] for option in category1_options]
        self.category1_options_map = {option[1]: option[0] for option in category1_options}
        
        # 第二类选考项目
        category2_options = [
            ("basketball", "篮球运球"),
            ("football", "足球运球"),
            ("volleyball", "排球垫球")
        ]
        self.category2_combo['values'] = [option[1] for option in category2_options]
        self.category2_options_map = {option[1]: option[0] for option in category2_options}
    
    def bind_events(self):
        """绑定事件"""
        # 必选项输入变化（监听Spinbox变化）
        self.required_minutes_var.trace_add('write', self.on_required_change)
        self.required_seconds_var.trace_add('write', self.on_required_change)
        
        # 第一类选考变化
        self.category1_var.trace_add('write', self.on_category1_change)
        self.category1_var_value.trace_add('write', self.on_category1_value_change)
        
        # 第二类选考变化
        self.category2_var.trace_add('write', self.on_category2_change)
        self.category2_var_value.trace_add('write', self.on_category2_value_change)
    
    def on_required_change(self, *args):
        """必选项输入变化"""
        self.calculate_required_score()
        self.update_total_score()
    
    def on_category1_change(self, *args):
        """第一类选考项目变化"""
        project_name = self.category1_var.get()
        if project_name:
            project_key = self.category1_options_map[project_name]
            self.update_category1_label(project_key)
        self.calculate_category1_score()
        self.update_total_score()
    
    def on_category1_value_change(self, *args):
        """第一类选考成绩变化"""
        self.calculate_category1_score()
        self.update_total_score()
    
    def on_category2_change(self, *args):
        """第二类选考项目变化"""
        project_name = self.category2_var.get()
        if project_name:
            project_key = self.category2_options_map[project_name]
            self.update_category2_label(project_key)
        self.calculate_category2_score()
        self.update_total_score()
    
    def on_category2_value_change(self, *args):
        """第二类选考成绩变化"""
        self.calculate_category2_score()
        self.update_total_score()
    
    def update_category1_label(self, project_key: str):
        """更新第一类选考标签"""
        # 获取该项目的评分标准范围
        scoring_data = get_scoring_data(self.user.gender)
        standards = scoring_data.get(project_key, [])
        
        labels = {
            "50m": "50米跑 (秒)",
            "sit_reach": "坐位体前屈 (厘米)",
            "standing_jump": "立定跳远 (厘米)",
            "pull_ups": "引体向上 (次)",
            "sit_ups": "仰卧起坐 (次)"
        }
        
        label_text = labels.get(project_key, "")
        
        # 添加范围提示
        if standards:
            if project_key == "50m":  # 越小越好
                min_val = standards[0][0]
                max_val = standards[-1][0]
                label_text += f" | 范围: {min_val:.1f}~{max_val:.1f}"
            elif project_key in ["sit_reach", "standing_jump", "pull_ups", "sit_ups"]:  # 越大越好
                max_val = standards[0][0]
                min_val = standards[-1][0]
                label_text += f" | 范围: {min_val:.0f}~{max_val:.0f}"
        
        self.category1_label.config(text=label_text)
    
    def update_category2_label(self, project_key: str):
        """更新第二类选考标签"""
        # 获取该项目的评分标准范围
        scoring_data = get_scoring_data(self.user.gender)
        standards = scoring_data.get(project_key, [])
        
        labels = {
            "basketball": "篮球运球 (秒)",
            "football": "足球运球 (秒)",
            "volleyball": "排球垫球 (次)"
        }
        
        label_text = labels.get(project_key, "")
        
        # 添加范围提示
        if standards:
            if project_key in ["basketball", "football"]:  # 越小越好
                min_val = standards[0][0]
                max_val = standards[-1][0]
                label_text += f" | 范围: {min_val:.1f}~{max_val:.1f}"
            else:  # volleyball - 越大越好
                max_val = standards[0][0]
                min_val = standards[-1][0]
                label_text += f" | 范围: {min_val}~{max_val}"
        
        self.category2_label.config(text=label_text)
    
    def calculate_required_score(self):
        """计算必选项得分"""
        try:
            minutes = self.required_minutes_var.get()
            seconds = self.required_seconds_var.get()
            
            if minutes == 0 and seconds == 0:
                self.required_score_var.set("得分: --")
                return
            
            # 转换为总秒数
            performance = minutes * 60 + seconds
            
            # 获取评分标准范围
            scoring_data = get_scoring_data(self.user.gender)
            standards = scoring_data[self.required_project]
            min_time = standards[0][0]  # 最好成绩
            max_time = standards[-1][0]  # 最差成绩
            
            # 限制在合理范围内
            if performance < min_time:
                performance = min_time
            elif performance > max_time:
                performance = max_time
            
            # 计算得分
            score = self.score_calculator.calculate_score(self.user.gender, self.required_project, performance)
            
            self.required_score_var.set(f"得分: {score:.1f}")
            
        except Exception as e:
            self.required_score_var.set("得分: 输入错误")
    
    def _clamp_performance(self, project_key: str, performance: float) -> float:
        """将成绩值限制在评分标准范围内"""
        try:
            scoring_data = get_scoring_data(self.user.gender)
            if project_key not in scoring_data:
                return performance
            
            standards = scoring_data[project_key]
            
            # 对于"越小越好"的项目（跑步、运球类）
            if project_key in ["1000m", "800m", "50m", "basketball", "football"]:
                min_val = standards[0][0]  # 最好成绩（最小值）
                max_val = standards[-1][0]  # 最差成绩（最大值）
                return max(min_val, min(performance, max_val))
            # 对于"越大越好"的项目（跳远、仰卧起坐、引体向上、排球等）
            else:
                max_val = standards[0][0]  # 最好成绩（最大值）
                min_val = standards[-1][0]  # 最差成绩（最小值）
                return max(min_val, min(performance, max_val))
        except:
            return performance
    
    def calculate_category1_score(self):
        """计算第一类选考得分"""
        try:
            project_name = self.category1_var.get()
            value_str = self.category1_var_value.get().strip()
            
            if not project_name or not value_str:
                self.category1_score_var.set("得分: --")
                return
            
            project_key = self.category1_options_map[project_name]
            
            # 根据项目类型验证和转换输入
            if project_key == "50m":
                performance = float(value_str)
            elif project_key in ["sit_reach", "standing_jump"]:
                performance = float(value_str)
            else:  # pull_ups, sit_ups
                performance = int(value_str)
            
            # 限制在评分标准范围内
            performance = self._clamp_performance(project_key, performance)
            
            # 计算得分
            score = self.score_calculator.calculate_score(self.user.gender, project_key, performance)
            
            self.category1_score_var.set(f"得分: {score:.1f}")
            
        except Exception as e:
            self.category1_score_var.set("得分: 输入错误")
    
    def calculate_category2_score(self):
        """计算第二类选考得分"""
        try:
            project_name = self.category2_var.get()
            value_str = self.category2_var_value.get().strip()
            
            if not project_name or not value_str:
                self.category2_score_var.set("得分: --")
                return
            
            project_key = self.category2_options_map[project_name]
            
            # 根据项目类型验证和转换输入
            if project_key in ["basketball", "football"]:
                performance = float(value_str)
            else:  # volleyball
                performance = int(value_str)
            
            # 限制在评分标准范围内
            performance = self._clamp_performance(project_key, performance)
            
            # 计算得分
            score = self.score_calculator.calculate_score(self.user.gender, project_key, performance)
            
            self.category2_score_var.set(f"得分: {score:.1f}")
            
        except Exception as e:
            self.category2_score_var.set("得分: 输入错误")
    
    def update_total_score(self):
        """更新总分显示"""
        try:
            # 获取各项得分
            required_score = self.get_score_from_label(self.required_score_var.get())
            category1_score = self.get_score_from_label(self.category1_score_var.get())
            category2_score = self.get_score_from_label(self.category2_score_var.get())
            
            if required_score is not None and category1_score is not None and category2_score is not None:
                total = required_score + category1_score + category2_score
                self.total_score_var.set(f"总分: {total:.1f}")
            else:
                self.total_score_var.set("总分: --")
                
        except Exception:
            self.total_score_var.set("总分: --")
    
    def get_score_from_label(self, label_text: str) -> Optional[float]:
        """从标签文本中提取得分"""
        try:
            if "得分: " in label_text and label_text != "得分: --" and label_text != "得分: 输入错误":
                score_str = label_text.split("得分: ")[1]
                return float(score_str)
        except:
            pass
        return None
    
    def validate_input(self) -> bool:
        """验证输入数据"""
        # 验证必选项
        minutes = self.required_minutes_var.get()
        seconds = self.required_seconds_var.get()
        
        if minutes == 0 and seconds == 0:
            messagebox.showerror(UI_TEXTS["input_error"], INPUT_HINTS["required_time"])
            return False
        
        if seconds >= 60:
            messagebox.showerror(UI_TEXTS["input_error"], INPUT_HINTS["seconds_range"])
            return False
        
        # 验证第一类选考
        if not self.category1_var.get():
            messagebox.showerror(UI_TEXTS["input_error"], INPUT_HINTS["category1_required"])
            return False
        
        if not self.category1_var_value.get().strip():
            messagebox.showerror(UI_TEXTS["input_error"], INPUT_HINTS["category1_score"])
            return False
        
        # 验证第二类选考
        if not self.category2_var.get():
            messagebox.showerror(UI_TEXTS["input_error"], INPUT_HINTS["category2_required"])
            return False
        
        if not self.category2_var_value.get().strip():
            messagebox.showerror(UI_TEXTS["input_error"], INPUT_HINTS["category2_score"])
            return False
        
        return True
    
    def handle_save(self):
        """处理保存"""
        if not self.validate_input():
            return
        
        try:
            # 准备数据
            required_project = self.required_project
            required_value = self.required_minutes_var.get() * 60 + self.required_seconds_var.get()
            
            category1_project = self.category1_options_map[self.category1_var.get()]
            category1_value = self.parse_category1_value(category1_project, self.category1_var_value.get().strip())
            
            category2_project = self.category2_options_map[self.category2_var.get()]
            category2_value = self.parse_category2_value(category2_project, self.category2_var_value.get().strip())
            
            # 计算得分
            scores = self.score_calculator.calculate_total_score(
                self.user.gender,
                {required_project: required_value},
                {category1_project: category1_value},
                {category2_project: category2_value}
            )
            
            # 创建成绩记录
            record_data = {
                "date": ScoreRecord({}, {}, {}).date,  # 使用当前日期
                "required": {required_project: required_value},
                "category1": {category1_project: category1_value},
                "category2": {category2_project: category2_value},
                "scores": scores,
                "total_score": scores["total"]
            }
            
            # 使用DataManager保存记录（会自动添加到用户对象并保存到文件）
            if self.data_manager.add_score_record(self.user.id, record_data):
                messagebox.showinfo(UI_TEXTS["save_success"], f"成绩已保存！\n总分: {scores['total']:.1f}")
                
                if self.on_save_success:
                    self.on_save_success(record_data)
                
                self.handle_reset()
            else:
                messagebox.showerror(UI_TEXTS["save_failed"], "无法保存成绩记录，请检查用户是否存在")
            
        except Exception as e:
            messagebox.showerror(UI_TEXTS["save_failed"], f"保存成绩时发生错误: {str(e)}")
    
    def parse_category1_value(self, project: str, value_str: str):
        """解析第一类选考值"""
        if project == "50m":
            performance = float(value_str)
        elif project in ["sit_reach", "standing_jump"]:
            performance = float(value_str)
        else:  # pull_ups, sit_ups
            performance = int(value_str)
        
        # 限制在评分标准范围内
        return self._clamp_performance(project, performance)
    
    def parse_category2_value(self, project: str, value_str: str):
        """解析第二类选考值"""
        if project in ["basketball", "football"]:
            performance = float(value_str)
        else:  # volleyball
            performance = int(value_str)
        
        # 限制在评分标准范围内
        return self._clamp_performance(project, performance)
    
    def handle_reset(self):
        """处理重置"""
        self.required_minutes_var.set(0)
        self.required_seconds_var.set(0)
        self.category1_var.set("")
        self.category1_var_value.set("")
        self.category2_var.set("")
        self.category2_var_value.set("")
        
        self.required_score_var.set("得分: --")
        self.category1_score_var.set("得分: --")
        self.category2_score_var.set("得分: --")
        self.total_score_var.set("总分: --")
    
    def set_save_callback(self, callback: Callable):
        """设置保存成功回调函数"""
        self.on_save_success = callback
    
    def show(self):
        """显示窗口"""
        self.window.mainloop()
    
    def destroy(self):
        """销毁窗口"""
        if self.window:
            self.window.destroy()

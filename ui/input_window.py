# -*- coding: utf-8 -*-
"""
成绩录入界面
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable, Dict
from config.scoring_standards import parse_time_to_seconds
from models.user import User
from models.score import ScoreRecord
from services.score_calculator import ScoreCalculator
from utils.validator import DataValidator
from config.constants import GENDER_MALE, GENDER_FEMALE, PROJECT_NAMES


class InputWindow:
    """成绩录入窗口类"""
    
    def __init__(self, user: User, parent=None):
        self.user = user
        self.parent = parent
        self.score_calculator = ScoreCalculator()
        self.on_save_success: Optional[Callable] = None
        
        self.setup_ui()
        self.update_ui_for_gender()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主窗口
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.window.title(f"成绩录入 - {self.user.name}")
        self.window.geometry("600x700")
        self.window.resizable(False, False)
        
        # 设置窗口居中
        self.center_window()
        
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text=f"成绩录入 - {self.user.name}", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 必选项框架
        required_frame = ttk.LabelFrame(main_frame, text="必选项 (10分)", padding="15")
        required_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 必选项标签和输入框
        self.required_label = ttk.Label(required_frame, text="", font=("Arial", 12))
        self.required_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.required_var = tk.StringVar()
        self.required_entry = ttk.Entry(required_frame, textvariable=self.required_var, 
                                       width=20, font=("Arial", 11))
        self.required_entry.pack(anchor=tk.W, pady=(0, 5))
        
        self.required_score_var = tk.StringVar(value="得分: --")
        self.required_score_label = ttk.Label(required_frame, textvariable=self.required_score_var, 
                                            foreground="blue", font=("Arial", 10, "bold"))
        self.required_score_label.pack(anchor=tk.W)
        
        # 第一类选考框架
        category1_frame = ttk.LabelFrame(main_frame, text="第一类选考 (10分)", padding="15")
        category1_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 项目选择
        ttk.Label(category1_frame, text="选择项目:").pack(anchor=tk.W, pady=(0, 5))
        self.category1_var = tk.StringVar()
        self.category1_combo = ttk.Combobox(category1_frame, textvariable=self.category1_var, 
                                          state="readonly", width=20)
        self.category1_combo.pack(anchor=tk.W, pady=(0, 10))
        
        # 成绩输入
        self.category1_label = ttk.Label(category1_frame, text="", font=("Arial", 12))
        self.category1_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.category1_var_value = tk.StringVar()
        self.category1_entry = ttk.Entry(category1_frame, textvariable=self.category1_var_value, 
                                        width=20, font=("Arial", 11))
        self.category1_entry.pack(anchor=tk.W, pady=(0, 5))
        
        self.category1_score_var = tk.StringVar(value="得分: --")
        self.category1_score_label = ttk.Label(category1_frame, textvariable=self.category1_score_var, 
                                             foreground="blue", font=("Arial", 10, "bold"))
        self.category1_score_label.pack(anchor=tk.W)
        
        # 第二类选考框架
        category2_frame = ttk.LabelFrame(main_frame, text="第二类选考 (10分)", padding="15")
        category2_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 项目选择
        ttk.Label(category2_frame, text="选择项目:").pack(anchor=tk.W, pady=(0, 5))
        self.category2_var = tk.StringVar()
        self.category2_combo = ttk.Combobox(category2_frame, textvariable=self.category2_var, 
                                          state="readonly", width=20)
        self.category2_combo.pack(anchor=tk.W, pady=(0, 10))
        
        # 成绩输入
        self.category2_label = ttk.Label(category2_frame, text="", font=("Arial", 12))
        self.category2_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.category2_var_value = tk.StringVar()
        self.category2_entry = ttk.Entry(category2_frame, textvariable=self.category2_var_value, 
                                        width=20, font=("Arial", 11))
        self.category2_entry.pack(anchor=tk.W, pady=(0, 5))
        
        self.category2_score_var = tk.StringVar(value="得分: --")
        self.category2_score_label = ttk.Label(category2_frame, textvariable=self.category2_score_var, 
                                             foreground="blue", font=("Arial", 10, "bold"))
        self.category2_score_label.pack(anchor=tk.W)
        
        # 总分显示框架
        total_frame = ttk.LabelFrame(main_frame, text="总分计算", padding="15")
        total_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.total_score_var = tk.StringVar(value="总分: --")
        self.total_score_label = ttk.Label(total_frame, textvariable=self.total_score_var, 
                                         font=("Arial", 14, "bold"), foreground="red")
        self.total_score_label.pack()
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # 保存按钮
        self.save_button = ttk.Button(button_frame, text="保存成绩", 
                                    command=self.handle_save, width=15)
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 重置按钮
        self.reset_button = ttk.Button(button_frame, text="重置", 
                                      command=self.handle_reset, width=15)
        self.reset_button.pack(side=tk.LEFT)
        
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
            self.required_label.config(text="1000米跑 (秒，格式: 3'45\" 或 225)")
            
            # 第一类选考项目
            category1_options = [
                ("50m", "50米跑"),
                ("sit_reach", "坐位体前屈"),
                ("standing_jump", "立定跳远"),
                ("pull_ups", "引体向上")
            ]
        else:
            # 女生必选项
            self.required_label.config(text="800米跑 (秒，格式: 3'25\" 或 205)")
            
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
        # 必选项输入变化
        self.required_var.trace('w', self.on_required_change)
        
        # 第一类选考变化
        self.category1_var.trace('w', self.on_category1_change)
        self.category1_var_value.trace('w', self.on_category1_value_change)
        
        # 第二类选考变化
        self.category2_var.trace('w', self.on_category2_change)
        self.category2_var_value.trace('w', self.on_category2_value_change)
    
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
        labels = {
            "50m": "50米跑 (秒)",
            "sit_reach": "坐位体前屈 (厘米)",
            "standing_jump": "立定跳远 (厘米)",
            "pull_ups": "引体向上 (次)",
            "sit_ups": "仰卧起坐 (次)"
        }
        self.category1_label.config(text=labels.get(project_key, ""))
    
    def update_category2_label(self, project_key: str):
        """更新第二类选考标签"""
        labels = {
            "basketball": "篮球运球 (秒)",
            "football": "足球运球 (秒)",
            "volleyball": "排球垫球 (次)"
        }
        self.category2_label.config(text=labels.get(project_key, ""))
    
    def calculate_required_score(self):
        """计算必选项得分"""
        try:
            time_str = self.required_var.get().strip()
            if not time_str:
                self.required_score_var.set("得分: --")
                return
            
            # 解析时间
            from config.scoring_standards import parse_time_to_seconds
            performance = parse_time_to_seconds(time_str)
            
            # 计算得分
            project = "1000m" if self.user.gender == GENDER_MALE else "800m"
            score = self.score_calculator.calculate_score(self.user.gender, project, performance)
            
            self.required_score_var.set(f"得分: {score:.1f}")
            
        except Exception as e:
            self.required_score_var.set("得分: 输入错误")
    
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
                from config.scoring_standards import parse_time_to_seconds
                performance = parse_time_to_seconds(value_str)
            elif project_key in ["sit_reach", "standing_jump"]:
                performance = float(value_str)
            else:  # pull_ups, sit_ups
                performance = int(value_str)
            
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
        time_str = self.required_var.get().strip()
        if not time_str:
            messagebox.showerror("输入错误", "请输入必选项成绩")
            return False
        
        try:
            from config.scoring_standards import parse_time_to_seconds
            parse_time_to_seconds(time_str)
        except:
            messagebox.showerror("输入错误", "必选项时间格式不正确")
            return False
        
        # 验证第一类选考
        if not self.category1_var.get():
            messagebox.showerror("输入错误", "请选择第一类选考项目")
            return False
        
        if not self.category1_var_value.get().strip():
            messagebox.showerror("输入错误", "请输入第一类选考成绩")
            return False
        
        # 验证第二类选考
        if not self.category2_var.get():
            messagebox.showerror("输入错误", "请选择第二类选考项目")
            return False
        
        if not self.category2_var_value.get().strip():
            messagebox.showerror("输入错误", "请输入第二类选考成绩")
            return False
        
        return True
    
    def handle_save(self):
        """处理保存"""
        if not self.validate_input():
            return
        
        try:
            # 准备数据
            required_project = "1000m" if self.user.gender == GENDER_MALE else "800m"
            required_value = parse_time_to_seconds(self.required_var.get().strip())
            
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
            
            # 保存记录
            self.user.add_record(record_data)
            
            messagebox.showinfo("保存成功", f"成绩已保存！\n总分: {scores['total']:.1f}")
            
            if self.on_save_success:
                self.on_save_success(record_data)
            
            self.handle_reset()
            
        except Exception as e:
            messagebox.showerror("保存失败", f"保存成绩时发生错误: {str(e)}")
    
    def parse_category1_value(self, project: str, value_str: str):
        """解析第一类选考值"""
        if project == "50m":
            from config.scoring_standards import parse_time_to_seconds
            return parse_time_to_seconds(value_str)
        elif project in ["sit_reach", "standing_jump"]:
            return float(value_str)
        else:  # pull_ups, sit_ups
            return int(value_str)
    
    def parse_category2_value(self, project: str, value_str: str):
        """解析第二类选考值"""
        if project in ["basketball", "football"]:
            return float(value_str)
        else:  # volleyball
            return int(value_str)
    
    def handle_reset(self):
        """处理重置"""
        self.required_var.set("")
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

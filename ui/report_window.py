# -*- coding: utf-8 -*-
"""
成绩报告与曲线图界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Callable, Dict, List
from models.user import User
from services.score_calculator import ScoreCalculator
from utils.chart_generator import ChartGenerator
from config.constants import PROJECT_NAMES


class ReportWindow:
    """成绩报告窗口类"""
    
    def __init__(self, user: User, parent=None):
        self.user = user
        self.parent = parent
        self.score_calculator = ScoreCalculator()
        self.chart_generator = ChartGenerator()
        
        self.setup_ui()
        self.load_user_data()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主窗口
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.window.title(f"成绩报告 - {self.user.name}")
        self.window.geometry("900x700")
        self.window.resizable(True, True)
        
        # 设置窗口居中
        self.center_window()
        
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text=f"成绩报告 - {self.user.name}", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 创建笔记本控件（标签页）
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 当前成绩标签页
        self.setup_current_score_tab(notebook)
        
        # 历史趋势标签页
        self.setup_trend_tab(notebook)
        
        # 弱项分析标签页
        self.setup_weakness_tab(notebook)
    
    def center_window(self):
        """窗口居中显示"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_current_score_tab(self, notebook):
        """设置当前成绩标签页"""
        current_frame = ttk.Frame(notebook, padding="15")
        notebook.add(current_frame, text="当前成绩")
        
        # 成绩概览框架
        overview_frame = ttk.LabelFrame(current_frame, text="成绩概览", padding="15")
        overview_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 总分显示
        self.total_score_var = tk.StringVar(value="总分: --")
        total_label = ttk.Label(overview_frame, textvariable=self.total_score_var, 
                               font=("Arial", 18, "bold"), foreground="red")
        total_label.pack(pady=(0, 10))
        
        # 等级评定
        self.grade_var = tk.StringVar(value="等级: --")
        grade_label = ttk.Label(overview_frame, textvariable=self.grade_var, 
                               font=("Arial", 14), foreground="blue")
        grade_label.pack()
        
        # 详细成绩框架
        details_frame = ttk.LabelFrame(current_frame, text="详细成绩", padding="15")
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # 成绩表格
        columns = ("项目", "成绩", "得分", "状态")
        self.score_tree = ttk.Treeview(details_frame, columns=columns, show="headings", height=6)
        
        # 设置列标题和宽度
        self.score_tree.heading("项目", text="项目")
        self.score_tree.heading("成绩", text="成绩")
        self.score_tree.heading("得分", text="得分")
        self.score_tree.heading("状态", text="状态")
        
        self.score_tree.column("项目", width=120)
        self.score_tree.column("成绩", width=100)
        self.score_tree.column("得分", width=80)
        self.score_tree.column("状态", width=100)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.score_tree.yview)
        self.score_tree.configure(yscrollcommand=scrollbar.set)
        
        self.score_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_trend_tab(self, notebook):
        """设置历史趋势标签页"""
        trend_frame = ttk.Frame(notebook, padding="15")
        notebook.add(trend_frame, text="历史趋势")
        
        # 控制按钮框架
        control_frame = ttk.Frame(trend_frame)
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 生成图表按钮
        self.generate_chart_button = ttk.Button(control_frame, text="生成趋势图", 
                                              command=self.generate_trend_chart, width=15)
        self.generate_chart_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 导出图表按钮
        self.export_chart_button = ttk.Button(control_frame, text="导出图表", 
                                           command=self.export_chart, width=15)
        self.export_chart_button.pack(side=tk.LEFT)
        
        # 历史记录表格
        history_frame = ttk.LabelFrame(trend_frame, text="历史记录", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # 历史记录表格
        history_columns = ("日期", "必选项", "第一类选考", "第二类选考", "总分")
        self.history_tree = ttk.Treeview(history_frame, columns=history_columns, show="headings", height=10)
        
        # 设置列标题
        for col in history_columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=120)
        
        # 滚动条
        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_weakness_tab(self, notebook):
        """设置弱项分析标签页"""
        weakness_frame = ttk.Frame(notebook, padding="15")
        notebook.add(weakness_frame, text="弱项分析")
        
        # 弱项识别框架
        weakness_analysis_frame = ttk.LabelFrame(weakness_frame, text="弱项识别", padding="15")
        weakness_analysis_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 最弱项显示
        self.weakest_item_var = tk.StringVar(value="最弱项: --")
        weakest_label = ttk.Label(weakness_analysis_frame, textvariable=self.weakest_item_var, 
                                 font=("Arial", 14, "bold"), foreground="red")
        weakest_label.pack(pady=(0, 10))
        
        # 最强项显示
        self.strongest_item_var = tk.StringVar(value="最强项: --")
        strongest_label = ttk.Label(weakness_analysis_frame, textvariable=self.strongest_item_var, 
                                  font=("Arial", 14, "bold"), foreground="green")
        strongest_label.pack()
        
        # 改进建议框架
        suggestion_frame = ttk.LabelFrame(weakness_frame, text="改进建议", padding="15")
        suggestion_frame.pack(fill=tk.BOTH, expand=True)
        
        # 建议文本
        self.suggestion_text = tk.Text(suggestion_frame, wrap=tk.WORD, height=15, 
                                     font=("Arial", 11), state=tk.DISABLED)
        
        # 滚动条
        suggestion_scrollbar = ttk.Scrollbar(suggestion_frame, orient=tk.VERTICAL, command=self.suggestion_text.yview)
        self.suggestion_text.configure(yscrollcommand=suggestion_scrollbar.set)
        
        self.suggestion_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        suggestion_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_user_data(self):
        """加载用户数据"""
        records = self.user.get_all_records()
        
        if not records:
            self.show_no_data_message()
            return
        
        # 显示最新成绩
        latest_record = records[-1]
        self.display_current_score(latest_record)
        
        # 显示历史记录
        self.display_history_records(records)
        
        # 分析弱项
        self.analyze_weakness(latest_record)
    
    def show_no_data_message(self):
        """显示无数据消息"""
        self.total_score_var.set("总分: 暂无数据")
        self.grade_var.set("等级: 暂无数据")
        self.weakest_item_var.set("最弱项: 暂无数据")
        self.strongest_item_var.set("最强项: 暂无数据")
        
        # 清空建议文本
        self.suggestion_text.config(state=tk.NORMAL)
        self.suggestion_text.delete(1.0, tk.END)
        self.suggestion_text.insert(1.0, "暂无成绩数据，请先录入成绩。")
        self.suggestion_text.config(state=tk.DISABLED)
    
    def display_current_score(self, record: Dict):
        """显示当前成绩"""
        scores = record["scores"]
        total_score = scores["total"]
        
        # 更新总分和等级
        self.total_score_var.set(f"总分: {total_score:.1f}")
        grade = self.score_calculator.get_grade_level(total_score)
        self.grade_var.set(f"等级: {grade}")
        
        # 清空现有数据
        for item in self.score_tree.get_children():
            self.score_tree.delete(item)
        
        # 显示各项成绩
        self.add_score_item("必选项", record["required"], scores["required"])
        self.add_score_item("第一类选考", record["category1"], scores["category1"])
        self.add_score_item("第二类选考", record["category2"], scores["category2"])
    
    def add_score_item(self, category: str, performance: Dict, score: float):
        """添加成绩项目到表格"""
        project_key = list(performance.keys())[0]
        project_name = PROJECT_NAMES.get(project_key, project_key)
        performance_value = list(performance.values())[0]
        
        # 格式化成绩显示
        if project_key in ["1000m", "800m", "50m", "basketball", "football"]:
            from config.scoring_standards import format_seconds_to_time
            if project_key in ["1000m", "800m", "50m"]:
                formatted_value = format_seconds_to_time(performance_value)
            else:
                formatted_value = f"{performance_value:.1f}秒"
        elif project_key in ["sit_reach", "standing_jump"]:
            formatted_value = f"{performance_value:.1f}厘米"
        else:
            formatted_value = f"{performance_value}次"
        
        # 状态评估
        if score >= 9:
            status = "优秀"
            status_color = "green"
        elif score >= 7:
            status = "良好"
            status_color = "blue"
        elif score >= 5:
            status = "中等"
            status_color = "orange"
        else:
            status = "需改进"
            status_color = "red"
        
        # 插入数据
        item = self.score_tree.insert("", tk.END, values=(
            f"{category}\n{project_name}", formatted_value, f"{score:.1f}", status
        ))
        
        # 设置状态颜色（如果支持）
        try:
            self.score_tree.set(item, "状态", status)
        except:
            pass
    
    def display_history_records(self, records: List[Dict]):
        """显示历史记录"""
        # 清空现有数据
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # 按日期排序（最新的在前）
        sorted_records = sorted(records, key=lambda x: x["date"], reverse=True)
        
        for record in sorted_records:
            date = record["date"]
            required_score = record["scores"]["required"]
            category1_score = record["scores"]["category1"]
            category2_score = record["scores"]["category2"]
            total_score = record["scores"]["total"]
            
            self.history_tree.insert("", tk.END, values=(
                date, f"{required_score:.1f}", f"{category1_score:.1f}", 
                f"{category2_score:.1f}", f"{total_score:.1f}"
            ))
    
    def analyze_weakness(self, record: Dict):
        """分析弱项"""
        scores = record["scores"]
        
        # 识别最弱项和最强项
        weakest_item = self.score_calculator.get_weakest_item(scores)
        strongest_item = self.score_calculator.get_strongest_item(scores)
        
        # 更新显示
        if weakest_item:
            weakest_name = self.get_item_display_name(weakest_item)
            self.weakest_item_var.set(f"最弱项: {weakest_name}")
        
        if strongest_item:
            strongest_name = self.get_item_display_name(strongest_item)
            self.strongest_item_var.set(f"最强项: {strongest_name}")
        
        # 生成改进建议
        self.generate_suggestions(scores, weakest_item)
    
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
    
    def generate_suggestions(self, scores: Dict[str, float], weakest_item: Optional[str]):
        """生成改进建议"""
        self.suggestion_text.config(state=tk.NORMAL)
        self.suggestion_text.delete(1.0, tk.END)
        
        suggestions = []
        
        # 总体评价
        total_score = scores["total"]
        if total_score >= 27:
            suggestions.append("🎉 恭喜！您的体育成绩非常优秀，继续保持！")
        elif total_score >= 24:
            suggestions.append("👍 您的体育成绩良好，还有提升空间。")
        elif total_score >= 18:
            suggestions.append("📈 您的体育成绩中等，建议加强训练。")
        elif total_score >= 15:
            suggestions.append("⚠️ 您的体育成绩刚及格，需要重点加强。")
        else:
            suggestions.append("🚨 您的体育成绩不及格，需要系统性的训练计划。")
        
        suggestions.append("")  # 空行
        
        # 弱项建议
        if weakest_item:
            suggestion_text = self.score_calculator.get_improvement_suggestions(weakest_item, self.user.gender)
            suggestions.append(f"💡 针对最弱项的建议：")
            suggestions.append(suggestion_text)
            suggestions.append("")  # 空行
        
        # 各项具体建议
        suggestions.append("📋 各项训练建议：")
        
        for item_key, score in scores.items():
            if item_key == "total":
                continue
            
            item_name = self.get_item_display_name(item_key)
            
            if score < 5:
                suggestions.append(f"• {item_name}：得分较低，需要重点加强训练")
            elif score < 7:
                suggestions.append(f"• {item_name}：有提升空间，建议增加训练频率")
            elif score < 9:
                suggestions.append(f"• {item_name}：表现良好，保持现有训练强度")
            else:
                suggestions.append(f"• {item_name}：表现优秀，继续保持")
        
        suggestions.append("")  # 空行
        suggestions.append("💪 训练建议：")
        suggestions.append("• 制定合理的训练计划，循序渐进")
        suggestions.append("• 注意训练前后的热身和拉伸")
        suggestions.append("• 保持良好的作息和饮食习惯")
        suggestions.append("• 定期测试成绩，调整训练方案")
        
        # 插入建议文本
        self.suggestion_text.insert(1.0, "\n".join(suggestions))
        self.suggestion_text.config(state=tk.DISABLED)
    
    def generate_trend_chart(self):
        """生成趋势图"""
        records = self.user.get_all_records()
        
        if len(records) < 2:
            messagebox.showwarning("数据不足", "需要至少2条记录才能生成趋势图")
            return
        
        try:
            chart_path = self.chart_generator.generate_score_trend_chart(records, self.user.name)
            messagebox.showinfo("生成成功", f"趋势图已生成：\n{chart_path}")
        except Exception as e:
            messagebox.showerror("生成失败", f"生成趋势图时发生错误：{str(e)}")
    
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
            chart_path = self.chart_generator.generate_score_trend_chart(records, self.user.name, file_path)
            messagebox.showinfo("导出成功", f"图表已导出：\n{chart_path}")
        except Exception as e:
            messagebox.showerror("导出失败", f"导出图表时发生错误：{str(e)}")
    
    def show(self):
        """显示窗口"""
        self.window.mainloop()
    
    def destroy(self):
        """销毁窗口"""
        if self.window:
            self.window.destroy()

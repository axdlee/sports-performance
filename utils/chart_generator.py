# -*- coding: utf-8 -*-
"""
图表生成工具
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from typing import List, Dict
import os


class ChartGenerator:
    """图表生成器"""
    
    def __init__(self):
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    def generate_score_trend_chart(self, records: List[Dict], user_name: str, save_path: str = None) -> str:
        """生成成绩趋势图
        
        Args:
            records: 成绩记录列表
            user_name: 用户姓名
            save_path: 保存路径，如果为None则自动生成
            
        Returns:
            保存的文件路径
        """
        if not records:
            raise ValueError("没有成绩记录")
        
        # 提取数据
        dates = []
        total_scores = []
        required_scores = []
        category1_scores = []
        category2_scores = []
        
        for record in records:
            date = datetime.strptime(record["date"], "%Y-%m-%d")
            dates.append(date)
            total_scores.append(record["total_score"])
            required_scores.append(record["scores"]["required"])
            category1_scores.append(record["scores"]["category1"])
            category2_scores.append(record["scores"]["category2"])
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 绘制折线图
        ax.plot(dates, total_scores, 'o-', linewidth=2, markersize=6, label='总分', color='#2E86AB')
        ax.plot(dates, required_scores, 's-', linewidth=1.5, markersize=5, label='必选项', color='#A23B72')
        ax.plot(dates, category1_scores, '^-', linewidth=1.5, markersize=5, label='第一类选考', color='#F18F01')
        ax.plot(dates, category2_scores, 'd-', linewidth=1.5, markersize=5, label='第二类选考', color='#C73E1D')
        
        # 设置图表属性
        ax.set_title(f'{user_name} 体育成绩发展趋势图', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('日期', fontsize=12)
        ax.set_ylabel('得分', fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # 设置x轴日期格式
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//10)))
        plt.xticks(rotation=45)
        
        # 设置y轴范围
        ax.set_ylim(0, 30)
        
        # 添加水平参考线
        ax.axhline(y=27, color='green', linestyle='--', alpha=0.5, label='优秀线')
        ax.axhline(y=24, color='blue', linestyle='--', alpha=0.5, label='良好线')
        ax.axhline(y=18, color='orange', linestyle='--', alpha=0.5, label='及格线')
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        if save_path is None:
            # 使用用户数据目录
            try:
                from utils.path_helper import get_user_data_dir
                base_dir = get_user_data_dir()
            except ImportError:
                base_dir = "data"
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(base_dir, f"{user_name}_成绩趋势图_{timestamp}.png")
        
        # 确保目录存在
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def generate_score_distribution_chart(self, scores: Dict[str, float], user_name: str, save_path: str = None) -> str:
        """生成成绩分布图
        
        Args:
            scores: 各项得分字典
            user_name: 用户姓名
            save_path: 保存路径
            
        Returns:
            保存的文件路径
        """
        # 准备数据
        items = []
        values = []
        colors = []
        
        for key, value in scores.items():
            if key == "total":
                continue
            
            # 项目名称映射
            item_names = {
                "required": "必选项",
                "category1": "第一类选考",
                "category2": "第二类选考"
            }
            
            items.append(item_names.get(key, key))
            values.append(value)
            
            # 根据得分设置颜色
            if value >= 9:
                colors.append('#2E86AB')  # 蓝色 - 优秀
            elif value >= 7:
                colors.append('#A23B72')  # 紫色 - 良好
            elif value >= 5:
                colors.append('#F18F01')  # 橙色 - 中等
            else:
                colors.append('#C73E1D')  # 红色 - 需要改进
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 绘制柱状图
        bars = ax.bar(items, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
        
        # 在柱子上添加数值标签
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # 设置图表属性
        ax.set_title(f'{user_name} 各项成绩分布图', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('得分', fontsize=12)
        ax.set_ylim(0, 10.5)
        
        # 添加水平参考线
        ax.axhline(y=9, color='green', linestyle='--', alpha=0.5, label='优秀线')
        ax.axhline(y=7, color='blue', linestyle='--', alpha=0.5, label='良好线')
        ax.axhline(y=5, color='orange', linestyle='--', alpha=0.5, label='及格线')
        
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        if save_path is None:
            # 使用用户数据目录
            try:
                from utils.path_helper import get_user_data_dir
                base_dir = get_user_data_dir()
            except ImportError:
                base_dir = "data"
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(base_dir, f"{user_name}_成绩分布图_{timestamp}.png")
        
        # 确保目录存在
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path

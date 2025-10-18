# -*- coding: utf-8 -*-
"""
成绩计算与评分逻辑模块
"""

from typing import Dict, Tuple, Optional
from config.scoring_standards import get_scoring_data, parse_time_to_seconds
from config.constants import GRADE_STANDARDS, PROJECT_IMPROVEMENT_SUGGESTIONS


class ScoreCalculator:
    """成绩计算器"""
    
    def __init__(self):
        self.male_scoring = get_scoring_data("male")
        self.female_scoring = get_scoring_data("female")
    
    def calculate_score(self, gender: str, project: str, performance: float) -> float:
        """计算单项得分
        
        Args:
            gender: 性别 ("male" 或 "female")
            project: 项目名称
            performance: 成绩值
            
        Returns:
            得分 (0-10分)
        """
        scoring_data = self.male_scoring if gender == "male" else self.female_scoring
        
        if project not in scoring_data:
            raise ValueError(f"不支持的项目: {project}")
        
        score_table = scoring_data[project]
        
        # 线性插值计算得分
        return self._interpolate_score(score_table, performance)
    
    def _interpolate_score(self, score_table: list, performance: float) -> float:
        """使用线性插值计算得分
        
        Args:
            score_table: 评分表 [(成绩值, 得分), ...]
            performance: 实际成绩
            
        Returns:
            计算得出的得分
        """
        # 按成绩值排序
        sorted_table = sorted(score_table, key=lambda x: x[0])
        
        # 如果成绩超出范围，返回边界值
        if performance <= sorted_table[0][0]:
            return sorted_table[0][1]
        if performance >= sorted_table[-1][0]:
            return sorted_table[-1][1]
        
        # 找到成绩所在的区间
        for i in range(len(sorted_table) - 1):
            if sorted_table[i][0] <= performance <= sorted_table[i + 1][0]:
                # 线性插值
                x1, y1 = sorted_table[i]
                x2, y2 = sorted_table[i + 1]
                
                if x2 == x1:  # 避免除零
                    return y1
                
                # 线性插值公式
                score = y1 + (y2 - y1) * (performance - x1) / (x2 - x1)
                return round(score, 1)
        
        return 0.0
    
    def calculate_total_score(self, gender: str, required: Dict, category1: Dict, category2: Dict) -> Dict[str, float]:
        """计算总分
        
        Args:
            gender: 性别
            required: 必选项成绩 {"1000m": 220} 或 {"800m": 205}
            category1: 第一类选考成绩 {"50m": 7.5} 等
            category2: 第二类选考成绩 {"basketball": 12.0} 等
            
        Returns:
            包含各项得分和总分的字典
        """
        scores = {}
        
        # 计算必选项得分
        required_project = list(required.keys())[0]
        required_performance = list(required.values())[0]
        scores["required"] = self.calculate_score(gender, required_project, required_performance)
        
        # 计算第一类选考得分
        category1_project = list(category1.keys())[0]
        category1_performance = list(category1.values())[0]
        scores["category1"] = self.calculate_score(gender, category1_project, category1_performance)
        
        # 计算第二类选考得分
        category2_project = list(category2.keys())[0]
        category2_performance = list(category2.values())[0]
        scores["category2"] = self.calculate_score(gender, category2_project, category2_performance)
        
        # 计算总分
        scores["total"] = scores["required"] + scores["category1"] + scores["category2"]
        
        return scores
    
    def get_grade_level(self, total_score: float) -> str:
        """根据总分获取等级评定
        
        Args:
            total_score: 总分
            
        Returns:
            等级名称
        """
        for grade, standard in GRADE_STANDARDS.items():
            if standard["min"] <= total_score <= standard["max"]:
                return standard["name"]
        
        return "不及格"
    
    def get_weakest_item(self, scores: Dict[str, float]) -> Optional[str]:
        """获取最弱项
        
        Args:
            scores: 各项得分字典
            
        Returns:
            最弱项名称，如果没有则返回None
        """
        # 排除总分，找到单项最低分
        item_scores = {k: v for k, v in scores.items() if k != "total"}
        if not item_scores:
            return None
        
        return min(item_scores, key=item_scores.get)
    
    def get_strongest_item(self, scores: Dict[str, float]) -> Optional[str]:
        """获取最强项
        
        Args:
            scores: 各项得分字典
            
        Returns:
            最强项名称，如果没有则返回None
        """
        # 排除总分，找到单项最高分
        item_scores = {k: v for k, v in scores.items() if k != "total"}
        if not item_scores:
            return None
        
        return max(item_scores, key=item_scores.get)
    
    def get_improvement_suggestions(self, weakest_item: str, gender: str) -> str:
        """获取改进建议
        
        Args:
            weakest_item: 最弱项
            gender: 性别
            
        Returns:
            改进建议文本
        """
        # 从constants导入统一的改进建议
        if weakest_item in PROJECT_IMPROVEMENT_SUGGESTIONS:
            suggestions_dict = PROJECT_IMPROVEMENT_SUGGESTIONS[weakest_item]
            if gender in suggestions_dict:
                return suggestions_dict[gender]
        
        return "建议加强该项训练，提高技术水平。"

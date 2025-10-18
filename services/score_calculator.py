# -*- coding: utf-8 -*-
"""
成绩计算与评分逻辑模块
"""

from typing import Dict, Tuple, Optional
from config.scoring_standards import get_scoring_data, parse_time_to_seconds
from config.constants import GRADE_STANDARDS


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
        suggestions = {
            "required": {
                "male": "建议加强长跑训练，每周进行3-4次有氧运动，包括慢跑、间歇跑等，逐步提高心肺功能和耐力。",
                "female": "建议加强长跑训练，每周进行3-4次有氧运动，包括慢跑、间歇跑等，逐步提高心肺功能和耐力。"
            },
            "50m": {
                "male": "建议加强短跑训练，重点练习起跑、加速跑和冲刺技术，同时进行腿部力量训练。",
                "female": "建议加强短跑训练，重点练习起跑、加速跑和冲刺技术，同时进行腿部力量训练。"
            },
            "sit_reach": {
                "male": "建议加强柔韧性训练，每天进行拉伸练习，重点练习腰部、背部和腿部柔韧性。",
                "female": "建议加强柔韧性训练，每天进行拉伸练习，重点练习腰部、背部和腿部柔韧性。"
            },
            "standing_jump": {
                "male": "建议加强下肢爆发力训练，包括深蹲、蛙跳、立定跳远等练习，提高腿部肌肉力量。",
                "female": "建议加强下肢爆发力训练，包括深蹲、蛙跳、立定跳远等练习，提高腿部肌肉力量。"
            },
            "pull_ups": {
                "male": "建议加强上肢力量训练，包括引体向上、俯卧撑、哑铃练习等，提高背部、手臂和肩部力量。",
                "female": "建议加强上肢力量训练，包括引体向上、俯卧撑、哑铃练习等，提高背部、手臂和肩部力量。"
            },
            "sit_ups": {
                "male": "建议加强核心力量训练，包括仰卧起坐、平板支撑、卷腹等练习，提高腹部肌肉力量。",
                "female": "建议加强核心力量训练，包括仰卧起坐、平板支撑、卷腹等练习，提高腹部肌肉力量。"
            },
            "basketball": {
                "male": "建议加强篮球运球技术练习，包括原地运球、行进间运球、变向运球等，提高球感和协调性。",
                "female": "建议加强篮球运球技术练习，包括原地运球、行进间运球、变向运球等，提高球感和协调性。"
            },
            "football": {
                "male": "建议加强足球运球技术练习，包括脚内侧运球、脚外侧运球、变向运球等，提高球感和协调性。",
                "female": "建议加强足球运球技术练习，包括脚内侧运球、脚外侧运球、变向运球等，提高球感和协调性。"
            },
            "volleyball": {
                "male": "建议加强排球垫球技术练习，包括原地垫球、移动垫球、对墙垫球等，提高球感和协调性。",
                "female": "建议加强排球垫球技术练习，包括原地垫球、移动垫球、对墙垫球等，提高球感和协调性。"
            }
        }
        
        if weakest_item in suggestions and gender in suggestions[weakest_item]:
            return suggestions[weakest_item][gender]
        
        return "建议加强该项训练，提高技术水平。"

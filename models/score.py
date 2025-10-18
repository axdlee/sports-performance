# -*- coding: utf-8 -*-
"""
成绩数据模型
"""

from datetime import datetime
from typing import Dict, Optional


class ScoreRecord:
    """成绩记录类"""
    
    def __init__(self, required: Dict, category1: Dict, category2: Dict):
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.required = required  # 必选项成绩
        self.category1 = category1  # 第一类选考成绩
        self.category2 = category2  # 第二类选考成绩
        self.scores: Dict[str, float] = {}  # 各项得分
        self.total_score: float = 0.0  # 总分
    
    def calculate_total_score(self):
        """计算总分"""
        self.total_score = sum(self.scores.values())
    
    def get_weakest_item(self) -> Optional[str]:
        """获取最弱项"""
        if not self.scores:
            return None
        
        # 排除总分，找到单项最低分
        item_scores = {k: v for k, v in self.scores.items() if k != "total"}
        if not item_scores:
            return None
            
        return min(item_scores, key=item_scores.get)
    
    def get_strongest_item(self) -> Optional[str]:
        """获取最强项"""
        if not self.scores:
            return None
        
        # 排除总分，找到单项最高分
        item_scores = {k: v for k, v in self.scores.items() if k != "total"}
        if not item_scores:
            return None
            
        return max(item_scores, key=item_scores.get)
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "date": self.date,
            "required": self.required,
            "category1": self.category1,
            "category2": self.category2,
            "scores": self.scores,
            "total_score": self.total_score
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ScoreRecord':
        """从字典创建成绩记录对象"""
        record = cls(data["required"], data["category1"], data["category2"])
        record.date = data["date"]
        record.scores = data.get("scores", {})
        record.total_score = data.get("total_score", 0.0)
        return record

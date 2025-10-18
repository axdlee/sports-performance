# -*- coding: utf-8 -*-
"""
用户数据模型
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional


class User:
    """用户类"""
    
    def __init__(self, name: str, gender: str, student_id: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.gender = gender
        self.student_id = student_id
        self.records: List[Dict] = []
        self.created_at = datetime.now().isoformat()
    
    def add_record(self, record: Dict):
        """添加成绩记录"""
        self.records.append(record)
    
    def get_latest_record(self) -> Optional[Dict]:
        """获取最新成绩记录"""
        if not self.records:
            return None
        return self.records[-1]
    
    def get_all_records(self) -> List[Dict]:
        """获取所有成绩记录"""
        return self.records
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "student_id": self.student_id,
            "records": self.records,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """从字典创建用户对象"""
        user = cls(data["name"], data["gender"], data.get("student_id"))
        user.id = data["id"]
        user.records = data.get("records", [])
        user.created_at = data.get("created_at", datetime.now().isoformat())
        return user

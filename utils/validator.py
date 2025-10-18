# -*- coding: utf-8 -*-
"""
数据验证工具
"""

import re
from typing import Tuple, Optional


class DataValidator:
    """数据验证器"""
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """验证姓名"""
        if not name or not name.strip():
            return False, "姓名不能为空"
        
        name = name.strip()
        if len(name) < 2:
            return False, "姓名至少需要2个字符"
        
        if len(name) > 20:
            return False, "姓名不能超过20个字符"
        
        # 检查是否包含特殊字符
        if not re.match(r'^[\u4e00-\u9fa5a-zA-Z\s]+$', name):
            return False, "姓名只能包含中文、英文字母和空格"
        
        return True, ""
    
    @staticmethod
    def validate_student_id(student_id: str) -> Tuple[bool, str]:
        """验证学号（可选）"""
        if not student_id:
            return True, ""  # 学号是可选的
        
        student_id = student_id.strip()
        if len(student_id) < 3:
            return False, "学号至少需要3个字符"
        
        if len(student_id) > 20:
            return False, "学号不能超过20个字符"
        
        # 学号只能包含数字、字母和连字符
        if not re.match(r'^[a-zA-Z0-9\-]+$', student_id):
            return False, "学号只能包含数字、字母和连字符"
        
        return True, ""
    
    @staticmethod
    def validate_gender(gender: str) -> Tuple[bool, str]:
        """验证性别"""
        if gender not in ["male", "female"]:
            return False, "请选择性别"
        return True, ""
    
    @staticmethod
    def validate_time_input(time_str: str, min_value: float = 0, max_value: float = 1000) -> Tuple[bool, str, Optional[float]]:
        """验证时间输入"""
        if not time_str or not time_str.strip():
            return False, "时间不能为空", None
        
        time_str = time_str.strip()
        
        try:
            # 尝试解析时间格式
            seconds = DataValidator._parse_time_to_seconds(time_str)
            
            if seconds < min_value:
                return False, f"时间不能小于{min_value}秒", None
            
            if seconds > max_value:
                return False, f"时间不能大于{max_value}秒", None
            
            return True, "", seconds
            
        except ValueError:
            return False, "时间格式不正确，请使用格式如：3'45\" 或 3:45 或 225", None
    
    @staticmethod
    def validate_distance_input(distance_str: str, min_value: float = 0, max_value: float = 500) -> Tuple[bool, str, Optional[float]]:
        """验证距离输入（厘米）"""
        if not distance_str or not distance_str.strip():
            return False, "距离不能为空", None
        
        try:
            distance = float(distance_str.strip())
            
            if distance < min_value:
                return False, f"距离不能小于{min_value}厘米", None
            
            if distance > max_value:
                return False, f"距离不能大于{max_value}厘米", None
            
            return True, "", distance
            
        except ValueError:
            return False, "请输入有效的数字", None
    
    @staticmethod
    def validate_count_input(count_str: str, min_value: int = 0, max_value: int = 100) -> Tuple[bool, str, Optional[int]]:
        """验证次数输入"""
        if not count_str or not count_str.strip():
            return False, "次数不能为空", None
        
        try:
            count = int(count_str.strip())
            
            if count < min_value:
                return False, f"次数不能小于{min_value}", None
            
            if count > max_value:
                return False, f"次数不能大于{max_value}", None
            
            return True, "", count
            
        except ValueError:
            return False, "请输入有效的整数", None
    
    @staticmethod
    def _parse_time_to_seconds(time_str: str) -> float:
        """解析时间字符串为秒数"""
        if "'" in time_str and '"' in time_str:
            # 格式: "3'45""
            parts = time_str.replace('"', '').split("'")
            minutes = int(parts[0])
            seconds = int(parts[1])
            return minutes * 60 + seconds
        elif ":" in time_str:
            # 格式: "3:45"
            parts = time_str.split(":")
            minutes = int(parts[0])
            seconds = int(parts[1])
            return minutes * 60 + seconds
        else:
            # 纯秒数
            return float(time_str)

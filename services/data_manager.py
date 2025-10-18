# -*- coding: utf-8 -*-
"""
JSON数据存储管理模块
"""

import json
import os
from typing import List, Optional, Dict
from models.user import User
from config.constants import DATA_FILE


class DataManager:
    """数据管理器"""
    
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.users: List[User] = []
        self.load_data()
    
    def load_data(self):
        """从JSON文件加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.users = [User.from_dict(user_data) for user_data in data.get("users", [])]
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"加载数据文件失败: {e}")
                self.users = []
        else:
            self.users = []
            self.save_data()  # 创建空的数据文件
    
    def save_data(self):
        """保存数据到JSON文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            data = {
                "users": [user.to_dict() for user in self.users]
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据文件失败: {e}")
            raise
    
    def add_user(self, user: User) -> bool:
        """添加用户"""
        try:
            # 检查是否已存在同名用户
            if self.find_user_by_name(user.name):
                return False
            
            self.users.append(user)
            self.save_data()
            return True
        except Exception as e:
            print(f"添加用户失败: {e}")
            return False
    
    def find_user_by_name(self, name: str) -> Optional[User]:
        """根据姓名查找用户"""
        for user in self.users:
            if user.name == name:
                return user
        return None
    
    def find_user_by_id(self, user_id: str) -> Optional[User]:
        """根据ID查找用户"""
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    def get_all_users(self) -> List[User]:
        """获取所有用户"""
        return self.users.copy()
    
    def update_user(self, user: User) -> bool:
        """更新用户信息"""
        try:
            for i, existing_user in enumerate(self.users):
                if existing_user.id == user.id:
                    self.users[i] = user
                    self.save_data()
                    return True
            return False
        except Exception as e:
            print(f"更新用户失败: {e}")
            return False
    
    def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        try:
            for i, user in enumerate(self.users):
                if user.id == user_id:
                    del self.users[i]
                    self.save_data()
                    return True
            return False
        except Exception as e:
            print(f"删除用户失败: {e}")
            return False
    
    def add_score_record(self, user_id: str, record: Dict) -> bool:
        """为用户添加成绩记录"""
        try:
            user = self.find_user_by_id(user_id)
            if user:
                user.add_record(record)
                self.save_data()
                return True
            return False
        except Exception as e:
            print(f"添加成绩记录失败: {e}")
            return False
    
    def get_user_records(self, user_id: str) -> List[Dict]:
        """获取用户的所有成绩记录"""
        user = self.find_user_by_id(user_id)
        if user:
            return user.get_all_records()
        return []
    
    def get_user_latest_record(self, user_id: str) -> Optional[Dict]:
        """获取用户最新成绩记录"""
        user = self.find_user_by_id(user_id)
        if user:
            return user.get_latest_record()
        return None

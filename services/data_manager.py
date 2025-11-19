# -*- coding: utf-8 -*-
"""
JSON数据存储管理模块
"""

import json
import os
from typing import List, Optional, Dict
from models.user import User
from config.constants import DATA_FILE
from utils.logger import get_logger

# 获取日志实例
logger = get_logger()


class DataManager:
    """数据管理器"""
    
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.users: List[User] = []
        self.load_data()
    
    def load_data(self):
        """从JSON文件加载数据"""
        logger.info(f'开始加载数据文件: {self.data_file}')
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.users = [User.from_dict(user_data) for user_data in data.get("users", [])]
                    logger.info(f'成功加载 {len(self.users)} 个用户数据')
            except json.JSONDecodeError as e:
                logger.error(f'JSON解析错误: {e}', exc_info=True)
                self.users = []
            except (KeyError, ValueError) as e:
                logger.error(f'数据格式错误: {e}', exc_info=True)
                self.users = []
            except Exception as e:
                logger.error(f'加载数据文件时发生未知错误: {e}', exc_info=True)
                self.users = []
        else:
            logger.info('数据文件不存在，创建新文件')
            self.users = []
            self.save_data()  # 创建空的数据文件
    
    def save_data(self):
        """保存数据到JSON文件"""
        try:
            logger.debug(f'开始保存数据到: {self.data_file}')
            
            # 确保目录存在
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            data = {
                "users": [user.to_dict() for user in self.users]
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f'成功保存 {len(self.users)} 个用户数据')
        except IOError as e:
            logger.error(f"文件IO错误: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"保存数据文件失败: {e}", exc_info=True)
            raise
    
    def add_user(self, user: User) -> bool:
        """添加用户"""
        try:
            logger.info(f'尝试添加用户: {user.name} ({user.gender})')
            
            # 检查是否已存在同名用户
            if self.find_user_by_name(user.name):
                logger.warning(f'用户已存在: {user.name}')
                return False
            
            self.users.append(user)
            self.save_data()
            logger.info(f'成功添加用户: {user.name}')
            return True
        except Exception as e:
            logger.error(f"添加用户失败: {e}", exc_info=True)
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
            logger.debug(f'尝试更新用户: {user.name} (ID: {user.id})')
            
            for i, existing_user in enumerate(self.users):
                if existing_user.id == user.id:
                    self.users[i] = user
                    self.save_data()
                    logger.info(f'成功更新用户: {user.name}')
                    return True
            
            logger.warning(f'未找到用户: ID={user.id}')
            return False
        except Exception as e:
            logger.error(f"更新用户失败: {e}", exc_info=True)
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
            logger.debug(f'为用户添加成绩记录: user_id={user_id}')
            
            user = self.find_user_by_id(user_id)
            if user:
                user.add_record(record)
                self.save_data()
                logger.info(f'成功为用户 {user.name} 添加成绩记录')
                return True
            
            logger.warning(f'未找到用户: ID={user_id}')
            return False
        except Exception as e:
            logger.error(f"添加成绩记录失败: {e}", exc_info=True)
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

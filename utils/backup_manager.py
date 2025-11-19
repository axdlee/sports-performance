# -*- coding: utf-8 -*-
"""
数据备份与恢复模块
"""

import os
import shutil
import json
from datetime import datetime
from typing import Optional, List
from utils.logger import get_logger

logger = get_logger()


class BackupManager:
    """备份管理器"""
    
    def __init__(self, data_file: str):
        """初始化备份管理器
        
        Args:
            data_file: 数据文件路径
        """
        self.data_file = data_file
        self.backup_dir = self._get_backup_directory()
        self._ensure_backup_dir()
        logger.info(f'备份管理器初始化完成，备份目录: {self.backup_dir}')
    
    def _get_backup_directory(self) -> str:
        """获取备份目录"""
        try:
            from utils.path_helper import get_data_file_path
            backup_path = get_data_file_path('backups/placeholder')
            return os.path.dirname(backup_path)
        except ImportError:
            # 开发环境回退方案
            return 'data/backups'
    
    def _ensure_backup_dir(self):
        """确保备份目录存在"""
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            logger.debug(f'备份目录已准备就绪: {self.backup_dir}')
        except Exception as e:
            logger.error(f'创建备份目录失败: {e}', exc_info=True)
    
    def create_backup(self, backup_name: str = None) -> Optional[str]:
        """创建数据备份
        
        Args:
            backup_name: 备份名称，默认使用时间戳
            
        Returns:
            备份文件路径，失败返回None
        """
        try:
            if not os.path.exists(self.data_file):
                logger.warning(f'数据文件不存在，无法备份: {self.data_file}')
                return None
            
            # 生成备份文件名
            if backup_name is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_name = f'backup_{timestamp}.json'
            elif not backup_name.endswith('.json'):
                backup_name += '.json'
            
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            logger.info(f'开始创建备份: {backup_path}')
            
            # 复制文件
            shutil.copy2(self.data_file, backup_path)
            
            # 验证备份
            if self._verify_backup(backup_path):
                logger.info(f'备份创建成功: {backup_path}')
                
                # 清理旧备份（保留最近10个）
                self._cleanup_old_backups(keep_count=10)
                
                return backup_path
            else:
                logger.error(f'备份验证失败: {backup_path}')
                return None
                
        except Exception as e:
            logger.error(f'创建备份失败: {e}', exc_info=True)
            return None
    
    def restore_backup(self, backup_path: str) -> bool:
        """恢复备份
        
        Args:
            backup_path: 备份文件路径
            
        Returns:
            是否成功恢复
        """
        try:
            if not os.path.exists(backup_path):
                logger.error(f'备份文件不存在: {backup_path}')
                return False
            
            # 验证备份文件
            if not self._verify_backup(backup_path):
                logger.error(f'备份文件无效: {backup_path}')
                return False
            
            logger.info(f'开始恢复备份: {backup_path}')
            
            # 先备份当前数据（安全措施）
            if os.path.exists(self.data_file):
                safety_backup = self.create_backup('pre_restore_backup')
                logger.info(f'已创建恢复前安全备份: {safety_backup}')
            
            # 恢复备份
            shutil.copy2(backup_path, self.data_file)
            
            logger.info(f'备份恢复成功: {backup_path} -> {self.data_file}')
            return True
            
        except Exception as e:
            logger.error(f'恢复备份失败: {e}', exc_info=True)
            return False
    
    def list_backups(self) -> List[dict]:
        """列出所有备份
        
        Returns:
            备份信息列表，每项包含name, path, size, created_time
        """
        try:
            backups = []
            
            if not os.path.exists(self.backup_dir):
                return backups
            
            # 遍历备份目录
            for filename in os.listdir(self.backup_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.backup_dir, filename)
                    
                    # 获取文件信息
                    stat = os.stat(filepath)
                    
                    backups.append({
                        'name': filename,
                        'path': filepath,
                        'size': stat.st_size,
                        'created_time': datetime.fromtimestamp(stat.st_mtime),
                        'formatted_size': self._format_size(stat.st_size),
                        'formatted_time': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    })
            
            # 按创建时间降序排序
            backups.sort(key=lambda x: x['created_time'], reverse=True)
            
            logger.debug(f'找到 {len(backups)} 个备份文件')
            return backups
            
        except Exception as e:
            logger.error(f'列出备份失败: {e}', exc_info=True)
            return []
    
    def delete_backup(self, backup_path: str) -> bool:
        """删除指定备份
        
        Args:
            backup_path: 备份文件路径
            
        Returns:
            是否成功删除
        """
        try:
            if not os.path.exists(backup_path):
                logger.warning(f'备份文件不存在: {backup_path}')
                return False
            
            os.remove(backup_path)
            logger.info(f'备份已删除: {backup_path}')
            return True
            
        except Exception as e:
            logger.error(f'删除备份失败: {e}', exc_info=True)
            return False
    
    def _verify_backup(self, backup_path: str) -> bool:
        """验证备份文件有效性
        
        Args:
            backup_path: 备份文件路径
            
        Returns:
            是否有效
        """
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # 检查必要的数据结构
                if 'users' not in data:
                    logger.warning(f'备份文件缺少users字段: {backup_path}')
                    return False
                
                if not isinstance(data['users'], list):
                    logger.warning(f'备份文件users字段格式错误: {backup_path}')
                    return False
                
                return True
                
        except json.JSONDecodeError as e:
            logger.error(f'备份文件JSON格式错误: {e}')
            return False
        except Exception as e:
            logger.error(f'验证备份文件失败: {e}', exc_info=True)
            return False
    
    def _cleanup_old_backups(self, keep_count: int = 10):
        """清理旧备份，保留最近的N个
        
        Args:
            keep_count: 保留的备份数量
        """
        try:
            backups = self.list_backups()
            
            # 如果备份数量超过限制，删除旧的
            if len(backups) > keep_count:
                backups_to_delete = backups[keep_count:]
                
                for backup in backups_to_delete:
                    # 跳过手动命名的备份（不以backup_开头）
                    if not backup['name'].startswith('backup_'):
                        continue
                    
                    self.delete_backup(backup['path'])
                    logger.info(f'清理旧备份: {backup["name"]}')
                
        except Exception as e:
            logger.error(f'清理旧备份失败: {e}', exc_info=True)
    
    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小显示
        
        Args:
            size_bytes: 字节数
            
        Returns:
            格式化后的大小字符串
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def auto_backup(self) -> Optional[str]:
        """自动备份（每次程序启动或重要操作前调用）
        
        Returns:
            备份文件路径，失败返回None
        """
        try:
            # 检查是否需要备份（避免频繁备份）
            backups = self.list_backups()
            
            # 如果今天还没有自动备份，则创建一次
            today = datetime.now().strftime('%Y%m%d')
            today_auto_backups = [b for b in backups if today in b['name'] and b['name'].startswith('backup_')]
            
            if not today_auto_backups:
                logger.info('执行每日自动备份')
                return self.create_backup()
            else:
                logger.debug('今日已有自动备份，跳过')
                return None
                
        except Exception as e:
            logger.error(f'自动备份失败: {e}', exc_info=True)
            return None

# -*- coding: utf-8 -*-
"""
日志系统模块
提供统一的日志管理功能，支持文件日志和控制台日志
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import Optional


class Logger:
    """日志管理器"""
    
    _instance: Optional['Logger'] = None
    _initialized: bool = False
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化日志系统"""
        if not Logger._initialized:
            self._setup_logger()
            Logger._initialized = True
    
    def _setup_logger(self):
        """设置日志配置"""
        # 创建logger
        self.logger = logging.getLogger('SportsPerformance')
        self.logger.setLevel(logging.DEBUG)
        
        # 清除已有的handlers
        self.logger.handlers.clear()
        
        # 获取日志目录
        log_dir = self._get_log_directory()
        
        # 创建日志目录
        os.makedirs(log_dir, exist_ok=True)
        
        # 日志文件路径
        log_file = os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')
        
        # 创建文件handler（带日志轮转）
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # 创建控制台handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 创建formatter
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        
        # 设置formatter
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)
        
        # 添加handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info('日志系统初始化完成')
    
    def _get_log_directory(self) -> str:
        """获取日志目录路径"""
        try:
            from utils.path_helper import get_data_file_path
            # 使用path_helper获取日志目录
            log_dir = os.path.dirname(get_data_file_path('logs/placeholder'))
            return log_dir
        except ImportError:
            # 开发环境回退方案
            return 'logs'
    
    def debug(self, message: str):
        """记录DEBUG级别日志"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """记录INFO级别日志"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """记录WARNING级别日志"""
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False):
        """记录ERROR级别日志"""
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = False):
        """记录CRITICAL级别日志"""
        self.logger.critical(message, exc_info=exc_info)
    
    def exception(self, message: str):
        """记录异常信息（自动包含堆栈跟踪）"""
        self.logger.exception(message)


# 创建全局logger实例
_logger_instance = Logger()


def get_logger() -> Logger:
    """获取日志实例"""
    return _logger_instance


# 便捷函数
def debug(message: str):
    """记录DEBUG级别日志"""
    _logger_instance.debug(message)


def info(message: str):
    """记录INFO级别日志"""
    _logger_instance.info(message)


def warning(message: str):
    """记录WARNING级别日志"""
    _logger_instance.warning(message)


def error(message: str, exc_info: bool = False):
    """记录ERROR级别日志"""
    _logger_instance.error(message, exc_info=exc_info)


def critical(message: str, exc_info: bool = False):
    """记录CRITICAL级别日志"""
    _logger_instance.critical(message, exc_info=exc_info)


def exception(message: str):
    """记录异常信息"""
    _logger_instance.exception(message)

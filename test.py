# -*- coding: utf-8 -*-
"""
测试脚本 - 验证系统功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.score_calculator import ScoreCalculator
from services.data_manager import DataManager
from models.user import User
from config.scoring_standards import parse_time_to_seconds


def test_score_calculator():
    """测试成绩计算器"""
    print("测试成绩计算器...")
    
    calculator = ScoreCalculator()
    
    # 测试男生1000米跑
    score = calculator.calculate_score("male", "1000m", 240)  # 4分钟
    print(f"男生1000米跑 4分钟: {score:.1f}分")
    
    # 测试女生800米跑
    score = calculator.calculate_score("female", "800m", 200)  # 3分20秒
    print(f"女生800米跑 3分20秒: {score:.1f}分")
    
    # 测试总分计算
    scores = calculator.calculate_total_score(
        "male",
        {"1000m": 240},
        {"50m": 8.0},
        {"basketball": 15.0}
    )
    print(f"男生总分计算: {scores}")
    
    print("成绩计算器测试完成！\n")


def test_data_manager():
    """测试数据管理器"""
    print("测试数据管理器...")
    
    manager = DataManager()
    
    # 创建测试用户
    test_user = User("测试用户", "male", "TEST001")
    
    # 添加用户
    success = manager.add_user(test_user)
    print(f"添加用户: {'成功' if success else '失败'}")
    
    # 查找用户
    found_user = manager.find_user_by_name("测试用户")
    print(f"查找用户: {'成功' if found_user else '失败'}")
    
    # 添加成绩记录
    record = {
        "date": "2025-10-18",
        "required": {"1000m": 240},
        "category1": {"50m": 8.0},
        "category2": {"basketball": 15.0},
        "scores": {"required": 8.0, "category1": 7.0, "category2": 6.0, "total": 21.0},
        "total_score": 21.0
    }
    
    success = manager.add_score_record(test_user.id, record)
    print(f"添加成绩记录: {'成功' if success else '失败'}")
    
    # 获取用户记录
    records = manager.get_user_records(test_user.id)
    print(f"获取用户记录: {len(records)}条")
    
    print("数据管理器测试完成！\n")


def test_time_parsing():
    """测试时间解析"""
    print("测试时间解析...")
    
    test_cases = [
        "3'45\"",  # 3分45秒
        "3:45",    # 3分45秒
        "225",     # 225秒
        "1'30\"",  # 1分30秒
        "90"       # 90秒
    ]
    
    for time_str in test_cases:
        try:
            seconds = parse_time_to_seconds(time_str)
            print(f"{time_str} -> {seconds}秒")
        except Exception as e:
            print(f"{time_str} -> 解析失败: {e}")
    
    print("时间解析测试完成！\n")


def test_chart_generator():
    """测试图表生成器"""
    print("测试图表生成器...")
    
    try:
        from utils.chart_generator import ChartGenerator
        
        generator = ChartGenerator()
        
        # 创建测试数据
        test_records = [
            {
                "date": "2025-10-01",
                "required": {"1000m": 250},
                "category1": {"50m": 8.5},
                "category2": {"basketball": 16.0},
                "scores": {"required": 7.0, "category1": 6.5, "category2": 5.0, "total": 18.5},
                "total_score": 18.5
            },
            {
                "date": "2025-10-15",
                "required": {"1000m": 240},
                "category1": {"50m": 8.0},
                "category2": {"basketball": 15.0},
                "scores": {"required": 8.0, "category1": 7.0, "category2": 6.0, "total": 21.0},
                "total_score": 21.0
            }
        ]
        
        # 生成图表
        chart_path = generator.generate_score_trend_chart(test_records, "测试用户")
        print(f"图表生成成功: {chart_path}")
        
    except Exception as e:
        print(f"图表生成测试失败: {e}")
    
    print("图表生成器测试完成！\n")


def main():
    """主测试函数"""
    print("体育成绩评估系统 - 功能测试")
    print("=" * 50)
    
    try:
        # 运行各项测试
        test_score_calculator()
        test_data_manager()
        test_time_parsing()
        test_chart_generator()
        
        print("=" * 50)
        print("所有测试完成！系统功能正常。")
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

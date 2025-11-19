# -*- coding: utf-8 -*-
"""
优化功能测试脚本
用于验证新增的日志、导出和备份功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import get_logger
from utils.data_exporter import DataExporter
from utils.backup_manager import BackupManager
from services.data_manager import DataManager
from config.constants import DATA_FILE

# 初始化日志
logger = get_logger()


def test_logger():
    """测试日志系统"""
    print("=" * 50)
    print("测试1: 日志系统")
    print("=" * 50)
    
    logger.debug("这是一条DEBUG日志")
    logger.info("这是一条INFO日志")
    logger.warning("这是一条WARNING日志")
    logger.error("这是一条ERROR日志")
    
    print("✅ 日志系统测试完成")
    print("📁 日志文件位置请查看控制台输出或logs目录\n")


def test_data_export():
    """测试数据导出功能"""
    print("=" * 50)
    print("测试2: 数据导出功能")
    print("=" * 50)
    
    data_manager = DataManager()
    exporter = DataExporter()
    
    # 获取所有用户
    users = data_manager.get_all_users()
    
    if not users:
        print("⚠️  暂无用户数据，跳过导出测试")
        return
    
    # 选择第一个有记录的用户
    test_user = None
    for user in users:
        if user.records:
            test_user = user
            break
    
    if not test_user:
        print("⚠️  暂无成绩记录，跳过导出测试")
        return
    
    print(f"使用用户: {test_user.name}")
    print(f"记录数量: {len(test_user.records)}")
    
    # 测试CSV导出
    csv_file = exporter.export_to_csv(test_user.records, test_user.name, output_dir=".")
    if csv_file:
        print(f"✅ CSV导出成功: {csv_file}")
    else:
        print("❌ CSV导出失败")
    
    # 测试Excel导出
    excel_file = exporter.export_to_excel(test_user.records, test_user.name, output_dir=".")
    if excel_file:
        print(f"✅ Excel导出成功: {excel_file}")
    else:
        print("⚠️  Excel导出失败（可能未安装openpyxl）")
    
    print()


def test_backup_manager():
    """测试备份管理功能"""
    print("=" * 50)
    print("测试3: 备份管理功能")
    print("=" * 50)
    
    backup_manager = BackupManager(DATA_FILE)
    
    # 1. 创建备份
    print("1. 创建测试备份...")
    backup_path = backup_manager.create_backup("test_backup")
    if backup_path:
        print(f"✅ 备份创建成功: {backup_path}")
    else:
        print("❌ 备份创建失败")
        return
    
    # 2. 列出备份
    print("\n2. 列出所有备份...")
    backups = backup_manager.list_backups()
    print(f"找到 {len(backups)} 个备份文件:")
    for i, backup in enumerate(backups[:5], 1):  # 只显示前5个
        print(f"   {i}. {backup['name']} - {backup['formatted_size']} - {backup['formatted_time']}")
    
    # 3. 验证备份
    print("\n3. 验证备份文件...")
    if backup_manager._verify_backup(backup_path):
        print("✅ 备份文件验证通过")
    else:
        print("❌ 备份文件验证失败")
    
    # 4. 清理测试备份
    print("\n4. 清理测试备份...")
    if backup_manager.delete_backup(backup_path):
        print("✅ 测试备份已清理")
    else:
        print("⚠️  测试备份清理失败")
    
    print()


def test_exception_handling():
    """测试异常处理"""
    print("=" * 50)
    print("测试4: 异常处理")
    print("=" * 50)
    
    data_manager = DataManager()
    
    # 测试正常操作
    print("1. 测试正常数据加载...")
    data_manager.load_data()
    print(f"✅ 加载了 {len(data_manager.users)} 个用户")
    
    # 测试添加重复用户（会触发warning日志）
    print("\n2. 测试重复用户检测...")
    if data_manager.users:
        duplicate_user = data_manager.users[0]
        result = data_manager.add_user(duplicate_user)
        if not result:
            print("✅ 正确识别重复用户")
        else:
            print("⚠️  未能识别重复用户")
    
    print()


def main():
    """主测试函数"""
    print("\n" + "=" * 50)
    print("体育成绩评估系统 - 优化功能测试")
    print("=" * 50 + "\n")
    
    try:
        # 运行各项测试
        test_logger()
        test_data_export()
        test_backup_manager()
        test_exception_handling()
        
        print("=" * 50)
        print("✅ 所有测试完成！")
        print("=" * 50)
        
        print("\n💡 提示:")
        print("1. 查看日志文件: logs/ 目录")
        print("2. 查看导出文件: 当前目录的 .csv 和 .xlsx 文件")
        print("3. 查看备份文件: data/backups/ 目录")
        print("4. 运行主程序: python3 main.py\n")
        
    except Exception as e:
        logger.exception("测试过程中发生错误")
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

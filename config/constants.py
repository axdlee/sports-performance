# -*- coding: utf-8 -*-
"""
常量配置文件
"""

# 导入路径辅助工具
import sys
import os

# 性别常量
GENDER_MALE = "male"
GENDER_FEMALE = "female"

# 项目类型
PROJECT_TYPE_REQUIRED = "required"  # 必选项
PROJECT_TYPE_CATEGORY1 = "category1"  # 第一类选考
PROJECT_TYPE_CATEGORY2 = "category2"  # 第二类选考

# 项目名称映射
PROJECT_NAMES = {
    # 必选项
    "1000m": "1000米跑",
    "800m": "800米跑",
    
    # 第一类选考
    "50m": "50米跑",
    "sit_reach": "坐位体前屈",
    "standing_jump": "立定跳远",
    "pull_ups": "引体向上",
    "sit_ups": "仰卧起坐",
    
    # 第二类选考
    "basketball": "篮球运球",
    "football": "足球运球",
    "volleyball": "排球垫球"
}

# 成绩等级评定标准
GRADE_STANDARDS = {
    "excellent": {"min": 27.0, "max": 30.0, "name": "优秀"},
    "good": {"min": 24.0, "max": 26.5, "name": "良好"},
    "medium": {"min": 18.0, "max": 23.5, "name": "中等"},
    "pass": {"min": 15.0, "max": 17.5, "name": "及格"},
    "fail": {"min": 0.0, "max": 14.5, "name": "不及格"}
}

# 文件路径
# 动态获取数据文件路径，以支持打包后的应用
def _get_data_file_path():
    """获取数据文件路径（支持打包环境）"""
    # 延迟导入以避免循环依赖
    try:
        from utils.path_helper import get_data_file_path
        return get_data_file_path("users.json")
    except ImportError:
        # 开发环境回退方案
        return "data/users.json"

DATA_FILE = _get_data_file_path()

# UI配置
WINDOW_TITLE = "体育成绩评估系统"
WINDOW_SIZE = "800x600"
WINDOW_MIN_SIZE = (600, 400)

# 报告窗口UI配置
REPORT_WINDOW_SIZE = "1100x800"

# 颜色主题配置
THEME_COLORS = {
    "primary": "#16a085",        # 青绿色主题
    "bg": "#ecf0f1",             # 背景色
    "card": "#ffffff",           # 卡片背景
    "success": "#2ecc71",        # 成功/优秀
    "warning": "#f39c12",        # 警告/中等
    "danger": "#e74c3c",         # 危险/不及格
    "info": "#3498db",           # 信息
    "text_dark": "#2c3e50",      # 深色文字
    "text_light": "#7f8c8d",     # 浅色文字
    "strong_bg": "#d5f4e6",      # 最强项背景
    "weak_bg": "#fadbd8",        # 最弱项背景
    "medium_bg": "#fff3cd",      # 中等背景
    "stats_bg": "#f8f9fa"        # 统计背景
}

# 字体配置
FONTS = {
    "title": ("Microsoft YaHei", 20, "bold"),
    "subtitle": ("Arial", 10),
    "card_title": ("Microsoft YaHei", 12, "bold"),
    "section_title": ("Microsoft YaHei", 11, "bold"),
    "text_normal": ("Microsoft YaHei", 11),
    "text_small": ("Microsoft YaHei", 10),
    "text_tiny": ("Microsoft YaHei", 9),
    "score_large": ("Arial", 32, "bold"),
    "score_medium": ("Microsoft YaHei", 24, "bold"),
    "score_small": ("Microsoft YaHei", 16, "bold"),
    "score_detail": ("Microsoft YaHei", 14, "bold")
}

# 图表配置
CHART_CONFIG = {
    "figure_size": (9, 4),
    "dpi": 100,
    "export_dpi": 150,
    "export_figure_size": (12, 6),
    "line_width_main": 2.5,
    "line_width_sub": 1.5,
    "marker_size_main": 8,
    "marker_size_sub": 6,
    "colors": {
        "total": "#16a085",
        "required": "#3498db",
        "category1": "#2ecc71",
        "category2": "#f39c12"
    },
    "markers": {
        "total": "o",
        "required": "s",
        "category1": "^",
        "category2": "d"
    }
}

# 成绩评价文本
SCORE_EVALUATION_TEXTS = {
    "excellent": {  # 27分以上
        "text": "🎉 恭喜！您的体育成绩非常优秀！您已经达到了很高的运动水平，各项指标都很出色。建议继续保持当前的训练强度，并可以尝试挑战更高的目标。保持良好的运动习惯，注意预防运动损伤，您可以成为同学们的榜样！",
        "threshold": 27.0
    },
    "good": {  # 24-27分
        "text": "👍 您的体育成绩良好！整体表现不错，但还有进步的空间。通过针对性训练，您完全有能力达到优秀水平。建议重点提升得分较低的项目，同时保持强项的训练。坚持科学训练，相信您很快就能突破到更高层次！",
        "threshold": 24.0
    },
    "medium": {  # 18-24分
        "text": "📈 您的体育成绩处于中等水平。这说明您具备基本的运动能力，但需要加强系统训练。建议制定详细的训练计划，每周至少进行3-4次针对性练习。提高成绩的关键在于持之以恒，注意训练的科学性和规律性。加油，您一定能够取得明显进步！",
        "threshold": 18.0
    },
    "pass": {  # 15-18分
        "text": "⚠️ 您的体育成绩刚达到及格线，需要重点加强训练。建议从最弱的项目入手，制定循序渐进的训练计划。不要急于求成，先打好基础，逐步提高。可以寻求体育老师或教练的指导，采用更科学的训练方法。相信通过努力，您的成绩会有显著提升！",
        "threshold": 15.0
    },
    "fail": {  # 15分以下
        "text": "🚨 您的体育成绩目前不及格，需要系统性的改进和提升。建议立即开始规律的体育锻炼，从基础训练做起。可以先设定小目标，比如每周进步一点点。强烈建议咨询专业教练，制定个性化的训练方案。记住，万事开头难，只要开始行动并坚持下去，一定会看到成效！",
        "threshold": 0.0
    }
}

# 弱项针对性建议 - 各得分段的训练强度描述
WEAKNESS_INTENSITY_TEXTS = {
    "very_low": {  # <3分
        "text": "您在该项目上的得分很低，需要从基础开始系统训练。",
        "frequency": "建议每周训练4-5次，每次30-40分钟。"
    },
    "low": {  # 3-5分
        "text": "您在该项目上还有较大提升空间，需要加强专项训练。",
        "frequency": "建议每周训练3-4次，每次25-35分钟。"
    },
    "medium": {  # 5-7分
        "text": "您在该项目上已有一定基础，需要针对性提高。",
        "frequency": "建议每周训练2-3次，每次20-30分钟。"
    },
    "high": {  # >7分
        "text": "您在该项目上表现尚可，可以进一步优化。",
        "frequency": "建议每周训练2次，每次15-25分钟。"
    }
}

# 项目改进建议（统一版本）
PROJECT_IMPROVEMENT_SUGGESTIONS = {
    "required": {
        "male": "加强长跑训练，每周进行3-4次有氧运动，包括慢跑、间歇跑等，逐步提高心肺功能和耐力。",
        "female": "加强长跑训练，每周进行3-4次有氧运动，包括慢跑、间歇跑等，逐步提高心肺功能和耐力。"
    },
    "1000m": {
        "male": "加强长跑训练，每周进行3-4次有氧运动，包括慢跑、间歇跑等，逐步提高心肺功能和耐力。",
        "female": "加强长跑训练，每周进行3-4次有氧运动，包括慢跑、间歇跑等，逐步提高心肺功能和耐力。"
    },
    "800m": {
        "male": "加强长跑训练，每周进行3-4次有氧运动，包括慢跑、间歇跑等，逐步提高心肺功能和耐力。",
        "female": "加强长跑训练，每周进行3-4次有氧运动，包括慢跑、间歇跑等，逐步提高心肺功能和耐力。"
    },
    "50m": {
        "male": "加强短跑训练，重点练习起跑、加速跑和冲刺技术，同时进行腿部力量训练。",
        "female": "加强短跑训练，重点练习起跑、加速跑和冲刺技术，同时进行腿部力量训练。"
    },
    "sit_reach": {
        "male": "加强柔韧性训练，每天进行拉伸练习，重点练习腰部、背部和腿部柔韧性。",
        "female": "加强柔韧性训练，每天进行拉伸练习，重点练习腰部、背部和腿部柔韧性。"
    },
    "standing_jump": {
        "male": "加强下肢爆发力训练，包括深蹲、蛙跳、立定跳远等练习，提高腿部肌肉力量。",
        "female": "加强下肢爆发力训练，包括深蹲、蛙跳、立定跳远等练习，提高腿部肌肉力量。"
    },
    "pull_ups": {
        "male": "加强上肢力量训练，包括引体向上、俯卧撑、哑铃练习等，提高背部、手臂和肩部力量。",
        "female": "加强上肢力量训练，包括引体向上、俯卧撑、哑铃练习等，提高背部、手臂和肩部力量。"
    },
    "sit_ups": {
        "male": "加强核心力量训练，包括仰卧起坐、平板支撑、卷腹等练习，提高腹部肌肉力量。",
        "female": "加强核心力量训练，包括仰卧起坐、平板支撑、卷腹等练习，提高腹部肌肉力量。"
    },
    "basketball": {
        "male": "加强篮球运球技术练习，包括原地运球、行进间运球、变向运球等，提高球感和协调性。",
        "female": "加强篮球运球技术练习，包括原地运球、行进间运球、变向运球等，提高球感和协调性。"
    },
    "football": {
        "male": "加强足球运球技术练习，包括脚内侧运球、脚外侧运球、变向运球等，提高球感和协调性。",
        "female": "加强足球运球技术练习，包括脚内侧运球、脚外侧运球、变向运球等，提高球感和协调性。"
    },
    "volleyball": {
        "male": "加强排球垫球技术练习，包括原地垫球、移动垫球、对墙垫球等，提高球感和协调性。",
        "female": "加强排球垫球技术练习，包括原地垫球、移动垫球、对墙垫球等，提高球感和协调性。"
    }
}

# 详细训练计划
DETAILED_TRAINING_PLANS = {
    "1000m": "训练计划:\n• 第1-2周: 慢跑800米 x 3组,间歇3分钟\n• 第3-4周: 慢跑1000米 x 2组,间歇5分钟\n• 第5-6周: 节奏跑1000米 x 2组,提升配速\n• 第7-8周: 全力跑1000米,争取突破",
    "800m": "训练计划:\n• 第1-2周: 慢跑600米 x 3组,间歇3分钟\n• 第3-4周: 慢跑800米 x 2组,间歇4分钟\n• 第5-6周: 节奏跑800米 x 2组,提升配速\n• 第7-8周: 全力跑800米,争取突破",
    "50m": "训练计划:\n• 起跑练习: 蹲踞式起跑30次/天\n• 加速跑: 30米冲刺 x 10组\n• 高抬腿: 30米 x 5组\n• 后蹬跑: 30米 x 5组\n• 腿部力量: 深蹲、跳跃训练",
    "sit_reach": "训练计划:\n• 坐位体前屈静态拉伸: 3组 x 30秒\n• 站立体前屈: 3组 x 15次\n• 腿部后侧拉伸: 每腿3组 x 20秒\n• 腰部拉伸: 瑜伽猫式等动作\n• 每天拉伸,循序渐进增加幅度",
    "standing_jump": "训练计划:\n• 深蹲跳: 4组 x 15次\n• 蛙跳: 20米 x 4组\n• 单腿跳: 每腿3组 x 10次\n• 台阶跳: 4组 x 20次\n• 摆臂练习配合腿部发力",
    "pull_ups": "训练计划:\n• 辅助引体(弹力带): 3组 x 8次\n• 反向划船: 4组 x 12次\n• 悬吊静止: 3组 x 最大时间\n• 背阔肌下拉: 4组 x 10次\n• 逐步减少辅助,增加次数",
    "sit_ups": "训练计划:\n• 标准仰卧起坐: 4组 x 80%最大次数\n• 卷腹: 4组 x 20次\n• 平板支撑: 3组 x 60秒\n• 俄罗斯转体: 4组 x 30次\n• 每周增加5-10次目标",
    "basketball": "训练计划:\n• 原地运球: 左右手各5分钟\n• 行进间运球: 往返10次\n• 变向运球: Z字形 x 10次\n• 双球运球: 5分钟提高协调\n• 障碍物运球: 提高控球能力",
    "football": "训练计划:\n• 脚内侧运球: 往返10次\n• 脚外侧运球: 往返10次\n• 变向运球: 8字形 x 10次\n• 障碍物绕桩: 连续练习\n• 提高触球频率和灵活性",
    "volleyball": "训练计划:\n• 对墙垫球: 连续100次 x 3组\n• 自垫球: 连续50次 x 3组\n• 移动垫球: 前后左右各方向\n• 双人对垫: 提高稳定性\n• 注意手型和击球部位"
}

# 生活与训练建议文本
LIFE_SUGGESTIONS_TEXT = """💪 训练建议:
• 制定合理的训练计划,循序渐进,避免过度训练
• 训练前充分热身(10-15分钟),激活肌肉,预防损伤
• 训练后做好拉伸放松(10-15分钟),促进恢复
• 记录训练日志,跟踪进步情况,及时调整方案
• 每周至少休息1-2天,让身体充分恢复

🍎 饮食建议:
• 保证充足的蛋白质摄入(鸡蛋、牛奶、瘦肉、豆类)
• 多吃新鲜蔬菜水果,补充维生素和矿物质
• 训练前1-2小时进食,避免空腹或过饱运动
• 训练后及时补充水分和能量(香蕉、运动饮料)
• 减少油炸食品和高糖食物,控制体重

😴 作息建议:
• 保证每天7-9小时的充足睡眠
• 尽量在晚上11点前入睡,确保深度睡眠
• 午休20-30分钟可以提高下午训练效果
• 避免熬夜和长时间使用电子设备
• 规律作息有助于提高运动表现

🎯 心理建议:
• 设定合理的短期和长期目标,保持动力
• 不要和别人比较,专注于自己的进步
• 遇到困难时保持积极心态,寻求帮助
• 庆祝每一个小进步,建立自信心
• 把运动当作生活习惯而非任务

⚠️ 安全提示:
• 身体不适时及时停止训练,不要勉强
• 使用正确的动作技术,避免受伤
• 注意训练场地安全,穿着合适的运动装备
• 如有慢性疾病,训练前咨询医生
• 运动损伤后要充分休息和治疗"""

# 成绩优先级配置
SCORE_PRIORITY = {
    "high": {"threshold": 5.0, "label": "🔴 高优先级", "bg_color": "#fadbd8"},
    "medium": {"threshold": 7.0, "label": "🟡 中优先级", "bg_color": "#fff3cd"},
    "low": {"threshold": 10.0, "label": "🟢 低优先级", "bg_color": "#d5f4e6"}
}

# 成绩状态标签配置
SCORE_STATUS = {
    "excellent": {"threshold": 9.0, "label": "优秀", "color": "#2ecc71"},
    "good": {"threshold": 7.0, "label": "良好", "color": "#3498db"},
    "medium": {"threshold": 5.0, "label": "中等", "color": "#f39c12"},
    "needs_improvement": {"threshold": 0.0, "label": "需改进", "color": "#e74c3c"}
}

# ========== UI组件配置 ==========

# CustomButton 默认配置
CUSTOM_BUTTON_CONFIG = {
    "default_bg": "#3498db",           # 默认背景色
    "default_fg": "white",             # 默认前景色
    "default_font": ("Microsoft YaHei", 11, "bold"),  # 默认字体
    "default_width": 20,               # 默认宽度（字符数）
    "default_height": 2,               # 默认高度（行数）
    "disabled_bg": "#bdc3c7",          # 禁用状态背景色
    "disabled_fg": "#7f8c8d",          # 禁用状态前景色
    "hover_darken_factor": 0.8,        # 悬停时变暗系数
    "press_darken_factor": 0.8,        # 按下时变暗系数
    "cursor": "hand2"                  # 光标样式
}

# 窗口尺寸配置
WINDOW_SIZES = {
    "main": "500x550",         # 主窗口
    "login": "600x700",        # 登录窗口
    "input": "750x700",        # 成绩录入窗口
    "report": "1100x800"       # 成绩报告窗口
}

# ========== 公共UI配置（所有窗口共享） ==========
COMMON_UI_CONFIG = {
    # 基础颜色
    "bg_color": "#ecf0f1",              # 窗口背景色
    "title_bg": "#16a085",              # 标题背景色
    "title_fg": "white",                # 标题前景色
    "frame_bg": "#ffffff",              # 框架背景色
    "frame_fg": "#2c3e50",              # 框架前景色
    
    # 标准字体
    "title_font": ("Microsoft YaHei", 22, "bold"),
    "subtitle_font": ("Arial", 9),
    "section_font": ("Microsoft YaHei", 12, "bold"),
    "label_font_bold": ("Microsoft YaHei", 11, "bold"),
    "label_font_normal": ("Microsoft YaHei", 11),
    "label_font_small": ("Microsoft YaHei", 10),
    "label_font_tiny": ("Microsoft YaHei", 9),
    "entry_font": ("Microsoft YaHei", 11),
    "button_font": ("Microsoft YaHei", 12, "bold"),
    "status_font": ("Microsoft YaHei", 10),
    
    # 标准颜色
    "label_primary_color": "#16a085",   # 主标签颜色
    "label_secondary_color": "#34495e", # 次要标签颜色
    "label_hint_color": "#7f8c8d",      # 提示文字颜色
    "card_bg": "#f8f9fa",               # 卡片背景色
    "card_hover_bg": "#e8f4f8",         # 卡片悬停色
    "card_text_color": "#2c3e50",       # 卡片文字颜色
    
    # 按钮颜色
    "login_button_bg": "#3498db",
    "register_button_bg": "#2ecc71",
    "save_button_bg": "#2ecc71",
    "reset_button_bg": "#95a5a6",
    "exit_button_bg": "#95a5a6",
    "disabled_button_bg": "#bdc3c7"
}

# ========== 窗口专属配置（仅包含差异化配置） ==========

# InputWindow 专属配置
INPUT_WINDOW_CONFIG = {
    **COMMON_UI_CONFIG,  # 继承公共配置
    # 覆盖/新增专属配置
    "entry_font": ("Arial", 12),        # 数字输入框使用Arial字体
    "score_font": ("Microsoft YaHei", 18, "bold"),
    "required_color": "#c0392b",        # 必选项颜色
    "category1_color": "#2980b9",       # 第一类选考颜色
    "category2_color": "#e67e22",       # 第二类选考颜色
    "label_hint_color": "#95a5a6",      # 输入窗口的提示色稍浅
    "score_display_color": "#3498db",   # 得分显示颜色
    "score_total_color": "#e74c3c",     # 总分显示颜色
}

# LoginWindow 专属配置
LOGIN_WINDOW_CONFIG = {
    **COMMON_UI_CONFIG,  # 继承公共配置
    # 覆盖/新增专属配置
    "male_color": "#3498db",            # 男生颜色
    "female_color": "#e74c3c",          # 女生颜色
    "card_bg": "#f8f9fa",               # 用户卡片背景色
    "card_hover_bg": "#e8f4f8",         # 用户卡片悬停背景色
    "card_text_color": "#2c3e50",       # 卡片文字颜色
    "card_hint_color": "#7f8c8d",       # 卡片提示文字颜色
}

# MainWindow 专属配置
MAIN_WINDOW_CONFIG = {
    **COMMON_UI_CONFIG,  # 继承公共配置
    # 覆盖/新增专属配置
    "label_font_normal": ("Microsoft YaHei", 12),  # 主窗口标签字体稍大
    "user_info_text_color": "#34495e",
    "switch_user_button_bg": "#9b59b6",  # 切换用户按钮颜色
    "input_button_bg": "#2ecc71",
    "report_button_bg": "#e67e22",
}

# 通用UI文本
UI_TEXTS = {
    "welcome": "💡 欢迎使用体育成绩评估系统",
    "not_logged_in": "未登录",
    "please_login": "请先登录",
    "no_records": "暂无成绩记录，请先录入成绩",
    "no_users": "暂无用户，请注册新用户",
    "save_success": "✅ 成绩已保存！",
    "save_failed": "保存失败",
    "login_success": "✅ 欢迎，{}！",
    "auto_login": "✅ 自动登录: {}",
    "selected_user": "✅ 已选择用户: {}",
    "welcome_back": "欢迎回来，{}！",
    "register_success": "注册成功，欢迎 {}！",
    "user_info_format": "✅ {} ({}) - 记录: {}条",
    "confirm_exit": "确认退出",
    "exit_message": "确定要退出程序吗？",
    "input_error": "输入错误",
    "save_error": "保存失败",
    "login_failed": "登录失败",
    "register_failed": "注册失败",
    "register_error": "用户注册失败，请重试",
    "user_exists": "用户 '{}' 已存在",
    "user_not_found": "用户不存在",
    "gender_mismatch": "性别信息不匹配",
    "register_prompt": "用户 '{}' 不存在，是否注册新用户？",
    "view_report_prompt": "成绩已保存！总分: {:.1f}\n\n是否查看成绩报告？"
}

# 输入提示文本
INPUT_HINTS = {
    "spinbox_hint": "💡 使用上下箭头或直接输入数字",
    "required_time": "请输入必选项成绩",
    "seconds_range": "秒钟数必须小于60",
    "category1_required": "请选择第一类选考项目",
    "category1_score": "请输入第一类选考成绩",
    "category2_required": "请选择第二类选考项目",
    "category2_score": "请输入第二类选考成绩",
    # 保留旧的key作为兼容
    "select_category1": "请选择第一类选考项目",
    "input_category1": "请输入第一类选考成绩",
    "select_category2": "请选择第二类选考项目",
    "input_category2": "请输入第二类选考成绩"
}

# 项目标签配置
PROJECT_LABELS = {
    # 完整标签（带单位）
    "50m": "50米跑 (秒)",
    "sit_reach": "坐位体前屈 (厘米)",
    "standing_jump": "立定跳远 (厘米)",
    "pull_ups": "引体向上 (次)",
    "sit_ups": "仰卧起坐 (次)",
    "basketball": "篮球运球 (秒)",
    "football": "足球运球 (秒)",
    "volleyball": "排球垫球 (次)",
    "1000m": "1000米跑 (秒)",
    "800m": "800米跑 (秒)",
    # 短标签（不带单位，用于下拉框）
    "50m_short": "50米跑",
    "sit_reach_short": "坐位体前屈",
    "standing_jump_short": "立定跳远",
    "pull_ups_short": "引体向上",
    "sit_ups_short": "仰卧起坐",
    "basketball_short": "篮球运球",
    "football_short": "足球运球",
    "volleyball_short": "排球垫球",
    "1000m_short": "1000米跑",
    "800m_short": "800米跑"
}

# 性别图标和文本
GENDER_CONFIG = {
    "male": {
        "icon": "👨",
        "text": "男",
        "color": "#3498db"
    },
    "female": {
        "icon": "👩",
        "text": "女",
        "color": "#e74c3c"
    }
}

# 窗口标题配置
WINDOW_TITLES = {
    "main": "体育成绩评估系统",
    "login": "用户登录 - 体育成绩评估系统",
    "input": "成绩录入 - {}",
    "report": "📊 成绩报告 - {}"
}

# 按钮文本配置
BUTTON_TEXTS = {
    "login": "🔑 登录",
    "switch_user": "🔄 切换用户",
    "register": "📝 注册新用户",
    "user_login": "🔑 用户登录",
    "input_score": "📝 成绩录入",
    "view_report": "📊 成绩报告",
    "exit": "❌ 退出程序",
    "exit_app": "❌ 退出程序",  # 别名
    "save": "💾 保存成绩",
    "reset": "🔄 重置",
    "refresh_chart": "🔄 刷新图表",
    "export_chart": "💾 导出图表"
}

# LabelFrame标题配置
LABEL_FRAME_TITLES = {
    "required": " 🏃 必选项 (10分) ",
    "category1": " 💪 第一类选考 (10分) ",
    "category2": " ⚽ 第二类选考 (10分) ",
    "total_score": " 📊 总分计算 ",
    "user_info": " 👤 用户信息 ",
    "current_user": " 👤 当前用户 ",
    "existing_users": " 📋 已有用户 (点击选择) "
}

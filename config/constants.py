# -*- coding: utf-8 -*-
"""
常量配置文件
"""

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
DATA_FILE = "data/users.json"

# UI配置
WINDOW_TITLE = "体育成绩评估系统"
WINDOW_SIZE = "800x600"
WINDOW_MIN_SIZE = (600, 400)

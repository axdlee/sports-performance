# 🏃‍♂️ 体育成绩评估系统

## 📋 项目简介

体育成绩评估系统是一款专为中学/高校设计的现代化桌面端体育成绩管理软件，支持macOS和Windows平台。系统基于《国家学生体质健康标准》开发，提供完整的成绩录入、自动计算、分析报告和趋势分析功能。

## ✨ 主要功能

### 🎯 核心功能
- **用户管理**: 多用户注册登录，简化流程（只需姓名+性别）
- **成绩录入**: 支持必选项和两类选考项目
- **自动评分**: 基于国家标准的精确计算
- **数据分析**: 等级评定、弱项识别、改进建议
- **历史记录**: 成绩趋势分析和图表生成
- **数据管理**: 本地JSON存储，支持多用户

### 🏃‍♂️ 测试项目
- **必选项**（10分）: 男生1000米跑 / 女生800米跑
- **第一类选考**（10分）: 50米跑、坐位体前屈、立定跳远、引体向上（男）/仰卧起坐（女）
- **第二类选考**（10分）: 篮球运球、足球运球、排球垫球

### 📊 评分标准
- **优秀**: 27-30分
- **良好**: 24-26.5分  
- **中等**: 18-23.5分
- **及格**: 15-17.5分
- **不及格**: 0-14.5分

## 🚀 安装与运行

### 方法一：使用安装包（推荐）

#### 获取预编译安装包
直接从 [Releases](../../releases) 下载对应平台的安装包：
- **macOS**: `体育成绩评估系统-v1.0.0-macOS.dmg` 或 `.app` 文件
- **Windows**: `体育成绩评估系统-v1.0.0-Windows-Setup.exe` 或压缩包

#### 自己构建安装包
```bash
# 确保在虚拟环境中
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 运行打包脚本（自动检测平台）
python build.py
```

生成的安装包位于 `dist/installer_macos/` 或 `dist/installer_windows/`

详细打包说明请参考 [BUILD_GUIDE.md](BUILD_GUIDE.md)

#### 安装说明

**macOS**:
1. 打开 DMG 文件或解压安装包
2. 将 "体育成绩评估系统.app" 拖拽到"应用程序"文件夹
3. 双击运行（首次运行可能需要右键 → 打开）

**Windows**:
1. 运行安装程序或解压压缩包
2. 双击 "体育成绩评估系统.exe" 运行
3. 如遇 Windows Defender 拦截，点击"更多信息" → "仍要运行"

### 方法二：从源码运行（开发者）

#### 快速开始
```bash
# 克隆项目
git clone <repository-url>
cd sports-performance

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py
```

#### 或直接运行（需已安装依赖）
```bash
python main.py
```

## 🎨 界面特色

- **现代化设计**: 采用专业配色方案和图标
- **用户友好**: 直观的操作流程和实时反馈
- **响应式布局**: 适配不同屏幕尺寸
- **多语言支持**: 中英文界面

## 📁 项目结构

```
sports-performance/
├── main.py                    # 程序入口
├── build.py                   # 安装包生成脚本
├── requirements.txt           # 依赖包列表
├── config/                    # 配置文件
│   ├── constants.py          # 常量定义
│   └── scoring_standards.py  # 评分标准
├── models/                    # 数据模型
├── services/                  # 业务逻辑
├── ui/                        # 用户界面
├── utils/                     # 工具类
│   └── path_helper.py        # 路径处理（支持打包）
└── data/                      # 开发环境数据（打包后使用系统目录）
```

## 💾 数据存储

打包后的应用将数据存储在系统标准位置：
- **macOS**: `~/Library/Application Support/SportsPerformance/`
- **Windows**: `%APPDATA%\SportsPerformance\`

详细说明请参考 [DATA_STORAGE.md](DATA_STORAGE.md)

## 🔧 技术栈

- **开发语言**: Python 3.7+
- **GUI框架**: Tkinter
- **图表库**: Matplotlib
- **图像处理**: Pillow
- **打包工具**: PyInstaller
- **数据格式**: JSON

## 📋 系统要求

### 使用安装包（推荐）
- **macOS**: 10.13 或更高版本
- **Windows**: Windows 10 (1809) 或更高版本
- **内存**: 至少 512MB RAM
- **存储**: 至少 100MB 可用空间
- **无需安装 Python 环境**

### 从源码运行（开发者）
- **Python**: 3.7+ (推荐 3.8-3.11)
- **操作系统**: macOS 10.13+ / Windows 10+
- **内存**: 至少 512MB RAM
- **存储**: 至少 100MB 可用空间

## 📦 打包构建

### 快速打包
```bash
# 在虚拟环境中运行
python build.py
```

### 详细说明
参见 [BUILD_GUIDE.md](BUILD_GUIDE.md) 获取完整的打包说明，包括：
- 跨平台打包配置
- DMG/安装程序创建
- 代码签名指南
- 常见问题解决
- CI/CD 集成示例

## 🎯 使用流程

1. **首次使用**: 输入姓名和性别注册账户
2. **成绩录入**: 选择测试项目并输入成绩
3. **查看报告**: 分析成绩等级和改进建议
4. **历史记录**: 查看成绩趋势和生成图表

## 📞 技术支持

如遇问题，请检查：
- 系统版本是否满足要求
- 依赖包是否正确安装
- 数据文件是否完整
- 系统权限设置

## 📝 更新日志

### v1.3.1 (2025-10-18)
- 🐛 修复打包后数据目录只读问题
  - 数据现在存储在系统用户目录
  - macOS: `~/Library/Application Support/SportsPerformance/`
  - Windows: `%APPDATA%\SportsPerformance\`
- ✅ 新增 `utils/path_helper.py` 路径处理模块
- ✅ 新增 `DATA_STORAGE.md` 数据存储说明文档
- ✅ 改进跨平台数据持久化

### v1.3.0 (2025-10-18)
- ✅ 完善跨平台打包机制
  - 统一的 `sports_performance.spec` 配置文件
  - 自动化的 `build.py` 打包脚本
  - 支持 macOS .app bundle 和 DMG 创建
  - 支持 Windows exe 和 Inno Setup 安装程序
- ✅ 新增详细的打包文档 `BUILD_GUIDE.md`
- ✅ 优化构建流程和错误处理
- ✅ 改进安装包结构和分发说明

### v1.2.0 (2025-10-18)
- ✅ 优化登录界面，移除学号字段
- ✅ 改进UI设计，采用现代化配色方案
- ✅ 修复登录跳转问题
- ✅ 优化安装包生成，支持真正的应用程序

### v1.1.0 (2025-10-18)
- ✅ 实现完整的成绩管理功能
- ✅ 支持历史记录和趋势分析
- ✅ 添加弱项识别和改进建议

### v1.0.0 (2025-10-18)
- ✅ 初始版本发布
- ✅ 基础功能实现

## 📄 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📚 相关文档

- [BUILD_GUIDE.md](BUILD_GUIDE.md) - 完整的打包构建指南
- [使用说明.md](使用说明.md) - 用户使用手册
- [项目完成报告.md](项目完成报告.md) - 项目开发总结

---

**开发者**: Sports Performance Assessment Team  
**版本**: 1.3.0  
**最后更新**: 2025-10-18

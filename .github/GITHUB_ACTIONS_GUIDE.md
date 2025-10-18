# GitHub Actions 自动构建指南

本项目已配置 GitHub Actions 自动化构建系统，可以在云端自动构建 Windows 和 macOS 安装包。

## 📋 前置准备

### 1. 创建 GitHub 仓库

如果还没有 GitHub 仓库，请先创建：

```bash
# 在 GitHub 网站上创建新仓库，然后关联本地仓库
git remote add origin https://github.com/axdlee/sports-performance.git
git branch -M main
git push -u origin main
```

### 2. 推送代码

确保所有文件都已提交并推送：

```bash
git add .
git commit -m "feat: 添加 GitHub Actions 自动构建配置"
git push origin main
```

## 🚀 触发构建的方式

### 方式 1: 手动触发（推荐用于测试）

1. 访问你的 GitHub 仓库
2. 点击 **Actions** 标签
3. 选择以下工作流之一：
   - `Build Windows Installer` - 仅构建 Windows
   - `Build All Platforms` - 构建 Windows 和 macOS
4. 点击右侧 **Run workflow** 按钮
5. （可选）输入版本号，如 `1.3.1`
6. 点击绿色的 **Run workflow** 按钮开始构建

### 方式 2: 推送标签（推荐用于发布）

创建并推送版本标签会自动触发构建并创建 Release：

```bash
# 创建版本标签
git tag -a v1.3.1 -m "Release version 1.3.1"

# 推送标签到 GitHub
git push origin v1.3.1
```

这将：
- ✅ 自动构建 Windows 和 macOS 安装包
- ✅ 创建 GitHub Release
- ✅ 自动上传安装包到 Release 页面

## 📦 下载构建产物

### 从 Actions 页面下载（手动触发时）

1. 访问仓库的 **Actions** 标签
2. 点击对应的工作流运行记录
3. 向下滚动到 **Artifacts** 部分
4. 下载：
   - `windows-installer` - Windows 安装包 ZIP
   - `macos-installer` - macOS 安装包 ZIP（如果是 All Platforms 工作流）

### 从 Releases 页面下载（标签触发时）

1. 访问仓库的 **Releases** 页面
2. 找到对应版本
3. 下载 Assets 中的安装包：
   - `体育成绩评估系统-v1.3.1-Windows.zip`
   - `体育成绩评估系统-v1.3.1-macOS.zip`

## 📝 工作流说明

### Build Windows Installer

**文件**: `.github/workflows/build-windows.yml`

**功能**:
- 仅在 Windows 虚拟机上构建
- 生成 Windows exe 和安装包
- 创建 ZIP 压缩包
- 上传构建产物

**触发条件**:
- 推送 `v*` 标签（如 `v1.3.1`）
- 手动触发（可指定版本号）

**构建时间**: 约 5-10 分钟

### Build All Platforms

**文件**: `.github/workflows/build-all-platforms.yml`

**功能**:
- 并行构建 Windows 和 macOS
- 生成两个平台的安装包
- 如果是标签触发，自动创建 Release
- 上传所有安装包到 Release

**触发条件**:
- 推送 `v*` 标签（如 `v1.3.1`）
- 手动触发（可指定版本号）

**构建时间**: 约 10-15 分钟

## 🔧 自定义配置

### 修改 Python 版本

编辑工作流文件中的 Python 版本：

```yaml
- name: 设置 Python 环境
  uses: actions/setup-python@v5
  with:
    python-version: '3.10'  # 改为你需要的版本，如 '3.11'
```

### 修改触发条件

如果想在每次推送到 main 分支时都构建：

```yaml
on:
  push:
    branches:
      - main
  # ... 其他触发条件
```

### 修改构建产物保留时间

默认保留 30 天，可以修改：

```yaml
- name: 上传构建产物
  uses: actions/upload-artifact@v4
  with:
    # ...
    retention-days: 90  # 改为 90 天
```

## 🐛 常见问题

### Q: Actions 页面看不到工作流

**A**: 确保：
1. `.github/workflows/` 目录已推送到 GitHub
2. YAML 文件语法正确（可用在线工具验证）
3. 刷新页面

### Q: 构建失败

**A**: 查看构建日志：
1. 点击失败的工作流运行
2. 展开失败的步骤查看详细错误
3. 常见原因：
   - 依赖安装失败：检查 `requirements.txt`
   - PyInstaller 错误：检查 `sports_performance.spec`
   - 权限问题：检查文件路径和权限

### Q: 无法下载构建产物

**A**: 注意：
- 必须登录 GitHub 才能下载 Artifacts
- Artifacts 会在保留期后自动删除
- Release 中的文件是永久的（推荐用于分发）

### Q: 想要构建 Linux 版本

**A**: 添加新的 job 到工作流：

```yaml
build-linux:
  name: Build Linux
  runs-on: ubuntu-latest
  steps:
    # 类似 macOS 的构建步骤
    # ...
```

## 📊 构建状态徽章

在 README.md 中添加构建状态徽章：

```markdown
![Build Windows](https://github.com/axdlee/sports-performance/workflows/Build%20Windows%20Installer/badge.svg)
![Build All](https://github.com/axdlee/sports-performance/workflows/Build%20All%20Platforms/badge.svg)
```

## 🔐 安全注意事项

1. **不要提交敏感信息**：
   - API 密钥
   - 密码
   - 证书文件

2. **使用 GitHub Secrets**：
   如需代码签名，将证书等敏感信息存储在 Repository Secrets

3. **检查构建日志**：
   确保日志中不包含敏感信息

## 📚 更多资源

- [GitHub Actions 官方文档](https://docs.github.com/cn/actions)
- [PyInstaller 文档](https://pyinstaller.org/)
- [软件打包最佳实践](https://packaging.python.org/)

## 🎯 快速开始示例

### 首次发布完整流程

```bash
# 1. 确保代码已提交
git add .
git commit -m "feat: 准备发布 v1.3.1"

# 2. 推送到 GitHub
git push origin main

# 3. 创建并推送标签
git tag -a v1.3.1 -m "Release version 1.3.1"
git push origin v1.3.1

# 4. 等待 10-15 分钟，然后访问 Releases 页面下载
# https://github.com/axdlee/sports-performance/releases
```

### 测试构建（不创建 Release）

1. 访问 GitHub Actions 页面
2. 选择 "Build Windows Installer"
3. 点击 "Run workflow"
4. 等待构建完成
5. 从 Artifacts 下载测试

---

**更新时间**: 2025-10  
**版本**: 1.0.0

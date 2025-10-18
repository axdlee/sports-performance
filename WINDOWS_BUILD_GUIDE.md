# Windows 安装包构建指南

## 🎯 概述

由于 PyInstaller 不支持跨平台打包，在 Mac 上无法直接构建 Windows exe。本项目已配置 **GitHub Actions 云端自动构建**，可以在 GitHub 的 Windows 虚拟机上自动生成 Windows 安装包。

## ✅ 优点

- ✨ 完全免费（GitHub Actions 对公共仓库免费）
- 🚀 自动化构建，无需本地 Windows 环境
- 📦 同时支持构建 Windows 和 macOS 安装包
- 🔄 可重复构建，版本管理方便
- 💾 自动创建 Release 和上传安装包

## 📋 快速开始（3 步完成）

### 第 1 步：创建 GitHub 仓库并推送代码

```bash
# 1. 在 GitHub 创建新仓库（例如：sports-performance）
# 访问 https://github.com/new

# 2. 关联远程仓库
git remote add origin https://github.com/你的用户名/sports-performance.git

# 3. 推送代码（已包含 GitHub Actions 配置）
git push -u origin main
```

### 第 2 步：创建版本标签触发构建

```bash
# 创建版本标签
git tag -a v1.3.1 -m "Release version 1.3.1"

# 推送标签到 GitHub
git push origin v1.3.1
```

### 第 3 步：下载构建好的安装包

等待 10-15 分钟后：

1. 访问你的仓库页面
2. 点击右侧的 **Releases** 链接
3. 找到刚创建的 `v1.3.1` 版本
4. 下载 **Assets** 中的 ZIP 文件：
   - `体育成绩评估系统-v1.3.1-Windows.zip` ✅
   - `体育成绩评估系统-v1.3.1-macOS.zip` ✅

完成！🎉

## 🔄 手动触发构建（不创建 Release）

如果只想测试构建，不想创建正式版本：

1. 访问仓库的 **Actions** 标签页
2. 左侧选择 `Build Windows Installer`
3. 点击右侧的 **Run workflow** 按钮
4. （可选）输入版本号
5. 点击绿色 **Run workflow** 开始构建
6. 等待 5-10 分钟
7. 在完成的工作流页面下载 **Artifacts** 中的 `windows-installer`

## 📦 工作流说明

项目包含 2 个自动化工作流：

### 1. Build Windows Installer
**文件**: `.github/workflows/build-windows.yml`  
**用途**: 仅构建 Windows 安装包  
**时长**: ~5-10 分钟  
**产物**: Windows ZIP 压缩包

### 2. Build All Platforms  
**文件**: `.github/workflows/build-all-platforms.yml`  
**用途**: 同时构建 Windows 和 macOS 安装包  
**时长**: ~10-15 分钟  
**产物**: Windows + macOS ZIP 压缩包，自动创建 Release

## 🎯 两种触发方式对比

| 触发方式 | 命令 | 创建 Release | 适用场景 |
|---------|------|-------------|---------|
| **推送标签** | `git push origin v1.3.1` | ✅ 是 | 正式发布版本 |
| **手动触发** | 在 Actions 页面点击 | ❌ 否 | 测试构建 |

## 📝 构建流程详解

GitHub Actions 会自动执行以下步骤：

1. ✅ 在 Windows Server 虚拟机上启动
2. ✅ 检出代码
3. ✅ 安装 Python 3.10
4. ✅ 安装依赖包（从 requirements.txt）
5. ✅ 运行 `python build.py` 构建 exe
6. ✅ 创建 ZIP 压缩包
7. ✅ 上传构建产物
8. ✅ （标签触发时）创建 Release 并上传

## 🐛 常见问题

### Q: 在哪里查看构建状态？

**A**: 访问仓库 → **Actions** 标签 → 点击对应的工作流运行记录

### Q: 构建失败怎么办？

**A**: 
1. 点击失败的工作流
2. 展开红色 ❌ 的步骤查看错误日志
3. 常见问题：
   - 依赖版本冲突：检查 `requirements.txt`
   - 文件路径错误：检查 `build.py` 和 `sports_performance.spec`
   - 图标文件缺失：确保 `assets/icon.ico` 存在

### Q: 可以在私有仓库使用吗？

**A**: 可以！但私有仓库的 GitHub Actions 有使用时长限制：
- 免费账户：2000 分钟/月
- Pro 账户：3000 分钟/月
- 本项目单次构建约消耗 10-15 分钟

### Q: 可以同时构建多个版本吗？

**A**: 可以！推送多个标签即可：
```bash
git tag v1.3.1 && git push origin v1.3.1
git tag v1.3.2 && git push origin v1.3.2
```

### Q: 如何修改构建的 Python 版本？

**A**: 编辑 `.github/workflows/*.yml` 文件：
```yaml
- name: 设置 Python 环境
  uses: actions/setup-python@v5
  with:
    python-version: '3.10'  # 改为 '3.11' 等
```

## 🔧 高级配置

### 添加构建状态徽章

在 `README.md` 中添加：

```markdown
![Windows Build](https://github.com/你的用户名/sports-performance/workflows/Build%20Windows%20Installer/badge.svg)
```

### 修改触发条件

如果想在每次推送到 main 分支时自动构建：

```yaml
on:
  push:
    branches:
      - main
  # ... 保留其他触发条件
```

### 启用构建缓存加速

工作流已启用 pip 缓存，首次构建后续会更快。

## 📚 相关文档

- **详细指南**: [.github/GITHUB_ACTIONS_GUIDE.md](.github/GITHUB_ACTIONS_GUIDE.md)
- **打包说明**: [BUILD_GUIDE.md](BUILD_GUIDE.md)
- **数据存储**: [DATA_STORAGE.md](DATA_STORAGE.md)

## 💡 其他方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **GitHub Actions** | 免费、自动化、可重复 | 需要 GitHub 仓库 | ⭐⭐⭐⭐⭐ |
| Docker + Wine | 本地构建 | 配置复杂、构建慢 | ⭐⭐ |
| Windows 虚拟机 | 完全本地控制 | 需购买 Parallels/VMware | ⭐⭐⭐ |
| 远程 Windows 机器 | 真实环境 | 需要额外硬件/云服务器 | ⭐⭐⭐ |

## 🛡️ 杀毒软件误报问题

PyInstaller 打包的程序经常被 Windows Defender 误报为病毒，这是正常现象。

**解决方法：**
1. 点击"更多信息" → "仍要运行"
2. 或将程序添加到 Windows Defender 排除列表

详细说明请查看：[ANTIVIRUS_NOTICE.md](ANTIVIRUS_NOTICE.md)

## 📞 技术支持

如有问题：
1. 查看 Actions 构建日志
2. 检查 `.github/workflows/*.yml` 配置
3. 参考 [GitHub Actions 文档](https://docs.github.com/cn/actions)
4. 杀毒软件误报请查看 [ANTIVIRUS_NOTICE.md](ANTIVIRUS_NOTICE.md)

---

**更新时间**: 2025-10  
**当前版本**: 1.3.1  
**推荐方式**: GitHub Actions 云端构建

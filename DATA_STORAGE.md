# 数据存储说明

## 📁 数据存储位置

为了支持应用打包后的正常运行，本系统将用户数据存储在系统的标准用户数据目录中，而不是应用程序包内部。

### macOS
```
~/Library/Application Support/SportsPerformance/
├── users.json          # 用户数据和成绩记录
├── last_user.json      # 上次登录用户
└── *.png              # 生成的图表文件
```

完整路径示例：
```
/Users/[用户名]/Library/Application Support/SportsPerformance/
```

### Windows
```
%APPDATA%\SportsPerformance\
├── users.json          # 用户数据和成绩记录
├── last_user.json      # 上次登录用户
└── *.png              # 生成的图表文件
```

完整路径示例：
```
C:\Users\[用户名]\AppData\Roaming\SportsPerformance\
```

### Linux（如果支持）
```
~/.local/share/SportsPerformance/
├── users.json          # 用户数据和成绩记录
├── last_user.json      # 上次登录用户
└── *.png              # 生成的图表文件
```

## 🔍 查找数据文件

### macOS
1. 打开 Finder
2. 按 `Command + Shift + G` 打开"前往文件夹"
3. 输入：`~/Library/Application Support/SportsPerformance`
4. 点击"前往"

或在终端执行：
```bash
open ~/Library/Application\ Support/SportsPerformance
```

### Windows
1. 打开文件资源管理器
2. 在地址栏输入：`%APPDATA%\SportsPerformance`
3. 按回车

或在命令提示符/PowerShell执行：
```cmd
explorer %APPDATA%\SportsPerformance
```

## 💾 数据备份

### 备份步骤
1. 找到数据目录（见上方说明）
2. 复制整个 `SportsPerformance` 文件夹
3. 保存到安全位置（如云盘、U盘等）

### 恢复数据
1. 关闭应用程序
2. 将备份的文件复制到数据目录
3. 重新启动应用程序

## 🗑️ 完全卸载

### macOS
1. 删除应用程序：将 `.app` 拖到废纸篓
2. 删除数据文件（可选）：
   ```bash
   rm -rf ~/Library/Application\ Support/SportsPerformance
   ```

### Windows
1. 删除应用程序文件夹
2. 删除数据文件（可选）：
   ```cmd
   rmdir /s %APPDATA%\SportsPerformance
   ```

## 🔧 开发环境

在开发环境（未打包）中运行时：
- 数据仍存储在用户数据目录（与打包后一致）
- 这确保了开发和生产环境的一致性
- 便于调试和测试

## 📝 数据文件格式

### users.json
```json
{
  "users": [
    {
      "id": "uuid",
      "name": "用户姓名",
      "gender": "male/female",
      "records": [
        {
          "date": "2024-10-18",
          "required_project": "1000m",
          "required_score": 9.5,
          "category1_project": "50m",
          "category1_score": 8.0,
          "category2_project": "basketball",
          "category2_score": 7.5,
          "total_score": 25.0,
          "grade": "良好"
        }
      ]
    }
  ]
}
```

### last_user.json
```json
{
  "last_user_id": "uuid"
}
```

## ⚠️ 注意事项

1. **数据安全**
   - 建议定期备份数据文件
   - 不要手动编辑 JSON 文件，除非你知道自己在做什么
   - 格式错误可能导致数据丢失

2. **隐私保护**
   - 数据存储在本地，不会上传到云端
   - 卸载应用时可选择是否删除数据
   - 多用户系统中，数据存储在当前用户目录下

3. **磁盘空间**
   - 数据文件很小（通常 < 1MB）
   - 图表文件可能占用较多空间
   - 可以定期清理旧的图表文件

4. **权限问题**
   - 应用需要有读写用户数据目录的权限
   - macOS 首次运行可能需要授予权限
   - Windows 通常无需额外授权

## 🛠️ 技术实现

应用使用 `utils/path_helper.py` 模块来处理路径：

```python
from utils.path_helper import get_user_data_dir, get_data_file_path

# 获取用户数据目录
data_dir = get_user_data_dir()

# 获取特定文件路径
users_file = get_data_file_path("users.json")
```

这确保了：
- ✅ 跨平台兼容性
- ✅ 打包后正常工作
- ✅ 数据持久化
- ✅ 多用户隔离

---

**注意**: 此文档适用于 v1.3.0 及更高版本。早期版本可能将数据存储在应用程序目录中。

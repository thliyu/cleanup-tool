# Cleanup Tool - 清理工具

一个简单易用的文件清理工具，帮助你清理系统垃圾文件，释放磁盘空间。

## 功能特性

- 📁 **扫描临时文件** - 自动扫描系统临时文件
- 🗑️ **清理缓存** - 清理浏览器缓存、系统缓存等
- ⚙️ **自定义规则** - 支持自定义清理规则
- 💾 **磁盘分析** - 显示磁盘使用情况
- ✅ **安全确认** - 删除前确认，防止误删

## 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/cleanup-tool.git
cd cleanup-tool

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 命令行模式

```bash
# 运行清理工具
python main.py

# 扫描临时文件
python main.py --scan

# 清理缓存
python main.py --clean-cache

# 查看磁盘使用情况
python main.py --disk-usage

# 自定义清理（删除 .tmp 文件）
python main.py --clean-pattern "*.tmp"
```

### 图形界面模式

```bash
python main.py --gui
```

## 项目结构

```
cleanup-tool/
├── src/
│   ├── __init__.py
│   ├── cleanup.py      # 清理功能核心模块
│   ├── scanner.py      # 文件扫描模块
│   ├── analyzer.py     # 磁盘分析模块
│   └── ui.py           # 用户界面模块
├── tests/              # 测试文件
├── docs/               # 文档
├── main.py             # 主程序入口
├── requirements.txt    # 依赖列表
└── README.md           # 项目说明
```

## 依赖

- Python 3.7+
- tkinter (图形界面)
- psutil (系统信息)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

# 使用指南

## 安装依赖

```bash
pip install -r requirements.txt
```

## 命令行使用

### 图形界面模式

```bash
python main.py
# 或
python main.py --gui
```

### 命令行模式

#### 扫描临时文件

```bash
python main.py --scan
```

#### 清理缓存

```bash
python main.py --clean-cache
```

#### 查看磁盘使用情况

```bash
python main.py --disk-usage
```

#### 按模式清理文件

```bash
python main.py --clean-pattern "*.tmp"
```

#### 预览模式（不实际删除）

```bash
python main.py --clean-pattern "*.tmp" --dry-run
```

## 图形界面功能

### 扫描标签页

- **扫描临时文件**：扫描系统临时目录中的文件
- **扫描缓存目录**：扫描浏览器和系统缓存目录

### 清理标签页

- **清理临时文件**：删除临时文件
- **清理缓存**：删除缓存文件
- **文件模式**：自定义要删除的文件模式（如 `*.tmp`）
- **预览**：预览将要删除的文件（不实际删除）
- **开始清理**：执行清理操作

### 磁盘分析标签页

- **磁盘分区**：显示所有磁盘分区的使用情况
- **目录分析**：分析指定目录的大小分布

### 设置标签页

- **临时文件设置**：设置删除多少天前的临时文件
- **自定义清理目录**：添加或删除要清理的目录

## Python API 使用

```python
from src.cleanup import CleanupManager
from src.scanner import FileScanner
from src.analyzer import DiskAnalyzer

# 扫描临时文件
scanner = FileScanner()
files = scanner.scan_temp_files()

# 清理临时文件
cleanup = CleanupManager()
deleted, failed = cleanup.clean_temp_files(max_age_days=7)

# 查看磁盘使用情况
analyzer = DiskAnalyzer()
usage = analyzer.get_disk_usage()
```

## 注意事项

1. **权限问题**：某些文件可能需要管理员权限才能删除
2. **重要文件**：清理前请确认要删除的文件不是重要文件
3. **备份**：建议在清理前备份重要数据
4. **预览模式**：使用 `--dry-run` 参数预览将要删除的文件

"""使用示例"""
import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cleanup import CleanupManager
from scanner import FileScanner
from analyzer import DiskAnalyzer


def example_scan_temp_files():
    """示例：扫描临时文件"""
    scanner = FileScanner()
    files = scanner.scan_temp_files()

    print(f"找到 {len(files)} 个临时文件")
    for file_info in files[:10]:
        print(f"  {file_info['path']} ({scanner.format_size(file_info['size'])})")


def example_clean_temp_files():
    """示例：清理临时文件"""
    cleanup = CleanupManager(dry_run=True)  # 预览模式
    deleted, failed = cleanup.clean_temp_files(max_age_days=7)

    print(f"预览：将删除 {deleted} 个文件，失败 {failed} 个")


def example_disk_usage():
    """示例：查看磁盘使用情况"""
    analyzer = DiskAnalyzer()
    usage = analyzer.get_disk_usage()

    print("磁盘使用情况:")
    for mountpoint, info in usage.items():
        print(f"  {mountpoint}:")
        print(f"    总大小: {analyzer.format_size(info['total'])}")
        print(f"    已用: {analyzer.format_size(info['used'])}")
        print(f"    可用: {analyzer.format_size(info['free'])}")
        print(f"    使用率: {info['percent']}%")


def example_analyze_directory():
    """示例：分析目录"""
    analyzer = DiskAnalyzer()
    results = analyzer.analyze_directory(str(Path.home()), max_depth=2)

    print(f"分析目录: {Path.home()}")
    print(f"找到 {len(results)} 个项目")
    for item in results[:10]:
        print(f"  {item['name']}: {analyzer.format_size(item['size'])}")


if __name__ == "__main__":
    print("=" * 50)
    print("示例 1: 扫描临时文件")
    print("=" * 50)
    example_scan_temp_files()

    print("\n" + "=" * 50)
    print("示例 2: 清理临时文件（预览模式）")
    print("=" * 50)
    example_clean_temp_files()

    print("\n" + "=" * 50)
    print("示例 3: 查看磁盘使用情况")
    print("=" * 50)
    example_disk_usage()

    print("\n" + "=" * 50)
    print("示例 4: 分析目录")
    print("=" * 50)
    example_analyze_directory()

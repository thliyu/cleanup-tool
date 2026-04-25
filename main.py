"""清理工具 - 主程序入口"""
import argparse
import sys
import tkinter as tk
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.cleanup import CleanupManager
from src.scanner import FileScanner
from src.analyzer import DiskAnalyzer
from src.ui import CleanupApp


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="清理工具 - 清理系统垃圾文件，释放磁盘空间"
    )

    parser.add_argument(
        "--gui",
        action="store_true",
        help="使用图形界面模式"
    )

    parser.add_argument(
        "--scan",
        action="store_true",
        help="扫描临时文件"
    )

    parser.add_argument(
        "--clean-cache",
        action="store_true",
        help="清理缓存"
    )

    parser.add_argument(
        "--disk-usage",
        action="store_true",
        help="显示磁盘使用情况"
    )

    parser.add_argument(
        "--clean-pattern",
        type=str,
        help="按模式清理文件（如 '*.tmp'）"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预览模式，不实际删除文件"
    )

    args = parser.parse_args()

    # 如果没有参数，默认使用 GUI
    if not any(vars(args).values()):
        args.gui = True

    # 图形界面模式
    if args.gui:
        root = tk.Tk()
        app = CleanupApp(root)
        root.mainloop()
        return

    # 命令行模式
    cleanup_manager = CleanupManager(dry_run=args.dry_run)
    scanner = FileScanner()
    analyzer = DiskAnalyzer()

    if args.scan:
        print("扫描临时文件...")
        files = scanner.scan_temp_files()
        print(f"找到 {len(files)} 个临时文件")
        for file_info in files[:20]:
            print(f"  {file_info['path']} ({scanner.format_size(file_info['size'])})")
        if len(files) > 20:
            print(f"  ... 还有 {len(files) - 20} 个文件")

    if args.clean_cache:
        print("清理缓存...")
        deleted, failed = cleanup_manager.clean_cache_dirs()
        print(f"删除 {deleted} 个文件，失败 {failed} 个")

    if args.disk_usage:
        print("磁盘使用情况:")
        usage = analyzer.get_disk_usage()
        for mountpoint, info in usage.items():
            print(f"  {mountpoint}:")
            print(f"    总大小: {analyzer.format_size(info['total'])}")
            print(f"    已用: {analyzer.format_size(info['used'])}")
            print(f"    可用: {analyzer.format_size(info['free'])}")
            print(f"    使用率: {info['percent']}%")

    if args.clean_pattern:
        print(f"按模式 '{args.clean_pattern}' 清理...")
        deleted, failed = cleanup_manager.clean_by_pattern(args.clean_pattern)
        print(f"删除 {deleted} 个文件，失败 {failed} 个")

    # 显示错误信息
    if cleanup_manager.get_errors():
        print("\n错误信息:")
        for error in cleanup_manager.get_errors():
            print(f"  {error}")


if __name__ == "__main__":
    main()

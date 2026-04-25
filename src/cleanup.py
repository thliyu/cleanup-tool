"""清理功能核心模块"""
import os
import shutil
import tempfile
from pathlib import Path
from typing import List, Tuple, Optional


class CleanupManager:
    """清理管理器"""

    def __init__(self, dry_run: bool = False):
        """
        初始化清理管理器

        Args:
            dry_run: 如果为True，只显示将要删除的文件，不实际删除
        """
        self.dry_run = dry_run
        self.deleted_files = []
        self.errors = []

    def scan_temp_files(self) -> List[Path]:
        """扫描系统临时文件"""
        temp_dirs = [
            Path(tempfile.gettempdir()),
            Path(os.environ.get("TEMP", "")),
            Path(os.environ.get("TMP", "")),
        ]

        temp_files = []
        for temp_dir in temp_dirs:
            if temp_dir.exists() and temp_dir.is_dir():
                try:
                    for item in temp_dir.rglob("*"):
                        if item.is_file():
                            temp_files.append(item)
                except (PermissionError, OSError) as e:
                    self.errors.append(f"无法访问 {temp_dir}: {e}")

        return temp_files

    def clean_temp_files(self, max_age_days: int = 7) -> Tuple[int, int]:
        """
        清理临时文件

        Args:
            max_age_days: 删除多少天前的文件

        Returns:
            (删除的文件数, 失败的文件数)
        """
        temp_files = self.scan_temp_files()
        deleted_count = 0
        failed_count = 0

        for file_path in temp_files:
            try:
                # 检查文件年龄
                file_age = (Path(file_path).stat().st_mtime)
                current_time = os.path.getmtime(file_path)
                age_days = (current_time - file_age) / (24 * 3600)

                if age_days >= max_age_days:
                    if not self.dry_run:
                        os.remove(file_path)
                    self.deleted_files.append(str(file_path))
                    deleted_count += 1
            except (PermissionError, OSError) as e:
                self.errors.append(f"无法删除 {file_path}: {e}")
                failed_count += 1

        return deleted_count, failed_count

    def clean_cache_dirs(self, cache_dirs: Optional[List[str]] = None) -> Tuple[int, int]:
        """
        清理缓存目录

        Args:
            cache_dirs: 要清理的缓存目录列表

        Returns:
            (删除的文件数, 失败的文件数)
        """
        if cache_dirs is None:
            cache_dirs = self.get_default_cache_dirs()

        deleted_count = 0
        failed_count = 0

        for cache_dir in cache_dirs:
            cache_path = Path(cache_dir)
            if not cache_path.exists():
                continue

            try:
                for item in cache_path.rglob("*"):
                    if item.is_file():
                        try:
                            if not self.dry_run:
                                os.remove(item)
                            self.deleted_files.append(str(item))
                            deleted_count += 1
                        except (PermissionError, OSError) as e:
                            self.errors.append(f"无法删除 {item}: {e}")
                            failed_count += 1
            except (PermissionError, OSError) as e:
                self.errors.append(f"无法访问 {cache_path}: {e}")

        return deleted_count, failed_count

    def get_default_cache_dirs(self) -> List[str]:
        """获取默认缓存目录"""
        cache_dirs = []

        # Windows 缓存目录
        if os.name == "nt":
            appdata = os.environ.get("APPDATA", "")
            localappdata = os.environ.get("LOCALAPPDATA", "")
            if appdata:
                cache_dirs.extend([
                    os.path.join(appdata, "Microsoft", "Windows", "Cookies"),
                    os.path.join(appdata, "Microsoft", "Windows", "Recent"),
                ])
            if localappdata:
                cache_dirs.extend([
                    os.path.join(localappdata, "Temp"),
                    os.path.join(localappdata, "Microsoft", "Windows", "INetCache"),
                ])

        # Linux/macOS 缓存目录
        else:
            home = os.path.expanduser("~")
            cache_dirs.extend([
                os.path.join(home, ".cache"),
                os.path.join(home, ".mozilla", "firefox", "*", "Cache"),
                os.path.join(home, ".config", "chromium", "Default", "Cache"),
            ])

        return cache_dirs

    def clean_by_pattern(self, pattern: str, search_dir: Optional[str] = None) -> Tuple[int, int]:
        """
        按模式清理文件

        Args:
            pattern: 文件模式（如 "*.tmp"）
            search_dir: 搜索目录，默认为临时目录

        Returns:
            (删除的文件数, 失败的文件数)
        """
        if search_dir is None:
            search_dir = tempfile.gettempdir()

        search_path = Path(search_dir)
        if not search_path.exists():
            return 0, 0

        deleted_count = 0
        failed_count = 0

        try:
            for file_path in search_path.rglob(pattern):
                if file_path.is_file():
                    try:
                        if not self.dry_run:
                            os.remove(file_path)
                        self.deleted_files.append(str(file_path))
                        deleted_count += 1
                    except (PermissionError, OSError) as e:
                        self.errors.append(f"无法删除 {file_path}: {e}")
                        failed_count += 1
        except (PermissionError, OSError) as e:
            self.errors.append(f"无法访问 {search_path}: {e}")

        return deleted_count, failed_count

    def get_errors(self) -> List[str]:
        """获取错误列表"""
        return self.errors

    def get_deleted_files(self) -> List[str]:
        """获取已删除文件列表"""
        return self.deleted_files

    def clear_history(self):
        """清空历史记录"""
        self.deleted_files.clear()
        self.errors.clear()

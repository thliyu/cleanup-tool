"""文件扫描模块"""
import os
import tempfile
from pathlib import Path
from typing import List, Dict, Tuple
import psutil


class FileScanner:
    """文件扫描器"""

    def __init__(self):
        self.temp_dirs = self._get_temp_dirs()

    def _get_temp_dirs(self) -> List[Path]:
        """获取临时目录列表"""
        dirs = []

        # 系统临时目录
        temp_dir = Path(tempfile.gettempdir())
        if temp_dir.exists():
            dirs.append(temp_dir)

        # 环境变量中的临时目录
        for env_var in ["TEMP", "TMP"]:
            env_path = os.environ.get(env_var, "")
            if env_path:
                path = Path(env_path)
                if path.exists() and path not in dirs:
                    dirs.append(path)

        return dirs

    def scan_temp_files(self) -> List[Dict]:
        """扫描临时文件"""
        files = []

        for temp_dir in self.temp_dirs:
            try:
                for item in temp_dir.rglob("*"):
                    if item.is_file():
                        try:
                            stat = item.stat()
                            files.append({
                                "path": str(item),
                                "size": stat.st_size,
                                "modified": stat.st_mtime,
                                "directory": str(temp_dir),
                            })
                        except (PermissionError, OSError):
                            continue
            except (PermissionError, OSError):
                continue

        return files

    def get_disk_usage(self) -> Dict[str, Dict]:
        """获取磁盘使用情况"""
        usage = {}

        for partition in psutil.disk_partitions():
            try:
                usage_info = psutil.disk_usage(partition.mountpoint)
                usage[partition.mountpoint] = {
                    "total": usage_info.total,
                    "used": usage_info.used,
                    "free": usage_info.free,
                    "percent": usage_info.percent,
                }
            except (PermissionError, OSError):
                continue

        return usage

    def format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    def scan_directory_size(self, directory: str) -> Tuple[int, int]:
        """
        扫描目录大小

        Args:
            directory: 目录路径

        Returns:
            (文件总数, 总大小)
        """
        total_size = 0
        file_count = 0

        try:
            for item in Path(directory).rglob("*"):
                if item.is_file():
                    try:
                        total_size += item.stat().st_size
                        file_count += 1
                    except (PermissionError, OSError):
                        continue
        except (PermissionError, OSError):
            return 0, 0

        return file_count, total_size

    def get_file_type_stats(self, files: List[Dict]) -> Dict[str, Dict]:
        """获取文件类型统计"""
        stats = {}

        for file_info in files:
            path = Path(file_info["path"])
            ext = path.suffix.lower() or "no_extension"

            if ext not in stats:
                stats[ext] = {"count": 0, "total_size": 0}

            stats[ext]["count"] += 1
            stats[ext]["total_size"] += file_info["size"]

        return stats

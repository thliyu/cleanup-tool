"""磁盘分析模块"""
import os
from pathlib import Path
from typing import Dict, List, Tuple
import psutil


class DiskAnalyzer:
    """磁盘分析器"""

    def __init__(self):
        pass

    def get_disk_partitions(self) -> List[Dict]:
        """获取磁盘分区信息"""
        partitions = []

        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent,
                })
            except (PermissionError, OSError):
                continue

        return partitions

    def format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    def analyze_directory(self, directory: str, max_depth: int = 3) -> List[Dict]:
        """
        分析目录大小分布

        Args:
            directory: 目录路径
            max_depth: 最大扫描深度

        Returns:
            目录大小列表
        """
        results = []

        try:
            dir_path = Path(directory)
            if not dir_path.exists():
                return results

            for item in dir_path.iterdir():
                if item.is_dir():
                    try:
                        size = self._get_dir_size(item, max_depth - 1)
                        results.append({
                            "name": item.name,
                            "path": str(item),
                            "size": size,
                            "is_dir": True,
                        })
                    except (PermissionError, OSError):
                        continue
                elif item.is_file():
                    try:
                        size = item.stat().st_size
                        results.append({
                            "name": item.name,
                            "path": str(item),
                            "size": size,
                            "is_dir": False,
                        })
                    except (PermissionError, OSError):
                        continue
        except (PermissionError, OSError):
            pass

        # 按大小排序
        results.sort(key=lambda x: x["size"], reverse=True)
        return results

    def _get_dir_size(self, directory: Path, depth: int) -> int:
        """递归获取目录大小"""
        if depth < 0:
            return 0

        total_size = 0
        try:
            for item in directory.rglob("*"):
                if item.is_file():
                    try:
                        total_size += item.stat().st_size
                    except (PermissionError, OSError):
                        continue
        except (PermissionError, OSError):
            return 0

        return total_size

    def get_largest_files(self, directory: str, limit: int = 10) -> List[Dict]:
        """
        获取目录中最大的文件

        Args:
            directory: 目录路径
            limit: 返回数量限制

        Returns:
            最大文件列表
        """
        files = []

        try:
            dir_path = Path(directory)
            if not dir_path.exists():
                return files

            for item in dir_path.rglob("*"):
                if item.is_file():
                    try:
                        stat = item.stat()
                        files.append({
                            "name": item.name,
                            "path": str(item),
                            "size": stat.st_size,
                            "modified": stat.st_mtime,
                        })
                    except (PermissionError, OSError):
                        continue
        except (PermissionError, OSError):
            return files

        # 按大小排序并返回前N个
        files.sort(key=lambda x: x["size"], reverse=True)
        return files[:limit]

    def get_file_type_summary(self, directory: str) -> Dict[str, Dict]:
        """
        获取文件类型汇总

        Args:
            directory: 目录路径

        Returns:
            文件类型统计
        """
        summary = {}

        try:
            dir_path = Path(directory)
            if not dir_path.exists():
                return summary

            for item in dir_path.rglob("*"):
                if item.is_file():
                    try:
                        ext = item.suffix.lower() or "no_extension"
                        size = item.stat().st_size

                        if ext not in summary:
                            summary[ext] = {"count": 0, "total_size": 0}

                        summary[ext]["count"] += 1
                        summary[ext]["total_size"] += size
                    except (PermissionError, OSError):
                        continue
        except (PermissionError, OSError):
            return summary

        return summary

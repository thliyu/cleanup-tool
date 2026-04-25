"""清理功能测试"""
import unittest
import tempfile
import os
from pathlib import Path
from src.cleanup import CleanupManager


class TestCleanup(unittest.TestCase):
    """清理功能测试类"""

    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.cleanup_manager = CleanupManager(dry_run=True)

    def tearDown(self):
        """清理测试环境"""
        if os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)

    def test_scan_temp_files(self):
        """测试扫描临时文件"""
        # 创建一些临时文件
        test_file = Path(self.temp_dir) / "test.tmp"
        test_file.write_text("test content")

        files = self.cleanup_manager.scan_temp_files()
        self.assertIsInstance(files, list)

    def test_clean_by_pattern(self):
        """测试按模式清理"""
        # 创建测试文件
        test_file1 = Path(self.temp_dir) / "test1.tmp"
        test_file2 = Path(self.temp_dir) / "test2.txt"
        test_file1.write_text("test1")
        test_file2.write_text("test2")

        deleted, failed = self.cleanup_manager.clean_by_pattern("*.tmp", self.temp_dir)
        self.assertEqual(deleted, 1)
        self.assertEqual(failed, 0)

    def test_get_errors(self):
        """测试获取错误列表"""
        errors = self.cleanup_manager.get_errors()
        self.assertIsInstance(errors, list)

    def test_get_deleted_files(self):
        """测试获取已删除文件列表"""
        files = self.cleanup_manager.get_deleted_files()
        self.assertIsInstance(files, list)


if __name__ == "__main__":
    unittest.main()

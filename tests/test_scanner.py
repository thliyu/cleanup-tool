"""扫描器测试"""
import unittest
from src.scanner import FileScanner


class TestScanner(unittest.TestCase):
    """扫描器测试类"""

    def setUp(self):
        """设置测试环境"""
        self.scanner = FileScanner()

    def test_scan_temp_files(self):
        """测试扫描临时文件"""
        files = self.scanner.scan_temp_files()
        self.assertIsInstance(files, list)

    def test_format_size(self):
        """测试格式化文件大小"""
        self.assertEqual(self.scanner.format_size(1024), "1.00 KB")
        self.assertEqual(self.scanner.format_size(1024 * 1024), "1.00 MB")
        self.assertEqual(self.scanner.format_size(1024 * 1024 * 1024), "1.00 GB")

    def test_get_disk_usage(self):
        """测试获取磁盘使用情况"""
        usage = self.scanner.get_disk_usage()
        self.assertIsInstance(usage, dict)


if __name__ == "__main__":
    unittest.main()

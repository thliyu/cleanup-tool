"""用户界面模块"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from .cleanup import CleanupManager
from .scanner import FileScanner
from .analyzer import DiskAnalyzer


class CleanupApp:
    """清理工具图形界面"""

    def __init__(self, root):
        self.root = root
        self.root.title("清理工具 v1.0")
        self.root.geometry("800x600")

        # 初始化管理器
        self.cleanup_manager = CleanupManager()
        self.scanner = FileScanner()
        self.analyzer = DiskAnalyzer()

        # 创建界面
        self._create_menu()
        self._create_notebook()
        self._create_status_bar()

    def _create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=file_menu)

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)

        self.root.config(menu=menubar)

    def _create_notebook(self):
        """创建标签页"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建各个标签页
        self._create_scan_tab()
        self._create_cleanup_tab()
        self._create_disk_tab()
        self._create_settings_tab()

    def _create_scan_tab(self):
        """创建扫描标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="扫描")

        # 扫描按钮区域
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(
            button_frame,
            text="扫描临时文件",
            command=self.scan_temp_files
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="扫描缓存目录",
            command=self.scan_cache_dirs
        ).pack(side=tk.LEFT, padx=5)

        # 结果显示区域
        result_frame = ttk.Frame(frame)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 树状视图显示扫描结果
        columns = ("path", "size", "modified")
        self.scan_tree = ttk.Treeview(
            result_frame,
            columns=columns,
            show="headings",
            height=15
        )

        self.scan_tree.heading("path", text="文件路径")
        self.scan_tree.heading("size", text="大小")
        self.scan_tree.heading("modified", text="修改时间")

        self.scan_tree.column("path", width=400)
        self.scan_tree.column("size", width=100)
        self.scan_tree.column("modified", width=150)

        # 滚动条
        scrollbar = ttk.Scrollbar(
            result_frame,
            orient=tk.VERTICAL,
            command=self.scan_tree.yview
        )
        self.scan_tree.configure(yscrollcommand=scrollbar.set)

        self.scan_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 统计信息
        self.scan_stats = ttk.Label(frame, text="扫描结果: 0 个文件")
        self.scan_stats.pack(fill=tk.X, padx=10, pady=5)

    def _create_cleanup_tab(self):
        """创建清理标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="清理")

        # 清理选项
        options_frame = ttk.LabelFrame(frame, text="清理选项", padding=10)
        options_frame.pack(fill=tk.X, padx=10, pady=10)

        self.clean_temp_var = tk.BooleanVar(value=True)
        self.clean_cache_var = tk.BooleanVar(value=True)
        self.clean_pattern_var = tk.StringVar(value="*.tmp")

        ttk.Checkbutton(
            options_frame,
            text="清理临时文件",
            variable=self.clean_temp_var
        ).pack(anchor=tk.W, pady=2)

        ttk.Checkbutton(
            options_frame,
            text="清理缓存",
            variable=self.clean_cache_var
        ).pack(anchor=tk.W, pady=2)

        pattern_frame = ttk.Frame(options_frame)
        pattern_frame.pack(fill=tk.X, pady=5)
        ttk.Label(pattern_frame, text="文件模式:").pack(side=tk.LEFT)
        ttk.Entry(
            pattern_frame,
            textvariable=self.clean_pattern_var,
            width=30
        ).pack(side=tk.LEFT, padx=5)

        # 操作按钮
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(
            button_frame,
            text="开始清理",
            command=self.start_cleanup
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="预览",
            command=self.preview_cleanup
        ).pack(side=tk.LEFT, padx=5)

        # 清理日志
        log_frame = ttk.LabelFrame(frame, text="清理日志", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_text = tk.Text(log_frame, height=10, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def _create_disk_tab(self):
        """创建磁盘分析标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="磁盘分析")

        # 磁盘分区信息
        disk_frame = ttk.LabelFrame(frame, text="磁盘分区", padding=10)
        disk_frame.pack(fill=tk.X, padx=10, pady=10)

        columns = ("mountpoint", "total", "used", "free", "percent")
        self.disk_tree = ttk.Treeview(
            disk_frame,
            columns=columns,
            show="headings",
            height=5
        )

        self.disk_tree.heading("mountpoint", text="挂载点")
        self.disk_tree.heading("total", text="总大小")
        self.disk_tree.heading("used", text="已用")
        self.disk_tree.heading("free", text="可用")
        self.disk_tree.heading("percent", text="使用率")

        self.disk_tree.pack(fill=tk.X)

        # 目录分析
        analyze_frame = ttk.LabelFrame(frame, text="目录分析", padding=10)
        analyze_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        dir_frame = ttk.Frame(analyze_frame)
        dir_frame.pack(fill=tk.X, pady=5)

        self.dir_path_var = tk.StringVar(value=Path.home())
        ttk.Label(dir_frame, text="目录:").pack(side=tk.LEFT)
        ttk.Entry(
            dir_frame,
            textvariable=self.dir_path_var,
            width=50
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            dir_frame,
            text="浏览",
            command=self.browse_directory
        ).pack(side=tk.LEFT)

        ttk.Button(
            dir_frame,
            text="分析",
            command=self.analyze_directory
        ).pack(side=tk.LEFT, padx=5)

        # 目录分析结果
        columns = ("name", "size", "path")
        self.dir_tree = ttk.Treeview(
            analyze_frame,
            columns=columns,
            show="headings",
            height=10
        )

        self.dir_tree.heading("name", text="名称")
        self.dir_tree.heading("size", text="大小")
        self.dir_tree.heading("path", text="路径")

        self.dir_tree.column("name", width=200)
        self.dir_tree.column("size", width=100)
        self.dir_tree.column("path", width=300)

        self.dir_tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def _create_settings_tab(self):
        """创建设置标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="设置")

        # 临时文件设置
        temp_frame = ttk.LabelFrame(frame, text="临时文件设置", padding=10)
        temp_frame.pack(fill=tk.X, padx=10, pady=10)

        self.temp_age_var = tk.IntVar(value=7)
        ttk.Label(temp_frame, text="删除多少天前的临时文件:").pack(anchor=tk.W)
        ttk.Scale(
            temp_frame,
            from_=1,
            to=30,
            variable=self.temp_age_var,
            orient=tk.HORIZONTAL
        ).pack(fill=tk.X, pady=5)
        self.temp_age_label = ttk.Label(temp_frame, text=f"{self.temp_age_var.get()} 天")
        self.temp_age_label.pack()

        # 自定义清理目录
        custom_frame = ttk.LabelFrame(frame, text="自定义清理目录", padding=10)
        custom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(custom_frame, text="添加要清理的目录:").pack(anchor=tk.W)

        dir_list_frame = ttk.Frame(custom_frame)
        dir_list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.dir_listbox = tk.Listbox(dir_list_frame, height=5)
        self.dir_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(dir_list_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.dir_listbox.yview)
        self.dir_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        button_frame = ttk.Frame(custom_frame)
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            button_frame,
            text="添加目录",
            command=self.add_custom_dir
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="删除目录",
            command=self.remove_custom_dir
        ).pack(side=tk.LEFT, padx=5)

    def _create_status_bar(self):
        """创建状态栏"""
        self.status_var = tk.StringVar(value="就绪")
        self.status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def scan_temp_files(self):
        """扫描临时文件"""
        self.status_var.set("正在扫描临时文件...")
        self.root.update()

        files = self.scanner.scan_temp_files()

        # 清空树状视图
        for item in self.scan_tree.get_children():
            self.scan_tree.delete(item)

        # 添加文件到树状视图
        for file_info in files[:100]:  # 限制显示数量
            self.scan_tree.insert("", tk.END, values=(
                file_info["path"],
                self.scanner.format_size(file_info["size"]),
                ""
            ))

        self.scan_stats.config(text=f"扫描结果: {len(files)} 个文件")
        self.status_var.set(f"扫描完成，找到 {len(files)} 个文件")

    def scan_cache_dirs(self):
        """扫描缓存目录"""
        self.status_var.set("正在扫描缓存目录...")
        self.root.update()

        cache_dirs = self.cleanup_manager.get_default_cache_dirs()
        total_files = 0

        for item in self.scan_tree.get_children():
            self.scan_tree.delete(item)

        for cache_dir in cache_dirs:
            if Path(cache_dir).exists():
                count, size = self.scanner.scan_directory_size(cache_dir)
                total_files += count
                self.scan_tree.insert("", tk.END, values=(
                    cache_dir,
                    self.scanner.format_size(size),
                    f"{count} 个文件"
                ))

        self.scan_stats.config(text=f"扫描结果: {total_files} 个文件")
        self.status_var.set(f"扫描完成，找到 {total_files} 个文件")

    def start_cleanup(self):
        """开始清理"""
        if not messagebox.askyesno("确认", "确定要开始清理吗？"):
            return

        self.status_var.set("正在清理...")
        self.root.update()

        self.cleanup_manager.clear_history()

        total_deleted = 0
        total_failed = 0

        if self.clean_temp_var.get():
            deleted, failed = self.cleanup_manager.clean_temp_files(
                max_age_days=self.temp_age_var.get()
            )
            total_deleted += deleted
            total_failed += failed

        if self.clean_cache_var.get():
            deleted, failed = self.cleanup_manager.clean_cache_dirs()
            total_deleted += deleted
            total_failed += failed

        # 清理日志
        self._update_log(f"清理完成！")
        self._update_log(f"删除文件: {total_deleted} 个")
        self._update_log(f"失败: {total_failed} 个")

        if self.cleanup_manager.get_errors():
            self._update_log("\n错误信息:")
            for error in self.cleanup_manager.get_errors():
                self._update_log(f"  - {error}")

        self.status_var.set(f"清理完成！删除 {total_deleted} 个文件")

    def preview_cleanup(self):
        """预览清理"""
        self.status_var.set("正在预览...")
        self.root.update()

        self.cleanup_manager.clear_history()
        self.cleanup_manager.dry_run = True

        total_files = 0

        if self.clean_temp_var.get():
            deleted, _ = self.cleanup_manager.clean_temp_files(
                max_age_days=self.temp_age_var.get()
            )
            total_files += deleted

        if self.clean_cache_var.get():
            deleted, _ = self.cleanup_manager.clean_cache_dirs()
            total_files += deleted

        self.cleanup_manager.dry_run = False

        self._update_log(f"预览完成！")
        self._update_log(f"将删除 {total_files} 个文件")

        self.status_var.set(f"预览完成！将删除 {total_files} 个文件")

    def analyze_directory(self):
        """分析目录"""
        directory = self.dir_path_var.get()

        if not Path(directory).exists():
            messagebox.showerror("错误", "目录不存在！")
            return

        self.status_var.set("正在分析目录...")
        self.root.update()

        # 清空树状视图
        for item in self.dir_tree.get_children():
            self.dir_tree.delete(item)

        # 分析目录
        results = self.analyzer.analyze_directory(directory)

        for item in results:
            self.dir_tree.insert("", tk.END, values=(
                item["name"],
                self.analyzer.format_size(item["size"]),
                item["path"]
            ))

        self.status_var.set(f"分析完成！找到 {len(results)} 个项目")

    def browse_directory(self):
        """浏览目录"""
        directory = filedialog.askdirectory()
        if directory:
            self.dir_path_var.set(directory)

    def add_custom_dir(self):
        """添加自定义目录"""
        directory = filedialog.askdirectory()
        if directory and directory not in self.dir_listbox.get(0, tk.END):
            self.dir_listbox.insert(tk.END, directory)

    def remove_custom_dir(self):
        """删除自定义目录"""
        selection = self.dir_listbox.curselection()
        if selection:
            self.dir_listbox.delete(selection[0])

    def _update_log(self, message: str):
        """更新日志"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def show_about(self):
        """显示关于对话框"""
        messagebox.showinfo(
            "关于",
            "清理工具 v1.0\n\n"
            "一个简单易用的文件清理工具\n"
            "帮助你清理系统垃圾文件，释放磁盘空间\n\n"
            "© 2024 Cleanup Tool"
        )

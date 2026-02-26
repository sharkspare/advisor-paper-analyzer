import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import sys
import io
from pachong import GoogleScholarScraper


class ScholarScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("谷歌学术论文爬虫")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # 设置主题颜色
        self.bg_color = "#f0f0f0"
        self.primary_color = "#4CAF50"
        self.root.configure(bg=self.bg_color)
        
        # 创建主框架
        self.create_widgets()
        
        # 爬虫对象
        self.scraper = None
        self.is_running = False
        
    def create_widgets(self):
        # 标题
        title_frame = tk.Frame(self.root, bg="#2196F3", height=80)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="📚 谷歌学术论文爬虫工具",
            font=("微软雅黑", 20, "bold"),
            bg="#2196F3",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # 输入区域框架
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(padx=30, pady=10, fill=tk.X)
        
        # User ID 输入
        user_id_frame = tk.Frame(input_frame, bg=self.bg_color)
        user_id_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            user_id_frame,
            text="导师用户ID:",
            font=("微软雅黑", 11),
            bg=self.bg_color,
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        self.user_id_entry = tk.Entry(
            user_id_frame,
            font=("Consolas", 11),
            relief=tk.SOLID,
            borderwidth=1
        )
        self.user_id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        # 不设置默认值，保护隐私
        
        # 提示标签
        tk.Label(
            input_frame,
            text="💡 提示: 从导师主页URL中提取，如 https://scholar.google.com/citations?user=AAAAAAAAAAAA",
            font=("微软雅黑", 9),
            bg=self.bg_color,
            fg="#666",
            anchor="w"
        ).pack(fill=tk.X, padx=(120, 0))
        
        # Max Papers 输入
        max_papers_frame = tk.Frame(input_frame, bg=self.bg_color)
        max_papers_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(
            max_papers_frame,
            text="爬取数量:",
            font=("微软雅黑", 11),
            bg=self.bg_color,
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        self.max_papers_entry = tk.Entry(
            max_papers_frame,
            font=("Consolas", 11),
            relief=tk.SOLID,
            borderwidth=1
        )
        self.max_papers_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.max_papers_entry.insert(0, "200")  # 默认值
        
        tk.Label(
            max_papers_frame,
            text="条",
            font=("微软雅黑", 11),
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        # 按钮框架
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        # 开始按钮
        self.start_button = tk.Button(
            button_frame,
            text="🚀 开始爬取",
            font=("微软雅黑", 12, "bold"),
            bg=self.primary_color,
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
            command=self.start_scraping
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        # 停止按钮
        self.stop_button = tk.Button(
            button_frame,
            text="⏹ 停止",
            font=("微软雅黑", 12, "bold"),
            bg="#f44336",
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.stop_scraping
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        # 清空按钮
        clear_button = tk.Button(
            button_frame,
            text="🗑 清空日志",
            font=("微软雅黑", 12, "bold"),
            bg="#FF9800",
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
            command=self.clear_log
        )
        clear_button.pack(side=tk.LEFT, padx=10)
        
        # 进度条
        self.progress_frame = tk.Frame(self.root, bg=self.bg_color)
        self.progress_frame.pack(padx=30, pady=10, fill=tk.X)
        
        tk.Label(
            self.progress_frame,
            text="进度:",
            font=("微软雅黑", 10),
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=500
        )
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 日志输出区域
        log_frame = tk.Frame(self.root, bg=self.bg_color)
        log_frame.pack(padx=30, pady=10, fill=tk.BOTH, expand=True)
        
        tk.Label(
            log_frame,
            text="📋 运行日志:",
            font=("微软雅黑", 11, "bold"),
            bg=self.bg_color,
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            bg="#ffffff",
            fg="#333",
            relief=tk.SOLID,
            borderwidth=1,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        self.status_label = tk.Label(
            self.root,
            text="状态: 就绪",
            font=("微软雅黑", 9),
            bg="#e0e0e0",
            anchor="w",
            padx=10,
            pady=5
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
    def log(self, message):
        """添加日志到文本框"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)
        
    def update_status(self, status):
        """更新状态栏"""
        self.status_label.config(text=f"状态: {status}")
        
    def validate_inputs(self):
        """验证输入"""
        user_id = self.user_id_entry.get().strip()
        max_papers = self.max_papers_entry.get().strip()
        
        if not user_id:
            messagebox.showerror("错误", "请输入导师用户ID！")
            return False
        
        if not max_papers.isdigit() or int(max_papers) <= 0:
            messagebox.showerror("错误", "爬取数量必须是正整数！")
            return False
        
        return True
    
    def start_scraping(self):
        """开始爬取"""
        if not self.validate_inputs():
            return
        
        if self.is_running:
            messagebox.showwarning("警告", "爬虫正在运行中！")
            return
        
        # 获取输入值
        user_id = self.user_id_entry.get().strip()
        max_papers = int(self.max_papers_entry.get().strip())
        
        # 更新UI状态
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_bar.start()
        self.is_running = True
        self.update_status("运行中...")
        
        # 清空之前的日志
        self.clear_log()
        self.log(f"{'='*60}")
        self.log(f"开始爬取论文信息")
        self.log(f"用户ID: {user_id}")
        self.log(f"目标数量: {max_papers} 条")
        self.log(f"{'='*60}\n")
        
        # 在新线程中运行爬虫
        thread = threading.Thread(
            target=self.run_scraper,
            args=(user_id, max_papers),
            daemon=True
        )
        thread.start()
    
    def run_scraper(self, user_id, max_papers):
        """在后台线程中运行爬虫"""
        try:
            # 创建爬虫实例
            self.scraper = GoogleScholarScraper(user_id=user_id, max_papers=max_papers)
            
            # 重定向print输出到GUI
            class GUIOutput:
                def __init__(self, log_func):
                    self.log_func = log_func
                    
                def write(self, text):
                    if text.strip():
                        self.log_func(text.rstrip())
                        
                def flush(self):
                    pass
            
            old_stdout = sys.stdout
            sys.stdout = GUIOutput(self.log)
            
            # 执行爬取
            papers = self.scraper.scrape()
            
            # 恢复stdout
            sys.stdout = old_stdout
            
            if papers:
                self.log(f"\n{'='*60}")
                self.log("正在保存数据...")
                
                # 保存结果（使用默认文件名 papers_userid）
                self.scraper.save_to_csv()
                self.scraper.save_to_txt()
                
                csv_filename = f'papers_{user_id}.csv'
                txt_filename = f'papers_{user_id}.txt'
                
                self.log(f"\n✅ 爬取完成！")
                self.log(f"共获取 {len(papers)} 条论文信息")
                
                # 统计信息
                years = [p['发表时间'] for p in papers if p['发表时间'] != 'N/A']
                if years:
                    self.log(f"年份范围: {min(years)} - {max(years)}")
                
                self.log(f"{'='*60}")
                
                self.root.after(0, lambda: messagebox.showinfo(
                    "成功",
                    f"爬取完成！\n\n共获取 {len(papers)} 条论文\n\n已保存到:\n- {csv_filename}\n- {txt_filename}"
                ))
            else:
                self.log("\n⚠️ 未获取到任何数据")
                self.root.after(0, lambda: messagebox.showwarning("警告", "未获取到任何论文数据！"))
                
        except Exception as e:
            error_msg = f"❌ 错误: {str(e)}"
            self.log(f"\n{error_msg}")
            self.root.after(0, lambda: messagebox.showerror("错误", f"爬取过程中出现错误:\n{str(e)}"))
        
        finally:
            # 恢复stdout
            sys.stdout = old_stdout
            
            # 更新UI状态
            self.root.after(0, self.scraping_finished)
    
    def stop_scraping(self):
        """停止爬取"""
        if messagebox.askyesno("确认", "确定要停止爬取吗？"):
            self.is_running = False
            self.log("\n⏹ 用户手动停止")
            self.scraping_finished()
    
    def scraping_finished(self):
        """爬取结束后的UI更新"""
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress_bar.stop()
        self.is_running = False
        self.update_status("就绪")


def main():
    root = tk.Tk()
    app = ScholarScraperGUI(root)
    
    # 居中显示窗口
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()

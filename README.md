# Google Scholar Paper Scraper

[English](#english) | [中文](#chinese)

<a name="chinese"></a>

## 📚 谷歌学术论文爬虫工具

一个简单易用的谷歌学术论文信息爬取工具，支持图形化界面，可快速获取导师的所有论文发表信息。

### ✨ 主要特性

- 🖥️ **图形化界面** - 无需编程基础，点击即可使用
- 📊 **双格式输出** - 自动生成CSV和TXT两种格式
- 🔄 **智能翻页** - 自动处理大量论文，智能检测列表末尾
- 💾 **批量爬取** - 支持一次性获取200+篇论文信息
- 📁 **文件自动命名** - 使用用户ID命名，避免覆盖
- 🚀 **一键打包** - 可打包成Windows exe文件，无需Python环境

### 📥 下载使用

#### 方式1：直接使用exe（推荐给非程序员）

1. 前往 [Releases](../../releases) 下载最新版本的exe文件
2. 解压后双击运行 `谷歌学术论文爬虫.exe`
3. 按照界面提示操作即可

#### 方式2：运行Python源码

```bash
# 克隆项目
git clone https://github.com/你的用户名/google-scholar-scraper.git
cd google-scholar-scraper

# 安装依赖
pip install -r requirements.txt

# 运行GUI程序
python gui_launcher.py

# 或直接运行爬虫（命令行）
python pachong.py
```

### 🎯 使用说明

1. **获取导师用户ID**
   - 访问 [谷歌学术](https://scholar.google.com)
   - 搜索导师并进入主页
   - 从URL中复制 `user=` 后面的ID
   ```
   https://scholar.google.com/citations?user=AAAAAAAAAAAA
                                             ↑↑↑↑↑↑↑↑↑↑↑↑
                                          这就是用户ID
   ```

2. **运行程序**
   - 输入用户ID和爬取数量
   - 点击"开始爬取"
   - 等待完成

3. **查看结果**
   - `papers_用户ID.csv` - Excel可打开
   - `papers_用户ID.txt` - 纯文本格式

### 📋 获取信息

- 📝 论文标题
- 👥 作者列表
- 📅 发表时间
- 📖 发表期刊/会议

### 🤖 进阶应用

将生成的论文数据上传给AI（ChatGPT/Claude等）进行深度分析：

- 研究方向演变趋势
- 科研活跃度评估
- 论文署名习惯分析
- 学术影响力统计
- 合作网络分析

详见完整文档中的 [AI分析指南](docs/README_CN.md#进阶技巧)

### 💻 系统要求

- **Python版本**: Python 3.7+
- **操作系统**: Windows / macOS / Linux
- **网络**: 需要能访问 scholar.google.com

### 🛠️ 技术栈

- **爬虫**: requests + BeautifulSoup4
- **GUI**: tkinter
- **打包**: PyInstaller

### 📦 打包成exe

```bash
# 安装打包工具
pip install pyinstaller

# 执行打包
python -m PyInstaller --name=谷歌学术论文爬虫 --onefile --windowed --clean gui_launcher.py

# 生成的exe在 dist/ 目录
```

或直接运行：
```bash
# Windows
.\打包.bat

# 自动准备分发文件
.\准备分发.bat
```

### 📖 文档

- [完整使用说明](docs/README_CN.md)
- [快速入门指南](docs/快速指南.txt)
- [打包说明](docs/打包说明.md)

### ⚠️ 注意事项

- 请遵守谷歌学术的使用条款
- 合理控制爬取频率，避免IP被封
- 仅供学习研究使用，请勿商用

### 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 📄 开源协议

本项目采用 [MIT License](LICENSE)

### 🙏 致谢

感谢谷歌学术提供的公开数据

---

<a name="english"></a>

## 📚 Google Scholar Paper Scraper

A simple and user-friendly tool to scrape paper information from Google Scholar with a graphical interface.

### ✨ Features

- 🖥️ **GUI Interface** - No programming required
- 📊 **Dual Format Output** - Generates both CSV and TXT files
- 🔄 **Smart Pagination** - Automatically handles large datasets
- 💾 **Batch Scraping** - Support 200+ papers at once
- 📁 **Auto Naming** - Files named by user ID
- 🚀 **Portable** - Can be packaged as Windows exe

### 📥 Installation

#### Method 1: Use Executable (Recommended for non-programmers)

1. Download from [Releases](../../releases)
2. Extract and run `谷歌学术论文爬虫.exe`
3. Follow the GUI instructions

#### Method 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/google-scholar-scraper.git
cd google-scholar-scraper

# Install dependencies
pip install -r requirements.txt

# Run GUI
python gui_launcher.py

# Or run CLI version
python pachong.py
```

### 🎯 Usage

1. **Get Scholar User ID**
   - Visit [Google Scholar](https://scholar.google.com)
   - Search and go to scholar's profile
   - Copy ID from URL: `user=AAAAAAAAAAAA`

2. **Run Program**
   - Enter user ID and paper count
   - Click "Start Scraping"
   - Wait for completion

3. **View Results**
   - `papers_userID.csv` - Excel compatible
   - `papers_userID.txt` - Plain text

### 📋 Data Collected

- 📝 Paper Title
- 👥 Authors
- 📅 Publication Year
- 📖 Journal/Conference

### 💻 Requirements

- **Python**: 3.7+
- **OS**: Windows / macOS / Linux
- **Network**: Access to scholar.google.com

### 🛠️ Tech Stack

- **Scraper**: requests + BeautifulSoup4
- **GUI**: tkinter
- **Packaging**: PyInstaller

### 📖 Documentation

- [Full Documentation (CN)](docs/README_CN.md)
- [Quick Start Guide](docs/快速指南.txt)
- [Build Guide](docs/打包说明.md)

### ⚠️ Disclaimer

- Follow Google Scholar's Terms of Service
- Use responsibly, avoid excessive scraping
- For educational purposes only

### 🤝 Contributing

Issues and Pull Requests are welcome!

### 📄 License

This project is licensed under the [MIT License](LICENSE)

---

**Star ⭐ this repo if you find it helpful!**

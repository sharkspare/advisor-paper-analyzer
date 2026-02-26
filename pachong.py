import requests
from bs4 import BeautifulSoup
import time
import csv
import random

class GoogleScholarScraper:
    def __init__(self, user_id, max_papers=200):
        """
        初始化爬虫
        :param user_id: 谷歌学术用户ID（从URL中获取）
        :param max_papers: 需要爬取的论文数量
        """
        self.user_id = user_id
        self.max_papers = max_papers
        self.base_url = "https://scholar.google.com/citations"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.papers = []
    
    def get_papers_page(self, start=0, pagesize=100):
        """
        获取指定页面的论文列表
        :param start: 起始位置
        :param pagesize: 每页数量
        :return: 解析后的HTML
        """
        params = {
            'user': self.user_id,
            'hl': 'zh-CN',
            'cstart': start,
            'pagesize': pagesize
        }
        
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"请求失败: {e}")
            return None
    
    def parse_paper_info(self, tr_element):
        """
        解析单条论文信息
        :param tr_element: tr标签元素
        :return: 论文信息字典
        """
        try:
            # 提取标题
            title_element = tr_element.find('a', class_='gsc_a_at')
            title = title_element.text.strip() if title_element else "N/A"
            
            # 提取作者
            author_element = tr_element.find('div', class_='gs_gray')
            authors = author_element.text.strip() if author_element else "N/A"
            
            # 提取发表时间（在最后一个td中）
            year_element = tr_element.find('span', class_='gsc_a_h')
            year = year_element.text.strip() if year_element else "N/A"
            
            # 提取期刊/会议信息（第二个gs_gray）
            gray_divs = tr_element.find_all('div', class_='gs_gray')
            publication = gray_divs[1].text.strip() if len(gray_divs) > 1 else "N/A"
            
            return {
                '标题': title,
                '作者': authors,
                '发表时间': year,
                '发表信息': publication
            }
        except Exception as e:
            print(f"解析论文信息时出错: {e}")
            return None
    
    def scrape(self):
        """
        执行爬取操作
        """
        print(f"开始爬取用户 {self.user_id} 的论文信息...")
        print(f"目标数量: {self.max_papers} 条")
        
        start = 0
        pagesize = 100  # 每页100条
        
        while len(self.papers) < self.max_papers:
            print(f"\n正在爬取第 {start + 1} - {start + pagesize} 条...")
            
            # 获取页面
            soup = self.get_papers_page(start, pagesize)
            if not soup:
                print("无法获取页面，停止爬取")
                break
            
            # 查找所有论文条目
            paper_rows = soup.find_all('tr', class_='gsc_a_tr')
            
            if not paper_rows:
                print("没有找到更多论文，爬取完成")
                break
            
            # 记录本页获取到的论文数量
            current_page_count = len(paper_rows)
            
            # 解析每条论文
            for row in paper_rows:
                if len(self.papers) >= self.max_papers:
                    break
                
                paper_info = self.parse_paper_info(row)
                if paper_info:
                    self.papers.append(paper_info)
                    print(f"  [{len(self.papers)}] {paper_info['发表时间']} - {paper_info['标题'][:50]}...")
            
            # 如果当前页论文数量少于pagesize，说明已经是最后一页了
            if current_page_count < pagesize:
                print("已到达论文列表末尾，停止爬取")
                break
            
            start += pagesize
            
            # 随机延迟，避免请求过快
            time.sleep(random.uniform(1, 3))
        
        print(f"\n爬取完成！共获取 {len(self.papers)} 条论文信息")
        return self.papers
    
    def save_to_csv(self, filename=None):
        """
        保存结果到CSV文件
        :param filename: 输出文件名，如果为None则自动生成
        """
        if not self.papers:
            print("没有数据可保存")
            return
        
        if filename is None:
            filename = f'papers_{self.user_id}.csv'
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=['标题', '作者', '发表时间', '发表信息'])
                writer.writeheader()
                writer.writerows(self.papers)
            print(f"数据已保存到 {filename}")
        except Exception as e:
            print(f"保存文件时出错: {e}")
    
    def save_to_txt(self, filename=None):
        """
        保存结果到TXT文件
        :param filename: 输出文件名，如果为None则自动生成
        """
        if not self.papers:
            print("没有数据可保存")
            return
        
        if filename is None:
            filename = f'papers_{self.user_id}.txt'
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for i, paper in enumerate(self.papers, 1):
                    f.write(f"{'='*80}\n")
                    f.write(f"第 {i} 篇论文\n")
                    f.write(f"{'='*80}\n")
                    f.write(f"标题: {paper['标题']}\n")
                    f.write(f"作者: {paper['作者']}\n")
                    f.write(f"发表时间: {paper['发表时间']}\n")
                    f.write(f"发表信息: {paper['发表信息']}\n\n")
            print(f"数据已保存到 {filename}")
        except Exception as e:
            print(f"保存文件时出错: {e}")


def main():
    # 示例用法
    # 从URL https://scholar.google.com/citations?user=qfaMS6EAAAAJ 中提取用户ID
    user_id = "qfaMS6EAAAAJ"  # 请替换为目标导师的用户ID
    
    # 创建爬虫实例
    scraper = GoogleScholarScraper(user_id=user_id, max_papers=400)
    
    # 执行爬取
    papers = scraper.scrape()
    
    # 保存结果（不传参数，自动使用 papers_userid 格式）
    scraper.save_to_csv()
    scraper.save_to_txt()
    
    # 打印统计信息
    print(f"\n{'='*80}")
    print(f"统计信息:")
    print(f"  总论文数: {len(papers)}")
    if papers:
        years = [p['发表时间'] for p in papers if p['发表时间'] != 'N/A']
        if years:
            print(f"  年份范围: {min(years)} - {max(years)}")


if __name__ == "__main__":
    main()

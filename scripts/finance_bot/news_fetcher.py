import feedparser
import os
import re
from datetime import datetime

def clean_text(text):
    """彻底清除 HTML 标签并处理特殊字符"""
    if not text:
        return ""
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def fetch_hk_news():
    """抓取新时空专业财经 RSS 源"""
    rss_urls = [
        "https://www.newtimespace.com/feed/rss_template.xml?id=100000&site=rss&lang=zh-cn"
    ]
    news_items = []
    seen_titles = set()
    
    for url in rss_urls:
        try:
            print(f"Fetching HK news from: {url}")
            d = feedparser.parse(url)
            for entry in d.entries[:5]:
                title = entry.get('title', '无标题')
                if title in seen_titles: continue
                
                summary = clean_text(entry.get('summary') or entry.get('description', ''))
                
                news_items.append({
                    "title": title,
                    "summary": summary,
                    "date": entry.get('published', '')[:16] # 截取日期部分
                })
                seen_titles.add(title)
        except Exception as e:
            print(f"Error fetching HK news: {e}")
    
    # 按时间戳尝试简单排序（如果有的话），这里取前 5 条最精华的
    return news_items[:6]

def update_markdown(hk_news):
    file_path = "docs/finance/index.md"
    if not os.path.exists(file_path): return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 构建今日简讯区域的内容 (纯港股版)
    brief_content = "## 🕒 今日简讯 (Today's Brief)\n\n"
    
    brief_content += "::: tip 🇭🇰 港股投研专题 (新时空)\n"
    if hk_news:
        for item in hk_news:
            brief_content += f"- **{item['title']}**\n  _{item['summary']}_\n\n"
    else:
        brief_content += "- 暂无港股更新\n"
    brief_content += ":::\n"

    # 正则替换原有简讯区域
    pattern = re.compile(r'## 🕒 今日简讯.*?## 📊 市场脉搏', re.DOTALL)
    new_page_content = pattern.sub(brief_content + "\n## 📊 市场脉搏", content)

    # 更新最后更新时间徽章
    new_page_content = re.sub(r'最后更新: \d{4}-\d{2}-\d{2}.*?"', f'最后更新: {datetime.now().strftime("%Y-%m-%d %H:%M")}"', new_page_content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_page_content)
    print("Finance dashboard updated: Focused on HK RSS source.")

if __name__ == "__main__":
    h_news = fetch_hk_news()
    update_markdown(h_news)

import feedparser
import os
import re
from datetime import datetime, timedelta, timezone
import time

# 数据源配置
CONFIG = {
    "A股要闻": {
        "name": "财联社加红要闻",
        "url": "https://rsshub.rssforever.com/cls/telegraph/red",
        "limit": 5
    },
    "港股投研": {
        "name": "新时空专业财经",
        "url": "https://www.newtimespace.com/feed/rss_template.xml?id=100000&site=rss&lang=zh-cn",
        "limit": 8
    }
}

def clean_text(text):
    """彻底清除 HTML 标签并处理特殊字符"""
    if not text:
        return ""
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"')
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'^【.*?】', '', text)
    return text.strip()

def fetch_feed(source_key):
    """通用 RSS 抓取函数"""
    cfg = CONFIG[source_key]
    print(f"正在抓取 {cfg['name']}...")
    try:
        d = feedparser.parse(cfg['url'])
        items = []
        for entry in d.entries[:cfg['limit']]:
            title = entry.get('title', '无标题')
            summary = clean_text(entry.get('summary') or entry.get('description', ''))
            
            # 1. 处理多个 Category (考虑到 0 个或多个的情况)
            categories = []
            if 'tags' in entry:
                # 很多 RSS 解析器会将 category 放入 tags 列表
                categories = [tag.get('term') for tag in entry.tags if tag.get('term')]
            elif 'category' in entry:
                # 如果只有一个 category 且不是列表
                categories = [entry.category]

            # 2. 将 GMT 时间转换为北京时间 (UTC+8) 并保留秒
            pub_time_beijing = "未知"
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                # 将结构化时间转为 UTC datetime，再转为北京时间
                utc_dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                beijing_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
                pub_time_beijing = beijing_dt.strftime("%H:%M:%S")

            items.append({
                "title": title,
                "summary": summary,
                "pub_time": pub_time_beijing,
                "categories": categories
            })
        return items
    except Exception as e:
        print(f"抓取 {cfg['name']} 失败: {e}")
        return []

def update_markdown(a_news, hk_news):
    file_path = "docs/finance/daily-news.md"
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # --- 1. 更新系统同步时间 ---
    tz_beijing = timezone(timedelta(hours=8))
    now_beijing = datetime.now(tz_beijing)
    sync_time_str = now_beijing.strftime("%Y-%m-%d %H:%M:%S")
    
    time_html = f'\n<p align="right">\n  <Badge type="tip" text="最后同步: {sync_time_str}" />\n</p>\n'
    
    content = re.sub(
        r'<!--\s*UPDATE_TIME_START\s*-->.*?<!--\s*UPDATE_TIME_END\s*-->', 
        f'<!-- UPDATE_TIME_START -->{time_html}<!-- UPDATE_TIME_END -->', 
        content, 
        flags=re.DOTALL
    )

    # --- 2. 更新新闻内容 ---
    news_body = "\n"
    
    # 通用新闻格式化函数
    def format_items(news_list, section_title):
        section_content = f"### {section_title}\n"
        if not news_list:
            section_content += "- 暂无实时更新\n\n"
            return section_content
            
        for item in news_list:
            # 标题与时间
            section_content += f"- **[{item['pub_time']}] {item['title']}**\n"
            # 正文内容
            section_content += f"  {item['summary']}\n"
            # 类别标签 (另起一行展示多个)
            if item['categories']:
                badges = " ".join([f'<Badge type="info" text="{cat}" />' for cat in item['categories']])
                section_content += f"  <br/> {badges}\n\n"
            else:
                section_content += "\n"
        return section_content

    news_body += format_items(a_news, "🔴 A股 & 宏观要闻")
    news_body += format_items(hk_news, "🇭🇰 港股投研专题")

    # 精准替换新闻区域
    content = re.sub(
        r'<!--\s*NEWS_START\s*-->.*?<!--\s*NEWS_END\s*-->', 
        f'<!-- NEWS_START -->{news_body}<!-- NEWS_END -->', 
        content, 
        flags=re.DOTALL
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Daily news updated with multiple categories and BJ precision time: {sync_time_str}")

if __name__ == "__main__":
    a_items = fetch_feed("A股要闻")
    hk_items = fetch_feed("港股投研")
    update_markdown(a_items, hk_items)

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
            
            # 1. 提取分类信息 (category)
            category = entry.get('category')
            # 兼容处理：有些 RSS 源会将分类放在 tags 列表中
            if not category and 'tags' in entry and entry.tags:
                category = entry.tags[0].get('term')

            # 2. 尝试解析发布时间
            pub_time = "未知"
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                pub_time = time.strftime('%H:%M', entry.published_parsed)

            items.append({
                "title": title,
                "summary": summary,
                "pub_time": pub_time,
                "category": category
            })
        return items
    except Exception as e:
        print(f"抓取 {cfg['name']} 失败: {e}")
        return []

def update_markdown(a_news, hk_news):
    file_path = "docs/finance/daily-news.md"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # --- 1. 更新系统同步时间 (校准为北京时间 UTC+8) ---
    tz_beijing = timezone(timedelta(hours=8))
    now_beijing = datetime.now(tz_beijing)
    sync_time_str = now_beijing.strftime("%Y-%m-%d %H:%M:%S")
    
    time_html = f'<p align="right">\n  <Badge type="tip" text="最后同步: {sync_time_str}" />\n</p>'
    
    if "<!-- UPDATE_TIME -->" in content:
        parts = content.split("<!-- UPDATE_TIME -->")
        suffix = parts[1].split("<!--", 1)
        if len(suffix) > 1:
            content = parts[0] + "<!-- UPDATE_TIME -->\n" + time_html + "\n\n<!--" + suffix[1]
        else:
            content = parts[0] + "<!-- UPDATE_TIME -->\n" + time_html

    # --- 2. 更新新闻内容 ---
    news_body = "\n"
    
    # A股区
    news_body += "### 🔴 A股 & 宏观要闻\n"
    if a_news:
        for item in a_news:
            # 如果有分类，则增加 Badge 徽章
            category_badge = f' <Badge type="info" text="{item["category"]}" />' if item.get('category') else ""
            news_body += f"- **[{item['pub_time']}] {item['title']}**{category_badge}\n  {item['summary']}\n\n"
    else:
        news_body += "- 暂无实时要闻更新\n\n"

    # 港股区
    news_body += "### 🇭🇰 港股投研专题\n"
    if hk_news:
        for item in hk_news:
            category_badge = f' <Badge type="info" text="{item["category"]}" />' if item.get('category') else ""
            brief = (item['summary'][:300] + '...') if len(item['summary']) > 300 else item['summary']
            news_body += f"- **[{item['pub_time']}] {item['title']}**{category_badge}\n  _{brief}_\n\n"
    else:
        news_body += "- 暂无港股动态更新\n"

    if "<!-- NEWS_START -->" in content and "<!-- NEWS_END -->" in content:
        parts = content.split("<!-- NEWS_START -->")
        suffix = parts[1].split("<!-- NEWS_END -->")
        content = parts[0] + "<!-- NEWS_START -->" + news_body + "<!-- NEWS_END -->" + suffix[1]

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Finance Brief updated with Category Badges. Beijing Time: {sync_time_str}")

if __name__ == "__main__":
    a_items = fetch_feed("A股要闻")
    hk_items = fetch_feed("港股投研")
    update_markdown(a_items, hk_items)

import feedparser
import os
import re
from datetime import datetime
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
            
            # 尝试解析发布时间，如果失败则用当前时间
            pub_time = "未知"
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                # 转换为北京时间（简单加 8 小时，或根据实际偏移）
                # 这里使用 time.strftime 格式化 RSS 原始时间
                pub_time = time.strftime('%H:%M', entry.published_parsed)

            items.append({
                "title": title,
                "summary": summary,
                "pub_time": pub_time
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

    # --- 1. 更新系统同步时间 (Action 运行时间) ---
    # 这代表了系统最后一次成功执行任务的时间点
    sync_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_html = f'<p align="right">\n  <Badge type="tip" text="最后同步: {sync_time_str}" />\n</p>'
    
    if "<!-- UPDATE_TIME -->" in content:
        parts = content.split("<!-- UPDATE_TIME -->")
        suffix = parts[1].split("<!--", 1)
        if len(suffix) > 1:
            content = parts[0] + "<!-- UPDATE_TIME -->\n" + time_html + "\n\n<!--" + suffix[1]
        else:
            content = parts[0] + "<!-- UPDATE_TIME -->\n" + time_html

    # --- 2. 更新数据来源说明 ---
    source_names = [cfg['name'] for cfg in CONFIG.values()]
    source_info = f"::: details 🛰️ 数据来源说明\n本页面资讯由自动化脚本从以下渠道抓取：**{', '.join(source_names)}**。\n:::\n"
    if "<!-- SOURCE_INFO -->" in content:
        parts = content.split("<!-- SOURCE_INFO -->")
        suffix = parts[1].split("---", 1)
        if len(suffix) > 1:
            content = parts[0] + "<!-- SOURCE_INFO -->\n" + source_info + "\n---" + suffix[1]
        else:
            content = parts[0] + "<!-- SOURCE_INFO -->\n" + source_info

    # --- 3. 更新新闻内容 ---
    news_body = "\n"
    
    # A股区
    news_body += "### 🔴 A股 & 宏观要闻\n"
    if a_news:
        for item in a_news:
            # 格式：[14:30] 标题
            news_body += f"- **[{item['pub_time']}] {item['title']}**\n  {item['summary']}\n\n"
    else:
        news_body += "- 暂无实时要闻更新\n\n"

    # 港股区
    news_body += "### 🇭🇰 港股投研专题\n"
    if hk_news:
        for item in hk_news:
            brief = (item['summary'][:300] + '...') if len(item['summary']) > 300 else item['summary']
            news_body += f"- **[{item['pub_time']}] {item['title']}**\n  _{brief}_\n\n"
    else:
        news_body += "- 暂无港股动态更新\n"

    if "<!-- NEWS_START -->" in content and "<!-- NEWS_END -->" in content:
        parts = content.split("<!-- NEWS_START -->")
        suffix = parts[1].split("<!-- NEWS_END -->")
        content = parts[0] + "<!-- NEWS_START -->" + news_body + "<!-- NEWS_END -->" + suffix[1]

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Finance Brief updated. Sync time: {sync_time_str}")

if __name__ == "__main__":
    a_items = fetch_feed("A股要闻")
    hk_items = fetch_feed("港股投研")
    update_markdown(a_items, hk_items)

import feedparser
import os
import re
from datetime import datetime

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
            items.append({
                "title": title,
                "summary": summary
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

    # --- 1. 更新高精度时间 ---
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_html = f'<p align="right">\n  <Badge type="tip" text="最后同步: {now_str}" />\n</p>'
    # 仅在标记后紧跟的内容进行替换，避免跨行误删
    if "<!-- UPDATE_TIME -->" in content:
        # 寻找标记后的第一个空行或下一个标记
        parts = content.split("<!-- UPDATE_TIME -->")
        # 重新构造：[前缀] + 标记 + [新时间内容] + [后缀(去掉旧的时间内容)]
        suffix = parts[1].split("<!--", 1) # 寻找下一个任何 HTML 标记
        if len(suffix) > 1:
            content = parts[0] + "<!-- UPDATE_TIME -->\n" + time_html + "\n\n<!--" + suffix[1]
        else:
            # 如果后面没有其他标记，则直接替换
            content = parts[0] + "<!-- UPDATE_TIME -->\n" + time_html

    # --- 2. 更新数据来源说明 ---
    source_names = [cfg['name'] for cfg in CONFIG.values()]
    source_info = f"::: details 🛰️ 数据来源说明\n本页面资讯由自动化脚本从以下渠道抓取：**{', '.join(source_names)}**。\n:::\n"
    if "<!-- SOURCE_INFO -->" in content:
        parts = content.split("<!-- SOURCE_INFO -->")
        # 寻找之后第一个 --- 或下一个标记
        suffix = parts[1].split("---", 1)
        if len(suffix) > 1:
            content = parts[0] + "<!-- SOURCE_INFO -->\n" + source_info + "\n---" + suffix[1]
        else:
            content = parts[0] + "<!-- SOURCE_INFO -->\n" + source_info

    # --- 3. 更新新闻内容 ---
    news_body = "\n"
    news_body += "### 🔴 A股 & 宏观要闻\n"
    if a_news:
        for item in a_news:
            news_body += f"- **{item['title']}**\n  {item['summary']}\n\n"
    else:
        news_body += "- 暂无实时要闻更新\n\n"

    news_body += "### 🇭🇰 港股投研专题\n"
    if hk_news:
        for item in hk_news:
            brief = (item['summary'][:300] + '...') if len(item['summary']) > 300 else item['summary']
            news_body += f"- **{item['title']}**\n  _{brief}_\n\n"
    else:
        news_body += "- 暂无港股动态更新\n"

    if "<!-- NEWS_START -->" in content and "<!-- NEWS_END -->" in content:
        parts = content.split("<!-- NEWS_START -->")
        suffix = parts[1].split("<!-- NEWS_END -->")
        content = parts[0] + "<!-- NEWS_START -->" + news_body + "<!-- NEWS_END -->" + suffix[1]

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Daily news updated with precision time: {now_str}")

if __name__ == "__main__":
    a_items = fetch_feed("A股要闻")
    hk_items = fetch_feed("港股投研")
    update_markdown(a_items, hk_items)

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
    if not text:
        return ""
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"')
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'^【.*?】', '', text)
    return text.strip()

def fetch_feed(source_key):
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
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # --- 1. 更新高精度时间 (保留标记) ---
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_html = f'<!-- UPDATE_TIME -->\n<p align="right">\n  <Badge type="tip" text="最后同步: {now_str}" />\n</p>'
    content = re.sub(r'<!-- UPDATE_TIME -->.*?(?=<p align="right">|$)', time_html, content, flags=re.DOTALL)
    # 如果没找到复杂结构，简单替换
    if '最后同步:' not in content and '<!-- UPDATE_TIME -->' in content:
        content = content.replace('<!-- UPDATE_TIME -->', time_html)

    # --- 2. 更新数据来源说明 (保留标记) ---
    source_names = [cfg['name'] for cfg in CONFIG.values()]
    source_info = f"<!-- SOURCE_INFO -->\n::: details 🛰️ 数据来源说明\n本页面资讯由自动化脚本从以下渠道抓取：**{', '.join(source_names)}**。\n:::\n"
    content = re.sub(r'<!-- SOURCE_INFO -->.*?:::\n', source_info, content, flags=re.DOTALL)

    # --- 3. 更新新闻内容 ---
    news_content = "<!-- NEWS_START -->\n"
    news_content += "### 🔴 A股 & 宏观要闻\n"
    if a_news:
        for item in a_news:
            news_content += f"- **{item['title']}**\n  {item['summary']}\n\n"
    else:
        news_content += "- 暂无实时要闻更新\n\n"

    news_content += "### 🇭🇰 港股投研专题\n"
    if hk_news:
        for item in hk_news:
            brief = (item['summary'][:300] + '...') if len(item['summary']) > 300 else item['summary']
            news_content += f"- **{item['title']}**\n  _{brief}_\n\n"
    else:
        news_content += "- 暂无港股动态更新\n"
    news_content += "<!-- NEWS_END -->"

    pattern_news = re.compile(r'<!-- NEWS_START -->.*?<!-- NEWS_END -->', re.DOTALL)
    new_page_content = pattern_news.sub(news_content, content)

    # 兜底更新（如果标记被意外删除）
    new_page_content = re.sub(r'最后同步: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', f'最后同步: {now_str}', new_page_content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_page_content)
    print(f"Daily news updated with precision time: {now_str}")

if __name__ == "__main__":
    a_items = fetch_feed("A股要闻")
    hk_items = fetch_feed("港股投研")
    update_markdown(a_items, hk_items)

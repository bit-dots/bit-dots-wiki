import feedparser
import os
import re
from datetime import datetime

# 数据源配置，便于脚本和页面同步
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
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # --- 1. 自动生成高精度更新时间 ---
    # 精确到秒：YYYY-MM-DD HH:MM:SS
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_html = f'<p align="right">\n  <Badge type="tip" text="最后同步: {now_str}" />\n</p>\n'
    
    # 替换时间标记
    content = re.compile(r'<!-- UPDATE_TIME -->').sub(time_html, content)

    # --- 2. 自动生成数据来源说明 ---
    source_names = [cfg['name'] for cfg in CONFIG.values()]
    source_info = f"\n::: details 🛰️ 数据来源说明\n本页面资讯由自动化脚本从以下渠道抓取：**{', '.join(source_names)}**。\n:::\n"
    
    # 替换来源标记
    content = re.compile(r'<!-- SOURCE_INFO -->').sub(source_info, content)

    # --- 3. 构建内容区块 ---
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

    # --- 替换新闻内容 ---
    pattern_news = re.compile(r'<!-- NEWS_START -->.*?<!-- NEWS_END -->', re.DOTALL)
    new_page_content = pattern_news.sub(news_content, content)

    # 最后的安全清理：如果 Markdown 里的时间徽章没有被标记替换，进行兜底正则更新
    # (这一步是为了兼容你之前手动写死的部分)
    new_page_content = re.sub(r'最后更新: \d{4}-\d{2}-\d{2}.*?"', f'最后同步: {now_str}"', new_page_content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_page_content)
    print(f"Daily news updated with precision time: {now_str}")

if __name__ == "__main__":
    a_items = fetch_feed("A股要闻")
    hk_items = fetch_feed("港股投研")
    update_markdown(a_items, hk_items)

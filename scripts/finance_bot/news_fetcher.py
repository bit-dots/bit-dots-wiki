import feedparser
import os
import re
from datetime import datetime

# 财联社与华尔街见闻的 RSS 源 (利用 RSSHub 镜像)
RSS_FEEDS = [
    {"name": "财联社", "url": "https://rsshub.app/cls/telegraph"},
    {"name": "华尔街见闻", "url": "https://rsshub.app/wallstreetcn/live/global"},
]

def clean_text(text):
    """清除 HTML 标签并处理特殊字符"""
    if not text:
        return ""
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"')
    # 移除 RSS 可能带有的【xxx】前缀或广告
    text = re.sub(r'^\s*【.*?】', '', text)
    return text.strip()

def fetch_finance_news():
    news_items = []
    for feed in RSS_FEEDS:
        try:
            print(f"Fetching from {feed['name']}...")
            d = feedparser.parse(feed["url"])
            
            # 每源取前 3 条
            for entry in d.entries[:3]:
                # 优先取摘要，没有则取标题
                raw_content = entry.get('summary') or entry.get('title', '')
                content = clean_text(raw_content)
                
                # 限制长度，保持看板整洁
                display_content = (content[:120] + '...') if len(content) > 120 else content
                    
                news_items.append({
                    "source": feed["name"],
                    "content": display_content,
                    "date": datetime.now().strftime("%H:%M")
                })
        except Exception as e:
            print(f"Error fetching {feed['name']}: {e}")
    
    return news_items

def update_markdown(news_items):
    file_path = "docs/finance/index.md"
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    start_index = -1
    end_index = -1
    for i, line in enumerate(lines):
        if "## 🕒 今日简讯" in line:
            start_index = i + 1
        elif start_index != -1 and line.startswith("---"):
            end_index = i
            break

    if start_index != -1 and end_index != -1:
        # 构建新的内容块
        new_content = ["\n", "::: info 实时快讯 (财联社 & 华尔街见闻)\n"]
        for item in news_items:
            # 格式：- [来源 14:30] 内容
            new_content.append(f"- **[{item['source']} {item['date']}]** {item['content']}\n\n")
        new_content.append(":::\n")

        # 检查内容是否有变化，避免无意义的提交
        # (简化处理：始终更新，因为时间戳会变)
        lines[start_index:end_index] = new_content

        # 更新最后更新时间徽章
        for i, line in enumerate(lines):
            if "最后更新:" in line:
                lines[i] = f'  <Badge type="tip" text="最后更新: {datetime.now().strftime("%Y-%m-%d %H:%M")}" />\n'
                break

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print("Successfully updated finance index.md with RSS news")

if __name__ == "__main__":
    items = fetch_finance_news()
    if items:
        update_markdown(items)
    else:
        print("No items fetched.")

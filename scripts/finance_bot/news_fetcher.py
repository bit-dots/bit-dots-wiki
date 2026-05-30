import feedparser
import os
from datetime import datetime

# 推荐的 RSS 源列表（可以根据需要增加）
RSS_FEEDS = [
    {"name": "Caixin Global", "url": "https://www.caixinglobal.com/rss/economy/"},
    {"name": "SCMP China", "url": "https://www.scmp.com/rss/91/feed"},
    {"name": "Wall Street CN", "url": "https://rsshub.app/wallstreetcn/live/global"}, # 示例，可能需要可用代理或源
]

def fetch_finance_news():
    news_items = []
    for feed in RSS_FEEDS:
        try:
            d = feedparser.parse(feed["url"])
            # 只取前 3 条
            for entry in d.entries[:3]:
                news_items.append({
                    "source": feed["name"],
                    "title": entry.title,
                    "link": entry.link,
                    "date": datetime.now().strftime("%Y-%m-%d")
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

    # 寻找 ## 🕒 今日简讯 (Today's Brief) 的位置
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
        new_content = ["::: info 自动抓取热点\n"]
        for item in news_items:
            new_content.append(f"- **[{item['source']}]** [{item['title']}]({item['link']}) ({item['date']})\n")
        new_content.append(":::\n")

        # 替换旧内容
        lines[start_index:end_index] = new_content

        # 更新最后更新时间
        for i, line in enumerate(lines):
            if "最后更新:" in line:
                lines[i] = f'  <Badge type="tip" text="最后更新: {datetime.now().strftime("%Y-%m-%d")}" />\n'
                break

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print("Successfully updated finance index.md")

if __name__ == "__main__":
    items = fetch_finance_news()
    if items:
        update_markdown(items)
    else:
        print("No news items found.")

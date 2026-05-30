import akshare as ak
import os
from datetime import datetime

def fetch_finance_news():
    news_items = []
    try:
        # 使用 AkShare 获取金十数据实时资讯
        # indicator="最新资讯" 获取最近 4 小时的快讯
        news_df = ak.js_news(indicator="最新资讯")
        
        # 只取前 5 条，并转换为列表
        # 金十数据返回的列通常包含 'datetime', 'content'
        count = 0
        for index, row in news_df.iterrows():
            if count >= 5: break
            
            # 清理内容，去除 HTML 标签（如果有）
            content = row['content'].replace('<br/>', ' ').strip()
            # 截断过长的内容
            if len(content) > 200:
                content = content[:197] + "..."
                
            news_items.append({
                "source": "金十数据",
                "title": content,
                "link": "https://www.jin10.com/", # 金十快讯通常没有单条链接
                "date": row['datetime'].strftime("%H:%M")
            })
            count += 1
            
    except Exception as e:
        print(f"Error fetching from AkShare: {e}")
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
        new_content = ["::: info 实时快讯 (由 AkShare 驱动)\n"]
        for item in news_items:
            # 格式：- [时间] 内容
            new_content.append(f"- **[{item['date']}]** {item['title']}\n")
        new_content.append(":::\n")

        # 替换旧内容
        lines[start_index:end_index] = new_content

        # 更新最后更新时间
        for i, line in enumerate(lines):
            if "最后更新:" in line:
                lines[i] = f'  <Badge type="tip" text="最后更新: {datetime.now().strftime("%Y-%m-%d %H:%M")}" />\n'
                break

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print("Successfully updated finance index.md with AkShare data")

if __name__ == "__main__":
    items = fetch_finance_news()
    if items:
        update_markdown(items)
    else:
        print("No news items found.")

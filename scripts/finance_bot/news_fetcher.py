import akshare as ak
import os
import re
from datetime import datetime

def clean_text(text):
    """彻底清除 HTML 标签并处理特殊字符"""
    if not text:
        return ""
    # 移除 HTML 标签
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    # 处理常见 HTML 实体
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"')
    # 移除多余换行和空格
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def fetch_finance_news():
    news_items = []
    try:
        print("Fetching news from AkShare...")
        # 获取最新资讯
        news_df = ak.js_news(indicator="最新资讯")
        
        if news_df.empty:
            print("No news found.")
            return []

        count = 0
        for index, row in news_df.iterrows():
            if count >= 5: break
            
            raw_content = row['content']
            content = clean_text(raw_content)
            
            # 限制长度，保持看板整洁
            display_content = (content[:100] + '...') if len(content) > 100 else content
                
            news_items.append({
                "time": row['datetime'].strftime("%H:%M"),
                "content": display_content
            })
            count += 1
        print(f"Successfully fetched {len(news_items)} items.")
    except Exception as e:
        print(f"Error fetching from AkShare: {e}")
    return news_items

def update_markdown(news_items):
    file_path = "docs/finance/index.md"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
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
        new_content = ["\n", "::: info 实时快讯 (由 AkShare 驱动)\n"]
        for item in news_items:
            # 增加双换行，确保 Markdown 列表正确渲染
            new_content.append(f"- **[{item['time']}]** {item['content']}\n\n")
        new_content.append(":::\n")

        # 替换旧内容
        lines[start_index:end_index] = new_content

        # 更新最后更新时间
        for i, line in enumerate(lines):
            if "最后更新:" in line:
                # 包含日期和具体时间
                lines[i] = f'  <Badge type="tip" text="最后更新: {datetime.now().strftime("%Y-%m-%d %H:%M")}" />\n'
                break

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print("Successfully updated docs/finance/index.md")
    else:
        print("Could not find appropriate markers in Markdown file to update.")

if __name__ == "__main__":
    items = fetch_finance_news()
    if items:
        update_markdown(items)
    else:
        print("No items to update.")

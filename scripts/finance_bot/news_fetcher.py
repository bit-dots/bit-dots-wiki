import akshare as ak
import os
import re
import pandas as pd
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
    # 移除财联社电报开头常见的【xxx】
    text = re.sub(r'^【.*?】', '', text)
    return text.strip()

def fetch_finance_news():
    news_items = []
    
    # 直接抓取财联社电报 (AkShare 原生接口)
    try:
        print("正在通过 AkShare 抓取财联社电报 (Cailianshe)...")
        cls_df = ak.stock_telegraph_cls()
        
        if cls_df.empty:
            print("未能获取到财联社数据。")
            return []

        # 取最新的 5 条
        for _, row in cls_df.head(5).iterrows():
            content = clean_text(row['content'])
            # 限制长度，保持看板整洁
            display_content = (content[:120] + '...') if len(content) > 120 else content
            news_items.append({
                "source": "财联社",
                "content": display_content,
                "time": row['datetime'].strftime("%H:%M")
            })
        print(f"成功获取 {len(news_items)} 条财联社快讯。")
    except Exception as e:
        print(f"抓取财联社失败: {e}")

    # 作为备选补充，抓取金十快讯
    if len(news_items) < 3:
        try:
            print("尝试抓取全球快讯 (via js_news)...")
            news_df = ak.js_news(indicator="最新资讯")
            for _, row in news_df.head(2).iterrows():
                content = clean_text(row['content'])
                display_content = (content[:120] + '...') if len(content) > 120 else content
                news_items.append({
                    "source": "全球快讯",
                    "content": display_content,
                    "time": row['datetime'].strftime("%H:%M")
                })
        except Exception as e:
            print(f"抓取全球快讯失败: {e}")
    
    return news_items

def update_markdown(news_items):
    file_path = "docs/finance/index.md"
    if not os.path.exists(file_path):
        print(f"未找到文件: {file_path}")
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
        # 构建新内容
        new_content = ["\n", "::: info 实时快讯 (由 AkShare 驱动)\n"]
        for item in news_items:
            new_content.append(f"- **[{item['source']} {item['time']}]** {item['content']}\n\n")
        new_content.append(":::\n")

        lines[start_index:end_index] = new_content

        # 更新更新时间徽章
        for i, line in enumerate(lines):
            if "最后更新:" in line:
                lines[i] = f'  <Badge type="tip" text="最后更新: {datetime.now().strftime("%Y-%m-%d %H:%M")}" />\n'
                break

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"成功更新 {file_path}")
    else:
        print("未能在 Markdown 文件中找到定位标记。")

if __name__ == "__main__":
    items = fetch_finance_news()
    if items:
        update_markdown(items)
    else:
        print("没有可更新的内容。")

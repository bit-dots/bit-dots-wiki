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
    
    # 1. 抓取财联社电报 (最新接口名为 stock_info_global_cls)
    try:
        print("正在尝试抓取财联社电报 (CLS)...")
        # 尝试多个可能的接口名以保证兼容性
        cls_df = pd.DataFrame()
        if hasattr(ak, 'stock_info_global_cls'):
            cls_df = ak.stock_info_global_cls(symbol="全部")
        elif hasattr(ak, 'stock_telegraph_cls'):
            cls_df = ak.stock_telegraph_cls()
        
        if not cls_df.empty:
            # 财联社新版接口列名可能是 '标题', '内容', '发布时间'
            content_col = '内容' if '内容' in cls_df.columns else 'content'
            time_col = '发布时间' if '发布时间' in cls_df.columns else 'datetime'
            
            for _, row in cls_df.head(5).iterrows():
                content = clean_text(row[content_col])
                display_content = (content[:120] + '...') if len(content) > 120 else content
                
                # 处理时间格式
                raw_time = row[time_col]
                if isinstance(raw_time, str):
                    time_str = raw_time[-5:] # 取 HH:MM
                else:
                    time_str = raw_time.strftime("%H:%M")

                news_items.append({
                    "source": "财联社",
                    "content": display_content,
                    "time": time_str
                })
            print(f"成功获取 {len(news_items)} 条财联社快讯。")
    except Exception as e:
        print(f"抓取财联社失败: {e}")

    # 2. 如果财联社失败，尝试抓取金十快讯 (js_news) 或百度经济日历
    if len(news_items) < 3:
        try:
            print("尝试抓取全球快讯作为补充...")
            news_df = pd.DataFrame()
            if hasattr(ak, 'js_news'):
                news_df = ak.js_news()
            elif hasattr(ak, 'news_economic_baidu'):
                # 百度日历作为最后的兜底
                news_df = ak.news_economic_baidu()
                news_df.rename(columns={'事件': 'content', '时间': 'datetime'}, inplace=True)
            
            if not news_df.empty:
                for _, row in news_df.head(3).iterrows():
                    content = clean_text(row.get('content', row.get('事件', '')))
                    if not content: continue
                    
                    display_content = (content[:120] + '...') if len(content) > 120 else content
                    
                    # 时间处理
                    raw_datetime = row.get('datetime', row.get('时间', datetime.now()))
                    time_str = raw_datetime if isinstance(raw_datetime, str) else raw_datetime.strftime("%H:%M")

                    news_items.append({
                        "source": "全球快讯",
                        "content": display_content,
                        "time": time_str
                    })
                print("成功补充全球快讯数据。")
        except Exception as e:
            print(f"备选方案抓取失败: {e}")
    
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
        new_content = ["\n", "::: info 实时快讯 (由 AkShare 驱动)\n"]
        for item in news_items:
            new_content.append(f"- **[{item['source']} {item['time']}]** {item['content']}\n\n")
        new_content.append(":::\n")

        lines[start_index:end_index] = new_content

        # 更新更新时间徽标
        for i, line in enumerate(lines):
            if "最后更新:" in line:
                lines[i] = f'  <Badge type="tip" text="最后更新: {datetime.now().strftime("%Y-%m-%d %H:%M")}" />\n'
                break

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"成功更新 {file_path}")

if __name__ == "__main__":
    items = fetch_finance_news()
    if items:
        update_markdown(items)
    else:
        print("没有可更新的内容。")

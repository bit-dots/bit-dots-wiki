import feedparser
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
    # 移除类似【xxx】的前缀
    text = re.sub(r'^【.*?】', '', text)
    return text.strip()

def fetch_feed(name, url, limit=5):
    """通用 RSS 抓取函数"""
    print(f"正在抓取 {name}: {url}")
    try:
        d = feedparser.parse(url)
        items = []
        for entry in d.entries[:limit]:
            title = entry.get('title', '无标题')
            summary = clean_text(entry.get('summary') or entry.get('description', ''))
            items.append({
                "title": title,
                "summary": summary,
                "time": datetime.now().strftime("%H:%M") # RSS 通常时间格式复杂，这里记录抓取时间或尝试解析
            })
        return items
    except Exception as e:
        print(f"抓取 {name} 失败: {e}")
        return []

def update_markdown(red_news, hk_news):
    file_path = "docs/finance/index.md"
    if not os.path.exists(file_path):
        print(f"未找到文件: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # --- 构建新内容区块 ---
    brief_content = "## 🕒 今日简讯 (Today's Brief)\n\n"
    
    # 1. 核心要闻区 (红色警告风格)
    brief_content += "::: danger 🔴 核心要闻 (财联社加红)\n"
    if red_news:
        for item in red_news:
            brief_content += f"- **{item['title']}**\n  {item['summary']}\n\n"
    else:
        brief_content += "- 暂无重磅要闻更新\n"
    brief_content += ":::\n\n"

    # 2. 港股投研区 (专业提示风格)
    brief_content += "::: tip 🇭🇰 港股投研专题 (新时空)\n"
    if hk_news:
        for item in hk_news:
            brief_content += f"- **{item['title']}**\n  _{item['summary']}_\n\n"
    else:
        brief_content += "- 暂无港股动态更新\n"
    brief_content += ":::\n"

    # --- 正则替换 ---
    # 匹配 ## 🕒 今日简讯 到下一个 ## 📊 市场脉搏 之间的部分
    pattern = re.compile(r'## 🕒 今日简讯.*?## 📊 市场脉搏', re.DOTALL)
    new_page_content = pattern.sub(brief_content + "\n## 📊 市场脉搏", content)

    # 更新最后更新时间徽章
    new_page_content = re.sub(r'最后更新: \d{4}-\d{2}-\d{2}.*?"', f'last_updated_at_marker"', new_page_content) # 先标记
    new_page_content = new_page_content.replace('last_updated_at_marker"', f'最后更新: {datetime.now().strftime("%Y-%m-%d %H:%M")}"')

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_page_content)
    print("Finance dashboard successfully updated with Dual-Section layout.")

if __name__ == "__main__":
    # 1. 抓取财联社加红要闻
    red_items = fetch_feed("财联社加红", "https://rsshub.rssforever.com/cls/telegraph/red", limit=3)
    
    # 2. 抓取新时空港股财经
    hk_items = fetch_feed("港股投研", "https://www.newtimespace.com/feed/rss_template.xml?id=100000&site=rss&lang=zh-cn", limit=5)
    
    # 3. 更新看板
    update_markdown(red_items, hk_items)

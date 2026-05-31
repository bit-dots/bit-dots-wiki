import requests
import feedparser
import re
import time

def clean_text(text):
    if not text:
        return ""
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"')
    return text.strip()

def test_mirror_rss():
    rss_url = "https://rsshub.rssforever.com/cls/telegraph/red"
    
    print(f"🕵️ 正在测试 RSSHub 镜像源 (Red): {rss_url}")
    try:
        # 使用镜像源通常没那么严格，但也建议带上简单的 UA
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(rss_url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ 抓取失败。状态码: {response.status_code}")
            return

        d = feedparser.parse(response.text)
        
        if not d.entries:
            print("❌ 镜像源解析结果为空。")
            return

        print(f"✅ 镜像源抓取成功！获取到 {len(d.entries)} 条实时提醒：\n")
        
        for i, entry in enumerate(d.entries[:5]):
            title = entry.get('title', '无标题')
            summary = clean_text(entry.get('summary') or entry.get('description', ''))
            print(f"{i+1}. {title}")
            print(f"   内容: {summary[:120]}...\n")

    except Exception as e:
        print(f"🔥 运行过程发生异常: {e}")

if __name__ == "__main__":
    test_mirror_rss()

#!/usr/bin/env python3
"""
NewsSnapper — CLI News Aggregator
Fetches headlines from Hacker News, Reddit, TechCrunch RSS.
Free version: 3 sources, CLI only.
Premium: 15+ sources, Telegram alerts, CSV export.
"""

import json
import sys
import textwrap
from datetime import datetime
from urllib.request import urlopen, Request
from xml.etree import ElementTree as ET

VERSION = "1.0.0"
SOURCES = {
    "hn": {
        "name": "Hacker News",
        "url": "https://hacker-news.firebaseio.com/v0/topstories.json",
        "type": "api",
        "limit": 10
    },
    "reddit": {
        "name": "Reddit r/programming",
        "url": "https://www.reddit.com/r/programming/hot.json?limit=10",
        "type": "json",
        "headers": {"User-Agent": "NewsSnapper/1.0"}
    },
    "techcrunch": {
        "name": "TechCrunch",
        "url": "https://techcrunch.com/feed/",
        "type": "rss"
    }
}

def fetch_json(url, headers=None):
    req = Request(url, headers=headers or {})
    with urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())

def fetch_rss(url):
    req = Request(url)
    with urlopen(req, timeout=15) as resp:
        return ET.fromstring(resp.read().decode())

def get_hn_stories():
    """Fetch top Hacker News stories."""
    ids = fetch_json(SOURCES["hn"]["url"])
    stories = []
    for sid in ids[:SOURCES["hn"]["limit"]]:
        try:
            item = fetch_json(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json")
            if item and item.get("title"):
                url = item.get("url", f"https://news.ycombinator.com/item?id={sid}")
                stories.append({
                    "title": item["title"],
                    "url": url,
                    "score": item.get("score", 0),
                    "source": "Hacker News"
                })
        except Exception:
            continue
    return stories

def get_reddit_stories():
    """Fetch top Reddit stories."""
    headers = SOURCES["reddit"]["headers"]
    data = fetch_json(SOURCES["reddit"]["url"], headers=headers)
    stories = []
    for post in data.get("data", {}).get("children", []):
        p = post.get("data", {})
        if p.get("title"):
            stories.append({
                "title": p["title"],
                "url": p.get("url", ""),
                "score": p.get("score", 0),
                "source": "Reddit r/programming"
            })
    return stories

def get_techcrunch_stories():
    """Fetch TechCrunch RSS headlines."""
    root = fetch_rss(SOURCES["techcrunch"]["url"])
    stories = []
    for item in root.findall(".//item")[:10]:
        title = item.findtext("title")
        link = item.findtext("link")
        if title:
            stories.append({
                "title": title,
                "url": link or "",
                "score": 0,
                "source": "TechCrunch"
            })
    return stories

def get_banner():
    return f"""
╔══════════════════════════════════════════════════╗
║        📰 NewsSnapper v{VERSION}                  ║
║     CLI News Aggregator — 3 Sources             ║
╚══════════════════════════════════════════════════╝
Time: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
"""

def print_stories(stories):
    if not stories:
        print("  ⚠ No stories found.")
        return
    for i, s in enumerate(stories, 1):
        print(f"  {i:2d}. {s['title']}")
        print(f"       🔗 {s['url'][:80]}")
        print(f"       📊 {s['source']} | {'⭐ ' + str(s['score']) if s['score'] else ''}")
        print()

def main():
    print(get_banner())
    
    for key in SOURCES:
        source = SOURCES[key]
        print(f"  📡 Fetching {source['name']}...")
        try:
            if key == "hn":
                stories = get_hn_stories()
            elif key == "reddit":
                stories = get_reddit_stories()
            elif key == "techcrunch":
                stories = get_techcrunch_stories()
            print(f"     ✅ Got {len(stories)} stories\n")
            print_stories(stories)
            print("  " + "─" * 50 + "\n")
        except Exception as e:
            print(f"     ❌ Error: {e}\n")
    
    print("  ──────────────────────────────────────────")
    print("  💡 Get the PREMIUM version for:")
    print("     15+ sources (Bloomberg, Reuters, CNBC, CoinDesk...)")
    print("     Telegram alerts for keywords you care about")
    print("     CSV / JSON export")
    print("     Scheduled daily digests")
    print()
    print("  👉 https://fargyy.gumroad.com/l/news-snapper")
    print("  👉 https://fargyy.gumroad.com")
    print()

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import re

def explore_site():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 1. Explore Home Page for Directory and URL Prefix
    home_url = "https://haokee-note.org/%E4%B8%BB%E9%A1%B5" # encoded "主页"
    print(f"Fetching Home Page: {home_url}")
    try:
        resp = requests.get(home_url, headers=headers)
        resp.raise_for_status()
        
        # DEBUG: Save HTML to file for inspection
        with open("home_debug.html", "w", encoding="utf-8") as f:
            f.write(resp.text)
        print("Saved home_debug.html")

        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Look for scripts that might contain data
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                if 'publish-01.obsidian.md' in script.string:
                    print("Found 'publish-01.obsidian.md' in a script tag!")
                    # print(script.string[:500]) # Print start of script
        
        # Look for the tree structure again, maybe different class
        # Obsidian Publish often uses .tree-item
        tree_items = soup.find_all(class_='tree-item')
        print(f"Found {len(tree_items)} tree items.")
        
        # Look for any links
        links = soup.find_all('a')
        print(f"Found {len(links)} total links.")

    except Exception as e:
        print(f"Error fetching home page: {e}")

    # 3. Explore Cache (Directory) and Content
    cache_url = "https://publish-01.obsidian.md/cache/7f880cb309be73ccd2d97c2223b38e09"
    print(f"\nFetching Cache (Directory): {cache_url}")
    try:
        resp = requests.get(cache_url, headers=headers)
        resp.raise_for_status()
        cache_data = resp.json()
        print(f"Cache keys: {list(cache_data.keys())[:5]}")
        # Save cache to inspect structure
        import json
        with open("cache_debug.json", "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
        print("Saved cache_debug.json")
    except Exception as e:
        print(f"Error fetching cache: {e}")

    # 4. Explore Content (Markdown?)
    # URL encoded "歌曲/纯爱战士祝睿融.md"
    content_url = "https://publish-01.obsidian.md/access/7f880cb309be73ccd2d97c2223b38e09/%E6%AD%8C%E6%9B%B2/%E7%BA%AF%E7%88%B1%E6%88%98%E5%A3%AB%E7%A5%9D%E7%9D%BF%E8%9E%8D.md"
    print(f"\nFetching Content: {content_url}")
    try:
        resp = requests.get(content_url, headers=headers)
        resp.raise_for_status()
        print("Content preview (first 500 chars):")
        print(resp.text[:500])
        with open("content_debug.md", "w", encoding="utf-8") as f:
            f.write(resp.text)
    except Exception as e:
        print(f"Error fetching content: {e}")

if __name__ == "__main__":
    explore_site()

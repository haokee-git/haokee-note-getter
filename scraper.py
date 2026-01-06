import requests
import json
import re
from urllib.parse import quote
from bs4 import BeautifulSoup

class HaokeeScraper:
    def __init__(self):
        self.base_url = "https://haokee-note.org/%E4%B8%BB%E9%A1%B5"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.site_info = None
        self.cache_data = None
        self.file_map = {} # Map filename to full path

    def get_site_info(self):
        """Fetches the home page and extracts siteInfo."""
        print(f"Fetching site info from {self.base_url}...")
        try:
            resp = requests.get(self.base_url, headers=self.headers)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Find script containing window.siteInfo
            for script in soup.find_all('script'):
                if script.string and 'window.siteInfo=' in script.string:
                    # Extract JSON object
                    match = re.search(r'window\.siteInfo=(.*?);', script.string)
                    if match:
                        json_str = match.group(1)
                        self.site_info = json.loads(json_str)
                        print(f"Site Info found: {self.site_info['uid']} @ {self.site_info['host']}")
                        return self.site_info
            
            raise ValueError("Could not find window.siteInfo in home page")
            
        except Exception as e:
            print(f"Error getting site info: {e}")
            raise

    def get_directory(self):
        """Fetches the directory structure (cache)."""
        if not self.site_info:
            self.get_site_info()
            
        uid = self.site_info['uid']
        host = self.site_info['host']
        cache_url = f"https://{host}/cache/{uid}"
        
        print(f"Fetching directory from {cache_url}...")
        try:
            resp = requests.get(cache_url, headers=self.headers)
            resp.raise_for_status()
            self.cache_data = resp.json()
            
            # Build file map for easier lookup (filename -> full path)
            self.file_map = {}
            for full_path in self.cache_data.keys():
                filename = full_path.split('/')[-1]
                # If duplicates exist, this simplistic map might overwrite, 
                # but usually media files have unique names or we can handle it better if needed.
                self.file_map[filename] = full_path
                
            return self.cache_data
        except Exception as e:
            print(f"Error fetching directory: {e}")
            raise

    def get_page_content(self, path):
        """Fetches the markdown content of a page."""
        if not self.site_info:
            self.get_site_info()
            
        uid = self.site_info['uid']
        host = self.site_info['host']
        
        # Path needs to be URL encoded
        # split by / and encode each part to be safe, or just quote the whole thing?
        # Requests usually handles some encoding, but the URL format is specific.
        # Example: .../access/uid/%E6%AD%8C%E6%9B%B2/%E7%BA%AF...md
        
        encoded_path = quote(path)
        # However, slash should not be encoded if it separates folders
        encoded_path = "/".join([quote(part) for part in path.split('/')])
        
        content_url = f"https://{host}/access/{uid}/{encoded_path}"
        
        print(f"Fetching content from {content_url}...")
        try:
            resp = requests.get(content_url, headers=self.headers)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            print(f"Error fetching content: {e}")
            return None

    def extract_media(self, content):
        """Parses markdown content and extracts media URLs."""
        if not content:
            return []
            
        media_files = []
        
        # Regex for Obsidian Wiki Links: ![[filename.ext]]
        wiki_links = re.findall(r'!\[\[(.*?)\]\]', content)
        for link in wiki_links:
            # Link might have pipe for alt text: ![[filename.png|alt]]
            filename = link.split('|')[0]
            full_path = self.resolve_path(filename)
            if full_path:
                media_files.append({
                    'name': filename,
                    'path': full_path,
                    'url': self.construct_url(full_path),
                    'type': self.get_file_type(filename)
                })

        # Regex for Standard Markdown: ![alt](filename.ext)
        md_links = re.findall(r'!\[.*?\]\((.*?)\)', content)
        for link in md_links:
            # Link might be a full URL or relative path
            if link.startswith('http'):
                # External image, maybe skip or include? 
                # User asked for "media files ... in the folder", implying hosted ones.
                # But let's include them if they seem relevant.
                # For now, focus on internal ones.
                pass
            else:
                # Relative path or filename
                # If it has encoded chars, unquote it
                from urllib.parse import unquote
                filename = unquote(link.split('/')[-1])
                full_path = self.resolve_path(filename)
                if full_path:
                    media_files.append({
                        'name': filename,
                        'path': full_path,
                        'url': self.construct_url(full_path),
                        'type': self.get_file_type(filename)
                    })
                    
        return media_files

    def resolve_path(self, filename):
        """Finds the full path in cache for a given filename."""
        # Check exact match first
        if filename in self.cache_data:
            return filename
            
        # Check file map
        if filename in self.file_map:
            return self.file_map[filename]
            
        return None

    def construct_url(self, full_path):
        uid = self.site_info['uid']
        host = self.site_info['host']
        encoded_path = "/".join([quote(part) for part in full_path.split('/')])
        return f"https://{host}/access/{uid}/{encoded_path}"

    def get_file_type(self, filename):
        ext = filename.split('.')[-1].lower()
        if ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg']:
            return 'image'
        elif ext in ['mp3', 'wav', 'ogg', 'm4a']:
            return 'audio'
        elif ext in ['mp4', 'webm', 'mov']:
            return 'video'
        return 'unknown'

if __name__ == "__main__":
    # Test
    scraper = HaokeeScraper()
    scraper.get_directory()
    print("Directory fetched.")
    content = scraper.get_page_content("歌曲/纯爱战士祝睿融.md")
    if content:
        media = scraper.extract_media(content)
        print("Found media:")
        for m in media:
            print(m)

import os
import urllib.request
import re
import html
from urllib.parse import urlparse

src_js_dir = r"C:\Users\surya\Documents\antigravity\keen-pythagoras\downloaded_assets\framerusercontent.com\sites\3r1Xu4DXLtC5PUnDU2zspB"
assets_dir = r"C:\Users\surya\Documents\antigravity\keen-pythagoras\downloaded_assets"

def download_file(file_url, dest_path):
    try:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = urllib.request.Request(file_url, headers=headers)
        with urllib.request.urlopen(req) as response, open(dest_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Downloaded: {file_url} -> {dest_path}")
    except Exception as e:
        print(f"Failed to download {file_url}: {e}")

def main():
    if not os.path.exists(src_js_dir):
        print("Source JS directory does not exist!")
        return
        
    all_asset_urls = set()
    
    # Scan all JS/MJS files for URLs
    for root, _, files in os.walk(src_js_dir):
        for f in files:
            if f.endswith(('.mjs', '.js')):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as file_obj:
                        content = file_obj.read()
                        
                    # Find all URLs
                    urls = re.findall(r'https?://[^\s"\'>]+', content)
                    for u in urls:
                        u = html.unescape(u)
                        # Clean up URL (remove trailing slashes, backslashes, quotes, closing parenthesis, etc.)
                        u = u.split('\\')[0].split('"')[0].split("'")[0].split(')')[0].split(']')[0]
                        if any(ext in u.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.mp4', '.webm', '.woff2', '.woff', '.ttf']):
                            all_asset_urls.add(u)
                except Exception as e:
                    print(f"Error reading {path}: {e}")

    print(f"Found {len(all_asset_urls)} unique asset URLs in JS files.")
    
    # Download them
    for a_url in sorted(all_asset_urls):
        parsed = urlparse(a_url)
        clean_path = parsed.path.lstrip('/')
        local_path = os.path.join(assets_dir, parsed.netloc, clean_path)
        
        # Check if already exists to avoid redownloading
        if not os.path.exists(local_path):
            download_file(a_url, local_path)
            
            # If it's a Framer image with query params, also download the base image
            if "framerusercontent.com/images" in a_url and "?" in a_url:
                base_url_img = a_url.split('?')[0]
                base_parsed = urlparse(base_url_img)
                base_local_path = os.path.join(assets_dir, base_parsed.netloc, base_parsed.path.lstrip('/'))
                if not os.path.exists(base_local_path):
                    download_file(base_url_img, base_local_path)
        else:
            print(f"Already exists: {local_path}")

if __name__ == "__main__":
    main()

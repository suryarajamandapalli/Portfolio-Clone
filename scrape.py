import os
import urllib.request
import re
import html
from urllib.parse import urljoin, urlparse

url = "https://sanjaymenon.framer.website/"
output_dir = r"C:\Users\surya\Documents\antigravity\keen-pythagoras"

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
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch HTML: {e}")
        return

    # Save raw HTML
    html_path = os.path.join(output_dir, "raw_index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Saved raw HTML to {html_path}")

    # Find all asset URLs (images, videos, fonts, css, js)
    asset_urls = set()
    
    # Match double quoted URLs or single quoted URLs
    urls = re.findall(r'https?://[^\s"\'>]+', html_content)
    for u in urls:
        # Decode HTML entities like &amp; -> &
        u = html.unescape(u)
        # Clean up URL (remove trailing slashes, backslashes, quotes, closing parenthesis, etc.)
        u = u.split('\\')[0].split('"')[0].split("'")[0].split(')')[0].split(']')[0]
        if any(ext in u.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.mp4', '.webm', '.woff2', '.woff', '.ttf', '.css', '.js', '.mjs']):
            asset_urls.add(u)

    print(f"Found {len(asset_urls)} potential asset URLs.")
    
    # Download them
    assets_dir = os.path.join(output_dir, "downloaded_assets")
    for a_url in sorted(asset_urls):
        parsed = urlparse(a_url)
        # Create a local path based on domain and path, but keep query params out of the filename or clean them
        # Let's clean the path so we don't have query params in the filename
        clean_path = parsed.path.lstrip('/')
        # If there are query params, we can append them to the filename or ignore them
        # But wait, Framer uses query params like ?width=... for responsive images. Let's save them with a clean name
        # and maybe also the original name if needed.
        local_path = os.path.join(assets_dir, parsed.netloc, clean_path)
        
        # Let's also download the original unscaled image if it has width/height params
        download_file(a_url, local_path)
        
        # If it's a Framer image with query params, also download the base image (without query params)
        if "framerusercontent.com/images" in a_url and "?" in a_url:
            base_url = a_url.split('?')[0]
            base_parsed = urlparse(base_url)
            base_local_path = os.path.join(assets_dir, base_parsed.netloc, base_parsed.path.lstrip('/'))
            download_file(base_url, base_local_path)

if __name__ == "__main__":
    main()

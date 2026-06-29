import os
import urllib.request
import re
import html
from urllib.parse import urljoin, urlparse

pages = {
    "/": "raw_index.html",
    "/resume": "raw_resume.html",
    "/checkout": "raw_checkout.html",
    "/old-home": "raw_old_home.html"
}

base_url = "https://sanjaymenon.framer.website"
output_dir = r"C:\Users\surya\Documents\antigravity\keen-pythagoras"
assets_dir = os.path.join(output_dir, "downloaded_assets")

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

def scrape_page(path_suffix, filename):
    url = base_url + path_suffix
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return ""

    # Save raw HTML
    html_path = os.path.join(output_dir, filename)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Saved raw HTML to {html_path}")
    return html_content

def main():
    all_asset_urls = set()
    
    for path_suffix, filename in pages.items():
        print(f"\n--- Scraping {path_suffix} ---")
        html_content = scrape_page(path_suffix, filename)
        if not html_content:
            continue
            
        # Find all asset URLs
        urls = re.findall(r'https?://[^\s"\'>]+', html_content)
        for u in urls:
            u = html.unescape(u)
            u = u.split('\\')[0].split('"')[0].split("'")[0].split(')')[0].split(']')[0]
            if any(ext in u.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.mp4', '.webm', '.woff2', '.woff', '.ttf', '.css', '.js', '.mjs']):
                all_asset_urls.add(u)

    print(f"\nFound {len(all_asset_urls)} total unique asset URLs across all pages.")
    
    # Download them
    for a_url in sorted(all_asset_urls):
        parsed = urlparse(a_url)
        clean_path = parsed.path.lstrip('/')
        local_path = os.path.join(assets_dir, parsed.netloc, clean_path)
        
        download_file(a_url, local_path)
        
        # If it's a Framer image with query params, also download the base image
        if "framerusercontent.com/images" in a_url and "?" in a_url:
            base_url_img = a_url.split('?')[0]
            base_parsed = urlparse(base_url_img)
            base_local_path = os.path.join(assets_dir, base_parsed.netloc, base_parsed.path.lstrip('/'))
            download_file(base_url_img, base_local_path)

if __name__ == "__main__":
    main()

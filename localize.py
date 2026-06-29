import os
import shutil
import re

src_dir = r"C:\Users\surya\Documents\antigravity\keen-pythagoras\downloaded_assets"
dist_dir = r"C:\Users\surya\Documents\antigravity\keen-pythagoras\dist"
output_dir = r"C:\Users\surya\Documents\antigravity\keen-pythagoras"

pages = [
    {"src": "raw_index.html", "dest": "index.html", "level": 0},
    {"src": "raw_resume.html", "dest": "resume/index.html", "level": 1},
    {"src": "raw_checkout.html", "dest": "checkout/index.html", "level": 1},
    {"src": "raw_old_home.html", "dest": "old-home/index.html", "level": 1}
]

def copy_assets():
    # Define target directories
    js_dist = os.path.join(dist_dir, "assets", "js")
    img_dist = os.path.join(dist_dir, "assets", "images")
    font_dist = os.path.join(dist_dir, "assets", "fonts")
    
    os.makedirs(js_dist, exist_ok=True)
    os.makedirs(img_dist, exist_ok=True)
    os.makedirs(font_dist, exist_ok=True)

    # Copy JS files
    js_src = os.path.join(src_dir, "framerusercontent.com", "sites", "3r1Xu4DXLtC5PUnDU2zspB")
    if os.path.exists(js_src):
        for f in os.listdir(js_src):
            shutil.copy(os.path.join(js_src, f), os.path.join(js_dist, f))
            print(f"Copied JS: {f}")

    # Copy Images
    img_src = os.path.join(src_dir, "framerusercontent.com", "images")
    if os.path.exists(img_src):
        for f in os.listdir(img_src):
            shutil.copy(os.path.join(img_src, f), os.path.join(img_dist, f))
            print(f"Copied Image: {f}")

    # Copy Fonts from assets
    font_src = os.path.join(src_dir, "framerusercontent.com", "assets")
    if os.path.exists(font_src):
        for f in os.listdir(font_src):
            shutil.copy(os.path.join(font_src, f), os.path.join(font_dist, f))
            print(f"Copied Font (assets): {f}")

    # Copy Fonts from third-party-assets
    tp_font_src = os.path.join(src_dir, "framerusercontent.com", "third-party-assets")
    if os.path.exists(tp_font_src):
        tp_font_dist = os.path.join(font_dist, "third-party-assets")
        shutil.copytree(tp_font_src, tp_font_dist, dirs_exist_ok=True)
        print("Copied third-party-assets font tree")

    # Copy Fonts from fonts.gstatic.com
    gstatic_src = os.path.join(src_dir, "fonts.gstatic.com")
    if os.path.exists(gstatic_src):
        gstatic_dist = os.path.join(font_dist, "gstatic")
        shutil.copytree(gstatic_src, gstatic_dist, dirs_exist_ok=True)
        print("Copied gstatic font tree")

def localize_content():
    # Process HTML pages
    for p in pages:
        src_path = os.path.join(output_dir, p["src"])
        dest_path = os.path.join(dist_dir, p["dest"])
        
        if not os.path.exists(src_path):
            print(f"Skipping missing page: {p['src']}")
            continue
            
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy(src_path, dest_path)
        
        # Determine relative prefix based on level
        rel_prefix = "./" if p["level"] == 0 else "../"
        
        replacements = [
            ("https://framerusercontent.com/sites/3r1Xu4DXLtC5PUnDU2zspB/", f"{rel_prefix}assets/js/"),
            ("https://framerusercontent.com/images/", f"{rel_prefix}assets/images/"),
            ("https://framerusercontent.com/assets/", f"{rel_prefix}assets/fonts/"),
            ("https://framerusercontent.com/third-party-assets/", f"{rel_prefix}assets/fonts/third-party-assets/"),
            ("https://fonts.gstatic.com/", f"{rel_prefix}assets/fonts/gstatic/"),
        ]
        
        with open(dest_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        for old, new in replacements:
            content = content.replace(old, new)
            
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Localized HTML: {p['dest']}")

    # Process JS files (always at level 2 relative to root: assets/js/)
    js_replacements = [
        ("https://framerusercontent.com/sites/3r1Xu4DXLtC5PUnDU2zspB/", "./"),
        ("https://framerusercontent.com/images/", "../images/"),
        ("https://framerusercontent.com/assets/", "../fonts/"),
        ("https://framerusercontent.com/third-party-assets/", "../fonts/third-party-assets/"),
        ("https://fonts.gstatic.com/", "../fonts/gstatic/"),
    ]

    js_dir = os.path.join(dist_dir, "assets", "js")
    for f in os.listdir(js_dir):
        if f.endswith(".mjs") or f.endswith(".js"):
            file_path = os.path.join(js_dir, f)
            with open(file_path, "r", encoding="utf-8") as file_obj:
                js_content = file_obj.read()
            
            for old, new in js_replacements:
                js_content = js_content.replace(old, new)
                
            with open(file_path, "w", encoding="utf-8") as file_obj:
                file_obj.write(js_content)
            print(f"Localized JS file: {f}")

if __name__ == "__main__":
    copy_assets()
    localize_content()
    print("Localization complete!")

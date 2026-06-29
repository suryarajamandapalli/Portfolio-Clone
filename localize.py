import os
import shutil

src_dir = r"C:\Users\surya\Documents\antigravity\keen-pythagoras\downloaded_assets"
workspace_dir = r"C:\Users\surya\Documents\antigravity\keen-pythagoras"

pages = [
    "index.html",
    "resume/index.html",
    "checkout/index.html",
    "old-home/index.html"
]

def copy_assets():
    # Define target directories
    js_dist = os.path.join(workspace_dir, "assets", "js")
    img_dist = os.path.join(workspace_dir, "assets", "images")
    font_dist = os.path.join(workspace_dir, "assets", "fonts")
    
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

    # Copy Fonts/Videos from assets
    font_src = os.path.join(src_dir, "framerusercontent.com", "assets")
    if os.path.exists(font_src):
        for f in os.listdir(font_src):
            shutil.copy(os.path.join(font_src, f), os.path.join(font_dist, f))
            print(f"Copied Font/Asset: {f}")

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
    # We will use absolute paths starting with /assets/
    replacements = [
        ("https://framerusercontent.com/sites/3r1Xu4DXLtC5PUnDU2zspB/", "/assets/js/"),
        ("https://framerusercontent.com/images/", "/assets/images/"),
        ("https://framerusercontent.com/assets/", "/assets/fonts/"),
        ("https://framerusercontent.com/third-party-assets/", "/assets/fonts/third-party-assets/"),
        ("https://fonts.gstatic.com/", "/assets/fonts/gstatic/"),
        # Also clean up any previously written relative paths to make them absolute
        ("../assets/js/", "/assets/js/"),
        ("../assets/images/", "/assets/images/"),
        ("../assets/fonts/", "/assets/fonts/"),
        ("./assets/js/", "/assets/js/"),
        ("./assets/images/", "/assets/images/"),
        ("./assets/fonts/", "/assets/fonts/"),
        # If there are any relative paths in JS files, make them absolute
        ("../images/", "/assets/images/"),
        ("../fonts/", "/assets/fonts/"),
        ("./", "/assets/js/") # Wait, be careful with replacing "./" in JS. We only want to replace specific imports.
    ]

    # Process HTML pages in-place
    for p in pages:
        page_path = os.path.join(workspace_dir, p)
        if not os.path.exists(page_path):
            print(f"Skipping missing page: {p}")
            continue
            
        with open(page_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        for old, new in replacements[:11]: # Only apply CDN and relative asset replacements
            content = content.replace(old, new)
            
        with open(page_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Localized HTML: {p}")

    # Process JS files in-place
    js_dir = os.path.join(workspace_dir, "assets", "js")
    for f in os.listdir(js_dir):
        if f.endswith(".mjs") or f.endswith(".js"):
            file_path = os.path.join(js_dir, f)
            with open(file_path, "r", encoding="utf-8") as file_obj:
                js_content = file_obj.read()
            
            # For JS files, we want to replace CDN URLs with absolute paths
            for old, new in [
                ("https://framerusercontent.com/sites/3r1Xu4DXLtC5PUnDU2zspB/", "/assets/js/"),
                ("https://framerusercontent.com/images/", "/assets/images/"),
                ("https://framerusercontent.com/assets/", "/assets/fonts/"),
                ("https://framerusercontent.com/third-party-assets/", "/assets/fonts/third-party-assets/"),
                ("https://fonts.gstatic.com/", "/assets/fonts/gstatic/"),
                ("../images/", "/assets/images/"),
                ("../fonts/", "/assets/fonts/"),
            ]:
                js_content = js_content.replace(old, new)
                
            # Also, we need to handle relative imports inside JS.
            # In our previous run, we replaced CDN JS URLs with "./".
            # E.g. import n from "./react.eHRKlns7.mjs"
            # Since these are in the same folder (/assets/js/), a relative import of "./" works perfectly!
            # So we should NOT replace "./" with "/assets/js/" for local JS imports, because relative imports between JS files in the same folder are perfectly valid.
            # But wait, what if they import from "/assets/js/"? That is also valid. Let's leave "./" as is since it's valid.
            
            with open(file_path, "w", encoding="utf-8") as file_obj:
                file_obj.write(js_content)
            print(f"Localized JS file: {f}")

if __name__ == "__main__":
    copy_assets()
    localize_content()
    print("Localization complete!")

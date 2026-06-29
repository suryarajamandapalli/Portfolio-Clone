import os
import re
from urllib.parse import urlparse

dist_dir = r"C:\Users\surya\Documents\antigravity\keen-pythagoras"

def resolve_path(base_file, ref_path):
    # If ref_path is an absolute URL or external, ignore
    if ref_path.startswith(('http://', 'https://', 'data:', '//')):
        return None
        
    # Remove query parameters or hashes
    ref_path = ref_path.split('?')[0].split('#')[0]
    
    # Resolve relative path
    base_dir = os.path.dirname(base_file)
    resolved = os.path.abspath(os.path.join(base_dir, ref_path))
    return resolved

def check_html(html_path):
    missing = []
    found_refs = []
    
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Find href, src, and modulepreload links
    refs = re.findall(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']', content)
    # Also find modulepreload links in scripts if any
    preload_refs = re.findall(r'href\s*:\s*["\']([^"\']+)["\']', content)
    
    all_refs = set(refs + preload_refs)
    
    for ref in all_refs:
        resolved = resolve_path(html_path, ref)
        if resolved:
            found_refs.append((ref, resolved))
            if not os.path.exists(resolved):
                missing.append((ref, resolved))
                
    return found_refs, missing

def check_js(js_path):
    missing = []
    found_refs = []
    
    with open(js_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Find imports/exports: e.g. import ... from "./..." or import "./..."
    imports = re.findall(r'(?:import|from)\s*["\']([^"\']+)["\']', content)
    # Find dynamic imports: import("./...")
    dyn_imports = re.findall(r'import\s*\(\s*["\']([^"\']+)["\']\s*\)', content)
    # Find asset string references: e.g. "../images/..." or "../fonts/..."
    assets = re.findall(r'["\'](\.\.[^"\']+)["\']', content)
    
    all_refs = set(imports + dyn_imports + assets)
    
    for ref in all_refs:
        resolved = resolve_path(js_path, ref)
        if resolved:
            found_refs.append((ref, resolved))
            if not os.path.exists(resolved):
                missing.append((ref, resolved))
                
    return found_refs, missing

def main():
    html_path = os.path.join(dist_dir, "index.html")
    
    print("Checking HTML...")
    html_refs, html_missing = check_html(html_path)
    print(f"Found {len(html_refs)} local references in index.html.")
    if html_missing:
        print("WARNING: Missing files in index.html:")
        for ref, res in html_missing:
            print(f"  - {ref} -> {res}")
    else:
        print("index.html: All local references OK.")
        
    print("\nChecking JS/MJS files...")
    js_dir = os.path.join(dist_dir, "assets", "js")
    total_js_refs = 0
    all_js_missing = []
    
    for root, _, files in os.walk(js_dir):
        for f in files:
            if f.endswith(('.mjs', '.js')):
                js_path = os.path.join(root, f)
                js_refs, js_missing = check_js(js_path)
                total_js_refs += len(js_refs)
                if js_missing:
                    all_js_missing.append((f, js_missing))
                    
    print(f"Processed JS files. Found {total_js_refs} total references.")
    if all_js_missing:
        print("WARNING: Missing files in JS files:")
        for f, missing_list in all_js_missing:
            print(f"In {f}:")
            for ref, res in missing_list:
                print(f"  - {ref} -> {res}")
    else:
        print("All JS files: All local references OK.")

if __name__ == "__main__":
    main()

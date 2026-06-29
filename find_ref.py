import os

search_dir = r"C:\Users\surya\Documents\antigravity\keen-pythagoras"
search_str = "ZFhoqlxuV09Rbo2TYA3i62HyQ"

for root, dirs, files in os.walk(search_dir):
    for f in files:
        if f.endswith(('.html', '.js', '.mjs', '.json', '.css')):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as file_obj:
                    content = file_obj.read()
                    if search_str in content:
                        print(f"Found in: {path}")
            except Exception as e:
                print(f"Error reading {path}: {e}")

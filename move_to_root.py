import os
import shutil

workspace_dir = r"C:\Users\surya\Documents\antigravity\keen-pythagoras"
dist_dir = os.path.join(workspace_dir, "dist")

def move_to_root():
    if not os.path.exists(dist_dir):
        print("dist folder does not exist!")
        return
        
    # Move files and folders from dist to workspace root
    for item in os.listdir(dist_dir):
        src = os.path.join(dist_dir, item)
        dst = os.path.join(workspace_dir, item)
        
        if os.path.exists(dst):
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            else:
                os.remove(dst)
                
        shutil.move(src, dst)
        print(f"Moved {item} to root")
        
    # Remove dist folder
    os.rmdir(dist_dir)
    print("Removed dist folder")

if __name__ == "__main__":
    move_to_root()

import os
import shutil

repo_root = "d:/2YP"
nested_root = os.path.join(repo_root, "phd_management")
pkg_dir = os.path.join(nested_root, "phd_management")

def move_file(src, dst):
    if os.path.exists(src):
        print(f"Moving {src} to {dst}")
        shutil.move(src, dst)
    else:
        print(f"File not found: {src}")

def main():
    print("Starting repo structure fix...")
    
    # 1. Move setup.py to repo root
    move_file(os.path.join(nested_root, "setup.py"), os.path.join(repo_root, "setup.py"))
    
    # 2. Move hooks.py to package dir (it belongs inside the package)
    # Check if hooks.py is in nested_root or already in pkg_dir
    hooks_src = os.path.join(nested_root, "hooks.py")
    if os.path.exists(hooks_src):
        move_file(hooks_src, os.path.join(pkg_dir, "hooks.py"))
    
    # 3. Move other files from nested root to repo root if necessary
    # (e.g. requirements.txt, README.md if they exist)
    for filename in ["requirements.txt", "README.md", "license.txt", "LICENSE"]:
        src = os.path.join(nested_root, filename)
        if os.path.exists(src):
            move_file(src, os.path.join(repo_root, filename))

    # 4. Move the package directory to repo root
    # We need to be careful not to overwrite if target exists (it shouldn't if we are attentive)
    target_pkg_dir = os.path.join(repo_root, "phd_management")
    
    # Since 'phd_management' (nested_root) and 'phd_management' (pkg_dir) have same name,
    # we can't move pkg_dir to repo_root directly because nested_root IS at repo_root/phd_management.
    # We must rename pkg_dir out of nested_root first.
    
    temp_pkg_dir = os.path.join(repo_root, "phd_management_temp_pkg")
    if os.path.exists(pkg_dir):
        print(f"Moving package {pkg_dir} to temp {temp_pkg_dir}")
        shutil.move(pkg_dir, temp_pkg_dir)
        
        # Now nested_root should be empty of the package
        # verification
        if not os.path.exists(pkg_dir):
            print("Package moved out successfully.")
    
    # 5. Remove the now-empty (or mostly empty) nested root folder
    # We already moved setup.py and hooks.py. 
    # Check if anything else remains in nested_root
    if os.path.exists(nested_root):
        print(f"Cleaning up {nested_root}")
        # shutil.rmtree(nested_root) # Dangerous if something left
        # Let's just renounce it? No we want clean repo.
        # But wait, we renamed pkg_dir out. So nested_root contains only what we didn't move.
        # Let's assume safely we can delete it if we moved everything important.
        # For safety, let's just list what's left.
        leftovers = os.listdir(nested_root)
        print(f"Leftovers in {nested_root}: {leftovers}")
        if not leftovers or leftovers == ['__pycache__']:
            shutil.rmtree(nested_root)
        else:
             print("Warning: nested_root not empty, manual check required.")

    # 6. Rename temp package dir to final name at repo root
    if os.path.exists(temp_pkg_dir):
        if os.path.exists(target_pkg_dir):
            print(f"Target {target_pkg_dir} already exists! This shouldn't happen if we deleted nested_root.")
        else:
            print(f"Restoring package to {target_pkg_dir}")
            shutil.move(temp_pkg_dir, target_pkg_dir)

if __name__ == "__main__":
    try:
        main()
        print("Success")
    except Exception as e:
        print(f"Error: {e}")

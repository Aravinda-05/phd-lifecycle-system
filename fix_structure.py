import os
import shutil

def safe_move(src, dst):
    if not os.path.exists(src):
        print(f"Source {src} does not exist, skipping.")
        return
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    try:
        shutil.move(src, dst)
        print(f"Moved {src} to {dst}")
    except Exception as e:
        print(f"Error moving {src} to {dst}: {e}")

# 1. Rename app_structure to phd_management
if os.path.exists("app_structure"):
    try:
        os.rename("app_structure", "phd_management")
        print("Renamed app_structure to phd_management")
    except OSError:
        # Maybe git is locking it or it exists?
        print("Could not rename app_structure, maybe phd_management exists?")

# Target module directory
module_dir = "phd_management/phd_management"
if not os.path.exists(module_dir):
    os.makedirs(module_dir)

# 2. Merge nested phd_management
nested_module = "phd_management/phd_management/phd_management"
if os.path.exists(nested_module):
    for root, dirs, files in os.walk(nested_module):
        for file in files:
            src_path = os.path.join(root, file)
            # Rel path from nested_module
            rel_path = os.path.relpath(src_path, nested_module)
            dst_path = os.path.join(module_dir, rel_path)
            safe_move(src_path, dst_path)
    shutil.rmtree(nested_module)

# 3. Merge nested phd_management_temp
nested_temp = "phd_management/phd_management/phd_management_temp"
if os.path.exists(nested_temp):
    for root, dirs, files in os.walk(nested_temp):
        for file in files:
            src_path = os.path.join(root, file)
            # Rel path from nested_temp
            rel_path = os.path.relpath(src_path, nested_temp)
            dst_path = os.path.join(module_dir, rel_path)
            safe_move(src_path, dst_path)
    shutil.rmtree(nested_temp)

# 4. Check if phd_management/phd_management actually contains the files now
# If somehow the original phd_management (folder) was just a container and NOT the module
# We might need to move `phd_management/phd_management` UP one level if `setup.py` is in `phd_management`.

# Let's ensure `__init__.py` is in `phd_management/phd_management`
if not os.path.exists(os.path.join(module_dir, "__init__.py")):
    with open(os.path.join(module_dir, "__init__.py"), "w") as f:
        f.write('__version__ = "0.0.1"')

print("Cleanup complete.")

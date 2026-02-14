import os
import shutil

APP_ROOT = "phd_management"
MODULE_ROOT = os.path.join(APP_ROOT, "phd_management")

def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)

def move_contents(src_dir, dst_dir):
    if not os.path.exists(src_dir):
        print(f"Skipping {src_dir} (does not exist)")
        return
    ensure_dir(dst_dir)
    for item in os.listdir(src_dir):
        s = os.path.join(src_dir, item)
        d = os.path.join(dst_dir, item)
        try:
            if os.path.exists(d):
                if os.path.isdir(d):
                    move_contents(s, d) # Recursively merge
                    shutil.rmtree(s)
                else:
                    print(f"File {d} already exists. Overwriting.")
                    os.remove(d)
                    shutil.move(s, d)
            else:
                shutil.move(s, d)
                print(f"Moved {s} -> {d}")
        except Exception as e:
            print(f"Error moving {s}: {e}")

# 1. Move App Base files (setup.py, hooks.py, __init__.py) from app_structure to phd_management
app_structure_base = "app_structure"
if os.path.exists(app_structure_base):
    for f in ["hooks.py", "setup.py", "__init__.py"]:
        src = os.path.join(app_structure_base, f)
        if os.path.exists(src):
            shutil.move(src, os.path.join(APP_ROOT, f))
            print(f"Moved {src} to {APP_ROOT}")

# 2. Merge app_structure/phd_management/phd_management -> phd_management/phd_management
src_nested_1 = "app_structure/phd_management/phd_management"
move_contents(src_nested_1, MODULE_ROOT)

# 3. Merge app_structure/phd_management/phd_management_temp -> phd_management/phd_management
src_nested_2 = "app_structure/phd_management/phd_management_temp"
move_contents(src_nested_2, MODULE_ROOT)

# 4. Cleanup empty directories
try:
    shutil.rmtree("app_structure")
    print("Removed app_structure")
except Exception as e:
    print(f"Could not remove app_structure: {e}")

print("Structure Fix v2 Complete.")

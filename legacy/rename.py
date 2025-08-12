# This script renames files in a directory in batches.

import os

dir = 'data_raw(from_wechat)'

for i, filename in enumerate(os.listdir(dir)):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        new_name = f"{i:03d}.jpg"  # Format the new name with leading zeros
        old_path = os.path.join(dir, filename)
        new_path = os.path.join(dir, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} to {new_name}")
    else:
        print(f"Skipped: {filename} (not an image file)")
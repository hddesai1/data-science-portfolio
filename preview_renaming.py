"""Preview folder renaming"""
import re
from pathlib import Path

base = Path('.')
folders = [d for d in base.iterdir() if d.is_dir() and re.match(r'Day+target*\s*\d+', d.name)]
folders = sorted(folders, key=lambda x: int(re.search(r'\d+', x.name).group()))

print('Sample renaming preview (first 15):\n')
for f in folders[:15]:
    day_num = int(re.search(r'\d+', f.name).group())
    title_match = re.search(r'Day+target*\s*\d+\.\s*(.+)', f.name)
    if title_match:
        title = title_match.group(1).strip()
        title = re.sub(r'[<>:"/\\|?*]', '', title)
        title = re.sub(r'\s+', '-', title)
        new_name = f"Project-{day_num:03d}-{title}"
    else:
        new_name = f"Project-{day_num:03d}"
    print(f"{f.name[:70]:<70} -> {new_name[:70]}")

print(f"\nTotal folders: {len(folders)}")

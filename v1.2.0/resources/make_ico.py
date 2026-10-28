"""
Generate multi-resolution .ico files from the generated logo options using Pillow.
Sizes embedded: 256x256, 128x128, 64x64, 48x48, 32x32, 16x16.
"""

import os
from PIL import Image

ICONS_DIR = os.path.abspath(r"v1.2.0\resources\icons")
APP_DIR = os.path.abspath(r"v1.2.0")

ICO_SIZES = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]

options = [
    ("option_1_topology_hub.png", "option_1.ico"),
    ("option_2_binary_shield.png", "option_2.ico"),
    ("option_3_hexagon_core.png", "option_3.ico"),
    ("option_4_minimalist_rings.png", "option_4.ico"),
    ("option_5_terminal_cube.png", "option_5.ico"),
]

for png_name, ico_name in options:
    png_path = os.path.join(ICONS_DIR, png_name)
    ico_path = os.path.join(ICONS_DIR, ico_name)
    if os.path.exists(png_path):
        img = Image.open(png_path)
        img.save(ico_path, format="ICO", sizes=ICO_SIZES)
        print(f"Generated {ico_name} ({len(ICO_SIZES)} mipmap sizes)")

# Set Option 1 (Topology Hub) as the default app_icon.ico
default_src = os.path.join(ICONS_DIR, "option_1_topology_hub.png")
if os.path.exists(default_src):
    img = Image.open(default_src)
    # Save in resources/icons
    img.save(os.path.join(ICONS_DIR, "app_icon.ico"), format="ICO", sizes=ICO_SIZES)
    # Also save directly in v1.2.0/ for PyInstaller
    img.save(os.path.join(APP_DIR, "app_icon.ico"), format="ICO", sizes=ICO_SIZES)
    print("Successfully created app_icon.ico in v1.2.0 root and resources/icons!")

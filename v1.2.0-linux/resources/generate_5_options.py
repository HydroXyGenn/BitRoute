"""
Script to procedurally generate 5 professional logo designs for IPv4 Subnet Toolkit v1.2.0.
Rendered with 2x supersampling (1024x1024 -> 512x512) for ultra-crisp antialiasing.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.abspath(r"v1.2.0\resources\icons")
os.makedirs(OUT_DIR, exist_ok=True)

FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_SEMI = r"C:\Windows\Fonts\segoeui.ttf"
FONT_MONO = r"C:\Windows\Fonts\consolab.ttf"


def create_base_canvas(size=1024):
    return Image.new("RGBA", (size, size), (0, 0, 0, 0))


def draw_squircle(draw, bounds, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(bounds, radius=radius, fill=fill, outline=outline, width=width)


# ============================================================================
# OPTION 1: NETWORK TOPOLOGY HUB (Routeur central + 4 Sous-réseaux)
# ============================================================================
def generate_option_1():
    img = create_base_canvas(1024)
    draw = ImageDraw.Draw(img)

    # 1. Dark Navy Rounded Background with Gradient simulation
    margin = 48
    draw_squircle(draw, [margin, margin, 1024 - margin, 1024 - margin], 220, (10, 18, 42, 255), (0, 195, 255, 180), 10)

    # Inner subtle grid / circuit glow
    for r in range(160, 480, 80):
        draw.ellipse([512 - r, 512 - r, 512 + r, 512 + r], outline=(0, 119, 254, 40), width=4)

    # 4 satellite subnet nodes (NW, NE, SW, SE)
    nodes = [
        (260, 260, "10."),
        (764, 260, "172."),
        (260, 764, "192."),
        (764, 764, "/24"),
    ]

    # Connecting bus lines from center to 4 nodes
    for nx, ny, _ in nodes:
        draw.line([512, 512, nx, ny], fill=(0, 229, 255, 200), width=14)
        # Glowing middle connector
        mx, my = (512 + nx) // 2, (512 + ny) // 2
        draw.ellipse([mx - 12, my - 12, mx + 12, my + 12], fill=(255, 255, 255, 240))

    # Draw 4 satellite node circles
    for nx, ny, label in nodes:
        draw.ellipse([nx - 90, ny - 90, nx + 90, ny + 90], fill=(13, 27, 65, 255), outline=(0, 229, 255, 255), width=8)
        draw.ellipse([nx - 70, ny - 70, nx + 70, ny + 70], fill=(0, 119, 254, 180))
        font_node = ImageFont.truetype(FONT_MONO, 46)
        bbox = draw.textbbox((0, 0), label, font=font_node)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((nx - tw // 2, ny - th // 2 - 4), label, fill=(255, 255, 255, 255), font=font_node)

    # Center Router Hub (Core)
    cr = 160
    draw.ellipse([512 - cr, 512 - cr, 512 + cr, 512 + cr], fill=(6, 12, 30, 255), outline=(0, 229, 255, 255), width=16)
    draw.ellipse([512 - cr + 24, 512 - cr + 24, 512 + cr - 24, 512 + cr - 24], fill=(0, 102, 238, 240))

    # Core Monogram "IPv4"
    font_core = ImageFont.truetype(FONT_BOLD, 84)
    bbox = draw.textbbox((0, 0), "IPv4", font=font_core)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((512 - tw // 2, 512 - th // 2 - 8), "IPv4", fill=(255, 255, 255, 255), font=font_core)

    return img.resize((512, 512), Image.Resampling.LANCZOS)


# ============================================================================
# OPTION 2: BINARY CYBER SHIELD (Bouclier & Matrice 32-bit)
# ============================================================================
def generate_option_2():
    img = create_base_canvas(1024)
    draw = ImageDraw.Draw(img)

    margin = 48
    draw_squircle(draw, [margin, margin, 1024 - margin, 1024 - margin], 220, (8, 14, 28, 255), (37, 99, 235, 180), 10)

    # Draw modern shield polygon
    shield_pts = [
        (512, 170),
        (820, 230),
        (760, 640),
        (512, 860),
        (264, 640),
        (204, 230),
    ]
    draw.polygon(shield_pts, fill=(15, 23, 42, 255), outline=(56, 189, 248, 255))
    # Inner border
    inner_pts = [
        (512, 200),
        (790, 254),
        (736, 620),
        (512, 824),
        (288, 620),
        (234, 254),
    ]
    draw.polygon(inner_pts, outline=(30, 64, 175, 200))

    # 4 horizontal segmented octet bars inside shield (representing 4 octets = 32 bits)
    bar_y_coords = [320, 420, 520, 620]
    bar_labels = ["11111111", "11111111", "11100000", "00000000"]
    bar_colors = [
        (59, 130, 246, 255),
        (59, 130, 246, 255),
        (16, 185, 129, 255),
        (71, 85, 105, 200),
    ]

    font_bits = ImageFont.truetype(FONT_MONO, 44)
    for y, label, col in zip(bar_y_coords, bar_labels, bar_colors):
        # segmented bar pill
        draw.rounded_rectangle([320, y, 704, y + 64], radius=16, fill=(15, 27, 54, 230), outline=col, width=4)
        bbox = draw.textbbox((0, 0), label, font=font_bits)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((512 - tw // 2, y + (64 - th) // 2 - 4), label, fill=col, font=font_bits)

    # Subnet Mask Badge at bottom
    font_badge = ImageFont.truetype(FONT_BOLD, 52)
    bbox = draw.textbbox((0, 0), "/19 SUBNET", font=font_badge)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([512 - tw // 2 - 24, 710, 512 + tw // 2 + 24, 780], radius=18, fill=(37, 99, 235, 255))
    draw.text((512 - tw // 2, 720), "/19 SUBNET", fill=(255, 255, 255, 255), font=font_badge)

    return img.resize((512, 512), Image.Resampling.LANCZOS)


# ============================================================================
# OPTION 3: HEXAGON SUBNET CORE (Architecture Hexagonale & Constellation)
# ============================================================================
def generate_option_3():
    img = create_base_canvas(1024)
    draw = ImageDraw.Draw(img)

    margin = 48
    draw_squircle(draw, [margin, margin, 1024 - margin, 1024 - margin], 220, (13, 17, 23, 255), (16, 185, 129, 180), 10)

    # Outer Hexagon calculation
    cx, cy, r = 512, 512, 340
    hex_pts = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        hex_pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))

    draw.polygon(hex_pts, fill=(18, 26, 36, 255), outline=(16, 185, 129, 255))

    # Inner concentric hexagon
    inner_hex = []
    r2 = 270
    for i in range(6):
        angle = math.radians(60 * i - 30)
        inner_hex.append((cx + r2 * math.cos(angle), cy + r2 * math.sin(angle)))
    draw.polygon(inner_hex, outline=(5, 150, 105, 140))

    # Triangulated network mesh lines between opposite vertices
    for i in range(3):
        draw.line([hex_pts[i], hex_pts[i + 3]], fill=(52, 211, 153, 100), width=6)

    # Glowing node circles at all 6 vertices
    for pt in hex_pts:
        draw.ellipse([pt[0] - 22, pt[1] - 22, pt[0] + 22, pt[1] + 22], fill=(255, 255, 255, 255), outline=(16, 185, 129, 255), width=6)

    # Central Core Circle
    draw.ellipse([cx - 130, cy - 130, cx + 130, cy + 130], fill=(9, 14, 20, 255), outline=(16, 185, 129, 255), width=10)

    # Stylized IP / Slash in center
    font_h = ImageFont.truetype(FONT_BOLD, 100)
    bbox = draw.textbbox((0, 0), "IP/4", font=font_h)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 8), "IP/4", fill=(52, 211, 153, 255), font=font_h)

    return img.resize((512, 512), Image.Resampling.LANCZOS)


# ============================================================================
# OPTION 4: MINIMALIST MODERN TECH RINGS (Épuré style Apple / Google)
# ============================================================================
def generate_option_4():
    img = create_base_canvas(1024)
    draw = ImageDraw.Draw(img)

    margin = 48
    draw_squircle(draw, [margin, margin, 1024 - margin, 1024 - margin], 220, (15, 23, 42, 255), (56, 189, 248, 160), 10)

    # 4 Clean Intersecting Orbital Rings (representing 4 octets of IPv4)
    centers = [
        (400, 400),
        (624, 400),
        (400, 624),
        (624, 624),
    ]
    ring_radius = 170

    colors = [
        (37, 99, 235, 200),
        (14, 165, 233, 200),
        (16, 185, 129, 200),
        (99, 102, 241, 200),
    ]

    for (x, y), col in zip(centers, colors):
        draw.ellipse([x - ring_radius, y - ring_radius, x + ring_radius, y + ring_radius], outline=col, width=16)

    # Central Dynamic Cut Slash "/"
    draw.line([340, 720, 684, 304], fill=(255, 255, 255, 255), width=32)

    # 4 Elegant Accent Intersection Dots
    for (x, y) in centers:
        draw.ellipse([x - 20, y - 20, x + 20, y + 20], fill=(255, 255, 255, 255))

    # Bottom Sleek Subtitle
    font_sub = ImageFont.truetype(FONT_BOLD, 52)
    bbox = draw.textbbox((0, 0), "SUBNET", font=font_sub)
    tw = bbox[2] - bbox[0]
    draw.text((512 - tw // 2, 800), "SUBNET", fill=(148, 163, 184, 255), font=font_sub)

    return img.resize((512, 512), Image.Resampling.LANCZOS)


# ============================================================================
# OPTION 5: HACKER TERMINAL ISOMETRIC CUBE (Phosphor Green #00FF66 on Black)
# ============================================================================
def generate_option_5():
    img = create_base_canvas(1024)
    draw = ImageDraw.Draw(img)

    margin = 48
    draw_squircle(draw, [margin, margin, 1024 - margin, 1024 - margin], 220, (0, 0, 0, 255), (0, 255, 102, 255), 12)

    # Draw 3D Isometric Cube in Terminal Green
    # Top face
    cx, cy = 512, 480
    w, h = 300, 160
    top_face = [
        (cx, cy - h),
        (cx + w, cy),
        (cx, cy + h),
        (cx - w, cy),
    ]
    # Left face
    h_side = 260
    left_face = [
        (cx - w, cy),
        (cx, cy + h),
        (cx, cy + h + h_side),
        (cx - w, cy + h_side),
    ]
    # Right face
    right_face = [
        (cx, cy + h),
        (cx + w, cy),
        (cx + w, cy + h_side),
        (cx, cy + h + h_side),
    ]

    draw.polygon(top_face, fill=(0, 28, 10, 255), outline=(0, 255, 102, 255), width=8)
    draw.polygon(left_face, fill=(0, 16, 6, 255), outline=(0, 255, 102, 255), width=8)
    draw.polygon(right_face, fill=(0, 22, 8, 255), outline=(0, 255, 102, 255), width=8)

    # Terminal Monospace Matrix Bits etched on top face
    font_term = ImageFont.truetype(FONT_MONO, 46)
    draw.text((cx - 140, cy - 50), "11111111", fill=(0, 255, 102, 255), font=font_term)
    draw.text((cx - 140, cy), "11100000", fill=(0, 204, 85, 230), font=font_term)

    # Left face text
    font_left = ImageFont.truetype(FONT_BOLD, 70)
    draw.text((cx - 240, cy + 100), "IP/v4", fill=(0, 255, 102, 255), font=font_left)

    # Right face text
    draw.text((cx + 60, cy + 100), "/24", fill=(51, 255, 136, 255), font=font_left)

    # Bottom Terminal Prompt
    font_prompt = ImageFont.truetype(FONT_MONO, 42)
    prompt_txt = "root@inpt:~# subnet"
    bbox = draw.textbbox((0, 0), prompt_txt, font=font_prompt)
    tw = bbox[2] - bbox[0]
    draw.text((512 - tw // 2, 830), prompt_txt, fill=(0, 255, 102, 220), font=font_prompt)

    return img.resize((512, 512), Image.Resampling.LANCZOS)


# ============================================================================
# COMPOSITE SHOWCASE (Toutes les 5 options sur une seule bannière)
# ============================================================================
def generate_showcase(icons):
    # Banner: 5 columns of 360 width + margins = 1920 x 580
    w_card = 360
    pad = 30
    total_w = 5 * w_card + 6 * pad
    total_h = 560

    showcase = Image.new("RGBA", (total_w, total_h), (11, 15, 25, 255))
    draw = ImageDraw.Draw(showcase)

    font_title = ImageFont.truetype(FONT_BOLD, 26)
    font_desc = ImageFont.truetype(FONT_SEMI, 19)

    metadata = [
        ("Option 1", "Topology Hub", "Routeur central & 4 octets"),
        ("Option 2", "Binary Shield", "Bouclier 32-bit & masque /19"),
        ("Option 3", "Hexagon Core", "Constellation réseau & mesh"),
        ("Option 4", "Minimalist Rings", "Style épuré tech / Apple-Google"),
        ("Option 5", "Hacker Terminal", "Cube isométrique vert néon"),
    ]

    for idx, (img, (num, title, desc)) in enumerate(zip(icons, metadata)):
        x_left = pad + idx * (w_card + pad)
        # Card container
        draw.rounded_rectangle([x_left, 24, x_left + w_card, total_h - 24], radius=24, fill=(18, 24, 38, 255), outline=(51, 65, 85, 255), width=2)

        # Thumbnail 260x260
        thumb = img.resize((260, 260), Image.Resampling.LANCZOS)
        showcase.paste(thumb, (x_left + (w_card - 260) // 2, 48), thumb)

        # Number & Title
        header_text = f"{num} : {title}"
        bbox = draw.textbbox((0, 0), header_text, font=font_title)
        tw = bbox[2] - bbox[0]
        draw.text((x_left + (w_card - tw) // 2, 335), header_text, fill=(255, 255, 255, 255), font=font_title)

        # Description
        bbox2 = draw.textbbox((0, 0), desc, font=font_desc)
        tw2 = bbox2[2] - bbox2[0]
        draw.text((x_left + (w_card - tw2) // 2, 375), desc, fill=(148, 163, 184, 255), font=font_desc)

        # Select Pill hint
        draw.rounded_rectangle([x_left + 70, 430, x_left + w_card - 70, 480], radius=12, fill=(37, 99, 235, 200))
        pill_txt = f"Choisir #{idx + 1}"
        font_pill = ImageFont.truetype(FONT_BOLD, 20)
        bbox_p = draw.textbbox((0, 0), pill_txt, font=font_pill)
        tw_p = bbox_p[2] - bbox_p[0]
        draw.text((x_left + (w_card - tw_p) // 2, 442), pill_txt, fill=(255, 255, 255, 255), font=font_pill)

    return showcase


def main():
    print("Generating Option 1: Network Topology Hub...")
    opt1 = generate_option_1()
    opt1.save(os.path.join(OUT_DIR, "option_1_topology_hub.png"))

    print("Generating Option 2: Binary Cyber Shield...")
    opt2 = generate_option_2()
    opt2.save(os.path.join(OUT_DIR, "option_2_binary_shield.png"))

    print("Generating Option 3: Hexagon Subnet Core...")
    opt3 = generate_option_3()
    opt3.save(os.path.join(OUT_DIR, "option_3_hexagon_core.png"))

    print("Generating Option 4: Minimalist Tech Rings...")
    opt4 = generate_option_4()
    opt4.save(os.path.join(OUT_DIR, "option_4_minimalist_rings.png"))

    print("Generating Option 5: Hacker Terminal Cube...")
    opt5 = generate_option_5()
    opt5.save(os.path.join(OUT_DIR, "option_5_terminal_cube.png"))

    print("Generating All 5 Options Showcase...")
    showcase = generate_showcase([opt1, opt2, opt3, opt4, opt5])
    showcase.save(os.path.join(OUT_DIR, "all_5_options_preview.png"))

    print("All 5 options successfully created in:", OUT_DIR)


if __name__ == "__main__":
    main()

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path(r"C:\New_audio\outputs\page_branding")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_ARIAL_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_GEORGIA_BOLD = r"C:\Windows\Fonts\georgiab.ttf"


def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def create_minimalist_avatar(filename="radio_2am_avatar_1.png"):
    """Option 1: Modern Dark Neon Minimalist Avatar (1080x1080)"""
    size = (1080, 1080)
    img = Image.new("RGBA", size, (11, 13, 18, 255))
    draw = ImageDraw.Draw(img)

    for r in range(480, 100, -15):
        alpha = int(25 * (1 - r / 480))
        draw.ellipse([540 - r, 540 - r, 540 + r, 540 + r], fill=(30, 41, 59, alpha))

    # Outer neon ring (Amber accent ring)
    draw.ellipse([180, 180, 900, 900], outline=(245, 158, 11, 220), width=4)
    draw.arc([160, 160, 920, 920], start=30, end=150, fill=(100, 116, 139, 140), width=2)
    draw.arc([160, 160, 920, 920], start=210, end=330, fill=(100, 116, 139, 140), width=2)

    # Audio Waveform bars in center
    bar_heights = [45, 80, 130, 200, 260, 290, 260, 200, 130, 80, 45]
    start_x = 540 - (len(bar_heights) * 22) // 2
    for i, h in enumerate(bar_heights):
        bx = start_x + i * 22
        by1 = 440 - h // 2
        by2 = 440 + h // 2
        color = (245, 158, 11) if 3 <= i <= 7 else (148, 163, 184)
        draw.rounded_rectangle([bx, by1, bx + 10, by2], radius=5, fill=color)

    # Typography: RADIO 2AM
    f_sub = get_font(FONT_BOLD, 46)
    f_title = get_font(FONT_ARIAL_BOLD, 92)

    text_sub = "R A D I O"
    bb_sub = draw.textbbox((0, 0), text_sub, font=f_sub)
    draw.text((540 - (bb_sub[2] - bb_sub[0]) // 2, 630), text_sub, font=f_sub, fill=(148, 163, 184, 255))

    text_main = "2 AM"
    bb_main = draw.textbbox((0, 0), text_main, font=f_title)
    draw.text((540 - (bb_main[2] - bb_main[0]) // 2, 700), text_main, font=f_title, fill=(255, 255, 255, 255))
    draw.ellipse([534, 830, 546, 842], fill=(239, 68, 68, 255))

    out_p = OUTPUT_DIR / filename
    img.convert("RGB").save(out_p, quality=95)
    print(f"Created {out_p}")
def create_cinematic_avatar(filename="radio_2am_avatar_2.png"):
    """Option 2: Deep Moody Amber-Gold & Dark Academia Avatar (1080x1080)"""
    size = (1080, 1080)
    img = Image.new("RGBA", size, (7, 10, 15, 255))
    draw = ImageDraw.Draw(img)

    draw.ellipse([140, 140, 940, 940], outline=(217, 119, 6, 180), width=3)
    draw.ellipse([156, 156, 924, 924], outline=(71, 85, 105, 100), width=1)

    # Crescent Moon / Midnight symbol
    moon_center = (540, 390)
    draw.ellipse([moon_center[0] - 80, moon_center[1] - 80, moon_center[0] + 80, moon_center[1] + 80], fill=(251, 191, 36, 230))
    draw.ellipse([moon_center[0] - 50, moon_center[1] - 85, moon_center[0] + 90, moon_center[1] + 75], fill=(7, 10, 15, 255))

    for y_offset in [510, 530, 550]:
        w = (570 - y_offset) * 3
        draw.line([540 - w, y_offset, 540 + w, y_offset], fill=(148, 163, 184, 120), width=2)

    f_brand = get_font(FONT_GEORGIA_BOLD, 84)
    f_tag = get_font(FONT_BOLD, 36)

    brand = "RADIO 2AM"
    bb = draw.textbbox((0, 0), brand, font=f_brand)
    draw.text((540 - (bb[2] - bb[0]) // 2, 610), brand, font=f_brand, fill=(254, 243, 199, 255))

    tag = "ĐỘC THOẠI & THỨC TỈNH"
    bt = draw.textbbox((0, 0), tag, font=f_tag)
    draw.text((540 - (bt[2] - bt[0]) // 2, 720), tag, font=f_tag, fill=(180, 83, 9, 255))

    out_p = OUTPUT_DIR / filename
    img.convert("RGB").save(out_p, quality=95)
    print(f"Created {out_p}")
    return out_p


def create_facebook_cover(filename="radio_2am_cover.png"):
    """Facebook Banner / Cover photo (1640 x 924)."""
    width, height = 1640, 924
    img = Image.new("RGBA", (width, height), (9, 12, 17, 255))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        ratio = y / height
        draw.line([(0, y), (width, y)], fill=(int(9 + 12 * (1 - ratio)), int(12 + 18 * (1 - ratio)), int(17 + 25 * (1 - ratio)), 255))

    for radius in range(500, 50, -25):
        alpha = int(22 * (1 - radius / 500))
        draw.ellipse([820 - radius * 1.5, 462 - radius, 820 + radius * 1.5, 462 + radius], fill=(217, 119, 6, alpha))

    bars = [20, 35, 60, 95, 140, 180, 230, 270, 290, 270, 230, 180, 140, 95, 60, 35, 20]
    bx_start = 820 - (len(bars) * 36) // 2
    for idx, bh in enumerate(bars):
        bx = bx_start + idx * 36
        draw.rounded_rectangle([bx, 360 - bh // 2, bx + 14, 360 + bh // 2], radius=7, fill=(71, 85, 105, 90))

    f_tag = get_font(FONT_BOLD, 30)
    tag_text = "PODCAST & VOICE-OVER  •  2:00 AM INSIGHTS"
    bb_t = draw.textbbox((0, 0), tag_text, font=f_tag)
    draw.text((820 - (bb_t[2] - bb_t[0]) // 2, 290), tag_text, font=f_tag, fill=(245, 158, 11, 230))

    f_main = get_font(FONT_ARIAL_BOLD, 120)
    title_text = "RADIO 2AM"
    bb_m = draw.textbbox((0, 0), title_text, font=f_main)
    draw.text((820 - (bb_m[2] - bb_m[0]) // 2, 340), title_text, font=f_main, fill=(255, 255, 255, 255))

    draw.line([660, 505, 980, 505], fill=(217, 119, 6, 200), width=3)
    draw.ellipse([816, 501, 824, 509], fill=(251, 191, 36, 255))

    f_slogan = get_font(FONT_BOLD, 42)
    slogan = "Nơi nói những sự thật mà ban ngày bạn không dám đối diện."
    bb_s = draw.textbbox((0, 0), slogan, font=f_slogan)
    draw.text((820 - (bb_s[2] - bb_s[0]) // 2, 535), slogan, font=f_slogan, fill=(226, 232, 240, 245))

    f_sub = get_font(FONT_REG, 30)
    sub = "Tư Duy Ngược  |  Triết Lý Thực Tế  |  Độc Thoại Chữa Lành Thật Sự"
    bb_sub = draw.textbbox((0, 0), sub, font=f_sub)
    draw.text((820 - (bb_sub[2] - bb_sub[0]) // 2, 610), sub, font=f_sub, fill=(148, 163, 184, 210))

    out_p = OUTPUT_DIR / filename
    img.convert("RGB").save(out_p, quality=95)
    print(f"Created {out_p}")
    return out_p


if __name__ == "__main__":
    create_minimalist_avatar("radio_2am_avatar_1.png")
    create_cinematic_avatar("radio_2am_avatar_2.png")
    create_facebook_cover("radio_2am_cover.png")


import os
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

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


def create_cinematic_photo_cover(img_url: str, filename: str, is_mic=True):
    width, height = 1640, 924
    cache_bg = OUTPUT_DIR / f"raw_bg_{filename}.jpg"

    req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp, open(cache_bg, "wb") as f:
        f.write(resp.read())

    base_img = Image.open(cache_bg).convert("RGBA")
    # Resize & crop to 1640x924
    base_ratio = base_img.width / base_img.height
    target_ratio = width / height

    if base_ratio > target_ratio:
        new_h = height
        new_w = int(height * base_ratio)
    else:
        new_w = width
        new_h = int(width / base_ratio)

    resized = base_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - width) // 2
    top = (new_h - height) // 2
    cropped = resized.crop((left, top, left + width, top + height))

    # Apply moody dark grading: lower brightness, increase contrast
    enhancer = ImageEnhance.Brightness(cropped)
    darkened = enhancer.enhance(0.42)
    enhancer_c = ImageEnhance.Contrast(darkened)
    contrasted = enhancer_c.enhance(1.25)

    # Add dark vignette overlay
    overlay = Image.new("RGBA", (width, height), (7, 10, 16, 170))
    composed = Image.alpha_composite(contrasted, overlay)
    draw = ImageDraw.Draw(composed)

    # Center decorative glow behind text
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for r in range(350, 40, -25):
        alpha = int(14 * (1 - r / 350))
        glow_draw.ellipse([820 - r * 1.6, 430 - r, 820 + r * 1.6, 430 + r], fill=(245, 158, 11, alpha))
    composed = Image.alpha_composite(composed, glow)
    draw = ImageDraw.Draw(composed)

    # Accent Header
    f_tag = get_font(FONT_BOLD, 26)
    tag_text = "PODCAST  •  VOICE-OVER  •  MIDNIGHT REFLECTIONS"
    bb_t = draw.textbbox((0, 0), tag_text, font=f_tag)
    draw.text((820 - (bb_t[2] - bb_t[0]) // 2, 280), tag_text, font=f_tag, fill=(245, 158, 11, 240))

    # Main Brand Name: RADIO 2AM
    f_main = get_font(FONT_ARIAL_BOLD, 115)
    title_text = "RADIO 2AM"
    bb_m = draw.textbbox((0, 0), title_text, font=f_main)
    # Subtle drop shadow
    draw.text((820 - (bb_m[2] - bb_m[0]) // 2 + 4, 334), title_text, font=f_main, fill=(0, 0, 0, 220))
    draw.text((820 - (bb_m[2] - bb_m[0]) // 2, 330), title_text, font=f_main, fill=(255, 255, 255, 255))

    # Divider bar
    draw.line([680, 490, 960, 490], fill=(217, 119, 6, 220), width=3)
    draw.ellipse([815, 486, 825, 494], fill=(251, 191, 36, 255))

    # Slogan
    f_slogan = get_font(FONT_BOLD, 38)
    slogan = "Nơi nói những sự thật mà ban ngày bạn không dám đối diện."
    bb_s = draw.textbbox((0, 0), slogan, font=f_slogan)
    draw.text((820 - (bb_s[2] - bb_s[0]) // 2 + 2, 522), slogan, font=f_slogan, fill=(0, 0, 0, 200))
    draw.text((820 - (bb_s[2] - bb_s[0]) // 2, 520), slogan, font=f_slogan, fill=(241, 245, 249, 255))

    # Subtext
    f_sub = get_font(FONT_REG, 28)
    sub = "Tư Duy Ngược  |  Triết Lý Đời Thực  |  Độc Thoại Thức Tỉnh"
    bb_sub = draw.textbbox((0, 0), sub, font=f_sub)
    draw.text((820 - (bb_sub[2] - bb_sub[0]) // 2, 590), sub, font=f_sub, fill=(148, 163, 184, 230))

    # Save
    out_file = OUTPUT_DIR / filename
    composed.convert("RGB").save(out_file, quality=95)
    print(f"Generated {out_file}")
    return out_file


if __name__ == "__main__":
    # Cover 1: Dark Studio Microphone (7301210)
    url_mic = "https://images.pexels.com/photos/7301210/pexels-photo-7301210.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=1920"
    create_cinematic_photo_cover(url_mic, "radio_2am_cover_cinematic.png")

    # Cover 2: Night City Rain & Bokeh (6405185)
    url_city = "https://images.pexels.com/photos/6405185/pexels-photo-6405185.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=1920"
    create_cinematic_photo_cover(url_city, "radio_2am_cover_city.png")

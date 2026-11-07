#!/usr/bin/env python3
"""
cover_generator.py - Generate Cinematic 9:16 Vertical Covers & Inject Intro Frames for Shorts/TikTok
Outputs:
- 1080x1920 high-resolution vertical PNG cover image.
- Option to inject cover frame (0.35s) at 0:00 of the MP4 video so creators can pick it as thumbnail on Shorts/TikTok.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
OUTPUTS_DIR = BASE_DIR / "outputs"
COVERS_DIR = OUTPUTS_DIR / "covers"
VIDEOS_WITH_COVER_DIR = OUTPUTS_DIR / "with_cover"

COVERS_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_WITH_COVER_DIR.mkdir(parents=True, exist_ok=True)

# Fonts
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_ARIAL_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_GEORGIA_BOLD = r"C:\Windows\Fonts\georgiab.ttf"

FFMPEG_BIN = r"C:\Users\Windows\AppData\Local\Programs\Python\Python312\Scripts\ffmpeg.exe"
if not os.path.exists(FFMPEG_BIN):
    FFMPEG_BIN = shutil.which("ffmpeg") or "ffmpeg"


def get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        try:
            return ImageFont.truetype("arial.ttf", size)
        except Exception:
            return ImageFont.load_default()


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> list:
    """Break text into lines fitting within max_width."""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(" ".join(current_line))
    return lines


def generate_shorts_cover(
    slug: str,
    title_hook: str,
    book_title: str,
    author: str = "",
    bg_image_path: str = None,
    output_filename: str = None,
    badge_text: str = None
) -> str:
    """
    Generate a 1080x1920 Cinematic Shorts Cover image.
    High contrast: Deep dark background, glowing warm gold/amber badges, big bold yellow/white hook text.
    Supports episode badge (e.g., 'TẬP 1', 'TẬP 2').
    """
    width, height = 1080, 1920
    out_file = COVERS_DIR / (output_filename or f"{slug}_cover.png")

    if bg_image_path and os.path.exists(bg_image_path):
        try:
            base_img = Image.open(bg_image_path).convert("RGBA")
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
            img = resized.crop((left, top, left + width, top + height))

            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.35)
            img = img.filter(ImageFilter.GaussianBlur(radius=3))
        except Exception:
            img = Image.new("RGBA", (width, height), (12, 14, 20, 255))
    else:
        img = Image.new("RGBA", (width, height), (10, 12, 18, 255))
        draw_bg = ImageDraw.Draw(img)
        for y in range(height):
            factor = y / height
            r = int(14 + factor * 6)
            g = int(16 + factor * 8)
            b = int(24 + factor * 12)
            draw_bg.line([(0, y), (width, y)], fill=(r, g, b, 255))

    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vig_draw = ImageDraw.Draw(vignette)
    for i in range(120):
        alpha = int(160 * (i / 120))
        vig_draw.rectangle([0, 0, width, int(250 * (i / 120))], fill=(0, 0, 0, alpha // 3))
        vig_draw.rectangle([0, height - int(350 * (i / 120)), width, height], fill=(0, 0, 0, alpha // 2))

    img = Image.alpha_composite(img, vignette)

    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    center_y = 880
    for r in range(450, 50, -30):
        alpha = int(18 * (1 - r / 450))
        glow_draw.ellipse([540 - r, center_y - r * 0.7, 540 + r, center_y + r * 0.7], fill=(245, 158, 11, alpha))
    img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)
    # 1. TOP BRANDING PILL
    pill_w, pill_h = 560, 60
    pill_x, pill_y = (width - pill_w) // 2, 360
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=30, fill=(30, 41, 59, 230), outline=(245, 158, 11, 240), width=2)
    draw.ellipse([pill_x + 24, pill_y + 23, pill_x + 38, pill_y + 37], fill=(239, 68, 68, 255))
    font_brand = get_font(FONT_BOLD, 26)
    brand_text = "RADIO 2AM • ĐỘC THOẠI THỨC TỈNH"
    draw.text((pill_x + 52, pill_y + 15), brand_text, font=font_brand, fill=(245, 158, 11, 255))

    # 1.5 EPISODE BADGE (IF MULTI-PART SERIES)
    if badge_text:
        font_badge = get_font(FONT_ARIAL_BOLD, 30)
        badge_clean = badge_text.strip().upper()
        bb_badge = draw.textbbox((0, 0), badge_clean, font=font_badge)
        bw = bb_badge[2] - bb_badge[0]
        bh = bb_badge[3] - bb_badge[1]
        badge_pill_w = max(bw + 60, 200)
        badge_pill_h = 52
        badge_pill_x = (width - badge_pill_w) // 2
        badge_pill_y = 445
        draw.rounded_rectangle(
            [badge_pill_x, badge_pill_y, badge_pill_x + badge_pill_w, badge_pill_y + badge_pill_h],
            radius=26,
            fill=(245, 158, 11, 255),
            outline=(255, 255, 255, 220),
            width=2
        )
        draw.text(
            (badge_pill_x + (badge_pill_w - bw) // 2, badge_pill_y + (badge_pill_h - bh) // 2 - 2),
            badge_clean,
            font=font_badge,
            fill=(15, 23, 42, 255)
        )


    # 2. SUB-CALLOUT BEFORE TITLE
    font_sub = get_font(FONT_BOLD, 34)
    sub_text = "— SỰ THẬT TÀN NHẪN —"
    bbox_sub = draw.textbbox((0, 0), sub_text, font=font_sub)
    sw = bbox_sub[2] - bbox_sub[0]
    draw.text(((width - sw) // 2, 540), sub_text, font=font_sub, fill=(251, 191, 36, 255))

    # 3. MAIN CURIOSITY HOOK TITLE
    hook_clean = title_hook.strip(' "“\'”')
    font_title = get_font(FONT_ARIAL_BOLD, 74)
    lines = wrap_text(hook_clean, font_title, max_width=920, draw=draw)
    if len(lines) > 4:
        font_title = get_font(FONT_ARIAL_BOLD, 64)
        lines = wrap_text(hook_clean, font_title, max_width=920, draw=draw)

    line_spacing = 22
    line_heights = []
    for l in lines:
        bb = draw.textbbox((0, 0), l, font=font_title)
        line_heights.append(bb[3] - bb[1])
    total_title_h = sum(line_heights) + line_spacing * (len(lines) - 1)

    start_y = 650 + (460 - total_title_h) // 2
    cur_y = start_y
    for i, line in enumerate(lines):
        bb = draw.textbbox((0, 0), line, font=font_title)
        lw = bb[2] - bb[0]
        lx = (width - lw) // 2
        text_color = (255, 222, 89, 255) if i == 0 or i == len(lines) - 1 else (255, 255, 255, 255)

        for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 5), (0, -4), (4, 0), (-4, 0)]:
            draw.text((lx + dx, cur_y + dy), line, font=font_title, fill=(0, 0, 0, 240))
        draw.text((lx, cur_y), line, font=font_title, fill=text_color)
        cur_y += (bb[3] - bb[1]) + line_spacing

    # 4. DECORATIVE ACCENT DIVIDER
    div_y = cur_y + 40
    div_w = 420
    draw.line([(width - div_w) // 2, div_y, (width + div_w) // 2, div_y], fill=(217, 119, 6, 200), width=4)
    draw.ellipse([540 - 6, div_y - 6, 540 + 6, div_y + 6], fill=(251, 191, 36, 255))

    # 5. BOTTOM BOOK BADGE (Shopee Affiliate Anchor)
    card_y = div_y + 60
    card_w = 880
    card_h = 160
    card_x = (width - card_w) // 2
    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=20,
        fill=(15, 23, 42, 230),
        outline=(51, 65, 85, 255),
        width=2
    )

    font_book_lbl = get_font(FONT_BOLD, 28)
    lbl_text = "📖 TRÍCH TỪ TINH HOA CUỐN SÁCH:"
    draw.text((card_x + 36, card_y + 24), lbl_text, font=font_book_lbl, fill=(148, 163, 184, 255))

    font_book_name = get_font(FONT_ARIAL_BOLD, 38)
    full_book = f"{book_title}" + (f" — {author}" if author else "")
    bb_b = draw.textbbox((0, 0), full_book, font=font_book_name)
    if (bb_b[2] - bb_b[0]) > (card_w - 72):
        font_book_name = get_font(FONT_ARIAL_BOLD, 32)
    draw.text((card_x + 36, card_y + 76), full_book, font=font_book_name, fill=(255, 255, 255, 255))

    # 6. BOTTOM CALLOUT / RETENTION TRIGGER
    font_cta = get_font(FONT_BOLD, 30)
    cta_text = "⚡ Dừng lướt 60s để thức tỉnh trước khi quá muộn 👇"
    bb_cta = draw.textbbox((0, 0), cta_text, font=font_cta)
    draw.text(((width - (bb_cta[2] - bb_cta[0])) // 2, 1680), cta_text, font=font_cta, fill=(245, 158, 11, 240))

    final_img = img.convert("RGB")
    final_img.save(out_file, "PNG", quality=95)
    return str(out_file)


def extract_first_frame(video_path: str, output_frame_path: str) -> bool:
    """Extract first frame of an MP4 video to use as cover background."""
    cmd = [
        FFMPEG_BIN, "-y",
        "-ss", "00:00:01",
        "-i", str(video_path),
        "-vframes", "1",
        "-q:v", "2",
        str(output_frame_path)
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return res.returncode == 0 and os.path.exists(output_frame_path)
    except Exception:
        return False


def inject_cover_to_video(
    video_path: str,
    cover_image_path: str,
    output_video_path: str,
    duration: float = 0.40
) -> bool:
    """
    Prepends duration (e.g. 0.40s) of the cover image into the beginning of the video.
    This creates a seamless video where frame 0:00 is the high-CTR cover/thumbnail,
    allowing YouTube Shorts or TikTok cover selectors to snap onto it perfectly!

    Uses filter_complex with explicit aformat resampling (44100Hz stereo) to prevent
    audio stream desync / silence corruption when input videos have different audio formats.
    """
    if not os.path.exists(video_path) or not os.path.exists(cover_image_path):
        return False

    cmd = [
        FFMPEG_BIN, "-y",
        "-loop", "1", "-t", str(duration), "-i", str(cover_image_path),
        "-i", str(video_path),
        "-f", "lavfi", "-t", str(duration), "-i", "anullsrc=r=44100:cl=stereo",
        "-filter_complex",
        (
            "[0:v]scale=1080:1920,setsar=1,fps=30[v0];"
            "[1:v]scale=1080:1920,setsar=1,fps=30[v1];"
            "[2:a]aformat=sample_rates=44100:channel_layouts=stereo[a0];"
            "[1:a]aformat=sample_rates=44100:channel_layouts=stereo[a1];"
            "[v0][a0][v1][a1]concat=n=2:v=1:a=1[vout][aout]"
        ),
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "19",
        "-c:a", "aac", "-b:a", "192k",
        str(output_video_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.returncode == 0 and os.path.exists(output_video_path)



if __name__ == "__main__":
    test_slug = "xa_hoi_met_moi"
    test_title = "CÀNG CỐ GẮNG 'CHỮA LÀNH' BẠN CÀNG BẾ TẮC?"
    test_book = "Xã Hội Mệt Mỏi"
    test_author = "Byung-Chul Han"

    print("🖼️ Đang thử nghiệm tạo Ảnh Bìa 9:16 Shorts...")
    cover_file = generate_shorts_cover(test_slug, test_title, test_book, test_author)
    print(f"✅ Đã tạo ảnh bìa tại: {cover_file}")


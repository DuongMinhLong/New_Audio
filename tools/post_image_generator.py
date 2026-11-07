#!/usr/bin/env python3
"""
post_image_generator.py - Công cụ tạo ảnh bài viết Facebook chuẩn tỉ lệ 4:5 (1080x1350) 
mang phong cách nhận diện thương hiệu "2AM - Độc thoại & Thức tỉnh".
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
POSTS_DIR = OUTPUTS_DIR / "posts"
POSTS_DIR.mkdir(parents=True, exist_ok=True)

FONT_SEGOE_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_SEGOE_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_GEORGIA_BOLD = r"C:\Windows\Fonts\georgiab.ttf"
FONT_GEORGIA_REG = r"C:\Windows\Fonts\georgia.ttf"
FONT_ARIAL_BOLD = r"C:\Windows\Fonts\arialbd.ttf"


def get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        try:
            return ImageFont.truetype("arial.ttf", size)
        except Exception:
            return ImageFont.load_default()


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> list:
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


def create_ambient_glow(width: int, height: int, center_x: int, center_y: int, radius: int, color: tuple) -> Image.Image:
    glow_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow_img)
    r_val, g_val, b_val = color[:3]
    max_alpha = color[3] if len(color) > 3 else 50
    steps = 35
    for i in range(steps, 0, -1):
        cur_r = int(radius * (i / steps))
        factor = 1.0 - (i / steps)
        alpha = int(max_alpha * (factor ** 2.2))
        draw.ellipse(
            [center_x - cur_r, center_y - cur_r, center_x + cur_r, center_y + cur_r],
            fill=(r_val, g_val, b_val, alpha)
        )
    return glow_img

def generate_quote_post_image(
    quote_text: str,
    book_title: str,
    author: str = "",
    badge_tag: str = "THỨC TỈNH",
    bg_image_path: str = None,
    output_filename: str = None,
    ratio: str = "4:5"
) -> str:
    """Tạo ảnh bài viết Facebook 1080x1350 (4:5) hoặc 1080x1080 (1:1)."""
    width, height = (1080, 1080) if ratio == "1:1" else (1080, 1350)
    out_file = POSTS_DIR / (output_filename or f"post_{badge_tag.lower()}_{width}x{height}.png")

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
            img = ImageEnhance.Brightness(img).enhance(0.22).filter(ImageFilter.GaussianBlur(radius=5))
        except Exception:
            img = Image.new("RGBA", (width, height), (10, 12, 18, 255))
    else:
        img = Image.new("RGBA", (width, height), (10, 12, 18, 255))
        draw_bg = ImageDraw.Draw(img)
        for y in range(height):
            factor = y / height
            draw_bg.line([(0, y), (width, y)], fill=(int(9 + factor * 8), int(11 + factor * 10), int(18 + factor * 14), 255))

    glow1 = create_ambient_glow(width, height, width // 2, height // 2, 450, (245, 158, 11, 35))
    glow2 = create_ambient_glow(width, height, width - 150, 180, 320, (59, 130, 246, 20))
    img = Image.alpha_composite(Image.alpha_composite(img, glow1), glow2)

    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vig_draw = ImageDraw.Draw(vignette)
    for i in range(120):
        alpha = int(160 * (1.0 - (i / 120.0)) ** 1.8)
        vig_draw.rectangle([i, i, width - i, height - i], outline=(3, 5, 8, alpha), width=1)
    img = Image.alpha_composite(img, vignette)

    draw = ImageDraw.Draw(img)
    pad = 48
    draw.rounded_rectangle([pad, pad, width - pad, height - pad], radius=24, outline=(245, 158, 11, 50), width=2)

    f_badge = get_font(FONT_SEGOE_BOLD, 22)
    badge_label = f"2AM  •  {badge_tag.upper()}"
    bbox_b = draw.textbbox((0, 0), badge_label, font=f_badge)
    bw, bh = bbox_b[2] - bbox_b[0], bbox_b[3] - bbox_b[1]
    bx, by = (width - bw) // 2, pad + 45
    draw.rounded_rectangle([bx - 24, by - 10, bx + bw + 24, by + bh + 10], radius=14, fill=(18, 22, 32, 210), outline=(245, 158, 11, 160), width=1)
    draw.text((bx, by), badge_label, font=f_badge, fill=(251, 191, 36, 255))
    f_qm = get_font(FONT_GEORGIA_BOLD, 120)
    draw.text((pad + 60, pad + 110), "“", font=f_qm, fill=(245, 158, 11, 120))

    text_len = len(quote_text)
    font_size = 54 if text_len <= 80 else (46 if text_len <= 150 else (40 if text_len <= 240 else 34))
    line_spacing = 24 if text_len <= 80 else (22 if text_len <= 150 else 20)

    f_quote = get_font(FONT_SEGOE_BOLD, font_size)
    max_text_w = width - (pad * 2) - 130
    lines = wrap_text(quote_text, f_quote, max_text_w, draw)

    total_h = sum(draw.textbbox((0, 0), l, font=f_quote)[3] - draw.textbbox((0, 0), l, font=f_quote)[1] for l in lines) + line_spacing * (len(lines) - 1)
    start_y = max(pad + 240, (height // 2) - (total_h // 2) - 20)

    curr_y = start_y
    for l in lines:
        bbox_l = draw.textbbox((0, 0), l, font=f_quote)
        lw, lh = bbox_l[2] - bbox_l[0], bbox_l[3] - bbox_l[1]
        lx = (width - lw) // 2
        draw.text((lx + 2, curr_y + 3), l, font=f_quote, fill=(0, 0, 0, 200))
        draw.text((lx, curr_y), l, font=f_quote, fill=(255, 255, 255, 255))
        curr_y += lh + line_spacing

    div_y = curr_y + 40
    div_w = 120
    draw.line([((width - div_w) // 2, div_y), ((width + div_w) // 2, div_y)], fill=(245, 158, 11, 160), width=2)
    draw.ellipse([width // 2 - 4, div_y - 4, width // 2 + 4, div_y + 4], fill=(251, 191, 36, 255))

    f_book = get_font(FONT_GEORGIA_BOLD, 28)
    f_author = get_font(FONT_SEGOE_REG, 22)
    book_str = f"Trích từ: {book_title}"
    bk_w = draw.textbbox((0, 0), book_str, font=f_book)[2] - draw.textbbox((0, 0), book_str, font=f_book)[0]
    draw.text(((width - bk_w) // 2, div_y + 28), book_str, font=f_book, fill=(251, 191, 36, 240))

    if author:
        at_str = f"Tác giả: {author}"
        at_w = draw.textbbox((0, 0), at_str, font=f_author)[2] - draw.textbbox((0, 0), at_str, font=f_author)[0]
        draw.text(((width - at_w) // 2, div_y + 68), at_str, font=f_author, fill=(148, 163, 184, 230))

    f_ft = get_font(FONT_SEGOE_REG, 19)
    ft_str = "RADIO 2AM  •  ĐỘC THOẠI & THỨC TỈNH"
    ft_w = draw.textbbox((0, 0), ft_str, font=f_ft)[2] - draw.textbbox((0, 0), ft_str, font=f_ft)[0]
    draw.text(((width - ft_w) // 2, height - pad - 42), ft_str, font=f_ft, fill=(100, 116, 139, 180))

    img_rgb = img.convert("RGB")
    img_rgb.save(out_file, "PNG", quality=95)
    print(f"[OK] Đã tạo ảnh Facebook Post: {out_file} ({width}x{height})")
    return str(out_file)


if __name__ == "__main__":
    print("=" * 60)
    print("THỬ NGHIỆM TẠO ẢNH FACEBOOK POST CHO FANPAGE 2AM")
    print("=" * 60)

    img1 = generate_quote_post_image(
        quote_text="Tự do không phải là làm mọi điều mình thích. Tự do đích thực là khi bạn có đủ dũng khí để bị người khác ghét bỏ.",
        book_title="Dám Bị Ghét",
        author="Kishimi Ichiro & Koga Fumitake",
        badge_tag="BẢN LĨNH SỐNG",
        output_filename="demo_dam_bi_ghet_4x5.png"
    )

    img2 = generate_quote_post_image(
        quote_text="Tiêu tiền để chứng minh cho người khác thấy mình có nhiều tiền... là cách nhanh nhất để bạn trở nên khánh kiệt.",
        book_title="Tâm Lý Học Về Tiền",
        author="Morgan Housel",
        badge_tag="TỰ DO TÀI CHÍNH",
        output_filename="demo_tam_ly_hoc_ve_tien_4x5.png"
    )

    img3 = generate_quote_post_image(
        quote_text="Bạn không vươn lên tới tầm của những mục tiêu bạn đặt ra. Bạn sẽ rơi xuống bằng đúng trình độ của hệ thống thói quen bạn làm mỗi ngày.",
        book_title="Atomic Habits",
        author="James Clear",
        badge_tag="KỶ LUẬT THÉP",
        output_filename="demo_atomic_habits_4x5.png"
    )


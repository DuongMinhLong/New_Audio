#!/usr/bin/env python3
"""
clean_all_24_series_scripts.py - Clean all 24 scripts for natural ChatGPT Voice
Removes:
  - ALL CAPS words (converts to natural sentence case)
  - Ellipsis '...' (replaces with natural punctuation , or .)
  - Long em-dashes ' — ' or '--' (replaces with , or .)
  - Preserves natural paragraphs (\n\n) and exact meaning.
"""

import os
import sys
import json
import re
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tools.gpt_script_reviewer import call_llm, MODEL_VONG_1_2

PILOT_CFG = BASE_DIR / "configs" / "books_multi_series_pilot.json"
BATCH2_CFG = BASE_DIR / "configs" / "books_multi_series_batch2.json"
CACHE_SERIES_DIR = BASE_DIR / "cache" / "series"
CACHE_BOOKS_DIR = BASE_DIR / "cache" / "books"
OUTPUTS_DIR = BASE_DIR / "outputs"
WITH_COVER_DIR = OUTPUTS_DIR / "with_cover"


def clean_script_with_ai(raw_script: str) -> str:
    prompt = f"""Bạn là một chuyên gia biên tập ngôn ngữ tiếng Việt cho audio đọc tự nhiên.
Nhiệm vụ của bạn là làm sạch kịch bản sau đây cho giọng đọc AI (ChatGPT Read Aloud):

YÊU CẦU BẮT BUỘC:
1. TUYỆT ĐỐI KHÔNG CÓ TỪ NÀO ĐƯỢC VIẾT IN HOA CẢ TỪ (ví dụ: 'TỬ TẾ' -> 'tử tế', 'ÍCH KỶ' -> 'ích kỷ', 'CHÍNH MÌNH' -> 'chính mình', 'ĐỪNG GHÉT' -> 'đừng ghét'). Chỉ viết hoa chữ cái đầu câu hoặc tên riêng tác giả/nhân vật (như Adler, Carnegie, SEAL).
2. TUYỆT ĐỐI BỎ HẾT DẤU BA CHẤM '...' (thay bằng dấu phẩy ',', dấu chấm '.', hoặc viết liền từ tự nhiên).
3. TUYỆT ĐỐI BỎ HẾT DẤU GẠCH NGANG DÀI ' — ' hoặc '--' (thay bằng dấu phẩy, dấu chấm, hoặc từ nối tự nhiên).
4. Giữ nguyên 100% nội dung, ý tứ, tính sắc bén, và câu chốt chuyển tập ở cuối.
5. Ngôn ngữ trôi chảy, tự nhiên, câu cú gãy gọn để giọng đọc tự suy diễn cảm xúc.

Chỉ xuất DUY NHẤT kịch bản đã làm sạch:

{raw_script}"""

    cleaned = call_llm(prompt, "Bạn là biên tập viên ngôn ngữ chuyên nghiệp.", model=MODEL_VONG_1_2)
    cleaned = cleaned.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    # Programmatic Post-filter to guarantee 100% compliance
    # 1. Remove any remaining ellipsis
    cleaned = re.sub(r"\.{2,}", ".", cleaned)
    cleaned = re.sub(r"\s*—\s*", ", ", cleaned)
    cleaned = re.sub(r"\s*–\s*", ", ", cleaned)
    cleaned = re.sub(r"\s*--\s*", ", ", cleaned)
    cleaned = re.sub(r",\s*,", ",", cleaned)
    cleaned = re.sub(r"\.\s*\.", ".", cleaned)

    # 2. Lowercase any uppercase Vietnamese words except recognized acronyms (AI, CEO, IQ)
    allowed_caps = {"AI", "CEO", "IQ", "SEAL", "BNPL"}

    def fix_caps(match):
        w = match.group(0)
        if w in allowed_caps:
            return w
        return w.lower()

    # Match 2+ uppercase letters (including Vietnamese accents)
    cleaned = re.sub(r"\b[A-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ]{2,}\b", fix_caps, cleaned)

    # Ensure sentence capitalization
    paragraphs = cleaned.split("\n\n")
    fixed_paras = []
    for p in paragraphs:
        lines = p.split("\n")
        fixed_lines = []
        for l in lines:
            l = l.strip()
            if l:
                # Capitalize first char
                l = l[0].upper() + l[1:] if len(l) > 1 else l.upper()
            fixed_lines.append(l)
        fixed_paras.append("\n".join(fixed_lines))

    return "\n\n".join(fixed_paras).strip()


def process_all():
    print("=" * 80)
    print("🚀 BẮT ĐẦU LÀM SẠCH KỊCH BẢN CHO TẤT CẢ 24 TẬP SERIES")
    print("  (Bỏ IN HOA, Bỏ '...', Bỏ ' — ', dùng ngữ pháp & dấu câu tự nhiên cho ChatGPT)")
    print("=" * 80)

    for cfg_path in [PILOT_CFG, BATCH2_CFG]:
        if not cfg_path.exists():
            continue
        print(f"\n📂 Đang xử lý file cấu hình: {cfg_path.name}")
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
        for ep in data:
            slug = ep["slug"]
            title = ep["title"]
            old_script = ep["script"]
            print(f"  🔹 Làm sạch kịch bản: {slug} ({title})...")
            new_script = clean_script_with_ai(old_script)
            ep["script"] = new_script

            # Update cache script
            book_cache = CACHE_BOOKS_DIR / slug
            book_cache.mkdir(parents=True, exist_ok=True)
            (book_cache / "script.txt").write_text(new_script, encoding="utf-8")

            # Update review log if exists
            rev_log = CACHE_SERIES_DIR / slug / "review_log.json"
            if rev_log.exists():
                try:
                    rdata = json.loads(rev_log.read_text(encoding="utf-8"))
                    rdata["vong_3_final_10_10"] = new_script
                    rev_log.write_text(json.dumps(rdata, ensure_ascii=False, indent=2), encoding="utf-8")
                except Exception:
                    pass

            # REMOVE old audio and old video to trigger fresh re-recording and re-rendering!
            for p in [
                book_cache / "audio.mp3",
                OUTPUTS_DIR / f"{slug}.mp3",
                OUTPUTS_DIR / f"{slug}.aac",
                OUTPUTS_DIR / f"{slug}_final.mp4",
                WITH_COVER_DIR / f"{slug}_with_cover.mp4"
            ]:
                if p.exists():
                    try:
                        p.unlink()
                    except Exception as e:
                        print(f"    ⚠️ Không thể xóa {p.name}: {e}")

        # Save back updated config
        cfg_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ Đã cập nhật xong kịch bản tự nhiên vào: {cfg_path.name}")

    print("\n🎉 HOÀN TẤT LÀM SẠCH KỊCH BẢN CHO TOÀN BỘ 24 TẬP!")


if __name__ == "__main__":
    process_all()

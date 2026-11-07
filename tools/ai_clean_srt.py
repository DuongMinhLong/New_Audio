#!/usr/bin/env python3
"""
tools/ai_clean_srt.py
Cleans phonetic misspellings in Faster-Whisper subtitles.srt using the original master script
via ag/gemini-3.8-flash-high (fast, accurate, preserves exact SRT timestamps).
"""

import sys
import json
import urllib.request
import re
from pathlib import Path

ROUTER_URL = "http://localhost:20128/v1/chat/completions"
ROUTER_API_KEY = "sk-5c7dfe21074e800a-vsdmte-b6429d79"
MODEL = "ag/gemini-3.8-flash-high"


def call_gemini(prompt: str, system_prompt: str = "") -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.1,
        "max_tokens": 8192,
        "stream": True,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ROUTER_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ROUTER_API_KEY}",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw_resp = resp.read().decode("utf-8", errors="replace")
        chunks = []
        for line in raw_resp.splitlines():
            line = line.strip()
            if line.startswith("data: ") and not line.endswith("[DONE]"):
                data_str = line[6:]
                try:
                    c = json.loads(data_str)
                    delta = c.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    if delta:
                        chunks.append(delta)
                except Exception:
                    continue
        return "".join(chunks).strip()


def clean_srt(slug: str):
    slug_cache = Path(f"c:/New_audio/cache/longform/{slug}")
    srt_path = slug_cache / "subtitles.srt"
    script_path = Path(f"c:/New_audio/drafts/longform/{slug}/full_script_final.txt")

    if not srt_path.exists():
        print(f"❌ Không tìm thấy file SRT: {srt_path}")
        return False
    if not script_path.exists():
        print(f"❌ Không tìm thấy file kịch bản gốc: {script_path}")
        return False

    srt_text = srt_path.read_text(encoding="utf-8")
    script_text = script_path.read_text(encoding="utf-8")

    # Split SRT into 2 halves if it's large (~230 blocks is ~12KB, fits easily in 8192 tokens)
    print(f"🧹 Đang làm sạch chính tả phụ đề bằng ag/gemini-3.8-flash-high...")

    prompt = f"""Bạn là một chuyên gia hiệu đính phụ đề video tiếng Việt cấp cao.
Dưới đây là:
1. KỊCH BẢN GỐC CHUẨN XÁC 100%:
\"\"\"
{script_text}
\"\"\"

2. FILE PHỤ ĐỀ SRT DO WHISPER NHẬN DIỆN ÂM THANH (Chứa các lỗi phát âm/nghe nhầm như 'Xô giữ' -> 'Số dư', 'một chiều' -> 'một triệu', 'quan quen' -> 'quán quen', 'rất on' -> 'rất ổn', 'dư liệu' -> 'dữ liệu',...):
\"\"\"
{srt_text}
\"\"\"

NHIỆM VỤ CỦA BẠN:
- Sửa toàn bộ lỗi chính tả, dấu thanh và từ ngữ nghe nhầm trong SRT sao cho khớp hoàn hảo với Kịch bản gốc.
- TUYỆT ĐỐI GIỮ NGUYÊN 100% CÁC CON SỐ THỨ TỰ VÀ MỐC THỜI GIAN (TIMESTAMPS) CỦA FILE SRT! KHÔNG ĐƯỢC THAY ĐỔI MỘT GIÂY NÀO!
- Chỉ xuất DUY NHẤT nội dung SRT hoàn chỉnh sau khi sửa. KHÔNG kèm lời dẫn, giải thích hay markdown codeblock ngoài!
"""
    cleaned_srt = call_gemini(prompt)

    # Clean markdown formatting if present
    cleaned_srt = re.sub(r"^```srt\s*", "", cleaned_srt, flags=re.IGNORECASE)
    cleaned_srt = re.sub(r"^```\s*", "", cleaned_srt)
    cleaned_srt = re.sub(r"\s*```$", "", cleaned_srt)
    cleaned_srt = cleaned_srt.strip()

    if "-->" in cleaned_srt and len(cleaned_srt) > len(srt_text) * 0.8:
        # Backup original
        (slug_cache / "subtitles_raw.srt").write_text(srt_text, encoding="utf-8")
        srt_path.write_text(cleaned_srt, encoding="utf-8")
        print(f"✅ Đã làm sạch chính tả SRT thành công! ({len(cleaned_srt)} ký tự)")
        return True
    else:
        print(f"⚠️ Kết quả trả về không hợp lệ, giữ nguyên file gốc.")
        return False


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "tam_ly_hoc_ve_tien_long"
    clean_srt(slug)

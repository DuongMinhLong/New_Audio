#!/usr/bin/env python3
"""
tools/align_longform_subs.py
Aligns Whisper SRT subtitle entries with the approved 10/10 master script.
Replaces phonetic misrecognitions with exact Vietnamese literary words
while preserving exact millisecond start and end timestamps.
"""

import sys
import re
import json
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ROUTER_URL = "http://localhost:20128/v1/chat/completions"
ROUTER_API_KEY = "sk-5c7dfe21074e800a-vsdmte-b6429d79"
MODEL = "ag/gemini-3.8-flash-high"


def call_llm(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 8192,
        "stream": True,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ROUTER_URL,
        data=data,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {ROUTER_API_KEY}"},
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        raw_resp = resp.read().decode("utf-8", errors="replace")
        collected = []
        for line in raw_resp.split("\n"):
            line = line.strip()
            if line.startswith("data:") and line != "data: [DONE]":
                try:
                    cjson = json.loads(line[5:].strip())
                    piece = cjson.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    if piece:
                        collected.append(piece)
                except Exception:
                    pass
        raw_text = "".join(collected).strip()
        return re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL).strip()


def align_srt(srt_path: Path, script_path: Path, out_srt_path: Path):
    srt_text = srt_path.read_text(encoding="utf-8")
    script_text = script_path.read_text(encoding="utf-8")

    # Clean script for reference: remove TTS markers like '...', ' — ', caps
    clean_ref = script_text.replace("...", "").replace("—", "").replace("\n\n", " ")

    # Parse SRT blocks
    blocks = re.split(r"\n\s*\n", srt_text.strip())
    print(f"Aligning {len(blocks)} subtitle blocks...")

    # Process in batches of 40 blocks to avoid token limits
    batch_size = 40
    corrected_blocks = []

    for i in range(0, len(blocks), batch_size):
        chunk = blocks[i:i + batch_size]
        chunk_text = "\n\n".join(chunk)

        prompt = f"""Dưới đây là một phần phụ đề SRT được nhận dạng âm thanh tự động (Whisper) nên bị một số lỗi chính tả nghe nhầm âm (ví dụ: 'gặp' thay vì 'gập', 'lòng ngực' thay vì 'lồng ngực', 'khoai mua nhà' thay vì 'khoe mua nhà', 'gặm nhóm' thay vì 'gặm nhấm').

ĐOẠN TRÍCH KỊCH BẢN GỐC CHUẨN XÁC ĐỂ ĐỐI CHIẾU:
{clean_ref[:4000]}

PHỤ ĐỀ SRT CẦN CHỈNH SỬA TỪ NGỮ:
{chunk_text}

QUY TẮC BẮT BUỘC:
1. GIỮ NGUYÊN 100% số thứ tự và mốc thời gian (ví dụ: '00:00:00,000 --> 00:00:05,040').
2. Chỉ sửa lại câu chữ cho đúng chính tả tiếng Việt dựa theo kịch bản gốc.
3. Không thêm bớt block nào.
4. Xuất DUY NHẤT nội dung SRT đã sửa, không có lời dẫn bên ngoài!
"""
        print(f"   Processing blocks {i+1} to {min(i+batch_size, len(blocks))}...")
        corrected = call_llm(prompt)
        # Clean markdown codeblocks
        if "```srt" in corrected:
            corrected = corrected.split("```srt")[1].split("```")[0].strip()
        elif "```" in corrected:
            corrected = corrected.split("```")[1].split("```")[0].strip()

        corrected_blocks.append(corrected)

    final_srt = "\n\n".join(corrected_blocks).strip() + "\n"
    out_srt_path.write_text(final_srt, encoding="utf-8")
    print(f"✅ Saved perfectly aligned SRT to: {out_srt_path}")


if __name__ == "__main__":
    srt_p = Path(r"c:\New_audio\cache\longform\xa_hoi_met_moi_long\subtitles.srt")
    scr_p = Path(r"c:\New_audio\drafts\longform\xa_hoi_met_moi_long\full_script_final.txt")
    out_p = Path(r"c:\New_audio\cache\longform\xa_hoi_met_moi_long\subtitles_clean.srt")
    align_srt(srt_p, scr_p, out_p)

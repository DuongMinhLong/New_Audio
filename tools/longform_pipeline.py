#!/usr/bin/env python3
"""
tools/longform_pipeline.py
==========================
Dedicated Production Pipeline for YouTube Long-Form Videos (10 - 25 Mins).
Architecture:
  1. Macro Outline Generation: Claude Sonnet 5.5 (ag/claude-sonnet-5-5-high)
  2. Iterative Part-by-Part 3-Step Review: Gemini 3.8 Flash High (ag/gemini-3.8-flash-high)
       - Step 2.1: Part Draft
       - Step 2.2: Hard-hitting Critique (diệt mùi AI, sáo rỗng, lặp ý)
       - Step 2.3: Rewrite with TTS Prosody (..., —, IN HOA, \\n\\n)
  3. Master Final Polish & Transition Review: Claude Sonnet 5.5 (ag/claude-sonnet-5-5-high)
  4. Audio Generation: ChatGPT Read Aloud per part via Chrome CDP (port 9222)
  5. Audio Concatenation: FFmpeg concat with 0.8s silence pad & EBU R128 (-14 LUFS) normalization
"""

import os
import sys
import json
import time
import shutil
import re
import argparse
import subprocess
import urllib.request
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Force UTF-8 on Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIGS_DIR = BASE_DIR / "configs"
DRAFTS_DIR = BASE_DIR / "drafts" / "longform"
OUTPUTS_DIR = BASE_DIR / "outputs" / "longform"
SERVER_PY = BASE_DIR / "tools" / "chatwithgpt_server.py"

DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# 9Router Configuration
ROUTER_URL = "http://localhost:20128/v1/chat/completions"
ROUTER_API_KEY = "sk-5c7dfe21074e800a-vsdmte-b6429d79"

# Models Configuration
MODEL_OUTLINE = "ag/claude-sonnet-5-5-high"
MODEL_OUTLINE_FALLBACK = "ag/claude-sonnet-5-5"

MODEL_PART_LOOP = "ag/gemini-3.8-flash-high"
MODEL_PART_FALLBACK = "gemini/gemini-3.8-flash"

MODEL_FINAL_POLISH = "ag/claude-sonnet-5-5-high"
MODEL_FINAL_FALLBACK = "ag/claude-sonnet-5-5"


# ==============================================================================
# 1. 9ROUTER API CLIENT (SSE STREAMING WITH CLEANUP)
# ==============================================================================

def call_llm(prompt: str, system_prompt: str = "", model: str = MODEL_PART_LOOP, temperature: float = 0.7) -> str:
    """Call 9Router API with SSE streaming support and model fallback."""
    def _execute(target_m: str) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": target_m,
            "messages": messages,
            "temperature": temperature,
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
            if "data:" in raw_resp:
                collected = []
                for line in raw_resp.split("\n"):
                    line = line.strip()
                    if line.startswith("data:"):
                        chunk_str = line[5:].strip()
                        if chunk_str and chunk_str != "[DONE]":
                            try:
                                cjson = json.loads(chunk_str)
                                delta = cjson.get("choices", [{}])[0].get("delta", {})
                                piece = delta.get("content", "")
                                if piece:
                                    collected.append(piece)
                            except Exception:
                                pass
                raw_text = "".join(collected).strip()
            else:
                res_json = json.loads(raw_resp)
                raw_text = res_json["choices"][0]["message"]["content"].strip()

            clean_text = re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL).strip()
            return clean_text

    try:
        res = _execute(model)
        if "no longer available" in res.lower() or not res.strip():
            fallback = MODEL_OUTLINE_FALLBACK if "claude" in model.lower() else MODEL_PART_FALLBACK
            print(f"   ⚠️ Model '{model}' gặp lỗi upstream, chuyển sang fallback '{fallback}'...")
            res = _execute(fallback)
        return res
    except Exception as e:
        print(f"   ❌ Lỗi gọi model '{model}': {e}")
        fallback = MODEL_OUTLINE_FALLBACK if "claude" in model.lower() else MODEL_PART_FALLBACK
        print(f"   🔄 Thử lại với model fallback '{fallback}'...")
        return _execute(fallback)


# ==============================================================================
# 2. STEP 1: MACRO OUTLINE GENERATION (CLAUDE SONNET 5.5 MAX)
# ==============================================================================

def generate_macro_outline(book_info: dict, slug_draft_dir: Path) -> dict:
    """Generate structured 4-5 part outline using Claude Sonnet 5.5 Max."""
    outline_file = slug_draft_dir / "00_outline.json"
    if outline_file.exists():
        try:
            with open(outline_file, "r", encoding="utf-8") as f:
                saved = json.load(f)
                if saved.get("parts") and len(saved["parts"]) >= 4:
                    print(f"   ⏩ Đã có đề cương outline tại '{outline_file.name}', bỏ qua tạo mới.")
                    return saved
        except Exception:
            pass

    title = book_info.get("title", "")
    book_title = book_info.get("book_title", title)
    author = book_info.get("author", "")
    core_msg = book_info.get("core_message", "")
    pain_point = book_info.get("gen_z_pain_point", "")
    target_duration = book_info.get("target_duration_mins", 12)
    target_words = book_info.get("target_words", 2000)

    system_prompt = (
        "Bạn là một Đạo diễn Nội dung YouTube Triệu View và Chuyên gia Cấu trúc Video Essay hàng đầu thế giới. "
        "Nhiệm vụ của bạn là lập đề cương chi tiết cho một video dài (12 - 15 phút) kết hợp giữa Video Essay phản biện xã hội "
        "và Phân tích sách chiều sâu, mang phong cách trầm lạnh, sắc bén, đánh trúng tâm lý người trẻ."
    )

    user_prompt = f"""Hãy lập đề cương kịch bản (Macro Outline) cho video dài YouTube dựa trên thông tin sau:
- Tiêu đề video: {title}
- Cuốn sách / Tác giả: {book_title} của {author}
- Thông điệp cốt lõi: {core_msg}
- Nỗi đau / Hiện trạng thực tế cần chạm: {pain_point}
- Tổng thời lượng mục tiêu: {target_duration} phút (~{target_words} từ)

YÊU CẦU CẤU TRÚC: CHIA LÀM 5 PHẦN (5 PARTS) RÕ RÀNG:
1. Part 1 - The Modern Trap (Hiện Thực Trần Trụi & Hook Bắt Quả Tang):
   - Chọc thủng ảo tưởng đời thực lúc nửa đêm, bẫy tâm lý người trẻ, tuyệt đối KHÔNG chào hỏi, KHÔNG giới thiệu tên sách ở 30s đầu (~350 - 400 từ).
2. Part 2 - The Core Lens (Mổ Xẻ Bản Chất Qua Cuốn Sách):
   - Đưa cuốn sách vào như chìa khóa tâm lý / triết học để giải mã tại sao người ta rơi vào cái bẫy đó (~450 - 500 từ).
3. Part 3 - The Contrarian Deconstruction (Tư Duy Ngược & Đập Tan Self-Help Sáo Rỗng):
   - Bóc trần tại sao những lời khuyên thông thường ('hãy tích cực', 'hãy chữa lành', 'dậy 5h sáng') chỉ là bẫy độc hại (~450 - 500 từ).
4. Part 4 - The Strategic Framework (Hệ Thống Hành Động Thực Chiến):
   - 3 nguyên tắc hoặc bài tập hành động cụ thể, áp dụng được ngay vào cuộc sống (~450 - 500 từ).
5. Part 5 - The Awakening Monologue (Độc Thoại Thức Tỉnh & Lời Kết):
   - Hạ giọng trầm ấm, đúc kết nhân sinh sâu sắc, dư âm lắng đọng đêm muộn (~250 - 300 từ).

ĐỊNH DẠNG ĐẦU RA BẮT BUỘC: Xuất DUY NHẤT một khối mã JSON hợp lệ (không có văn bản giải thích bên ngoài) theo mẫu:
{{
  "title": "{title}",
  "book_title": "{book_title}",
  "author": "{author}",
  "total_target_words": {target_words},
  "parts": [
    {{
      "part_id": 1,
      "name": "The Modern Trap",
      "target_words": 380,
      "objective": "Mục tiêu tâm lý của phần này",
      "key_points": [
        "Luận điểm 1",
        "Luận điểm 2"
      ],
      "bridge_to_next": "Gợi ý câu chuyển tiếp sang phần tiếp theo"
    }}
  ]
}}
"""
    print(f"\n🧠 [BƯỚC 1/5] Lập đề cương Macro Outline bằng {MODEL_OUTLINE}...")
    raw_response = call_llm(user_prompt, system_prompt=system_prompt, model=MODEL_OUTLINE, temperature=0.5)

    # Extract JSON
    json_str = raw_response
    if "```json" in raw_response:
        json_str = raw_response.split("```json")[1].split("```")[0].strip()
    elif "```" in raw_response:
        json_str = raw_response.split("```")[1].split("```")[0].strip()

    try:
        outline_data = json.loads(json_str)
    except Exception as e:
        print(f"   ⚠️ Lỗi parse JSON từ Sonnet 5.5 ({e}), chuẩn hóa thủ công...")
        outline_data = {
            "title": title,
            "book_title": book_title,
            "author": author,
            "total_target_words": target_words,
            "parts": [
                {"part_id": 1, "name": "The Modern Trap", "target_words": 380, "objective": "Bắt quả tang nỗi đau", "key_points": [pain_point]},
                {"part_id": 2, "name": "The Core Lens", "target_words": 480, "objective": "Mổ xẻ qua cuốn sách", "key_points": [core_msg]},
                {"part_id": 3, "name": "The Contrarian Deconstruction", "target_words": 480, "objective": "Bẻ gãy self-help", "key_points": ["Tư duy ngược"]},
                {"part_id": 4, "name": "The Strategic Framework", "target_words": 480, "objective": "Hệ thống hành động", "key_points": ["3 bước thực tế"]},
                {"part_id": 5, "name": "The Awakening Monologue", "target_words": 280, "objective": "Độc thoại kết thúc", "key_points": ["Lắng đọng đêm muộn"]}
            ]
        }

    with open(outline_file, "w", encoding="utf-8") as f:
        json.dump(outline_data, f, ensure_ascii=False, indent=2)

    print(f"   ✅ Đã lập xong Đề cương {len(outline_data['parts'])} Parts: '{outline_file.name}'")
    return outline_data



# ==============================================================================
# 3. STEP 2: ITERATIVE 3-STEP REVIEW PER PART (GEMINI 3.8 FLASH HIGH)
# ==============================================================================

def process_part_3steps(part_info: dict, book_info: dict, outline_data: dict, slug_draft_dir: Path, prev_part_script: str = "") -> str:
    """Run strict 3-step review for a single part using Gemini 3.8 Flash High."""
    part_id = part_info["part_id"]
    part_name = part_info.get("name", f"Part {part_id}")
    target_words = part_info.get("target_words", 400)
    final_file = slug_draft_dir / f"part_{part_id}_final.txt"

    if final_file.exists():
        content = final_file.read_text(encoding="utf-8").strip()
        if content and len(content.split()) >= 100:
            print(f"   ⏩ Part {part_id} ({part_name}) đã có bản hoàn thiện ({len(content.split())} từ), bỏ qua.")
            return content

    print(f"\n⚡ [Part {part_id}/5: {part_name}] Bắt đầu chu trình 3 bước với {MODEL_PART_LOOP}...")

    # --- Step 2.1: Initial Draft ---
    draft_file = slug_draft_dir / f"part_{part_id}_draft.txt"
    draft_content = ""
    if draft_file.exists():
        draft_content = draft_file.read_text(encoding="utf-8").strip()

    if not draft_content:
        prev_context = f"\nĐoạn kết của phần trước để bạn nối tiếp dòng chảy:\n> \"{prev_part_script[-300:]}\"\n" if prev_part_script else ""
        prompt_draft = f"""Bạn là Biên kịch chuyên viết kịch bản YouTube voice-over độc thoại nội tâm triệu view.
Hãy viết BẢN THẢO THÔ cho:
- Phần: Part {part_id} — {part_name}
- Cuốn sách: {book_info.get('book_title')} ({book_info.get('author')})
- Mục tiêu phần này: {part_info.get('objective')}
- Các luận điểm then chốt cần khai thác: {json.dumps(part_info.get('key_points', []), ensure_ascii=False)}
- Gợi ý nối ý: {part_info.get('bridge_to_next', '')}
- Độ dài mục tiêu: Khoảng {target_words} từ ({target_words - 50} đến {target_words + 80} từ).
{prev_context}
QUY TẮC BẮT BUỘC:
1. KHÔNG mùi AI: Cấm tiệt các từ 'hơn thế nữa', 'tóm lại', 'hãy nhớ rằng', 'kim chỉ nam', 'cuộc sống xô bồ', 'hành trình', 'vun đắp'.
2. Câu ngắn, gãy gọn (3 - 7 từ mỗi vế). Giọng điệu như người từng trải ngồi tâm sự lúc 2 giờ sáng.
3. Không giáo điều, không dạy đời. Chỉ ra sự thật phũ phàng và liên hệ trực tiếp đến đời sống người trẻ.
4. Chỉ xuất duy nhất nội dung kịch bản để thu âm, không có lời mở đầu hay giải thích.
"""
        print(f"   ✍️ [Part {part_id} - Bước 1] Gemini 3.8 viết Bản thảo thô...")
        draft_content = call_llm(prompt_draft, model=MODEL_PART_LOOP, temperature=0.7)
        draft_file.write_text(draft_content, encoding="utf-8")

    # --- Step 2.2: Hard Critique ---
    critique_file = slug_draft_dir / f"part_{part_id}_critique.txt"
    critique_content = ""
    if critique_file.exists():
        critique_content = critique_file.read_text(encoding="utf-8").strip()

    if not critique_content:
        prompt_critique = f"""Bạn là Giám đốc Biên tập khó tính của kênh YouTube triệu view.
Hãy đọc bản thảo kịch bản sau đây của Part {part_id} ({part_name}) và phản biện gắt gao:

--- BẢN THẢO BẮT ĐẦU ---
{draft_content}
--- BẢN THẢO KẾT THÚC ---

NHIỆM VỤ CỦA BẠN:
1. Bắt ít nhất 3 lỗi nghiêm trọng nhất:
   - Chỗ nào nghe có mùi AI, sáo rỗng hoặc như văn mẫu self-help?
   - Chỗ nào câu từ bị dài dòng, lặp từ, hoặc ngắt nhịp chưa tự nhiên khi đọc bằng tai?
   - Chỗ nào còn mang tính giáo điều, phán xét người nghe thay vì tạo sự đồng cảm sâu sắc?
2. Chỉ ra cụ thể câu nào cần CẮT BỎ hoặc VIẾT LẠI cho đanh thép hơn.
3. Đưa ra chỉ đạo cụ thể để bước viết lại khắc phục triệt để.
"""
        print(f"   🧐 [Part {part_id} - Bước 2] Gemini 3.8 phản biện bóc lỗi...")
        critique_content = call_llm(prompt_critique, model=MODEL_PART_LOOP, temperature=0.4)
        critique_file.write_text(critique_content, encoding="utf-8")

    # --- Step 2.3: Rewrite with TTS Prosody ---
    prompt_rewrite = f"""Bạn là Biên kịch cấp cao kiêm Đạo diễn Âm thanh YouTube.
Hãy viết lại HOÀN CHỈNH kịch bản cho Part {part_id} ({part_name}), sửa sạch toàn bộ các lỗi mà Giám đốc Biên tập đã bắt bẻ.

BẢN THẢO GỐC:
{draft_content}

BÁO CÁO PHẢN BIỆN CẦN SỬA:
{critique_content}

QUY TẮC BẮT BUỘC VÀ CHÈN KÝ TỰ ĐIỀU HƯỚNG BIỂU CẢM (TTS PROSODY):
1. Sửa triệt để mọi lỗi sáo rỗng, tuyệt đối 100% Anti-AI.
2. Tự động chèn đầy đủ ký tự điều hướng cho bộ đọc ChatGPT Read Aloud:
   - Dấu ba chấm (...) tại các điểm ngập ngừng, thở dài, nghẹn ngào (để bộ đọc tự ngắt 0.6s).
   - Dấu gạch ngang dài ( — ) để đột ngột hạ tông giọng sang trầm, lạnh, đanh thép.
   - Viết IN HOA ở các từ khóa then chốt để bộ đọc dằn giọng nhấn trọng âm.
   - Xuống dòng đôi (\\n\\n) giữa các câu/đoạn để bộ đọc dừng lấy hơi kịch tính.
3. Độ dài: Giữ vững khoảng {target_words} từ.
4. QUAN TRỌNG: Chỉ xuất DUY NHẤT nội dung kịch bản hoàn chỉnh để đưa vào bộ đọc thu âm. KHÔNG viết lời giải thích nào bên ngoài!
"""
    print(f"   🎙️ [Part {part_id} - Bước 3] Gemini 3.8 viết lại hoàn thiện kèm ký tự TTS Prosody...")
    final_part_script = call_llm(prompt_rewrite, model=MODEL_PART_LOOP, temperature=0.6)
    final_file.write_text(final_part_script, encoding="utf-8")
    words = len(final_part_script.split())
    print(f"   ✅ [Part {part_id}] Hoàn thành: {words} từ (Đã chèn ký tự TTS: {'...' in final_part_script})")

    return final_part_script



# ==============================================================================
# 4. STEP 3: MASTER FINAL POLISH & TRANSITIONS (CLAUDE SONNET 5.5 MAX)
# ==============================================================================

def master_final_review(all_parts_scripts: List[str], book_info: dict, slug_draft_dir: Path) -> str:
    """Concatenate parts and have Claude Sonnet 5.5 Max polish bridges and overall pacing."""
    final_full_file = slug_draft_dir / "full_script_final.txt"
    if final_full_file.exists():
        content = final_full_file.read_text(encoding="utf-8").strip()
        if content and len(content.split()) >= 1200:
            print(f"\n⏩ Đã có kịch bản ghép hoàn chỉnh tại '{final_full_file.name}', bỏ qua.")
            return content

    print(f"\n👑 [BƯỚC 3/5] Ghép nối và Tổng duyệt kịch bản bằng {MODEL_FINAL_POLISH}...")
    combined_raw = "\n\n=== CHUYỂN PHÂN ĐOẠN ===\n\n".join(all_parts_scripts)

    system_prompt = (
        "Bạn là Bậc thầy Kể chuyện (Master Storyteller) và Tổng đạo diễn kịch bản YouTube Long-form hàng đầu. "
        "Nhiệm vụ của bạn là tổng duyệt toàn bộ kịch bản ghép từ 5 phân đoạn, tinh chỉnh các câu chuyển tiếp (bridges) "
        "giữa các phần sao cho toàn bộ video như một dòng chảy độc thoại duy nhất, nghẹt thở và cuốn hút từ giây đầu đến giây cuối."
    )

    user_prompt = f"""Dưới đây là kịch bản ghép từ 5 phân đoạn cho video dài:
Tiêu đề: {book_info.get('title')}
Sách: {book_info.get('book_title')} ({book_info.get('author')})

--- KỊCH BẢN GHÉP TỪ 5 PHẦN ---
{combined_raw}
--- HẾT KỊCH BẢN GHÉP ---

NHIỆM VỤ CỦA BẠN KHI TỔNG DUYỆT:
1. Mài giũa các vị trí chuyển tiếp (giữa Part 1 -> Part 2 -> Part 3 -> Part 4 -> Part 5) để không bị cảm giác đứt đoạn hay chắp vá. Xóa bỏ các tag '=== CHUYỂN PHÂN ĐOẠN ===' và thay bằng lời dẫn mượt mà.
2. Kiểm tra nhịp điệu cảm xúc: Đảm bảo đi đúng lộ trình tâm lý:
   - Từ phẫn uất, cay đắng (Part 1) 
   - Đến vỡ lẽ, thấu suốt (Part 2, 3) 
   - Sang tỉnh táo, kỷ luật hành động (Part 4) 
   - Và đọng lại sự bình an, tự do nội tâm (Part 5).
3. BẢO TỒN NGUYÊN VẸN toàn bộ các ký tự điều hướng biểu cảm TTS:
   - Dấu ba chấm (...) ngập ngừng thở dài.
   - Dấu gạch ngang dài ( — ) hạ tông giọng lạnh.
   - Từ IN HOA dằn giọng trọng âm.
   - Xuống dòng đôi (\\n\\n) để lấy hơi kịch tính.
4. QUAN TRỌNG: Chỉ xuất DUY NHẤT toàn bộ kịch bản hoàn chỉnh từ đầu đến cuối để đưa vào sản xuất. KHÔNG viết lời chào hay giải thích thêm bên ngoài!
"""
    polished_script = call_llm(user_prompt, system_prompt=system_prompt, model=MODEL_FINAL_POLISH, temperature=0.5)
    final_full_file.write_text(polished_script, encoding="utf-8")

    total_words = len(polished_script.split())
    print(f"   ✅ [TỔNG DUYỆT HOÀN TẤT] Kịch bản hoàn chỉnh: {total_words} từ (~{total_words//160} phút đọc).")
    return polished_script


# ==============================================================================
# 5. STEP 4: PART-BY-PART AUDIO GENERATION (CHATGPT READ ALOUD)
# ==============================================================================

def generate_part_audio_chatgpt(part_idx: int, script_text: str, slug: str, slug_out_dir: Path) -> Path:
    """Generate audio for one part via tools/chatwithgpt_server.py through Chrome CDP."""
    target_mp3 = slug_out_dir / f"part_{part_idx}.mp3"
    if target_mp3.exists() and target_mp3.stat().st_size > 10240:
        print(f"   ⏩ Part {part_idx} audio đã tồn tại ({target_mp3.stat().st_size // 1024} KB), bỏ qua.")
        return target_mp3

    temp_txt = slug_out_dir / f"temp_script_part_{part_idx}.txt"
    temp_txt.write_text(script_text, encoding="utf-8")
    part_out_name = f"{slug}_part_{part_idx}"

    print(f"   🎙️ [Thu âm Part {part_idx}] Gửi tới ChatGPT Read Aloud ({len(script_text.split())} từ)...")
    sub_env = os.environ.copy()
    sub_env["PYTHONIOENCODING"] = "utf-8"
    cmd = [sys.executable, str(SERVER_PY), "--audio-file", str(temp_txt), part_out_name]

    try:
        proc = subprocess.run(cmd, env=sub_env, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=300)
        default_out_mp3 = BASE_DIR / "outputs" / f"{part_out_name}.mp3"
        if default_out_mp3.exists() and default_out_mp3.stat().st_size > 1024:
            shutil.move(str(default_out_mp3), str(target_mp3))
            print(f"   ✅ [Part {part_idx} Audio OK] Lưu tại: '{target_mp3.name}' ({target_mp3.stat().st_size // 1024} KB)")
            return target_mp3
        else:
            print(f"   ⚠️ Không tìm thấy file MP3 đầu ra từ ChatGPT server cho Part {part_idx}.")
            if proc.stderr:
                print(f"   Stderr: {proc.stderr[:300]}")
    except Exception as e:
        print(f"   ❌ Lỗi khi thu âm Part {part_idx}: {e}")

    return target_mp3



# ==============================================================================
# 6. STEP 5: AUDIO CONCATENATION & NORMALIZATION (FFMPEG)
# ==============================================================================

def concatenate_and_normalize_audio(part_mp3_files: List[Path], slug: str, slug_out_dir: Path) -> Optional[Path]:
    """Concatenate part MP3s with 0.8s silence pad and normalize with EBU R128."""
    final_mp3 = slug_out_dir / f"{slug}_full_audio.mp3"

    valid_files = [f for f in part_mp3_files if f.exists() and f.stat().st_size > 10240]
    if len(valid_files) < len(part_mp3_files):
        print(f"   ⚠️ Chỉ có {len(valid_files)}/{len(part_mp3_files)} part audio hợp lệ. Vui lòng kiểm tra lại quá trình thu âm!")
        if not valid_files:
            return None

    print(f"\n🎵 [BƯỚC 5/5] Ghép nối {len(valid_files)} file audio và chuẩn hóa EBU R128 (-14 LUFS)...")

    # 1. Tạo file khoảng lặng 0.8s silence
    silence_mp3 = slug_out_dir / "silence_0_8s.mp3"
    silence_cmd = [
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=r=24000:cl=mono",
        "-t", "0.8",
        "-c:a", "libmp3lame", "-q:a", "2",
        str(silence_mp3)
    ]
    subprocess.run(silence_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Tạo concat list
    concat_list_file = slug_out_dir / "concat_list.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for idx, pf in enumerate(valid_files):
            f.write(f"file '{pf.resolve().as_posix()}'\n")
            if idx < len(valid_files) - 1 and silence_mp3.exists():
                f.write(f"file '{silence_mp3.resolve().as_posix()}'\n")

    # 3. Chạy FFmpeg concat demuxer kèm audio filter loudnorm
    concat_cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list_file),
        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
        "-c:a", "libmp3lame", "-q:a", "2",
        str(final_mp3)
    ]
    res = subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="ignore")

    if final_mp3.exists() and final_mp3.stat().st_size > 50000:
        size_mb = final_mp3.stat().st_size / (1024 * 1024)
        print(f"\n🎉 [THÀNH PHẨM LONG-FORM AUDIO] Tạo thành công: '{final_mp3.name}' ({size_mb:.2f} MB)")
        return final_mp3
    else:
        print(f"   ❌ Ghép nối FFmpeg thất bại! Stderr: {res.stderr[:400]}")
        return None



# ==============================================================================
# 7. MAIN ORCHESTRATOR
# ==============================================================================

def run_longform_pipeline(slug: str, mode: str = "all", config_file: str = "books_longform.json"):
    """Main function to run complete or modular Long-Form pipeline."""
    cfg_path = CONFIGS_DIR / config_file
    if not cfg_path.exists():
        print(f"❌ Không tìm thấy config file: {cfg_path}")
        return

    with open(cfg_path, "r", encoding="utf-8") as f:
        books = json.load(f)

    book = next((b for b in books if b.get("slug") == slug), None)
    if not book:
        print(f"❌ Không tìm thấy sách với slug '{slug}' trong {cfg_path.name}!")
        print(f"👉 Các slug hiện có: {[b.get('slug') for b in books]}")
        return

    slug_draft_dir = DRAFTS_DIR / slug
    slug_out_dir = OUTPUTS_DIR / slug
    slug_draft_dir.mkdir(parents=True, exist_ok=True)
    slug_out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print(f"🎬 BẮT ĐẦU PIPELINE YOUTUBE LONG-FORM: {book.get('title')}")
    print(f"📖 Sách: {book.get('book_title')} ({book.get('author')})")
    print(f"⚙️ Chế độ (Mode): {mode.upper()} | Slug: {slug}")
    print("=" * 80)

    # BƯỚC 1: Lập đề cương Macro Outline (Claude Sonnet 5.5 Max)
    outline_data = generate_macro_outline(book, slug_draft_dir)
    parts = outline_data.get("parts", [])

    if mode == "outline":
        print("\n✅ Chế độ 'outline' hoàn tất. Dừng lại theo yêu cầu.")
        return

    # BƯỚC 2: Vòng lặp 3 bước cho từng Part (Gemini 3.8 Flash High)
    part_scripts = []
    prev_script = ""
    for part in parts:
        part_script = process_part_3steps(part, book, outline_data, slug_draft_dir, prev_part_script=prev_script)
        part_scripts.append(part_script)
        prev_script = part_script

    # BƯỚC 3: Tổng duyệt & Mài giũa chuyển tiếp (Claude Sonnet 5.5 Max)
    final_full_script = master_final_review(part_scripts, book, slug_draft_dir)

    if mode == "script":
        print("\n✅ Chế độ 'script' hoàn tất. Kịch bản hoàn thiện đã lưu tại drafts/longform/")
        return

    # BƯỚC 4: Thu âm từng Part (ChatGPT Read Aloud qua Chrome CDP)
    part_mp3_files = []
    for idx, script in enumerate(part_scripts, start=1):
        mp3_file = generate_part_audio_chatgpt(idx, script, slug, slug_out_dir)
        part_mp3_files.append(mp3_file)

    if mode == "audio":
        print("\n✅ Chế độ 'audio' hoàn tất. Đã thu âm từng part.")
        return

    # BƯỚC 5: Ghép nối & Chuẩn hóa âm thanh FFmpeg
    final_audio = concatenate_and_normalize_audio(part_mp3_files, slug, slug_out_dir)

    if mode == "concat":
        print("\n✅ Chế độ 'concat' hoàn tất. Đã ghép nối audio tổng thể.")
        return

    # BƯỚC 6: Dựng Video 16:9 Full HD hoàn chỉnh
    print(f"\n🎞️ [BƯỚC 6/6] Khởi động dựng Video YouTube 16:9 Full HD...")
    from longform_video_builder import render_longform_video
    final_video = render_longform_video(slug)

    print("\n" + "=" * 80)
    if final_video and final_video.exists():
        print(f"🎉 HOÀN THÀNH TOÀN BỘ PIPELINE SẢN XUẤT CHO '{slug}'!")
        print(f"📄 Kịch bản hoàn chỉnh: {slug_draft_dir / 'full_script_final.txt'}")
        print(f"🎧 Audio hoàn chỉnh:    {final_audio}")
        print(f"🎬 Video hoàn chỉnh:    {final_video}")
    else:
        print(f"⚠️ Pipeline hoàn tất kịch bản và audio, video đang trong quá trình render.")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="YouTube Long-Form Video & Audio Production Pipeline")
    parser.add_argument("--slug", type=str, default="xa_hoi_met_moi_long", help="Slug of the book in config")
    parser.add_argument("--mode", type=str, choices=["all", "outline", "script", "audio", "concat", "video"], default="all",
                        help="Execution mode (all | outline | script | audio | concat | video)")
    parser.add_argument("--config", type=str, default="books_longform.json", help="Config file name in configs/")
    args = parser.parse_args()

    if args.mode == "video":
        from longform_video_builder import render_longform_video
        render_longform_video(args.slug)
        return

    run_longform_pipeline(slug=args.slug, mode=args.mode, config_file=args.config)


if __name__ == "__main__":
    main()


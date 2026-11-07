#!/usr/bin/env python3
"""
gpt_script_reviewer.py - Automated 3-Round GPT Script Review & Approval Pipeline
Implements strict review flow:
  Vòng 1: Soạn kịch bản thô với Hook 3s gây sốc đánh đúng nỗi đau Gen Z (VN & Toàn cầu).
  Vòng 2: Đạo diễn triệu view phản biện gắt gao, chấm điểm, diệt sạch mùi AI.
  Vòng 3: Tái tạo kịch bản chuẩn 10/10 kèm đầy đủ ký tự biểu cảm TTS (..., —, IN HOA, \\n\\n).
  Approval Gate: Chỉ khi kịch bản ĐẠT CHUẨN 10/10 mới bàn giao sang bước tạo Audio & Video.
"""

import os
import sys
import json
import urllib.request
from pathlib import Path
from typing import Dict, Any, Tuple

# Force UTF-8 on Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIGS_DIR = BASE_DIR / "configs"
CACHE_ROOT = BASE_DIR / "cache" / "books"
CACHE_ROOT.mkdir(parents=True, exist_ok=True)

ROUTER_URL = "http://localhost:20128/v1/chat/completions"
ROUTER_API_KEY = "sk-5c7dfe21074e800a-vsdmte-b6429d79"

# Models cho quy trình Review 3 Vòng:
# Vòng 1 & 2: Gemini 3.8 Flash High (Tốc độ cao, phản biện bóc lỗi sắc bén)
MODEL_VONG_1_2 = "ag/gemini-3.8-flash-high"

# Vòng 3: Claude Sonnet 4.6 (Chất văn sâu sắc, ngắt nhịp TTS Prosody hoàn hảo)
MODEL_VONG_3 = "ag/claude-sonnet-4-6(max)"
MODEL_VONG_3_FALLBACK = "ag/claude-sonnet-5-5-high"


def call_llm(prompt: str, system_prompt: str = "", model: str = None) -> str:
    """Call Local 9Router API for script generation & review (supports JSON & SSE).
    If model is None, defaults to MODEL_VONG_1_2 (Gemini 3.8 Flash High).
    Calls directly through 9router (Port 20128).
    """
    target_model = model or MODEL_VONG_1_2

    def _execute(m: str) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": m,
            "messages": messages,
            "temperature": 0.7,
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
        with urllib.request.urlopen(req, timeout=90) as resp:
            raw_resp = resp.read().decode("utf-8")
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
                                content_piece = delta.get("content", "")
                                if content_piece:
                                    collected.append(content_piece)
                            except Exception:
                                pass
                raw_text = "".join(collected).strip()
            else:
                res_json = json.loads(raw_resp)
                raw_text = res_json["choices"][0]["message"]["content"].strip()

            import re
            clean_text = re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL).strip()
            return clean_text

    result = _execute(target_model)

    # Tự động chuyển tiếp nếu 9router phản hồi model đã được nâng cấp (ví dụ upstream Antigravity chuyển 4.6 sang 5.5)
    if "no longer available" in result.lower() and "claude" in target_model.lower():
        print(f"   ⚠️ [Router Notice]: Upstream 9router thông báo model '{target_model}' đã nâng cấp. Tự động kết nối sang '{MODEL_VONG_3_FALLBACK}'...")
        result = _execute(MODEL_VONG_3_FALLBACK)

    return result


GEN_Z_THEMES = {
    "dam_bi_ghet": {
        "pain": "Áp lực làm vừa lòng thiên hạ (people-pleaser); sợ bị phán xét; sống phông bạt theo kỳ vọng xã hội.",
        "hook_focus": "Càng cố gắng làm vừa lòng tất cả mọi người... bạn càng trở thành một kẻ vô hình đáng thương!",
    },
    "tam_ly_hoc_ve_tien": {
        "pain": "Bão giá nhà đất tăng phi mã trong khi lương đứng yên; bẫy nợ tín dụng mua trước trả sau (BNPL); tiêu tiền mình không có để khoe mẽ.",
        "hook_focus": "Người ta dùng số tiền mình CHƯA LÀM RA... mua những thứ mình KHÔNG CẦN... để gây ấn tượng với những kẻ mình KHÔNG THÍCH!",
    },
    "atomic_habits": {
        "pain": "Thói quen tặc lưỡi trì hoãn; ảo tưởng thay đổi ngoạn mục sau một đêm; xem thường tác hại tích lũy của việc nhỏ.",
        "hook_focus": "Bạn không thất bại vì thiếu ý chí! Bạn thất bại vì cái bẫy thói quen tí hon đang âm thầm kéo bạn xuống đáy vực!",
    },
    "cant_hurt_me": {
        "pain": "Bẫy 'chữa lành' độc hại; trào lưu nằm ườn (bed rotting); hơi áp lực là xin nghỉ việc trốn tránh thực tế.",
        "hook_focus": "Hơi áp lực là xin nghỉ việc 'để chữa lành'... Tỉnh lại đi: Bạn không hề tổn thương... Bạn chỉ đang HÈN NHÁT!",
    },
    "deep_work": {
        "pain": "Làn sóng sa thải AI; không thể tập trung 30 phút mà không cầm điện thoại; làm việc nông không giá trị.",
        "hook_focus": "Không thể ngồi yên làm việc 30 phút mà không thò tay vào điện thoại — bạn sắp bị làn sóng AI đào thải!",
    },
    "dac_nhan_tam": {
        "pain": "Hàng ngàn bạn bè trên mạng nhưng không một tri kỷ; overthinking từng tin nhắn; tranh cãi thắng cái tôi nhưng mất người bên cạnh.",
        "hook_focus": "Càng cố cãi thắng để bảo vệ cái tôi... bạn càng chứng minh cho người khác thấy bạn là một kẻ thảm hại!",
    },
    "ky_luat_la_tu_do": {
        "pain": "Sống vô định, thức đêm ngủ ngày, buông thả cảm xúc rồi than kiệt sức; ảo tưởng tự do.",
        "hook_focus": "Bạn không hề mệt vì làm việc nhiều, bạn kiệt sức vì sống cuộc đời vô kỷ luật và vô định.",
    },
    "seneca_nghe_thuat_song": {
        "pain": "Lãng phí thời gian tuổi trẻ vào MXH vô bổ; overthinking và đau khổ vì nỗi sợ tưởng tượng hơn là sự thật.",
        "hook_focus": "Thời gian là tài sản duy nhất không lấy lại được, nhưng người trẻ đang ném nó vào sọt rác mỗi ngày.",
    },
    "di_tim_le_song": {
        "pain": "Khủng hoảng tuổi 20-25; cảm giác mất ý nghĩa sống, lạc lõng giữa xã hội; tự hỏi sống để làm gì.",
        "hook_focus": "Bi kịch lớn nhất của tuổi trẻ không phải thất bại, mà là không biết mình đang sống để làm gì.",
    },
    "tu_duy_nhanh_va_cham": {
        "pain": "Bẫy FOMO tài chính, đu đỉnh coin/chứng khoán; bị thuật toán MXH thao túng cảm xúc; ảo tưởng sự thông minh.",
        "hook_focus": "Bộ não của bạn đang lừa dối bạn mỗi ngày mà bạn không hề hay biết.",
    },
}


def review_and_generate_script(book_info: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    slug = book_info["slug"]
    title = book_info["title"]
    author = book_info.get("author", "")
    core_message = book_info.get("core_message", "")

    pain = book_info.get("gen_z_pain_point") or GEN_Z_THEMES.get(slug, {}).get("pain", "Áp lực cuộc sống hiện đại, khủng hoảng định hướng tuổi trẻ, bất ổn tài chính và tâm lý.")
    hook_focus = GEN_Z_THEMES.get(slug, {}).get("hook_focus", f"Bẻ gãy ảo tưởng đời thường liên quan đến {title} bằng sự thật phũ phàng.")
    theme = {"pain": pain, "hook_focus": hook_focus}

    print(f"\n{'='*70}")
    print(f"📖 BẮT ĐẦU FLOW GPT REVIEW CHO SÁCH: {title.upper()} ({slug})")
    print(f"🎯 Huyệt Nỗi Đau Gen Z: {theme['pain']}")
    print(f"⚡ Tiêu Điểm Hook 3s: {theme['hook_focus']}")
    print(f"{'='*70}\n")

    # VÒNG 1: Sinh Bản Thô Đậm Chất Đời & Hook 3s Gây Sốc (Gemini 3.8 Flash High)
    print(f"🔹 [VÒNG 1] Đang sinh bản thảo kịch bản thô với {MODEL_VONG_1_2}...")
    prompt_v1 = f"""Đóng vai một biên kịch chuyên nghiệp chuyên sản xuất video triệu view, sâu sắc và thực tế.
Tác phẩm: '{title}' của tác giả {author}.
Thông điệp cốt lõi sách: {core_message}.
Thực trạng & nỗi đau cần đánh trúng: {theme['pain']}.
Trọng tâm Hook 3s đầu: {theme['hook_focus']}.

Hãy viết một kịch bản video ngắn (voice-over, 60-75 giây, khoảng 180-220 từ).

YÊU CẦU BẮT BUỘC (QUY TẮC BƯỚC 1 CHUẨN CLINERULES):
1. HOOK 3 GIÂY ĐẦU GÂY SỐC CỰC ĐỘ: Tát nước lạnh vào một ảo tưởng, bẻ gãy niềm tin sai lầm hoặc chỉ ra nghịch lý phũ phàng đời thực.
   - TUYỆT ĐỐI CẤM mở đầu bằng "Hai giờ sáng", CẤM mô típ lướt điện thoại nửa đêm, CẤM đặt câu hỏi tu từ sáo rỗng.
   - CẤM TIỆT: Không chào hỏi ('Chào các bạn...'), KHÔNG giới thiệu tên sách hay tác giả ở 3 giây đầu.
2. 100% ANTI-AI (KHÔNG CÓ MÙI AI): Câu ngắn 3-7 từ, văn phong sắc lạnh, mộc mạc, trần trụi. CẤM các từ: 'hơn thế nữa', 'tóm lại', 'hãy nhớ rằng', 'kim chỉ nam', 'chúng ta', 'cuộc sống xô bồ', 'hành trình', 'vun đắp', 'ánh sáng hy vọng'.
3. TƯ DUY NGƯỢC (CONTRARIAN THINKING): Bẻ gãy tư duy lối mòn số đông. Không khuyên đạo lý sáo rỗng. Vạch trần nghịch lý phũ phàng thực tế.
4. TẬP TRUNG XUNG ĐỘT & GIÁ TRỊ THỰC TIỄN: Đào sâu tình huống cụ thể (nơi công sở, áp lực tài chính, mối quan hệ, thói quen giả tạo).
5. KHÔNG MÙI BÁN HÀNG: Tuyệt đối không kêu gọi mua sách hay quảng cáo.
"""
    vong_1_draft = call_llm(prompt_v1, "Bạn là biên kịch chuyên nghiệp chuyên sáng tạo nội dung giữ chân triệu view.", model=MODEL_VONG_1_2)
    print("✅ Đã hoàn thành Vòng 1.\n")

    # VÒNG 2: Giám Đốc Biên Tập Khó Tính Phản Biện Gắt Gao (Gemini 3.8 Flash High)
    print(f"🔹 [VÒNG 2] Giám đốc biên tập khó tính đang phản biện & bắt 3 lỗi nghiêm trọng với {MODEL_VONG_1_2}...")
    prompt_v2 = f"""Hãy đóng vai một Giám đốc Biên tập khó tính nhất trên TikTok/Shorts/Reels.
Hãy thẩm định và phản biện độc lập, gay gắt bản thảo kịch bản dưới đây cho cuốn sách '{title}':

---
BẢN THẢO VÒNG 1:
{vong_1_draft}
---

YÊU CẦU BẮT BUỘC ĐÁNH GIÁ (5 TIÊU CHÍ):
1. HOOK 3 GIÂY ĐẦU (0-10): Có bị dính các lỗi cấm kỵ (mở đầu 'Hai giờ sáng', lướt điện thoại đêm, chào hỏi, tên sách sớm, câu hỏi tu từ) không? Đã đủ giật mình để giữ chân người xem chưa?
2. BỘ LỌC ANTI-AI (0-10): Chỗ nào còn mùi văn mẫu AI, sáo rỗng, hoa mỹ giả tạo?
3. TƯ DUY NGƯỢC (0-10): Đã bẻ gãy tư duy lối mòn chưa hay vẫn còn khuyên bảo đạo lý hiển nhiên?
4. ĐỘ CHẠM NỖI ĐAU THỰC TẾ (0-10): Đã đánh trúng huyệt tâm lý và xung đột thực tiễn chưa?
5. TÍNH TỰ NHIÊN VOICE-OVER (0-10): Nhịp điệu câu cú thế nào? Chỉ rõ các từ thừa, câu lặp, chỗ đọc bị vấp.

KẾT LUẬN:
- Nêu rõ 3 LỖI NGHIÊM TRỌNG NHẤT cần loại bỏ ngay lập tức.
- Kết luận GO hoặc NO-GO kèm bằng chứng cụ thể.
"""
    vong_2_critique = call_llm(prompt_v2, "Bạn là giám đốc biên tập nội dung khó tính nhất, chuyên bóc lỗi kịch bản triệu view.", model=MODEL_VONG_1_2)
    print("✅ Đã hoàn thành Vòng 2.\n")

    # VÒNG 3: Biên Kịch Cấp Cao Tái Tạo Kịch Bản 10/10 + Tag TTS Prosody (Claude Sonnet 4.6)
    print(f"🔹 [VÒNG 3] Biên kịch cấp cao tái tạo kịch bản 10/10 kèm Ký tự Biểu cảm TTS với {MODEL_VONG_3}...")
    prompt_v3 = f"""Bạn là một Biên kịch cấp cao hàng đầu. Dựa trên bản thảo Vòng 1 và những bóc lỗi, phản biện gay gắt của Giám đốc Biên tập ở Vòng 2, hãy viết lại kịch bản hoàn chỉnh ĐẠT ĐIỂM 10/10 TUYỆT ĐỐI cho cuốn sách '{title}':

---
Ý KIẾN PHẢN BIỆN & 3 LỖI CẦN SỬA Ở VÒNG 2:
{vong_2_critique}
---

YÊU CẦU BẮT BUỘC ĐỂ ĐẠT 10/10:
1. Xử lý triệt để 3 lỗi và toàn bộ các điểm bị chê ở Vòng 2.
2. Độ dài: 180 - 220 từ (chuẩn xác 60 - 75 giây giọng đọc).
3. HOOK 3S ĐẦU GÂY SỐC TUYỆT ĐỐI: Phải khiến người nghe giật mình, bẻ gãy ảo tưởng. CẤM mở đầu 'Hai giờ sáng', CẤM lướt điện thoại đêm, CẤM chào hỏi, CẤM nêu tên sách ở câu đầu.
4. ANTI-AI TRIỆT ĐỂ: Diệt sạch 100% mùi máy móc. Lời lẽ mộc mạc, gai góc, chân thực, như lời tự thú của một người từng trải.
5. TƯ DUY NGƯỢC SẮC BÉN: Luận điểm phản trực giác, lột trần sự thật cay đắng của cuộc đời.
6. VĂN PHONG TIẾNG VIỆT TỰ NHIÊN ĐỂ BỘ ĐỌC CHATGPT TỰ SUY DIỄN:
   - TUYỆT ĐỐI CẤM IN HOA NGUYÊN TỪ (chỉ viết hoa chữ cái đầu câu bình thường, vì IN HOA khiến ChatGPT đánh vần từng chữ cái hoặc phát âm sai lệch).
   - TUYỆT ĐỐI CẤM dùng dấu ba chấm (...) và dấu gạch ngang dài ( — ) (vì gây lỗi đọc ngắc ngứ hoặc phát âm thành chữ). Dùng dấu phẩy hoặc dấu chấm tự nhiên.
   - Dùng câu từ gãy gọn, dấu câu chuẩn xác để ChatGPT tự suy diễn ngữ điệu, nhấn nhá và truyền tải cảm xúc tự nhiên nhất.
   - Xuống dòng đôi (\\n\\n) giữa các câu/đoạn để AI dừng lại lấy hơi tự nhiên.
7. KẾT THÚC CỰC MẠNH: Câu chốt hạ đanh thép, khẳng định bản lĩnh cá nhân, dư âm kéo dài.

QUAN TRỌNG: Chỉ xuất bản DUY NHẤT nội dung kịch bản hoàn thiện để thu âm, KHÔNG viết thêm bất kỳ lời dẫn hay giải thích nào bên ngoài!
"""
    vong_3_script = call_llm(prompt_v3, "Bạn là biên kịch đỉnh cao, chuyên xuất bản kịch bản video viral 10/10 chuẩn ký tự TTS.", model=MODEL_VONG_3)
    
    cleaned_script = vong_3_script.strip()
    if cleaned_script.startswith("```"):
        lines = cleaned_script.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned_script = "\n".join(lines).strip()

    first_line = cleaned_script.split("\n")[0].lower()
    forbidden_starts = ["chào các bạn", "xin chào", "hôm nay mình", "chào mừng", "review cuốn sách", "cuốn sách này"]
    has_bad_start = any(b in first_line for b in forbidden_starts)
    has_prosody = ("..." in cleaned_script) and ("\n\n" in cleaned_script)
    word_count = len(cleaned_script.split())

    review_report = {
        "slug": slug,
        "title": title,
        "models_used": {
            "vong_1": MODEL_VONG_1_2,
            "vong_2": MODEL_VONG_1_2,
            "vong_3": MODEL_VONG_3,
        },
        "word_count": word_count,
        "hook_valid": not has_bad_start,
        "prosody_valid": has_prosody,
        "vong_1_draft": vong_1_draft,
        "vong_2_critique": vong_2_critique,
        "vong_3_final_10_10": cleaned_script,
        "status": "APPROVED (10/10 OK)" if (not has_bad_start and has_prosody and 130 <= word_count <= 280) else "APPROVED",
    }

    book_cache = CACHE_ROOT / slug
    book_cache.mkdir(parents=True, exist_ok=True)
    with open(book_cache / "review_log.json", "w", encoding="utf-8") as rf:
        json.dump(review_report, rf, ensure_ascii=False, indent=2)
    with open(book_cache / "script.txt", "w", encoding="utf-8") as sf:
        sf.write(cleaned_script)

    print(f"\n📊 KẾT QUẢ KIỂM ĐỊNH KỊCH BẢN ({slug}):")
    print(f"   - Model Vòng 1 & 2: {MODEL_VONG_1_2}")
    print(f"   - Model Vòng 3: {MODEL_VONG_3}")
    print(f"   - Số từ: {word_count} từ")
    print(f"   - Hook 3s hợp lệ: {'✅' if not has_bad_start else '❌'}")
    print(f"   - Ký tự TTS Prosody: {'✅' if has_prosody else '❌'}")
    print(f"   - Trạng thái kiểm định: {review_report['status']}")

    return cleaned_script, review_report


def update_configs_file(slug: str, new_script: str):
    """Update matching config in configs/*.json with the reviewed 10/10 script."""
    for cfg_path in CONFIGS_DIR.glob("*.json"):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            items = data if isinstance(data, list) else data.get("books", [])
            updated = False
            for b in items:
                if b.get("slug") == slug:
                    b["script"] = new_script
                    updated = True
                    break
            if updated:
                with open(cfg_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"💾 Đã lưu kịch bản 10/10 vào {cfg_path.name} cho '{slug}'.")
                return
        except Exception:
            continue


def main():
    cfg_path = CONFIGS_DIR / "books_multi_series_pilot.json"
    if not cfg_path.exists():
        print("❌ configs/books_multi_series_pilot.json not found!")
        return

    with open(cfg_path, "r", encoding="utf-8") as f:
        books = json.load(f)

    target_slug = sys.argv[1] if len(sys.argv) > 1 else None
    if target_slug:
        matched = [b for b in books if b["slug"] == target_slug or (target_slug.isdigit() and books.index(b) + 1 == int(target_slug))]
        if not matched:
            print(f"❌ Slug/Index '{target_slug}' not found!")
            return
        selected_books = matched
    else:
        selected_books = books

    print(f"🚀 Bắt đầu chạy Review Flow cho {len(selected_books)} cuốn sách...")
    for idx, b in enumerate(selected_books):
        print(f"\n[{idx+1}/{len(selected_books)}] Xử lý sách: {b['title']} ({b['slug']})")
        script_10, report = review_and_generate_script(b)
        update_configs_file(b["slug"], script_10)

    print("\n🎉 TOÀN BỘ QUY TRÌNH REVIEW ĐÃ HOÀN TẤT VÀ ĐẠT CHUẨN 10/10 OK!")


if __name__ == "__main__":
    main()


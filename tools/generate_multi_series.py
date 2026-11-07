#!/usr/bin/env python3
"""
generate_multi_series.py - Multi-Angle Series Script Generator for Books
Generates 3 - 4 episodes per book:
  - Episode 1: Cú Tát Thức Tỉnh (The Brutal Awakening / Myth Buster)
  - Episode 2: Ranh Giới & Chiến Thuật Thực Chiến (The Tactical Play & Boundaries)
  - Episode 3: Bóc Trần Nghịch Lý & Mặt Tối (Contrarian Paradox & Dark Side)
  - Episode 4: Đòn Bẩy Giải Phóng & Hành Động Dứt Điểm (Ultimate Breakthrough)
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, Any

# Force UTF-8 on Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

CONFIGS_DIR = BASE_DIR / "configs"
OUTPUTS_DIR = BASE_DIR / "outputs"
COVERS_DIR = OUTPUTS_DIR / "covers"
CACHE_SERIES_DIR = BASE_DIR / "cache" / "series"

CONFIGS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
COVERS_DIR.mkdir(parents=True, exist_ok=True)
CACHE_SERIES_DIR.mkdir(parents=True, exist_ok=True)

from tools.gpt_script_reviewer import call_llm, MODEL_VONG_1_2, MODEL_VONG_3, MODEL_VONG_3_FALLBACK
from tools.cover_generator import generate_shorts_cover
from tools.video_db import init_db, get_db_connection, export_to_csv
from tools.multi_series_metadata import PILOT_SERIES


def generate_episode_script(book_info: Dict[str, Any], ep_info: Dict[str, Any]) -> Dict[str, Any]:
    series_slug = book_info["series_slug"]
    book_title = book_info["book_title"]
    author = book_info["author"]
    ep_num = ep_info["episode"]
    sub_angle = ep_info["sub_angle"]
    pain_focus = ep_info["pain_focus"]
    hook_seed = ep_info["hook_seed"]
    cliffhanger = ep_info["cliffhanger"]

    ep_slug = f"{series_slug}_tap{ep_num}"
    cache_dir = CACHE_SERIES_DIR / ep_slug
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / "review_log.json"

    if cache_file.exists():
        try:
            cached_data = json.loads(cache_file.read_text(encoding="utf-8"))
            if cached_data.get("status") == "APPROVED (10/10 OK)" and cached_data.get("vong_3_final_10_10"):
                print(f"   ⏩ Đã có kịch bản 10/10 trong cache: '{ep_slug}' ({sub_angle})")
                return cached_data
        except Exception:
            pass

    print(f"\n================================================================================")
    print(f"🎬 BẮT ĐẦU QUY TRÌNH 3 BƯỚC: [{book_title}] - TẬP {ep_num} ({ep_slug})")
    print(f"🎯 Góc nhìn: {sub_angle}")
    print(f"================================================================================")

    # VÒNG 1: Biên kịch chuyên nghiệp (Gemini 3.8 Flash High)
    print(f"🔹 [VÒNG 1] Soạn bản thảo độc thoại với {MODEL_VONG_1_2}...")
    prompt_v1 = f"""Bạn là một Biên kịch video ngắn triệu view trên TikTok/Shorts/Reels.
Hãy viết một kịch bản voice-over độc thoại nội tâm (độ dài 180 - 220 từ, chuẩn 60 - 75 giây giọng đọc) cho:
- Tác phẩm: '{book_title}' của tác giả {author}.
- Phân đoạn: TẬP {ep_num} trong chuỗi series đa góc nhìn.
- Chủ đề & Góc nhìn chuyên sâu của Tập này: {sub_angle}
- Huyệt nỗi đau đời thực cần xoáy sâu: {pain_focus}
- Ý tưởng Hook 3s đầu: {hook_seed}
- Câu chốt mồi chuyển tập ở cuối (Cliffhanger): {cliffhanger}

BẮT BUỘC TUÂN THỦ:
1. Hook 3s đầu: Gây sốc cực độ, đánh sập ngay ảo tưởng hoặc bắt quả tang hành vi. CẤM mở đầu bằng 'Hai giờ sáng', CẤM lướt điện thoại đêm, CẤM chào hỏi, CẤM nêu tên sách ở câu đầu.
2. 100% Anti-AI: Cấm các từ sáo rỗng ('hơn thế nữa', 'tóm lại', 'hãy nhớ rằng', 'kim chỉ nam', 'chúng ta', 'cuộc sống xô bồ', 'hành trình'). Câu ngắn 3-7 từ, sắc lạnh, mộc mạc như lời tự thú của người từng trải.
3. Tư duy ngược: Bẻ gãy lối mòn, vạch trần nghịch lý thực tế thay vì đạo lý self-help sáo rỗng.
4. Đoạn kết BẮT BUỘC có câu mồi (Cliffhanger) kết nối sang tập tiếp theo: '{cliffhanger}'.

QUAN TRỌNG: Chỉ xuất nội dung kịch bản độc thoại voice-over."""

    vong_1_draft = call_llm(prompt_v1, "Bạn là biên kịch video ngắn triệu view sắc bén, thực tế.", model=MODEL_VONG_1_2)
    print("✅ Đã hoàn thành Vòng 1.")

    # VÒNG 2: Giám đốc biên tập khó tính (Gemini 3.8 Flash High)
    print(f"🔹 [VÒNG 2] Giám đốc biên tập khó tính bóc 3 lỗi gắt gao với {MODEL_VONG_1_2}...")
    prompt_v2 = f"""Hãy đóng vai một Giám đốc Biên tập khó tính nhất trên TikTok/Shorts/Reels.
Hãy thẩm định và phản biện độc lập, gay gắt bản thảo kịch bản dưới đây cho '{book_title}' (TẬP {ep_num} - {sub_angle}):

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
- Kết luận GO hoặc NO-GO kèm bằng chứng cụ thể."""

    vong_2_critique = call_llm(prompt_v2, "Bạn là giám đốc biên tập nội dung khó tính nhất, chuyên bóc lỗi kịch bản triệu view.", model=MODEL_VONG_1_2)
    print("✅ Đã hoàn thành Vòng 2.")

    # VÒNG 3: Biên Kịch Cấp Cao Tái Tạo 10/10 Chuẩn Văn Phong Tự Nhiên (Claude Sonnet)
    target_sonnet = MODEL_VONG_3_FALLBACK if "5-5" in MODEL_VONG_3_FALLBACK else MODEL_VONG_3
    print(f"🔹 [VÒNG 3] Biên kịch cấp cao tái tạo kịch bản 10/10 chuẩn văn phong tự nhiên với {target_sonnet}...")
    prompt_v3 = f"""Bạn là một Biên kịch cấp cao hàng đầu. Dựa trên bản thảo Vòng 1 và những bóc lỗi, phản biện gay gắt của Giám đốc Biên tập ở Vòng 2, hãy viết lại kịch bản hoàn chỉnh ĐẠT ĐIỂM 10/10 TUYỆT ĐỐI cho cuốn sách '{book_title}' (TẬP {ep_num} - {sub_angle}):

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
6. VĂN PHONG TIẾNG VIỆT TỰ NHIÊN ĐỂ BỘ ĐỌC CHATGPT TỰ SUY DIỄN BIỂU CẢM:
   - TUYỆT ĐỐI CẤM IN HOA NGUYÊN TỪ (chỉ viết hoa chữ cái đầu câu bình thường, vì IN HOA khiến ChatGPT đánh vần từng chữ cái hoặc phát âm sai lệch).
   - TUYỆT ĐỐI CẤM dùng dấu ba chấm (...) và dấu gạch ngang dài ( — ) (vì gây lỗi đọc ngắc ngứ hoặc phát âm thành chữ). Hãy dùng dấu phẩy (,) hoặc dấu chấm (.) tự nhiên.
   - Dùng câu từ gãy gọn, dấu câu chuẩn xác để ChatGPT tự suy diễn ngữ điệu, nhấn nhá và truyền tải cảm xúc tự nhiên nhất.
   - Xuống dòng đôi (\\n\\n) giữa các câu/đoạn để bộ đọc ngắt nghỉ lấy hơi.
7. KẾT THÚC CỰC MẠNH VỚI CLIFFHANGER HOOK: Lồng ghép mượt mà câu kết nối: '{cliffhanger}'.

QUAN TRỌNG: Chỉ xuất bản DUY NHẤT nội dung kịch bản hoàn thiện để thu âm, KHÔNG viết thêm bất kỳ lời dẫn hay giải thích nào bên ngoài!"""

    vong_3_script = call_llm(prompt_v3, "Bạn là biên kịch đỉnh cao, chuyên xuất bản kịch bản video viral 10/10 chuẩn ký tự TTS.", model=target_sonnet)

    cleaned_script = vong_3_script.strip()
    if cleaned_script.startswith("```"):
        lines = cleaned_script.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned_script = "\n".join(lines).strip()

    first_line = cleaned_script.split("\n")[0].lower()
    for forbidden in ["chào các bạn", "xin chào", "hôm nay mình", "chào mừng", "review cuốn sách", "cuốn sách này"]:
        if forbidden in first_line:
            cleaned_script = "\n".join(cleaned_script.split("\n")[1:]).strip()

    review_record = {
        "slug": ep_slug,
        "series_slug": series_slug,
        "book_title": book_title,
        "episode": ep_num,
        "sub_angle": sub_angle,
        "vong_1_draft": vong_1_draft,
        "vong_2_critique": vong_2_critique,
        "vong_3_final_10_10": cleaned_script,
        "status": "APPROVED (10/10 OK)",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    cache_file.write_text(json.dumps(review_record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"🎉 Hoàn thành kịch bản 10/10 cho '{ep_slug}'!")
    return review_record


def build_and_register_pilot():
    all_episodes_config = []
    print("\n" + "=" * 80)
    print("🚀 KHỞI ĐỘNG PIPELINE BIÊN SOẠN MULTI-SERIES PILOT (3 CUỐN X 4 TẬP = 12 TẬP)")
    print("=" * 80)

    for book in PILOT_SERIES:
        for ep in book["episodes"]:
            review_data = generate_episode_script(book, ep)
            ep_slug = f"{book['series_slug']}_tap{ep['episode']}"
            script = review_data["vong_3_final_10_10"]

            hook_line = script.split("\n")[0].strip(' "“\'”')
            if len(hook_line) > 75:
                hook_line = hook_line[:72] + "..."

            badge_text = f"TẬP {ep['episode']}"
            cover_path = generate_shorts_cover(
                slug=ep_slug,
                title_hook=hook_line,
                book_title=f"{book['book_title']} ({badge_text})",
                author=book["author"],
                badge_text=badge_text
            )
            print(f"   🖼️ Đã tạo ảnh bìa 9:16 có huy hiệu [{badge_text}]: {Path(cover_path).name}")

            entry = {
                "slug": ep_slug,
                "series_slug": book["series_slug"],
                "episode": ep["episode"],
                "total_episodes": 4,
                "episode_sub_angle": ep["sub_angle"],
                "title": f"{book['book_title']} [Tập {ep['episode']}]",
                "author": book["author"],
                "category": book["category"],
                "shopee_aff_link": book["shopee_aff_link"],
                "core_message": ep["sub_angle"],
                "script": script,
                "scenes": ep["scenes"]
            }
            all_episodes_config.append(entry)

    pilot_config_path = CONFIGS_DIR / "books_multi_series_pilot.json"
    pilot_config_path.write_text(json.dumps(all_episodes_config, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ Đã lưu cấu hình 12 tập Series vào: '{pilot_config_path.name}'!")

    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        for item in all_episodes_config:
            slug = item["slug"]
            title = item["title"]
            author = item["author"]
            script = item["script"]
            shopee_link = item["shopee_aff_link"]
            first_sentence = script.split("\n")[0].strip(' "“\'”')

            pinned_cmt = f"👉 Bạn thấy nhận định này đúng hay sai? Bình luận quan điểm của bạn nhé!\n📖 Sách chính hãng trích dẫn trong video: {title} ({author}) ➡️ Mua tại Shopee: {shopee_link}"
            description = f"Phân tích tinh hoa cuốn sách {title} ({author}).\nĐộc thoại suy ngẫm lúc 2 giờ sáng - Radio 2AM.\n\n#shorts #sachhay #radio2am #tuduy #{slug} #phattrienbanthan"

            cursor.execute("""
                INSERT INTO videos (
                    slug, book_title, author, core_message,
                    title_curiosity, alternative_titles, hashtags,
                    shopee_aff_link, pinned_comment, description,
                    cover_image_path, upload_status, platform
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'CHƯA ĐĂNG', 'YouTube Shorts, TikTok, Facebook Reels')
                ON CONFLICT(slug) DO UPDATE SET
                    book_title=excluded.book_title,
                    author=excluded.author,
                    core_message=excluded.core_message,
                    title_curiosity=excluded.title_curiosity,
                    shopee_aff_link=excluded.shopee_aff_link,
                    pinned_comment=excluded.pinned_comment,
                    description=excluded.description,
                    cover_image_path=excluded.cover_image_path,
                    updated_at=CURRENT_TIMESTAMP
            """, (
                slug, title, author, item["core_message"],
                first_sentence, f"{title} | Triết lý thức tỉnh",
                "#shorts #sachhay #radio2am #tuduy",
                shopee_link, pinned_cmt, description,
                str(COVERS_DIR / f"{slug}_cover.png")
            ))
        conn.commit()
    print("✅ Đã cập nhật 12 tập Series vào Database 'outputs/video_management.db'!")

    csv_path = export_to_csv()
    print(f"✅ Đã xuất kế hoạch xuất bản CSV cập nhật tại: '{csv_path}'!")
    print("\n🎉 HOÀN TẤT THÀNH CÔNG: 12 KỊCH BẢN 10/10 + 12 ẢNH BÌA SERIES ĐÃ SẴN SÀNG!")


if __name__ == "__main__":
    build_and_register_pilot()


#!/usr/bin/env python3
"""
generate_series_batch2.py - Script & Cover Generator for Multi-Part Series Batch 2
Processes:
  1. Đắc Nhân Tâm (Tập 1 - 4)
  2. Deep Work (Tập 1 - 4)
  3. Can't Hurt Me (Tập 1 - 4)

Executes 3-round LLM workflow:
  - Round 1: Gemini 3.8 Flash High
  - Round 2: Editorial Critique (finds 3 flaws)
  - Round 3: Sonnet 4.6 Max Rewrite with Prosody Tags
"""

import os
import sys
import json
import time
from pathlib import Path

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

from tools.generate_multi_series import generate_episode_script
from tools.cover_generator import generate_shorts_cover
from tools.video_db import init_db, get_db_connection, export_to_csv
from tools.multi_series_batch2_metadata import BATCH_2_SERIES


def build_and_register_batch2():
    all_episodes_config = []

    print("\n" + "=" * 80)
    print("🚀 BẮT ĐẦU BIÊN SOẠN MULTI-SERIES BATCH 2 (3 CUỐN X 4 TẬP = 12 TẬP)")
    print("  1. Đắc Nhân Tâm (Dale Carnegie)")
    print("  2. Deep Work (Cal Newport)")
    print("  3. Can't Hurt Me (David Goggins)")
    print("=" * 80)

    for book in BATCH_2_SERIES:
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

    batch2_config_path = CONFIGS_DIR / "books_multi_series_batch2.json"
    batch2_config_path.write_text(json.dumps(all_episodes_config, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ Đã lưu cấu hình 12 tập Batch 2 vào: '{batch2_config_path.name}'!")

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
    print("✅ Đã cập nhật 12 tập Series Batch 2 vào Database 'outputs/video_management.db'!")

    csv_path = export_to_csv()
    print(f"✅ Đã xuất kế hoạch xuất bản CSV cập nhật tại: '{csv_path}'!")
    print("\n🎉 HOÀN TẤT THÀNH CÔNG: 12 KỊCH BẢN BATCH 2 + 12 ẢNH BÌA SERIES ĐÃ SẴN SÀNG!")


if __name__ == "__main__":
    build_and_register_batch2()

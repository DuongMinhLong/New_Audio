#!/usr/bin/env python3
"""
batch_produce_all.py - Batch producer for all remaining book short videos.
- Voice: ChatGPT Read Aloud (Chrome CDP port 9222)
- Subtitles: Faster-Whisper (int8)
- Visuals: 10 vertical Pexels clips (1080x1920, Color Grade, Vignette)
- Audio: EBU R128 (-14 LUFS) with subtle BGM
- Database: Auto-syncs to video_management.db & exports CSV after each video
"""

import os
import sys
import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

CONFIGS_DIR = BASE_DIR / "configs"
OUTPUTS_DIR = BASE_DIR / "outputs"

from tools.run_full_pipeline import run_pipeline_for_book
from tools.video_db import sync_all_from_configs, export_to_csv


def get_all_configured_books() -> list:
    config_files = [
        "books_10.json",
        "books_genz.json",
        "books_genz_20.json",
        "books_genz_batch3.json",
        "books_batch4.json",
        "books_batch5.json"
    ]
    books = []
    seen = set()
    for c in config_files:
        p = CONFIGS_DIR / c
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            for b in data:
                slug = b.get("slug")
                if slug and slug not in seen:
                    seen.add(slug)
                    books.append(b)
    return books


def produce_all(max_count: int = None, force: bool = False):
    all_books = get_all_configured_books()
    pending = []

    for b in all_books:
        slug = b["slug"]
        final_mp4 = OUTPUTS_DIR / f"{slug}_final.mp4"
        if not final_mp4.exists() or force:
            pending.append(b)

    total_pending = len(pending)
    print(f"\n============================================================")
    print(f"🎬 BATCH PRODUCTION ENGINE (RADIO 2AM)")
    print(f"Tổng số sách trong hệ thống: {len(all_books)}")
    print(f"Đã hoàn thành: {len(all_books) - total_pending}")
    print(f"Còn lại cần sản xuất: {total_pending}")
    print(f"============================================================\n")

    if total_pending == 0:
        print("🎉 Toàn bộ video trong hệ thống đã được sản xuất hoàn tất 100%!")
        return

    if max_count:
        pending = pending[:max_count]
        print(f"👉 Sẽ xử lý {len(pending)} video trong lượt chạy này.")

    success_count = 0
    fail_count = 0

    for idx, book in enumerate(pending, 1):
        slug = book["slug"]
        title = book.get("title", slug)
        print(f"\n[{idx}/{len(pending)}] 🚀 BẮT ĐẦU: {title} ({slug})")
        t0 = time.time()
        try:
            res = run_pipeline_for_book(book, skip_review=False, skip_audio=False)
            if res and Path(res).exists():
                dur = time.time() - t0
                size_mb = Path(res).stat().st_size / (1024 * 1024)
                success_count += 1
                print(f"✅ Hoàn thành [{idx}/{len(pending)}] trong {dur:.1f}s ({size_mb:.2f} MB)")
                # Update DB and export CSV immediately
                sync_all_from_configs()
                export_to_csv()
            else:
                fail_count += 1
                print(f"❌ Thất bại khi tạo video: {slug}")
        except Exception as e:
            fail_count += 1
            print(f"❌ Lỗi xử lý {slug}: {e}")

        time.sleep(2)

    print(f"\n============================================================")
    print(f"🏁 TỔNG KẾT ĐỢT CHẠY:")
    print(f"  - Thành công: {success_count}")
    print(f"  - Thất bại: {fail_count}")
    print(f"  - Dữ liệu Database và CSV đã được đồng bộ 100%!")
    print(f"============================================================")


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    produce_all(max_count=limit)

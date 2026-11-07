#!/usr/bin/env python3
"""
reproduce_all_24_series.py - Master Production Runner for all 24 Series Episodes
Processes:
  Batch 1: Dám Bị Ghét, Tâm Lý Học Về Tiền, Atomic Habits (Tập 1 - 4) -> 12 episodes
  Batch 2: Đắc Nhân Tâm, Deep Work, Can't Hurt Me (Tập 1 - 4) -> 12 episodes

All scripts are completely clean:
  - 0 IN HOA
  - 0 '...'
  - 0 ' — '
  - Pure natural Vietnamese phrasing for ChatGPT Read Aloud to deduce intonation.
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

from tools.produce_series_batch import produce_episode
from tools.cover_generator import generate_shorts_cover
from tools.video_db import init_db, sync_all_from_configs, export_to_csv


def regenerate_covers(episodes):
    for ep in episodes:
        slug = ep["slug"]
        script = ep["script"]
        hook_line = script.split("\n")[0].strip(' "“\'”')
        if len(hook_line) > 75:
            hook_line = hook_line[:72] + "..."
        badge_text = f"TẬP {ep['episode']}"
        generate_shorts_cover(
            slug=slug,
            title_hook=hook_line,
            book_title=f"{ep['title'].split('[')[0].strip()} ({badge_text})",
            author=ep["author"],
            badge_text=badge_text
        )


def main():
    init_db()
    sync_all_from_configs()

    pilot_file = CONFIGS_DIR / "books_multi_series_pilot.json"
    batch2_file = CONFIGS_DIR / "books_multi_series_batch2.json"

    pilot_eps = json.loads(pilot_file.read_text(encoding="utf-8")) if pilot_file.exists() else []
    batch2_eps = json.loads(batch2_file.read_text(encoding="utf-8")) if batch2_file.exists() else []

    all_24 = pilot_eps + batch2_eps
    total = len(all_24)

    print("=" * 80)
    print(f"🎬 BẮT ĐẦU SẢN XUẤT LẠI TOÀN BỘ {total} TẬP SERIES ĐA GÓC NHÌN")
    print("🎯 Giọng đọc ChatGPT tự suy diễn ngữ điệu tự nhiên (0 IN HOA, 0 '...', 0 ' — ')")
    print("=" * 80)

    print("\n🖼️ Đang làm mới ảnh bìa Thumbnail 9:16...")
    regenerate_covers(all_24)
    print("✅ Đã làm mới xong toàn bộ ảnh bìa!")

    success_cnt = 0
    fail_cnt = 0

    t_start = time.time()
    for idx, ep in enumerate(all_24, 1):
        slug = ep["slug"]
        title = ep["title"]
        print(f"\n[{idx}/{total}] 🚀 ĐANG XỬ LÝ: {title} ({slug})")
        t0 = time.time()
        ok = produce_episode(ep)
        elapsed = time.time() - t0
        if ok:
            success_cnt += 1
            print(f"✅ Hoàn thành [{idx}/{total}] {slug} trong {elapsed:.1f}s")
            export_to_csv()
        else:
            fail_cnt += 1
            print(f"❌ Thất bại [{idx}/{total}] {slug}")

    sync_all_from_configs()
    csv_path = export_to_csv()
    total_time = time.time() - t_start

    print("\n" + "=" * 80)
    print("🏁 TỔNG KẾT TOÀN DIỆN:")
    print(f"  - Thành công: {success_cnt}/{total}")
    print(f"  - Thất bại:   {fail_cnt}/{total}")
    print(f"  - Tổng thời gian: {total_time / 60:.1f} phút")
    print(f"  - File xuất bản cập nhật: {csv_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()

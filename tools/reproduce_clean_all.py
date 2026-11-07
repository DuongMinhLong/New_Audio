#!/usr/bin/env python3
"""
reproduce_clean_all.py - Batch Producer for all remaining 22 Series Episodes
Applies the new 10/10 Viral Shorts Standard:
  - Preserves 100% existing ChatGPT Read Aloud voice in cache
  - Ken Burns slow push-in zoom (1.07x) on every shot
  - Forced Rec.709 yuv420p color metadata (anti-audio corruption)
  - Segoe UI Black bold yellow subtitles with black outline & shadow
  - EBU R128 (-14 LUFS) voice + BGM at volume=0.18 (-22dB) with aformat
  - 0.40s Thumbnail intro frame injection
"""

import os
import sys
import json
import time
from pathlib import Path

# Force UTF-8
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tools.produce_series_pilot import produce_episode
from tools.video_db import export_to_csv, init_db

REMAINING_SLUGS = [
    "deep_work_tap2", "deep_work_tap3", "deep_work_tap4",
    "cant_hurt_me_tap1", "cant_hurt_me_tap2", "cant_hurt_me_tap3", "cant_hurt_me_tap4"
]

def load_all_items():
    items = {}
    pilot_p = BASE_DIR / "configs" / "books_multi_series_pilot.json"
    batch2_p = BASE_DIR / "configs" / "books_multi_series_batch2.json"
    if pilot_p.exists():
        with open(pilot_p, "r", encoding="utf-8") as f:
            for it in json.load(f):
                items[it["slug"]] = it
    if batch2_p.exists():
        with open(batch2_p, "r", encoding="utf-8") as f:
            for it in json.load(f):
                items[it["slug"]] = it
    return items

def clean_stale_cache(slug: str):
    cache_dir = BASE_DIR / "cache" / "books" / slug
    if cache_dir.exists():
        for f in cache_dir.glob("norm_shot_*.mp4"):
            try:
                f.unlink()
            except Exception:
                pass
        comb = cache_dir / "combined_visuals.mp4"
        if comb.exists():
            try:
                comb.unlink()
            except Exception:
                pass
    
    final_p = BASE_DIR / "outputs" / f"{slug}_final.mp4"
    if final_p.exists():
        try:
            final_p.unlink()
        except Exception:
            pass
    cover_p = BASE_DIR / "outputs" / "with_cover" / f"{slug}_with_cover.mp4"
    if cover_p.exists():
        try:
            cover_p.unlink()
        except Exception:
            pass

def main():
    init_db()
    items = load_all_items()
    total = len(REMAINING_SLUGS)

    print("=" * 80)
    print(f"🎬 BẮT ĐẦU SẢN XUẤT 22 TẬP CÒN LẠI THEO CHUẨN 10/10 VIRAL")
    print("=" * 80)

    t_start = time.time()
    success_cnt = 0

    for idx, slug in enumerate(REMAINING_SLUGS, 1):
        if slug not in items:
            print(f"⚠️ [{idx}/{total}] Bỏ qua vì không tìm thấy cấu hình: {slug}")
            continue

        item = items[slug]
        print(f"\n[{idx}/{total}] ⚙️ Đang làm mới cache và render: {item.get('title')} ({slug})...")
        clean_stale_cache(slug)

        t0 = time.time()
        ok = produce_episode(item)
        elapsed = time.time() - t0

        if ok:
            success_cnt += 1
            print(f"✅ Hoàn thành [{idx}/{total}] {slug} trong {elapsed:.1f}s")
            export_to_csv()
        else:
            print(f"❌ Thất bại [{idx}/{total}] {slug}")

    export_to_csv()
    tot_min = (time.time() - t_start) / 60.0
    print("\n" + "=" * 80)
    print(f"🏁 ĐÃ RENDER XONG: {success_cnt}/{total} TẬP TRONG {tot_min:.1f} PHÚT")
    print("=" * 80)

if __name__ == "__main__":
    main()

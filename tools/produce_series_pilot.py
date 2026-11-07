#!/usr/bin/env python3
"""
produce_series_pilot.py - Automated Batch Producer for 12 Multi-Angle Pilot Episodes
Processes:
  1. Dám Bị Ghét (Tập 1 - 4)
  2. Tâm Lý Học Về Tiền (Tập 1 - 4)
  3. Atomic Habits (Tập 1 - 4)

Steps per episode:
  - Generate ChatGPT Read Aloud Voice via Chrome CDP
  - Align Subtitles via Faster-Whisper int8
  - Download & Normalize 10 Cinematic Pexels B-Rolls
  - Mix EBU R128 (-14 LUFS) Audio + Ambient BGM (-22dB)
  - Inject 0.40s Episode Cover Frame into 0:00 (for Shorts/TikTok Grid)
  - Upsert Database & Export CSV
"""

import os
import sys
import json
import time
import shutil
import subprocess
from pathlib import Path

# Force UTF-8 on Windows standard streams
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
WITH_COVER_DIR = OUTPUTS_DIR / "with_cover"
CACHE_ROOT = BASE_DIR / "cache" / "books"

OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
COVERS_DIR.mkdir(parents=True, exist_ok=True)
WITH_COVER_DIR.mkdir(parents=True, exist_ok=True)
CACHE_ROOT.mkdir(parents=True, exist_ok=True)

from tools.batch_book_generator import process_single_book
from tools.batch_book_generator import process_single_book
from tools.cover_generator import inject_cover_to_video
from tools.video_db import get_db_connection, export_to_csv, init_db



def ensure_audio_exists(item: dict) -> bool:
    slug = item["slug"]
    script = item["script"]
    out_mp3 = OUTPUTS_DIR / f"{slug}.mp3"
    book_cache = CACHE_ROOT / slug
    book_cache.mkdir(parents=True, exist_ok=True)
    cache_mp3 = book_cache / "audio.mp3"

    if out_mp3.exists() and out_mp3.stat().st_size > 1000:
        if not cache_mp3.exists():
            shutil.copy2(out_mp3, cache_mp3)
        return True

    if cache_mp3.exists() and cache_mp3.stat().st_size > 1000:
        if not out_mp3.exists():
            shutil.copy2(cache_mp3, out_mp3)
        return True

    print(f"🎙️ Đang thu âm giọng đọc ChatGPT Read Aloud cho: '{slug}'...")
    script_file = book_cache / "script.txt"
    script_file.write_text(script, encoding="utf-8")

    server_py = BASE_DIR / "tools" / "chatwithgpt_server.py"
    sub_env = os.environ.copy()
    sub_env["PYTHONIOENCODING"] = "utf-8"
    cmd = [sys.executable, str(server_py), "--audio-file", str(script_file), slug]
    proc = subprocess.run(cmd, env=sub_env, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    print(proc.stdout)

    if out_mp3.exists() and out_mp3.stat().st_size > 1000:
        shutil.copy2(out_mp3, cache_mp3)
        return True
    return False


def produce_episode(item: dict) -> bool:
    slug = item["slug"]
    title = item["title"]
    final_mp4 = OUTPUTS_DIR / f"{slug}_final.mp4"
    with_cover_mp4 = WITH_COVER_DIR / f"{slug}_with_cover.mp4"
    cover_png = COVERS_DIR / f"{slug}_cover.png"

    # Step 1: Ensure audio is captured
    if not ensure_audio_exists(item):
        print(f"❌ Không thể tạo audio cho {slug}")
        return False

    # Step 2: Render video 9:16
    if not final_mp4.exists():
        rendered = process_single_book(item, force_tts=False)
        if not rendered or not final_mp4.exists():
            print(f"❌ Render video thất bại cho {slug}")
            return False
    else:
        print(f"⏩ Video đã render sẵn: {final_mp4.name}")

    # Step 3: Inject Cover Thumbnail Frame
    if not with_cover_mp4.exists() and cover_png.exists():
        print(f"🖼️ Ghép khung hình ảnh bìa 0.4s vào đầu video: {slug}...")
        ok = inject_cover_to_video(str(final_mp4), str(cover_png), str(with_cover_mp4), duration=0.40)
        if not ok:
            print(f"⚠️ Cảnh báo: Lỗi ghép cover cho {slug}")

    # Step 4: Update Database record
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE videos
            SET local_video_path = ?,
                video_with_cover_path = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE slug = ?
        """, (
            str(final_mp4),
            str(with_cover_mp4) if with_cover_mp4.exists() else None,
            slug
        ))
        conn.commit()

    return True


def run_batch():
    init_db()
    pilot_config = CONFIGS_DIR / "books_multi_series_pilot.json"
    if not pilot_config.exists():
        print("❌ Không tìm thấy file books_multi_series_pilot.json!")
        return

    episodes = json.loads(pilot_config.read_text(encoding="utf-8"))
    print("\n" + "=" * 80)
    print(f"🚀 BẮT ĐẦU SẢN XUẤT 12 TẬP PILOT SERIES (3 CUỐN X 4 TẬP)")
    print(f"Tổng số tập cần xử lý: {len(episodes)}")
    print("=" * 80 + "\n")

    success_cnt = 0
    fail_cnt = 0

    for idx, ep in enumerate(episodes, 1):
        slug = ep["slug"]
        title = ep["title"]
        print(f"\n[{idx}/{len(episodes)}] 🎬 BẮT ĐẦU: {title} ({slug})")
        t0 = time.time()
        ok = produce_episode(ep)
        elapsed = time.time() - t0
        if ok:
            success_cnt += 1
            print(f"✅ Hoàn thành [{idx}/{len(episodes)}] {slug} trong {elapsed:.1f}s")
            export_to_csv()
        else:
            fail_cnt += 1
            print(f"❌ Thất bại [{idx}/{len(episodes)}] {slug}")

    print("\n" + "=" * 80)
    print(f"🏁 TỔNG KẾT QUÁ TRÌNH SẢN XUẤT:")
    print(f"  - Thành công: {success_cnt}/{len(episodes)}")
    print(f"  - Thất bại:   {fail_cnt}/{len(episodes)}")
    print("=" * 80)


if __name__ == "__main__":
    run_batch()

from tools.cover_generator import inject_cover_to_video
from tools.video_db import get_db_connection, export_to_csv, init_db

#!/usr/bin/env python3
"""
tools/run_full_pipeline.py
==========================
Unified Full End-to-End Pipeline:
  1. Review & Polish Script (3 Rounds via 9Router):
     - Vòng 1 & 2: ag/gemini-3.8-flash-high
     - Vòng 3: ag/claude-sonnet-4-6(max)
  2. Capture Studio Audio via ChatGPT Web Read Aloud (Chrome CDP port 9222).
  3. Clean old visual/subtitle cache to avoid timeline mismatches.
  4. Render 9:16 Vertical Video with Faster-Whisper, Pexels B-Roll & EBU R128 BGM.
"""

import os
import sys
import json
import time
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

CONFIGS_DIR = BASE_DIR / "configs"
OUTPUTS_DIR = BASE_DIR / "outputs"
CACHE_ROOT = BASE_DIR / "cache" / "books"

from tools.gpt_script_reviewer import review_and_generate_script, update_configs_file
from tools.batch_book_generator import process_single_book
from tools.video_db import sync_all_from_configs, export_to_csv



def clean_book_mismatch_cache(slug: str):
    """Clean visual cuts and old srt when a new script/audio is produced."""
    book_cache = CACHE_ROOT / slug
    if not book_cache.exists():
        return
    for f in book_cache.glob("norm_shot_*.mp4"):
        try:
            f.unlink()
        except Exception:
            pass
    for name in ["combined_visuals.mp4", "concat_list.txt", "subtitles.srt"]:
        p = book_cache / name
        if p.exists():
            try:
                p.unlink()
            except Exception:
                pass


def run_pipeline_for_book(book: dict, skip_review: bool = False, skip_audio: bool = False) -> str:
    slug = book["slug"]
    title = book["title"]
    book_cache = CACHE_ROOT / slug
    book_cache.mkdir(parents=True, exist_ok=True)
    script_file = book_cache / "script.txt"

    print("\n" + "=" * 70)
    print(f"🎬 [PIPELINE FULL] BẮT ĐẦU CHO: {title.upper()} ({slug})")
    print("=" * 70)

    # BƯỚC 1: Review 3 Vòng qua 9Router
    if not skip_review:
        print(f"\n📝 [BƯỚC 1/3] Thẩm định kịch bản 3 vòng qua 9Router...")
        script_10, report = review_and_generate_script(book)
        book["script"] = script_10
        update_configs_file(slug, script_10)
    else:
        print(f"\n⏩ [BƯỚC 1/3] Bỏ qua review, sử dụng kịch bản hiện tại.")
        if script_file.exists():
            with open(script_file, "r", encoding="utf-8") as sf:
                book["script"] = sf.read().strip()

    # BƯỚC 2: Lấy Audio ChatGPT Read Aloud qua Chrome CDP
    if not skip_audio:
        print(f"\n🎙️ [BƯỚC 2/3] Thu âm giọng đọc ChatGPT Read Aloud qua Chrome CDP (port 9222)...")
        server_py = BASE_DIR / "tools" / "chatwithgpt_server.py"
        sub_env = os.environ.copy()
        sub_env["PYTHONIOENCODING"] = "utf-8"
        cmd = [sys.executable, str(server_py), "--audio-file", str(script_file), slug]
        proc = subprocess.run(cmd, env=sub_env, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        print(proc.stdout)

        # Đồng bộ file audio vào cache
        out_mp3 = OUTPUTS_DIR / f"{slug}.mp3"
        cache_mp3 = book_cache / "audio.mp3"
        if out_mp3.exists():
            shutil.copy2(out_mp3, cache_mp3)
        elif not cache_mp3.exists():
            print(f"❌ Không tìm thấy file audio cho {slug}!")
            return None
    else:
        print(f"\n⏩ [BƯỚC 2/3] Bỏ qua thu âm, sử dụng audio sẵn có.")

    # BƯỚC 3: Dọn dẹp cache lệch timeline & Render Video
    print(f"\n🎞️ [BƯỚC 3/3] Đồng bộ Faster-Whisper và Render video 9:16...")
    clean_book_mismatch_cache(slug)

    # Xóa file output cũ nếu có để buộc render mới
    final_mp4 = OUTPUTS_DIR / f"{slug}_final.mp4"
    if final_mp4.exists():
        try:
            final_mp4.unlink()
        except Exception:
            pass

    out_file = process_single_book(book, force_tts=False)
    if out_file and Path(out_file).exists():
        size_mb = Path(out_file).stat().st_size / (1024 * 1024)
        print(f"\n🎉 [HOÀN TẤT] Video thành phẩm: {Path(out_file).name} ({size_mb:.2f} MB)")
        try:
            sync_all_from_configs()
            export_to_csv()
        except Exception as e:
            print(f"⚠️ Lỗi đồng bộ DB/CSV: {e}")

        return out_file
    else:
        print(f"\n❌ Thất bại khi tạo video cho {slug}!")
        return None


def load_all_books() -> list:
    """Load all unique books across canonical json files in configs/."""
    all_books = {}
    ordered_cfgs = [
        "books_multi_series_pilot.json",
        "books_multi_series_batch2.json",
        "books_multi_series_batch3.json"
    ]
    for name in ordered_cfgs:
        cfg_path = CONFIGS_DIR / name
        if cfg_path.exists():
            try:
                data = json.loads(cfg_path.read_text(encoding="utf-8"))
                items = data if isinstance(data, list) else data.get("books", [])
                for b in items:
                    slug = b.get("slug")
                    if slug and slug not in all_books:
                        all_books[slug] = b
            except Exception:
                continue
    return list(all_books.values())


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    # Check if a specific config file was provided
    custom_cfg = next((f.split("=", 1)[1] for f in flags if f.startswith("--config=")), None)
    if custom_cfg:
        cfg_file = Path(custom_cfg)
        with open(cfg_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            books = data if isinstance(data, list) else data.get("books", [])
    elif "--all" in flags or "--all-pending" in flags:
        books = load_all_books()
    else:
        cfg_file = CONFIGS_DIR / "books_multi_series_pilot.json"
        with open(cfg_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            books = data if isinstance(data, list) else data.get("books", [])

    target_slug = args[0] if args else None
    if target_slug:
        # Search target slug in loaded books or all configs
        matched = [b for b in books if b["slug"] == target_slug or (target_slug.isdigit() and books.index(b) + 1 == int(target_slug))]
        if not matched:
            all_b = load_all_books()
            matched = [b for b in all_b if b["slug"] == target_slug]
        if not matched:
            print(f"❌ Không tìm thấy sách '{target_slug}'")
            return
        selected = matched
    else:
        selected = books

    # Filter pending only if --all-pending or --resume
    all_pending_mode = "--all-pending" in flags or "--resume" in flags
    if all_pending_mode:
        pending_list = []
        for b in selected:
            slug = b["slug"]
            final_mp4 = OUTPUTS_DIR / f"{slug}_final.mp4"
            if final_mp4.exists():
                print(f"⏩ [ĐÃ CÓ VIDEO] {b['title']} ({slug})")
            else:
                pending_list.append(b)
        selected = pending_list

    limit_flag = next((f.split("=", 1)[1] for f in flags if f.startswith("--limit=")), None)
    if limit_flag and limit_flag.isdigit():
        selected = selected[:int(limit_flag)]

    print(f"\n🚀 SỐ LƯỢNG SÁCH CẦN XỬ LÝ: {len(selected)} cuốn...")
    results = []
    for idx, b in enumerate(selected, 1):
        print(f"\n>>> TIẾN ĐỘ: [{idx}/{len(selected)}] ĐANG XỬ LÝ: {b['title']} ({b['slug']})")
        res = run_pipeline_for_book(b)
        if res:
            results.append((b["title"], res))
        time.sleep(2)

    print("\n" + "=" * 70)
    print(f"🏁 ĐÃ HOÀN TẤT: {len(results)}/{len(selected)} VIDEO THÀNH CÔNG!")
    for t, p in results:
        print(f"   ✅ {t}: {p}")
    print("=" * 70)

    if "--shutdown" in flags:
        print("\n💤 Tự động hẹn giờ tắt máy sau 60 giây...")
        os.system('shutdown /s /t 60 /c "Hoan tat toan bo video sach! May se tat sau 60s."')



if __name__ == "__main__":
    main()

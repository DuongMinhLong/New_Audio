import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
cfg_path = BASE_DIR / "configs" / "books_multi_series_batch3.json"
with open(cfg_path, "r", encoding="utf-8") as f:
    items = json.load(f)

print("=" * 75)
print("📊 BÁO CÁO TIẾN ĐỘ SẢN XUẤT 24 TẬP BATCH 3 (MULTI-SERIES)")
print("=" * 75)

completed = 0
in_progress = None

for i, it in enumerate(items, 1):
    slug = it["slug"]
    title = it["title"]
    final_p = BASE_DIR / "outputs" / f"{slug}_final.mp4"
    with_cov_p = BASE_DIR / "outputs" / "with_cover" / f"{slug}_with_cover.mp4"
    cache_p = BASE_DIR / "cache" / "books" / slug
    
    if final_p.exists() and final_p.stat().st_size > 1000000:
        completed += 1
        wc_status = "ĐÃ GHÉP 0:00" if with_cov_p.exists() else "CHỜ GHÉP"
        print(f"[{i:2d}/24] ✅ ĐÃ XONG: {slug:<30} ({final_p.stat().st_size / (1024*1024):.1f} MB | {wc_status})")
    elif cache_p.exists() and (cache_p / "audio.mp3").exists():
        in_progress = slug
        print(f"[{i:2d}/24] ⏳ ĐANG XỬ LÝ: {slug:<30} (Đang tải B-roll/Render video...)")
    else:
        print(f"[{i:2d}/24] ⚪ CHỜ XỬ LÝ: {slug:<30}")

print("-" * 75)
pct = (completed / len(items)) * 100
print(f"🚀 TỔNG TIẾN ĐỘ: {completed}/{len(items)} tập ({pct:.1f}%)")
if in_progress:
    print(f"🔄 Tập đang chạy hiện tại: {in_progress}")
rem = len(items) - completed
est_min = rem * 2.8
print(f"⏱️ Dự kiến hoàn tất toàn bộ sau khoảng: {est_min:.0f} phút nữa")
print(f"💤 Cơ chế Auto-Shutdown: Sẽ tự động tắt máy sau khi đạt 24/24 (100%)")
print("=" * 75)

"""
schedule_all_series.py - Lên lịch đăng tự động toàn bộ 24 tập theo đúng khung giờ vàng 11:30 & 20:00
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import json
import sqlite3
from datetime import datetime, timezone, timedelta

from tools.fb_video_uploader import upload_facebook_reel
from tools.video_db import get_video, update_status

# Danh sách 24 tập theo thứ tự phát hành
EPISODES = [
    "dam_bi_ghet_tap1", "dam_bi_ghet_tap2", "dam_bi_ghet_tap3", "dam_bi_ghet_tap4",
    "tam_ly_hoc_ve_tien_tap1", "tam_ly_hoc_ve_tien_tap2", "tam_ly_hoc_ve_tien_tap3", "tam_ly_hoc_ve_tien_tap4",
    "atomic_habits_tap1", "atomic_habits_tap2", "atomic_habits_tap3", "atomic_habits_tap4",
    "dac_nhan_tam_tap1", "dac_nhan_tam_tap2", "dac_nhan_tam_tap3", "dac_nhan_tam_tap4",
    "deep_work_tap1", "deep_work_tap2", "deep_work_tap3", "deep_work_tap4",
    "cant_hurt_me_tap1", "cant_hurt_me_tap2", "cant_hurt_me_tap3", "cant_hurt_me_tap4"
]

def schedule_series():
    tz_vn = timezone(timedelta(hours=7))
    # Bắt đầu lên lịch từ hôm nay (2026-11-05)
    # dam_bi_ghet_tap1 đã đăng ngay rồi
    # dam_bi_ghet_tap2: hôm nay 11:30
    # dam_bi_ghet_tap3: hôm nay 20:00
    # dam_bi_ghet_tap4: ngày mai 11:30...
    
    start_date = datetime(2026, 11, 5) # hôm nay
    
    schedule_slots = []
    # slot 0 là dam_bi_ghet_tap1 (đã đăng lúc 00:22)
    # slots tiếp theo:
    # 2: 2026-11-05 11:30
    # 3: 2026-11-05 20:00
    # 4: 2026-11-06 11:30
    # 5: 2026-11-06 20:00...
    
    current_day = start_date
    slot_times = [
        current_day.replace(hour=11, minute=30, second=0, tzinfo=tz_vn),
        current_day.replace(hour=20, minute=0, second=0, tzinfo=tz_vn)
    ]
    
    # Tạo danh sách mốc thời gian cho 23 tập còn lại (từ tập 2 đến tập 24)
    all_times = []
    day_offset = 0
    while len(all_times) < 23:
        d = start_date + timedelta(days=day_offset)
        t_lunch = d.replace(hour=11, minute=30, second=0, tzinfo=tz_vn)
        t_dinner = d.replace(hour=20, minute=0, second=0, tzinfo=tz_vn)
        all_times.append(t_lunch)
        if len(all_times) < 23:
            all_times.append(t_dinner)
        day_offset += 1

    print("=" * 70)
    print(" LÊN LỊCH TỰ ĐỘNG FACEBOOK REELS (11:30 & 20:00 MỖI NGÀY)")
    print("=" * 70)

    # Tập 1 bỏ qua vì đã đăng
    remaining_episodes = EPISODES[1:]

    for idx, (slug, sch_time) in enumerate(zip(remaining_episodes, all_times), 2):
        v = get_video(slug)
        if not v:
            print(f"[X] Không tìm thấy slug: {slug}")
            continue

        if v.get("upload_status") == "ĐÃ ĐĂNG":
            print(f"[{idx:2d}/24] {slug}: Đã đăng trước đó, bỏ qua.")
            continue

        video_path = v.get("video_with_cover_path") or v.get("local_video_path")
        if not video_path or not os.path.exists(video_path):
            print(f"[X] File video không tồn tại cho {slug}: {video_path}")
            continue

        title = v.get("title_curiosity")
        hashtags = v.get("hashtags")
        aff_link = v.get("shopee_aff_link")

        caption = f"{title}\n\n📖 {v.get('book_title')} - {v.get('author')}\n"
        if aff_link:
            caption += f"🛒 Link mua sách chính hãng: {aff_link}\n"
        caption += f"\n{hashtags}"

        unix_ts = int(sch_time.timestamp())
        human_time = sch_time.strftime("%d/%m/%Y lúc %H:%M")

        print(f"\n[{idx:2d}/24] Đang lên lịch: {v.get('book_title')}")
        print(f"    - Thời điểm phát hành: {human_time} (Unix: {unix_ts})")
        print(f"    - File: {os.path.basename(video_path)}")

        try:
            fb_video_id = upload_facebook_reel(
                video_path=video_path,
                caption=caption,
                scheduled_publish_time=unix_ts
            )
            if fb_video_id:
                watch_url = f"https://www.facebook.com/reel/{fb_video_id}"
                update_status(slug, "ĐÃ LÊN LỊCH", watch_url)
                print(f"    [OK] Đã lên lịch thành công! Video ID: {fb_video_id}")
            else:
                print(f"    [X] Lỗi khi lên lịch {slug}")
        except Exception as e:
            print(f"    [!] Exception: {e}")

if __name__ == "__main__":
    schedule_series()

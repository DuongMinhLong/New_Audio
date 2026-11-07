"""
reschedule_all_clean.py - Xóa sạch các video cũ bị mất tiếng do lỗi cover, 
sau đó lên lịch lại 100% video gốc (outputs/[slug]_final.mp4) có đầy đủ âm thanh giọng đọc & BGM!
"""

import os
import sys
import json
import sqlite3
import urllib.request
from pathlib import Path
from datetime import datetime, timezone, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tools.fb_video_uploader import upload_facebook_reel, load_default_page_config
from tools.video_db import get_video, update_status

# Danh sách 24 tập theo thứ tự
EPISODES = [
    "dam_bi_ghet_tap1", "dam_bi_ghet_tap2", "dam_bi_ghet_tap3", "dam_bi_ghet_tap4",
    "tam_ly_hoc_ve_tien_tap1", "tam_ly_hoc_ve_tien_tap2", "tam_ly_hoc_ve_tien_tap3", "tam_ly_hoc_ve_tien_tap4",
    "atomic_habits_tap1", "atomic_habits_tap2", "atomic_habits_tap3", "atomic_habits_tap4",
    "dac_nhan_tam_tap1", "dac_nhan_tam_tap2", "dac_nhan_tam_tap3", "dac_nhan_tam_tap4",
    "deep_work_tap1", "deep_work_tap2", "deep_work_tap3", "deep_work_tap4",
    "cant_hurt_me_tap1", "cant_hurt_me_tap2", "cant_hurt_me_tap3", "cant_hurt_me_tap4"
]

def delete_old_scheduled():
    print("=" * 70)
    print("BƯỚC 1: XÓA CÁC VIDEO CŨ BỊ LỖI MẤT TIẾNG TRÊN FACEBOOK...")
    print("=" * 70)
    
    cfg = load_default_page_config()
    token = cfg["page_access_token"]
    
    conn = sqlite3.connect("outputs/video_management.db")
    c = conn.cursor()
    c.execute("SELECT slug, published_url FROM videos WHERE id >= 8658 AND id <= 8680")
    rows = c.fetchall()
    
    for slug, url in rows:
        if not url:
            continue
        vid_id = url.split("/")[-1]
        del_url = f"https://graph.facebook.com/v22.0/{vid_id}?access_token={token}"
        req = urllib.request.Request(del_url, method="DELETE")
        try:
            with urllib.request.urlopen(req) as resp:
                print(f"  [Xóa OK] {slug} (ID: {vid_id})")
        except Exception as e:
            print(f"  [!] Không thể xóa {slug} (ID: {vid_id}): {e}")

def schedule_clean_episodes():
    print("\n" + "=" * 70)
    print("BƯỚC 2: LÊN LỊCH LẠI TOÀN BỘ BẰNG FILE GỐC (CÓ ĐỦ TIẾNG 100%)...")
    print("=" * 70)
    
    tz_vn = timezone(timedelta(hours=7))
    now_vn = datetime.now(tz_vn)
    start_date = (now_vn + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    
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

    remaining_episodes = EPISODES[1:]

    for idx, (slug, sch_time) in enumerate(zip(remaining_episodes, all_times), 2):
        v = get_video(slug)
        if not v:
            print(f"[X] Không tìm thấy slug: {slug}")
            continue

        # Luôn dùng file gốc outputs/{slug}_final.mp4 (có âm thanh đầy đủ)
        video_path = f"outputs/{slug}_final.mp4"
        if not os.path.exists(video_path):
            print(f"[X] File video gốc không tồn tại: {video_path}")
            continue

        title = v.get("title_curiosity")
        hashtags = v.get("hashtags")
        aff_link = v.get("shopee_aff_link")
        book_title = v.get("book_title")
        author = v.get("author")

        caption = f"{title}\n\n📖 {book_title} - {author}\n"
        if aff_link:
            caption += f"🛒 Link mua sách chính hãng: {aff_link}\n"
        caption += f"\n{hashtags}"

        unix_ts = int(sch_time.timestamp())
        human_time = sch_time.strftime("%d/%m/%Y lúc %H:%M")

        print(f"\n[{idx:2d}/24] Đang lên lịch: {book_title}")
        print(f"    - Thời điểm: {human_time}")
        print(f"    - File chuẩn: {video_path} ({os.path.getsize(video_path)/(1024*1024):.2f} MB)")

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
    delete_old_scheduled()
    schedule_clean_episodes()

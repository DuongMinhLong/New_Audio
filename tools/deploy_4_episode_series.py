#!/usr/bin/env python3
"""
deploy_4_episode_series.py - Lên kế hoạch và Deploy 4 tập trong 1 Series lên Facebook Fanpage 2AM.
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tools.fb_video_uploader import upload_facebook_reel, load_default_page_config
from tools.video_db import update_status

SERIES_PRESETS = {
    "dam_bi_ghet": {
        "title": "Dám Bị Ghét",
        "author": "Ichiro Kishimi & Fumitake Koga",
        "shopee_link": "https://s.shopee.vn/9pfUrqKRhr",
        "episodes": [
            {
                "slug": "dam_bi_ghet_tap1",
                "ep": 1,
                "title_curiosity": "Càng Cố Gắng Làm Hài Lòng Mọi Người... Bạn Càng Vô Hình!",
                "hook": "Càng cố gắng sống tử tế để được tất cả mọi người yêu quý... Bạn càng trở thành một kẻ vô hình đáng thương!",
                "pinned_comment": "👉 Đọc trọn vẹn triết lý Adler qua cuốn 'Dám Bị Ghét' chính hãng tại: https://s.shopee.vn/9pfUrqKRhr",
            },
            {
                "slug": "dam_bi_ghet_tap2",
                "ep": 2,
                "title_curiosity": "Làm Vừa Lòng Sếp Hay Bố Mẹ... Không Phải Việc Của Bạn!",
                "hook": "Làm vừa lòng sếp hay bố mẹ... KHÔNG PHẢI VIỆC CỦA BẠN! Hãy học kỹ thuật phân chia nhiệm vụ.",
                "pinned_comment": "👉 Bạn đang gánh việc của ai? Sách 'Dám Bị Ghét' chính hãng: https://s.shopee.vn/9pfUrqKRhr",
            },
            {
                "slug": "dam_bi_ghet_tap3",
                "ep": 3,
                "title_curiosity": "Đừng Lấy Tổn Thương Tuổi Thơ Ra Làm Tấm Khiên Nữa!",
                "hook": "Đừng mượn cớ tổn thương tuổi thơ nữa... Bạn chỉ đang dùng quá khứ làm TẤM KHIÊN để lười thay đổi!",
                "pinned_comment": "👉 Dũng khí đối diện sự thật cùng 'Dám Bị Ghét': https://s.shopee.vn/9pfUrqKRhr",
            },
            {
                "slug": "dam_bi_ghet_tap4",
                "ep": 4,
                "title_curiosity": "Tự Do Đích Thực: Giây Phút Bạn Dám Bị Kẻ Khác Ghét Bỏ!",
                "hook": "Tự do đích thực của một con người... bắt đầu từ giây phút bạn DÁM BỊ KẺ KHÁC GHÉT BỎ!",
                "pinned_comment": "👉 Link đặt trọn bộ sách chính hãng tại đây: https://s.shopee.vn/9pfUrqKRhr",
            }
        ]
    }
}

def build_deployment_schedule():
    tz_vn = timezone(timedelta(hours=7))
    now_vn = datetime.now(tz_vn)
    day1 = now_vn.date()
    day2 = day1 + timedelta(days=1)
    day3 = day1 + timedelta(days=2)
    
    # 4 mốc phát hành: Tối nay 20:00, Trưa mai 11:30, Tối mai 20:00, Trưa mốt 11:30
    return [
        datetime(day1.year, day1.month, day1.day, 20, 0, 0, tzinfo=tz_vn),
        datetime(day2.year, day2.month, day2.day, 11, 30, 0, tzinfo=tz_vn),
        datetime(day2.year, day2.month, day2.day, 20, 0, 0, tzinfo=tz_vn),
        datetime(day3.year, day3.month, day3.day, 11, 30, 0, tzinfo=tz_vn),
    ]

def print_plan(series_key="dam_bi_ghet"):
    preset = SERIES_PRESETS.get(series_key)
    schedules = build_deployment_schedule()
    
    print("=" * 80)
    print(f"📋 KẾ HOẠCH DEPLOY 4 TẬP: {preset['title'].upper()} ({preset['author']})")
    print("=" * 80)
    print(f"🎯 Kênh phát hành: Facebook Reels (Fanpage 2AM)")
    print(f"🛒 Shopee Affiliate: {preset['shopee_link']}")
    print("-" * 80)

    for ep, sch in zip(preset["episodes"], schedules):
        slug = ep["slug"]
        video_path = f"outputs/{slug}_final.mp4"
        exists = os.path.exists(video_path)
        size_mb = os.path.getsize(video_path) / (1024 * 1024) if exists else 0
        unix_ts = int(sch.timestamp())
        human_time = sch.strftime("%d/%m/%Y lúc %H:%M (Giờ VN)")

        print(f"\n[TẬP {ep['ep']}/4] 🕒 LỊCH PHÁT HÀNH: {human_time}")
        print(f"  • Video: {video_path} [{'SẴN SÀNG - ' + f'{size_mb:.1f} MB' if exists else 'THIẾU'}]")
        print(f"  • Tiêu đề Hook: {ep['title_curiosity']}")
        print(f"  • Hook mở đầu: \"{ep['hook']}\"")
        print(f"  • Pinned Comment: {ep['pinned_comment']}")
        print(f"  • Unix Timestamp: {unix_ts}")

    print("\n" + "=" * 80)

def execute_schedule(series_key="dam_bi_ghet"):
    preset = SERIES_PRESETS.get(series_key)
    schedules = build_deployment_schedule()
    cfg = load_default_page_config()
    
    print(f"\n🚀 Đang lên lịch Reels cho Fanpage: {cfg['page_name']} (ID: {cfg['page_id']})")

    for ep, sch in zip(preset["episodes"], schedules):
        slug = ep["slug"]
        video_path = f"outputs/{slug}_final.mp4"
        if not os.path.exists(video_path):
            print(f"[X] Bỏ qua Tập {ep['ep']}: File {video_path} không tồn tại!")
            continue

        hashtags = f"#2am #sachhay #{series_key} #phattrienbanthan #shorts #reels"
        caption = f"{ep['title_curiosity']}\n\n📖 {preset['title']} - {preset['author']}\n🛒 Link sách: {preset['shopee_link']}\n\n{hashtags}"
        unix_ts = int(sch.timestamp())
        human_time = sch.strftime("%d/%m/%Y lúc %H:%M")

        print(f"\nĐang lên lịch Tập {ep['ep']}: {ep['title_curiosity']} -> {human_time}")
        fb_video_id = upload_facebook_reel(video_path=video_path, caption=caption, scheduled_publish_time=unix_ts)
        if fb_video_id:
            watch_url = f"https://www.facebook.com/reel/{fb_video_id}"
            update_status(slug, "ĐÃ LÊN LỊCH", watch_url)
            print(f"  [OK] Đã lên lịch thành công! Video ID: {fb_video_id}")
        else:
            print(f"  [X] Thất bại khi lên lịch {slug}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--series", default="dam_bi_ghet")
    parser.add_argument("--schedule", action="store_true")
    args = parser.parse_args()
    if args.schedule:
        execute_schedule(args.series)
    else:
        print_plan(args.series)

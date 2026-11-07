#!/usr/bin/env python3
"""
schedule_book_photo_posts.py - Điều phối lên lịch phát hành các bài viết Photo Post từ outputs/post_management.db
theo khung giờ vàng 15:30 mỗi ngày trên Fanpage 2AM.
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tools.post_db import get_posts_by_book, update_post_status
from tools.fb_post_uploader import upload_facebook_photo, load_default_page_config


def schedule_book_posts(book_slug="dam_bi_ghet", dry_run=True):
    posts = get_posts_by_book(book_slug)
    if not posts:
        print(f"[X] Không tìm thấy bài viết nào cho cuốn sách: {book_slug}")
        return

    tz_vn = timezone(timedelta(hours=7))
    now_vn = datetime.now(tz_vn)
    
    # Nếu hiện tại trước 15:00 hôm nay, bắt đầu lịch ngay từ 15:30 chiều nay
    if now_vn.hour < 15 or (now_vn.hour == 15 and now_vn.minute <= 10):
        start_date = now_vn.date()
    else:
        start_date = (now_vn + timedelta(days=1)).date()

    print("=" * 80)
    mode_text = "[MÔ PHỎNG - DRY-RUN]" if dry_run else "[THỰC THI META GRAPH API]"
    print(f"LÊN LỊCH PHÁT HÀNH 4 PHẦN BÀI VIẾT: {posts[0]['book_title'].upper()} {mode_text}")
    print("=" * 80)

    for i, post in enumerate(posts):
        sch_date = start_date + timedelta(days=i)
        sch_time = datetime(sch_date.year, sch_date.month, sch_date.day, 15, 30, 0, tzinfo=tz_vn)
        unix_ts = int(sch_time.timestamp())
        human_time = sch_time.strftime("%d/%m/%Y lúc %H:%M (Giờ VN)")

        slug = post["slug"]
        img_path = post["image_path"]
        caption = post["caption"]
        badge = post["badge_tag"]
        quote = post["quote_on_image"]

        print(f"\n[PHẦN {post['part_number']}/4] 🕒 LỊCH: {human_time}")
        print(f"  • Tiêu đề: {post['part_title']}")
        print(f"  • Badge: [{badge}]")
        print(f"  • Quote: \"{quote}\"")
        print(f"  • File ảnh: {img_path} [{'TỒN TẠI' if os.path.exists(img_path) else 'KHÔNG TỒN TẠI'}]")

        if dry_run:
            print("  -> Trạng thái: Sẵn sàng lên lịch xuất bản.")
            continue

        result = upload_facebook_photo(
            photo_path=img_path,
            caption=caption,
            scheduled_publish_time=unix_ts,
            dry_run=False
        )
        if result:
            photo_id = result.get("id")
            post_id = result.get("post_id")
            pub_url = f"https://www.facebook.com/{post_id}" if post_id else f"https://www.facebook.com/photo/?fbid={photo_id}"
            update_post_status(
                slug=slug,
                new_status="ĐÃ LÊN LỊCH",
                published_url=pub_url,
                post_id=post_id,
                photo_id=photo_id,
                scheduled_time=human_time,
                scheduled_timestamp=unix_ts
            )
            print(f"  [OK] Đã lên lịch thành công trên Fanpage: {pub_url}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--book", default="dam_bi_ghet")
    parser.add_argument("--schedule", action="store_true")
    args = parser.parse_args()
    schedule_book_posts(args.book, dry_run=not args.schedule)

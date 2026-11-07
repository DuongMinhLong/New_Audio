#!/usr/bin/env python3
"""
schedule_daily_posts.py - Điều phối sinh ảnh và Lên lịch 12 Bài viết Facebook (Photo Posts)
theo khung giờ vàng 15:30 mỗi ngày trên Fanpage 2AM.
"""

import os
import sys
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tools.daily_post_series import DAILY_POSTS
from tools.post_image_generator import generate_quote_post_image, POSTS_DIR
from tools.fb_post_uploader import upload_facebook_photo, load_default_page_config

DB_PATH = BASE_DIR / "outputs" / "video_management.db"


def init_posts_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS facebook_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE,
            book_title TEXT,
            author TEXT,
            badge_tag TEXT,
            quote_text TEXT,
            caption TEXT,
            image_path TEXT,
            scheduled_time TEXT,
            scheduled_timestamp INTEGER,
            status TEXT DEFAULT 'CHƯA ĐĂNG',
            facebook_post_id TEXT,
            facebook_photo_id TEXT,
            published_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def generate_all_post_images():
    """Tạo 12 ảnh 4:5 chất lượng cao cho toàn bộ series."""
    print("=" * 70)
    print("BƯỚC 1: KHỞI TẠO 12 ẢNH QUOTE 4:5 (1080x1350) CHO BÀI VIẾT FACEBOOK")
    print("=" * 70)
    
    generated_paths = {}
    for i, p in enumerate(DAILY_POSTS, 1):
        filename = f"{p['slug']}_4x5.png"
        img_path = POSTS_DIR / filename
        if not img_path.exists():
            print(f"[{i:2d}/12] Đang tạo ảnh cho {p['book_title']}...")
            path = generate_quote_post_image(
                quote_text=p["quote_on_image"],
                book_title=p["book_title"],
                author=p["author"],
                badge_tag=p["badge_tag"],
                output_filename=filename,
                ratio="4:5"
            )
            generated_paths[p["slug"]] = path
        else:
            print(f"[{i:2d}/12] [ĐÃ CÓ] {filename}")
            generated_paths[p["slug"]] = str(img_path)
    return generated_paths


def run_post_pipeline(dry_run: bool = True):
    init_posts_db()
    images = generate_all_post_images()

    tz_vn = timezone(timedelta(hours=7))
    start_date = datetime(2026, 11, 6)

    print("\n" + "=" * 70)
    mode_text = "[DRY-RUN - XEM TRƯỚC LỊCH TRÌNH]" if dry_run else "[THỰC THI LÊN LỊCH META GRAPH API]"
    print(f"BƯỚC 2: {mode_text} 12 BÀI VIẾT (15:30 HÀNG NGÀY)")
    print("=" * 70)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for i, p in enumerate(DAILY_POSTS, 1):
        slug = p["slug"]
        sch_date = start_date + timedelta(days=p["day_offset"])
        sch_time = sch_date.replace(hour=15, minute=30, second=0, tzinfo=tz_vn)
        unix_ts = int(sch_time.timestamp())
        human_time = sch_time.strftime("%d/%m/%Y lúc %H:%M")
        img_path = images.get(slug)

        print(f"\n--- [{i:2d}/12] {p['book_title']} | Lịch: {human_time} ---")
        print(f"  - Badge: [{p['badge_tag']}]")
        print(f"  - File ảnh: {os.path.basename(img_path)}")

        if dry_run:
            print(f"  - Trạng thái mô phỏng: Sẵn sàng lên lịch vào {human_time}")
            continue

        c.execute("SELECT status, published_url FROM facebook_posts WHERE slug = ?", (slug,))
        row = c.fetchone()
        if row and row[0] in ("ĐÃ LÊN LỊCH", "ĐÃ ĐĂNG"):
            print(f"  [BỎ QUA] Bài này đã có trạng thái: {row[0]} ({row[1]})")
            continue

        result = upload_facebook_photo(
            photo_path=img_path,
            caption=p["caption"],
            scheduled_publish_time=unix_ts,
            dry_run=False
        )

        if result:
            photo_id = result.get("id")
            post_id = result.get("post_id")
            pub_url = f"https://www.facebook.com/{post_id}" if post_id else f"https://www.facebook.com/{photo_id}"
            
            c.execute("""
                INSERT INTO facebook_posts (
                    slug, book_title, author, badge_tag, quote_text, caption,
                    image_path, scheduled_time, scheduled_timestamp, status,
                    facebook_post_id, facebook_photo_id, published_url, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'ĐÃ LÊN LỊCH', ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(slug) DO UPDATE SET
                    status = 'ĐÃ LÊN LỊCH',
                    facebook_post_id = excluded.facebook_post_id,
                    facebook_photo_id = excluded.facebook_photo_id,
                    published_url = excluded.published_url,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                slug, p["book_title"], p["author"], p["badge_tag"], p["quote_on_image"],
                p["caption"], img_path, human_time, unix_ts, post_id, photo_id, pub_url
            ))
            conn.commit()
            print(f"  [OK] Đã lưu vào Database: {pub_url}")
        else:
            print(f"  [X] Lỗi lên lịch cho {slug}")

    conn.close()
    print("\n" + "=" * 70)
    print("HOÀN TẤT TIẾN TRÌNH!")
    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quản lý lịch bài viết Facebook 2AM")
    parser.add_argument("--schedule", action="store_true", help="Thực thi lên lịch thực tế lên Facebook Fanpage")
    parser.add_argument("--gen-images-only", action="store_true", help="Chỉ tạo 12 ảnh bài viết")

    args = parser.parse_args()

    if args.gen_images_only:
        generate_all_post_images()
    elif args.schedule:
        run_post_pipeline(dry_run=False)
    else:
        run_post_pipeline(dry_run=True)


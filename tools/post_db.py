#!/usr/bin/env python3
"""
post_db.py - Quản lý cơ sở dữ liệu SQLite chuyên biệt cho Bài viết kèm Ảnh (Photo Posts).
Tách biệt hoàn toàn với video_management.db.
Lưu trữ tại: outputs/post_management.db
"""

import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "outputs" / "post_management.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_post_db():
    """Khởi tạo bảng posts riêng biệt."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            book_slug TEXT NOT NULL,
            book_title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT,
            part_number INTEGER NOT NULL,
            part_title TEXT,
            sub_angle TEXT,
            badge_tag TEXT,
            quote_on_image TEXT NOT NULL,
            caption TEXT NOT NULL,
            image_path TEXT,
            shopee_aff_link TEXT,
            hashtags TEXT,
            upload_status TEXT DEFAULT 'CHƯA ĐĂNG',
            scheduled_time TEXT,
            scheduled_timestamp INTEGER,
            facebook_post_id TEXT,
            facebook_photo_id TEXT,
            published_url TEXT,
            review_log TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def add_or_update_post(post_data: dict) -> int:
    """Thêm mới hoặc cập nhật bài viết theo slug."""
    init_post_db()
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO posts (
            slug, book_slug, book_title, author, category,
            part_number, part_title, sub_angle, badge_tag,
            quote_on_image, caption, image_path, shopee_aff_link,
            hashtags, upload_status, scheduled_time, scheduled_timestamp,
            facebook_post_id, facebook_photo_id, published_url, review_log,
            updated_at
        ) VALUES (
            :slug, :book_slug, :book_title, :author, :category,
            :part_number, :part_title, :sub_angle, :badge_tag,
            :quote_on_image, :caption, :image_path, :shopee_aff_link,
            :hashtags, :upload_status, :scheduled_time, :scheduled_timestamp,
            :facebook_post_id, :facebook_photo_id, :published_url, :review_log,
            CURRENT_TIMESTAMP
        )
        ON CONFLICT(slug) DO UPDATE SET
            book_slug = excluded.book_slug,
            book_title = excluded.book_title,
            author = excluded.author,
            category = excluded.category,
            part_number = excluded.part_number,
            part_title = excluded.part_title,
            sub_angle = excluded.sub_angle,
            badge_tag = excluded.badge_tag,
            quote_on_image = excluded.quote_on_image,
            caption = excluded.caption,
            image_path = excluded.image_path,
            shopee_aff_link = excluded.shopee_aff_link,
            hashtags = excluded.hashtags,
            upload_status = COALESCE(excluded.upload_status, posts.upload_status),
            scheduled_time = COALESCE(excluded.scheduled_time, posts.scheduled_time),
            scheduled_timestamp = COALESCE(excluded.scheduled_timestamp, posts.scheduled_timestamp),
            facebook_post_id = COALESCE(excluded.facebook_post_id, posts.facebook_post_id),
            facebook_photo_id = COALESCE(excluded.facebook_photo_id, posts.facebook_photo_id),
            published_url = COALESCE(excluded.published_url, posts.published_url),
            review_log = COALESCE(excluded.review_log, posts.review_log),
            updated_at = CURRENT_TIMESTAMP
    """, {
        "slug": post_data["slug"],
        "book_slug": post_data.get("book_slug", ""),
        "book_title": post_data["book_title"],
        "author": post_data.get("author", ""),
        "category": post_data.get("category", "Tâm Lý & Phát Triển Bản Thân"),
        "part_number": post_data.get("part_number", 1),
        "part_title": post_data.get("part_title", ""),
        "sub_angle": post_data.get("sub_angle", ""),
        "badge_tag": post_data.get("badge_tag", "THỨC TỈNH"),
        "quote_on_image": post_data["quote_on_image"],
        "caption": post_data["caption"],
        "image_path": post_data.get("image_path", ""),
        "shopee_aff_link": post_data.get("shopee_aff_link", ""),
        "hashtags": post_data.get("hashtags", "#radio2am #sachhay #thuctinh"),
        "upload_status": post_data.get("upload_status", "CHƯA ĐĂNG"),
        "scheduled_time": post_data.get("scheduled_time", None),
        "scheduled_timestamp": post_data.get("scheduled_timestamp", None),
        "facebook_post_id": post_data.get("facebook_post_id", None),
        "facebook_photo_id": post_data.get("facebook_photo_id", None),
        "published_url": post_data.get("published_url", None),
        "review_log": post_data.get("review_log", None)
    })

    conn.commit()
    post_id = c.lastrowid
    conn.close()
    return post_id


def get_post(slug: str) -> dict:
    """Lấy thông tin 1 bài viết theo slug."""
    init_post_db()
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE slug = ?", (slug,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def get_posts_by_book(book_slug: str) -> list:
    """Lấy toàn bộ các phần bài viết của 1 cuốn sách."""
    init_post_db()
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE book_slug = ? ORDER BY part_number ASC", (book_slug,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_posts() -> list:
    """Lấy toàn bộ danh sách bài viết trong cơ sở dữ liệu."""
    init_post_db()
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id ASC")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_post_status(slug: str, new_status: str, published_url: str = None, post_id: str = None, photo_id: str = None, scheduled_time: str = None, scheduled_timestamp: int = None):
    """Cập nhật trạng thái phát hành bài viết."""
    init_post_db()
    conn = get_connection()
    c = conn.cursor()
    query = "UPDATE posts SET upload_status = ?, updated_at = CURRENT_TIMESTAMP"
    params = [new_status]
    if published_url:
        query += ", published_url = ?"
        params.append(published_url)
    if post_id:
        query += ", facebook_post_id = ?"
        params.append(post_id)
    if photo_id:
        query += ", facebook_photo_id = ?"
        params.append(photo_id)
    if scheduled_time:
        query += ", scheduled_time = ?"
        params.append(scheduled_time)
    if scheduled_timestamp:
        query += ", scheduled_timestamp = ?"
        params.append(scheduled_timestamp)
    query += " WHERE slug = ?"
    params.append(slug)
    c.execute(query, params)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_post_db()
    print(f"[OK] Đã khởi tạo thành công cơ sở dữ liệu bài viết tại: {DB_PATH}")


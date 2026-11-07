#!/usr/bin/env python3
"""
video_db.py - SQLite Database Manager for Video Publishing & Affiliate Workflow
Tracks:
- Video paths (original MP4 & MP4 with injected cover)
- High-CTR curiosity titles & alternative titles
- Shopee Affiliate links
- Pinned comments (debate hooks) & Descriptions
- Upload status (CHƯA ĐĂNG, ĐÃ LÊN LỊCH, ĐÃ ĐĂNG, LỖI)
- Export to Excel/CSV with UTF-8 BOM
"""

import os
import sys
import json
import sqlite3
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
OUTPUTS_DIR = BASE_DIR / "outputs"
CONFIGS_DIR = BASE_DIR / "configs"
COVERS_DIR = OUTPUTS_DIR / "covers"
WITH_COVER_DIR = OUTPUTS_DIR / "with_cover"
DB_PATH = OUTPUTS_DIR / "video_management.db"

OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
COVERS_DIR.mkdir(parents=True, exist_ok=True)
WITH_COVER_DIR.mkdir(parents=True, exist_ok=True)


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create videos table and indexes if they don't exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slug TEXT UNIQUE NOT NULL,
                book_title TEXT NOT NULL,
                author TEXT,
                core_message TEXT,
                local_video_path TEXT,
                cover_image_path TEXT,
                video_with_cover_path TEXT,
                title_curiosity TEXT,
                alternative_titles TEXT,
                hashtags TEXT,
                shopee_aff_link TEXT,
                pinned_comment TEXT,
                short_comment_replies TEXT,
                description TEXT,
                upload_status TEXT DEFAULT 'CHƯA ĐĂNG',
                platform TEXT DEFAULT 'YouTube Shorts, TikTok, Facebook Reels',
                scheduled_time TEXT DEFAULT '11:30 & 20:00',
                published_url TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_slug ON videos(slug);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON videos(upload_status);")
        conn.commit()


def sync_all_from_configs(custom_aff_base: str = None) -> int:
    """
    Scan all configs, match with generated MP4s in outputs/,
    generate marketing metadata, and populate/update SQLite DB.
    """
    from tools.generate_marketing_meta import generate_marketing_meta

    init_db()
    config_files = [
        "books_multi_series_pilot.json",
        "books_multi_series_batch2.json",
        "books_multi_series_batch3.json"
    ]

    unique_books: Dict[str, dict] = {}
    for cfg in config_files:
        p = CONFIGS_DIR / cfg
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                for b in data:
                    slug = b.get("slug")
                    if slug and slug not in unique_books:
                        unique_books[slug] = b
            except Exception as e:
                print(f"⚠️ Lỗi đọc file cấu hình {cfg}: {e}")

    count = 0
    with get_db_connection() as conn:
        cursor = conn.cursor()
        for slug, book in unique_books.items():
            # Check local file paths
            mp4_final = OUTPUTS_DIR / f"{slug}_final.mp4"
            local_video_path = str(mp4_final) if mp4_final.exists() else ""

            cover_img = COVERS_DIR / f"{slug}_cover.png"
            cover_image_path = str(cover_img) if cover_img.exists() else ""

            with_cov_mp4 = WITH_COVER_DIR / f"{slug}_with_cover.mp4"
            video_with_cover_path = str(with_cov_mp4) if with_cov_mp4.exists() else ""

            # Check if record already exists to preserve custom links / status
            cursor.execute("SELECT id, shopee_aff_link, upload_status, published_url FROM videos WHERE slug = ?", (slug,))
            row = cursor.fetchone()

            existing_aff = row["shopee_aff_link"] if row else None
            existing_status = row["upload_status"] if row else "CHƯA ĐĂNG"
            existing_url = row["published_url"] if row else ""

            aff_link = existing_aff or (f"{custom_aff_base}/{slug}" if custom_aff_base else None)

            # Generate curiosity meta
            meta = generate_marketing_meta(book, shopee_link=aff_link)

            cursor.execute("""
                INSERT INTO videos (
                    slug, book_title, author, core_message,
                    local_video_path, cover_image_path, video_with_cover_path,
                    title_curiosity, alternative_titles, hashtags,
                    shopee_aff_link, pinned_comment, short_comment_replies,
                    description, upload_status, published_url, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(slug) DO UPDATE SET
                    local_video_path = excluded.local_video_path,
                    cover_image_path = excluded.cover_image_path,
                    video_with_cover_path = excluded.video_with_cover_path,
                    title_curiosity = excluded.title_curiosity,
                    alternative_titles = excluded.alternative_titles,
                    hashtags = excluded.hashtags,
                    pinned_comment = excluded.pinned_comment,
                    short_comment_replies = excluded.short_comment_replies,
                    description = excluded.description,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                slug,
                meta["book_title"],
                meta["author"],
                book.get("core_message", ""),
                local_video_path,
                cover_image_path,
                video_with_cover_path,
                meta["title_curiosity"],
                json.dumps(meta["alternative_titles"], ensure_ascii=False),
                meta["hashtags"],
                meta["shopee_aff_link"],
                meta["pinned_comment"],
                meta["short_comment_reply"],
                meta["description"],
                existing_status,
                existing_url
            ))
            count += 1
        conn.commit()
    return count

def list_videos(status_filter: str = None) -> List[Dict[str, Any]]:
    """List videos, optionally filtered by status."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if status_filter:
            cursor.execute("SELECT * FROM videos WHERE upload_status = ? ORDER BY id ASC", (status_filter,))
        else:
            cursor.execute("SELECT * FROM videos ORDER BY id ASC")
        rows = cursor.fetchall()
        return [dict(r) for r in rows]


def get_video(slug_or_id: Any) -> Optional[Dict[str, Any]]:
    """Get single video by slug or id."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if isinstance(slug_or_id, int) or (isinstance(slug_or_id, str) and slug_or_id.isdigit()):
            cursor.execute("SELECT * FROM videos WHERE id = ?", (int(slug_or_id),))
        else:
            cursor.execute("SELECT * FROM videos WHERE slug = ?", (str(slug_or_id),))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_status(slug: str, new_status: str, published_url: str = None) -> bool:
    """Update upload status and optional published URL."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if published_url:
            cursor.execute("""
                UPDATE videos SET upload_status = ?, published_url = ?, updated_at = CURRENT_TIMESTAMP
                WHERE slug = ?
            """, (new_status, published_url, slug))
        else:
            cursor.execute("""
                UPDATE videos SET upload_status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE slug = ?
            """, (new_status, slug))
        conn.commit()
        return cursor.rowcount > 0


def update_shopee_link(slug: str, new_link: str) -> bool:
    """Update Shopee affiliate link and update description & comments."""
    from tools.generate_marketing_meta import generate_marketing_meta
    v = get_video(slug)
    if not v:
        return False

    meta = generate_marketing_meta({
        "slug": slug,
        "title": v["book_title"],
        "author": v["author"],
        "core_message": v["core_message"]
    }, shopee_link=new_link)

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE videos SET
                shopee_aff_link = ?,
                pinned_comment = ?,
                short_comment_replies = ?,
                description = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE slug = ?
        """, (new_link, meta["pinned_comment"], meta["short_comment_reply"], meta["description"], slug))
        conn.commit()
        return cursor.rowcount > 0


def export_to_csv(csv_path: str = None) -> str:
    """Export all video data into an Excel-friendly CSV (UTF-8 BOM)."""
    init_db()
    out_csv = Path(csv_path) if csv_path else OUTPUTS_DIR / "video_publishing_plan.csv"
    videos = list_videos()

    fieldnames = [
        "id", "slug", "book_title", "author", "upload_status",
        "title_curiosity", "shopee_aff_link", "published_url",
        "local_video_path", "cover_image_path", "video_with_cover_path",
        "hashtags", "pinned_comment", "description"
    ]

    with open(out_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for v in videos:
            writer.writerow(v)

    return str(out_csv)


def format_upload_kit(slug: str) -> str:
    """Format full copy-paste kit for publishing 1 video."""
    v = get_video(slug)
    if not v:
        return f"❌ Không tìm thấy video có slug: {slug}"

    alts = []
    try:
        alts = json.loads(v["alternative_titles"])
    except Exception:
        pass

    alt_str = "\n".join([f"   • {a}" for a in alts])

    output = f"""
================================================================================
🚀 GÓI THÔNG TIN UPLOAD VIDEO: [{v['book_title']} - {v['author']}]
================================================================================
Trạng thái hiện tại: [{v['upload_status']}]
File Video gốc:        {v['local_video_path'] or 'CHƯA CÓ'}
File Ảnh bìa (9:16):    {v['cover_image_path'] or 'CHƯA TẠO'}
File Video kèm Ảnh bìa: {v['video_with_cover_path'] or 'CHƯA GHÉP'}
Link Shopee Affiliate:  {v['shopee_aff_link']}

--------------------------------------------------------------------------------
📌 1. TIÊU ĐỀ VIDEO HIẾU KỲ (CLICK-THROUGH RATE CAO):
--------------------------------------------------------------------------------
{v['title_curiosity']}

[Gợi ý các tiêu đề phụ để A/B test hoặc đăng Reels/TikTok]:
{alt_str}

--------------------------------------------------------------------------------
💬 2. BÌNH LUẬN GHIM (PINNED COMMENT - TRANH LUẬN + AFFILIATE):
--------------------------------------------------------------------------------
{v['pinned_comment']}

--------------------------------------------------------------------------------
📝 3. MÔ TẢ VIDEO (DESCRIPTION):
--------------------------------------------------------------------------------
{v['description']}

--------------------------------------------------------------------------------
🏷️ 4. HASHTAGS VIRAL:
--------------------------------------------------------------------------------
{v['hashtags']}

--------------------------------------------------------------------------------
💬 5. MẪU TRẢ LỜI BÌNH LUẬN NHANH KHI KHÁN GIẢ HỎI TÊN SÁCH:
--------------------------------------------------------------------------------
{v['short_comment_replies']}
================================================================================
"""
    return output


def batch_generate_all_covers(inject_video: bool = False) -> Tuple[int, int]:
    """
    Generate 9:16 vertical cover images for all books in DB.
    Optionally inject cover frame at 0:00 into final MP4 video.
    """
    from tools.cover_generator import generate_shorts_cover, inject_cover_to_video

    init_db()
    videos = list_videos()
    cover_count = 0
    inject_count = 0

    with get_db_connection() as conn:
        cursor = conn.cursor()
        for v in videos:
            slug = v["slug"]
            hook_title = v["title_curiosity"]
            book_title = v["book_title"]
            author = v["author"]
            video_path = v["local_video_path"]

            # Generate Cover PNG
            cover_path = generate_shorts_cover(slug, hook_title, book_title, author)
            cover_count += 1

            with_cov_path = ""
            if inject_video and video_path and os.path.exists(video_path):
                out_cov_video = WITH_COVER_DIR / f"{slug}_with_cover.mp4"
                print(f"🎬 Đang ghép khung ảnh bìa vào đầu video: {slug}...")
                ok = inject_cover_to_video(video_path, cover_path, str(out_cov_video))
                if ok:
                    with_cov_path = str(out_cov_video)
                    inject_count += 1

            cursor.execute("""
                UPDATE videos SET
                    cover_image_path = ?,
                    video_with_cover_path = COALESCE(NULLIF(?, ''), video_with_cover_path),
                    updated_at = CURRENT_TIMESTAMP
                WHERE slug = ?
            """, (cover_path, with_cov_path, slug))
        conn.commit()

    return cover_count, inject_count


if __name__ == "__main__":
    print("🔄 Đang đồng bộ hóa toàn bộ video từ configs vào Database...")
    synced = sync_all_from_configs()
    print(f"✅ Đã đồng bộ {synced} video vào Database tại: {DB_PATH}")

    print("\n📊 Xuất báo cáo kế hoạch xuất bản ra Excel / CSV...")
    csv_file = export_to_csv()
    print(f"✅ Đã xuất file CSV tại: {csv_file}")



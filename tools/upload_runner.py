"""
upload_runner.py - Kiểm tra và thực thi upload video theo plan lên Facebook Reels
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import json
import sqlite3
from datetime import datetime, timedelta

from tools.fb_video_uploader import upload_facebook_reel, post_comment, load_default_page_config
from tools.video_db import get_video, update_status



def test_upload_first_episode():
    slug = "dam_bi_ghet_tap1"
    print("=" * 65)
    print(f"🎬 BẮT ĐẦU ĐĂNG TẬP MỞ MÀN: {slug}")
    print("=" * 65)
    
    video_info = get_video(slug)
    if not video_info:
        print(f"[X] Không tìm thấy slug {slug} trong Database!")
        return

    # Kiểm tra file video
    video_path = video_info.get("video_with_cover_path") or video_info.get("local_video_path")
    print(f"File video: {video_path}")
    if not video_path or not os.path.exists(video_path):
        print(f"[X] File không tồn tại trên ổ cứng!")
        return

    title = video_info.get("title_curiosity")
    hashtags = video_info.get("hashtags")
    aff_link = video_info.get("shopee_aff_link")
    pinned_comment = video_info.get("pinned_comment")

    caption = f"{title}\n\n📖 {video_info.get('book_title')} - {video_info.get('author')}\n"
    if aff_link:
        caption += f"🛒 Link mua sách chính hãng: {aff_link}\n"
    caption += f"\n{hashtags}"

    print(f"\n[Caption sẽ đăng]:\n{caption}\n")
    print(f"[Comment sẽ bắn]:\n{pinned_comment}\n")
    print("-" * 65)

    # Đăng video lên Facebook Reels
    print("[*] Đang gửi video lên Facebook Reels API...")
    fb_video_id = upload_facebook_reel(video_path=video_path, caption=caption)

    if fb_video_id:
        print(f"\n[OK] Đã đăng Reels thành công! ID: {fb_video_id}")
        
        # Bắn comment ghim chứa link sản phẩm Shopee
        print("[*] Đang tự động bắn comment chứa link Shopee Affiliate...")
        comment_id = post_comment(fb_video_id, pinned_comment)
        
        # Cập nhật database
        watch_url = f"https://www.facebook.com/reel/{fb_video_id}"
        update_status(slug, "ĐÃ ĐĂNG", watch_url)
        print(f"\n🎉 [HOÀN TẤT] Video đã lên sóng tại: {watch_url}")
        return watch_url

    else:
        print("[X] Đăng video thất bại!")
        return None

if __name__ == "__main__":
    test_upload_first_episode()

#!/usr/bin/env python3
"""
fb_post_uploader.py - Tự động đăng Bài viết kèm Ảnh (Photo Post) hoặc Lên lịch đăng lên Fanpage Facebook.
Sử dụng Page Access Token vĩnh viễn và Meta Graph API v22.0.
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime, timezone, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tools.fb_video_uploader import load_default_page_config, GRAPH_API_VERSION, BASE_URL


def upload_facebook_photo(
    photo_path: str,
    caption: str,
    scheduled_publish_time: int = None,
    page_id: str = None,
    page_token: str = None,
    dry_run: bool = False
) -> dict:
    """
    Đăng 1 ảnh kèm nội dung bài viết lên Facebook Fanpage.
    Hỗ trợ lên lịch xuất bản tự động (scheduled_publish_time là Unix timestamp).
    
    Quy tắc Meta Graph API:
    - Nếu đăng ngay: published=True
    - Nếu lên lịch: published=False, scheduled_publish_time nằm trong khoảng [10 phút, 75 ngày].
    """
    if not page_id or not page_token:
        cfg = load_default_page_config()
        page_id = page_id or cfg["page_id"]
        page_token = page_token or cfg["page_access_token"]

    if not os.path.exists(photo_path):
        print(f"[X] Không tìm thấy file ảnh: {photo_path}")
        return None

    if dry_run:
        print("\n" + "=" * 60)
        print("🔍 [DRY-RUN - CHẾ ĐỘ KIỂM TRA] THÔNG TIN BÀI VIẾT:")
        print(f"  - Fanpage ID: {page_id}")
        print(f"  - File ảnh: {photo_path}")
        if scheduled_publish_time:
            tz_vn = timezone(timedelta(hours=7))
            dt = datetime.fromtimestamp(scheduled_publish_time, tz=tz_vn)
            print(f"  - Lịch đăng: {dt.strftime('%d/%m/%Y lúc %H:%M (Giờ VN)')}")
        else:
            print("  - Lịch đăng: ĐĂNG NGAY LẬP TỨC")
        print("  - Nội dung bài viết:\n" + "-" * 40)
        print(caption)
        print("-" * 40)
        return {"dry_run": True, "status": "SIMULATED_OK"}

    url = f"{BASE_URL}/{page_id}/photos"
    
    params = {
        "access_token": page_token,
        "caption": caption
    }

    if scheduled_publish_time:
        params["published"] = "false"
        params["scheduled_publish_time"] = scheduled_publish_time
    else:
        params["published"] = "true"

    file_size_kb = os.path.getsize(photo_path) / 1024
    print(f"[*] Đang gửi ảnh lên Fanpage {page_id}...")
    print(f"    - File: {os.path.basename(photo_path)} ({file_size_kb:.1f} KB)")

    with open(photo_path, "rb") as f:
        files = {"source": f}
        resp = requests.post(url, data=params, files=files, timeout=60)

    if resp.status_code == 200:
        data = resp.json()
        photo_id = data.get("id")
        post_id = data.get("post_id")
        mode_str = f"ĐÃ LÊN LỊCH ({scheduled_publish_time})" if scheduled_publish_time else "ĐÃ ĐĂNG NGAY"
        print(f"[OK] [THÀNH CÔNG] {mode_str} bài viết lên Fanpage!")
        print(f"    - Photo ID: {photo_id}")
        if post_id:
            print(f"    - Post ID: {post_id}")
            print(f"    - Link bài viết: https://www.facebook.com/{post_id}")
        return data
    else:
        print(f"[X] Đăng bài thất bại ({resp.status_code}):", resp.text)
        return None


if __name__ == "__main__":
    cfg = load_default_page_config()
    print("=" * 60)
    print(f"FACEBOOK POST UPLOADER - FANPAGE: {cfg['page_name']} (ID: {cfg['page_id']})")
    print("=" * 60)
    print("Kiểm tra Dry-Run với ảnh demo:")
    demo_img = str(BASE_DIR / "outputs" / "posts" / "demo_dam_bi_ghet_4x5.png")
    test_caption = (
        "Tự do không phải là làm mọi điều mình thích.\n\n"
        "Tự do đích thực là khi bạn có đủ dũng khí để bị người khác ghét bỏ.\n\n"
        "📖 Dám Bị Ghét - Kishimi Ichiro\n"
        "#radio2am #dambighet #thuctinh"
    )
    upload_facebook_photo(demo_img, test_caption, dry_run=True)

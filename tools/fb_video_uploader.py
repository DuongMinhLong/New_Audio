"""
fb_video_uploader.py - Tự động đăng Video thường hoặc Thước phim (Reels) và Comment lên Fanpage Facebook
Sử dụng Page Access Token vĩnh viễn và Meta Graph API.
"""

import os
import sys
import json
import requests
from pathlib import Path

GRAPH_API_VERSION = "v22.0"
BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

def load_default_page_config():
    """Tải token và ID Fanpage: ưu tiên biến môi trường (.env), sau đó đến configs/fb_page_tokens.json"""
    env_token = os.getenv("FB_PAGE_ACCESS_TOKEN")
    env_page_id = os.getenv("FB_PAGE_ID")
    env_page_name = os.getenv("FB_PAGE_NAME", "Fanpage")

    if env_token and env_page_id:
        return {
            "page_name": env_page_name,
            "page_id": env_page_id,
            "page_access_token": env_token,
            "is_permanent": True
        }

    cfg_path = Path(__file__).resolve().parent.parent / "configs" / "fb_page_tokens.json"
    if cfg_path.exists():
        with open(cfg_path, "r", encoding="utf-8") as f:
            pages = json.load(f)
        if pages:
            return pages[0]

    raise FileNotFoundError("Không tìm thấy cấu hình Facebook trong cả .env lẫn configs/fb_page_tokens.json!")

def upload_standard_video(video_path: str, title: str, description: str, page_id: str = None, page_token: str = None):
    """
    Đăng video thông thường (16:9 ngang hoặc bất kỳ) lên Fanpage.
    """
    if not page_id or not page_token:
        cfg = load_default_page_config()
        page_id = page_id or cfg["page_id"]
        page_token = page_token or cfg["page_access_token"]

    if not os.path.exists(video_path):
        print(f"[X] Không tìm thấy file video: {video_path}")
        return None

    url = f"https://graph-video.facebook.com/{GRAPH_API_VERSION}/{page_id}/videos"
    params = {
        "access_token": page_token,
        "title": title,
        "description": description
    }
    
    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    print(f"[*] Đang tải video lên Fanpage {page_id}...")
    print(f"    - File: {os.path.basename(video_path)} ({file_size_mb:.2f} MB)")

    with open(video_path, "rb") as f:
        files = {"source": f}
        resp = requests.post(url, data=params, files=files, timeout=600)
    
    if resp.status_code == 200:
        data = resp.json()
        video_id = data.get("id")
        print(f"[OK] Đăng video thành công! Video ID: {video_id}")
        return video_id
    else:
        print(f"[X] Đăng video thất bại ({resp.status_code}):", resp.text)
        return None

def upload_facebook_reel(video_path: str, caption: str, scheduled_publish_time: int = None, page_id: str = None, page_token: str = None):
    """
    Đăng Thước phim (Facebook Reel 9:16) lên Fanpage qua Reels Publishing API.
    Hỗ trợ lên lịch đăng tự động (scheduled_publish_time là Unix timestamp).
    """
    if not page_id or not page_token:
        cfg = load_default_page_config()
        page_id = page_id or cfg["page_id"]
        page_token = page_token or cfg["page_access_token"]

    if not os.path.exists(video_path):
        print(f"[X] Không tìm thấy file video: {video_path}")
        return None

    file_size = os.path.getsize(video_path)
    file_size_mb = file_size / (1024 * 1024)
    print(f"[*] Khởi tạo đăng Reel lên Fanpage {page_id}...")
    print(f"    - File: {os.path.basename(video_path)} ({file_size_mb:.2f} MB)")

    # BƯỚC 1: Khởi tạo phiên tải lên
    init_url = f"{BASE_URL}/{page_id}/video_reels"
    init_payload = {
        "upload_phase": "start",
        "access_token": page_token
    }
    r1 = requests.post(init_url, data=init_payload, timeout=30)
    if r1.status_code != 200:
        print("[X] Bước 1 lỗi:", r1.text)
        return None
    
    init_data = r1.json()
    video_id = init_data.get("video_id")
    upload_url = init_data.get("upload_url")
    print(f"[1/3] Khởi tạo thành công! Video ID: {video_id}")

    # BƯỚC 2: Tải dữ liệu video lên máy chủ
    headers = {
        "Authorization": f"OAuth {page_token}",
        "offset": "0",
        "file_size": str(file_size)
    }
    with open(video_path, "rb") as f:
        video_bytes = f.read()

    print("[2/3] Đang truyền tải dữ liệu video...")
    r2 = requests.post(upload_url, headers=headers, data=video_bytes, timeout=600)
    if r2.status_code != 200:
        print("[X] Bước 2 lỗi:", r2.text)
        return None
    print("[2/3] Tải video lên máy chủ hoàn tất!")

    # BƯỚC 3: Công bố Thước phim (Publish Reel hoặc Schedule)
    publish_url = f"{BASE_URL}/{page_id}/video_reels"
    publish_payload = {
        "upload_phase": "finish",
        "access_token": page_token,
        "video_id": video_id,
        "video_state": "SCHEDULED" if scheduled_publish_time else "PUBLISHED",
        "description": caption
    }
    if scheduled_publish_time:
        publish_payload["scheduled_publish_time"] = scheduled_publish_time

    r3 = requests.post(publish_url, data=publish_payload, timeout=30)
    if r3.status_code == 200:
        mode_text = f"ĐÃ LÊN LỊCH ({scheduled_publish_time})" if scheduled_publish_time else "ĐÃ ĐĂNG NGAY"
        print(f"[3/3] [THÀNH CÔNG] {mode_text} Facebook Reel lên Trang!")
        print(f"    - Reel ID: {video_id}")
        return video_id
    else:
        print("[X] Bước 3 công bố lỗi:", r3.text)
        return None

def post_comment(post_or_video_id: str, message: str, page_token: str = None):
    """
    Tự động đăng bình luận vào bài viết hoặc video vừa đăng.
    """
    if not page_token:
        cfg = load_default_page_config()
        page_token = cfg["page_access_token"]

    url = f"{BASE_URL}/{post_or_video_id}/comments"
    payload = {
        "access_token": page_token,
        "message": message
    }
    resp = requests.post(url, data=payload, timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        comment_id = data.get("id")
        print(f"[OK] Đã đăng comment thành công! Comment ID: {comment_id}")
        return comment_id
    else:
        print(f"[X] Đăng comment thất bại ({resp.status_code}):", resp.text)
        return None

def upload_book_to_facebook(slug: str, is_reel: bool = True):
    """
    Tự động lấy thông tin cuốn sách từ Database, đăng Video/Reel lên Fanpage
    và tự động comment link sản phẩm (Shopee Affiliate / Pinned Comment).
    """
    from tools.video_db import get_video, update_status

    
    video_info = get_video(slug)
    if not video_info:
        print(f"[X] Không tìm thấy video với slug: {slug} trong Database!")
        return None

    # Tìm đường dẫn file video gốc (outputs/{slug}_final.mp4) có đầy đủ âm thanh giọng đọc & BGM
    video_path = video_info.get("local_video_path")
    if not video_path or not os.path.exists(video_path):
        candidate = Path(__file__).resolve().parent.parent / "outputs" / f"{slug}_final.mp4"
        if candidate.exists():
            video_path = str(candidate)
        else:
            candidate2 = Path(__file__).resolve().parent.parent / "outputs" / "books" / slug / f"{slug}_final.mp4"
            if candidate2.exists():
                video_path = str(candidate2)
            else:
                print(f"[X] Không tìm thấy file video cho sách {slug}: {video_path}")
                return None

    title = video_info.get("title_curiosity") or video_info.get("book_title")
    hashtags = video_info.get("hashtags", "#radio2am #sachhay")
    aff_link = video_info.get("shopee_aff_link", "")
    pinned_comment = video_info.get("pinned_comment", "")

    # Tạo nội dung Caption Reel: Tiêu đề + Giới thiệu sách + Link Shopee + Hashtags
    caption = f"{title}\n\n📖 Tác phẩm: {video_info.get('book_title')} - {video_info.get('author')}\n"
    if aff_link:
        caption += f"🛒 Mua sách chính hãng tại: {aff_link}\n"
    caption += f"\n{hashtags}"

    print(f"[*] Đang chuẩn bị đăng video sách: {video_info.get('book_title')}...")
    if is_reel:
        fb_video_id = upload_facebook_reel(video_path=video_path, caption=caption)
    else:
        fb_video_id = upload_standard_video(video_path=video_path, title=title, description=caption)

    if fb_video_id:
        # Tự động bình luận link sản phẩm / affiliate
        comment_text = pinned_comment if pinned_comment else (f"👉 Đặt mua cuốn sách '{video_info.get('book_title')}' chính hãng tại: {aff_link}" if aff_link else "")
        if comment_text:
            print(f"[*] Đang tự động comment link sản phẩm bên dưới video...")
            post_comment(fb_video_id, comment_text)

        # Cập nhật trạng thái trong database
        published_url = f"https://www.facebook.com/watch/?v={fb_video_id}"
        update_video_status(slug, "ĐÃ ĐĂNG", published_url)
        print(f"[THÀNH CÔNG] Đã đăng video và cập nhật Database: {published_url}")
        return fb_video_id

    return None

if __name__ == "__main__":
    cfg = load_default_page_config()
    print("=" * 60)
    print(f"FANPAGE HIỆN TẠI: {cfg['page_name']} (ID: {cfg['page_id']})")
    print(f"TRẠNG THÁI TOKEN: Vĩnh viễn (Never Expire)")
    print("=" * 60)
    print("Cách sử dụng trong code:")
    print("  from tools.fb_video_uploader import upload_facebook_reel, upload_standard_video, post_comment")
    print("  video_id = upload_facebook_reel('outputs/short.mp4', 'Caption video ở đây')")
    print("  post_comment(video_id, '👉 Cuốn sách gốc tại bình luận này!')")


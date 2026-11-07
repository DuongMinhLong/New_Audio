"""
get_fb_long_token.py - Tự động đổi Short-Lived User Token sang Page Access Token VĨNH VIỄN (Never Expire)
Hỗ trợ đăng Video thường và Facebook Reels.
"""

import sys
import json
import urllib.request
import urllib.parse

GRAPH_API_VERSION = "v22.0"
BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

def fetch_json(url: str, params: dict = None) -> dict:
    if params:
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}" if "?" not in url else f"{url}&{query_string}"
    else:
        full_url = url

    req = urllib.request.Request(full_url, headers={"User-Agent": "FBTokenHelper/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        try:
            return {"error": json.loads(err_body)}
        except Exception:
            return {"error": {"message": err_body}}
    except Exception as e:
        return {"error": {"message": str(e)}}

def exchange_for_long_lived_token(app_id: str, app_secret: str, short_token: str) -> str:
    """Đổi Short-Lived User Token lấy Long-Lived User Token (60 ngày)"""
    url = f"{BASE_URL}/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id.strip(),
        "client_secret": app_secret.strip(),
        "fb_exchange_token": short_token.strip()
    }
    data = fetch_json(url, params)
    if "error" in data:
        print("[!] Lỗi khi đổi Long-lived User Token:", data["error"])
        return None
    return data.get("access_token")

def get_permanent_page_tokens(long_user_token: str) -> list:
    """Từ Long-Lived User Token, lấy danh sách Page Token VĨNH VIỄN (Never Expire)"""
    url = f"{BASE_URL}/me/accounts"
    params = {
        "fields": "id,name,access_token,category,tasks",
        "access_token": long_user_token.strip()
    }
    data = fetch_json(url, params)
    if "error" in data:
        print("[!] Lỗi khi lấy Page Token:", data["error"])
        return []
    return data.get("data", [])

def check_token_info(token: str, app_id: str, app_secret: str):
    """Kiểm tra thời hạn sống của token qua Debug Tool"""
    url = f"{BASE_URL}/debug_token"
    params = {
        "input_token": token,
        "access_token": f"{app_id}|{app_secret}"
    }
    data = fetch_json(url, params)
    if "data" in data:
        info = data["data"]
        expires_at = info.get("expires_at", 0)
        is_valid = info.get("is_valid", False)
        type_ = info.get("type", "UNKNOWN")
        scopes = info.get("scopes", [])
        print(f"    - Loại token: {type_}")
        print(f"    - Hợp lệ: {is_valid}")
        print(f"    - Hết hạn: {'VĨNH VIỄN (Never Expire)' if expires_at == 0 else f'Sau {expires_at} giây'}")
        print(f"    - Quyền hạn (Scopes): {', '.join(scopes)}")
    else:
        print("    [!] Không thể debug token:", data)

def main():
    print("=" * 65)
    print(" CÔNG CỤ TẠO PAGE ACCESS TOKEN VĨNH VIỄN (NEVER EXPIRE)")
    print("=" * 65)
    
    app_id = input("1. Nhập App ID: ").strip()
    app_secret = input("2. Nhập App Secret: ").strip()
    short_token = input("3. Nhập User Access Token (từ Graph API Explorer): ").strip()
    
    if not (app_id and app_secret and short_token):
        print("[X] Vui lòng nhập đầy đủ App ID, App Secret và User Token!")
        return

    print("\n[*] Đang gửi yêu cầu đổi sang Long-Lived User Token (60 ngày)...")
    long_user_token = exchange_for_long_lived_token(app_id, app_secret, short_token)
    if not long_user_token:
        return
    print("[OK] Đã lấy thành công Long-Lived User Token!")

    print("\n[*] Đang lấy danh sách Fanpage và tạo Page Token VĨNH VIỄN...")
    pages = get_permanent_page_tokens(long_user_token)
    if not pages:
        print("[!] Không tìm thấy Fanpage nào do tài khoản này quản lý.")
        return

    print(f"\n[OK] Tìm thấy {len(pages)} Fanpage:")
    print("-" * 65)
    
    saved_tokens = []
    for i, p in enumerate(pages, 1):
        p_name = p.get("name")
        p_id = p.get("id")
        p_token = p.get("access_token")
        print(f"\n[{i}] Fanpage: {p_name} (ID: {p_id})")
        print(f"    Page Access Token Vĩnh Viễn:\n    {p_token}")
        
        print("    Kiểm tra hạn sử dụng:")
        check_token_info(p_token, app_id, app_secret)
        
        saved_tokens.append({
            "page_name": p_name,
            "page_id": p_id,
            "page_access_token": p_token
        })

    # Lưu ra file json để bot tự lấy đăng video
    output_path = "configs/fb_page_tokens.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(saved_tokens, f, ensure_ascii=False, indent=2)
    print("\n" + "=" * 65)
    print(f"[THÀNH CÔNG] Đã lưu thông tin Token vào: {output_path}")
    print("=" * 65)

if __name__ == "__main__":
    main()

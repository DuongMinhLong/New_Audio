import json
import urllib.request
import urllib.parse
from pathlib import Path

app_id = "1762562321520999"
app_secret = "3083fdb26adcddf3777a0c072607c797"
short_token = "EAAZADCoURmWcBS6pHZAYMEMuC5BpUnrBCf6H7OnorspMe08NWs55lkXCBDtfPTP5zow9KbY1j4oBVTtlHygDnd2DTaiqucDKUxCIRGEsVlnPSOE6pxMIX5A9DyQZAMkADsXiWrTx1QoZAAgxot8zktj8jDmF4KxbkT6iEUBFVTcTRrZA4xligvgsbYiBJoRhL911IzTLZA519GWEKFTMZBCeygItpYyEZCTL8fiz"

def fetch_json(url, params=None):
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "FBTokenHelper/1.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return {"error": json.loads(body)}
        except:
            return {"error": body}

# 1. Exchange for long-lived user token
print("[*] Đang gửi yêu cầu đổi token sang Long-Lived Token...")
exchange_url = "https://graph.facebook.com/v22.0/oauth/access_token"
params = {
    "grant_type": "fb_exchange_token",
    "client_id": app_id,
    "client_secret": app_secret,
    "fb_exchange_token": short_token
}
res = fetch_json(exchange_url, params)
print("Kết quả đổi token:", res)
long_user_token = res.get("access_token") if "access_token" in res else short_token

# 2. Get permanent page tokens
print("\n[*] Đang truy vấn Fanpages...")
accounts_url = "https://graph.facebook.com/v22.0/me/accounts"
accounts_res = fetch_json(accounts_url, {
    "fields": "id,name,access_token,category,tasks",
    "access_token": long_user_token
})

pages = accounts_res.get("data", [])
print(f"Tìm thấy {len(pages)} Fanpage.")

saved_tokens = []
for p in pages:
    page_name = p.get("name")
    page_id = p.get("id")
    page_token = p.get("access_token")
    
    # Debug token
    dbg = fetch_json("https://graph.facebook.com/v22.0/debug_token", {
        "input_token": page_token,
        "access_token": f"{app_id}|{app_secret}"
    })
    
    info = dbg.get("data", {})
    expires_at = info.get("expires_at", 0)
    is_valid = info.get("is_valid", False)
    scopes = info.get("scopes", [])
    
    print("\n--------------------------------------------------")
    print(f"Fanpage: {page_name} (ID: {page_id})")
    print(f"Token: {page_token}")
    print(f"Hợp lệ: {is_valid}")
    print(f"Hạn dùng (expires_at): {expires_at} -> {'VĨNH VIỄN (Never Expire)' if expires_at == 0 else f'Hết hạn: {expires_at}'}")
    print(f"Scopes: {', '.join(scopes)}")
    
    saved_tokens.append({
        "page_name": page_name,
        "page_id": page_id,
        "page_access_token": page_token,
        "is_permanent": (expires_at == 0)
    })

if saved_tokens:
    config_file = Path("configs/fb_page_tokens.json")
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(saved_tokens, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] Đã cập nhật {config_file}")
    
    # Cập nhật .env
    env_file = Path(".env")
    if env_file.exists():
        env_content = env_file.read_text(encoding="utf-8")
        lines = env_content.splitlines()
        new_lines = []
        for line in lines:
            if line.startswith("FB_PAGE_ACCESS_TOKEN="):
                new_lines.append(f"FB_PAGE_ACCESS_TOKEN={saved_tokens[0]['page_access_token']}")
            else:
                new_lines.append(line)
        env_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        print("[OK] Đã cập nhật FB_PAGE_ACCESS_TOKEN trong .env")

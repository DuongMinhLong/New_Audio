import sqlite3, os
from pathlib import Path

conn = sqlite3.connect('outputs/video_management.db')
c = conn.cursor()
c.execute('SELECT slug, book_title, title_curiosity, hashtags, shopee_aff_link FROM videos ORDER BY id')
rows = c.fetchall()

series_dict = {}
for slug, btitle, cur_title, htags, aff in rows:
    parts = slug.rsplit('_tap', 1)
    if len(parts) == 2:
        s_name = parts[0]
        ep_num = parts[1]
    else:
        s_name = slug
        ep_num = '1'
    if s_name not in series_dict:
        series_dict[s_name] = []
    
    mp4_path = f'outputs/{slug}_final.mp4'
    exists = os.path.exists(mp4_path)
    size_mb = os.path.getsize(mp4_path) / (1024*1024) if exists else 0
    series_dict[s_name].append({
        'slug': slug,
        'ep': ep_num,
        'book_title': btitle,
        'title_curiosity': cur_title,
        'aff': aff,
        'exists': exists,
        'size_mb': size_mb
    })

print("=== TỔNG HỢP CÁC SERIE SẴN SÀNG ===")
for s_name, eps in series_dict.items():
    ready_count = sum(1 for e in eps if e['exists'])
    all_exist = (ready_count == 4 and len(eps) == 4)
    status_str = "SẴN SÀNG 4/4 TẬP" if all_exist else f"CHƯA ĐỦ ({ready_count}/{len(eps)} tập)"
    print(f"\nSeries: {s_name.upper()} -> {status_str}")
    if all_exist:
        for e in eps:
            print(f"  - Tập {e['ep']}: {e['title_curiosity']} ({e['size_mb']:.1f} MB)")

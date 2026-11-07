#!/usr/bin/env python3
"""
manage_videos.py - Interactive CLI & Management Tool for Video Publishing & Affiliate Workflow
"""

import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tools.video_db import (
    init_db,
    sync_all_from_configs,
    list_videos,
    get_video,
    update_status,
    update_shopee_link,
    export_to_csv,
    format_upload_kit,
    batch_generate_all_covers
)
from tools.cover_generator import inject_cover_to_video, generate_shorts_cover


def print_banner():
    print("""
================================================================================
🎬 HỆ THỐNG QUẢN LÝ VIDEO, TIÊU ĐỀ HIẾU KỲ & SHOPEE AFFILIATE (RADIO 2AM)
================================================================================
""")


def show_video_table(videos: list):
    print(f"\n{'ID':<4} | {'STATUS':<11} | {'SLUG':<26} | {'TIÊU ĐỀ HIẾU KỲ (HIGH CTR)'}")
    print("-" * 90)
    for v in videos:
        status_icon = "🟢" if v["upload_status"] == "ĐÃ ĐĂNG" else ("🟡" if v["upload_status"] == "ĐÃ LÊN LỊCH" else "⚪")
        print(f"{v['id']:<4} | {status_icon} {v['upload_status']:<8} | {v['slug']:<26} | {v['title_curiosity'][:48]}")
    print("-" * 90)
    print(f"Tổng cộng: {len(videos)} video\n")

def menu():
    init_db()
    while True:
        print_banner()
        print("1. 📋 Xem danh sách tất cả video & trạng thái đăng")
        print("2. 🚀 Lấy thông tin 1 video để đăng (Title, Description, Pinned Comment, Link Sách)")
        print("3. 🔗 Cập nhật Link Shopee Affiliate cho 1 cuốn sách")
        print("4. 🌐 Cập nhật mã Shopee Affiliate chung cho TẤT CẢ sách")
        print("5. ✏️ Cập nhật Trạng thái Video (CHƯA ĐĂNG ➡️ ĐÃ ĐĂNG / ĐÃ LÊN LỊCH)")
        print("6. 🖼️ Tạo lại Ảnh Bìa 9:16 (Cover PNG) cho tất cả video")
        print("7. 🎬 Ghép Ảnh Bìa vào đầu 1 video (Tạo frame 0:00 làm Thumbnail Shorts/TikTok)")
        print("8. 🎬 Ghép Ảnh Bìa vào đầu TẤT CẢ video có sẵn trong outputs/")
        print("9. 📊 Xuất danh sách ra file Excel / CSV (video_publishing_plan.csv)")
        print("10. 🔄 Đồng bộ lại toàn bộ video từ thư mục configs")
        print("11. 📥 Nhập file kết quả Shopee Affiliate (Batch Custom Links) vào Database")
        print("12. ⚡ Tự động sản xuất Video Shorts hàng loạt (Voice ChatGPT + Pexels + Sub)")
        print("13. 📚 Sản xuất Video Series Đa Góc Nhìn (Pilot 3 cuốn x 4 tập = 12 video)")
        print("0. 🚪 Thoát")
        print("-" * 80)

        choice = input("👉 Chọn chức năng (0-13): ").strip()
        if choice == "0":
            print("\n👋 Tạm biệt!")
            break

        elif choice == "1":
            status_filter = input("Lọc theo trạng thái (nhấn Enter để xem tất cả, hoặc gõ 'CHƯA ĐĂNG', 'ĐÃ ĐĂNG'): ").strip()
            videos = list_videos(status_filter if status_filter else None)
            show_video_table(videos)
            input("Nhấn Enter để quay lại menu...")

        elif choice == "2":
            query = input("\nNhập ID hoặc Slug của sách (ví dụ: 1 hoặc 'dam_bi_ghet'): ").strip()
            if query:
                print(format_upload_kit(query))
            input("Nhấn Enter để quay lại menu...")

        elif choice == "3":
            slug = input("\nNhập Slug của sách cần đổi link Shopee: ").strip()
            v = get_video(slug)
            if not v:
                print(f"❌ Không tìm thấy video: {slug}")
            else:
                print(f"Sách: {v['book_title']}")
                print(f"Link hiện tại: {v['shopee_aff_link']}")
                new_link = input("Nhập Link Shopee Affiliate mới: ").strip()
                if new_link:
                    update_shopee_link(slug, new_link)
                    print(f"✅ Đã cập nhật link Shopee Affiliate cho {slug}!")
            input("Nhấn Enter để quay lại menu...")

        elif choice == "4":
            base_url = input("\nNhập base link Shopee Affiliate của bạn (ví dụ: https://s.shopee.vn/my_aff_id): ").strip()
            if base_url:
                confirm = input(f"Bạn có chắc muốn cập nhật link cho toàn bộ 56 video theo dạng {base_url}/[slug]? (y/n): ").strip().lower()
                if confirm == "y":
                    synced = sync_all_from_configs(custom_aff_base=base_url)
                    export_to_csv()
                    print(f"✅ Đã cập nhật Shopee Affiliate cho {synced} video!")
            input("Nhấn Enter để quay lại menu...")

        elif choice == "5":
            slug = input("\nNhập Slug của video cần cập nhật: ").strip()
            v = get_video(slug)
            if not v:
                print(f"❌ Không tìm thấy video: {slug}")
            else:
                print(f"Video: {v['book_title']} | Trạng thái hiện tại: {v['upload_status']}")
                print("1. CHƯA ĐĂNG\n2. ĐÃ LÊN LỊCH\n3. ĐÃ ĐĂNG\n4. LỖI")
                st_choice = input("Chọn trạng thái mới (1-4): ").strip()
                st_map = {"1": "CHƯA ĐĂNG", "2": "ĐÃ LÊN LỊCH", "3": "ĐÃ ĐĂNG", "4": "LỖI"}
                new_st = st_map.get(st_choice, "CHƯA ĐĂNG")

                pub_url = None
                if new_st == "ĐÃ ĐĂNG":
                    pub_url = input("Dán link video sau khi đăng (YouTube/TikTok link): ").strip()

                update_status(slug, new_st, pub_url)
                export_to_csv()
                print(f"✅ Đã cập nhật trạng thái [{new_st}] cho {slug}!")
            input("Nhấn Enter để quay lại menu...")

        elif choice == "6":
            print("\n🖼️ Đang sinh ảnh bìa 9:16 cho tất cả video...")
            c, _ = batch_generate_all_covers(inject_video=False)
            print(f"✅ Đã tạo {c} ảnh bìa dọc tại thư mục outputs/covers/!")
            input("Nhấn Enter để quay lại menu...")

        elif choice == "7":
            slug = input("\nNhập Slug của video muốn ghép ảnh bìa: ").strip()
            v = get_video(slug)
            if not v:
                print(f"❌ Không tìm thấy video: {slug}")
            else:
                v_in = v["local_video_path"]
                c_in = v["cover_image_path"] or str(Path("outputs/covers") / f"{slug}_cover.png")
                v_out = str(Path("outputs/with_cover") / f"{slug}_with_cover.mp4")

                if not os.path.exists(v_in):
                    print(f"❌ Không tìm thấy file video gốc: {v_in}")
                else:
                    if not os.path.exists(c_in):
                        generate_shorts_cover(slug, v["title_curiosity"], v["book_title"], v["author"])

                    print(f"🎬 Đang ghép khung ảnh bìa vào đầu video {slug}...")
                    ok = inject_cover_to_video(v_in, c_in, v_out, duration=0.40)
                    if ok:
                        from tools.video_db import get_db_connection
                        with get_db_connection() as conn:
                            conn.execute("UPDATE videos SET video_with_cover_path = ? WHERE slug = ?", (v_out, slug))
                            conn.commit()
                        print(f"✅ Video hoàn thiện lưu tại: {v_out}")
                        print("👉 Khi đăng lên YouTube Shorts / TikTok, hãy chọn frame đầu tiên làm Thumbnail!")
                    else:
                        print("❌ Ghép khung hình thất bại.")
            input("Nhấn Enter để quay lại menu...")

        elif choice == "8":
            confirm = input("\nBạn có chắc muốn ghép Ảnh Bìa vào đầu TẤT CẢ video trong outputs/? (y/n): ").strip().lower()
            if confirm == "y":
                print("🎬 Bắt đầu ghép ảnh bìa cho tất cả video...")
                c, inj = batch_generate_all_covers(inject_video=True)
                export_to_csv()
                print(f"✅ Đã ghép xong {inj} video vào thư mục outputs/with_cover/!")
            input("Nhấn Enter để quay lại menu...")

        elif choice == "9":
            csv_path = export_to_csv()
            print(f"\n✅ Đã xuất toàn bộ kế hoạch video ra file CSV tại:\n{csv_path}")
            print("👉 Bạn có thể mở file này bằng Microsoft Excel hoặc kéo thả vào Google Sheets!")
            input("Nhấn Enter để quay lại menu...")

        elif choice == "10":
            print("\n🔄 Đang đồng bộ hóa từ thư mục configs...")
            synced = sync_all_from_configs()
            export_to_csv()
            print(f"✅ Đã đồng bộ thành công {synced} video vào Database!")
            input("Nhấn Enter để quay lại menu...")

        elif choice == "11":
            print("\n📥 NHẬP FILE KẾT QUẢ TỪ SHOPEE AFFILIATE (EXCEL / CSV)")
            path = input("Nhập đường dẫn file (hoặc kéo thả file vào đây): ").strip('"\' ')
            if path:
                from tools.import_shopee_affiliate import import_from_excel_or_csv
                import_from_excel_or_csv(Path(path))
            input("Nhấn Enter để quay lại menu...")

        elif choice == "12":
            print("\n⚡ SẢN XUẤT VIDEO SHORTS HÀNG LOẠT (VOICE CHATGPT + PEXELS + SUB)")
            limit_str = input("Nhập số lượng video muốn tạo (nhấn Enter để tạo TẤT CẢ các video còn lại): ").strip()
            limit = int(limit_str) if limit_str.isdigit() else None
            from tools.batch_produce_all import produce_all
            produce_all(max_count=limit)
            input("Nhấn Enter để quay lại menu...")

        elif choice == "13":
            print("\n📚 SẢN XUẤT VIDEO SERIES ĐA GÓC NHÌN (3-4 TẬP/CUỐN)")
            print("  1. Sản xuất Batch 1 Pilot (Dám Bị Ghét, Tâm Lý Học Về Tiền, Atomic Habits - 12 tập)")
            print("  2. Sản xuất Batch 2 (Đắc Nhân Tâm, Deep Work, Can't Hurt Me - 12 tập)")
            print("  3. Sản xuất TOÀN BỘ 24 tập Series (Batch 1 + Batch 2)")
            sub_c = input("👉 Chọn gói series (1-3): ").strip()
            from tools.produce_series_batch import run_batch
            if sub_c == "1":
                run_batch("books_multi_series_pilot.json")
            elif sub_c == "2":
                run_batch("books_multi_series_batch2.json")
            elif sub_c == "3":
                run_batch("books_multi_series_pilot.json")
                run_batch("books_multi_series_batch2.json")
            else:
                print("Lựa chọn không hợp lệ!")
            input("Nhấn Enter để quay lại menu...")


        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại!")


if __name__ == "__main__":
    menu()


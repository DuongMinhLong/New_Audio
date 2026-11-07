# Quy Chuẩn Đăng Tải & Xuất Bản (Deployment & Social)

## 1. NGUYÊN TẮC BẢO TOÀN ÂM THANH KHI GHÉP COVER (ANTI-AUDIO CORRUPTION)
- **Nguyên nhân lỗi cũ**: Ghép 0.4 giây ảnh bìa tĩnh với video gốc bằng lệnh concat đơn giản làm lệch timestamp và sample rate, triệt tiêu luồng audio về 1 kb/s (video bị câm).
- **Quy tắc bắt buộc (`tools/cover_generator.py`)**:
  - Dùng `filter_complex` với bộ lọc tái lấy mẫu rõ ràng:
    `aformat=sample_rates=44100:channel_layouts=stereo` cho cả 2 luồng trước khi `concat=n=2:v=1:a=1`.
- **Kiểm tra âm lượng trước khi upload**:
  - Bắt buộc kiểm tra file qua FFmpeg volumedetect: `mean_volume` phải nằm trong khoảng **-24 dB đến -14 dB**. Tuyệt đối không upload file câm (1 kb/s).

---

## 2. QUY TRÌNH ĐĂNG TẢI LÊN FACEBOOK REELS & FANPAGE
- **Công cụ chính**:
  - `tools/fb_video_uploader.py`: Đăng Reels lên Fanpage 2AM.
  - `tools/fb_post_uploader.py`: Đăng bài viết kèm ảnh quote (tỉ lệ 4:5).
  - `tools/schedule_daily_posts.py`: Lên lịch tự động theo khung giờ vàng.
- **Quy chuẩn nguồn Upload**:
  - Luôn ưu tiên dùng file video gốc `outputs/{slug}_final.mp4` đã được chuẩn hóa EBU R128 (-14 LUFS).
- **Quản lý Dữ liệu & Shopee Affiliate**:
  - Tự động đồng bộ trạng thái đăng tải vào SQLite Database `video_management.db` qua `tools/video_db.py`.
  - Caption bài viết tự động gắn link Affiliate Shopee và bộ hashtag tối ưu tìm kiếm: `#2am #sachhay #phattrienbanthan #shorts #reels`.

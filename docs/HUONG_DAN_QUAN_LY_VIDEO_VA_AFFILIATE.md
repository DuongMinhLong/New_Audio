# 📚 HƯỚNG DẪN QUẢN LÝ VIDEO, TIÊU ĐỀ HIẾU KỲ & SHOPEE AFFILIATE CHO SHORTS / TIKTOK

Tài liệu này hướng dẫn chi tiết cách vận hành hệ thống Database, quy chuẩn đặt **Tiêu đề kích thích tò mò (High-CTR Title)**, giải pháp **Tạo Ảnh Bìa & Khung hình đầu video cho Shorts**, cùng **Chiến lược Comment & Description chốt đơn Shopee Affiliate**.

---

## 🚀 1. KHỞI CHẠY HỆ THỐNG QUẢN LÝ
Bạn có thể quản lý toàn bộ 56+ video chỉ với 1 cú nhấp chuột:
- **Cách 1 (Nhanh nhất)**: Double-click vào file **`manage_videos.bat`** trên Windows.
- **Cách 2**: Chạy lệnh từ terminal:
  ```bash
  python manage_videos.py
  ```

---

## 🗄️ 2. CẤU TRÚC DATABASE & FILE EXCEL KẾ HOẠCH XUẤT BẢN
Hệ thống sử dụng cơ sở dữ liệu SQLite siêu nhẹ tại:
- **Database**: `outputs/video_management.db`
- **File Excel / CSV đồng bộ**: `outputs/video_publishing_plan.csv` *(Định dạng UTF-8 BOM, mở bằng Excel hoặc Google Sheets không bao giờ bị lỗi font tiếng Việt!)*

### Các trường dữ liệu quản lý:
1. `id`: Số thứ tự video.
2. `slug`: Mã định danh (`dac_nhan_tam`, `dam_bi_ghet`, `xa_hoi_met_moi`...).
3. `book_title` & `author`: Tên sách và tác giả.
4. `upload_status`: Trạng thái (`CHƯA ĐĂNG` ⚪, `ĐÃ LÊN LỊCH` 🟡, `ĐÃ ĐĂNG` 🟢, `LỖI` 🔴).
5. `title_curiosity`: Tiêu đề giật tít hiếu kỳ (CTR cao, tối ưu hiển thị dưới 65 ký tự trên điện thoại).
6. `alternative_titles`: 3 - 4 tiêu đề phụ để A/B testing khi đăng TikTok, Reels hoặc YouTube Shorts.
7. `shopee_aff_link`: Link tiếp thị liên kết Shopee của bạn.
8. `pinned_comment`: Bình luận ghim (Khơi mào tranh luận + Link Shopee Affiliate).
9. `description`: Mô tả chuẩn SEO, kêu gọi hành động (CTA) và disclaimer.
10. `hashtags`: Bộ hashtag viral (`#shorts #sachhay #radio2am #tuduy...`).
11. `cover_image_path`: Đường dẫn file Ảnh bìa dọc 9:16 (`outputs/covers/[slug]_cover.png`).
12. `video_with_cover_path`: Đường dẫn video MP4 đã ghép sẵn 0.4s frame ảnh bìa ở giây đầu tiên (`outputs/with_cover/[slug]_with_cover.mp4`).
13. `published_url`: Link thực tế của video sau khi đã upload (để bạn theo dõi và đo lường view).

---

## 🖼️ 3. GIẢI PHÁP ẢNH BÌA / COVER CHO SHORTS & TIKTOK
Người dùng thường gặp vấn đề: **YouTube Shorts không cho tải thumbnail tuỳ chỉnh như video dài nếu không can thiệp từ đầu**.

Hệ thống đã giải quyết triệt để bằng 2 lựa chọn:
1. **File Ảnh Bìa Độc Lập 9:16 (1080x1920)**:
   - Toàn bộ 56 ảnh bìa đã được tự động render tại thư mục: `outputs/covers/`.
   - Thiết kế Typography phong cách điện ảnh tối (Cinematic Dark): Tiêu đề vàng/trắng tương phản cực mạnh, nổi bật trên màn hình di động, có nhãn nhận diện sách và Radio 2AM.
2. **Khung Hình Đầu Video (Intro Frame at 0:00)**:
   - Sử dụng chức năng **số 7 hoặc số 8** trong menu `manage_videos.bat`.
   - Hệ thống dùng FFmpeg chèn chính xác **0.4 giây** ảnh bìa vào giây đầu tiên của video (lưu tại `outputs/with_cover/`).
   - **Khi bạn đăng lên YouTube Shorts (trên điện thoại) hoặc TikTok**: Chỉ cần kéo thanh chọn khung hình về **đúng 0:00 giây đầu tiên**, video sẽ có ngay một chiếc Thumbnail triệu view cực kỳ bắt mắt trên Grid kênh!


---

## 🎯 4. CÔNG THỨC ĐẶT TIÊU ĐỀ KÍCH THÍCH TÒ MÒ (CURIOSITY GAP)
Muốn khán giả bấm vào xem, tiêu đề phải tạo ra một "khoảng trống tò mò" (Curiosity Gap) hoặc đánh sập một niềm tin cũ:

| Công thức | Nguyên lý tâm lý | Ví dụ thực tế trong hệ thống |
| :--- | :--- | :--- |
| **Bẻ gãy ảo tưởng** | Khiến người xem sốc vì điều họ tưởng là đúng hóa ra sai lầm | *Đừng Đọc Đắc Nhân Tâm Nếu Bạn Sợ Giả Tạo!* |
| **Nghịch lý phũ phàng** | Chỉ ra sự bất công hoặc trớ trêu trong đời sống | *Lý Do Người Chăm Chỉ Vẫn Nghèo Cả Đời!* |
| **Tát nước lạnh** | Vạch trần sự yếu đuối trốn tránh | *Càng Cố Gắng 'Chữa Lành', Bạn Càng Bế Tắc?* |
| **Thức tỉnh & giải thoát** | Chỉ ra căn nguyên của sự khổ đau | *Chừng Nào Còn Sợ Bị Ghét, Bạn Còn Làm Nô Lệ!* |

---

## 💬 5. CHIẾN LƯỢC BÌNH LUẬN & MÔ TẢ CHỐT ĐƠN AFFILIATE

### 1. Pinned Comment (Bình luận ghim trên đầu video):
- **Phần 1: Khơi mào tranh luận (Debate Hook)**: Đặt một câu hỏi nhức nhối để kích thích người xem vào cãi nhau hoặc chia sẻ trải nghiệm (Ví dụ: *"Giữa 'Được mọi người quý mến nhưng sống giả tạo' và 'Bị nhiều người ghét nhưng được sống thật với chính mình', bạn chọn cái nào?"*). Càng nhiều comment tranh luận, thuật toán càng đẩy video lên triệu view!
- **Phần 2: Giới thiệu giải pháp + Link Shopee Affiliate**: Không nói "hãy mua sách", mà nói: *"Cuốn sách đã giúp mình dám từ bỏ việc làm hài lòng người khác: [Tên Sách] - Link bản chính hãng mình mua ở đây: [LINK]"*.
- **Phần 3: Cảnh báo sách lậu**: Nhắc người xem tránh mua phải sách lậu in thiếu trang sai chữ để tăng độ tin cậy và kích thích nhấp link Shopee Mall chính hãng.

### 2. Video Description (Phần mô tả):
- Dòng 1: Tiêu đề hiếu kỳ đánh trúng cảm xúc.
- Dòng 2: Tóm tắt 1 câu trần trụi về bài học của cuốn sách.
- Call To Action (CTA): Link Shopee Affiliate kèm thông báo ưu đãi Freeship Extra và Voucher trong giỏ hàng.
- Viral Hashtags: Tự động gắn thẻ chuẩn SEO cho từng cuốn sách.

### 3. Short Reply Comment (Mẫu trả lời người xem):
- Khi khán giả để lại bình luận hỏi: *"Sách tên gì ad?", "Mua ở đâu?", "Đọc sách này có tác dụng gì?"*, bạn chỉ cần copy mẫu câu trả lời nhanh có sẵn trong hệ thống để rep ngay lập tức!

---

## ⚙️ 6. CÁCH ĐỔI MÃ LINK SHOPEE AFFILIATE CỦA BẠN
Khi bạn có tài khoản Shopee Affiliate (Shopee KOL/KOC):
1. Chạy file `manage_videos.bat`.
2. Chọn **Chức năng 4: Cập nhật mã Shopee Affiliate chung cho TẤT CẢ sách**.
3. Nhập đường dẫn link gốc của bạn (ví dụ: `https://s.shopee.vn/aff_cuaban`).
4. Hệ thống sẽ tự động cập nhật lại toàn bộ 56 cuốn sách, viết lại toàn bộ Description và Pinned Comment tương ứng, đồng thời xuất ra file Excel mới ngay lập tức!


---

## 📺 7. MÔ HÌNH SERIES ĐA GÓC NHÌN (MULTI-ANGLE BOOK SERIES)
Thay vì chỉ làm 1 video đơn lẻ 60s cho mỗi cuốn sách, hệ thống đã mở rộng mô hình **1 cuốn = Series 3 - 4 tập đa chiều**:
1. **Tập 1 - Cú Tát Thức Tỉnh**: Bẻ gãy ảo tưởng sai lầm phổ biến, tát nước lạnh vào mặt người nghe, kết thúc bằng Cliffhanger mồi sang Tập 2.
2. **Tập 2 - Ranh Giới Thực Chiến**: Kỹ thuật tâm lý và hành vi thực tế (cách từ chối, thiết lập môi trường, dựng ranh giới thép).
3. **Tập 3 - Bóc Trần Nghịch Lý**: Mặt tối ít người để ý trong sách, phản biện tư duy lối mòn, kích thích tranh luận nảy lửa dưới bình luận.
4. **Tập 4 - Đòn Bẩy Tự Do**: Tinh hoa giải phóng nhận thức, câu chốt đanh thép khẳng định bản lĩnh cá nhân, kêu gọi cày lại trọn bộ Playlist từ Tập 1.

### Các chuỗi Series đã hoàn tất sản xuất:
- **Batch 1 (Pilot)**:
  1. *Dám Bị Ghét* (4 tập)
  2. *Tâm Lý Học Về Tiền* (4 tập)
  3. *Atomic Habits* (4 tập)
- **Batch 2**:
  4. *Đắc Nhân Tâm* (4 tập)
  5. *Deep Work (Làm Việc Sâu)* (4 tập)
  6. *Can't Hurt Me (Không Thể Làm Tôi Tổn Thương)* (4 tập)
- **Tổng cộng**: 24 video độc thoại chuyên sâu kèm 24 thumbnail 0:00 sẵn sàng đăng tải.
- Toàn bộ video gốc nằm tại: `outputs/[slug]_final.mp4`.
- Video có sẵn ảnh bìa thumbnail 0:00 nằm tại: `outputs/with_cover/[slug]_with_cover.mp4`.
- Sử dụng chức năng số **13** trong `manage_videos.bat` để chạy lại hoặc mở rộng chuỗi series mới bất kỳ lúc nào!


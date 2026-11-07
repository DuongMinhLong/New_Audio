# Quy Chuẩn Sản Xuất Video Ngắn Triệu View (The 3-Second Viral Shorts Standard)

## 📌 Tổng Quan
Tài liệu quy chuẩn kỹ thuật (SOP) toàn diện để tự động hóa sản xuất video dọc 9:16 (TikTok, YouTube Shorts, Facebook Reels) đạt tỷ lệ giữ chân khán giả cao nhất (High-Retention Rate), kết hợp giọng đọc ChatGPT Read Aloud, B-roll Pexels điện ảnh tối màu, hiệu ứng chuyển động Ken Burns, phụ đề Segoe UI Black và chuẩn hóa âm thanh EBU R128.

---

## 🎯 1. NGUYÊN TẮC KỊCH BẢN & GIỌNG ĐỌC CHATGPT READ ALOUD (10/10)

### Độ dài chuẩn vàng
- **180 đến 220 từ** (thời lượng đọc thực tế: **58 – 62 giây**).
- Không viết quá ngắn (< 150 từ gây hụt cảm xúc) và không viết quá dài (> 240 từ làm video vượt quá 60s gây giảm tương tác trên Shorts).

### Quy tắc Dấu câu Tự nhiên (Natural Prosody - Anti-TTS Distortion)
- **TUYỆT ĐỐI CẤM IN HOA NGUYÊN TỪ**: Viết hoa chữ cái đầu câu bình thường. CẤM viết hoa toàn bộ từ khóa (như "HÈN NHÁT", "ÍCH KỶ") vì làm bộ đọc ChatGPT đánh vần từng chữ cái hoặc phát âm ngọng/sai trọng âm.
- **TUYỆT ĐỐI CẤM DẤU BA CHẤM (`...`) VÀ DẤU GẠCH NGANG DÀI (` — `)**: Dấu `...` hoặc ` — ` khiến ChatGPT ngắt nhịp kỳ quặc, phát ra âm bật hơi giả tạo hoặc đọc thành từ ngữ lạ.
- **DÙNG DẤU CÂU CHUẨN TIẾNG VIỆT**: Dấu chấm (`.`), dấu phẩy (`,`), dấu hỏi (`?`) và câu gãy gọn (3 – 7 từ mỗi vế). ChatGPT Read Aloud có khả năng tự suy diễn ngữ cảnh, nhấn nhá cảm xúc và ngắt nghỉ lấy hơi cực kỳ thông minh khi được cung cấp văn bản tiếng Việt chuẩn ngữ pháp.
- **XUỐNG DÒNG ĐÔI (`\n\n`)**: Đặt giữa các ý chính hoặc chuyển đổi góc nhìn để giọng đọc tự động có khoảng dừng 0.5s – 0.8s chuyển đoạn tự nhiên.

### Thu âm giọng đọc qua Chrome CDP
- Sử dụng công cụ `tools/chatwithgpt_server.py` kết nối trực tiếp với Chrome mở cổng CDP `9222`.
- File audio thô được xuất ra dưới định dạng AAC / MP3 (24000Hz mono), lưu trữ an toàn trong `cache/books/{slug}/audio.mp3`.

---

## 🎬 2. QUY TẮC NHỊP CẮT 3 GIÂY & B-ROLL ĐIỆN ẢNH (PACING & VISUALS)

### Quy tắc 3 giây (The 3-Second Rule Pacing)
- Khán giả video ngắn có sự chú ý thị giác rất nhanh. Giữ một góc máy tĩnh quá 4 giây sẽ gây cảm giác đơn điệu, nhàm chán.
- **Quy chuẩn**: Chia kịch bản 60 giây thành **15 đến 16 phân cảnh điện ảnh** (mỗi cảnh kéo dài **3.5s – 3.8s**).
- Nhịp cắt nhanh dồn dập, chuyển đổi góc máy liên tục theo sát từng câu thoại để duy trì sự tập trung tối đa của người xem.

### Chuyển động điện ảnh Slow Zoom (Ken Burns Push-in)
- Mọi cảnh quay khi chuẩn hóa (`normalize_shot`) bắt buộc tích hợp bộ lọc zoom chậm tiến về phía trước:
  ```bash
  zoompan=z='min(zoom+0.0010,1.07)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30
  ```
- Biến mọi clip tĩnh lặng thành cú máy Dolly có chiều sâu, tạo cảm giác thôi thúc và kịch tính.

### Bộ Từ Khóa B-Roll Định Tông (Dark Stoic Whitelist)
- Chỉ tìm kiếm các cảnh quay mang tính điện ảnh, u tối, nội tâm, khắc kỷ:
  - `dark silhouette man looking into camera moody shadows`
  - `hands typing and deleting message smartphone dark room`
  - `stressed office worker fake smile colleague desk evening`
  - `lonely figure walking under street lamp quiet rain night`
  - `dramatic lightning storm dark clouds striking sky moody`
  - `shadow puppet strings pulling tired puppet silhouette`
  - `vintage clock ticking rapidly dark empty office night`
  - `ancient philosopher marble statue dark dramatic lighting museum`
  - `dark endless spiral stairs vertigo psychological depth`
  - `stoic man silhouette standing on high rooftop overlooking dark city`
- **CẤM TIỆT 100%**: Các clip sinh hoạt đời thường, sáng trưng, đi dép lê, ngồi uống trà đọc sách, làm tụt mood nội dung.


---

## ⚙️ 3. NGUYÊN TẮC ÉP HỆ MÀU REC.709 CHỐNG RỤNG ÂM THANH FFMPEG

### Cơ chế lỗi từng gặp
Khi ghép nối các clip Pexels mang chuẩn màu **HDR (Rec.2020 / HLG)** với các clip **SDR (Rec.709)**, lệnh render cuối cùng qua `-filter_complex` gặp xung đột hệ màu, khiến FFmpeg tự động kích hoạt `Reconfiguring filter graph because video parameters changed`. Việc này xả trắng bộ đệm (audio buffer) của bộ lọc `amix`, làm **mất 6 đến 8 giây âm thanh** giữa chừng và gây lệch khớp phụ đề.

### Giải pháp kỹ thuật bắt buộc
Trong hàm `normalize_shot` / `normalize_scene`, bắt buộc ép cứng các cờ:
```bash
-c:v libx264 -preset fast -crf 20 \
-pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709
```
Đảm bảo 100% video nối bằng concat demuxer đồng nhất tuyệt đối, ngăn FFmpeg tái cấu hình filter graph giữa chừng.

---

## 📝 4. TYPOGRAPHY PHỤ ĐỀ HIỆN ĐẠI (`Segoe UI Black`)

### Cấu hình chuẩn ASS / SRT Filter
```ini
FontName=Segoe UI Black,FontSize=20,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2.8,Shadow=1.5,Alignment=2,MarginV=90
```
- **Font chữ**: `Segoe UI Black` (nét dày, đậm, lực, sang trọng trên màn hình điện thoại).
- **Màu chữ**: Vàng rực (`&H0000FFFF`), nổi bật trên mọi nền tối.
- **Viền & Đổ bóng**: Viền đen dày `Outline=2.8`, bóng mờ mềm mại `Shadow=1.5`, cấm dùng hộp đen `BorderStyle=3` che khuất khung hình.
- **Vị trí**: Căn lề dưới an toàn `MarginV=90` (tránh bị che bởi nút like/share/comment của TikTok, Reels, Shorts).

---

## 🔊 5. CHUẨN HÓA ÂM THANH EBU R128 & MIX BGM CHỐNG DEAD AIR

### Cấu trúc bộ lọc âm thanh chuẩn
```bash
-filter_complex \
  "[0:v]subtitles=subtitles.srt:force_style='FontName=Segoe UI Black,FontSize=20,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2.8,Shadow=1.5,Alignment=2,MarginV=90'[vout];" \
  "[1:a]loudnorm=I=-14:TP=-1.5:LRA=7,aformat=sample_rates=44100:channel_layouts=stereo[voice];" \
  "[2:a]volume=0.18,aformat=sample_rates=44100:channel_layouts=stereo[bgm];" \
  "[voice][bgm]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]" \
-map "[vout]" -map "[aout]" \
-c:v libx264 -preset fast -crf 20 \
-c:a aac -b:a 192k -shortest
```
- **Voice**: Chuẩn hóa EBU R128 (`loudnorm=I=-14:TP=-1.5:LRA=7`), đẩy giọng đọc lên to rõ, vang và đanh thép.
- **BGM**: Nhạc nền ambient đặt ở mức **`volume=0.18`** (~ -22 dB). Nhạc nền đệm êm ái phía dưới, xóa sạch hiện tượng "ngắt trắng / câm tiếng" (dead air) khi giọng đọc dừng nghỉ lấy hơi.
- **Tái lấy mẫu đồng bộ**: Bắt buộc thêm `aformat=sample_rates=44100:channel_layouts=stereo` cho cả 2 luồng trước khi vào `amix`.

---

## 🖼️ 6. GHÉP KHUNG HÌNH ẢNH BÌA THUMBNAIL (0.40S INTRO FRAME)
- Ghép 0.40 giây ảnh bìa dọc 1080x1920 có badge (TẬP 1, TẬP 2...) vào giây 0:00 của video bằng `tools/cover_generator.py`.
- Giúp người đăng video dễ dàng chọn ảnh bìa thumbnail ngay trên giao diện TikTok/Shorts/Reels.
- Sử dụng `filter_complex` với tái lấy mẫu rõ ràng `aformat=sample_rates=44100:channel_layouts=stereo` để chống lỗi triệt tiêu âm thanh (1 kb/s).

---

## 📋 7. CHECKLIST 6 ĐIỂM KIỂM ĐỊNH NGHIỆM THU TRƯỚC KHI XUẤT BẢN
1. [x] **Thời lượng**: Audio và Video khớp nhau đến $\pm 0.1$ giây (tổng 58s – 62s).
2. [x] **Toàn vẹn câu chữ**: Chạy Faster-Whisper kiểm tra 100% câu từ không bị nuốt chữ hay cắt cụt.
3. [x] **Âm lượng trung bình**: `mean_volume` nằm trong khoảng `-21.0 dB` đến `-19.5 dB`.
4. [x] **Nhạc nền BGM**: Chạy liên tục suốt video ở mức êm dịu, không bị ngắt quãng.
5. [x] **Typography**: Hiển thị font `Segoe UI Black` chữ vàng viền đen bóng mờ, không bị lỗi font tiếng Việt.
6. [x] **File Thumbnail**: File `outputs/with_cover/{slug}_with_cover.mp4` có audio 44.1kHz Stereo $\ge 192\text{ kb/s}$ hợp lệ.

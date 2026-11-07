# Quy Chuẩn Thu Âm & Xử Lý Audio (Audio Generation)

## 1. PHƯƠNG THỨC THU ÂM CHÍNH (CHATGPT READ ALOUD QUA CHROME CDP)
- **Công cụ**: `tools/chatwithgpt_server.py` kết nối trực tiếp với Google Chrome mở cổng CDP `9222`.
- **Yêu cầu môi trường**:
  - Chrome phải được khởi chạy với cờ `--remote-debugging-port=9222` (dùng file `launch_chrome_chatgpt.bat`).
  - ChatGPT Web phải đăng nhập sẵn và tab mở sẵn.
- **Cơ chế thu âm**:
  - Gửi nội dung kịch bản vào prompt ChatGPT Web.
  - Tự động kích hoạt tính năng **Đọc to** (Read Aloud).
  - Bắt luồng AAC stream từ mạng thời gian thực, lưu trữ an toàn và convert sang MP3 qua FFmpeg.
  - Lưu tại: `outputs/{slug}.mp3` và copy vào `cache/books/{slug}/audio.mp3`.

---

## 2. PHƯƠNG THỨC DỰ PHÒNG (FALLBACK: EDGE TTS)
- Khi Chrome CDP port 9222 không mở hoặc ChatGPT Web gặp lỗi:
  - Sử dụng Edge TTS giọng tiếng Việt tự nhiên (`vi-VN-HoaiMyNeural` hoặc `vi-VN-NamMinhNeural`).
  - Đảm bảo kịch bản đọc mượt mà, không gián đoạn.

---

## 3. CHUẨN HÓA ÂM THANH (EBU R128 NORMALIZATION)
- **Thông số chuẩn phát hành**:
  - Target Loudness: **-14 LUFS** (chuẩn TikTok, Reels, YouTube Shorts).
  - True Peak (TP): **-1.5 dB**.
  - Loudness Range (LRA): **7.0**.
  - Sample rate: **44100 Hz**, Kênh: **Stereo (2 channels)**.
- **Lệnh FFmpeg chuẩn hóa loudnorm 2-pass hoặc 1-pass**:
  ```bash
  ffmpeg -y -i input.mp3 -af loudnorm=I=-14:TP=-1.5:LRA=7:dual_mono=false:print_format=summary -ar 44100 -ac 2 normalized.mp3
  ```
- **Kiểm tra chất lượng**:
  - `mean_volume` bắt buộc nằm trong khoảng **-24 dB đến -14 dB**.
  - Tuyệt đối không để audio bị câm (1 kb/s) hoặc vượt ngưỡng clipping (> 0 dB).

---

## 4. QUY TẮC ĐỐI VỚI BGM (BACKGROUND MUSIC)
- Mix BGM bên dưới voice-over bằng FFmpeg `amix`.
- BGM giữ ở mức âm lượng nhẹ: `volume=0.05` đến `0.18` (khoảng -22 dB).
- Tắt tính năng chia đôi âm lượng mặc định của `amix`: `amix=inputs=2:duration=first:dropout_transition=2:normalize=0`.
- Thêm bộ lọc `aformat=sample_rates=44100:channel_layouts=stereo` cho cả Voice và BGM trước khi đưa vào `amix`.

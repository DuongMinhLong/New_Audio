# Quy Chuẩn Dựng Video 9:16 Shorts & 16:9 Long-Form (Video Creation)

## 1. NGUYÊN TẮC CỐT LÕI: TUYỆT ĐỐI KHÔNG ĐỂ LỆCH SUBTITLE
- Dòng thời gian B-roll (Visual Cuts: 10–12 cảnh, 4–7s/cảnh) và dòng thời gian Phụ đề (Speech Cues) PHẢI tách rời độc lập.
- Phụ đề PHẢI luôn được đồng bộ trực tiếp từ file âm thanh thực tế thông qua **Faster-Whisper** (`transcribe_audio_to_srt`).
- Cấm gán cứng thời lượng phụ đề theo thời lượng clip B-roll.

---

## 2. QUY CHUẨN VIDEO DỌC SHORTS (9:16 - 1080x1920)
- **B-roll từ Pexels**:
  - Tự động lọc định dạng dọc 9:16 (`width <= 1080` hoặc `height >= 1920`).
  - Mỗi cảnh dài 4 - 6 giây, chọn footage có chuyển động điện ảnh, tâm trạng trầm lắng/suy tư.
- **Color Grading**:
  - `contrast=1.15, brightness=-0.03, saturation=0.85, vignette=PI/4`.
- **Chống rụng âm thanh (Anti-Drop Audio)**:
  - Khi normalize từng shot, ép cứng chuẩn màu Rec.709:
    `-pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709`
  - Đồng bộ tần số lấy mẫu trước `amix`: `aformat=sample_rates=44100:channel_layouts=stereo`.
- **Kiểu Phụ Đề Shorts (ASS Subtitle)**:
  - Font: Arial, Size: 20-22, Màu chữ vàng rực (`&H0000FFFF`), Viền đen (`Outline=2.5`), Đổ bóng (`Shadow=1.5`).
  - `BorderStyle=1` (CẤM dùng hộp đen `BorderStyle=3`). Căn an toàn lề dưới: `MarginV=90`.

---

## 3. QUY CHUẨN VIDEO DÀI LONG-FORM (16:9 - 1920x1080)
- **Công cụ điều phối**: `tools/longform_pipeline.py` & `tools/longform_video_builder.py`.
- **Cấu trúc 5 Hồi (2.000 - 2.500 từ, 10 - 25 phút)**:
  - Thu âm từng Part độc lập (`part_1.mp3` ... `part_5.mp3`).
  - Ghép nối audio bằng FFmpeg kèm khoảng lặng ngắt nhịp 0.8s, chuẩn hóa EBU R128 (-14 LUFS).
- **Hình ảnh B-roll 16:9**:
  - 25 cảnh 16:9 điện ảnh tối màu từ Pexels (`scale=1920:1080`, `contrast=1.12`, `vignette=PI/4`).
- **Phụ đề Documentary**:
  - Font Arial, Size 21, Chữ vàng ấm (`&H0000FFFF`), Viền đen mảnh (`Outline=2.0`), `BorderStyle=1`, `MarginV=42`.
  - Tự động sửa lỗi phát âm Faster-Whisper bằng `tools/ai_clean_srt.py`.

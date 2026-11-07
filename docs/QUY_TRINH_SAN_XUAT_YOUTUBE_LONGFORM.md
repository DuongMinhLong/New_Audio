# 🎬 QUY TRÌNH SẢN XUẤT VIDEO YOUTUBE DÀI (LONG-FORM 10 - 25 PHÚT)

> **Mô hình**: Video Essay Triết học Ứng dụng & Phân tích Sách Chiều sâu (Hybrid: Einzelgänger x The Burnout Society x Stoicism).  
> **Giọng đọc**: ChatGPT Read Aloud nguyên bản (thu âm qua Chrome CDP port 9222).  
> **Cơ chế**: Chia nhỏ từng Part (Chunking), Review 3 bước độc lập, Ghép nối kịch bản bằng Claude Sonnet 5.5 Max, ghép nối Audio bằng FFmpeg.

---

## 🏛️ PHÂN BỔ MÔ HÌNH AI & VAI TRÒ (QUA 9ROUTER PORT 20128)

| Giai đoạn | Mô hình phụ trách | Vai trò & Trách nhiệm |
| :--- | :--- | :--- |
| **1. Macro Outline** | `ag/claude-sonnet-5-5-high` *(Sonnet 5.5 Max)* | Định hình cấu trúc 5 Hồi vĩ mô, chia nhỏ mục tiêu, luận điểm và câu nối cho từng Part. |
| **2. Vòng lặp Part (Bước 2.1 - 2.3)** | `ag/gemini-3.8-flash-high` | **2.1 Draft**: Viết bản thảo thô theo đề cương Part.<br>**2.2 Critique**: Bóc 3 lỗi nặng nhất (soi mùi AI, sáo rỗng, lặp ý).<br>**2.3 Rewrite**: Viết lại sửa sạch lỗi, chèn ký tự TTS (`...`, ` — `, `IN HOA`, `\n\n`). |
| **3. Master Final Polish** | `ag/claude-sonnet-5-5-high` *(Sonnet 5.5 Max)* | Đọc tổng thể 5 Part ghép, mài giũa các câu nối (bridges) mượt mà, bảo toàn 100% ký tự biểu cảm TTS. |
| **4. Part Audio Capture** | `chatwithgpt_server.py` (CDP 9222) | Đưa từng Part vào ChatGPT Read Aloud và bắt luồng AAC stream chuyển sang MP3. |
| **5. Master Audio Concat** | **FFmpeg** | Ghép nối các Part với khoảng lặng 0.8s, chuẩn hóa âm thanh chuẩn EBU R128 (-14 LUFS). |

---

## 🏗️ CẤU TRÚC 5 HỒI CỦA VIDEO DÀI (12 - 16 PHÚT)

1. **Part 1 - The Modern Trap (Hiện Thực Trần Trụi & Hook Bắt Quả Tang)** (~350 - 450 từ)
   - Bắt quả tang nỗi đau lúc nửa đêm (1h sáng, cày 11 tiếng về vẫn tội lỗi, lướt điện thoại).
   - Tuyệt đối CẤM chào hỏi, CẤM nêu tên sách ở 30s đầu.
2. **Part 2 - The Core Lens (Mổ Xẻ Bản Chất Qua Cuốn Sách)** (~500 - 650 từ)
   - Đưa cuốn sách vào như chìa khóa tâm lý/triết học: Phân tích cơ chế "Xã hội thành tích", "Bạo lực của sự tích cực", "Kẻ bóc lột và kẻ bị bóc lột là một".
3. **Part 3 - The Contrarian Deconstruction (Tư Duy Ngược & Đập Tan Self-Help Sáo Rỗng)** (~450 - 550 từ)
   - Bóc trần bẫy "chữa lành" độc hại: Mua nến thơm, đi retreat chỉ là "trạm sạc pin" để thứ Hai quay lại làm nô lệ.
4. **Part 4 - The Strategic Framework (Hệ Thống Hành Động Thực Chiến)** (~500 - 600 từ)
   - 3 bài tập cụ thể: *Quyền năng của sự phủ định (dám không làm gì)*, *Tách danh tính khỏi thành tích*, *Đặt đường biên cho cai ngục nội tâm*.
5. **Part 5 - The Awakening Monologue (Độc Thoại Thức Tỉnh & Lời Kết)** (~250 - 350 từ)
   - Hạ giọng trầm ấm, lắng đọng triết lý nhân sinh, cho phép bản thân được làm một con người bình thường.

---

## 🚀 HƯỚNG DẪN VẬN HÀNH 1-CLICK

### Cách 1: Chạy bằng Batch File (Giao diện menu đơn giản)
Nhấp đúp chuột vào file:
```
c:\New_audio\run_longform.bat
```
Chọn slug sách và chế độ (1: Toàn bộ A-Z, 2: Outline, 3: Script, 4: Audio, 5: Concat).

---

### Cách 2: Chạy trực tiếp từ dòng lệnh (CLI)

```powershell
# 1. Chạy trọn gói từ A đến Z (Outline -> Script 5 parts -> Sonnet Master -> Audio ChatGPT -> Concat FFmpeg)
python tools/longform_pipeline.py --slug xa_hoi_met_moi_long --mode all

# 2. Chỉ tạo Đề cương (Outline) bằng Claude Sonnet 5.5 Max:
python tools/longform_pipeline.py --slug xa_hoi_met_moi_long --mode outline

# 3. Chỉ viết kịch bản (Gemini 3-step từng part + Sonnet 5.5 tổng duyệt):
python tools/longform_pipeline.py --slug xa_hoi_met_moi_long --mode script

# 4. Chỉ thu âm từng Part bằng ChatGPT Read Aloud:
python tools/longform_pipeline.py --slug xa_hoi_met_moi_long --mode audio

# 5. Chỉ ghép nối các Part audio đã thu và chuẩn hóa -14 LUFS:
python tools/longform_pipeline.py --slug xa_hoi_met_moi_long --mode concat
```

---

## 📂 THƯ MỤC LƯU TRỮ THÀNH PHẨM

* **Kịch bản chi tiết từng phần & bản tổng duyệt**:
  `c:\New_audio\drafts\longform\[slug]\`
  - `00_outline.json`: Đề cương vĩ mô Sonnet 5.5.
  - `part_1_draft.txt` ... `part_5_draft.txt`: Bản thảo Gemini 3.8.
  - `part_1_critique.txt` ... `part_5_critique.txt`: Báo cáo phản biện bóc lỗi Gemini 3.8.
  - `part_1_final.txt` ... `part_5_final.txt`: Kịch bản hoàn thiện chèn TTS của từng Part.
  - `full_script_final.txt`: Kịch bản tổng thể đã được Sonnet 5.5 mài giũa câu nối liền mạch.
* **Âm thanh thành phẩm**:
  `c:\New_audio\outputs\longform\[slug]\`
  - `part_1.mp3` ... `part_5.mp3`: File giọng đọc ChatGPT Read Aloud của từng phần.
  - `[slug]_full_audio.mp3`: File âm thanh hoàn chỉnh dài 12 - 15 phút (chuẩn Studio 48000Hz, EBU R128 -14 LUFS).

  - `[slug]_final.mp4`: File Video YouTube 16:9 Full HD hoàn chỉnh (B-roll điện ảnh, phụ đề Netflix, âm thanh chuẩn EBU R128).

---

## 🎞️ BƯỚC 6: DỰNG VIDEO 16:9 FULL HD (NETFLIX SUBTITLES)

Video builder (`tools/longform_video_builder.py`) hỗ trợ:
- Tự động tải 25 cảnh B-roll 16:9 chuẩn Cinematic Landscape từ Pexels.
- Cắt chuẩn hóa 1920x1080 30fps kèm bộ lọc màu điện ảnh (`contrast=1.12`, `vignette=PI/4`).
- Trích xuất phụ đề tự động bằng Faster-Whisper CPU (int8).
- Làm sạch lỗi phát âm bằng kịch bản gốc.
- Phụ đề chuẩn Netflix: `BorderStyle=1, Outline=2.0, Shadow=1.5, MarginV=42, FontSize=21`, chữ vàng ấm `&H0000FFFF`.
- Lệnh chạy:
  ```powershell
  python tools/longform_pipeline.py --slug [slug] --mode video
  ```


---

## 📚 KHO CHỦ ĐỀ SÁCH & XÃ HỘI (PRE-CONFIGURED TOPICS)

Các chủ đề được cấu hình sẵn trong `configs/books_longform.json` và bộ từ khóa cảnh quay tương ứng trong `tools/longform_video_builder.py`:

| Chủ đề / Slug | Thể loại | Cuốn sách cốt lõi | Huyệt nỗi đau Xã hội & Gen Z |
| :--- | :--- | :--- | :--- |
| `xa_hoi_met_moi_long` | **Xã hội / Triết học** | *Xã Hội Mệt Mỏi (The Burnout Society)* - Byung-Chul Han | Hội chứng kiệt sức thầm lặng, bạo lực của sự tích cực, bẫy 'chữa lành' trốn tránh, làm việc kiệt sức nhưng vẫn tự trách mình. |
| `tam_ly_hoc_ve_tien_long` | **Tài chính / Tâm lý Xã hội** | *Tâm Lý Học Về Tiền (The Psychology of Money)* - Morgan Housel | Mua trước trả sau (BNPL), bão giá nhà tăng gấp 3 lương đứng yên, áp lực flexing và bi kịch của những kẻ giàu giả tạo. |
| `dam_bi_ghet_long` | **Tâm lý / Bản lĩnh Sống** | *Dám Bị Ghét (The Courage to Be Disliked)* - Kishimi Ichiro & Koga Fumitake | Nỗi sợ bị phán xét, hội chứng 'người tốt' phục tùng làm hài lòng tất cả mọi người, overthinking mạng xã hội lúc nửa đêm. |

---

## 🧹 CÔNG NGHỆ LÀM SẠCH PHỤ ĐỀ AI TỰ ĐỘNG (AI SRT CLEANER)

- File công cụ: `tools/ai_clean_srt.py` (tích hợp trực tiếp vào `tools/longform_video_builder.py`).
- Cơ chế: Sau khi Faster-Whisper trích xuất phụ đề (thường mắc lỗi ngữ âm dấu câu tiếng Việt do bộ giải mã int8), hệ thống tự động gửi `subtitles.srt` cùng `full_script_final.txt` lên `ag/gemini-3.8-flash-high`.
- Kết quả: Giữ nguyên 100% các mốc thời gian mili-giây, sửa toàn bộ lỗi chính tả tiếng Việt (`Xô giữ` ➔ `Số dư`, `một chiều` ➔ `một triệu`, `rất on` ➔ `rất ổn`, `dư liệu` ➔ `dữ liệu`). Phụ đề nét căng, chuẩn xác tuyệt đối.


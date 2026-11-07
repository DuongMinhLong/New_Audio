# Workspace New_audio - MCP ChatWithGPT & Automated TTS Pipeline

Hệ thống tích hợp sẵn **MCP Server `chatwithgpt`** cho Cline / Claude Dev, hỗ trợ trò chuyện trực tiếp với ChatGPT và **tự động tải giọng đọc Read Aloud (Đọc to) chuẩn phòng thu (AAC & MP3)** qua Chrome CDP và FFmpeg.

---

## 🛠️ Công Cụ Cung Cấp Cho Cline (MCP Tools)

| Tool | Mô tả |
| :--- | :--- |
| `text_to_audio(text, output_name, convert_to_mp3)` | **Tự động 100%**: Nhận văn bản bất kỳ, yêu cầu ChatGPT đọc và xuất file audio gốc `.aac` kèm file `.mp3` chuẩn chất lượng cao. |
| `chat_and_get_audio(prompt, output_name, convert_to_mp3)` | **Tự động 100%**: Gửi câu hỏi/prompt sáng tạo tới ChatGPT, lấy câu trả lời và tự động bắt luồng audio Đọc to lưu thành `.mp3`. |
| `get_last_response_audio(output_name, convert_to_mp3)` | Tải ngay audio Đọc to của câu trả lời gần nhất đang có trên màn hình ChatGPT mà không cần gửi prompt mới. |
| `chat_with_gpt(prompt, mode)` | Gửi prompt trực tiếp và nhận phản hồi văn bản từ ChatGPT (`mode='web'` hoặc `mode='api'`). |
| `chatgpt_status()` | Kiểm tra trạng thái Chrome CDP (port 9222), FFmpeg converter và 9Router. |
| `chatgpt_launch()` | Khởi động trình duyệt Chrome với profile đã đăng nhập sẵn ChatGPT trên port 9222. |
| `chatgpt_new_chat()` | Điều hướng tab ChatGPT về cuộc hội thoại mới sạch sẽ. |

---

## 🎙️ Cơ Chế Tự Động Bắt Audio Read Aloud

1. **Kết Nối Trực Tiếp Qua Chrome CDP (Port 9222)**:
   - Điều khiển tab `chatgpt.com` đang đăng nhập thực tế.
   - Khi có phản hồi, tự động kích hoạt tính năng **Đọc to** (Read Aloud).
2. **Bắt Luồng Native Stream Chống Lộ Âm Thanh**:
   - Tự động can thiệp mute âm thanh của trình duyệt để quá trình diễn ra hoàn toàn êm ái, không làm phiền loa máy tính.
   - Lắng nghe luồng dữ liệu nhị phân gốc từ endpoint `/backend-api/synthesize` (chất lượng 24000 Hz AAC).
3. **Chuyển Đổi Sang MP3 Chuẩn Studio Bằng FFmpeg**:
   - Tự động convert luồng `.aac` thành định dạng `.mp3` tương thích 100% với CapCut, Adobe Premiere, DaVinci Resolve, v.v.
   - Lưu trữ tự động vào thư mục `outputs/`.

---

## 🚀 Hướng Dẫn Sử Dụng Nhanh

### Cách 1: Chạy Thử 1-Click Bằng Batch File
- Nhấp đúp vào file `test_generate_audio.bat`
- Nhập đoạn văn bản bạn muốn đọc (hoặc nhấn Enter để dùng mặc định).
- File audio `.mp3` và `.aac` sẽ xuất hiện ngay trong thư mục `outputs/`.

### Cách 2: Chạy Bằng Lệnh Dòng Lệnh (CLI)
```powershell
# Chuyển đổi văn bản thành giọng đọc MP3
python tools/chatwithgpt_server.py --audio "Chào mừng các bạn đến với kênh của tôi." intro_video

# Tải audio của câu trả lời mới nhất đang có trên ChatGPT
python tools/chatwithgpt_server.py --get-last-audio latest_reply

# Kiểm tra trạng thái kết nối
python tools/chatwithgpt_server.py --status
```

### Cách 3: Ra Lệnh Cho Cline Trong Chat
Bạn chỉ cần nói với Cline:
> *"Hãy dùng ChatGPT đọc to đoạn văn bản sau và lưu thành file MP3: [Nội dung]"*

Cline sẽ tự động gọi MCP tool `text_to_audio` và trả về đường dẫn file đã hoàn thiện.

---

## 📂 Cấu Trúc Thư Mục

- `tools/chatwithgpt_server.py`: Mã nguồn chính của MCP Server.
- `tools/batch_book_generator.py`: Pipeline tự động hóa sản xuất hàng loạt video tóm tắt sách (TTS -> Faster-Whisper alignment -> Pexels B-roll -> Subtitles -> BGM mix).
- `tools/video_builder.py`: Tự động tìm kiếm & tải B-roll Pexels (9:16 HD), đồng bộ phụ đề chính xác từng mili-giây bằng Faster-Whisper, mix nhạc nền BGM (-22dB) và xuất video hoàn chỉnh.
- `configs/books_10.json`: Cấu hình 10 cuốn sách huyền thoại kinh điển kèm kịch bản 10/10 biểu cảm cao và danh sách cảnh quay điện ảnh Pexels.
- `configs/books_genz.json`: Cấu hình 6 cuốn sách chuyên sâu về Gen Z và các vấn đề xã hội nóng (Hustle culture, Lo âu mạng xã hội, Toxic positivity, Bẫy tiêu dùng, Cancel culture, Bế tắc quyết định).
- `build_10_books.bat`: Khởi chạy render 10 video tóm tắt sách kinh điển 1-click hoặc render theo thứ tự/slug.
- `build_genz_books.bat`: Khởi chạy render trọn bộ 6 video sách Gen Z và vấn đề xã hội 1-click hoặc render theo thứ tự/slug.
- `configs/books_genz_20.json`: Cấu hình 20 cuốn sách hot bắt trend dành cho Gen Z & giới trẻ (Quarter-life crisis, Trì hoãn, Chữa lành độc hại, Phông bạt tài chính, Bẫy chuột làm thuê, Trap boy/ghosting, Thao túng tâm lý Gaslighting, Ranh giới cá nhân, Sức mạnh người hướng nội, Bản lĩnh đơn độc, Sức mạnh hiện tại, Phong trào FIRE tuổi 30).
- `build_20_genz_books.bat`: Khởi chạy render trọn bộ 20 video sách Gen Z 1-click hoặc render theo thứ tự/slug.
- `configs/books_genz_batch3.json`: Cấu hình 20 cuốn sách triệu view Gen Z Phần 3 (Nghiện dopamine, 48 quy tắc quyền lực, Bản tính con người, Không thể xao nhãng, Cứ làm đi, Chủ nghĩa cốt lõi, Dám hạnh phúc, Sao chúng ta lại ngủ, Đàm phán đỉnh cao, Lãnh đạo trầm lặng, Xung quanh toàn kẻ ngốc, Tạo thời gian, Tối giản số, Lì lợm bền bỉ Grit, Đếch biết làm sao, Sự tập trung bị đánh cắp, Tư duy xác suất Poker, Sáng tạo như nghệ sĩ, Thiết kế cuộc đời, Ikigai).
- `build_genz_batch3.bat`: Khởi chạy render trọn bộ 20 video sách Gen Z Phần 3 (Batch 3) 1-click hoặc render theo thứ tự/slug.


- `outputs/`: Thư mục lưu trữ duy nhất các video thành phẩm hoàn chỉnh (`*_final.mp4`), tự động dọn sạch file tạm.
- `launch_chrome_chatgpt.bat`: Khởi động Chrome chế độ CDP port 9222.
- `test_generate_audio.bat`: Kiểm tra và tạo audio 1-click.
- `build_video.bat`: Tự động tải stock video từ Pexels, căn sub chuẩn từng giây và render video hoàn chỉnh 1-click.
- `test_chatwithgpt.bat`: Kiểm tra kết nối chat văn bản.
- `docs/QUY_TRINH_SAN_XUAT_AUDIO_SACH_10_10.md`: Quy trình chuẩn (SOP) từng bước sản xuất kịch bản + audio sách + video Pexels triệu view.
- `docs/framework_kich_ban_sach_10_10.md`: Framework chi tiết kèm kịch bản mẫu & bảng mã ký tự điều hướng biểu cảm TTS.





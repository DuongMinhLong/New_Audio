# 📖 QUY TRÌNH CHUẨN (SOP): SẢN XUẤT AUDIO & KỊCH BẢN SÁCH TRIỆU VIEW 10/10

> **Mục đích:** Quy trình từng bước (Step-by-Step) để sản xuất nội dung review sách chuyển đổi cao làm Shopee Affiliate.  
> **Nguyên tắc cốt lõi:** Hook gây sốc 3s đầu ➡️ Đào sâu góc khuất/nghịch lý ➡️ 0% mùi văn mẫu AI ➡️ 0% chèo kéo bán hàng ➡️ Gài ký tự điều hướng biểu cảm TTS ➡️ Xuất audio chuẩn phòng thu.

---

## 🧭 QUY TRÌNH 4 BƯỚC TỔNG QUAN

```
BƯỚC 1: Chọn cuốn sách & Lấy Link Tiếp Thị Shopee (Lưu vào bảng cá nhân)
                         ⬇
BƯỚC 2: Copy Prompt 3 Vòng vào ChatGPT (Kèm Bảng Ký Tự Biểu Cảm)
                         ⬇
BƯỚC 3: Dùng Tool `text_to_audio` xuất file MP3 giọng đọc phòng thu
                         ⬇
BƯỚC 4: Kéo Audio + Ảnh bìa sách vào CapCut/Premiere xuất video triệu view
```

---

## 🛠️ BƯỚC 1: CHỌN SÁCH & LẤY LINK SHOPEE AFFILIATE (KHÔNG CẦN API)

1. Mở trang gian hàng sách Mall uy tín trên Shopee (*Fahasa, Nhã Nam, Kim Đồng, First News, 1980Books*).
2. Chọn cuốn sách muốn làm, copy đường link web sản phẩm (`https://shopee.vn/...`).
3. Truy cập cổng tiếp thị: **`https://affiliate.shopee.vn/offer/custom_link`**.
4. Dán link vừa copy ➡️ Bấm **Tạo link** để nhận link rút gọn tiếp thị vĩnh viễn (`https://s.shopee.vn/...`).
5. Lưu tên sách và link này vào 1 file Excel hoặc Google Sheet để sau khi đăng video thì ghim vào bình luận hoặc gắn vào Bio kênh.

---

## ✍️ BƯỚC 2: BỘ PROMPT CHUẨN GPT VIẾT KỊCH BẢN 10/10 (5 TIÊU CHUẨN VÀNG)

> ⚠️ **NGUYÊN TẮC BẤT DI BẤT DỊCH (APPROVAL GATEKEEPER):**  
> Việc viết kịch bản **hoàn toàn do GPT tự động thực hiện**. Chỉ khi kịch bản được đánh giá **ĐẠT 10/10 OK** theo đủ 5 tiêu chuẩn dưới đây thì mới được phép chuyển sang Bước 3 để get audio về (Read Aloud TTS)!

### 🎯 5 TIÊU CHUẨN ĐỂ KỊCH BẢN ĐẠT 10/10:
1. **Sốc 3s đầu**: Đánh sập ảo tưởng hoặc bắt quả tang hành vi lúc nửa đêm. CẤM chào hỏi, CẤM nêu tên sách ở 3s đầu.
2. **Không có mùi AI (Anti-AI 100%)**: Cấm tuyệt đối văn mẫu sáo rỗng (*'hơn thế nữa', 'tóm lại', 'hãy nhớ rằng', 'kim chỉ nam', 'chúng ta', 'cuộc sống xô bồ'*). Giọng độc thoại trần trụi lúc 2h sáng.
3. **Tư duy ngược (Contrarian Thinking)**: Bẻ gãy lối mòn tư duy thông thường, chỉ ra nghịch lý thực tế cay đắng thay vì khuyên đạo lý.
4. **Liên hệ Gen Z & Vấn đề xã hội nóng**: Gắn chặt áp lực lướt Threads 2h sáng, bão giá nhà tăng lương đứng yên, bẫy nợ BNPL, bẫy 'chữa lành' trốn việc, hội chứng sương mù não do nghiện video ngắn.
5. **Gắn đầy đủ ký tự biểu cảm TTS Prosody**: `...` (ngắt lắng đọng), ` — ` (hạ tông giọng trầm), `IN HOA` (dằn trọng âm), `\n\n` (lấy hơi kịch tính).

---

### 🌟 PROMPT 1-SHOT TOÀN NĂNG (GỬI TRỰC TIẾP CHO GPT XUẤT KỊCH BẢN THU ÂM NGAY)
```text
Bạn là một Đạo diễn Nội dung triệu view và Chuyên gia biên kịch video ngắn hàng đầu trên TikTok/Shorts/Reels.
Hãy viết một kịch bản voice-over độc thoại nội tâm (độ dài 180 - 220 từ, chuẩn 60 - 75 giây) đúc kết từ tinh hoa cuốn sách: '[TÊN CUỐN SÁCH]' của tác giả [TÁC GIẢ].
Chủ đề & huyệt nỗi đau Gen Z cần chạm: [CHỦ ĐỀ / NỖI ĐAU THỰC TẾ].

BẮT BUỘC TUÂN THỦ 5 TIÊU CHUẨN VÀNG ĐỂ ĐẠT ĐIỂM 10/10:

1. HOOK 3S ĐẦU GÂY SỐC CỰC ĐỘ:
   - Đánh sập ngay một ảo tưởng hoặc bắt quả tang hành vi lúc nửa đêm của người nghe.
   - CẤM TIỆT: Không chào hỏi ('Chào các bạn...'), KHÔNG giới thiệu tên sách hay tác giả ở câu đầu tiên.

2. 100% ANTI-AI (KHÔNG CÓ MÙI AI):
   - Tuyệt đối KHÔNG dùng các từ: 'hơn thế nữa', 'tóm lại', 'hãy nhớ rằng', 'kim chỉ nam', 'chúng ta', 'cuộc sống xô bồ', 'hành trình', 'vun đắp'.
   - Văn phong câu ngắn (3-7 từ), sắc lạnh, trần trụi, như lời tự thú của một người từng rơi xuống đáy vực thất bại lúc 2 giờ sáng.

3. TƯ DUY NGƯỢC (CONTRARIAN THINKING):
   - Đưa ra góc nhìn phản trực giác, bẻ gãy suy nghĩ thông thường của số đông.
   - Vạch trần nghịch lý thực tế thay vì khuyên nhủ đạo lý self-help sáo rỗng.

4. LIÊN HỆ THỰC TRẠNG GEN Z VÀ XÃ HỘI NÓNG:
   - Lồng ghép trực tiếp các bối cảnh đời thực: Lướt Threads lúc 2h sáng rồi thấy mình bất tài, bão giá nhà tăng gấp ba lương đứng yên, bẫy nợ tín dụng BNPL, bẫy 'chữa lành' trốn việc, nghiện video ngắn làm sương mù não, overthinking tin nhắn đã xem.

5. TỰ ĐỘNG CHÈN ĐẦY ĐỦ KÝ TỰ ĐIỀU HƯỚNG BIỂU CẢM CHO BỘ ĐỌC CHATGPT READ ALOUD:
   - Dấu ba chấm (...) tại các điểm ngập ngừng, thở dài, nghẹn ngào (để bộ đọc tự ngắt 0.6s).
   - Dấu gạch ngang dài ( — ) để đột ngột hạ tông giọng sang trầm, lạnh, đanh thép.
   - Viết IN HOA ở các từ khóa then chốt để bộ đọc dằn giọng nhấn trọng âm.
   - Xuống dòng đôi (\n\n) giữa các câu/đoạn để bộ đọc dừng lấy hơi kịch tính.

QUAN TRỌNG: Chỉ xuất bản DUY NHẤT nội dung kịch bản hoàn chỉnh để đưa vào bộ đọc thu âm. KHÔNG viết lời chào, lời dẫn hay giải thích nào bên ngoài!
```

---

### 📌 QUY TRÌNH CHUẨN 3 BƯỚC: VIẾT → PHẢN BIỆN TÌM LỖI THẬT → VIẾT LẠI (KIỂM SOÁT 100% CHẤT LƯỢNG)
*(Chi tiết mẫu hoàn chỉnh lưu tại: `templates/prompts/youtube_3step_workflow.md`)*

#### BƯỚC 1 (Prompt 1) — Biên kịch chuyên nghiệp [API 9router: ag/gemini-3.8-flash-high]:
Gửi Prompt 1 với đầy đủ thông tin sách, thời lượng mục tiêu (Shorts 60s hoặc YouTube dài 10-15 phút) qua model `ag/gemini-3.8-flash-high`.
- Bắt buộc: Hook 3s đánh sập sự thật khó chấp nhận, kể chuyện thay vì giảng đạo, cấm tuyệt đối mô típ "Hai giờ sáng", cấm lướt điện thoại ban đêm, cấm câu hỏi tu từ sáo rỗng.

#### BƯỚC 2 (Prompt 2) — Giám đốc biên tập khó tính [API 9router: ag/gemini-3.8-flash-high]:
Gửi bản thảo ở Bước 1 vào Prompt 2 qua model `ag/gemini-3.8-flash-high`.
- Ép model đóng vai giám đốc biên tập, chấm theo 5 tiêu chí (0-10), xác định 3 lỗi nghiêm trọng nhất, chỉ ra đoạn thừa/lặp, và đưa ra kết luận `GO` hoặc `NO-GO`. Tuyệt đối không cho phép model tự khen hay cho điểm ảo.

#### BƯỚC 3 (Prompt 3) — Biên kịch cấp cao [API 9router: ag/claude-sonnet-4-6(max)]:
Gửi kịch bản gốc kèm báo cáo lỗi ở Bước 2 vào Prompt 3 qua model `ag/claude-sonnet-4-6(max)`.
- Tận dụng thế mạnh hành văn sâu sắc, giàu cảm xúc của Claude Sonnet: xử lý triệt để các lỗi bị bắt, tinh chỉnh nhịp kể đọc thành tiếng, tự động chèn các ký tự điều hướng biểu cảm TTS (`...`, ` — `, `IN HOA`, `\n\n`), và chỉ xuất DUY NHẤT lời thoại kịch bản hoàn chỉnh để nạp vào bộ đọc thu âm.

---

## 🎧 BƯỚC 3: XUẤT AUDIO MP3 CHUẨN PHÒNG THU

Sau khi ChatGPT trả về kịch bản Vòng 3, có 2 cách cực nhanh để xuất ra file MP3 giọng đọc ChatGPT:

### Cách A: Gọi trực tiếp qua lệnh Command Line (Nhanh nhất)
Mở PowerShell hoặc CMD và chạy lệnh:
```powershell
python c:\New_audio\tools\chatwithgpt_server.py --audio "[DÁN TOÀN BỘ KỊCH BẢN VÒNG 3 VÀO ĐÂY]" --output-name [TEN_FILE_KHONG_DAU]
```
*Ví dụ:*
```powershell
python c:\New_audio\tools\chatwithgpt_server.py --audio "Điều tàn nhẫn nhất của cuộc đời là... Bạn có thể sống tử tế cả một đời..." --output-name tam_ly_hoc_ve_tien
```
File MP3 sẽ nằm tại: `c:\New_audio\outputs\[TEN_FILE_KHONG_DAU].mp3`

### Cách B: Nhắn tin cho Cline (MCP `text_to_audio`)
Nhắn trực tiếp trong khung chat của Cline:
> *"Xuất file audio cho kịch bản sau với tên file là `ten_sach`: [Dán kịch bản]"*

---

## 💡 GỢI Ý GÓC KHUẤT & HOOK 3S CHO CÁC DÒNG SÁCH BÁN CHẠY NHẤT (GẮN LIỀN THỰC TRẠNG GEN Z)

Khi áp dụng cho các cuốn sách khác, bạn chỉ cần thay [CHỦ ĐỀ/NỖI ĐAU] và [GÓC NHÌN ẨN] theo ma trận thực trạng Gen Z dưới đây:

| Cuốn Sách | Thực Trạng Gen Z Trọng Tâm | Hook 3 Giây Đầu (Chạm Huyệt Nỗi Đau) | Góc Khuất Ít Người Thấy Cần Đào Sâu |
| :--- | :--- | :--- | :--- |
| **Atomic Habits** | Nghiện video ngắn TikTok/Shorts, não mục rỗng (Brain rot), trì hoãn mạn tính. | *"Lý do bạn không bao giờ thay đổi được cuộc đời... không phải vì bạn lười, mà vì não của bạn đã bị nghiện DOPAMINE RẺ TIỀN!"* | Người ta cứ nghĩ cần ý chí thép. Sự thật: Người có kỷ luật cao nhất là người ít dùng ý chí nhất, vì họ thiết kế môi trường để không thể lười biếng. |
| **Tâm Lý Học Về Tiền** | Giá nhà tăng phi mã, bẫy nợ tín dụng, BNPL, sống ảo phông bạt để bằng bạn bè. | *"Bi kịch lớn nhất của người trẻ hiện nay là... Dùng số tiền mình KHÔNG CÓ... để mua thứ mình KHÔNG CẦN... nhằm gây ấn tượng với người mình KHÔNG THÍCH!"* | Sự giàu có thực sự là những món đồ bạn KHÔNG mua. Người ta thích tỏ ra giàu có hơn là thực sự giàu có. |
| **Dám Bị Ghét** | Áp lực đồng trang lứa trên Threads, sợ bị phán xét, sống vì kỳ vọng gia đình. | *"Lý do khiến bạn lướt Threads lúc 2 giờ sáng rồi cảm thấy mình là KẺ BẤT TÀI... không phải vì bạn kém cỏi!"* | Phân chia nhiệm vụ: Người ta ghét bạn là việc của họ, còn sống cuộc đời của bạn là việc của bạn. Đừng bao giờ sống để làm vừa lòng khán giả. |
| **Deep Work** | Phân mảnh tâm trí, hội chứng sương mù não, sợ AI thay thế công việc đầu đời. | *"Nếu bạn không thể ngồi yên làm việc 30 phút mà không chạm vào điện thoại... Bạn sắp bị làn sóng AI và thế giới này ĐÀO THẢI!"* | Làm việc nông (lướt web, check mail) tạo ảo giác bận rộn nhưng giá trị bằng không. Chỉ có Deep Work mới tạo ra năng lực bất khả thay thế. |
| **Can't Hurt Me** | Bẫy "chữa lành" độc hại, hội chứng nằm ườn (bed rotting), trốn tránh thực tại. | *"Hơi áp lực một chút là xin nghỉ việc 'để chữa lành'... Sự thật phũ phàng là: Bạn không hề bị tổn thương... Bạn chỉ đang HÈN NHÁT mà thôi!"* | Cuộc đời không nợ bạn sự êm ấm. Đừng chờ đợi động lực hời hợt; kỷ luật thép và sự trơ lì trước nỗi đau là vũ khí duy nhất để sinh tồn. |
| **Càng Kỷ Luật Càng Tự Do** | Thức đêm cày phim, ngủ ngày, mất phương hướng nghề nghiệp sau khi ra trường. | *"Bạn không hề mệt mỏi vì làm việc quá nhiều... Bạn kiệt sức vì sống một cuộc đời VÔ KỶ LUẬT và vô định!"* | Kỷ luật không phải là sự gò bó, mà là chiếc áo giáp duy nhất giúp bạn không bị biến cố cuộc đời quật ngã. |
| **Đắc Nhân Tâm** | Hàng ngàn bạn bè trên mạng nhưng cô đơn cùng cực, overthinking từng tin nhắn. | *"Nghịch lý lớn nhất của thời đại số là... Chúng ta kết nối với cả thế giới... nhưng lại không có nổi một người để tâm sự lúc 2 giờ sáng!"* | Con người không hành động bằng lý trí mà bằng cảm xúc. Đừng tranh cãi để thắng cái tôi; hãy học cách lắng nghe chân thành để thu phục lòng người. |


---

## 🎬 BƯỚC 4: TỰ ĐỘNG TẠO VIDEO TRIỆU VIEW CINEMATIC 9:16 (1080x1920)

Hệ thống đã nâng cấp toàn diện quy trình tạo video theo chuẩn giữ chân người xem cao nhất (TikTok / Shorts / Reels):

### 1. 4 Nâng cấp mang lại độ thẩm mỹ cao (Cinematic 10/10)
- **Nhịp cắt nhanh (Fast Pacing)**: Cắt ngắn còn 4 – 7 giây mỗi shot (12 shots cho 74s video) thay vì để 1 góc máy tĩnh quá lâu.
- **Bộ lọc màu điện ảnh (Moody Contrast & Dark Vignette)**: Tự động cân chỉnh tương phản, hạ sáng nhẹ và ép viền đen điện ảnh tập trung ánh nhìn vào tâm.
- **Nhạc nền Ambient lót nhẹ (BGM Mixing)**: Hòa âm bản piano/ambient trầm mặc (`assets/bg_music.mp3`) ở mức âm lượng `-22dB` bên dưới giọng đọc, xóa tan cảm giác khô khốc.
- **Phụ đề vàng viền đen (Burned-in Captions)**: Tự động tạo file `.srt` và ép chữ vàng nổi bật (`PrimaryColour=Yellow`, `BorderStyle=3`) ở góc dưới màn hình khớp từng nhịp nói.

### 2. Cơ chế Đồng bộ Phụ đề Frame-Perfect (Khắc phục lỗi lệch sub)
Trong phiên bản mới nhất, hệ thống tách rời hoàn toàn:
1. **Dòng thời gian Hình ảnh (B-Roll Visuals)**: Chuyển cảnh 4 - 7s một lần (12 cuts) để giữ chân người xem.
2. **Dòng thời gian Phụ đề (Subtitle Speech Cues)**: Đồng bộ chính xác theo từng mili-giây của giọng đọc thực tế:
   - Tích hợp sẵn bộ nhận diện **Faster-Whisper (AI VAD & Word/Segment Timestamps)** để tự động quét toàn bộ file audio và trích xuất đúng từng mili-giây giọng đọc dừng/nghỉ/nhấn.
   - Hỗ trợ danh sách `timed_subtitles` tùy biến chuẩn chính tả văn học tiếng Việt 100%.

### 3. Cách chạy 1-Click
- Nhấp đúp vào file `build_video.bat` tại thư mục gốc `c:\New_audio`.
- Thành phẩm sẽ được xuất ngay tại: `outputs/chu_nghia_khac_ky_final.mp4`.

### 4. Tùy biến phân cảnh video cho sách khác
Để tạo video cho bất kỳ cuốn sách nào khác, bạn có thể chạy lệnh CLI:
```powershell
python tools/video_builder.py --audio "outputs/ten_file_audio.mp3" --output "outputs/ten_video_final.mp4"
```
Hệ thống sẽ tự động dùng Faster-Whisper để nhận diện giọng đọc, căn sub chuẩn từng giây mà không bao giờ bị lệch nhịp.


### 5. Tiêu chuẩn Mastering Âm thanh Triệu View (Loudnorm EBU R128 + Anti-Attenuation)
- **Chuẩn hóa giọng đọc Voice-over**: Áp dụng bộ lọc EBU R128 `loudnorm=I=-14:TP=-1.5:LRA=7` để đẩy giọng đọc lên đúng **-14 LUFS** (chuẩn âm thanh to rõ, sắc nét, đanh thép trên TikTok, Shorts, Reels) và giới hạn True Peak ở `-1.5 dB` chống méo tiếng tuyệt đối.
- **Tắt cơ chế tự động chia đôi biên độ của amix**: Bắt buộc thêm `normalize=0:dropout_transition=0` vào bộ lọc `amix` của FFmpeg. Nếu thiếu cờ này, FFmpeg sẽ ngầm chia đôi biên độ (-6 dB), làm giọng đọc bị nhỏ đi một nửa.
- **Hòa âm BGM lót nhẹ**: Nhạc nền ambient được tinh chỉnh ở mức `volume=0.05` (-26 dB) để lót êm ái phía sau, tôn trọn vẹn giọng đọc lên vị trí chủ đạo.
- **Lệnh FFmpeg chuẩn áp dụng toàn bộ hệ thống**:
```bash
-filter_complex "[0:v]{sub_style}[vout];[1:a]loudnorm=I=-14:TP=-1.5:LRA=7[voice];[2:a]volume=0.05[bgm];[voice][bgm]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]"
```


# Skill: Book Summary Video Generator (Chuẩn Triệu View 10/10)
# Description: Quy trình tự động hóa end-to-end sản xuất video dọc 9:16 tóm tắt sách / triết lý sống đạt chuẩn giữ chân khán giả cao (High-Retention), kết hợp ChatGPT Read Aloud TTS, Pexels B-Roll điện ảnh, nhạc nền BGM và phụ đề đồng bộ chính xác từng mili-giây.

---

## 🎯 2 NGUYÊN TẮC BẮT BUỘC SỐNG CÒN CỦA VIDEO TRIỆU VIEW

### ⚡ NGUYÊN TẮC 1: 3 GIÂY ĐẦU TIÊN BẮT BUỘC PHẢI GÂY SỐC CỰC ĐỘ (SHOCKING HOOK / PATTERN INTERRUPT)
> ⚠️ **LUẬT SỐNG CÒN VỀ GIỮ CHÂN KHÁN GIẢ (RETENTION):**
> 1. Người xem TikTok, Shorts, Reels quyết định lướt hay ở lại trong **1 đến 2 giây đầu tiên**. Mở đầu **BẮT BUỘC PHẢI GÂY SỐC**, đập tan một ảo tưởng, tát nước lạnh vào mặt, hoặc bắt quả tang hành vi đau xót lúc 2h sáng.
> 2. **CẤM TUYỆT ĐỐI**:
>    - CẤM chào hỏi rườm rà: *"Xin chào các bạn...", "Hôm nay mình sẽ chia sẻ..."*.
>    - CẤM nêu tên sách / tác giả ở 3s đầu: *"Hôm nay mình review cuốn sách Dám Bị Ghét..."* ➡️ Khán giả lướt đi ngay lập tức!
>    - CẤM nói đạo lý ru ngủ sáo rỗng: *"Cuộc sống này ai cũng có khó khăn...", "Chúng ta cần phải cố gắng..."*.
> 3. **4 CÔNG THỨC HOOK 3S GÂY SỐC KINH ĐIỂN**:
>    - **Dạng 1 (Tát nước lạnh vào ảo tưởng)**: *"Điều tàn nhẫn nhất của cuộc đời là... Bạn có thể sống tử tế cả đời, rồi vẫn bị phản bội... như một kẻ ngốc!"*
>    - **Dạng 2 (Bắt quả tang tội lỗi lúc 2h sáng)**: *"Lý do bạn lướt Threads lúc 2 giờ sáng rồi cảm thấy mình là KẺ BẤT TÀI... không phải vì bạn kém cỏi!"*
>    - **Dạng 3 (Nghịch lý phũ phàng thực tế)**: *"Bi kịch lớn nhất của người trẻ là... Giá nhà tăng gấp ba, nhưng lương thì vẫn đứng yên một chỗ!"*
>    - **Dạng 4 (Dằn mặt hội chứng trốn tránh)**: *"Hơi áp lực một chút là xin nghỉ việc 'để chữa lành'... Sự thật là: Bạn không tổn thương... Bạn chỉ đang HÈN NHÁT!"*

---

### 🕒 NGUYÊN TẮC 2: TUYỆT ĐỐI KHÔNG ĐỂ LỆCH SUBTITLE (TIMELINE SEPARATION POLICY)
> ⚠️ **LUẬT CỐT LÕI VỀ TIMELINE:**
> 1. **KHÔNG BAO GIỜ gán thời lượng phụ đề theo thời lượng cảnh B-roll video.** (Video có thể 5s, nhưng câu nói chỉ kéo dài 2.5s rồi dừng nghỉ lấy hơi 1.5s).
> 2. **Dòng thời gian Phụ đề (Subtitle Timeline) PHẢI bám theo luồng âm thanh thực tế** thông qua bộ nhận diện **Faster-Whisper** hoặc danh sách mốc thời gian mili-giây chính xác (`timed_subtitles`).
> 3. **Dòng thời gian Hình ảnh (Visual B-Roll Timeline)**: Độc lập hoàn toàn, cắt chuyển cảnh nhanh 4 - 7s một lần (10 - 12 cảnh) để duy trì nhịp độ kích thích thị giác.

---

## 🛠️ CÁC BƯỚC THỰC HIỆN TOÀN BỘ PIPELINE

### BƯỚC 1: GPT Tự Động Soạn Thảo & Kiểm Định Kịch Bản Đạt Chuẩn 10/10
> ⚠️ **LUẬT GATEKEEPER 10/10 & PHÂN BỔ MODEL 9ROUTER:** 
> - **Vòng 1 (Bản thảo) & Vòng 2 (Phản biện gắt gao)**: Dùng **API 9router: `ag/gemini-3.8-flash-high`** để quét lỗi, bóc tách sáo rỗng và phản biện không nương tay.
> - **Vòng 3 (Tái sinh kịch bản thu âm 10/10)**: Dùng **API 9router: `ag/claude-sonnet-4-6(max)`** để viết lại bản hoàn thiện với văn phong sâu sắc, giàu cảm xúc và gài đầy đủ ký tự TTS Prosody.
> - Kịch bản phải vượt qua kiểm định **10/10 TUYỆT ĐỐI** trước khi được phép đưa sang bước lấy giọng đọc TTS!

**5 Tiêu Chuẩn Bắt Buộc Đạt 10/10:**
1. **Hook 3s đầu gây sốc cực độ**: Đánh sập ảo tưởng hoặc bắt quả tang hành vi đau xót lúc nửa đêm. CẤM chào hỏi, CẤM nêu tên sách ở câu đầu.
2. **Không có mùi AI (Anti-AI 100%)**: Cấm từ ngữ sáo rỗng (*'hơn thế nữa', 'tóm lại', 'hãy nhớ rằng', 'kim chỉ nam', 'chúng ta', 'cuộc sống xô bồ'*). Giọng độc thoại trần trụi lúc 2h sáng.
3. **Tư duy ngược (Contrarian Thinking)**: Bẻ gãy suy nghĩ thông thường của số đông, chỉ ra nghịch lý thực tế cay đắng.
4. **Huyệt nỗi đau Gen Z & Vấn đề xã hội nóng**: Threads 2h sáng, bão giá nhà tăng gấp ba lương đứng yên, bẫy nợ BNPL, bẫy 'chữa lành' trốn việc, não mục sương mù vì video ngắn.
5. **Gắn đầy đủ ký tự biểu cảm TTS Prosody**:
   - `...` (Ba chấm): AI hạ tông giọng, thở hắt ra, ngắt nhịp lắng đọng 0.5s - 0.8s.
   - ` — ` (Gạch ngang dài): Đột ngột ngắt nhịp, chuyển sang giọng trầm, đanh thép.
   - `\n\n` (2 lần xuống dòng): Ép AI dừng lại lấy hơi trước khi vào đoạn mới.
   - `IN HOA`: Nhấn mạnh trọng âm cực mạnh vào từ khóa then chốt.

Mọi kịch bản sách phải tuân theo cấu trúc 5 giai đoạn:
1. **Hook (0 - 5s)**: Đánh gục niềm tin sai lầm cũ bằng thực trạng trần trụi (*"Điều tàn nhẫn nhất của cuộc đời là..."*).
2. **Pain / Tension (5 - 25s)**: Đào sâu vào nỗi đau nội tâm, sự bế tắc thực tế của người nghe (Gen Z / người trẻ).
3. **Turn / Insight (25 - 45s)**: Tư duy ngược + bài học triết lý cốt lõi từ cuốn sách.
4. **Actionable / Reality (45 - 60s)**: Hành động cụ thể, góc nhìn gai góc thực tế, không lý thuyết suông.
5. **Climax / Power Hook (60 - 75s)**: Đỉnh cao cảm xúc, khẳng định bản lĩnh cá nhân.

---

## 🧠 BỘ CATALOG THỰC TRẠNG GEN Z (VIỆT NAM & THẾ GIỚI) - BẢO BỐI TẠO HOOK & NỖI ĐAU TRIỆU VIEW

Để video sách đạt tỷ lệ giữ chân (Retention) cao nhất trên TikTok, Shorts, Reels, **tuyệt đối không nói đạo lý chung chung**. Hãy gắn thông điệp của cuốn sách vào **7 thực trạng nhức nhối nhất mà Gen Z (Việt Nam & Thế giới) đang trực tiếp đối mặt hàng ngày**:

### 1. ÁP LỰC ĐỒNG TRANG LỨA TRÊN THREADS / TIKTOK & VĂN HÓA "PHÔNG BẠT" (Peer Pressure & Flexing)
* **Bối cảnh Quốc tế:** Hội chứng FOMO, Imposter Syndrome (kẻ giả mạo). Mạng xã hội biến cuộc sống thành cuộc đua ảo; người trẻ so sánh hậu trường đầy bất an của mình với highlight hào nhoáng của người khác.
* **Đặc thù Việt Nam:** "Đại dịch Threads": 20 tuổi khoe mua nhà, mở startup doanh thu bạc tỷ, du học toàn phần. Văn hóa "phông bạt" vay nợ mua iPhone mới nhất, check-in cafe sang chảnh để không thua kém bạn bè. Đêm về trùm chăn tự dằn vặt: *"Tại sao ai cũng giỏi giang, chỉ có mình là kẻ bất tài, vô dụng?"*.
* **Từ khóa Gen Z:** *Flexing, Overthinking, Peer pressure, Thao túng tâm lý, Bị bỏ lại phía sau, Lướt Threads 2 giờ sáng*.
* **Cuốn sách áp dụng:** **Dám Bị Ghét** (Adler), **Tâm Lý Học Về Tiền** (Morgan Housel), **Chủ Nghĩa Khắc Kỷ**.

### 2. BÃO GIÁ BẤT ĐỘNG SẢN & TUYỆT VỌNG TÀI CHÍNH (Housing Crisis & Financial Trap)
* **Bối cảnh Quốc tế:** "Generation Rent" (thế hệ ở thuê trọn đời) tại Mỹ, Úc, Hàn Quốc. Giấc mơ mua nhà trước tuổi 35 tan biến. Lối thoát ảo: sa đà vào meme coin, crypto, trading đòn bẩy cao, cờ bạc trực tuyến với hy vọng đổi đời trong 1 đêm.
* **Đặc thù Việt Nam:** Chung cư Hà Nội, TP.HCM tăng vọt 60-100 triệu/m2. Lương cử nhân mới ra trường 7-10 triệu VNĐ, làm 50 năm không ăn tiêu cũng không mua nổi nhà. Bẫy nợ "Mua trước trả sau" (BNPL), thẻ tín dụng khiến chưa hết tháng đã cạn tiền.
* **Từ khóa Gen Z:** *Giá nhà trên trời, Lương ba cọc ba đồng, Đu đỉnh crypto, Trả nợ thẻ tín dụng, Vỡ mộng mua nhà, BNPL, Sống mòn*.
* **Cuốn sách áp dụng:** **Tâm Lý Học Về Tiền**, **Atomic Habits**, **Người Giàu Có Nhất Thành Babylon**.

### 3. THẤT NGHIỆP BẰNG CỬ NHÂN, LÀN SÓNG SA THẢI AI & KIỆT SỨC SỚM (AI Layoffs & Early Burnout)
* **Bối cảnh Quốc tế:** Big Tech sa thải hàng loạt; AI thay thế vị trí Entry-level / Junior. Bằng đại học mất giá. Hiện tượng "Quiet Quitting" (nghỉ việc trong im lặng), "Quarter-life Crisis" (khủng hoảng tuổi 25).
* **Đặc thù Việt Nam:** Cầm tấm bằng Giỏi đại học đi xin việc bị ép lương 5-6 triệu; tuyển dụng đòi hỏi "2-3 năm kinh nghiệm cho sinh viên mới ra trường". Nhiều cử nhân giấu bằng ĐH đi làm shipper, phục vụ quán nước. Áp lực vừa đi làm vừa sợ AI xóa sổ công việc.
* **Từ khóa Gen Z:** *Thất nghiệp bằng đỏ, Sa thải AI, Burnout tuổi 22, Bị bóc lột OT, Quiet Quitting, Mất định hướng nghề nghiệp*.
* **Cuốn sách áp dụng:** **Can't Hurt Me** (David Goggins), **Deep Work** (Cal Newport), **Càng Kỷ Luật Càng Tự Do**.

---

### 4. NGHIỆN DOPAMINE RẺ TIỀN, MẤT TẬP TRUNG SÂU & "DOOMSCROLLING" (Digital Addiction & Brain Fog)
* **Bối cảnh Quốc tế:** Não bộ bị phân mảnh bởi video ngắn (TikTok, Reels, Shorts). Hiện tượng "Doomscrolling" (lướt tin tiêu cực liên tục trong vô thức), hội chứng sương mù não (Brain Fog), giảm khả năng chú ý xuống dưới 8 giây.
* **Đặc thù Việt Nam:** Thức đến 3-4 giờ sáng lướt mạng xã hội; sáng dậy uể oải, mất hết sinh khí, không thể đọc nổi một cuốn sách quá 10 trang, không thể ngồi làm việc liên tục 30 phút mà không cầm điện thoại lên. Cảm giác tội lỗi dằn vặt vì một ngày trôi qua vô nghĩa.
* **Từ khóa Gen Z:** *Doomscrolling, Zombie lướt điện thoại, Nghiện dopamine, Trì hoãn mạn tính, Mất tập trung, Brain fog, Ngủ ngày cày đêm*.
* **Cuốn sách áp dụng:** **Deep Work**, **Atomic Habits**, **Chủ Nghĩa Khắc Kỷ**.

### 5. BẪY "CHỮA LÀNH" ĐỘC HẠI & NẰM ƯỜN TRỐN CHẠY (Toxic Healing & "Bed Rotting")
* **Bối cảnh Quốc tế:** Xu hướng "Bed Rotting" (nằm ườn trên giường hàng ngày không rời đi), dán nhãn mọi khó khăn thành "chấn thương tâm lý" (Trauma) để trốn tránh nỗ lực.
* **Đặc thù Việt Nam:** "Đại dịch chữa lành": Đi làm vài tháng thấy áp lực là xin nghỉ việc "đi Đà Lạt chữa lành", "đi phượt chữa lành". Chi hàng chục triệu cho các khóa học tâm linh / tarot vô bổ trong khi bản chất là sự lười biếng và hèn nhát không dám đối diện với kỷ luật lao động khắc nghiệt.
* **Từ khóa Gen Z:** *Chữa lành, Đứa trẻ bên trong, Nằm ườn (Bed rotting), Trốn tránh thực tại, Tâm linh độc hại, Yêu bản thân sai cách*.
* **Cuốn sách áp dụng:** **Can't Hurt Me**, **Đi Tìm Lẽ Sống** (Viktor Frankl), **Chủ Nghĩa Khắc Kỷ**.

### 6. CÔ ĐƠN KẾT NỐI, SỢ GIAO TIẾP XÃ HỘI & OVERTHINKING (Hyper-connected Loneliness)
* **Bối cảnh Quốc tế:** WHO xem "Sự cô đơn" là đại dịch toàn cầu mới. Thế hệ siêu kết nối trên Internet nhưng cô độc nhất trong lịch sử. Nỗi sợ gọi điện thoại (Phone call anxiety), hội chứng lo âu xã hội (Social anxiety).
* **Đặc thù Việt Nam:** Hàng ngàn bạn bè trên Facebook/Instagram, Story lúc nào cũng sôi động, nhưng lúc gặp biến cố gia đình hay thất tình lúc nửa đêm... lướt danh bạ không tìm nổi một người có thể gọi điện để khóc. Các mối quan hệ hời hợt, dễ đến dễ đi.
* **Từ khóa Gen Z:** *Cô đơn giữa đám đông, Sợ nghe điện thoại, Overthinking từng tin nhắn, Quan hệ hời hợt, Mối quan hệ mập mờ, Rối loạn âu lo*.
* **Cuốn sách áp dụng:** **Đắc Nhân Tâm**, **Dám Bị Ghét**, **Hiểu Về Trái Tim**.

### 7. XUNG ĐỘT THẾ HỆ & GÁNH NẶNG KỲ VỌNG Á ĐÔNG (Generational Clash & Family Burden)
* **Bối cảnh Quốc tế:** Tranh cãi giữa Gen Z và thế hệ Boomer/Gen X về quan điểm sống: sống để tận hưởng hay sống để cống hiến cho công ty.
* **Đặc thù Việt Nam:** Áp lực "con nhà người ta", cha mẹ định kiến phải vào biên chế nhà nước, phải lấy chồng/vợ sinh con trước 27 tuổi. Cảm giác nghẹt thở vì sống hộ kỳ vọng chưa thành của bố mẹ; cảm giác tội lỗi (Guilt) mỗi khi muốn bứt phá làm theo đam mê của riêng mình.
* **Từ khóa Gen Z:** *Con nhà người ta, Ép cưới, Áp lực gia đình, Chữ hiếu nặng nề, Định kiến thế hệ, Mất tiếng nói trong nhà*.
* **Cuốn sách áp dụng:** **Dám Bị Ghét**, **Chủ Nghĩa Khắc Kỷ**, **Tư Duy Nhanh Và Chậm**.

---

## 🎯 CÔNG THỨC RÁP THỰC TRẠNG GEN Z VÀO KỊCH BẢN TRIỆU VIEW

| Bước | Thành Phần | Cách Triển Khai Cho Gen Z | Ví Dụ Minh Họa (Sách Dám Bị Ghét) |
| :--- | :--- | :--- | :--- |
| **1** | **Hook 3s** | Bẻ gãy ảo tưởng hoặc chạm ngay vào cảm giác tội lỗi/lo âu lúc nửa đêm | *"Lý do khiến bạn lướt Threads lúc 2 giờ sáng rồi cảm thấy mình là KẺ BẤT TÀI... không phải vì bạn kém cỏi!"* |
| **2** | **Pain (15-20s)**| Đào sâu cảm giác kiệt sức, so sánh ngấm ngầm, bế tắc tài chính hoặc cô đơn | *"Bạn thấy người ta 20 tuổi mua nhà, làm Founder... Còn bạn vẫn chật vật với đồng lương ít ỏi, vừa sợ bị sa thải, vừa sợ ánh mắt bố mẹ thất vọng..."* |
| **3** | **Turn (Insight)**| Dẫn bài học sách như chiếc chìa khóa giải thoát triệt để | *"Dám Bị Ghét dạy một sự thật giải thoát đến nghẹt thở: Bạn không sinh ra để làm vừa lòng khán giả! Cuộc đời họ là việc của họ, cuộc đời bạn là việc của bạn!"* |
| **4** | **Actionable** | Hành động thực tế: buông bỏ so sánh, kỷ luật cụ thể | *"Tắt điện thoại. Ngừng theo dõi những hào nhoáng phông bạt. Học cách DÁM BỊ GHÉT để bắt đầu sống thật."* |
| **5** | **Climax** | Tuyên ngôn bản lĩnh cá nhân, chốt hạ đầy sức nặng | *"Đừng để người khác viết kịch bản cho cuộc đời bạn... Hãy can đảm bước đi một mình!"* |

---

### BƯỚC 2: Thu Âm Tự Động Với ChatGPT Read Aloud (Chỉ Khi Kịch Bản Đã Đạt 10/10)
> ⚠️ **ĐIỀU KIỆN TIÊN QUYẾT:** Tuyệt đối KHÔNG được get audio nếu kịch bản chưa pass đủ 5 tiêu chuẩn 10/10 (Hook 3s sốc, Anti-AI, Tư duy ngược, Nỗi đau Gen Z, Ký tự biểu cảm TTS).

1. Đảm bảo Chrome mở port 9222 qua:
   ```cmd
   launch_chrome_chatgpt.bat
   ```
2. Sinh âm thanh chất lượng Studio 24000Hz thông qua MCP tool hoặc CLI:
   ```powershell
   python tools/chatwithgpt_server.py --audio "<NOI_DUNG_KICH_BAN_10_10>" <ten_file_output>
   ```
   Kết quả xuất ra: `outputs/<ten_file_output>.mp3`.

---

### BƯỚC 3: Tạo Phụ Đề Chuẩn Khớp Âm Tiết Bằng Faster-Whisper
Hệ thống tự động sử dụng `faster-whisper` để quét file MP3 vừa tạo:
```python
# Gọi hàm tự động trong tools/video_builder.py
transcribe_audio_to_srt(audio_path, srt_path)
```
Hoặc cấu hình danh sách `timed_subtitles` tùy biến trong code:
```python
timed_subtitles = [
    (0.00, 1.44, "Điều tàn nhẫn nhất\ncủa cuộc đời là..."),
    (1.50, 4.66, "Bạn có thể sống tử tế cả một đời,\nrồi vẫn bị phản bội..."),
    ...
]
```

**Quy chuẩn style phụ đề (ASS / SRT Filter - Xem thêm skills/viral-short-video-standard.md):**
```ini
FontName=Segoe UI Black,FontSize=20,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2.8,Shadow=1.5,Alignment=2,MarginV=90
```
- Chữ vàng rực nổi bật trên nền tối (`PrimaryColour=&H0000FFFF`).
- Viền đen nét đậm `Outline=2.8` và đổ bóng mờ `Shadow=1.5` chuẩn Netflix/Shorts (`BorderStyle=1`), không che mặt.
- Căn lề dưới `MarginV=90` (tránh bị che bởi nút like/share của TikTok, Reels, Shorts).

---

### BƯỚC 4: Tải Stock Video Pexels Dọc 9:16, Slow Zoom & Ép Hệ Màu Rec.709
1. Lấy Pexels API Key từ `C:\Long_YT\.env` hoặc file cấu hình hệ thống.
2. Tìm kiếm B-roll tối màu, điện ảnh, trừu tượng (mưa, bóng người đêm, tượng điêu khắc đá, đồng hồ cát, sóng biển). Chia nhịp cắt 3 giây (~15–16 cảnh/video 60s).
3. **Filter bắt buộc**: Ưu tiên video dọc độ phân giải $\le 1080 \times 1920$ (tránh tải nhầm file 4K nặng lag).
4. Áp dụng Slow Zoom (Ken Burns 1.07x) & Color Grade & Ép hệ màu Rec.709:
   ```bash
   -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,zoompan=z='min(zoom+0.0010,1.07)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,eq=contrast=1.15:brightness=-0.03:saturation=0.85,vignette=PI/4" \
   -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709
   ```

---

### BƯỚC 5: Mix Audio Đa Tầng & Render Video 1 Pass (FFmpeg)
Ghép toàn bộ video B-roll đã nối (`combined_visuals.mp4`), audio đọc ChatGPT, nhạc nền ambient BGM (`assets/bg_music.mp3`) và phụ đề vào 1 lệnh duy nhất:

```bash
ffmpeg -y -i combined_visuals.mp4 -i speech.mp3 -stream_loop -1 -i bg_music.mp3 \
  -filter_complex "[0:v]subtitles=subtitles.srt:force_style='FontName=Segoe UI Black,FontSize=20,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2.8,Shadow=1.5,Alignment=2,MarginV=90'[vout];[1:a]loudnorm=I=-14:TP=-1.5:LRA=7,aformat=sample_rates=44100:channel_layouts=stereo[voice];[2:a]volume=0.18,aformat=sample_rates=44100:channel_layouts=stereo[bgm];[voice][bgm]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]" \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset fast -crf 20 \
  -c:a aac -b:a 192k -shortest output_final.mp4
```

*Giọng đọc voice-over luôn được chuẩn hóa EBU R128 (-14 LUFS) để vang, to rõ theo chuẩn TikTok/Shorts/Reels, và tắt tính năng tự chia đôi âm lượng của `amix` (`normalize=0`). Nhạc nền BGM được hòa âm lót nhẹ bên dưới (`volume=0.18` ~ -22dB) để triệt tiêu hoàn toàn dead air.*

---

## ⚡ LỆNH THỰC THI NHANH CHO CLINE
Khi người dùng yêu cầu: *"Tạo video sách về [Chủ đề/Tên sách]"*:
1. Chọn 1 nỗi đau thực trạng Gen Z (Việt Nam & Thế giới) từ bộ Catalog tương ứng với cuốn sách, soạn kịch bản theo framework 10/10 với đầy đủ tag biểu cảm.
2. Gọi `tools/chatwithgpt_server.py --audio ...` để sinh file voice MP3.
3. Chạy `tools/video_builder.py` để tự động tải B-roll, trích xuất phụ đề bằng Faster-Whisper, mix BGM và xuất video hoàn chỉnh.
4. Trích xuất test frame và kiểm tra trực quan chất lượng trước khi bàn giao cho người dùng.

---

## 🚀 SẢN XUẤT HÀNG LOẠT (BATCH PRODUCTION)
Khi sản xuất hàng loạt nhiều cuốn sách:
1. Thêm cấu hình danh sách sách vào `configs/books_10.json` (chứa `slug`, `title`, `script`, `scenes`).
2. Chạy pipeline batch 1-click:
   ```cmd
   build_10_books.bat
   ```
   hoặc chạy theo số thứ tự:
   ```cmd
   python tools/batch_book_generator.py 1
   ```
3. Pipeline tự động cách ly cache từng cuốn trong `cache/books/{slug}/`, tự động nhận diện giọng đọc, map chính xác từng mili-giây phụ đề không lệch 1 khung hình, render ra `outputs/{slug}_final.mp4`.


# Quy Chuẩn Biên Soạn Bài Viết & Tạo Ảnh Trích Dẫn 10/10 (Photo Post Generation)

Tài liệu này chuẩn hóa quy trình sản xuất **Ảnh Quote 4:5 (Visual Punchline)** kết hợp **Bài viết chuyên sâu (Article Caption)** cho Fanpage Facebook, Instagram và Threads của kênh **Radio 2AM**.

---

## 1. NGUYÊN TẮC CỐT LÕI: QUY TRÌNH 3 BƯỚC (CHỐNG AI TỰ KHEN)
Tuyệt đối không gộp chung vào 1 prompt duy nhất. Phải tách rời 3 vai trò và phân bổ model chuyên biệt qua 9Router:

1. **Bước 1 (Draft) [`ag/gemini-3.8-flash-high`]**:
   - Khởi tạo đồng thời:
     * **Câu Quote trên ảnh (15 - 25 từ)**: Đanh thép, đập thẳng vào nhận thức sai lầm cũ, bẻ lái tư duy.
     * **Bài viết chi tiết (250 - 400 từ)**: Cấu trúc 4 tầng, đào sâu tình huống thực tế đời thường, giải pháp triết học/tâm lý học từ sách.
2. **Bước 2 (Critique) [`ag/gemini-3.8-flash-high`]**:
   - Đóng vai "Tổng Biên Tập & Chuyên gia Giữ chân Độc giả", thẩm định độc lập theo 5 tiêu chí (thang điểm 0 - 10).
   - Vạch trần 3 lỗi nghiêm trọng nhất: văn mẫu AI, đạo lý suông, câu chữ sáo rỗng, thiếu kết nối giữa ảnh và bài viết. Kết luận rõ ràng: **GO** (Đạt) hoặc **REWRITE** (Viết lại).
3. **Bước 3 (Rewrite) [`ag/claude-sonnet-4-6(max)` hoặc fallback `ag/claude-sonnet-5-5-high`]**:
   - Biên kịch cấp cao viết lại toàn diện, mài giũa từng câu chữ, nâng tầm thẩm mỹ của câu Quote trên ảnh và thổi chất giọng trầm ấm, sắc lạnh, sâu sắc của 2AM vào bài viết.

---

## 2. 5 TIÊU CHUẨN VÀNG ĐẠT ĐIỂM 10/10

### 1. Visual Hook Dừng Ngón Tay (Stop-The-Scroll Quote)
- Câu chữ trên ảnh tối đa **15 - 25 từ**.
- Phải là một **Cú đấm thị giác (Visual punchline)**: Phản trực giác, bộc lộ nghịch lý hoặc vạch trần một ảo tưởng mà người đọc đang gồng gánh.
- Người lướt bảng tin chỉ mất 1 giây để đọc hết câu trên ảnh và buộc phải dừng lại bấm vào bài viết để đọc tiếp.

### 2. 100% Anti-AI (Diệt Sạch Mùi Văn Mẫu)
- **CẤM TUYỆT ĐỐI** các liên từ và sáo ngữ: *"hơn thế nữa"*, *"tóm lại"*, *"hãy nhớ rằng"*, *"kim chỉ nam"*, *"chúng ta thường"*, *"cuộc sống xô bồ"*, *"hành trình hoàn thiện bản thân"*, *"ánh sáng hy vọng"*, *"vun đắp tương lai"*.
- Không viết giọng rao giảng đạo đức, không dùng đại từ nhân xưng chung chung giả tạo. Giọng văn phải như một người đi trước từng trải, thấu hiểu, nói thẳng sự thật nhưng giàu tính nhân văn.

### 3. Cấu Trúc Bài Viết 4 Tầng Chuẩn Mobile UI
Bài viết độ dài **250 - 400 từ**, chia thành các đoạn ngắn (2 - 3 câu mỗi đoạn), xuống dòng đôi (`\n\n`) để không gây ngợp mắt:
- **Tầng 1 (3 dòng đầu - Text Hook)**: Đập ngay vào nghịch lý hoặc tình huống va chạm thực tế (phần hiển thị trước nút *"Xem thêm / See more"*).
- **Tầng 2 (Bóc trần thực tế)**: Đào sâu vào nỗi đau, sự kiệt sức, áp lực ngầm mà độc giả đang âm thầm chịu đựng.
- **Tầng 3 (Giải mã từ cuốn sách)**: Trình bày góc nhìn cốt lõi của tác giả (tâm lý học Adler, khắc kỷ Seneca, thói quen nguyên tử James Clear...) để giải quyết tận gốc vấn đề.
- **Tầng 4 (Hành động & CTA)**: Bài học hành động cụ thể + Thông tin tác phẩm & Link mua sách chính hãng Shopee Affiliate + Bộ hashtag chuẩn.

### 4. Đánh Đúng Huyệt Nỗi Đau Đời Thực (Real Life Pain Points)
Tập trung vào 3 cụm chủ đề lớn đồng bộ với chuỗi tác phẩm của 2AM:
- **Tâm lý & Bản lĩnh sống** *(Dám Bị Ghét, Xã Hội Mệt Mỏi, Nghệ Thuật Sống - Seneca, Đi Tìm Lẽ Sống)*: Hội chứng sợ bị ghét (People-pleaser), ôm đồm cảm xúc của sếp/gia đình, bẫy đổ lỗi quá khứ, khủng hoảng hiện sinh.
- **Tư duy tài chính** *(Tâm Lý Học Về Tiền, Tư Duy Nhanh Và Chậm, Cha Giàu Cha Nghèo)*: Mua đồ xa xỉ để chứng minh bản thân, bẫy nợ tín dụng, nhầm lẫn giữa "Giàu bề nổi (Rich)" và "Thịnh vượng đích thực (Wealth)".
- **Kỷ luật & Hiệu suất** *(Atomic Habits, Kỷ Luật Là Tự Do, Deep Work, Can't Hurt Me)*: Ảo tưởng động lực, dopamine rẻ tiền từ mạng xã hội, trì hoãn kinh niên, bẫy bận rộn ảo.

### 5. Tính Nhất Quán & Chuyển Đổi Tự Nhiên
- Câu Quote trên ảnh và bài viết Caption phải là một thể thống nhất hữu cơ.
- Lời kêu gọi hành động (CTA) gắn link Shopee Affiliate xuất hiện tự nhiên như một lời gợi ý đọc nguồn gốc sách chính hãng, không chèo kéo bán hàng thô thiển.


---

## 3. BỘ PROMPT CHUẨN GỬI 9ROUTER

### Vòng 1: Tạo Bản Thảo (Draft) [Model: `ag/gemini-3.8-flash-high`]
```text
Bạn là một Cố vấn Nội dung và Chuyên gia Copywriting hàng đầu trên mạng xã hội (Facebook/Instagram/Threads).
Hãy biên soạn 1 bộ nội dung gồm [CÂU QUOTE TRÊN ẢNH] và [BÀI VIẾT CHI TIẾT] đúc kết từ tinh hoa cuốn sách: '[TÊN SÁCH]' của tác giả [TÁC GIẢ].
Chủ đề & Huyệt nỗi đau đời thực: [CHỦ ĐỀ / VẤN ĐỀ THỰC TẾ].

YÊU CẦU BẮT BUỘC ĐỂ ĐẠT ĐIỂM 10/10:
1. CÂU QUOTE TRÊN ẢNH (15 - 25 từ): Đanh thép, đập sập ảo tưởng, tư duy ngược, gây tò mò cực độ để người lướt dừng lại đọc bài.
2. BADGE TAG: 1 thẻ phân loại ngắn 2 - 4 từ (Ví dụ: BẢN LĨNH SỐNG, TỰ DO TÀI CHÍNH, KỶ LUẬT THÉP).
3. BÀI VIẾT CHI TIẾT (250 - 400 từ):
   - 3 dòng đầu: Mở đầu gây sốc / nghịch lý hiển thị trước nút 'Xem thêm'.
   - Thân bài: Khai thác tình huống thực tế, bóc tách tâm lý, áp dụng triết lý từ sách để đưa ra góc nhìn giải thoát.
   - Kết bài: Thông điệp thức tỉnh sâu sắc, ngắn gọn.
   - 100% ANTI-AI: CẤM 'hơn thế nữa', 'tóm lại', 'hãy nhớ rằng', 'kim chỉ nam', 'chúng ta', 'cuộc sống xô bồ', 'hành trình'.
   - Format: Các đoạn ngắn 2-3 câu, xuống dòng đôi.

Định dạng xuất chuẩn Markdown / JSON rõ ràng.
```

### Vòng 2: Phản Biện & Bắt Lỗi (Critique) [Model: `ag/gemini-3.8-flash-high`]
```text
Bạn là Giám đốc Biên tập khó tính và Chuyên gia Giữ chân Độc giả kỳ cựu trên mạng xã hội.
Hãy mổ xẻ và chấm điểm khắt khe bản thảo Photo Post sau đây:
[DÁN BẢN THẢO VÒNG 1 VÀO ĐÂY]

BẢNG ĐIỂM 5 TIÊU CHÍ (Thang điểm 0 - 10):
1. Visual Hook trên Ảnh (Độ giật mình, tính dừng ngón tay): ?/10
2. Bộ lọc Anti-AI (Có bị mùi sách dịch, văn mẫu hô hào không): ?/10
3. Chiều sâu Tư duy ngược & Tính sắc bén: ?/10
4. Độ chạm Nỗi đau thực tế độc giả: ?/10
5. Sự liền mạch hữu cơ giữa Ảnh và Bài viết: ?/10

YÊU CẦU:
- Vạch trần ít nhất 3 điểm yếu chí mạng (câu nào sáo rỗng, ý nào bị nhai lại, đoạn nào lê thê).
- Đưa ra hướng chỉnh sửa cụ thể.
- Kết luận: GO (đạt trên 45/50) hoặc REWRITE.
```

### Vòng 3: Tái Sinh Hoàn Chỉnh (Rewrite) [Model: `ag/claude-sonnet-4-6(max)`]
```text
Bạn là Cây bút Chủ lực và Giọng văn Linh hồn của kênh Radio 2AM.
Dựa trên bản thảo Vòng 1 và bản mổ xẻ khắt khe của Vòng 2, hãy viết lại TOÀN DIỆN bộ nội dung Photo Post đạt điểm tuyệt đối 10/10.

YÊU CẦU BẮT BUỘC:
- Khắc phục 100% các lỗi mà Vòng 2 đã chỉ ra.
- Câu Quote trên ảnh phải cô đọng, sắc như dao cạo, chạm thẳng vào tâm can.
- Bài viết phải mang chất giọng mộc mạc, từng trải, nói thẳng nhưng nhân văn, chia đoạn thoáng mắt cho người đọc di động.
- Cuối bài gắn kèm dòng trích dẫn sách, tác giả, link mua Shopee và hashtag chuẩn 2AM:
  📖 Tác phẩm: [TÊN SÁCH] - [TÁC GIẢ]
  🛒 Mua sách chính hãng tại: [LINK SHOPEE AFFILIATE]
  #radio2am #[slug_sach] #thuctinh #phattrienbanthan
```

---

## 4. QUY CHUẨN KỸ THUẬT TẠO ẢNH BÀI VIẾT (`tools/post_image_generator.py`)
- **Tỉ lệ khung hình**: **4:5 (1080 x 1350 px)** — Tỉ lệ chiếm diện tích lớn nhất trên Facebook Mobile Feed, tăng 35% tỉ lệ dừng xem so với ảnh vuông 1:1.
- **Phong cách thị giác (Visual Style)**:
  * Nền tối điện ảnh (Dark Slate `#0b0f17`), phủ bóng mờ B-roll mờ ảo có chiều sâu.
  * Hiệu ứng vầng sáng hổ phách (Ambient Amber Glow `#f59e0b`, alpha gradient 35 lớp) tạo điểm nhấn tâm lý tĩnh lặng ban đêm.
  * Typography: Header Segoe UI Bold / Georgia viền bóng đổ mềm chống lẫn nền, Quote Mark lớn cách điệu mạ vàng.
  * Phân cấp hiển thị:
    `[BADGE_TAG] -> "CÂU QUOTE CHÍNH" -> Trích từ: Tên sách (Vàng hổ phách) -> Tác giả (Xám bạc) -> Footer: RADIO 2AM • ĐỘC THOẠI & THỨC TỈNH`.

---

## 5. QUY CHUẨN XUẤT BẢN & LÊN LỊCH (`tools/schedule_daily_posts.py`)
- **Khung giờ vàng phát hành bài viết**: **15:30 chiều mỗi ngày** (Giờ giải lao trà chiều công sở, tâm lý thư giãn, tỉ lệ đọc bài viết dài đạt đỉnh trước khi đón giờ cao điểm Reels 20:00).
- **Công cụ điều phối**:
  * Tự động sinh ảnh hàng loạt vào `outputs/posts/{slug}_4x5.png`.
  * Lên lịch tự động lên Meta Fanpage qua Graph API v22.0 (`tools/fb_post_uploader.py`).
  * Đồng bộ trạng thái vào bảng `facebook_posts` trong cơ sở dữ liệu `outputs/video_management.db`.

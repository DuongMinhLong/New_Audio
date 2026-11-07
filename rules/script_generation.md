# Quy Chuẩn Biên Soạn Kịch Bản 10/10 (Script Generation)

## 1. NGUYÊN TẮC CỐT LÕI: QUY TRÌNH 3 BƯỚC
- **CẤM TỰ KHEN BẢN THÂN**: Phải tách rời 3 vai trò và phân bổ model chuyên biệt qua 9Router:
  1. **Bước 1 (Draft) [`ag/gemini-3.8-flash-high`]**: Tạo bản thảo ban đầu tập trung vào tình huống thực tế, xung đột và giá trị thực tiễn (CẤM mở đầu "Hai giờ sáng", cấm lướt điện thoại đêm, cấm câu hỏi tu từ sáo rỗng).
  2. **Bước 2 (Critique) [`ag/gemini-3.8-flash-high`]**: Giám đốc biên tập review độc lập, chấm điểm 5 tiêu chí (0-10), bắt 3 lỗi nghiêm trọng nhất, chỉ ra đoạn thừa/lặp, kết luận GO/NO-GO.
  3. **Bước 3 (Rewrite) [`ag/claude-sonnet-4-6(max)` hoặc fallback `ag/claude-sonnet-5-5-high`]**: Biên kịch cấp cao viết lại xử lý triệt để các lỗi, văn phong tiếng Việt chuẩn tự nhiên.

---

## 2. 5 TIÊU CHUẨN BẮT BUỘC ĐẠT 10/10
1. **Sốc 3 Giây Đầu Tiên (Shocking Hook)**:
   - Đánh sập ngay một niềm tin sai lầm cũ, tát nước lạnh vào ảo tưởng.
   - CẤM TIỆT: Không chào hỏi, không giới thiệu tên sách hay tác giả ở 3s đầu, không đạo lý chung chung.
2. **100% Anti-AI (Không có mùi AI)**:
   - CẤM các từ: "hơn thế nữa", "tóm lại", "hãy nhớ rằng", "kim chỉ nam", "chúng ta thường", "cuộc sống xô bồ", "hành trình", "vun đắp", "ánh sáng hy vọng".
   - Câu ngắn (3 - 7 từ mỗi vế), giọng điệu mộc mạc, sắc lạnh, từng trải.
3. **Tư Duy Ngược (Contrarian Thinking)**:
   - Phản trực giác, bẻ gãy lối mòn (ví dụ: Chăm chỉ không giúp bạn giàu; Sống tốt không đảm bảo được yêu quý; Tích cực gượng ép chỉ sinh hoảng loạn).
4. **Huyệt Nỗi Đau Gen Z**:
   - Áp lực đồng trang lứa (lướt Threads thấy bạn bè khoe lương 50 triệu), bão giá nhà tăng gấp ba lương đứng yên, bẫy nợ BNPL, bẫy "chữa lành" trốn tránh thực tế, sương mù não vì dopamine rẻ tiền.
5. **Văn Phong Tự Nhiên Cho ChatGPT Tự Suy Diễn**:
   - Viết hoa chữ cái đầu câu bình thường. CẤM IN HOA NGUYÊN TỪ (tránh ChatGPT đánh vần từng chữ).
   - CẤM dấu ba chấm `...` và gạch ngang dài ` — ` (tránh lỗi phát âm ngắt nhịp kỳ quặc).
   - Dùng dấu câu thông thường chuẩn ngữ pháp (chấm, phẩy, hỏi).
   - Xuống dòng đôi (`\n\n`) giữa các ý chính để bộ đọc tự ngắt nghỉ lấy hơi.
   - Độ dài: **180 - 220 từ** (chuẩn 60 - 75 giây).

---

## 3. PROMPT CHUẨN GỬI 9ROUTER
```text
Bạn là một Đạo diễn Nội dung triệu view và Chuyên gia biên kịch video ngắn hàng đầu trên TikTok/Shorts/Reels.
Hãy viết một kịch bản voice-over độc thoại nội tâm (độ dài 180 - 220 từ, chuẩn 60 - 75 giây) đúc kết từ tinh hoa cuốn sách: '[TÊN SÁCH]' của tác giả [TÁC GIẢ].
Chủ đề & huyệt nỗi đau Gen Z cần chạm: [CHỦ ĐỀ / NỖI ĐAU THỰC TẾ].

BẮT BUỘC TUÂN THỦ 5 TIÊU CHUẨN VÀNG ĐỂ ĐẠT ĐIỂM 10/10:
1. HOOK 3S ĐẦU GÂY SỐC: Đánh sập ảo tưởng. CẤM chào hỏi, CẤM nêu tên sách ở 3s đầu.
2. 100% ANTI-AI: CẤM 'hơn thế nữa', 'tóm lại', 'hãy nhớ rằng', 'kim chỉ nam', 'chúng ta', 'cuộc sống xô bồ', 'hành trình'. Câu ngắn 3-7 từ.
3. TƯ DUY NGƯỢC: Bẻ gãy lối mòn số đông.
4. NỖI ĐAU GEN Z: Áp lực đồng trang lứa, bão giá, bẫy chữa lành, sương mù não.
5. VĂN PHONG TỰ NHIÊN: CẤM IN HOA CẢ TỪ, CẤM '...', CẤM ' — '. Dấu câu chuẩn. Xuống dòng đôi ngắt ý.

Chỉ xuất DUY NHẤT nội dung kịch bản thu âm, không có lời dẫn bên ngoài!
```

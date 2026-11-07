#!/usr/bin/env python3
"""
tools/generate_longform_script.py
=================================
Automated and Manual Workflow Tool for Long-Form (and Short-Form) YouTube Scripts
using the rigorous 3-step quality control pipeline:
  Step 1 (Prompt 1): Professional YouTube Scriptwriter (Initial Draft)
  Step 2 (Prompt 2): Tough YouTube Editorial Director (Independent Review & Bug Catching)
  Step 3 (Prompt 3): Senior Scriptwriter (Final Revision with TTS Prosody Markers)
"""

import os
import sys
import json
import time
import asyncio
import argparse
from pathlib import Path

# Force UTF-8 on Windows stdout/stderr
if sys.platform == "win32":
    import io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "buffer"):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIGS_DIR = BASE_DIR / "configs"
DRAFTS_DIR = BASE_DIR / "drafts"
PROMPTS_TEMPLATE_FILE = BASE_DIR / "templates" / "prompts" / "youtube_3step_workflow.md"
DRAFTS_DIR.mkdir(parents=True, exist_ok=True)

CDP_ENDPOINT = "http://127.0.0.1:9222"
CHATGPT_URL = "https://chatgpt.com/"


def load_book_info(slug: str) -> dict:
    """Find book info from configs/*.json by slug."""
    for cfg_file in CONFIGS_DIR.glob("*.json"):
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                items = data if isinstance(data, list) else data.get("books", [])
                for b in items:
                    if b.get("slug") == slug:
                        return b
        except Exception:
            continue
    return {
        "slug": slug,
        "title": slug.replace("_", " ").title(),
        "author": "",
        "core_message": "",
        "gen_z_pain_point": ""
    }


def build_prompt_1(title: str, author: str, core_message: str, pain_point: str, duration: str) -> str:
    """Build Prompt 1: Professional YouTube Scriptwriter (Initial Draft)."""
    book_desc = f"{title}"
    if author:
        book_desc += f" của tác giả {author}"
    if core_message:
        book_desc += f" (Thông điệp cốt lõi: {core_message})"

    target_audience = "Người trưởng thành đang gặp áp lực công việc, tài chính, các mối quan hệ hoặc mất phương hướng."
    if pain_point:
        target_audience += f" Đặc biệt chạm trúng huyệt nỗi đau thực tế: {pain_point}"

    return f"""Bạn là biên kịch chuyên viết kịch bản YouTube dài về phát triển bản thân, tâm lý ứng dụng, triết học thực tế và những bài học từ sách nổi tiếng.

Mục tiêu không phải viết một bài văn hay hoặc tóm tắt sách. Mục tiêu là tạo ra một kịch bản khiến người nghe muốn tiếp tục nghe, nhìn thấy chính mình trong câu chuyện và nhận được giá trị thực tế.

## I. THÔNG TIN ĐẦU VÀO

- Tên sách/chủ đề: {book_desc}
- Tiêu đề video: {title} — Nghịch Lý Trần Trụi & Sự Thật Không Ai Dám Nói
- Đối tượng khán giả: {target_audience}
- Thời lượng mục tiêu: {duration}
- Phong cách: Thẳng thắn, sâu sắc, giàu hình ảnh, có chiều sâu tâm lý, không giáo điều.
- Định dạng: Kịch bản thuyết minh YouTube bằng tiếng Việt, ưu tiên trải nghiệm nghe bằng tai.

## II. QUY TẮC VIẾT BẮT BUỘC

### 1. HOOK — GIÀNH SỰ CHÚ Ý NGAY TỪ ĐẦU
Ba giây đầu tiên phải tạo ra sự chú ý bằng một tình huống, sự thật khó chấp nhận, mâu thuẫn hoặc hậu quả thực tế.
Không mở đầu bằng: “Hai giờ sáng…”, nhân vật nằm lướt điện thoại đêm, câu triết lý chung chung.

### 2. KỂ CHUYỆN THAY VÌ GIẢNG ĐẠO
Dùng những tình huống cụ thể, quyết định khó khăn, hậu quả và xung đột nội tâm. Mỗi ví dụ cần có nhân vật, hoàn cảnh, lựa chọn, cái giá phải trả hoặc sự thay đổi trong nhận thức.

### 3. KHAI THÁC Ý TƯỞNG TỪ SÁCH
Giải thích bằng ngôn ngữ dễ hiểu, chỉ ra vấn đề thực tế, minh họa bằng tình huống đời thường, đưa ra cách áp dụng cụ thể. Không bịa trích dẫn, số liệu hoặc phát ngôn của tác giả.

### 4. GIỮ CHÂN NGƯỜI NGHE
Loại bỏ triết lý sáo rỗng, loại bỏ lặp ý và câu hỏi tu từ liên tục. Đan xen câu ngắn để tạo lực với câu dài để đào sâu.

### 5. GIÁ TRỊ THỰC TẾ
Các hành động đề xuất phải cụ thể, có thể bắt đầu ngay, phù hợp với hoàn cảnh người trưởng thành bình thường.

### 6. KẾT THÚC CÓ SỨC NẶNG
Không tóm tắt lại bài. Đưa luận điểm trở về vấn đề ban đầu với nhận thức mới. Câu cuối ngắn, rõ và đáng nhớ.

## III. ĐỊNH DẠNG ĐẦU RA
Chỉ xuất DUY NHẤT kịch bản hoàn chỉnh, sẵn sàng đưa vào công cụ tạo giọng đọc. Không kèm lời mở đầu, không checklist hay giải thích quy trình."""



def build_prompt_2(draft_script: str) -> str:
    """Build Prompt 2: Independent Review by Editorial Director."""
    return f"""Bạn là giám đốc biên tập YouTube khó tính. Hãy đánh giá bản kịch bản được cung cấp như một sản phẩm sắp xuất bản, không phải một bài viết cần được khen ngợi.

Mục tiêu: xác định chính xác những điểm khiến khán giả rời video, cảm thấy nhàm chán hoặc không nhận được giá trị thực sự.

Chấm theo 5 tiêu chí, mỗi tiêu chí từ 0–10:
1. Hook 3 giây đầu: đủ bất ngờ, cụ thể và tạo nhu cầu nghe tiếp.
2. Sức hút kể chuyện: có tình huống, xung đột, diễn biến và hệ quả.
3. Chiều sâu nội dung: ý tưởng có giá trị, được phân tích chứ không chỉ diễn đạt lại.
4. Khả năng giữ chân: nhịp kể hợp lý, không lặp ý, không có đoạn thừa.
5. Kết thúc và khả năng ứng dụng: bài học thiết thực, kết thúc có sức nặng.

QUY TẮC REVIEW:
- Không cho điểm cao chỉ vì câu chữ trôi chảy.
- Không mặc định rằng kịch bản dài hoặc giàu triết lý là sâu sắc.
- Nếu hook mở đầu bằng mô típ sáo rỗng, phải đánh dấu rõ và đề xuất hướng thay thế.
- Mọi nhận xét tiêu cực phải trích dẫn đoạn hoặc xác định chính xác vị trí trong kịch bản.
- Phân biệt lỗi nghiêm trọng ảnh hưởng trực tiếp đến khả năng giữ chân với lỗi văn phong nhỏ.
- Không bịa dữ liệu về tỷ lệ giữ chân hoặc lượt xem.
- Không yêu cầu sửa theo sở thích cá nhân nếu không chỉ ra được tác dụng của thay đổi.
- Không viết lại toàn bộ kịch bản ở bước này.

ĐẦU RA:
A. Bảng điểm 5 tiêu chí và lý do chấm.
B. Ba lỗi nghiêm trọng nhất, theo thứ tự ưu tiên. Với mỗi lỗi, nêu vị trí, nguyên nhân, tác hại và hướng sửa cụ thể.
C. Các đoạn lặp ý, sáo rỗng, thiếu logic hoặc làm chậm nhịp kể.
D. Điểm mạnh cần giữ nguyên khi sửa.
E. Danh sách chỉnh sửa bắt buộc để bản tiếp theo đạt chuẩn xuất bản.
F. Kết luận: GO hoặc NO-GO.

Không nương tay, nhưng mọi đánh giá phải có bằng chứng từ chính kịch bản.

BẢN KỊCH BẢN CẦN REVIEW:
{draft_script.strip()}"""


def build_prompt_3(original_script: str, review_report: str) -> str:
    """Build Prompt 3: Senior Scriptwriter Rewrite (Ready for TTS Audio)."""
    return f"""Bạn là biên kịch cấp cao chịu trách nhiệm tạo phiên bản cuối cùng có thể xuất bản.

Đầu vào gồm:
1. Kịch bản gốc.
2. Báo cáo review và các lỗi được xác định.

NHIỆM VỤ:
Viết lại toàn bộ kịch bản để xử lý những lỗi nghiêm trọng trong báo cáo review, đồng thời giữ lại các đoạn thực sự hiệu quả của bản gốc.

ƯU TIÊN SỬA THEO THỨ TỰ:
1. Hook và sự tò mò ban đầu.
2. Tính cụ thể của tình huống và sức hút kể chuyện.
3. Các đoạn trùng lặp hoặc thiếu giá trị.
4. Logic lập luận và độ chính xác của ý tưởng từ sách.
5. Nhịp kể, khả năng nghe tự nhiên và kết thúc.

YÊU CẦU:
- Không chỉ thay từ đồng nghĩa hoặc đánh bóng câu chữ.
- Nếu một đoạn yếu về cấu trúc, hãy xây dựng lại cấu trúc của đoạn đó.
- Không xóa một đoạn tốt chỉ để làm nội dung ngắn hơn.
- Không kéo dài bằng lời khuyên chung chung.
- Không bịa câu chuyện có thật, trích dẫn, số liệu hoặc thông tin về tác giả.
- Không bắt đầu bằng “Hai giờ sáng”, cảnh lướt điện thoại ban đêm hoặc những mô típ sáo rỗng đã bị cấm trong đề bài.
- Giữ đúng thời lượng mục tiêu.
- Văn phong phải tự nhiên khi đọc thành tiếng, không giống bài luận hoặc văn bản do AI ghép nối.
- TỰ ĐỘNG CHÈN ĐẦY ĐỦ CÁC KÝ TỰ ĐIỀU HƯỚNG BIỂU CẢM ĐỂ BỘ ĐỌC READ ALOUD THỂ HIỆN TỰ NHIÊN:
  + Dấu ba chấm (...) tại các điểm ngập ngừng, thở dài (ngắt 0.6s).
  + Dấu gạch ngang dài ( — ) để hạ tông giọng đột ngột sang trầm, lạnh, đanh thép.
  + Viết IN HOA ở các từ khóa then chốt để dằn giọng nhấn trọng âm.
  + Xuống dòng đôi (\\n\\n) giữa các câu/đoạn để bộ đọc dừng lấy hơi kịch tính.
- Không thêm những lời giải thích về quá trình chỉnh sửa vào phần thuyết minh.
- Không tuyên bố đạt 10/10 nếu chất lượng chưa thực sự đáp ứng tiêu chí.

Trước khi xuất bản, kiểm tra lại từng lỗi bắt buộc trong báo cáo review và xác nhận chúng đã được giải quyết trong bản viết lại.

ĐẦU RA:
Chỉ xuất DUY NHẤT toàn bộ kịch bản hoàn chỉnh, sẵn sàng thu âm. Không xuất báo cáo review lần hai, không có lời dẫn mở đầu hay kết luận.

KỊCH BẢN GỐC:
{original_script.strip()}

BÁO CÁO REVIEW:
{review_report.strip()}"""



def clean_script_text(raw_text: str) -> str:
    """Extract clean script lines, removing markdown headers, stage directions, etc."""
    import re
    lines = []
    in_code_block = False
    for line in raw_text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block or stripped.startswith("#"):
            continue
        stripped = re.sub(r"^\[.*?\]\s*", "", stripped)
        stripped = re.sub(r"^\(\d+:\d+\s*-\s*\d+:\d+\)\s*", "", stripped)
        stripped = re.sub(r"^\*\([^\)]+\)\*\s*", "", stripped)
        if stripped:
            lines.append(stripped)
    return "\n\n".join(lines)


async def send_prompt_and_wait(page, prompt: str, timeout: int = 180) -> str:
    """Send prompt to ChatGPT composer and wait until response is finished generating."""
    for _ in range(20):
        stop_btn = await page.query_selector("button[aria-label*='Dừng'], button[aria-label*='Stop']")
        if not stop_btn or not await stop_btn.is_visible():
            break
        await asyncio.sleep(0.5)

    before_count = await page.evaluate("""() => {
        const blocks = Array.from(document.querySelectorAll("[class*='block-']"));
        return blocks.filter(b => b.innerText.includes('ChatGPT đã nói') || b.innerText.includes('ChatGPT said')).length;
    }""")

    composers = await page.query_selector_all("[class*='ComposerLayout'] div.ProseMirror, div.ProseMirror")
    if not composers:
        composers = await page.query_selector_all("div[contenteditable='true']")
    input_el = composers[-1]
    await input_el.click()
    await asyncio.sleep(0.3)

    await input_el.focus()
    await page.keyboard.press("Control+A")
    await page.keyboard.press("Backspace")
    await asyncio.sleep(0.1)

    await input_el.evaluate("""el => {
        el.innerText = '';
        el.textContent = '';
        if (el.innerHTML) el.innerHTML = '<p><br></p>';
        el.dispatchEvent(new Event('input', { bubbles: true }));
    }""")
    await asyncio.sleep(0.2)

    await page.keyboard.insert_text(prompt)
    await asyncio.sleep(0.5)

    sent = False
    for _ in range(30):
        clicked = await page.evaluate("""() => {
            const btn = document.querySelector("button[data-testid='send-button'], button[aria-label='Gửi']");
            if (btn && !btn.disabled) {
                btn.click();
                return true;
            }
            return false;
        }""")
        if clicked:
            sent = True
            break
        await asyncio.sleep(0.25)

    if not sent:
        await input_el.focus()
        await page.keyboard.press("Enter")

    print(f"   ⏳ Đã gửi prompt! Đang đợi ChatGPT phản hồi...")
    await asyncio.sleep(2.0)

    start_t = time.time()
    prev_len = 0
    stable_count = 0
    final_text = ""

    while time.time() - start_t < timeout:
        await asyncio.sleep(1.5)
        stop_btn = await page.query_selector("button[aria-label*='Dừng'], button[aria-label*='Stop'], button[data-testid='stop-button']")
        is_stopping = stop_btn and await stop_btn.is_visible()

        assistant_text = await page.evaluate("""() => {
            const blocks = Array.from(document.querySelectorAll("[class*='block-']"));
            const assistantBlocks = blocks.filter(b => b.innerText.includes('ChatGPT đã nói') || b.innerText.includes('ChatGPT said'));
            if (assistantBlocks.length === 0) return null;
            let t = assistantBlocks[assistantBlocks.length - 1].innerText;
            return t.replace(/^ChatGPT đã nói:?\\s*/i, '').trim();
        }""")

        curr_count = await page.evaluate("""() => {
            const blocks = Array.from(document.querySelectorAll("[class*='block-']"));
            return blocks.filter(b => b.innerText.includes('ChatGPT đã nói') || b.innerText.includes('ChatGPT said')).length;
        }""")

        if curr_count > before_count and assistant_text:
            curr_len = len(assistant_text)
            if not is_stopping and curr_len > 40:
                if curr_len == prev_len:
                    stable_count += 1
                    if stable_count >= 2:
                        final_text = assistant_text
                        break
                else:
                    prev_len = curr_len
                    stable_count = 0

    if not final_text:
        raise RuntimeError("ChatGPT không phản hồi hoặc timeout.")
    return final_text




async def run_cdp_auto_pipeline(book_data: dict, duration: str, title: str, author: str, pain_point: str):
    """Run full 3-turn pipeline inside ChatGPT Web via Chrome CDP."""
    from playwright.async_api import async_playwright

    slug = book_data["slug"]
    print(f"\n🚀 Khởi động pipeline tự động qua Chrome CDP cho: {title} ({slug})")
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp(CDP_ENDPOINT)
        except Exception as e:
            print(f"❌ Không thể kết nối tới Chrome CDP ({CDP_ENDPOINT}): {e}")
            print("👉 Vui lòng khởi động Chrome với cờ: --remote-debugging-port=9222")
            return

        context = browser.contexts[0]
        page = None
        for p_page in context.pages:
            if "chatgpt.com" in p_page.url:
                page = p_page
                break
        if not page:
            page = await context.new_page()
            await page.goto(CHATGPT_URL, wait_until="domcontentloaded")
            await asyncio.sleep(2.0)

        # 1. Turn 1
        print("\n📝 [BƯỚC 1/3] Đang gửi Prompt 1: Biên kịch chuyên nghiệp...")
        p1 = build_prompt_1(title, author, book_data.get("core_message", ""), pain_point, duration)
        p1_file = DRAFTS_DIR / f"{slug}_p1_prompt.txt"
        p1_file.write_text(p1, encoding="utf-8")

        raw_draft = await send_prompt_and_wait(page, p1)
        draft_file = DRAFTS_DIR / f"{slug}_p1_raw.txt"
        draft_file.write_text(raw_draft, encoding="utf-8")
        print(f"✅ Đã nhận bản thảo ({len(raw_draft)} ký tự). Đã lưu tại: {draft_file}")

        # 2. Turn 2
        print("\n🔍 [BƯỚC 2/3] Đang gửi Prompt 2: Giám đốc biên tập review khó tính...")
        p2 = build_prompt_2(raw_draft)
        p2_file = DRAFTS_DIR / f"{slug}_p2_prompt.txt"
        p2_file.write_text(p2, encoding="utf-8")

        review_report = await send_prompt_and_wait(page, p2)
        review_file = DRAFTS_DIR / f"{slug}_p2_review.txt"
        review_file.write_text(review_report, encoding="utf-8")
        print(f"✅ Đã nhận báo cáo phản biện. Đã lưu tại: {review_file}")

        # 3. Turn 3
        print("\n✨ [BƯỚC 3/3] Đang gửi Prompt 3: Biên kịch cấp cao viết lại bản thu âm...")
        p3 = build_prompt_3(raw_draft, review_report)
        p3_file = DRAFTS_DIR / f"{slug}_p3_prompt.txt"
        p3_file.write_text(p3, encoding="utf-8")

        final_raw = await send_prompt_and_wait(page, p3)
        final_clean = clean_script_text(final_raw)
        final_file = DRAFTS_DIR / f"{slug}_p3_final.txt"
        final_file.write_text(final_clean, encoding="utf-8")
        print(f"🎉 HOÀN THÀNH BẢN CUỐI! Đã lưu tại: {final_file}")
        print(f"📊 Độ dài bản cuối: {len(final_clean.split())} từ.")



def main():
    parser = argparse.ArgumentParser(description="YouTube Book Script 3-Step Production Workflow Helper")
    parser.add_argument("--slug", type=str, required=True, help="Book slug (e.g., tam_ly_hoc_ve_tien, dam_bi_ghet)")
    parser.add_argument("--title", type=str, default="", help="Custom book/video title")
    parser.add_argument("--author", type=str, default="", help="Author name")
    parser.add_argument("--pain", type=str, default="", help="Specific Gen Z pain point")
    parser.add_argument("--duration", type=str, default="12 phút (~2000 từ)", help="Target duration string or minutes")
    parser.add_argument("--mode", type=str, default="export", choices=["export", "review", "finalize", "auto"],
                        help="Operation mode: 'export' (generate copy-paste prompts), 'review' (build p2 from p1_raw), 'finalize' (build p3 from p1_raw + p2_review), 'auto' (run 3-turn CDP)")

    args = parser.parse_args()
    slug = args.slug.strip()
    book_info = load_book_info(slug)

    title = args.title or book_info.get("title", slug.replace("_", " ").title())
    author = args.author or book_info.get("author", "")
    pain_point = args.pain or book_info.get("gen_z_pain_point", "")
    core_msg = book_info.get("core_message", "")
    duration = args.duration
    if duration.isdigit():
        duration = f"{duration} phút (~{int(duration)*160} từ)"

    print("=" * 70)
    print("🎬 YOUTUBE SCRIPT 3-STEP PIPELINE HELPER")
    print(f"📖 Cuốn sách: {title}")
    if author:
        print(f"✍️ Tác giả: {author}")
    print(f"⏱️ Thời lượng mục tiêu: {duration}")
    print(f"⚙️ Chế độ (Mode): {args.mode}")
    print("=" * 70)

    if args.mode == "export":
        p1 = build_prompt_1(title, author, core_msg, pain_point, duration)
        p1_path = DRAFTS_DIR / f"{slug}_p1_prompt.txt"
        p1_path.write_text(p1, encoding="utf-8")

        p2_tmpl = build_prompt_2("[DÁN BẢN THẢO TỪ PROMPT 1 VÀO ĐÂY]")
        p2_path = DRAFTS_DIR / f"{slug}_p2_template.txt"
        p2_path.write_text(p2_tmpl, encoding="utf-8")

        p3_tmpl = build_prompt_3("[DÁN KỊCH BẢN GỐC PROMPT 1 VÀO ĐÂY]", "[DÁN BÁO CÁO REVIEW PROMPT 2 VÀO ĐÂY]")
        p3_path = DRAFTS_DIR / f"{slug}_p3_template.txt"
        p3_path.write_text(p3_tmpl, encoding="utf-8")

        print(f"\n✅ ĐÃ XUẤT CẢ 3 PROMPT SẴN SÀNG COPY VÀO CHATGPT WEB:")
        print(f"   1. Bước 1: {p1_path}")
        print(f"   2. Bước 2: {p2_path}")
        print(f"   3. Bước 3: {p3_path}")
        print("\n💡 Các bước thực hiện thủ công:")
        print(f"   - Copy nội dung {p1_path.name} dán vào ChatGPT Web.")
        print(f"   - Lưu câu trả lời vào: drafts/{slug}_p1_raw.txt")
        print(f"   - Chạy: python tools/generate_longform_script.py --slug {slug} --mode review")

    elif args.mode == "review":
        raw_path = DRAFTS_DIR / f"{slug}_p1_raw.txt"
        if not raw_path.exists():
            print(f"❌ Không tìm thấy: {raw_path}")
            print(f"👉 Vui lòng tạo file {raw_path} và dán kết quả từ Bước 1 vào trước.")
            return
        draft_content = raw_path.read_text(encoding="utf-8")
        p2 = build_prompt_2(draft_content)
        p2_path = DRAFTS_DIR / f"{slug}_p2_input.txt"
        p2_path.write_text(p2, encoding="utf-8")
        print(f"\n✅ ĐÃ TẠO PROMPT REVIEW BƯỚC 2: {p2_path}")
        print(f"👉 Chỉ cần copy {p2_path.name} dán vào ChatGPT Web!")
        print(f"👉 Sau đó dán câu trả lời review vào: drafts/{slug}_p2_review.txt")
        print(f"👉 Rồi chạy: python tools/generate_longform_script.py --slug {slug} --mode finalize")

    elif args.mode == "finalize":
        raw_path = DRAFTS_DIR / f"{slug}_p1_raw.txt"
        rev_path = DRAFTS_DIR / f"{slug}_p2_review.txt"
        if not raw_path.exists() or not rev_path.exists():
            print(f"❌ Thiếu file: cần cả {raw_path} và {rev_path}")
            return
        p3 = build_prompt_3(raw_path.read_text(encoding="utf-8"), rev_path.read_text(encoding="utf-8"))
        p3_path = DRAFTS_DIR / f"{slug}_p3_input.txt"
        p3_path.write_text(p3, encoding="utf-8")
        print(f"\n✅ ĐÃ TẠO PROMPT VIẾT LẠI BƯỚC 3: {p3_path}")
        print(f"👉 Copy {p3_path.name} dán vào ChatGPT để nhận bản cuối chuẩn thu âm!")
        print(f"👉 Lưu bản cuối vào: drafts/{slug}_p3_final.txt")

    elif args.mode == "auto":
        asyncio.run(run_cdp_auto_pipeline(book_info, duration, title, author, pain_point))


if __name__ == "__main__":
    main()


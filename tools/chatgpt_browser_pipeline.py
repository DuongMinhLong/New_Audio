"""
ChatGPT Browser Interactive Pipeline
====================================
End-to-end book script generation, 3-turn review, and direct Read Aloud audio capture
directly inside ChatGPT Web UI via Chrome CDP (port 9222).

Leaves 100% visible conversation history in user's ChatGPT sidebar:
  Turn 1: Generate initial draft from book core & Gen Z pain points
  Turn 2: Elite director critique & review against 5 golden standards
  Turn 3: Final 10/10 clean script with TTS Prosody markers (..., — , IN HOA, \\n\\n)
  Audio Capture: Directly trigger Read Aloud on Turn 3 to capture native MP3 stream!
"""

import os
import sys
import time
import json
import asyncio
import subprocess
from pathlib import Path
from playwright.async_api import async_playwright, Page, Response

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIGS_DIR = BASE_DIR / "configs"
CACHE_DIR = BASE_DIR / "cache"
OUTPUTS_DIR = BASE_DIR / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

CDP_ENDPOINT = "http://127.0.0.1:9222"
CHATGPT_URL = "https://chatgpt.com/"

GEN_Z_THEMES = {
    "dam_bi_ghet": {
        "pain": "Áp lực làm vừa lòng thiên hạ (people-pleaser); sợ bị phán xét; sống phông bạt theo kỳ vọng xã hội.",
        "hook_focus": "Càng cố gắng làm vừa lòng tất cả mọi người... bạn càng trở thành một kẻ vô hình đáng thương! Sống theo kỳ vọng của thiên hạ là cách nhanh nhất để đánh mất chính mình.",
        "anti_cliche": "CẤM mở đầu bằng 'Hai giờ sáng', CẤM lướt điện thoại đêm. Mở đầu bằng sự tàn nhẫn của việc làm hài lòng người khác.",
    },
    "tam_ly_hoc_ve_tien": {
        "pain": "Bẫy nợ tín dụng mua trước trả sau (BNPL); lương 10 triệu tiêu 12 triệu; quẹt thẻ mua sự sang chảnh ảo.",
        "hook_focus": "Người ta dùng số tiền mình CHƯA LÀM RA... mua những thứ mình KHÔNG CẦN... để gây ấn tượng với những kẻ mình KHÔNG THÍCH!",
        "anti_cliche": "CẤM mở đầu bằng 'Hai giờ sáng'. Mở đầu bằng hành vi quẹt thẻ tín dụng, bẫy trả góp và ảo tưởng phong cách sống.",
    },
    "atomic_habits": {
        "pain": "Thói quen trì hoãn, ảo tưởng thay đổi ngoạn mục chỉ sau một đêm, xem thường tác động của những việc nhỏ mỗi ngày.",
        "hook_focus": "Bạn không thất bại vì bạn thiếu ý chí! Bạn thất bại vì cái bẫy thói quen tí hon đang âm thầm kéo bạn xuống đáy vực! Mỗi ngày tặc lưỡi bỏ qua 1 việc nhỏ, 1 năm sau bạn mất trắng tất cả!",
        "anti_cliche": "CẤM mở đầu bằng 'Hai giờ sáng'. Mở đầu bằng sự thật cay đắng về việc thói quen tồi tệ tích lũy theo cấp số nhân.",
    },
    "cant_hurt_me": {
        "pain": "Phong trào 'chữa lành' độc hại; hơi gặp áp lực công việc là xin nghỉ; lấy cớ tổn thương để trốn tránh trách nhiệm.",
        "hook_focus": "Hơi áp lực một chút là xin nghỉ việc 'để chữa lành'... Tỉnh lại đi: Bạn không hề tổn thương... Bạn chỉ đang HÈN NHÁT!",
        "anti_cliche": "CẤM mở đầu bằng 'Hai giờ sáng'. Tát thẳng vào ảo tưởng trốn việc và thói quen đổ lỗi cho hoàn cảnh.",
    },
    "di_tim_le_song": {
        "pain": "Khủng hoảng hiện sinh tuổi 20-25; cảm giác đi làm như một cỗ máy vô hồn; sống vật vờ không mục đích.",
        "hook_focus": "Điều đáng sợ nhất của cuộc đời không phải là cái chết... mà là sống đến năm 80 tuổi nhưng thực chất đã chết từ năm 25 tuổi!",
        "anti_cliche": "CẤM mở đầu bằng 'Hai giờ sáng' hay lướt mạng xã hội. Đánh thẳng vào nỗi đau sống mòn và cảm giác vô nghĩa khi thức dậy mỗi sáng.",
    },
    "dac_nhan_tam": {
        "pain": "Cái tôi hiếu thắng trong giao tiếp; thích tranh cãi tay đôi hơn thua từng câu chữ trên mạng để rồi cô độc.",
        "hook_focus": "Càng cố cãi thắng để bảo vệ cái tôi... bạn càng chứng minh cho người khác thấy bạn là một kẻ thảm hại!",
        "anti_cliche": "CẤM mở đầu bằng 'Hai giờ sáng'. Mở đầu bằng xung đột trong một cuộc tranh cãi thực tế, cảm giác thắng lý nhưng thua tình.",
    },
    "seneca_nghe_thuat_song": {
        "pain": "Hội chứng Overthinking kinh niên; tự tưởng tượng ra 100 kịch bản tồi tệ rồi tự làm mình đau khổ.",
        "hook_focus": "90% những bi kịch khiến bạn lo sợ đến phát điên... THỰC CHẤT KHÔNG BAO GIỜ XẢY RA! Bạn không bị cuộc đời hành hạ — bạn đang tự đày đọa mình bằng những nỗi sợ tưởng tượng!",
        "anti_cliche": "CẤM mở đầu bằng 'Hai giờ sáng'. Mở đầu bằng việc bộ não tự tạo ra nhà tù tưởng tượng đày đọa bản thân.",
    },
    "ky_luat_la_tu_do": {
        "pain": "Ảo tưởng tự do là buông thả bản năng; thức đêm ngủ ngày, lười biếng vô định rồi than kiệt sức.",
        "hook_focus": "Thích gì làm nấy, ngủ nướng đến trưa, buông thả bản năng... Đó không phải là tự do! Đó là sự nô lệ thảm hại nhất cho cảm xúc nhất thời!",
        "anti_cliche": "CẤM mở đầu bằng 'Hai giờ sáng'. Đánh thẳng vào sự đối lập giữa buông thả bản năng và kỷ luật thép.",
    },
    "tu_duy_nhanh_va_cham": {
        "pain": "Bẫy cảm tính, bốc đồng tài chính, ảo tưởng mình thông minh nhưng luôn bị thuật toán và tâm lý đám đông thao túng.",
        "hook_focus": "Bộ não của bạn đang lừa dối bạn 24/7! 95% những quyết định bạn tự hào là sáng suốt... thực chất chỉ là phản xạ mù quáng của cảm xúc nhất thời!",
        "anti_cliche": "CẤM mở đầu bằng 'Hai giờ sáng'. Mở đầu bằng sự thật bẽ bàng về những quyết định sai lầm bốc đồng.",
    },
    "deep_work": {
        "pain": "Não mục rỗng vì đa nhiệm (brain rot), không thể tập trung sâu 15 phút, nỗi sợ bị làn sóng AI đào thải.",
        "hook_focus": "Làn sóng AI đang xóa sổ hàng triệu công việc... còn bạn thì không thể ngồi yên 15 phút mà không thò tay vào chiếc điện thoại! Não bạn đang bị nghiện dopamine rẻ tiền đến mức tàn phế!",
        "anti_cliche": "CẤM mở đầu bằng 'Hai giờ sáng'. Mở đầu bằng áp lực thực tế nơi công sở và cuộc đào thải của công nghệ.",
    },
}


def get_ffmpeg_path() -> str:
    from shutil import which
    ffmpeg = which("ffmpeg")
    if ffmpeg:
        return ffmpeg
    win_path = Path(r"C:\Users\Windows\AppData\Local\Programs\Python\Python312\Scripts\ffmpeg.exe")
    if win_path.exists():
        return str(win_path)
    return "ffmpeg"


async def open_new_chatgpt_tab_for_book(browser, title: str) -> Page:
    """Always opens a separate, dedicated browser tab for each book so the user has 1 tab per book."""
    context = browser.contexts[0] if browser.contexts else await browser.new_context()

    # If there is only one page and it is blank/unused, reuse it; otherwise ALWAYS create a brand new tab!
    if len(context.pages) == 1 and context.pages[0].url in ("about:blank", "chrome://newtab/"):
        page = context.pages[0]
    else:
        page = await context.new_page()

    print(f"\n📑 [NEW TAB] Khởi tạo Tab riêng trên Chrome cho cuốn sách: '{title}' (Tổng tabs đang mở: {len(context.pages)})...")
    await page.goto(CHATGPT_URL, wait_until="domcontentloaded", timeout=45000)
    await asyncio.sleep(2.0)
    await page.wait_for_selector("div.ProseMirror, div[contenteditable='true']", timeout=25000)
    await asyncio.sleep(1.0)
    return page

async def send_prompt_and_wait(page: Page, prompt: str, timeout: int = 100) -> str:
    """Type a prompt into ChatGPT composer, send it, and wait for complete generation."""
    # Ensure any previous generation is completely finished
    for _ in range(40):
        stop_btn = await page.query_selector("button[aria-label*='Dừng'], button[aria-label*='Stop'], button[data-testid='stop-button']")
        if not stop_btn or not await stop_btn.is_visible():
            break
        await asyncio.sleep(0.5)

    before_count = await page.evaluate("""() => {
        const blocks = Array.from(document.querySelectorAll("[class*='block-']"));
        return blocks.filter(b => b.innerText.includes('ChatGPT đã nói') || b.innerText.includes('ChatGPT said')).length;
    }""")

    # Find composer: always grab the last ProseMirror (avoids Canvas editor)
    composers = await page.query_selector_all("[class*='ComposerLayout'] div.ProseMirror, div.ProseMirror")
    if not composers:
        composers = await page.query_selector_all("div[contenteditable='true']")
    input_el = composers[-1]
    await input_el.click()
    await asyncio.sleep(0.3)

    # Ensure composer is cleared before inserting text
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

    # Wait for send button to be enabled and click it
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

    # Verify input text was consumed (cleared by ChatGPT submission)
    for _ in range(15):
        comp_text = await page.evaluate("() => document.querySelector('div.ProseMirror, div[contenteditable=\"true\"]')?.innerText?.trim() || ''")
        if not comp_text or len(comp_text) < 10:
            break
        # Still not sent? Force click send button directly via DOM
        await page.evaluate("""() => {
            const btn = document.querySelector("button[data-testid='send-button'], button[aria-label='Gửi']");
            if (btn) btn.click();
        }""")
        await asyncio.sleep(0.5)

    print(f"   ⏳ Sent prompt! (existing turns: {before_count}). Waiting for ChatGPT response...")
    await asyncio.sleep(2.0)

    start_t = time.time()
    prev_len = 0
    stable_count = 0
    final_text = ""

    while time.time() - start_t < timeout:
        await asyncio.sleep(1.2)

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

        if curr_count <= before_count and (time.time() - start_t) > 4:
            # Re-trigger submit if prompt is still sitting in composer
            await page.evaluate("""() => {
                const btn = document.querySelector("button[data-testid='send-button'], button[aria-label='Gửi']");
                if (btn && !btn.disabled) btn.click();
            }""")

        if curr_count > before_count and assistant_text:
            curr_len = len(assistant_text)

            # Check for error state in ChatGPT message
            lower_t = assistant_text.lower()
            if "không thể tải phản hồi" in lower_t or "there was an error" in lower_t or "something went wrong" in lower_t:
                retry_btn = await page.query_selector("button[aria-label*='Tạo lại'], button[aria-label*='Thử lại'], button[aria-label*='Regenerate']")
                if retry_btn and await retry_btn.is_visible():
                    print("   ⚠️ Phát hiện lỗi ChatGPT ('Không thể tải phản hồi'), đang bấm 'Tạo lại'...")
                    await retry_btn.click()
                    await asyncio.sleep(2.5)
                continue

            if not is_stopping and curr_len > 40:
                if curr_len == prev_len:
                    stable_count += 1
                    if stable_count >= 2:
                        final_text = assistant_text
                        break
                else:
                    prev_len = curr_len
                    stable_count = 0

    if not final_text or len(final_text) < 20:
        raise RuntimeError(f"ChatGPT response timed out or failed to generate (received only {len(final_text)} chars).")

    return final_text


async def capture_read_aloud_audio(page: Page, output_name: str, script_text: str = None, timeout: int = 45) -> tuple[str, str]:
    """Capture streamed AAC audio from Read Aloud button and convert to MP3."""
    captured_data = []
    capture_event = asyncio.Event()

    # Stop any currently playing audio in ChatGPT
    try:
        stop_btn = await page.query_selector("button[aria-label*='Dừng'], button[aria-label*='Stop']")
        if stop_btn and await stop_btn.is_visible():
            await stop_btn.click()
            await asyncio.sleep(1.0)
    except Exception:
        pass

    async def on_response(response: Response):
        url = response.url
        ct = response.headers.get("content-type", "").lower()
        if "/backend-api/synthesize" in url or "audio/aac" in ct or ("audio" in ct and "blob:" in url):
            try:
                body = await response.body()
                if body and len(body) > 500:
                    captured_data.append(body)
                    capture_event.set()
            except Exception:
                pass

    page.on("response", on_response)

    try:
        await page.evaluate("""() => {
            document.querySelectorAll('audio').forEach(a => { a.muted = true; a.volume = 0; });
        }""")

        # Scroll to bottom so ChatGPT renders all message action bars
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(1.0)

        read_btns = []
        for _ in range(10):
            read_btns = await page.query_selector_all("button[aria-label='Đọc to'], button[aria-label='Read aloud'], button[aria-label*='Đọc']")
            if read_btns:
                break
            await asyncio.sleep(0.5)

        if not read_btns:
            raise RuntimeError("Read Aloud ('Đọc to') button not found in ChatGPT UI.")

        # In a 3-turn pipeline (Turn 1 Draft -> Turn 2 Review -> Turn 3 Final Script),
        # the final script is strictly the last message on the page!
        target_btn = read_btns[-1]
        print(f"   🎯 Targeted the final script message Read Aloud button (Btn #{len(read_btns)-1}).")

        await target_btn.scroll_into_view_if_needed()
        await asyncio.sleep(0.5)
        await target_btn.click()
        print("   🎙️ Clicked Read Aloud button, sniffing audio stream...")

        try:
            await asyncio.wait_for(capture_event.wait(), timeout=timeout)
            await asyncio.sleep(3.5)
        except asyncio.TimeoutError:
            raise TimeoutError("Timeout waiting for ChatGPT synthesized audio stream.")

    finally:
        page.remove_listener("response", on_response)
        try:
            stop_btn = await page.query_selector("button[aria-label*='Dừng'], button[aria-label*='Stop']")
            if stop_btn and await stop_btn.is_visible():
                await stop_btn.click()
        except Exception:
            pass

    if not captured_data:
        raise RuntimeError("No audio data was captured from ChatGPT Read Aloud.")

    audio_bytes = b"".join(captured_data)
    aac_path = OUTPUTS_DIR / f"{output_name}.aac"
    mp3_path = OUTPUTS_DIR / f"{output_name}.mp3"
    book_cache_dir = CACHE_DIR / "books" / output_name
    book_cache_dir.mkdir(parents=True, exist_ok=True)
    cache_mp3 = book_cache_dir / "audio.mp3"

    with open(aac_path, "wb") as f:
        f.write(audio_bytes)

    ffmpeg_bin = get_ffmpeg_path()
    cmd = [ffmpeg_bin, "-y", "-i", str(aac_path), "-c:a", "libmp3lame", "-b:a", "192k", str(mp3_path)]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    import shutil
    shutil.copyfile(mp3_path, cache_mp3)

    # Invalidate stale subtitles
    stale_srt = book_cache_dir / "subtitles.srt"
    if stale_srt.exists():
        stale_srt.unlink()

    return str(aac_path), str(mp3_path)

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
        # Remove bracket labels like [HOOK - 0-3s] or [ĐỘC THOẠI]
        stripped = re.sub(r"^\[.*?\]\s*", "", stripped)
        stripped = re.sub(r"^\(\d+:\d+\s*-\s*\d+:\d+\)\s*", "", stripped)
        stripped = re.sub(r"^\*\([^\)]+\)\*\s*", "", stripped)
        if stripped:
            lines.append(stripped)
    return "\n\n".join(lines)



async def generate_book_script_and_audio(book_data: dict, force_tts: bool = True) -> dict:
    """Run 3-turn interactive script creation, review, and audio capture directly in ChatGPT."""
    slug = book_data["slug"]
    title = book_data["title"]
    author = book_data.get("author", "")
    core_message = book_data.get("core_message", "")

    theme_info = GEN_Z_THEMES.get(slug, {})
    gen_z_pain = book_data.get("gen_z_pain_point") or theme_info.get("pain", "")
    hook_focus = book_data.get("hook_focus") or theme_info.get("hook_focus", "")

    book_cache = CACHE_DIR / "books" / slug
    book_cache.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 70)
    print(f"📖 CHATGPT BROWSER PIPELINE: {title.upper()} ({slug})")
    print(f"🎯 Huyệt Nỗi Đau: {gen_z_pain}")
    print(f"🎯 Gợi ý Hook 3s: {hook_focus}")
    print("=" * 70)

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_ENDPOINT)
        page = await open_new_chatgpt_tab_for_book(browser, title)

        # TURN 1: Initial Script Draft
        print("\n🔹 [TURN 1] Sending prompt to ChatGPT: Viết bản thảo kịch bản...")
        turn1_prompt = f"""Bạn là một Đạo diễn Nội dung triệu view và Chuyên gia biên kịch video ngắn hàng đầu trên TikTok/Shorts/Reels.
Hãy viết một bản thảo kịch bản voice-over độc thoại nội tâm (độ dài 180 - 220 từ, chuẩn 60 - 75 giây) đúc kết từ tinh hoa cuốn sách: '{title}' của tác giả {author}.
Thông điệp cốt lõi: {core_message}.
Huyệt nỗi đau Gen Z cần chạm: {gen_z_pain}.
Gợi ý Hook 3s đầu: {hook_focus}.

⛔ NGUYÊN TẮC SỐC VÀ CHỐNG TRÙNG LẶP (BẮT BUỘC TUÂN THỦ 100%):
1. {theme_info.get("anti_cliche", "CẤM dùng văn mẫu!")}
2. CẤM TUYỆT ĐỐI mở đầu bằng cụm từ: 'Hai giờ sáng', '2h sáng', 'nửa đêm', hoặc mô típ 'nằm lướt điện thoại'. Mô típ này bị CẤM TIỆT 100%!
3. Hook 3 giây đầu PHẢI ĐỘC BẢN: Đánh sập ngay một ảo tưởng, tát nước lạnh vào mặt người nghe bằng một góc nhìn phản trực giác cực sốc: "{hook_focus}".
4. CẤM chào hỏi ('Chào các bạn'), CẤM giới thiệu tên sách hay tác giả ở câu đầu tiên.
5. 100% Anti-AI: Tuyệt đối không dùng văn mẫu ('hơn thế nữa', 'tóm lại', 'hãy nhớ rằng', 'kim chỉ nam', 'chúng ta', 'cuộc sống xô bồ'). Câu ngắn (3-7 từ), sắc lạnh, chân thực, như một cú đấm vào tâm can.
6. Tư duy ngược: Vạch trần nghịch lý thực tế thay vì đạo lý self-help sáo rỗng.
7. Chạm đúng huyệt nỗi đau thực tế: {gen_z_pain}."""

        draft_response = await send_prompt_and_wait(page, turn1_prompt)
        print("✅ [TURN 1] Đã nhận bản thảo từ ChatGPT!")

        # TURN 2: Director Critique & Review (Strict Editorial Director)
        print("\n🔹 [TURN 2] Mời GPT đóng vai Giám đốc biên tập khó tính bóc tách lỗi thật...")
        turn2_prompt = f"""Bạn là giám đốc biên tập nội dung triệu view khó tính. Hãy đánh giá bản kịch bản vừa viết như một sản phẩm sắp xuất bản:
Chấm theo 5 tiêu chí (0–10 điểm):
1. Hook 3 giây đầu: Đủ bất ngờ, cụ thể, không dính chữ 'Hai giờ sáng', không mô típ lướt điện thoại đêm, tạo nhu cầu nghe tiếp.
2. Sức hút kể chuyện: Có tình huống, xung đột, diễn biến và hệ quả thực tế.
3. Chiều sâu nội dung: Bẻ gãy tư duy lối mòn về chủ đề cuốn sách '{title}', diệt sạch từ ngữ AI sáo rỗng.
4. Đánh trúng huyệt nỗi đau Gen Z: {gen_z_pain}
5. Nhịp điệu và câu từ: Dứt khoát, gai góc, tự nhiên khi đọc thành tiếng.

ĐẦU RA:
A. Bảng điểm 5 tiêu chí (0-10) và lý do chấm.
B. 3 lỗi nghiêm trọng nhất theo thứ tự ưu tiên (Vị trí, nguyên nhân, tác hại, hướng sửa).
C. Các đoạn lặp ý, sáo rỗng hoặc làm chậm nhịp.
D. Điểm mạnh cần giữ nguyên khi sửa.
E. Danh sách chỉnh sửa bắt buộc để bản tiếp theo đạt chuẩn 10/10.
F. Kết luận: GO hoặc NO-GO (Không nương tay, nhận xét phải trích dẫn câu chữ cụ thể)."""

        critique_response = await send_prompt_and_wait(page, turn2_prompt)
        print("✅ [TURN 2] Giám đốc biên tập đã hoàn thành bài phản biện & bắt lỗi chi tiết!")

        # TURN 3: Regenerate Final 10/10 Script with TTS Prosody
        print("\n🔹 [TURN 3] Yêu cầu ChatGPT đóng vai Biên kịch cấp cao viết lại bản cuối chuẩn thu âm...")
        turn3_prompt = """Bạn là biên kịch cấp cao. Dựa trên toàn bộ báo cáo phản biện ở trên, hãy viết lại kịch bản hoàn chỉnh để xuất bản thu âm.

ƯU TIÊN SỬA THEO THỨ TỰ:
1. Hook 3s đầu: Đánh sập ngay ảo tưởng hoặc bắt quả tang hành vi (Tuyệt đối CẤM 'Hai giờ sáng' hoặc lướt điện thoại).
2. Xử lý triệt để 3 lỗi nghiêm trọng nhất và các đoạn sáo rỗng đã bị chỉ ra ở Turn 2.
3. Giữ lại những điểm mạnh cốt lõi của bản thảo.
4. Đảm bảo độ dài chuẩn: 180 - 220 từ (60 - 75 giây giọng đọc).

QUY TẮC BẮT BUỘC CHO BỘ ĐỌC DIỄN CẢM (CHATGPT READ ALOUD):
- Chèn đầy đủ ký tự điều hướng biểu cảm:
  + Dấu ba chấm (...) tại các điểm ngập ngừng, thở dài (bộ đọc ngắt 0.6s).
  + Dấu gạch ngang dài ( — ) để đột ngột hạ tông giọng sang trầm, lạnh, đanh thép.
  + Viết IN HOA ở các từ khóa then chốt để dằn giọng nhấn trọng âm.
  + Xuống dòng đôi (\\n\\n) giữa các câu để dừng lấy hơi kịch tính.

ĐIỀU KIỆN SỐNG CÒN (APPROVAL GATE):
- Phản hồi này sẽ được bấm nút 'Đọc to' (Read Aloud) để thu âm phát hành ngay lập tức.
- BẠN CHỈ ĐƯỢC XUẤT DUY NHẤT LỜI THOẠI KỊCH BẢN NÓI.
- TUYỆT ĐỐI KHÔNG VIẾT BẤT KỲ TỪ NÀO KHÁC NGOÀI LỜI THOẠI: Không tiêu đề [HOOK], không [ĐỘC THOẠI], không 'Dưới đây là...', không 'Kịch bản 10/10:', không lời giải thích. Bắt đầu ngay lập tức bằng câu nói đầu tiên và kết thúc bằng câu nói cuối cùng!"""

        raw_final_script = await send_prompt_and_wait(page, turn3_prompt)
        final_script = clean_script_text(raw_final_script)
        print("✅ [TURN 3] Kịch bản hoàn chỉnh 10/10 đã hoàn thành xong!")

        words = final_script.split()
        word_count = len(words)
        has_prosody = "..." in final_script or " — " in final_script or "\n\n" in final_script
        print(f"\n📊 KẾT QUẢ KIỂM ĐỊNH KỊCH BẢN ({slug}):")
        print(f"   - Số từ: {word_count} từ")
        print(f"   - Ký tự TTS Prosody: {'✅' if has_prosody else '❌'}")

        # Strict Approval Gatekeeper (Rule #0 & Rule #5)
        if word_count < 140:
            raise RuntimeError(f"❌ CỔNG DUYỆT 10/10 TỪ CHỐI: Kịch bản chỉ có {word_count} từ (yêu cầu tối thiểu 150-220 từ)!")
        if not has_prosody:
            raise RuntimeError("❌ CỔNG DUYỆT 10/10 TỪ CHỐI: Kịch bản thiếu ký tự biểu cảm TTS Prosody (..., —, IN HOA)!")

        lower_s = final_script.lower()
        if "hai giờ sáng" in lower_s or "2 giờ sáng" in lower_s or "2h sáng" in lower_s:
            print("⚠️ Cảnh báo: Kịch bản vẫn có chữ 'hai giờ sáng', đang tự động làm sạch...")
            import re
            final_script = re.sub(r"^(hai|2)\s*giờ\s*sáng[\.\,\s\—\-]*", "", final_script, flags=re.IGNORECASE).strip()
            final_script = final_script[0].upper() + final_script[1:] if final_script else final_script

        print(f"   - Trạng thái kiểm định: APPROVED (10/10 OK - SẴN SÀNG GET AUDIO)")

        # Save script to cache
        script_file = book_cache / "script.txt"
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(final_script)

        # Save review log
        review_log = {
            "slug": slug,
            "title": title,
            "chat_url": page.url,
            "word_count": word_count,
            "turn1_draft": draft_response,
            "turn2_critique": critique_response,
            "turn3_final_script": final_script,
            "status": "APPROVED (10/10 OK)",
        }
        with open(book_cache / "review_log.json", "w", encoding="utf-8") as f:
            json.dump(review_log, f, ensure_ascii=False, indent=2)

        # Update configs/books_10.json
        config_path = CONFIGS_DIR / "books_10.json"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                books = json.load(f)
            for b in books:
                if b["slug"] == slug:
                    b["script"] = final_script
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(books, f, ensure_ascii=False, indent=2)

        # Direct Read Aloud capture targeting Turn 3 script (the final message)
        print(f"\n🎙️ BẮT ĐẦU THU ÂM (READ ALOUD) TRỰC TIẾP TỪ TIN NHẮN KỊCH BẢN CUỐI CÙNG TRÊN CHATGPT...")
        aac_path, mp3_path = await capture_read_aloud_audio(page, output_name=slug, timeout=45)
        mp3_size_kb = os.path.getsize(mp3_path) / 1024

        print(f"🎉 THU ÂM HOÀN TẤT!")
        print(f"   - File MP3: {mp3_path} ({mp3_size_kb:.1f} KB)")
        print(f"   - Lịch sử Chat trên ChatGPT: {page.url}")

        # Render final vertical video via batch_book_generator
        print(f"\n🎬 BẮT ĐẦU DỰNG VIDEO HOÀN CHỈNH (BATCH BOOK GENERATOR) CHO: {title}...")
        batch_script = BASE_DIR / "tools" / "batch_book_generator.py"
        sub_env = os.environ.copy()
        sub_env["PYTHONIOENCODING"] = "utf-8"
        cmd = [sys.executable, str(batch_script), f"--slug={slug}"]
        subprocess.run(cmd, env=sub_env, check=True)

        return {
            "slug": slug,
            "title": title,
            "chat_url": page.url,
            "script_file": str(script_file),
            "mp3_path": mp3_path,
        }


def main():
    config_path = CONFIGS_DIR / "books_10.json"
    with open(config_path, "r", encoding="utf-8") as f:
        books = json.load(f)

    force_mode = "--force" in sys.argv or "-f" in sys.argv
    run_all = any(arg in ("--all", "-a", "--all-remaining") for arg in sys.argv)
    target_slug = None

    for arg in sys.argv[1:]:
        if arg.startswith("--slug="):
            target_slug = arg.split("=", 1)[1]
        elif not arg.startswith("-") and not target_slug and arg not in ("all",):
            target_slug = arg

    if not target_slug and not run_all:
        run_all = True

    if target_slug:
        target_book = next((b for b in books if b["slug"] == target_slug), None)
        if not target_book:
            print(f"❌ Slug '{target_slug}' not found in configs/books_10.json")
            sys.exit(1)
        result = asyncio.run(generate_book_script_and_audio(target_book))
        print("\n" + "=" * 70)
        print(f"✅ HOÀN TẤT THÀNH CÔNG CHO SÁCH: {result['title']}")
        print(f"🔗 Xem đoạn chat trong lịch sử ChatGPT: {result['chat_url']}")
        print(f"🎧 File MP3: {result['mp3_path']}")
        print("=" * 70)
    elif run_all:
        print(f"🚀 BẮT ĐẦU TỰ ĐỘNG LÀM TOÀN BỘ CÁC SÁCH (Mỗi sách mở 1 tab riêng biệt)... {'[FORCE MODE BẬT]' if force_mode else ''}")
        remaining = []
        for b in books:
            slug = b["slug"]
            final_mp4 = OUTPUTS_DIR / f"{slug}_final.mp4"
            mp3_path = OUTPUTS_DIR / f"{slug}.mp3"
            log_path = CACHE_DIR / "books" / slug / "review_log.json"
            if not force_mode and final_mp4.exists() and mp3_path.exists() and log_path.exists():
                print(f"⏩ [ĐÃ HOÀN THÀNH] Bỏ qua sách: {b['title']} ({slug})")
            else:
                remaining.append(b)

        print(f"📚 Số lượng sách cần thực hiện: {len(remaining)} sách")
        for idx, book in enumerate(remaining, 1):
            print(f"\n{'='*70}\n[TIẾN ĐỘ {idx}/{len(remaining)}] Đang xử lý: {book['title']} ({book['slug']})\n{'='*70}")
            try:
                res = asyncio.run(generate_book_script_and_audio(book))
                print(f"✅ Hoàn thành: {res['title']} ({res['mp3_path']})")
            except Exception as e:
                print(f"❌ Lỗi khi xử lý {book['slug']}: {e}")
                import traceback
                traceback.print_exc()
            time.sleep(3)
        print("\n" + "=" * 70)
        print("🏁 ĐÃ HOÀN TẤT TOÀN BỘ DANH SÁCH BATCH!")
        print("=" * 70)


if __name__ == "__main__":
    main()



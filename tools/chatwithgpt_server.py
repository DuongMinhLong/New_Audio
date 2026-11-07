"""
MCP Server: chatwithgpt
Provides Model Context Protocol (MCP) tools for Cline to chat directly with ChatGPT.
Supports:
1. Web Mode (Chrome CDP): Uses active/logged-in ChatGPT session on Chrome port 9222 (supports Reasoning mode, zero API cost).
2. API Mode (Local 9Router): Fast fallback via local router (port 20128).
"""

import os
import sys
import json
import time
import shutil
import asyncio
import urllib.request
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

# Force UTF-8 encoding on standard streams to avoid charmap errors on Windows
if sys.platform == "win32":
    import io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "buffer"):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from mcp.server.mcpserver import MCPServer
from playwright.async_api import async_playwright, BrowserContext, Page, Response

# --- Configuration ---
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CDP_PORT = 9222
CDP_ENDPOINT = f"http://127.0.0.1:{CDP_PORT}"
CHATGPT_URL = "https://chatgpt.com"

# Directories
WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(WORKSPACE_DIR, "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# Default profile used for automation
GFLOW_BASE_DIR = os.path.expandvars(r"%LocalAppData%\ffroliva\gflow-cli")
DEFAULT_PROFILE = os.path.join(GFLOW_BASE_DIR, "profile_duongminhlong91")
if not os.path.exists(DEFAULT_PROFILE):
    DEFAULT_PROFILE = os.path.expandvars(r"%LocalAppData%\Google\Chrome\User Data")

ROUTER_URL = "http://localhost:20128/v1/chat/completions"
ROUTER_API_KEY = "sk-5c7dfe21074e800a-vsdmte-b6429d79"
DEFAULT_ROUTER_MODEL = "ag/gemini-3.8-flash-high"

app = MCPServer("chatwithgpt")

# --- FFmpeg & Audio Helpers ---

def get_ffmpeg_path() -> Optional[str]:
    """Locate ffmpeg executable on Windows."""
    found = shutil.which("ffmpeg")
    if found:
        return found
    candidates = [
        r"C:\Users\Windows\AppData\Local\Programs\Python\Python312\Scripts\ffmpeg.exe",
        os.path.expandvars(r"%LocalAppData%\Programs\Python\Python312\Scripts\ffmpeg.exe"),
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def convert_aac_to_mp3(aac_path: str, mp3_path: str) -> bool:
    """Convert an AAC file to standard MP3 using ffmpeg."""
    ffmpeg_bin = get_ffmpeg_path()
    if not ffmpeg_bin:
        return False
    try:
        cmd = [
            ffmpeg_bin,
            "-y",
            "-i", aac_path,
            "-c:a", "libmp3lame",
            "-q:a", "2",
            mp3_path
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        return proc.returncode == 0 and os.path.exists(mp3_path)
    except Exception:
        return False

# --- CDP Helpers ---

def is_cdp_available(timeout: float = 1.5) -> bool:
    try:
        req = urllib.request.Request(f"{CDP_ENDPOINT}/json/version", headers={"User-Agent": "MCP-ChatWithGPT"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                return bool(data.get("webSocketDebuggerUrl"))
    except Exception:
        return False
    return False

def launch_chrome_cdp(force_restart: bool = False) -> bool:
    if is_cdp_available():
        return True

    if not os.path.exists(CHROME_PATH):
        return False

    os.makedirs(DEFAULT_PROFILE, exist_ok=True)
    args = [
        CHROME_PATH,
        f"--user-data-dir={DEFAULT_PROFILE}",
        f"--remote-debugging-port={CDP_PORT}",
        "--no-first-run",
        "--no-default-browser-check",
        CHATGPT_URL
    ]

    subprocess.Popen(args, close_fds=True)
    for _ in range(25):
        time.sleep(0.5)
        if is_cdp_available():
            return True
    return is_cdp_available()

async def get_or_create_chatgpt_page(context: BrowserContext) -> Page:
    for page in context.pages:
        try:
            if "chatgpt.com" in page.url.lower():
                return page
        except Exception:
            continue
    page = await context.new_page()
    await page.goto(CHATGPT_URL, wait_until="domcontentloaded", timeout=45000)
    await asyncio.sleep(2.0)
    return page

INPUT_SELECTORS = [
    "#prompt-textarea",
    "div[contenteditable='true']",
    "textarea[data-id='root']",
    "textarea",
]

SEND_SELECTORS = [
    "button[data-testid='send-button']",
    "button[aria-label*='Send prompt']",
    "button[aria-label*='Send']",
    "button[aria-label*='Gửi']",
    "button:has(svg[viewBox*='24'])",
    "button:has(svg[viewBox*='20'])",
]

STOP_SELECTORS = [
    "button[data-testid='stop-button']",
    "button[aria-label*='Stop']",
    "button[aria-label*='Dừng']",
    "button:has(svg rect)",
    "button[data-composer-navigation-target='stop']",
]

RESPONSE_SELECTORS = [
    "[data-dil-message-id]",
    "[class*='DilResponseRoot']",
    "[data-message-author-role='assistant'] .markdown",
    "[data-markdown-text-style]",
    "[data-chatgpt-copy-reference]",
    "[class*='MarkdownRoot']",
    "[data-message-author-role='assistant']",
    "article:has([data-message-author-role='assistant'])",
]

READ_ALOUD_SELECTORS = [
    "button[aria-label='Đọc to']",
    "button[aria-label='Read aloud']",
    "button[aria-label*='Đọc']",
    "button[aria-label*='Read']",
]

async def _extract_latest_response(page: Page) -> str:
    for selector in RESPONSE_SELECTORS:
        nodes = await page.query_selector_all(selector)
        if nodes:
            last_node = nodes[-1]
            text = await last_node.inner_text()
            if text and len(text.strip()) > 10:
                return text.strip()
    return ""

async def _find_input_element(page: Page):
    for sel in INPUT_SELECTORS:
        try:
            el = await page.query_selector(sel)
            if el and await el.is_visible():
                return el
        except Exception:
            continue
    return None

async def _dismiss_modals(page: Page):
    """Dismiss any comparison modals, banners or overlays if present."""
    for skip_sel in ["button:has-text('Bỏ qua')", "button:has-text('Skip')", "button:has-text('Dismiss')", "button[aria-label*='Close']"]:
        try:
            skip_btn = await page.query_selector(skip_sel)
            if skip_btn and await skip_btn.is_visible():
                await skip_btn.click(timeout=1500)
                await asyncio.sleep(0.5)
        except Exception:
            pass

async def _submit_prompt(page: Page, prompt: str):
    await _dismiss_modals(page)
    input_el = await _find_input_element(page)
    if not input_el:
        raise RuntimeError("ChatGPT input textarea not found. Please ensure ChatGPT is logged in.")

    try:
        await input_el.click(timeout=3000)
    except Exception:
        try:
            await input_el.focus()
        except Exception:
            pass
    await asyncio.sleep(0.3)

    success = await page.evaluate("""(text) => {
        const input = document.querySelector('#prompt-textarea') || document.querySelector('div[contenteditable="true"]') || document.querySelector('textarea');
        if (!input) return false;
        if (input.tagName === 'TEXTAREA') {
            input.value = text;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            return true;
        } else if (input.isContentEditable) {
            input.focus();
            document.execCommand('insertText', false, text);
            return true;
        }
        return false;
    }""", prompt)

    if not success:
        await page.keyboard.insert_text(prompt)

    await asyncio.sleep(0.8)

    sent = False
    for send_sel in SEND_SELECTORS:
        try:
            btn = await page.query_selector(send_sel)
            if btn and await btn.is_enabled():
                await btn.click(force=True, timeout=3000)
                sent = True
                break
        except Exception:
            pass

    if not sent:
        await page.keyboard.press("Enter")

async def _wait_for_generation_finish(page: Page, timeout: int = 150) -> str:
    start_time = time.time()
    await asyncio.sleep(3.0)

    prev_len = 0
    stable_count = 0
    while time.time() - start_time < timeout:
        is_generating = False
        for stop_sel in STOP_SELECTORS:
            stop_btn = await page.query_selector(stop_sel)
            if stop_btn and await stop_btn.is_visible():
                is_generating = True
                break

        curr_text = await _extract_latest_response(page)
        curr_len = len(curr_text)

        if not is_generating and curr_len > 20:
            if curr_len == prev_len:
                stable_count += 1
                if stable_count >= 2:
                    return curr_text
            else:
                stable_count = 0
                prev_len = curr_len
        await asyncio.sleep(1.5)

    curr_text = await _extract_latest_response(page)
    if curr_text:
        return curr_text
    raise TimeoutError(f"ChatGPT did not finish generating response within {timeout}s.")

async def _capture_read_aloud_audio(page: Page, timeout: int = 40, mute_speaker: bool = True) -> bytes:
    """
    Trigger the Read Aloud button and capture the streamed AAC audio bytes.
    Optionally mutes audio playback so it operates silently in the background.
    """
    captured_data = []
    capture_event = asyncio.Event()

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
        if mute_speaker:
            await page.evaluate("""() => {
                document.querySelectorAll('audio').forEach(a => { a.muted = true; a.volume = 0; });
            }""")

        read_btns = []
        for sel in READ_ALOUD_SELECTORS:
            nodes = await page.query_selector_all(sel)
            if nodes:
                read_btns.extend(nodes)

        if not read_btns:
            raise RuntimeError("Read Aloud ('Đọc to') button not found in ChatGPT UI.")

        target_btn = read_btns[-1]
        await target_btn.scroll_into_view_if_needed()
        await asyncio.sleep(0.5)
        await target_btn.click()

        try:
            await asyncio.wait_for(capture_event.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            raise TimeoutError("Timeout waiting for ChatGPT synthesized audio response.")

    finally:
        page.remove_listener("response", on_response)
        try:
            stop_btn = await page.query_selector("button[aria-label*='Dừng'], button[aria-label*='Stop'], button[data-testid*='stop']")
            if stop_btn and await stop_btn.is_visible():
                await stop_btn.click()
            else:
                for sel in READ_ALOUD_SELECTORS:
                    btns = await page.query_selector_all(sel)
                    if btns:
                        await btns[-1].click()
                        break
        except Exception:
            pass

    if captured_data:
        return captured_data[0]
    raise RuntimeError("No audio data could be captured from the Read Aloud stream.")

async def _save_captured_audio(audio_bytes: bytes, output_name: str = "", convert_to_mp3_format: bool = True) -> Tuple[str, Optional[str]]:
    """Save audio bytes to outputs folder and optionally convert to MP3."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if output_name:
        base_name = Path(output_name).stem
        clean_name = "".join([c if c.isalnum() or c in ("-", "_") else "_" for c in base_name]).strip("_")
        if not clean_name:
            clean_name = f"chatgpt_{timestamp}"
    else:
        clean_name = f"chatgpt_voice_{timestamp}"

    aac_filename = f"{clean_name}.aac"
    aac_path = os.path.join(OUTPUTS_DIR, aac_filename)

    with open(aac_path, "wb") as f:
        f.write(audio_bytes)

    mp3_path = None
    if convert_to_mp3_format:
        mp3_filename = f"{clean_name}.mp3"
        candidate_mp3 = os.path.join(OUTPUTS_DIR, mp3_filename)
        if convert_aac_to_mp3(aac_path, candidate_mp3):
            mp3_path = candidate_mp3

    return aac_path, mp3_path

async def _send_chatgpt_web(prompt: str, timeout: int = 150) -> str:
    if not is_cdp_available():
        launched = launch_chrome_cdp()
        if not launched:
            raise RuntimeError("Chrome CDP (port 9222) is not accessible and could not be launched.")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_ENDPOINT)
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await get_or_create_chatgpt_page(context)
        await asyncio.sleep(1.0)

        await _submit_prompt(page, prompt)
        return await _wait_for_generation_finish(page, timeout=timeout)

def _call_local_router(prompt: str, model: str = DEFAULT_ROUTER_MODEL, timeout: int = 120) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ROUTER_API_KEY}"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "stream": False
    }
    req = urllib.request.Request(ROUTER_URL, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        content = res["choices"][0]["message"]["content"]
        # Filter think tags if present
        import re
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
        return content


# --- MCP Tools ---

@app.tool()
async def chat_with_gpt(prompt: str, mode: str = "web", model_override: str = "", timeout: int = 150) -> str:
    """
    Send a prompt to ChatGPT and retrieve the complete response.
    Args:
        prompt: The query or instruction to send to ChatGPT.
        mode: 'web' (default, uses active ChatGPT web session via Chrome CDP) or 'api' (uses local 9Router port 20128).
        model_override: Specific model ID when using mode='api' (e.g. 'ag/claude-sonnet-5-5-high', 'oc/big-pickle', 'ag/gemini-3.8-flash-high').
        timeout: Maximum seconds to wait for generation.
    """
    if mode.lower() == "web":
        try:
            return await _send_chatgpt_web(prompt, timeout=timeout)
        except Exception as e:
            # Fallback to local router if available
            try:
                fallback_res = _call_local_router(prompt, model=model_override or DEFAULT_ROUTER_MODEL, timeout=60)
                return f"⚠️ [Notice: Web session failed ({e}), returned response via local router]:\n\n{fallback_res}"
            except Exception:
                return f"❌ ChatGPT Web Error: {e}"
    else:
        try:
            return _call_local_router(prompt, model=model_override or DEFAULT_ROUTER_MODEL, timeout=timeout)
        except Exception as e:
            return f"❌ Local Router API Error: {e}"

@app.tool()
async def chat_and_get_audio(prompt: str, output_name: str = "", convert_to_mp3: bool = True, timeout: int = 180) -> str:
    """
    100% AUTOMATED: Send a prompt to ChatGPT, generate response, and automatically capture Read Aloud (Đọc to) audio.
    Saves the native audio stream (.aac) and converts it to high-quality .mp3 via ffmpeg.
    Args:
        prompt: The query/prompt to send to ChatGPT.
        output_name: Optional desired filename (without extension, e.g. 'vietnam_capital').
        convert_to_mp3: Whether to automatically convert AAC to MP3 using ffmpeg (default True).
        timeout: Max seconds to wait for text generation + audio synthesis.
    """
    if not is_cdp_available():
        launch_chrome_cdp()

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_ENDPOINT)
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await get_or_create_chatgpt_page(context)
        await asyncio.sleep(0.5)

        # Always navigate to clean new chat to prevent DOM lag, scroll issues, or modal popups
        try:
            current_url = page.url.lower().rstrip("/")
            if "/c/" in current_url or current_url != "https://chatgpt.com":
                await page.goto("https://chatgpt.com/", timeout=15000, wait_until="domcontentloaded")
                await asyncio.sleep(1.5)
        except Exception:
            pass

        # 1. Send prompt & wait for text
        await _submit_prompt(page, prompt)
        text_response = await _wait_for_generation_finish(page, timeout=timeout - 40)
        await asyncio.sleep(1.5)

        # 2. Trigger Read Aloud & capture audio stream
        audio_bytes = await _capture_read_aloud_audio(page, timeout=40, mute_speaker=True)

        # 3. Save files
        aac_path, mp3_path = await _save_captured_audio(audio_bytes, output_name=output_name, convert_to_mp3_format=convert_to_mp3)

        size_kb = len(audio_bytes) / 1024
        result_lines = [
            "### 🎙️ ChatGPT Audio Được Tạo Tự Động Thành Công!\n",
            f"**Văn bản phản hồi:**\n> {text_response}\n",
            f"- **File âm thanh gốc (AAC)**: `{aac_path}` ({size_kb:.1f} KB)",
        ]
        if mp3_path:
            mp3_size_kb = os.path.getsize(mp3_path) / 1024
            result_lines.append(f"- **File MP3 chuẩn phòng thu**: `{mp3_path}` ({mp3_size_kb:.1f} KB)")
        else:
            result_lines.append("- *Lưu ý: Không tìm thấy ffmpeg để convert sang MP3, file gốc AAC đã sẵn sàng sử dụng.*")

        result_lines.append("\n✅ *File audio đã được lưu an toàn trong thư mục `outputs/`.*")
        return "\n".join(result_lines)

@app.tool()
async def text_to_audio(text: str, output_name: str = "", convert_to_mp3: bool = True, timeout: int = 180) -> str:
    """
    100% AUTOMATED: Convert an EXACT custom text to ChatGPT's Read Aloud voice.
    Instructs ChatGPT to repeat the text verbatim, then immediately captures the synthesized speech audio.
    Args:
        text: The exact Vietnamese or English text to read aloud.
        output_name: Optional desired filename (without extension).
        convert_to_mp3: Whether to automatically convert AAC to MP3 using ffmpeg (default True).
        timeout: Max seconds to wait.
    """
    strict_prompt = f"Hãy chép lại chính xác nguyên văn câu sau đây vào phản hồi của bạn, không thêm bớt bất kỳ từ ngữ, phiên âm IPA, lời dẫn hay giải thích nào khác:\n\n{text.strip()}"
    return await chat_and_get_audio(strict_prompt, output_name=output_name, convert_to_mp3=convert_to_mp3, timeout=timeout)

@app.tool()
async def get_last_response_audio(output_name: str = "", convert_to_mp3: bool = True, timeout: int = 40) -> str:
    """
    Capture Read Aloud audio of whatever response is CURRENTLY latest on your active ChatGPT tab.
    Does NOT send a new prompt - immediately clicks 'Đọc to' on the latest response and grabs the audio.
    Args:
        output_name: Optional desired filename.
        convert_to_mp3: Whether to convert AAC to MP3 (default True).
        timeout: Max seconds to wait for audio capture.
    """
    if not is_cdp_available():
        launch_chrome_cdp()

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_ENDPOINT)
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await get_or_create_chatgpt_page(context)
        await asyncio.sleep(0.5)

        latest_text = await _extract_latest_response(page)
        audio_bytes = await _capture_read_aloud_audio(page, timeout=timeout, mute_speaker=True)
        aac_path, mp3_path = await _save_captured_audio(audio_bytes, output_name=output_name, convert_to_mp3_format=convert_to_mp3)

        size_kb = len(audio_bytes) / 1024
        result_lines = [
            "### 🎙️ Đã Bắt Audio Câu Trả Lời Mới Nhất Trên ChatGPT!\n",
            f"**Đoạn trích:**\n> {latest_text[:200]}...\n" if latest_text else "",
            f"- **File âm thanh gốc (AAC)**: `{aac_path}` ({size_kb:.1f} KB)",
        ]
        if mp3_path:
            mp3_size_kb = os.path.getsize(mp3_path) / 1024
            result_lines.append(f"- **File MP3 chuẩn phòng thu**: `{mp3_path}` ({mp3_size_kb:.1f} KB)")

        return "\n".join(result_lines)

@app.tool()
async def chatgpt_status() -> str:
    """
    Check the connection status of ChatGPT (Chrome CDP port 9222 and Local 9Router port 20128) and FFmpeg.
    """
    cdp_online = is_cdp_available()
    router_online = False
    try:
        req = urllib.request.Request("http://127.0.0.1:20128/v1/models", headers={"User-Agent": "MCP-Test"})
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            router_online = resp.status == 200
    except Exception:
        router_online = False

    ffmpeg_bin = get_ffmpeg_path()

    lines = [
        "### 🤖 MCP ChatWithGPT & Audio Status Report\n",
        f"- **Chrome CDP (Port 9222 - Web ChatGPT)**: {'🟢 ONLINE' if cdp_online else '🔴 OFFLINE'}",
        f"- **FFmpeg Converter**: {'🟢 ONLINE (' + ffmpeg_bin + ')' if ffmpeg_bin else '🟡 KHÔNG TÌM THẤY (Chỉ lưu file AAC)'}",
        f"- **Local 9Router (Port 20128 - API Fallback)**: {'🟢 ONLINE' if router_online else '🔴 OFFLINE'}",
        f"- **Outputs Directory**: `{OUTPUTS_DIR}`",
        f"- **Profile Directory**: `{DEFAULT_PROFILE}`",
        "\n*Note: Chrome CDP is ready to generate and capture Read Aloud audio automatically.*"
    ]
    return "\n".join(lines)

@app.tool()
async def chatgpt_launch() -> str:
    """
    Launch or restart Google Chrome with CDP port 9222 and ChatGPT tab open.
    """
    success = launch_chrome_cdp()
    if success:
        return "✅ Chrome CDP launched successfully on port 9222 with ChatGPT ready."
    return "❌ Failed to launch Chrome with CDP port 9222. Please verify Chrome path."

@app.tool()
async def chatgpt_new_chat() -> str:
    """
    Navigate the ChatGPT tab to a clean new chat session (https://chatgpt.com/).
    """
    if not is_cdp_available():
        launch_chrome_cdp()

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_ENDPOINT)
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await get_or_create_chatgpt_page(context)
        await page.goto(CHATGPT_URL, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(2.0)
        return "✅ ChatGPT tab navigated to new conversation."

# --- CLI Diagnostics ---

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--status":
        print(asyncio.run(chatgpt_status()))
    elif len(sys.argv) > 1 and sys.argv[1] == "--launch":
        print(asyncio.run(chatgpt_launch()))
    elif len(sys.argv) > 1 and sys.argv[1] == "--test":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "Chào bạn, hãy trả lời ngắn gọn: 1 + 1 = mấy?"
        print(f"Testing chat_with_gpt: '{prompt}'...")
        res = asyncio.run(chat_with_gpt(prompt))
        print("Response:\n", res)
    elif len(sys.argv) > 1 and sys.argv[1] == "--audio":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "Thủ đô của Việt Nam là Hà Nội."
        output_name = sys.argv[3] if len(sys.argv) > 3 else "test_cli"
        print(f"Generating audio for: '{prompt}'...")
        res = asyncio.run(text_to_audio(prompt, output_name=output_name))
        print(res)
    elif len(sys.argv) > 1 and sys.argv[1] == "--audio-file":
        txt_path = sys.argv[2]
        output_name = sys.argv[3] if len(sys.argv) > 3 else "test_file_audio"
        with open(txt_path, "r", encoding="utf-8") as f:
            prompt = f.read()
        print(f"Generating audio from file '{txt_path}' ({len(prompt)} chars)...")
        res = asyncio.run(text_to_audio(prompt, output_name=output_name))
        print(res)

    elif len(sys.argv) > 1 and sys.argv[1] == "--get-last-audio":
        output_name = sys.argv[2] if len(sys.argv) > 2 else "latest_response"
        print("Capturing last response audio...")
        res = asyncio.run(get_last_response_audio(output_name=output_name))
        print(res)
    else:
        app.run(transport="stdio")


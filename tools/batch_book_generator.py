#!/usr/bin/env python3
"""
batch_book_generator.py - Automated End-to-End Video Production for Book Summaries
"""

import os
import sys
import json
import re
import asyncio
import subprocess
import shutil
import urllib.request
import urllib.parse
from pathlib import Path
from typing import List, Dict, Tuple, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
# Force UTF-8 encoding on standard streams to avoid charmap errors on Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

CONFIGS_DIR = BASE_DIR / "configs"
CACHE_ROOT = BASE_DIR / "cache" / "books"
ASSETS_DIR = BASE_DIR / "assets"
BGM_FILE = ASSETS_DIR / "bg_music.mp3"

OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
CACHE_ROOT.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

FFMPEG_BIN = r"C:\Users\Windows\AppData\Local\Programs\Python\Python312\Scripts\ffmpeg.exe"
if not os.path.exists(FFMPEG_BIN):
    FFMPEG_BIN = shutil.which("ffmpeg") or "ffmpeg"


def get_pexels_api_key() -> str:
    env_key = os.getenv("PEXELS_API_KEY")
    if env_key:
        return env_key
    candidates = [
        Path(r"C:\Long_YT\.env"),
        Path(r"C:\AI_2D_videos\.env"),
        BASE_DIR / ".env",
    ]
    for env_path in candidates:
        if env_path.exists():
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("PEXELS_API_KEY="):
                            k = line.split("=", 1)[1].strip().strip('"').strip("'")
                            if k:
                                return k
            except Exception:
                pass
    return "tgdzY6rgztHoPEyvXNvJPLax0PONXghUJhZ4er4QjbTx9keP11UmF0Nv"


def get_audio_duration(audio_path: str) -> float:
    cmd = [FFMPEG_BIN, "-i", str(audio_path)]
    proc = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    for line in proc.stderr.split("\n"):
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = parts.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 60.0
def download_pexels_clip(query: str, output_path: str, min_duration: int = 4) -> bool:
    api_key = get_pexels_api_key()
    encoded = urllib.parse.quote(query)
    url = f"https://api.pexels.com/videos/search?query={encoded}&orientation=portrait&per_page=5"

    req = urllib.request.Request(url)
    req.add_header("Authorization", api_key)
    req.add_header("User-Agent", "Mozilla/5.0")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            videos = data.get("videos", [])
            if not videos:
                return False

            candidates = [v for v in videos if v.get("duration", 0) >= min_duration]
            video = candidates[0] if candidates else videos[0]

            mp4_files = [
                f for f in video.get("video_files", [])
                if f.get("file_type") == "video/mp4" and (f.get("height") or 0) >= (f.get("width") or 0)
            ]
            if not mp4_files:
                mp4_files = [f for f in video.get("video_files", []) if f.get("file_type") == "video/mp4"]

            target_1080 = [f for f in mp4_files if f.get("width") == 1080 and f.get("height") == 1920]
            if target_1080:
                chosen = target_1080[0]
            else:
                hd_candidates = [f for f in mp4_files if (f.get("width") or 0) <= 1080]
                if hd_candidates:
                    hd_candidates.sort(key=lambda x: (x.get("width", 0) * x.get("height", 0)), reverse=True)
                    chosen = hd_candidates[0]
                else:
                    mp4_files.sort(key=lambda x: (x.get("width", 0) * x.get("height", 0)))
                    chosen = mp4_files[0]

            dl_url = chosen.get("link")
            dl_req = urllib.request.Request(
                dl_url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            )
            with urllib.request.urlopen(dl_req, timeout=35) as dl_resp, open(output_path, "wb") as out_f:
                shutil.copyfileobj(dl_resp, out_f)
            return True
    except Exception as e:
        print(f"   ❌ Pexels download error: {e}")
        return False


def normalize_shot(raw_video: str, target_dur: float, output_video: str) -> bool:
    vf = (
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,setsar=1,fps=30,"
        "zoompan=z='min(zoom+0.0010,1.07)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,"
        "eq=contrast=1.15:brightness=-0.03:saturation=0.85,"
        "vignette=PI/4"
    )
    cmd = [
        FFMPEG_BIN, "-y",
        "-stream_loop", "-1",
        "-i", str(raw_video),
        "-t", f"{target_dur:.2f}",
        "-vf", vf,
        "-an",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-colorspace", "bt709",
        str(output_video)
    ]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    return res.returncode == 0

def format_srt_time(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis >= 1000:
        secs += 1
        millis -= 1000
    if secs >= 60:
        mins += 1
        secs -= 60
    if mins >= 60:
        hrs += 1
        mins -= 60
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"


def split_script_into_cues(text: str) -> List[str]:
    """Break script into short, natural 4-9 word cues optimized for mobile 9:16 reading."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    cues = []
    for p in paragraphs:
        parts = re.split(r"(?<=[.!?…—])\s+", p)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            subparts = re.split(r"(?<=\.\.\.)\s+", part)
            for sp in subparts:
                sp = sp.strip()
                if not sp:
                    continue
                if len(sp) > 42 and "," in sp:
                    comma_parts = re.split(r"(?<=,)\s+", sp)
                    cues.extend([cp.strip() for cp in comma_parts if cp.strip()])
                else:
                    cues.append(sp)
    return cues


def generate_accurate_subtitles(audio_path: str, script_text: str, srt_path: Path) -> bool:
    """Generate millisecond-accurate SRT matching Whisper speech timestamps to original script."""
    import numpy as np
    from faster_whisper import WhisperModel

    print("   🎙️ Transcribing with Faster-Whisper (int8) for frame-accurate timing...")
    cmd = [FFMPEG_BIN, "-i", str(audio_path), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True)
    audio_data = np.frombuffer(proc.stdout, np.float32)

    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_data, language="vi", vad_filter=True, word_timestamps=True)

    whisper_words = []
    for s in segments:
        for w in s.words:
            whisper_words.append({"word": w.word.strip(), "start": w.start, "end": w.end})

    if not whisper_words:
        print("   ⚠️ No words detected in speech audio.")
        return False

    cues = split_script_into_cues(script_text)
    tot_script_words = sum(len(c.split()) for c in cues)
    tot_whisper_words = len(whisper_words)
    ratio = tot_whisper_words / max(1, tot_script_words)

    entries = []
    w_curr = 0.0
    for idx, cue in enumerate(cues, 1):
        n_w = len(cue.split())
        s_idx = int(round(w_curr))
        e_idx = min(int(round(w_curr + n_w * ratio)) - 1, tot_whisper_words - 1)
        s_idx = min(s_idx, tot_whisper_words - 1)
        if e_idx < s_idx:
            e_idx = s_idx

        start_time = whisper_words[s_idx]["start"]
        end_time = whisper_words[e_idx]["end"]
        if end_time <= start_time:
            end_time = start_time + 1.2
        w_curr += n_w * ratio

        # Format line: break if cue > 32 chars
        display_cue = cue
        if len(display_cue) > 32 and " " in display_cue:
            mid = len(display_cue) // 2
            split_at = display_cue.rfind(" ", 0, mid + 6)
            if split_at != -1:
                display_cue = display_cue[:split_at] + "\n" + display_cue[split_at + 1:]

        entries.append((start_time, end_time, display_cue))

    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, (s, e, text) in enumerate(entries, 1):
            f.write(f"{idx}\n{format_srt_time(s)} --> {format_srt_time(e)}\n{text}\n\n")

    print(f"   ✅ Created {len(entries)} subtitle cues with 0.00s drift -> {srt_path.name}")
    return True

def process_single_book(book: Dict, force_tts: bool = False) -> Optional[str]:
    slug = book["slug"]
    title = book["title"]
    script = book.get("script", "")
    scenes = book.get("scenes")
    if not scenes:
        from tools.build_all_remaining_configs import get_preset_scenes
        scenes = get_preset_scenes(book.get("category", ""))

    book_cache = CACHE_ROOT / slug
    book_cache.mkdir(parents=True, exist_ok=True)

    audio_path = OUTPUTS_DIR / f"{slug}.mp3"
    if not audio_path.exists() and (book_cache / "audio.mp3").exists():
        audio_path = book_cache / "audio.mp3"
    final_output = OUTPUTS_DIR / f"{slug}_final.mp4"

    if final_output.exists() and not force_tts:
        size_mb = final_output.stat().st_size / (1024 * 1024)
        print(f"⏩ Video already exists: {final_output.name} ({size_mb:.2f} MB). Skipping.")
        return str(final_output)

    print(f"\n" + "=" * 60)
    print(f"📖 PROCESSING: {title} ({slug})")
    print("=" * 60)

    # 1. AUDIO GENERATION
    if not audio_path.exists() or force_tts:
        print(f"🎙️ Generating Expressive Read Aloud Audio for '{slug}'...")
        script_file = book_cache / "script.txt"
        with open(script_file, "w", encoding="utf-8") as sf:
            sf.write(script)
        server_py = BASE_DIR / "tools" / "chatwithgpt_server.py"
        sub_env = os.environ.copy()
        sub_env["PYTHONIOENCODING"] = "utf-8"
        cmd = [sys.executable, str(server_py), "--audio-file", str(script_file), slug]
        p = subprocess.run(cmd, env=sub_env, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        if not audio_path.exists():
            print(f"❌ Failed to generate TTS audio for {slug}!\nOutput:\n{p.stdout}\n{p.stderr}")
            return None
        print(f"✅ TTS Audio generated: {audio_path.name}")
    else:
        print(f"🎵 Using existing TTS audio: {audio_path.name}")

    total_dur = get_audio_duration(str(audio_path))
    print(f"⏱️ Audio duration: {total_dur:.2f}s")

    # 2. SUBTITLE GENERATION
    srt_path = book_cache / "subtitles.srt"
    if not srt_path.exists():
        ok = generate_accurate_subtitles(str(audio_path), script, srt_path)
        if not ok:
            print("❌ Subtitle generation failed!")
            return None
    else:
        print(f"📝 Using cached subtitles: {srt_path.name}")

    # 3. PEXELS B-ROLL & NORMALIZATION
    num_scenes = len(scenes)
    each_dur = total_dur / num_scenes
    for sc in scenes:
        sc["target_dur"] = each_dur

    norm_clips = []
    for idx, sc in enumerate(scenes):
        query = sc["query"]
        dur = sc["target_dur"]
        raw_clip = book_cache / f"raw_shot_{idx + 1}.mp4"
        norm_clip = book_cache / f"norm_shot_{idx + 1}.mp4"

        print(f"🎬 Scene {idx + 1}/{num_scenes}: '{query}' ({dur:.1f}s)")
        if not raw_clip.exists():
            ok = download_pexels_clip(query, str(raw_clip), min_duration=3)
            if not ok:
                download_pexels_clip("dark cinematic mystery", str(raw_clip), min_duration=2)

        if not norm_clip.exists():
            print(f"   ⚙️ Normalizing Shot {idx + 1} (1080x1920, Color Grade, Vignette)...")
            normalize_shot(str(raw_clip), dur, str(norm_clip))

        norm_clips.append(str(norm_clip))

    # 4. CONCAT VISUALS
    concat_txt = book_cache / "concat_list.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for nc in norm_clips:
            safe_p = Path(nc).resolve().as_posix()
            f.write(f"file '{safe_p}'\n")

    combined_visual = book_cache / "combined_visuals.mp4"
    print("🎞️ Concatenating visual stream...")
    concat_cmd = [
        FFMPEG_BIN, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(combined_visual)
    ]
    subprocess.run(concat_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    # 5. FINAL ASSEMBLY (Visuals + Subtitles + Speech + BGM)
    sub_style = (
        "subtitles=subtitles.srt:force_style='FontName=Segoe UI Black,"
        "FontSize=20,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,"
        "BorderStyle=1,Outline=2.8,Shadow=1.5,Alignment=2,MarginV=90'"
    )

    print(f"🔊 Merging Audio (Loudnorm -14 LUFS) + BGM + Subtitles into {final_output.name}...")
    if BGM_FILE.exists():
        final_cmd = [
            FFMPEG_BIN, "-y",
            "-i", str(combined_visual),
            "-i", str(audio_path),
            "-stream_loop", "-1",
            "-i", str(BGM_FILE),
            "-filter_complex",
            (
                f"[0:v]{sub_style}[vout];"
                "[1:a]loudnorm=I=-14:TP=-1.5:LRA=7,aformat=sample_rates=44100:channel_layouts=stereo[voice];"
                "[2:a]volume=0.18,aformat=sample_rates=44100:channel_layouts=stereo[bgm];"
                "[voice][bgm]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]"
            ),
            "-map", "[vout]",
            "-map", "[aout]",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "20",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(final_output)
        ]
    else:
        final_cmd = [
            FFMPEG_BIN, "-y",
            "-i", str(combined_visual),
            "-i", str(audio_path),
            "-filter_complex",
            (
                f"[0:v]{sub_style}[vout];"
                "[1:a]loudnorm=I=-14:TP=-1.5:LRA=7,aformat=sample_rates=44100:channel_layouts=stereo[aout]"
            ),
            "-map", "[vout]",
            "-map", "[aout]",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "20",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(final_output)
        ]

    subprocess.run(final_cmd, cwd=str(book_cache), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    if final_output.exists():
        # Keep book_cache / "audio.mp3" safe, clean temporary audio in outputs/
        raw_out_mp3 = OUTPUTS_DIR / f"{slug}.mp3"
        raw_out_aac = OUTPUTS_DIR / f"{slug}.aac"
        if raw_out_mp3.exists():
            if not (book_cache / "audio.mp3").exists():
                try:
                    shutil.copy2(raw_out_mp3, book_cache / "audio.mp3")
                except Exception:
                    pass
            try:
                raw_out_mp3.unlink()
            except Exception:
                pass
        if raw_out_aac.exists():
            try:
                raw_out_aac.unlink()
            except Exception:
                pass

        size_mb = final_output.stat().st_size / (1024 * 1024)
        print(f"🎉 SUCCEEDED: {final_output.name} ({size_mb:.2f} MB)")
        return str(final_output)
    return None


def main():
    config_file = CONFIGS_DIR / "books_multi_series_pilot.json"
    
    # Check if a custom config file is passed via --config
    args = sys.argv[1:]
    target_slug = None
    
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith("--config="):
            custom_cfg = Path(arg.split("=", 1)[1])
            config_file = custom_cfg if custom_cfg.is_absolute() else (CONFIGS_DIR / custom_cfg.name if (CONFIGS_DIR / custom_cfg.name).exists() else BASE_DIR / custom_cfg)
        elif arg == "--config" and i + 1 < len(args):
            i += 1
            custom_cfg = Path(args[i])
            config_file = custom_cfg if custom_cfg.is_absolute() else (CONFIGS_DIR / custom_cfg.name if (CONFIGS_DIR / custom_cfg.name).exists() else BASE_DIR / custom_cfg)
        elif arg.startswith("--slug="):
            target_slug = arg.split("=", 1)[1]
        elif arg == "--slug" and i + 1 < len(args):
            i += 1
            target_slug = args[i]
        elif arg.isdigit():
            target_slug = arg  # will resolve after loading books
        else:
            target_slug = arg
        i += 1

    if not config_file.exists():
        print(f"❌ Missing config file: {config_file}")
        sys.exit(1)

    with open(config_file, "r", encoding="utf-8") as f:
        books = json.load(f)

    if target_slug and target_slug.isdigit():
        idx = int(target_slug) - 1
        if 0 <= idx < len(books):
            target_slug = books[idx]["slug"]

    to_process = books
    if target_slug:
        to_process = [b for b in books if b["slug"] == target_slug]
        if not to_process:
            print(f"❌ Slug '{target_slug}' not found in {config_file.name}")
            sys.exit(1)

    print(f"🚀 Starting batch generation for {len(to_process)} book(s)...")
    successes = []
    for b in to_process:
        res = process_single_book(b)
        if res:
            successes.append(res)

    print("\n" + "=" * 60)
    print(f"🏁 COMPLETED: {len(successes)}/{len(to_process)} videos rendered successfully!")
    for s in successes:
        print(f"   📹 {s}")
    print("=" * 60)


if __name__ == "__main__":
    main()


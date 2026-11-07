#!/usr/bin/env python3
"""
video_builder.py - Automated Pexels Cinematic B-Roll Downloader & Video Assembler
Generates high-retention 9:16 vertical videos with:
- 12 fast-paced cinematic B-roll shots (4-7s per cut)
- Cinematic color grading (moody contrast + dark vignette)
- Ambient background music (BGM) mixing (-22dB)
- Highlighted on-screen captions / subtitles
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Constants
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
CACHE_DIR = BASE_DIR / "cache" / "pexels"
ASSETS_DIR = BASE_DIR / "assets"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

FFMPEG_BIN = r"C:\Users\Windows\AppData\Local\Programs\Python\Python312\Scripts\ffmpeg.exe"
if not os.path.exists(FFMPEG_BIN):
    FFMPEG_BIN = shutil.which("ffmpeg") or "ffmpeg"


def get_pexels_api_key() -> str:
    """Retrieve Pexels API key from environment or project config files."""
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
    """Get accurate duration of audio file using ffmpeg."""
    cmd = [FFMPEG_BIN, "-i", audio_path]
    proc = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    for line in proc.stderr.split("\n"):
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = parts.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 73.81


def download_pexels_portrait(query: str, output_path: str, min_duration: int = 4) -> bool:
    """Search and download highest quality vertical MP4 from Pexels with min duration filter."""
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
                print(f"⚠️ No Pexels video found for '{query}'")
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
            print(f"📥 Downloading '{query}' ({chosen.get('width')}x{chosen.get('height')}, {video.get('duration')}s)...")

            dl_req = urllib.request.Request(
                dl_url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            )
            with urllib.request.urlopen(dl_req, timeout=30) as dl_resp, open(output_path, "wb") as out_f:
                shutil.copyfileobj(dl_resp, out_f)
            return True
    except Exception as e:
        print(f"❌ Error downloading Pexels video for '{query}': {e}")
        return False


def normalize_scene(raw_video: str, target_duration: float, output_video: str) -> bool:
    """
    Scale & crop to 1080x1920 (9:16 portrait) at 30fps.
    Apply moody cinematic color grade + dark vignette.
    Loop seamlessly if clip is shorter than target_duration.
    """
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
        "-i", raw_video,
        "-t", f"{target_duration:.2f}",
        "-vf", vf,
        "-an",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-colorspace", "bt709",
        output_video
    ]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    return res.returncode == 0


def format_srt_time(seconds: float) -> str:
    """Format seconds into SRT timestamp: 00:01:23,456"""
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


def write_srt_entries(entries: List[Tuple[float, float, str]], srt_path: Path):
    """Write list of (start_sec, end_sec, text) tuples to an SRT file."""
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, (s, e, text) in enumerate(entries, 1):
            f.write(f"{idx}\n{format_srt_time(s)} --> {format_srt_time(e)}\n{text}\n\n")


def transcribe_audio_to_srt(audio_path: str, srt_path: Path) -> bool:
    """
    Auto-transcribe audio using faster-whisper with millisecond timestamp precision.
    """
    try:
        import numpy as np
        from faster_whisper import WhisperModel

        print(f"🎙️ Auto-transcribing audio with Faster-Whisper for frame-perfect subtitles...")
        cmd = [FFMPEG_BIN, "-i", audio_path, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True)
        audio_data = np.frombuffer(proc.stdout, np.float32)

        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(audio_data, language="vi", vad_filter=True)

        entries = []
        for s in segments:
            text = s.text.strip()
            if text:
                # Add newline if text is long (>32 chars)
                if len(text) > 32 and " " in text:
                    mid = len(text) // 2
                    split_idx = text.rfind(" ", 0, mid + 8)
                    if split_idx != -1:
                        text = text[:split_idx] + "\n" + text[split_idx + 1:]
                entries.append((s.start, s.end, text))

        write_srt_entries(entries, srt_path)
        print(f"✅ Generated {len(entries)} synced subtitle cues with Faster-Whisper!")
        return True
    except Exception as e:
        print(f"⚠️ Faster-Whisper auto-transcription failed: {e}")
        return False


def build_final_video(audio_path: str, scenes: List[Dict], output_path: str, timed_subtitles: Optional[List[Tuple[float, float, str]]] = None) -> bool:
    """
    Build complete video:
    1. Downloads & normalizes portrait B-roll clips (color graded + vignette).
    2. Stitches clips together into combined visual stream.
    3. Generates styled Vietnamese subtitles (SRT) perfectly synchronized with speech audio.
    4. Mixes speech audio + background music (BGM -22dB) + subtitles.
    """
    total_audio_dur = get_audio_duration(audio_path)
    print(f"🎵 Audio duration: {total_audio_dur:.2f}s ({audio_path})")

    specified_sum = sum(s["duration"] for s in scenes)
    if specified_sum <= 0:
        each = total_audio_dur / len(scenes)
        for s in scenes:
            s["duration"] = each
    else:
        diff = total_audio_dur - specified_sum
        scenes[-1]["duration"] = max(2.0, scenes[-1]["duration"] + diff)

    norm_clips = []
    for idx, scene in enumerate(scenes):
        q = scene["query"]
        dur = scene["duration"]
        raw_clip = str(CACHE_DIR / f"raw_shot_{idx + 1}.mp4")
        norm_clip = str(CACHE_DIR / f"norm_shot_{idx + 1}.mp4")

        print(f"\n🎬 Shot {idx + 1}/{len(scenes)}: '{q}' (Duration: {dur:.2f}s)")
        if not os.path.exists(raw_clip):
            ok = download_pexels_portrait(q, raw_clip, min_duration=4)
            if not ok:
                download_pexels_portrait("dark cinematic mood", raw_clip, min_duration=2)

        print(f"⚙️ Normalizing Shot {idx + 1} (1080x1920, Color Grade, Vignette)...")
        ok = normalize_scene(raw_clip, dur, norm_clip)
        if not ok:
            print(f"❌ Failed to normalize shot {idx + 1}")
            return False
        norm_clips.append(norm_clip)

    concat_txt = CACHE_DIR / "concat_list.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for nc in norm_clips:
            safe_path = Path(nc).resolve().as_posix()
            f.write(f"file '{safe_path}'\n")

    combined_video = str(CACHE_DIR / "combined_visuals.mp4")
    print("\n🎞️ Concatenating all shots...")
    concat_cmd = [
        FFMPEG_BIN, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        combined_video
    ]
    subprocess.run(concat_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    srt_file = CACHE_DIR / "subtitles.srt"
    if timed_subtitles:
        write_srt_entries(timed_subtitles, srt_file)
        print(f"📝 Applied {len(timed_subtitles)} exact timed subtitles to: {srt_file}")
    elif not srt_file.exists():
        # Fallback to Whisper auto-transcription
        ok = transcribe_audio_to_srt(audio_path, srt_file)
        if not ok:
            # Fallback to scene-based timing if Whisper is unavailable
            cur_time = 0.0
            fallback_entries = []
            for s in scenes:
                dur = s["duration"]
                text = s.get("sub", "")
                if text:
                    fallback_entries.append((cur_time, cur_time + dur - 0.15, text))
                cur_time += dur
            write_srt_entries(fallback_entries, srt_file)

    bgm_file = ASSETS_DIR / "bg_music.mp3"
    sub_style = (
        "subtitles=subtitles.srt:force_style='FontName=Segoe UI Black,"
        "FontSize=20,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,"
        "BorderStyle=1,Outline=2.8,Shadow=1.5,Alignment=2,MarginV=90'"
    )

    print(f"🔊 Merging Audio (Loudnorm -14 LUFS) + BGM + Subtitles into {output_path}...")
    if bgm_file.exists():
        final_cmd = [
            FFMPEG_BIN, "-y",
            "-i", combined_video,
            "-i", audio_path,
            "-stream_loop", "-1",
            "-i", str(bgm_file),
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
            output_path
        ]
    else:
        final_cmd = [
            FFMPEG_BIN, "-y",
            "-i", combined_video,
            "-i", audio_path,
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
            output_path
        ]

    res = subprocess.run(final_cmd, cwd=str(CACHE_DIR), stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"\n✨ ULTRA-CINEMATIC FINAL VIDEO CREATED SUCCESSFULLY!")
        print(f"📁 Path: {output_path} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"❌ Error multiplexing final video: {res.stderr}")
        return False



def build_stoic_default():
    """Build the 10/10 Stoic Video with 12 fast-paced cinematic cuts and frame-accurate subtitles."""
    audio_file = str(OUTPUTS_DIR / "chu_nghia_khac_ky_expressive.mp3")
    if not os.path.exists(audio_file):
        audio_file = str(OUTPUTS_DIR / "chu_nghia_khac_ky.mp3")

    scenes = [
        {"query": "rain drops glass dark", "duration": 6.0},
        {"query": "silhouette of a hooded person walking at night", "duration": 5.8},
        {"query": "depressed sad man sitting head hands dark", "duration": 5.2},
        {"query": "foggy misty dark forest lonely", "duration": 7.5},
        {"query": "lightning storm clouds dark sky", "duration": 8.0},
        {"query": "close-up footage of lighted candle", "duration": 6.0},
        {"query": "antique hourglass with flowing sand", "duration": 5.5},
        {"query": "a man looking out the window night", "duration": 5.0},
        {"query": "ancient roman marble sculpture in museum setting", "duration": 6.5},
        {"query": "ancient statues in istanbul museum exhibit", "duration": 6.0},
        {"query": "a man standing still on a cliff edge", "duration": 6.0},
        {"query": "dramatic ocean waves crashing on rocky shore", "duration": 6.31}
    ]

    stoic_subs = [
        (0.00, 1.44, "Điều tàn nhẫn nhất\ncủa cuộc đời là..."),
        (1.50, 4.66, "Bạn có thể sống tử tế cả một đời,\nrồi vẫn bị phản bội..."),
        (4.80, 5.80, "...như một kẻ ngốc!"),
        (6.56, 8.80, "Tôi từng nghĩ chỉ cần cố gắng đủ nhiều..."),
        (8.80, 11.62, "...đối xử tốt với mọi người,\nmọi chuyện rồi sẽ ổn."),
        (12.30, 13.50, "Tôi nhịn... Tôi chịu đựng..."),
        (14.10, 16.62, "Tôi tự an ủi mình rằng:\nngày mai sẽ khác."),
        (17.14, 19.20, "Nhưng ngày mai đến...\nngười ta vẫn rời đi."),
        (19.80, 21.10, "Công sức vẫn bị phủi bỏ..."),
        (21.40, 23.60, "Và người mất ngủ mỗi đêm...\nvẫn là tôi."),
        (24.58, 27.50, "Chủ nghĩa Khắc Kỷ dạy tôi một bài học\n— lạnh đến tận xương:"),
        (27.50, 29.68, "Đừng chỉ chuẩn bị cho điều tốt đẹp..."),
        (29.96, 32.00, "Hãy tập sống với những điều\nTỒI TỆ NHẤT."),
        (32.66, 34.20, "Hãy tưởng tượng ngày bạn mất việc."),
        (35.20, 36.80, "Người bạn tin tưởng nhất quay lưng..."),
        (37.00, 38.20, "Tài khoản cạn sạch..."),
        (38.60, 39.80, "Không một ai gọi hỏi thăm..."),
        (40.00, 41.30, "Không một ai chìa tay cứu bạn."),
        (42.10, 43.60, "Đừng né tránh những viễn cảnh ấy."),
        (44.10, 45.00, "Nhìn thẳng vào chúng."),
        (45.48, 48.60, "Và tự hỏi:\nNếu tất cả biến mất... tôi còn lại gì?"),
        (49.20, 50.80, "Câu trả lời...\nphải là CHÍNH BẠN!"),
        (51.30, 53.20, "Không phải tiền bạc...\nKhông phải danh tiếng..."),
        (53.36, 55.20, "Cũng không phải sự công nhận\ncủa bất kỳ ai."),
        (55.66, 57.20, "Bạn không thể ngăn người khác phản bội."),
        (58.08, 60.00, "Càng không thể bắt cuộc đời công bằng."),
        (60.50, 63.80, "Bạn chỉ có thể quyết định mình sẽ làm gì...\nkhi mọi thứ sụp đổ."),
        (65.06, 67.00, "Đừng cầu xin cuộc đời nhẹ tay với bạn..."),
        (67.60, 70.90, "Hãy trở thành người mà ngay cả khi\nsố phận cướp đi tất cả..."),
        (71.20, 73.00, "Nó... vẫn không thể cướp mất\nCHÍNH BẠN!")
    ]

    output_file = str(OUTPUTS_DIR / "chu_nghia_khac_ky_final.mp4")
    return build_final_video(audio_file, scenes, output_file, timed_subtitles=stoic_subs)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Pexels Video Assembler")
    parser.add_argument("--audio", help="Path to audio file", default=None)
    parser.add_argument("--output", help="Path to output mp4 file", default=None)
    args = parser.parse_args()

    if args.audio and args.output:
        build_final_video(args.audio, [], args.output)
    else:
        build_stoic_default()


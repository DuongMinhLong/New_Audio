#!/usr/bin/env python3
"""
tools/longform_video_builder.py
===============================
Automated Landscape (16:9 1920x1080) Video Builder for YouTube Long-Form.
Features:
  - Curated Cinematic 16:9 B-Roll Download & Cache from Pexels API
  - Color Grading (Atmospheric Moody Contrast + Vignette)
  - Frame-perfect Subtitle Generation via Faster-Whisper (CPU int8)
  - Professional Audio Mixing: Voice (-14 LUFS) + BGM (-26dB)
  - 1080p 30fps Full HD Final Render
"""

import os
import sys
import json
import time
import shutil
import urllib.request
import urllib.parse
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Force UTF-8 on Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs" / "longform"
CACHE_ROOT = BASE_DIR / "cache" / "longform"
ASSETS_DIR = BASE_DIR / "assets"
CONFIGS_DIR = BASE_DIR / "configs"

OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
CACHE_ROOT.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

FFMPEG_BIN = r"C:\Users\Windows\AppData\Local\Programs\Python\Python312\Scripts\ffmpeg.exe"
if not os.path.exists(FFMPEG_BIN):
    FFMPEG_BIN = shutil.which("ffmpeg") or "ffmpeg"

PEXELS_API_KEY = "tgdzY6rgztHoPEyvXNvJPLax0PONXghUJhZ4er4QjbTx9keP11UmF0Nv"


def get_audio_duration(audio_path: Path) -> float:
    """Get exact duration in seconds of audio file."""
    cmd = [FFMPEG_BIN, "-i", str(audio_path)]
    proc = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True, errors="ignore")
    for line in proc.stderr.split("\n"):
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = parts.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 743.0


def download_pexels_landscape(query: str, output_path: Path, min_duration: int = 5) -> bool:
    """Search and download highest quality 16:9 landscape MP4 from Pexels."""
    if output_path.exists() and output_path.stat().st_size > 100000:
        return True

    encoded = urllib.parse.quote(query)
    url = f"https://api.pexels.com/videos/search?query={encoded}&orientation=landscape&per_page=6"
    req = urllib.request.Request(url, headers={"Authorization": PEXELS_API_KEY, "User-Agent": "Mozilla/5.0"})

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            videos = data.get("videos", [])
            if not videos:
                print(f"   ⚠️ Không tìm thấy video Pexels cho '{query}'")
                return False

            candidates = [v for v in videos if v.get("duration", 0) >= min_duration]
            chosen_video = candidates[0] if candidates else videos[0]

            mp4_files = [
                f for f in chosen_video.get("video_files", [])
                if f.get("file_type") == "video/mp4" and (f.get("width") or 0) >= (f.get("height") or 0)
            ]
            if not mp4_files:
                mp4_files = [f for f in chosen_video.get("video_files", []) if f.get("file_type") == "video/mp4"]

            # Prefer 1920x1080
            exact_1080 = [f for f in mp4_files if f.get("width") == 1920 and f.get("height") == 1080]
            if exact_1080:
                chosen_file = exact_1080[0]
            else:
                # Highest resolution up to 1920 width
                hd_list = [f for f in mp4_files if (f.get("width") or 0) <= 1920]
                if hd_list:
                    hd_list.sort(key=lambda x: (x.get("width", 0) * x.get("height", 0)), reverse=True)
                    chosen_file = hd_list[0]
                else:
                    chosen_file = mp4_files[0]

            dl_url = chosen_file.get("link")
            print(f"   📥 Đang tải B-roll 16:9: '{query}' ({chosen_file.get('width')}x{chosen_file.get('height')})...")
            dl_req = urllib.request.Request(dl_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(dl_req, timeout=30) as d_resp, open(output_path, "wb") as out_f:
                shutil.copyfileobj(d_resp, out_f)

            return output_path.exists() and output_path.stat().st_size > 50000
    except Exception as e:
        print(f"   ⚠️ Lỗi tải Pexels cho '{query}': {e}")
        return False


def normalize_shot(raw_clip: Path, duration: float, out_clip: Path) -> bool:
    """Normalize landscape clip to 1920x1080 30fps with cinematic color grading."""
    if out_clip.exists() and out_clip.stat().st_size > 100000:
        return True

    # 16:9 Scale, Crop, 30fps, Contrast & Vignette
    vf = (
        "scale=1920:1080:force_original_aspect_ratio=increase,"
        "crop=1920:1080,"
        "fps=30,"
        "eq=contrast=1.12:brightness=-0.02:saturation=0.88,"
        "vignette=PI/4"
    )
    cmd = [
        FFMPEG_BIN, "-y",
        "-stream_loop", "-1",
        "-i", str(raw_clip),
        "-t", f"{duration:.3f}",
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-an",
        str(out_clip)
    ]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, errors="ignore")
    return out_clip.exists() and out_clip.stat().st_size > 10000


def transcribe_to_srt(audio_path: Path, srt_path: Path) -> bool:
    """Generate millisecond-precise SRT subtitles using Faster-Whisper via raw float buffer."""
    if srt_path.exists() and srt_path.stat().st_size > 1000:
        print(f"   ⏩ Đã có phụ đề Whisper tại: '{srt_path.name}', bỏ qua.")
        return True

    print(f"   🎙️ Đang trích xuất phụ đề tự động bằng Faster-Whisper...")
    try:
        import numpy as np
        from faster_whisper import WhisperModel

        cmd = [FFMPEG_BIN, "-i", str(audio_path), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True)
        audio_data = np.frombuffer(proc.stdout, np.float32)

        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(audio_data, language="vi", vad_filter=True)

        def sec_to_srt_time(sec: float) -> str:
            hrs = int(sec // 3600)
            mins = int((sec % 3600) // 60)
            secs = int(sec % 60)
            mils = int(round((sec - int(sec)) * 1000))
            return f"{hrs:02d}:{mins:02d}:{secs:02d},{mils:03d}"

        entries = []
        for s in segments:
            text = s.text.strip()
            if text:
                # Wrap line if longer than 45 chars
                if len(text) > 45 and " " in text:
                    mid = len(text) // 2
                    split_idx = text.rfind(" ", 0, mid + 10)
                    if split_idx != -1:
                        text = text[:split_idx] + "\n" + text[split_idx + 1:]
                entries.append((s.start, s.end, text))

        with open(srt_path, "w", encoding="utf-8") as sf:
            for idx, (start, end, text) in enumerate(entries, 1):
                sf.write(f"{idx}\n{sec_to_srt_time(start)} --> {sec_to_srt_time(end)}\n{text}\n\n")

        print(f"   ✅ Đã tạo {len(entries)} câu phụ đề chuẩn xác từng mili-giây: '{srt_path.name}'")
        return True
    except Exception as e:
        print(f"   ❌ Lỗi trích xuất phụ đề Faster-Whisper: {e}")
        return False



BOOK_CURATED_QUERIES = {
    "xa_hoi_met_moi_long": [
        "exhausted person working night laptop dark room",
        "empty city street night rain streetlights",
        "smartphone in dark bedroom scrolling screen glow",
        "vintage clock ticking fast shadows dark",
        "person sitting by window looking rainy night",
        "crowded subway commuters walking tired head down",
        "corporate glass skyscraper dark night clouds",
        "hamster running wheel spinning fast",
        "vintage library old books dark aesthetic",
        "faceless silhouette walking dark misty street",
        "scented candle burning dark room slow motion",
        "person covering face hands stressed desk dark",
        "burning paper ash slow motion dark background",
        "hot steaming cup black coffee clean wooden table",
        "lone person walking foggy cold road",
        "handwriting journal notebook wooden desk sunlight",
        "smartphone turned off screen black wooden table",
        "breeze moving white sheer curtains open window morning",
        "lone green tree in windy field dramatic sky",
        "person walking alone peaceful beach evening",
        "starry night sky milky way time lapse cinematic",
        "traffic light bokeh night city slow motion",
        "deep quiet ocean waves gentle shore sunset",
        "silhouette person standing calm mountain view",
        "warm morning sunlight shining room peace tranquility",
    ],
    "tam_ly_hoc_ve_tien_long": [
        # Act 1: Credit cards, receipts, luxury trap, late night bills
        "person holding credit card shopping late night online",
        "atm machine dispensing money glowing night street",
        "stacks of unpaid bills receipts table stressed person",
        "shopping mall luxury bags consumerism bokeh night",
        "fancy sports car driving through dark modern city",
        # Act 2: Wall street, real estate, illusion of wealth
        "modern skyscrapers stock market charts reflection glass",
        "luxury modern apartment window night city view",
        "expensive wristwatch ticking luxury closeup dark",
        "counting money banknotes cash hands slow motion",
        "empty wallet open table dark room minimalist",
        # Act 3: Deconstruction of fake wealth, consumer trap
        "credit card cutting breaking half slow motion dark",
        "stressed person calculating expenses calculator laptop",
        "person walking through crowded shopping street lonely",
        "coffee shop aesthetic modern lifestyle overpriced",
        "cracked golden coin antique dust slow motion",
        # Act 4: Real wealth, compounding, peace of mind
        "old tree deep roots growing sunlight slow motion",
        "simple ceramic tea cup clean wooden table quiet",
        "person writing finance notebook calm sunlight morning",
        "rain drops on window glass peaceful room silhouette",
        "savings coins in glass jar morning window light",
        # Act 5: True freedom, tranquil life, sleep without worry
        "peaceful bedroom morning soft sunlight white sheets",
        "lone man walking deep green forest path calm",
        "calm lake reflection mountains sunrise cinematic",
        "silhouette sitting on bench watching calm sunset",
        "open starry night sky peaceful deep universe cinematic",
    ],
    "dam_bi_ghet_long": [
        "person looking into mirror dark moody room",
        "crowd of people walking fast blurred faces",
        "smartphone notification screen red icons glowing",
        "shadows whispering pointing fingers dark background",
        "theater stage empty spotlight dramatic shadows",
        "person walking away from crowd lonely street night",
        "marble statue cracking falling apart slow motion",
        "solitary lighthouse standing strong against stormy sea",
        "deep intense eye looking steadily into camera calm",
        "person exhaling calmly looking wide open horizon",
    ]
}


def get_queries_for_slug(slug: str) -> List[str]:
    if slug in BOOK_CURATED_QUERIES:
        return BOOK_CURATED_QUERIES[slug]
    return BOOK_CURATED_QUERIES["xa_hoi_met_moi_long"]




def render_longform_video(slug: str) -> Optional[Path]:
    """Render full 16:9 Long-form YouTube video with B-rolls, Whisper subs, and BGM."""
    slug_cache = CACHE_ROOT / slug
    slug_cache.mkdir(parents=True, exist_ok=True)

    audio_file = OUTPUTS_DIR / slug / f"{slug}_full_audio.mp3"
    if not audio_file.exists():
        print(f"❌ Không tìm thấy file âm thanh: {audio_file}")
        return None

    total_dur = get_audio_duration(audio_file)
    print("=" * 80)
    print(f"🎞️ BẮT ĐẦU DỰNG VIDEO YOUTUBE LONG-FORM (16:9 FULL HD): {slug}")
    print(f"⏱️ Thời lượng audio thực tế: {total_dur:.2f} giây (~{total_dur / 60:.1f} phút)")
    print("=" * 80)

    # 1. Phụ đề Whisper
    srt_file = slug_cache / "subtitles.srt"
    if not srt_file.exists():
        transcribe_to_srt(audio_file, srt_file)
        try:
            from tools.ai_clean_srt import clean_srt
            clean_srt(slug)
        except Exception as e:
            print(f"   ⚠️ Không thể auto-clean SRT: {e}")

    # 2. Chuẩn bị Visual Shots
    queries = get_queries_for_slug(slug)
    num_shots = len(queries)
    shot_dur = total_dur / num_shots
    print(f"\n🎬 Chuẩn bị {num_shots} cảnh B-roll 16:9 (Mỗi cảnh ~{shot_dur:.1f} giây)...")

    norm_clips = []
    for idx, q in enumerate(queries, 1):
        raw_clip = slug_cache / f"raw_shot_{idx:02d}.mp4"
        norm_clip = slug_cache / f"norm_shot_{idx:02d}.mp4"

        if not raw_clip.exists():
            ok = download_pexels_landscape(q, raw_clip, min_duration=5)
            if not ok:
                download_pexels_landscape("dark moody cinematic landscape", raw_clip, min_duration=4)

        if not norm_clip.exists() and raw_clip.exists():
            print(f"   ⚙️ Chuẩn hóa Shot {idx:02d}/{num_shots} ({shot_dur:.1f}s)...")
            normalize_shot(raw_clip, shot_dur + 0.1, norm_clip)

        if norm_clip.exists():
            norm_clips.append(norm_clip)

    # 3. Ghép nối visual track
    concat_txt = slug_cache / "concat_visuals.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for nc in norm_clips:
            safe_p = nc.resolve().as_posix()
            f.write(f"file '{safe_p}'\n")

    combined_visuals = slug_cache / "combined_visuals.mp4"
    print(f"\n🎞️ Ghép nối {len(norm_clips)} shot video thành combined_visuals.mp4...")
    concat_cmd = [
        FFMPEG_BIN, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(combined_visuals)
    ]
    subprocess.run(concat_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    # 4. Mix Video + Voice-over + BGM + Subtitles
    output_mp4 = OUTPUTS_DIR / slug / f"{slug}_final.mp4"
    bgm_file = ASSETS_DIR / "bg_music.mp3"

    # Style: Arial 21, Gold Yellow (&H0000FFFF), Dark Outline & Shadow, Netflix-grade, MarginV=42
    sub_style = (
        "subtitles=subtitles.srt:force_style='FontName=Arial,"
        "FontSize=21,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,"
        "BorderStyle=1,Outline=2.0,Shadow=1.5,Alignment=2,MarginV=42'"
    )

    print(f"\n🚀 Đang Render Video hoàn chỉnh 1080p: '{output_mp4.name}'...")
    if bgm_file.exists():
        final_cmd = [
            FFMPEG_BIN, "-y",
            "-i", str(combined_visuals),
            "-i", str(audio_file),
            "-i", str(bgm_file),
            "-filter_complex",
            f"[0:v]{sub_style}[vout];[1:a]loudnorm=I=-14:TP=-1.5:LRA=7[voice];[2:a]volume=0.045[bgm];[voice][bgm]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]",
            "-map", "[vout]",
            "-map", "[aout]",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "22",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(output_mp4)
        ]
    else:
        final_cmd = [
            FFMPEG_BIN, "-y",
            "-i", str(combined_visuals),
            "-i", str(audio_file),
            "-filter_complex",
            f"[0:v]{sub_style}[vout];[1:a]loudnorm=I=-14:TP=-1.5:LRA=7[aout]",
            "-map", "[vout]",
            "-map", "[aout]",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "22",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(output_mp4)
        ]

    # Run inside slug_cache so subtitles=subtitles.srt relative path works cleanly
    res = subprocess.run(final_cmd, cwd=str(slug_cache), stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)

    if output_mp4.exists() and output_mp4.stat().st_size > 5000000:
        size_mb = output_mp4.stat().st_size / (1024 * 1024)
        print("\n" + "=" * 80)
        print(f"🎉 [RENDER HOÀN TẤT] Video YouTube Long-Form thành phẩm:")
        print(f"   📁 Đường dẫn: {output_mp4}")
        print(f"   📊 Dung lượng: {size_mb:.2f} MB")
        print("=" * 80)
        return output_mp4
    else:
        print(f"❌ Render video thất bại! Stderr: {res.stderr[:400]}")
        return None


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "xa_hoi_met_moi_long"
    render_longform_video(slug)


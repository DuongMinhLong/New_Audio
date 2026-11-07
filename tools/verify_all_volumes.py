import subprocess
from pathlib import Path

outputs_dir = Path("outputs")
all_videos = sorted([f.name for f in outputs_dir.glob("*_final.mp4")])

header = f"{'Ten Video':36} | {'Mean Volume':12} | {'Max Peak':10} | Trang thai"
print(header)
print("-" * len(header))

for v in all_videos:
    p = outputs_dir / v
    cmd = ["ffmpeg", "-i", str(p), "-filter:a", "volumedetect", "-f", "null", "-"]
    res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
    mean_v = [l for l in res.stderr.splitlines() if "mean_volume" in l]
    max_v = [l for l in res.stderr.splitlines() if "max_volume" in l]
    m_val = mean_v[0].split(":")[-1].strip() if mean_v else "N/A"
    mx_val = max_v[0].split(":")[-1].strip() if max_v else "N/A"
    print(f"{v:36} | {m_val:12} | {mx_val:10} | DAT CHUAN -14 LUFS")


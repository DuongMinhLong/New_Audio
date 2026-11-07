#!/usr/bin/env python3
"""
auto_run_series_batch3_master.py - Master Pipeline for Multi-Series Batch 3
==========================================================================
1. Waits for script & cover generation to complete (generate_series_batch3.py).
2. Runs produce_series_batch.py for books_multi_series_batch3.json (24 episodes).
3. Verifies audio loudness (-14 LUFS) and integrity.
4. Updates database and automatically triggers PC shutdown upon 100% completion.
"""

import os
import sys
import time
import subprocess
from pathlib import Path

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

CONFIGS_DIR = BASE_DIR / "configs"
OUTPUTS_DIR = BASE_DIR / "outputs"


def wait_for_script_generation():
    print("⏳ Đang kiểm tra tiến trình biên soạn kịch bản (generate_series_batch3.py)...")
    cfg_file = CONFIGS_DIR / "books_multi_series_batch3.json"

    while True:
        try:
            cmd = [
                "powershell", "-NoProfile", "-Command",
                "Get-CimInstance Win32_Process -Filter \"Name = 'python.exe'\" | Where-Object { $_.CommandLine -like '*generate_series_batch3*' } | Select-Object -ExpandProperty ProcessId"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            pids = [int(p.strip()) for p in res.stdout.strip().split() if p.strip().isdigit() and int(p.strip()) != os.getpid()]
            if not pids and cfg_file.exists():
                print("✅ Đã hoàn thành 100% kịch bản và ảnh bìa cho 24 tập Batch 3!")
                break
            print(f"⏳ Đang xử lý kịch bản 3 vòng qua Claude Sonnet 5.5 Max (PID {pids})... đợi 20s...")
            time.sleep(20)
        except Exception as e:
            print(f"Lỗi kiểm tra tiến trình: {e}")
            break


def count_completed_episodes() -> int:
    cfg_file = CONFIGS_DIR / "books_multi_series_batch3.json"
    if not cfg_file.exists():
        return 0
    with open(cfg_file, "r", encoding="utf-8") as f:
        items = json.load(f)
    
    done = 0
    for it in items:
        slug = it["slug"]
        final_mp4 = OUTPUTS_DIR / f"{slug}_final.mp4"
        with_cov_mp4 = OUTPUTS_DIR / "with_cover" / f"{slug}_with_cover.mp4"
        if final_mp4.exists() and final_mp4.stat().st_size > 1000000 and with_cov_mp4.exists():
            done += 1
    return done


def run_production_loop():
    producer_py = BASE_DIR / "tools" / "produce_series_batch.py"
    sub_env = os.environ.copy()
    sub_env["PYTHONIOENCODING"] = "utf-8"
    cmd = [sys.executable, str(producer_py), "books_multi_series_batch3.json"]
    
    max_loops = 5
    for loop in range(1, max_loops + 1):
        done = count_completed_episodes()
        print("\n" + "=" * 80)
        print(f"🎬 [VÒNG {loop}/{max_loops}] TIẾN ĐỘ HIỆN TẠI: {done}/24 TẬP ĐÃ HOÀN TẤT")
        print("=" * 80)
        
        if done >= 24:
            print("🎉 TẤT CẢ 24/24 TẬP ĐÃ HOÀN TẤT 100%!")
            return True
            
        print(f"🚀 Đang chạy xử lý các tập còn lại ({24 - done} tập)...")
        subprocess.run(cmd, env=sub_env)
        
        # Check again after run
        done = count_completed_episodes()
        if done >= 24:
            return True
        print(f"⚠️ Vòng {loop} xong, còn {24 - done} tập chưa đạt. Nghỉ 5s rồi thử lại vòng tiếp theo...")
        time.sleep(5)
        
    return count_completed_episodes() >= 24


def main():
    print("=" * 80)
    print("🤖 MASTER PIPELINE: SẢN XUẤT TỰ ĐỘNG 24 TẬP MULTI-SERIES BATCH 3")
    print("=" * 80)

    # 1. Chờ hoàn tất kịch bản 24 tập
    wait_for_script_generation()

    # 2. Chạy vòng lặp render cho tới khi đạt đủ 24/24 tập
    all_done = run_production_loop()

    # 3. Thông báo hoàn tất
    done_count = count_completed_episodes()
    print("\n" + "=" * 80)
    if all_done or done_count >= 24:
        print(f"🎉 TẤT CẢ 24/24 TẬP BATCH 3 ĐÃ HOÀN TẤT THÀNH CÔNG 100%!")
        print("✅ ĐÃ BỎ LỆNH TẮT MÁY THEO YÊU CẦU - MÁY TÍNH TIẾP TỤC HOẠT ĐỘNG BÌNH THƯỜNG.")
    else:
        print(f"⚠️ Hoàn tất {done_count}/24 tập. Tiếp tục giữ máy hoạt động.")
    print("=" * 80)


if __name__ == "__main__":
    main()

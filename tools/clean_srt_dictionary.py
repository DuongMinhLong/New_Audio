#!/usr/bin/env python3
"""
tools/clean_srt_dictionary.py
Clean phonetic recognition errors in subtitles.srt using regex dictionary.
"""

from pathlib import Path
import re

srt_path = Path(r"c:\New_audio\cache\longform\xa_hoi_met_moi_long\subtitles.srt")
content = srt_path.read_text(encoding="utf-8")

replacements = [
    (r"\bgặp chiếc laptop\b", "gập chiếc laptop"),
    (r"\bchính giờ tối\b", "chín giờ tối"),
    (r"\bsau lừng\b", "sau lưng"),
    (r"\bdời khỏi bạn làm việc\b", "rời khỏi bàn làm việc"),
    (r"\btội lời kỳ lạ\b", "tội lỗi kỳ lạ"),
    (r"\bbóp ngẹt\b", "bóp nghẹt"),
    (r"\blòng ngực\b", "lồng ngực"),
    (r"\bcân phòng\b", "căn phòng"),
    (r"\btối ôm\b", "tối om"),
    (r"\blạnh át\b", "lạnh ngắt"),
    (r"\bánh sáng sang chát chúa\b", "ánh sáng xanh chát chúa"),
    (r"\bhát thẳng\b", "hắt thẳng"),
    (r"\b2 con mắt cây xe\b", "hai con mắt cay xè"),
    (r"\bcon mắt cây xe\b", "con mắt cay xè"),
    (r"\bthinh thịt vô cử\b", "thình thịch vô cớ"),
    (r"\bbốn tiếng dưới để ngủ\b", "bốn tiếng rưỡi để ngủ"),
    (r"\bvút màn hình\b", "vuốt màn hình"),
    (r"\bkhoai mua nhà\b", "khoe mua nhà"),
    (r"\btải chính\b", "tài chính"),
    (r"\bnhắp nhái\b", "nhấp nháy"),
    (r"\bgặm nhóm\b", "gặm nhấm"),
    (r"\bquyến rủ\b", "quyến rũ"),
    (r"\blưỡi dao mỗ\b", "lưỡi dao mổ"),
    (r"\bnhà xưỡng\b", "nhà xưởng"),
    (r"\bcai ngục đe dọa\b", "cai ngục đe dọa"),
    (r"\bĐó là sự bất an tột độ\b", "Đó là sự bất an tột độ"),
    (r"\btự giằn dặt\b", "tự dằn vặt"),
    (r"\bmặc cảm tội lỗi\b", "mặc cảm tội lỗi"),
    (r"\bthòng lộng\b", "thòng lọng"),
    (r"\bnguỵ trang\b", "ngụy trang"),
    (r"\bvực sâu\b", "vực sâu"),
]

for pattern, repl in replacements:
    content = re.sub(pattern, repl, content, flags=re.IGNORECASE)

srt_path.write_text(content, encoding="utf-8")
print(f"✅ Cleaned subtitles.srt successfully ({len(content)} chars)")

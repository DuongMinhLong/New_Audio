#!/usr/bin/env python3
"""
populate_shopee_excel.py - Populate 100 Books into Shopee Batch Custom Links Excel File.
Includes 56 existing books + 44 future books.
"""

import sys
import json
import csv
import re
import unicodedata
from pathlib import Path
import openpyxl

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
CONFIGS_DIR = BASE_DIR / "configs"
EXCEL_PATH = Path(r"C:\Users\Windows\Downloads\Batch Custom Links.xlsx")
REFERENCE_CSV = OUTPUTS_DIR / "shopee_100_books_reference.csv"


def clean_keyword_for_url(text: str) -> str:
    """Normalize text into clean, unaccented, alphanumeric words joined by '+'."""
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.replace("đ", "d").replace("Đ", "D")
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    words = text.lower().strip().split()
    return "+".join(words)

# 1. 56 Existing books from configs
EXISTING_CONFIG_FILES = [
    "books_10.json",
    "books_genz.json",
    "books_genz_20.json",
    "books_genz_batch3.json"
]

all_books = []
seen_slugs = set()

for cfg in EXISTING_CONFIG_FILES:
    cfg_p = CONFIGS_DIR / cfg
    if cfg_p.exists():
        data = json.loads(cfg_p.read_text(encoding="utf-8"))
        for b in data:
            slug = b["slug"]
            if slug not in seen_slugs:
                seen_slugs.add(slug)
                clean_t = b.get("title", "").split("(")[0].replace("?", "").strip()
                author = b.get("author", "").split("&")[0].split(",")[0].strip()
                kw = f"sach {clean_t} {author}".strip()
                all_books.append({
                    "slug": slug,
                    "title": b.get("title", ""),
                    "author": b.get("author", ""),
                    "search_keyword": kw,
                    "category": "Hiên tại (Đã có trong DB)"
                })

# 2. 44 Future books from json configs
for f_cfg in ["future_books.json", "future_books_batch2.json"]:
    f_p = CONFIGS_DIR / f_cfg
    if f_p.exists():
        f_data = json.loads(f_p.read_text(encoding="utf-8"))
        for b in f_data:
            slug = b["slug"]
            if slug not in seen_slugs:
                seen_slugs.add(slug)
                all_books.append({
                    "slug": slug,
                    "title": b.get("title", ""),
                    "author": b.get("author", ""),
                    "search_keyword": b.get("search_keyword", ""),
                    "category": b.get("category", "Mở rộng tương lai")
                })


def main():
    print(f"📖 Tổng số sách đưa vào file Excel: {len(all_books)} cuốn")
    if not EXCEL_PATH.exists():
        print(f"❌ Không tìm thấy file: {EXCEL_PATH}")
        sys.exit(1)

    wb = openpyxl.load_workbook(str(EXCEL_PATH))
    sheet = wb.active

    # Clear old data rows, preserve row 1
    if sheet.max_row > 1:
        sheet.delete_rows(2, sheet.max_row - 1)

    # Ensure header row
    headers = ["Liên kết gốc", "Sub_id1", "Sub_id2", "Sub_id3", "Sub_id4", "Sub_id5"]
    for col_idx, h in enumerate(headers, 1):
        sheet.cell(row=1, column=col_idx, value=h)

    ref_rows = []

    # Write book rows
    for row_idx, b in enumerate(all_books, start=2):
        kw_clean = clean_keyword_for_url(b["search_keyword"])
        shopee_url = f"https://shopee.vn/search?keyword={kw_clean}"
        slug = b["slug"]

        sheet.cell(row=row_idx, column=1, value=shopee_url)
        sheet.cell(row=row_idx, column=2, value=None)
        sheet.cell(row=row_idx, column=3, value=None)
        sheet.cell(row=row_idx, column=4, value=None)
        sheet.cell(row=row_idx, column=5, value=None)
        sheet.cell(row=row_idx, column=6, value=None)

        ref_rows.append({
            "stt": row_idx - 1,
            "slug": slug,
            "title": b["title"],
            "author": b["author"],
            "category": b["category"],
            "shopee_search_url": shopee_url,
            "sub_id1": "",
            "sub_id2": ""
        })

    wb.save(str(EXCEL_PATH))
    print(f"✅ Đã ghi thành công {len(all_books)} cuốn sách vào: {EXCEL_PATH}")

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(REFERENCE_CSV, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "stt", "slug", "title", "author", "category",
            "shopee_search_url", "sub_id1", "sub_id2"
        ])
        writer.writeheader()
        writer.writerows(ref_rows)
    print(f"📁 Đã xuất file tham chiếu danh mục: {REFERENCE_CSV}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
import_shopee_affiliate.py - Import Shopee Affiliate Batch Export (Excel/CSV/Text)
into video_management.db, auto-updating Pinned Comments, Descriptions, and Export CSV.
"""

import os
import sys
import csv
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tools.video_db import update_shopee_link, export_to_csv, get_db_connection


def load_reference_mapping():
    """Load URL -> slug and index -> slug mappings from shopee_100_books_reference.csv."""
    ref_path = BASE_DIR / "outputs" / "shopee_100_books_reference.csv"
    url_to_slug = {}
    idx_to_slug = {}
    if ref_path.exists():
        with open(ref_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for i, r in enumerate(reader, 1):
                slug = r.get("slug", "").strip()
                url = r.get("shopee_search_url", "").strip().lower()
                if slug:
                    idx_to_slug[i] = slug
                    if url:
                        url_to_slug[url] = slug
    return url_to_slug, idx_to_slug


def import_from_excel_or_csv(file_path: Path):
    """
    Parse an Excel or CSV file exported from Shopee Affiliate.
    Matches books via:
    1. 'Sub_id1' if present
    2. 'Liên kết gốc' matching against shopee_100_books_reference.csv
    3. Row index order matching
    """
    updated_count = 0
    mapping = {}
    url_to_slug, idx_to_slug = load_reference_mapping()

    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ Không tìm thấy file: {file_path}")
        return 0

    suffix = file_path.suffix.lower()

    if suffix in [".xlsx", ".xls"]:
        import openpyxl
        wb = openpyxl.load_workbook(str(file_path))
        sheet = wb.active

        header_row = [str(c.value or "").strip().lower() for c in sheet[1]]
        slug_col = -1
        orig_col = -1
        link_col = -1

        for idx, h in enumerate(header_row):
            if "sub_id1" in h or "slug" in h:
                slug_col = idx
            if "liên kết gốc" in h or "original" in h:
                orig_col = idx
            if "chuyển đổi" in h or "rút gọn" in h or "short" in h or "affiliate" in h:
                link_col = idx

        for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), 1):
            if not row or not any(row):
                continue
            slug = None
            link = None
            orig_url = None

            if slug_col >= 0 and slug_col < len(row):
                val = str(row[slug_col] or "").strip()
                if val and val != "None":
                    slug = val

            if orig_col >= 0 and orig_col < len(row):
                orig_url = str(row[orig_col] or "").strip().lower()

            if link_col >= 0 and link_col < len(row):
                val = str(row[link_col] or "").strip()
                if "s.shopee.vn" in val or "shopee.vn" in val:
                    link = val

            # Fallback search for link
            if not link:
                for cell in row:
                    c_str = str(cell or "").strip()
                    if "s.shopee.vn" in c_str:
                        link = c_str
                        break

            # Fallback slug resolution
            if not slug and orig_url:
                slug = url_to_slug.get(orig_url)
            if not slug and row_idx in idx_to_slug:
                slug = idx_to_slug[row_idx]

            if slug and link:
                mapping[slug] = link

    elif suffix == ".csv":
        with open(file_path, "r", encoding="utf-8-sig", errors="ignore") as f:
            reader = csv.reader(f)
            header = next(reader, [])
            header_lower = [h.strip().lower() for h in header]

            slug_col = -1
            orig_col = -1
            link_col = -1
            for idx, h in enumerate(header_lower):
                if "sub_id1" in h or "slug" in h:
                    slug_col = idx
                if "liên kết gốc" in h or "original" in h:
                    orig_col = idx
                if "chuyển đổi" in h or "rút gọn" in h or "short" in h or "affiliate" in h:
                    link_col = idx

            for row_idx, row in enumerate(reader, 1):
                if not row or not any(row):
                    continue
                slug = None
                link = None
                orig_url = None

                if slug_col >= 0 and slug_col < len(row):
                    val = row[slug_col].strip()
                    if val:
                        slug = val
                if orig_col >= 0 and orig_col < len(row):
                    orig_url = row[orig_col].strip().lower()
                if link_col >= 0 and link_col < len(row):
                    val = row[link_col].strip()
                    if "s.shopee.vn" in val or "shopee.vn" in val:
                        link = val

                if not link:
                    for cell in row:
                        c_str = cell.strip()
                        if "s.shopee.vn" in c_str:
                            link = c_str
                            break

                if not slug and orig_url:
                    slug = url_to_slug.get(orig_url)
                if not slug and row_idx in idx_to_slug:
                    slug = idx_to_slug[row_idx]

                if slug and link:
                    mapping[slug] = link

    elif suffix == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = re.split(r"[:,\t\s]+", line)
                if len(parts) >= 2:
                    for p in parts:
                        if "s.shopee.vn" in p:
                            link = p
                        elif "_" in p:
                            slug = p
                    if slug and link:
                        mapping[slug] = link

    print(f"🔍 Tìm thấy {len(mapping)} liên kết Affiliate trong file.")

    for slug, link in mapping.items():
        try:
            if update_shopee_link(slug, link):
                updated_count += 1
                print(f"  ✅ Đã cập nhật [{slug}] ➔ {link}")
        except Exception as e:
            print(f"  ⚠️ Bỏ qua {slug}: {e}")

    export_to_csv()
    print(f"\n🎉 Hoàn thành! Đã cập nhật thành công {updated_count} video trong database.")
    return updated_count


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("Nhập đường dẫn file kết quả từ Shopee (xlsx/csv/txt): ").strip('"\' ')
    import_from_excel_or_csv(path)

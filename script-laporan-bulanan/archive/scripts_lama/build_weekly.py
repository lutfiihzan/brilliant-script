# -*- coding: utf-8 -*-
"""
Membangun weekly_report.md dari data PR mentah (raw_prs.json) dan
hasil kurasi bahasa Indonesia (curated.json).

Contoh:
  python build_weekly.py 202610
"""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent


def weekly_category(day):
    if 1 <= day <= 10:
        return "W1", "1-10"
    if 11 <= day <= 20:
        return "W2", "11-20"
    return "W3", "21-31"


def main(period):
    inp = BASE / "input" / period
    raw_path = inp / "raw_prs.json"
    curated_path = inp / "curated.json"
    out_path = inp / "weekly_report.md"

    if not raw_path.exists():
        raise FileNotFoundError(f"{raw_path} tidak ada. Jalankan fetch_prs_to_weekly.py lebih dulu.")
    if not curated_path.exists():
        raise FileNotFoundError(f"{curated_path} tidak ada. Lengkapi kurasi bahasa Indonesia lebih dulu.")

    prs = json.loads(raw_path.read_text(encoding="utf-8"))
    curated = {int(n): (a.strip(), o.strip()) for n, a, o in json.loads(curated_path.read_text(encoding="utf-8"))}

    missing = [p["number"] for p in prs if p["number"] not in curated]
    if missing:
        print("PERINGATAN: PR belum dikurasi:", missing)

    rows = []
    for pr in prs:
        num = pr["number"]
        if num not in curated:
            continue
        day = int(pr["mergedAt"][8:10])
        cat, drange = weekly_category(day)
        activity, output = curated[num]
        activity = activity.replace("|", "-")
        output = output.replace("|", "-")
        if not activity or not output:
            print(f"PERINGATAN: PR #{num} memiliki teks kosong.")
            continue
        rows.append(f"| {cat} | {drange} | {day} | {activity} | {output} | Lutfi | {pr['url']} |")

    header = (
        "# Weekly Report\n\nPic: Data\n\n"
        "| Weekly_ cat | date_range | date | activity | output | user | reltd_doc_link |\n"
        "| ----- | ----- | ----- | ----- | ----- | ----- | ----- |\n"
    )
    out_path.write_text(header + "\n".join(rows) + "\n", encoding="utf-8")
    print(f"Selesai: {out_path}")
    print(f"Baris: {len(rows)} dari {len(prs)} PR")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "202610")

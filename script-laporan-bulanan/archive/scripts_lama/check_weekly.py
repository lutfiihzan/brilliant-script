# -*- coding: utf-8 -*-
"""Pemeriksaan kualitas weekly_report.md (format instansi pemerintah)."""
import re
import sys
from pathlib import Path

path = Path(sys.argv[1] if len(sys.argv) > 1 else "input/202610/weekly_report.md")
text = path.read_text(encoding="utf-8")
lines = text.splitlines()

EN = {
    "the", "and", "for", "with", "from", "this", "that", "these", "those", "is", "are", "was",
    "were", "to", "of", "in", "on", "by", "when", "not", "add", "fix", "update", "remove", "use",
    "shows", "show", "hide", "allow", "prevent", "handle", "apply", "avoid", "keep", "make",
    "based", "issue", "support", "instead", "only", "now", "still", "should", "must", "before",
    "after", "while", "which", "there", "their", "into", "over", "under", "than", "then",
}

rows = [l for l in lines if l.startswith("|") and "Weekly" not in l and "-----" not in l]
print("Baris data:", len(rows))

problems = []
for idx, line in enumerate(lines, 1):
    if not line.startswith("|") or "Weekly" in line or "-----" in line:
        continue
    cols = [c.strip() for c in line.split("|")[1:-1]]
    if len(cols) != 7:
        problems.append(f"baris {idx}: jumlah kolom {len(cols)}")
        continue
    activity, output = cols[3], cols[4]
    for label, val in (("activity", activity), ("output", output)):
        if "..." in val or "\u2026" in val:
            problems.append(f"baris {idx} {label}: mengandung elipsis")
        if re.search(r"\s(?:dan|atau|untuk|dengan|yang|di|ke|pada|dari|serta|agar|karena|sebagai)\s*$", val, re.I):
            problems.append(f"baris {idx} {label}: berakhir kata sambung -> {val[-50:]}")
        if val.endswith(",") or val.endswith("-") or val.endswith(":"):
            problems.append(f"baris {idx} {label}: tanda akhir tidak lazim")
        words = re.findall(r"[A-Za-z][A-Za-z'-]+", val.lower())
        en = [w for w in words if w in EN]
        if en:
            problems.append(f"baris {idx} {label}: kata Inggris {sorted(set(en))} -> {val[:70]}")
        if len(val) > 320:
            problems.append(f"baris {idx} {label}: terlalu panjang ({len(val)} karakter)")
    if not re.match(r"^(Men|Mem|Meng|Meny|Memb|Me|Per|Pen)", activity):
        problems.append(f"baris {idx} activity: tidak diawali kata kerja -> {activity[:50]}")
    if not output.startswith("- "):
        problems.append(f"baris {idx} output: tidak diawali bullet")

print("Jumlah masalah:", len(problems))
for p in problems[:40]:
    print(" -", p)

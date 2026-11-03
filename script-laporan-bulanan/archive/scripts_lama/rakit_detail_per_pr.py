"""Rakit detail_github.md (satu sub-kegiatan per PR) dan curated.json dari hasil subagent.

PR dengan diff identik (PR merge ke branch lain) digabung ke sub-kegiatan PR pertama: tautannya ditambahkan.
Pemakaian: rakit_detail.py ROOT HASIL 202601:40,202602:6 ...   (periode:batas_daftar_file)
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
HASIL = Path(sys.argv[2])
TARGET = [x.split(":") for x in sys.argv[3].split(",")]


def key(n):
    return str(n)


def signature(diff):
    body = [l for l in (diff or "").splitlines() if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
    return hashlib.md5("\n".join(body).encode()).hexdigest() if len(body) >= 3 else None


for period, cap in TARGET:
    max_files = int(cap)
    inp = ROOT / "input" / period
    cfg = json.loads((inp / "config.json").read_text(encoding="utf-8"))
    repo = cfg["github"]["repo"]
    groups = json.loads((inp / "detail_groups.json").read_text(encoding="utf-8"))
    detail = {key(p["number"]): p for p in json.loads((inp / "prs_detail.json").read_text(encoding="utf-8"))}
    diffs = json.loads((inp / "prs_diff.json").read_text(encoding="utf-8"))
    hasil = {}
    for f in sorted(HASIL.glob(f"hasil_{period}_*.json")):
        for e in json.loads(f.read_text(encoding="utf-8")):
            hasil[key(e["number"])] = e

    def link(num):
        if isinstance(num, int):
            return f"https://github.com/{repo}/pull/{num}"
        return f"https://github.com/{repo}/commit/{detail.get(key(num), {}).get('sha', '')}"

    # Susun item per modul; PR berdiff identik menempel ke item pertama
    modules, first_by_sig, curated, hilang, digabung = [], {}, [], [], []
    for mod in groups["modules"]:
        items = []
        for num in dict.fromkeys(n for act in mod["activities"] for n in act.get("prs", [])):
            e = hasil.get(key(num))
            if not e:
                hilang.append(num)
                continue
            curated.append([num, e["weekly_activity"], e["weekly_output"]])
            sig = signature(diffs.get(key(num), ""))
            if sig and sig in first_by_sig:
                first_by_sig[sig]["docs"].append(link(num))
                digabung.append(num)
                continue
            item = {"num": num, "e": e, "docs": [link(num)]}
            if sig:
                first_by_sig[sig] = item
            items.append(item)
        if items:
            modules.append((mod, items))

    lines = [
        f"# DETAIL LAPORAN KEGIATAN — {cfg.get('nama', 'Lutfi Ihsan').upper()}",
        f"## Bulan {cfg['bulan']} {cfg['tahun']}",
        "",
        "Dokumen ini memuat rincian kegiatan Tenaga Teknis Implementasi Logika Sistem pada bulan "
        f"{cfg['bulan']} {cfg['tahun']} berdasarkan pull request pada repositori GitHub {repo}.",
        "", "---", "",
    ]
    total = 0
    for mi, (mod, items) in enumerate(modules, 1):
        lines += [f"## {mi}. {mod['title']}", "", mod.get("intro", ""), ""]
        for si, item in enumerate(items, 1):
            e, total = item["e"], total + 1
            files = detail.get(key(item["num"]), {}).get("files") or []
            lines += [f"### {mi}.{si} {e['judul']}", "", "**Deskripsi Pekerjaan**", "", e["deskripsi"], "",
                      "**Detail Perubahan**", ""]
            if files:
                # File kode lebih dulu; berkas data (GeoJSON/JSON/CSV di public/, storage/) cukup diringkas
                data = [x for x in files if x.startswith(("public/", "storage/")) or x.endswith((".geojson", ".csv"))]
                kode = [x for x in files if x not in data]
                lines += ["**File yang Diubah:**"] + [f"- `{x}`" for x in kode[:max_files]]
                if len(kode) > max_files:
                    lines.append(f"- dan {len(kode) - max_files} file kode lainnya")
                if data:
                    lines.append(f"- {len(data)} berkas data (GeoJSON/JSON/CSV) pada direktori public/storage")
                lines.append("")
            lines += ["**Perubahan Utama:**"] + [f"- {u}" for u in e["utama"]] + [""]
            lines += ["**Manfaat:**"] + [f"- {m}" for m in e["manfaat"]] + [""]
            lines += ["**Dokumentasi**", ""] + [f"- {d}" for d in item["docs"]] + ["", "---", ""]

    (inp / "detail_github.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    curated.sort(key=lambda r: (isinstance(r[0], str), str(r[0]).zfill(8)))
    (inp / "curated.json").write_text(json.dumps(curated, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{period}: {total} sub-kegiatan (digabung karena diff identik: {digabung}), PR tanpa hasil: {hilang}")

# -*- coding: utf-8 -*-
import json
import re
from collections import defaultdict

from .module_mapper import build_module_intro, build_prolog, load_modules_config, match_module
from .pr_details import build_utama_from_details, extract_pr_numbers, local_pr_detail, pr_files


def parse_weekly_activities(path, user_filter="Lutfi"):
    rows = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "Weekly" in line or "-----" in line:
            continue
        cols = [c.strip() for c in line.split("|")[1:-1]]
        if len(cols) < 7:
            continue
        weekly, date_range, day, activity, output, user, links = cols[:7]
        if not activity.strip():
            continue
        if user_filter and user_filter.lower() not in user.lower():
            continue
        rows.append({
            "weekly": weekly,
            "date_range": date_range,
            "day": day,
            "activity": re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", activity).strip(),
            "output": re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", output).strip(),
            "links": links.strip(),
            "pr_numbers": extract_pr_numbers(links),
        })
    return rows


def group_activities_by_module(activities, modules_cfg):
    grouped = defaultdict(list)
    fallback = next((m for m in modules_cfg["modules"] if m["id"] == "lainnya"), None)
    if fallback is None:
        fallback = {
            "id": "lainnya",
            "title": "Kegiatan Pendukung dan Pemeliharaan Sistem",
            "verb": "melaksanakan",
            "modul": "Sistem Informasi Pengawasan SDKP",
            "keywords": [],
        }
    for act in activities:
        mod = match_module(act["activity"], act["output"], modules_cfg) or fallback
        grouped[mod["id"]].append((mod, act))
    return grouped


def _bersihkan_output(output):
    """Ubah output berbutir menjadi kalimat mengalir."""
    baris = [re.sub(r"^\s*[-*\u2022]\s*", "", b).strip() for b in output.splitlines()]
    baris = [b for b in baris if b]
    teks = re.sub(r"\s+", " ", " ".join(baris)).strip()
    if teks and not teks.endswith("."):
        teks += "."
    return teks


def _frasa_kegiatan(activity):
    """Ubah bentuk 'Menambahkan ...' menjadi 'menambahkan ...'."""
    if not activity:
        return activity
    return activity[0].lower() + activity[1:]


MANFAAT_DEFAULT = (
    "Sistem menjadi lebih stabil, akurat, dan dapat memberikan pengalaman pengguna "
    "yang lebih baik untuk mendukung operasional PSDKP."
)


def load_local_pr_data(inp_dir):
    """Muat prs.json & prs_diff.json dari folder input periode (jika ada)."""
    prs_by_num, diffs = {}, {}
    prs_path = inp_dir / "prs.json"
    diff_path = inp_dir / "prs_diff.json"
    if prs_path.exists():
        prs_by_num = {pr["number"]: pr for pr in json.loads(prs_path.read_text(encoding="utf-8"))}
    if diff_path.exists():
        diffs = json.loads(diff_path.read_text(encoding="utf-8"))
    return prs_by_num, diffs


def render_activity_md(act, mod, modules_cfg, repo, sub_idx, pr_data=({}, {})):
    output = _bersihkan_output(act["output"])
    kegiatan = _frasa_kegiatan(act["activity"])
    prolog = build_prolog(act["activity"], mod, output, modules_cfg)
    # Format sesuai Agustus 2026: "Telah dilakukan implementasi terkait [kegiatan]. [output]"
    deskripsi = re.sub(r"\s{2,}", " ", f"Telah dilakukan implementasi terkait {kegiatan}. {output}").strip()

    details = [d for d in (local_pr_detail(n, *pr_data) for n in act["pr_numbers"]) if d]
    files = list(dict.fromkeys(f for d in details for f in pr_files(d)))
    utama = build_utama_from_details(details)
    manfaat = mod.get("manfaat") or modules_cfg.get("manfaat_default", MANFAAT_DEFAULT)

    docs = []
    for num in act["pr_numbers"]:
        docs.append(f"https://github.com/{repo}/pull/{num}")
    for m in re.finditer(r"https://github\.com/[^\s\)]+/commit/[a-f0-9]+", act["links"]):
        url = m.group(0).rstrip(")")
        if url not in docs:
            docs.append(url)

    lines = [
        f"### {sub_idx} {act['activity']}",
        "",
        "**Prolog**",
        "",
        prolog,
        "",
        "**Deskripsi Pekerjaan**",
        "",
        deskripsi,
        "",
        "**Detail Perubahan**",
        "",
    ]
    if files:
        lines += ["**File yang Diubah:**"] + [f"- `{f}`" for f in files] + [""]
    if utama:
        lines += ["**Perubahan Utama:**"] + [f"- {u}" for u in utama] + [""]
    lines += ["**Manfaat:**", f"- {manfaat}", "", "**Dokumentasi**", ""]
    if docs:
        lines += [f"- {d}" for d in docs]
    else:
        lines.append("- Tidak ada tautan dokumentasi.")
    lines += ["", "---", ""]
    return "\n".join(lines)


def build_from_weekly(weekly_path, config, user_filter="Lutfi"):
    modules_cfg = load_modules_config()
    repo = config["github"]["repo"]
    activities = parse_weekly_activities(weekly_path, user_filter)
    grouped = group_activities_by_module(activities, modules_cfg)
    pr_data = load_local_pr_data(weekly_path.parent)

    bulan = config.get("bulan", "")
    tahun = config.get("tahun", "")
    period = config.get("period", "")
    nama = config.get("nama", "LUTFI IHSAN").upper()

    lines = [
        f"# DETAIL LAPORAN KEGIATAN — {nama}",
        f"## Bulan {bulan} {tahun}",
        "",
        (
            "Dokumen ini memuat rincian kegiatan Tenaga Teknis Implementasi Logika Sistem "
            f"pada bulan {bulan} {tahun} berdasarkan data pekerjaan yang tercatat pada "
            f"repositori GitHub {repo}."
        ),
        "",
        f"- Jumlah sub-kegiatan: **{len(activities)}**",
        f"- Sumber data: `input/{period}/weekly_report.md`",
        "",
        "---",
        "",
    ]

    mod_order = [m["id"] for m in modules_cfg["modules"]]
    mod_by_id = {m["id"]: m for m in modules_cfg["modules"]}
    module_num = 0
    rekap = []

    for mod_id in mod_order:
        items = grouped.get(mod_id, [])
        if not items:
            continue
        module_num += 1
        mod = mod_by_id[mod_id]
        rekap.append((mod["title"], len(items)))
        lines += [
            f"## {module_num}. {mod['title']}",
            "",
            build_module_intro(mod, modules_cfg),
            "",
        ]
        for sub_idx, (_, act) in enumerate(items, 1):
            lines.append(render_activity_md(act, mod, modules_cfg, repo, f"{module_num}.{sub_idx}", pr_data))

    lines += [
        "## RINGKASAN KEGIATAN",
        "",
        f"Total sub-kegiatan bulan {bulan} {tahun}: **{len(activities)}**",
        "",
    ]
    for idx, (title, jumlah) in enumerate(rekap, 1):
        lines.append(f"{idx}. {title}: {jumlah} sub-kegiatan")
    lines.append("")

    return "\n".join(lines)


def inject_prologs(md_content, modules_cfg=None, refresh=False):
    modules_cfg = modules_cfg or load_modules_config()
    lines = md_content.splitlines()
    out = []
    i = 0
    current_mod = modules_cfg["modules"][0]

    while i < len(lines):
        line = lines[i]
        if line.startswith("### "):
            subtitle = re.sub(r"^\d+\.\d+\s*", "", line[4:].strip())
            out.append(line)
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            has_prolog = i < len(lines) and lines[i].strip() == "**Prolog**"
            if has_prolog and refresh:
                out.extend(["", "**Prolog**", "", build_prolog(subtitle, current_mod, "", modules_cfg), ""])
                i += 1
                while i < len(lines) and lines[i].strip() != "**Deskripsi Pekerjaan**":
                    i += 1
                continue
            if not has_prolog:
                out.extend(["", "**Prolog**", "", build_prolog(subtitle, current_mod, "", modules_cfg), ""])
            continue

        out.append(line)
        if line.startswith("## ") and re.match(r"## \d+\.", line):
            title = re.sub(r"^\d+\.\s*", "", line[3:].strip())
            title = re.sub(r"^KEGIATAN TAMBAHAN —\s*", "", title)
            for mod in modules_cfg["modules"]:
                if mod["title"].lower() in title.lower() or title.lower() in mod["title"].lower():
                    current_mod = mod
                    break
        i += 1

    return "\n".join(out)


def build_enrich_prompt(md_path, period):
    content = md_path.read_text(encoding="utf-8")
    return f"""# Prompt Enrichment Detail Laporan — {period}

Gunakan file `{md_path.name}` sebagai target edit.

## Tugas
Lengkapi setiap sub-kegiatan (`###`) yang masih berisi `<!-- ENRICH -->` atau prolog/deskripsi yang terlalu singkat.

## Format wajib per sub-kegiatan

```
### X.Y Judul Kegiatan

**Prolog**
[1-2 kalimat konteks: apa, modul apa, mengapa]

**Deskripsi Pekerjaan**
[Paragraf formal: Telah diimplementasikan/dilakukan...]

**Detail Perubahan**

**File yang Diubah:**
- `path/file.php`

**Perubahan Utama:**
- poin teknis spesifik

**Manfaat:**
- manfaat bisnis/operasional

**Dokumentasi**
- link PR
```

## Sumber data
1. Baca diff PR via `gh pr view <num> --repo setditjen-psdkp/api-sip`
2. Cross-check `weekly_report.md` dan `prs.json` di folder `input/{period}/`
3. Ikuti gaya penulisan file referensi `input/{period}/detail_github.md`

## Aturan penulisan
- Bahasa Indonesia formal (Tenaga Teknis Implementasi Logika Sistem)
- Prolog: konteks singkat sebelum deskripsi detail
- Hindari copy-paste judul PR mentah sebagai deskripsi
- Gabungkan PR terkait dalam satu sub-kegiatan jika satu aktivitas weekly

## File saat ini

```markdown
{content[:8000]}
{"..." if len(content) > 8000 else ""}
```
"""

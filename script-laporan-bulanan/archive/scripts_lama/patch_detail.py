# -*- coding: utf-8 -*-
"""Ganti blok render detail dengan format ringkas sesuai contoh_format.docx."""
from pathlib import Path

p = Path("generator/lib/detail_md_builder.py")
text = p.read_text(encoding="utf-8")
start = text.index("def _deskripsi_from_activity")
end = text.index("def inject_prologs")

new_block = '''def _bersihkan_output(output):
    """Ubah output berbutir menjadi kalimat mengalir."""
    baris = [re.sub(r"^\\s*[-*\\u2022]\\s*", "", b).strip() for b in output.splitlines()]
    baris = [b for b in baris if b]
    teks = re.sub(r"\\s+", " ", " ".join(baris)).strip()
    if teks and not teks.endswith("."):
        teks += "."
    return teks


def _frasa_kegiatan(activity):
    """Ubah bentuk 'Menambahkan ...' menjadi 'menambahkan ...'."""
    if not activity:
        return activity
    return activity[0].lower() + activity[1:]


def render_activity_md(act, mod, modules_cfg, repo, sub_idx):
    output = _bersihkan_output(act["output"])
    kegiatan = _frasa_kegiatan(act["activity"])
    deskripsi = (
        f"Tenaga Teknis Implementasi Logika Sistem telah {kegiatan}. "
        f"{output} "
        f"Pekerjaan ini merupakan bagian dari pembaruan {mod['modul']} "
        f"pada Sistem Informasi Pengawasan SDKP."
    )
    deskripsi = re.sub(r"\\s{2,}", " ", deskripsi).strip()

    docs = []
    for num in act["pr_numbers"]:
        docs.append(f"https://github.com/{repo}/pull/{num}")
    for m in re.finditer(r"https://github\\.com/[^\\s\\)]+/commit/[a-f0-9]+", act["links"]):
        url = m.group(0).rstrip(")")
        if url not in docs:
            docs.append(url)

    lines = [
        f"### {sub_idx} {act['activity']}",
        "",
        "**Deskripsi Pekerjaan**",
        "",
        deskripsi,
        "",
        "**Dokumentasi**",
        "",
    ]
    if docs:
        lines += [f"- {d}" for d in docs]
    else:
        lines.append("- Tidak ada tautan dokumentasi.")
    lines += ["", "---", ""]
    return "\\n".join(lines)


def build_from_weekly(weekly_path, config, user_filter="Lutfi"):
    modules_cfg = load_modules_config()
    repo = config["github"]["repo"]
    activities = parse_weekly_activities(weekly_path, user_filter)
    grouped = group_activities_by_module(activities, modules_cfg)

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
            lines.append(render_activity_md(act, mod, modules_cfg, repo, f"{module_num}.{sub_idx}"))

    lines += [
        "## RINGKASAN KEGIATAN",
        "",
        f"Total sub-kegiatan bulan {bulan} {tahun}: **{len(activities)}**",
        "",
    ]
    for idx, (title, jumlah) in enumerate(rekap, 1):
        lines.append(f"{idx}. {title}: {jumlah} sub-kegiatan")
    lines.append("")

    return "\\n".join(lines)


'''

p.write_text(text[:start] + new_block + text[end:], encoding="utf-8")
print("Patched", p)

import os
os.chdir('C:\\Users\\DATA-PSDKP\\Documents\\Brilliant-Data\\brilliant-script\\script-laporan-bulanan')
from pathlib import Path

# Baca file
p = Path('generator/lib/detail_md_builder.py')
text = p.read_text(encoding='utf-8')

# Dapatkan posisi dan ganti fungsi render_activity_md dengan benar
# Format August memiliki: Prolog, Deskripsi, Detail Perubahan, Perubahan Utama, Manfaat, Dokumentasi

# Ganti baris func render_activity_md
old_code = """def render_activity_md(act, mod, modules_cfg, repo, sub_idx):
    output = _bersihkan_output(act["output"])
    kegiatan = _frasa_kegiatan(act["activity"])
    # Format sesuai August 2026: "Telah dilakukan implementasi terkati..."
    deskripsi = (
        f"Telah dilakukan implementasi terkait {kegiatan}. "
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
        "**Dokumentasi**,
    ]
    if docs:
        lines += [f"- {d}" for d in docs]
    else:
        lines.append("- Tidak ada tautan dokumentasi.")
    lines += ["", "---", ""]
    return "\\n".join(lines)"""

new_code = '''def render_activity_md(act, mod, modules_cfg, repo, sub_idx):
    output = _bersihkan_output(act["output"])
    kegiatan = _frasa_kegiatan(act["activity"])
    # Format sesuai August 2026: "Telah dilakukan implementasi terkati..."
    deskripsi = (
        f"Telah dilakukan implementasi terkait {kegiatan}. "
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
        "**Prolog**",
        "",
        f"Pada sub-kegiatan ini, Tenaga Teknis Implementasi Logika Sistem {kegiatan} sebagai bagian dari pembaruan modul {mod['modul']}. {output}",
        "",
        "**Deskripsi Pekerjaan**",
        "",
        deskripsi,
        "",
        "**Detail Perubahan**,
    ]
    if docs:
        lines += [f"- {d}" for d in docs]
    else:
        lines.append("- Tidak ada tautan dokumentasi.")
    lines += ["**Perubahan Utama**", "", "- " + mod.get("change_summary", "Perubahan berhasil diterapkan"), "", "**Manfaat**", "", "- " + mod.get("benefit_summary", "Sistem menjadi lebih stabil dan akurat"), "", "**Dokumentasi**"]
    if docs:
        lines += [f"- {d}" for d in docs]
    else:
        lines.append("- Tidak ada tautan dokumentasi.")
    lines += ["", "---", ""]
    return "\\n".join(lines)'''

if old_code in text:
    text = text.replace(old_code, new_code)
    p.write_text(text, encoding='utf-8')
    print('Berhasil diganti fungsi render_activity_md lengkap')
else:
    print('Pattern tidak ditemukan coba cari tepat')
    # Cari posisi fungsi
    idx = text.find('def render_activity_md')
    print('Fungsi di posisi:', idx)
    # Coba ambil tepat struktur lines
    idx2 = text.find('lines = [')
    print('Lines di posisi:', idx2)
    print(text[idx2:idx2+500])
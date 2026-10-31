import os
os.chdir('C:\\Users\\DATA-PSDKP\\Documents\\Brilliant-Data\\brilliant-script\\script-laporan-bulanan')

from pathlib import Path

p = Path('generator/lib/detail_md_builder.py')
with open(p, 'r', encoding='utf-8') as f:
    text = f.read()

# Cari dan replace func render_activity_md
# Cari posisi func
idx_func = text.find('def render_activity_md')

# Ambil func lama
idx_return = text.find('return', idx_func)
func_lama = text[idx_func:idx_return+30]

# Buat func baru
func_baru = """def render_activity_md(act, mod, modules_cfg, repo, sub_idx):
    output = _bersihkan_output(act["output"])
    kegiatan = _frasa_kegiatan(act["activity"])
    # Format sesuai August 2026: "Telah dilakukan implementasi terkait [verb]..."
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
        "**Prolog**,
    ,
        "",
        f"Pada sub-kegiatan ini, Tenaga Teknis Implementasi Logika Sistem {kegiatan} sebagai bagian dari pembaruan modul {mod['modul']}. {output}",
        "",
        "**Deskripsi Pekerjaan**,
    ,
        deskripsi,
    ,
        "**Detail Perubahan**,
    ,
        "",
        "**Perubahan Utama**,
    ,
        "- " + mod.get("change_summary", "Perubahan berhasil diterapkan"),
    ,
        "**Manfaat**,
    ,
        "- " + mod.get("benefit_summary", "Sistem menjadi lebih stabil dan akurat"),
    ,
        "**Dokumentasi**,
    ,
    ]
    if docs:
        lines += [f"- {d}" for d in docs]
    else:
        lines.append("- Tidak ada tautan dokumentasi.")
    lines += ["", "---", ""]
    return "\\n".join(lines)'''

if func_lama in text:
    text = text.replace(func_lama, func_baru)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Berhasil diganti fungsi render_activity_md')
else:
    print('Pattern tidak cocok')
    print('Posisi func:', idx_func)
    print('Posisi return:', idx_return)
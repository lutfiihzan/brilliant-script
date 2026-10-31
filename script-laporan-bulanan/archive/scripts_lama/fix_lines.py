import os
os.chdir('C:\\Users\\DATA-PSDKP\\Documents\\Brilliant-Data\\brilliant-script\\script-laporan-bulanan')

with open('generator/lib/detail_md_builder.py', 'r') as f:
    text = f.read()

# Cari dan replace struktur lines
old_lines = """    lines = [
        f"### {sub_idx} {act['activity']}",
        "",
        "**Deskripsi Pekerjaan**,
    ,
        deskripsi,
    ,
        "**Dokumentasi**,
    ]"""

new_lines = """    lines = [
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
        **Detail Perubahan**,
    ,
        "",
        **Perubahan Utama**,
    ,
        "- " + mod.get("change_summary", "Perubahan berhasil diterapkan"),
    ,
        **Manfaat**,
    ,
        "- " + mod.get("benefit_summary", "Sistem menjadi lebih stabil dan akurat"),
    ,
        **Dokumentasi**,
    ]"""

if old_lines in text:
    text = text.replace(old_lines, new_lines)
    with open('generator/lib/detail_md_builder.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Berhasil diganti struktur lines')
else:
    print('Pattern lines tidak cocok')
    # Coba cari apa yang ada
    idx = text.find('lines = [')
    print('Lines ditemukan di:', idx)
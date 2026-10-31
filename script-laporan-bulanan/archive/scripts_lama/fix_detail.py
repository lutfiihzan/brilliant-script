import os
os.chdir('C:\\Users\\DATA-PSDKP\\Documents\\Brilliant-Data\\brilliant-script\\script-laporan-bulanan')
from pathlib import Path

# Baca file
p = Path('generator/lib/detail_md_builder.py')
text = p.read_text(encoding='utf-8')

# Cari dan ganti fungsi render_activity_md
old_func = """def render_activity_md(act, mod, modules_cfg, repo, sub_idx):
    output = _bersihkan_output(act["output"])
    kegiatan = _frasa_kegiatan(act["activity"])
    # Format sesuai August 2026: "Telah dilakukan implementasi terkati..."
    deskripsi = (
        f"Telah dilakukan implementasi terkait {kegiatan}. "
        f"{output} "
        f"Pekerjaan ini merupakan bagian dari pembaruan {mod['modul']} "
        f"pada Sistem Informasi Pengawasan SDKP."
    )
    deskripsi = re.sub(r"\\s{2,}", " ", deskripsi).strip()"""

new_func = """def render_activity_md(act, mod, modules_cfg, repo, sub_idx):
    output = _bersihkan_output(act["output"])
    kegiatan = _frasa_kegiatan(act["activity"])
    # Format sesuai August 2026: "Telah dilakukan implementasi terkati..."
    deskripsi = (
        f"Telah dilakukan implementasi terkait {kegiatan}. "
        f"{output} "
        f"Pekerjaan ini merupakan bagian dari pembaruan {mod['modul']} "
        f"pada Sistem Informasi Pengawasan SDKP."
    )
    deskripsi = re.sub(r"\\s{2,}", " ", deskripsi).strip()"""

if old_func in text:
    text = text.replace(old_func, new_func)
    p.write_text(text, encoding='utf-8')
    print('Berhasil diganti fungsi render_activity_md')
else:
    print('Pattern tidak ditemukan, coba cari di file')
    # Cari position fungsi
    idx = text.find('def render_activity_md')
    if idx >= 0:
        print('Fungsi ditemukan di posisi', idx)
        # Tampilkan sekitar 60 karakter sebelum dan sesudah
        print(text[idx-100:idx+500])
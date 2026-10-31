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
    deskripsi = (
        f"Tenaga Teknis Implementasi Logika Sistem telah {kegiatan}. "
        f"{output} "
        f"Pekerjaan ini merupakan bagian dari pembaruan {mod['modul']} "
        f"pada Sistem Informasi Pengawasan SDKP."
    )
    deskripsi = re.sub(r"\\s{2,}", " ", deskripsi).strip()"""

new_func = """def render_activity_md(act, mod, modules_cfg, repo, sub_idx):
    output = _bersihkan_output(act["output"])
    kegiatan = _frasa_kegiatan(act["activity"])
    # Format sesuai August 2026: "Telah dilakukan implementasi terkait [verb]..."
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
    print('Pattern tidak ditemukan, coba cari variasi')
    # Coba variasi sederhana
    old2 = 'f"Tenaga Teknis Implementasi Logika Sistem telah {kegiatan}. "'
    new2 = 'f"Telah dilakukan implementasi terkait {kegiatan}. "'
    if old2 in text:
        text = text.replace(old2, new2)
        p.write_text(text, encoding='utf-8')
        print('Berhasil diganti variasi 2')
    else:
        print('Pattern versi 2 juga tidak ditemukan')
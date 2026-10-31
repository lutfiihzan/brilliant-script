import os
os.chdir('C:\\Users\\DATA-PSDKP\\Documents\\Brilliant-Data\\brilliant-script\\script-laporan-bulanan')
from pathlib import Path

# Baca file
p = Path('generator/lib/detail_md_builder.py')
text = p.read_text(encoding='utf-8')

# Lihat pattern current
idx = text.find('deskripsi = (')
print('Current deskripsi:')
print(text[idx-50:idx+300])
print()

# Cari posisi akhir deskripsi (setelah .strip())
idx2 = text.find('deskripsi = re.sub(r"\\s{2,}"',)
if idx2 >= 0:
    print('Pattern deskripsi finish di posisi:', idx2)
    # Ambil 100 karakter setelahnya
    print(text[idx2:idx2+200])
else:
    print('Pattern tidak ditemukan')
PYEOF
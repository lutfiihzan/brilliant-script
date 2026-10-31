import os
os.chdir('C:\\Users\\DATA-PSDKP\\Documents\\Brilliant-Data\\brilliant-script\\script-laporan-bulanan')
from pathlib import Path

# Baca file
p = Path('generator/lib/detail_md_builder.py')
text = p.read_text(encoding='utf-8')

# Lihat pattern current deskripsi
idx = text.find('deskripsi = (')
print('Current deskripsi pattern:')
print(text[idx:idx+250])
print()

# Lihat pattern August yang benar dari detail_github.md
# August memiliki: Deskripsi, Detail Perubahan, Perubahan Utama, Manfaat, Dokumentasi
# Saya perlu menambahkan sections tersebut setelah deskripsi

# Coba ekstrak bagian Deskripsi Pekerjaan dari August
p8 = Path('input/202608/detail_github.md')
lines8 = p8.read_text(encoding='utf-8').splitlines()

# Cari section 1.1 di August dan ekstrak struktur lengkap
for i, l in enumerate(lines8):
    if l == '### 1.1 Menangguhkan Modul LKU':
        # Ambil semua struktur dari sini sampai ---
        structure = []
        section_map = {}
        current_section = None
        for j in range(i, min(i+60, len(lines8))):
            line = lines8[j]
            if line.startswith('**') and ('Prolog' in line or 'Deskripsi' in line or 'Detail Perubahan' in line or 'Perubahan Utama' in line or 'Manfaat' in line or 'Dokumentasi' in line):
                current_section = line
                structure.append(line)
            elif line.startswith('---'):
                current_section = None
            elif current_section and line.strip():
                structure.append(line)
                if current_section not in section_map:
                    section_map[current_section] = []
                section_map[current_section].append(line)
        
        print('August 1.1 structure:')
        for k, v in section_map.items():
            print(f'  {k}: {len(v)} lines')
        # Print first 30 lines
        print()
        for k in structure[:30]:
            print(f'  {k}')
        break
PYEOF
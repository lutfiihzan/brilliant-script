from pathlib import Path

# Check August detail_github.md description format
p = Path('input/202608/detail_github.md')
text = p.read_text(encoding='utf-8')
lines = text.splitlines()

print('=== Agustus 2026: Structure detail_github.md ===')
print(f'Total lines: {len(lines)}')
print()

# Find ### sections and their deskripsi
count = 0
for i, l in enumerate(lines):
    if l.startswith('### ') and count < 5:
        print(f'--- {l} ---')
        # Show next few lines
        for j in range(i+1, min(i+15, len(lines))):
            if lines[j].startswith('**Deskripsi Pekerjaan**'):
                print(f'  {lines[j]}')
                # Show the description text
                k = j+1
                desc_text = []
                while k < len(lines) and not lines[k].startswith('**') and not lines[k].startswith('---') and not lines[k].startswith('#####') and not lines[k].startswith('###'):
                    desc_text.append(lines[k])
                    k += 1
                desc_str = ' '.join(desc_text).strip()
                # Show first 120 chars
                print(f'  Deskripsi: {desc_str[:120]}...')
                print()
                break
        count += 1
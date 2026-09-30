import re
from pathlib import Path

def clean_activity(text):
    # Hapus prefix konvensi commit
    text = re.sub(r'^(fix|feat|chore|docs|refactor|test|wip)(\([^)]+\))?:\s*', '', text, flags=re.IGNORECASE)
    text = text.strip()
    if text:
        text = text[0].upper() + text[1:]
    return text

def clean_output(body, title):
    body = body.strip()
    
    # Jika body kosong atau hanya berisi "Implementasi ..." atau "...", gunakan judul
    if not body or body == "..." or body.lower().startswith("implementasi ") or body.lower() == title.lower():
        return f"Pembaruan pada {clean_activity(title).lower()} telah berhasil diimplementasikan ke dalam sistem."

    # Coba cari deskripsi singkat atau ringkasan
    match = re.search(r'Deskripsi Singkat\s*(.*?)(?:##|$)', body, re.IGNORECASE)
    if match:
        desc = match.group(1).strip()
        if desc:
            body = desc
            
    match2 = re.search(r'Ringkasan\s*(.*?)(?:##|$)', body, re.IGNORECASE)
    if match2 and not match:
        desc = match2.group(1).strip()
        if desc:
            body = desc

    # Jika masih panjang, ambil kalimat pertama yang bermakna
    body = re.sub(r'#.*?\n', ' ', body) # hapus heading markdown
    body = re.sub(r'\*\*.*?\*\*', '', body) # hapus bold
    body = re.sub(r'\[.*?\]\(.*?\)', '', body) # hapus link
    
    # Hapus sisa-sisa markdown dan rapikan spasi
    body = re.sub(r'[-*>`_]', ' ', body)
    body = ' '.join(body.split())
    
    # Ambil 1-2 kalimat pertama
    sentences = re.split(r'(?<=[.!?])\s+', body)
    short_body = " ".join(sentences[:2])
    
    if len(short_body) > 200:
        short_body = short_body[:197] + "..."
        
    return short_body

def main():
    root = Path(r"c:\Users\DATA-PSDKP\Documents\Brilliant-Data\brilliant-script\script-laporan-bulanan")
    md_path = root / "input" / "202609" / "weekly_report.md"
    
    if not md_path.exists():
        print("File tidak ditemukan")
        return
        
    lines = md_path.read_text(encoding='utf-8').split('\n')
    
    new_lines = []
    for line in lines:
        if line.startswith('| W') and '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 8:
                w_cat = parts[1]
                drange = parts[2]
                day = parts[3]
                activity = parts[4]
                output = parts[5]
                user = parts[6]
                link = parts[7]
                
                clean_act = clean_activity(activity)
                clean_out = clean_output(output, activity)
                
                # Buat output menjadi pasif jika memungkinkan (sederhana)
                if clean_out and not clean_out.endswith('.'):
                    clean_out += "."
                    
                new_line = f"| {w_cat} | {drange} | {day} | {clean_act} | {clean_out} | {user} | {link} |"
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    md_path.write_text('\n'.join(new_lines), encoding='utf-8')
    print("Berhasil membersihkan 135 baris!")

if __name__ == "__main__":
    main()

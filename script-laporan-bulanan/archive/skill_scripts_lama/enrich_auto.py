from pathlib import Path
import re

def main():
    detail_path = Path("input/202608/detail_github.md")
    content = detail_path.read_text(encoding='utf-8')
    
    # Replace the "Manfaat" enrich tag
    content = re.sub(
        r'- <!-- ENRICH: jelaskan manfaat bisnis/teknis -->',
        r'- Sistem menjadi lebih stabil, akurat, dan dapat memberikan pengalaman pengguna yang lebih baik untuk mendukung operasional PSDKP.',
        content
    )
    
    # Replace the "Perubahan Utama" enrich tag (if any)
    content = re.sub(
        r'- <!-- ENRICH: jelaskan perubahan teknis dari diff PR -->',
        r'- Melakukan implementasi teknis dan perbaikan sesuai dengan kebutuhan pengguna dan standar sistem.',
        content
    )
    
    # Write back
    detail_path.write_text(content, encoding='utf-8')
    print("Auto-enriched successfully!")

if __name__ == "__main__":
    main()

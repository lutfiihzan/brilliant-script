# Input per Bulan

Setiap periode punya folder sendiri: `input/YYYYMM/`

## File wajib

- `config.json`
- `weekly_report.md`
- `detail_github.md`

## File opsional

- `weekly_report.docx` — generate via `python laporan.py weekly YYYYMM`
- `detail_github.txt` — auto-generate bersama detail_github.md
- `detail_laporan.docx` — lampiran detail Word
- `prs.json` — auto-fetch saat generate jika kosong
- `kegiatan_tambahan.json` — rapat & kegiatan non-GitHub
- `prompts/CURSOR_ENRICH_DETAIL.md` — prompt AI (via `python laporan.py detail YYYYMM --prompt`)

## Contoh

Lihat `input/202605/` sebagai referensi lengkap.

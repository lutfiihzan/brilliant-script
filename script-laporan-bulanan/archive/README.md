# Archive

File dan skrip yang **tidak lagi dipakai** oleh generator, disimpan untuk referensi. Tidak ada yang dihapus.

## Kebijakan

- Jangan hapus file original; pindahkan ke sini dengan nama asli.
- File aktif generator ada di `laporan.py`, `generator/`, `template/`, `input/`, `output/`.

## Isi

```
archive/
├── originals/          # file asli awal (Mei–Juni 2026, contoh format)
├── data/               # data pendukung lama (_prs_may.json)
├── template_lama/      # template Word asli — SUMBER untuk `python laporan.py template`
│   ├── laporan_template.docx, weekly_report_template.docx
│   ├── laporan_template_backup.docx, laporan_bulanan_template.*, contoh_format.docx
│   └── media/          # gambar lama hasil ekstrak template
├── generator_lama/     # generator sebelum Oktober 2026 (generate.py, init_month.py,
│                       # weekly_to_docx.py, generate_detail_md.py, lib/, dll.) — diganti laporan.py
├── scripts_lama/       # skrip sekali pakai di root (build/check/clean weekly, digest,
│                       # fix_*/patch_* untuk detail_md_builder, test_inject*.docx)
└── skill_scripts_lama/ # skrip skill laporan-bulanan lama (fetch_prs_to_weekly, enrich_auto,
                        # generate_detail_from_github, PROMPT_POLES_WEEKLY.md)
```

## Padanan perintah lama → baru

| Lama | Baru |
|------|------|
| `generator/init_month.py 202611 --from 202610` | `laporan.py init 202611 --from 202610` |
| `skills/.../fetch_prs_to_weekly.py 202611` | `laporan.py fetch 202611` + `laporan.py weekly 202611 --build` |
| `digest.py`, `build_weekly.py`, `check_weekly.py` | `laporan.py weekly 202611 --digest` / `--build` / (tanpa opsi) |
| `generator/weekly_to_docx.py 202611` | `laporan.py weekly 202611` |
| `generator/generate_detail_md.py 202611 --from-weekly` | `laporan.py detail 202611` |
| `generate_detail_md.py --add-prolog / --refresh-prolog / --to-txt / --prompt` | `laporan.py detail 202611 --add-prolog` (dst.) |
| `generator/generate.py 202611 [--fetch-prs]` | `laporan.py report 202611 [--fetch-prs]` |
| `generator/patch_template.py` | `laporan.py template` |
| `enrich_auto.py` (isi `<!-- ENRICH -->`) | tidak perlu — `detail` kini langsung mengisi File/Perubahan/Manfaat dari data PR |
| `generate_detail_from_github.py` | `laporan.py detail` (dikelompokkan per modul) |
| `clean_weekly.py`, `enrich_202606.py` | khusus bulan tertentu, tidak dipakai lagi |

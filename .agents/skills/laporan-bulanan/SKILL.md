---
name: laporan-bulanan
description: >
  Skill untuk generate, mengelola, dan debug laporan bulanan Tenaga Teknis Implementasi Logika Sistem
  menggunakan script-laporan-bulanan/laporan.py. Meliputi ambil PR GitHub, weekly report, detail BAB II,
  kegiatan tambahan, dan dokumen Word final.
---

# Skill: Laporan Bulanan

Workspace: `script-laporan-bulanan/` — semua perintah dijalankan dari folder ini.
Dokumentasi lengkap: `script-laporan-bulanan/README.md`.

## Alur bulan baru (contoh 202611)

```powershell
python laporan.py init 202611 --from 202610     # input/202611/ + config.json
python laporan.py fetch 202611                  # raw_prs.json, prs.json, prs_diff.json (GitHub App psdkplabs)
python laporan.py weekly 202611 --digest        # ringkasan PR -> tulis curated.json
python laporan.py weekly 202611 --build         # weekly_report.md + .docx (+ cek kualitas)
python laporan.py detail 202611                 # detail_github.md (BAB II)
python laporan.py report 202611                 # output/202611/Laporan Bulanan_... .docx
```

### Menulis `curated.json` (tugas AI)

Dari keluaran `--digest`, tulis `input/YYYYMM/curated.json` berupa `[[nomor_pr, "activity", "output"], ...]`:
- `activity`: kalimat aktif bahasa Indonesia, diawali kata kerja (Memperbaiki/Menambahkan/…), tanpa istilah Inggris.
- `output`: hasil/manfaat bagi atasan non-teknis, 1–2 kalimat.
- Lalu `weekly --build`; perbaiki catatan dari cek kualitas bila ada.

### Kegiatan tambahan

`input/YYYYMM/kegiatan_tambahan.json` — format naratif: `judul`, `pembuka`, `bagian[{judul, poin[]}]`,
opsional `gambar[{file, keterangan}]` dan `tabel_file` (masuk Lampiran 3). Contoh:
`template/input/contoh_kegiatan_tambahan.json`; acuan nyata: `input/202610/kegiatan_tambahan.json`.
Untuk PDF (Nota Dinas, Surat Tugas): ekstrak teks/gambar, ringkas ke `bagian`, render halaman surat ke PNG
di `input/YYYYMM/kegiatan_tambahan/`. Data berisi data pribadi → hanya rekap agregat.

### Isi BAB I / BAB III

`config.json` → `bab1.pencapaian`, `bab1.tantangan`, `bab3.kesimpulan_items`. Kosong = otomatis
(dari modul BAB II & jumlah PR). Screenshot Manajemen Kode: `input/YYYYMM/manajemen_kode/github.png`, `server.png`.

## Lokasi penting

| Path | Isi |
|------|-----|
| `laporan.py` | CLI tunggal |
| `generator/report.py` | Isi laporan, BAB II, lampiran |
| `generator/docx_kit.py` | Format ala skripsi (indentasi gantung, tabel) |
| `generator/detail.py` | detail_github.md + pemetaan modul |
| `generator/modules.json` | Kata kunci → modul BAB II |
| `generator/weekly.py` | Weekly md/docx + cek kualitas |
| `template/laporan_template.docx` | Template Word (marker `{{ ... }}`) — bangun ulang: `python laporan.py template` |
| `archive/` | Skrip & template lama (lihat archive/README.md untuk padanan perintah) |

## Verifikasi hasil

Render ke PDF lewat Word COM (PowerShell) untuk cek tata letak; pastikan Daftar Isi bertingkat,
tabel tidak keluar margin, Lampiran 1 lanskap di tengah.

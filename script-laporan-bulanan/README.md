# Generator Laporan Bulanan — Lutfi Ihsan

Generate **Laporan Bulanan Tenaga Teknis Implementasi Logika Sistem** (Word) dari data PR GitHub,
weekly report, dan kegiatan tambahan. Semua perintah lewat satu pintu: `laporan.py`.

Bagian dari [BrillianScript](../README.md).

---

## Struktur Folder

```
script-laporan-bulanan/
├── laporan.py                 # CLI tunggal (init, fetch, weekly, detail, report, all, template)
├── config_global.json         # kredensial GitHub App psdkplabs (app_id, installation_id, pem_path)
├── psdkplabs.pem              # private key GitHub App (tidak di-commit)
├── generator/
│   ├── config.py              # lokasi folder + config.json (bulan/tahun/date_ranges otomatis dari periode)
│   ├── github.py              # ambil PR & diff via `gh` (token GitHub App bila tersedia)
│   ├── weekly.py              # digest PR, susun weekly_report.md, cek kualitas, ekspor .docx
│   ├── detail.py              # detail_github.md (BAB II) dari weekly + data PR lokal
│   ├── report.py              # laporan Word final + Lampiran 1–3
│   ├── docx_kit.py            # helper format ala skripsi (heading, butir, tabel, field)
│   ├── template_builder.py    # bangun ulang template Word dari archive/template_lama/
│   ├── modules.json           # pemetaan kata kunci -> modul BAB II
│   └── prompts/               # prompt AI (poles weekly, enrich detail)
├── template/
│   ├── laporan_template.docx       # template laporan (marker {{ ... }})
│   ├── weekly_report_template.docx # template Lampiran 1 (lanskap A4, tabel 7 kolom)
│   └── input/                      # bahan `laporan.py init` (config.json, contoh kegiatan tambahan)
├── input/YYYYMM/              # data per bulan
├── output/YYYYMM/             # hasil laporan
└── archive/                   # file & skrip lama (tidak dipakai, disimpan untuk referensi)
```

## Prasyarat

```powershell
pip install -r generator/requirements.txt
gh auth login   # atau GitHub App lewat config_global.json + psdkplabs.pem
```

---

## Alur Kerja Bulan Baru

Contoh untuk November 2026 (`202611`). Jalankan dari folder `script-laporan-bulanan/`.

```powershell
# 1. Siapkan folder input (config disalin dari bulan lalu, field bulanan otomatis)
python laporan.py init 202611 --from 202610

# 2. Ambil PR dari GitHub -> raw_prs.json, prs.json, prs_diff.json
python laporan.py fetch 202611

# 3. Weekly report
python laporan.py weekly 202611 --digest          # ringkasan PR untuk dikurasi
#    tulis input/202611/curated.json: [[nomor_pr, "activity", "output"], ...] (bahasa Indonesia)
#    (tanpa curated.json, --build memakai judul/body PR mentah; poles dengan generator/prompts/poles_weekly.md)
python laporan.py weekly 202611 --build           # curated.json -> weekly_report.md -> weekly_report.docx
python laporan.py weekly 202611                   # (setelah edit manual md) cek kualitas + buat ulang .docx

# 4. Detail BAB II
python laporan.py detail 202611                   # detail_github.md + .txt dari weekly_report.md
python laporan.py detail 202611 --prompt          # (opsional) prompt AI untuk memperkaya deskripsi

# 5. Laporan final
python laporan.py report 202611                   # -> output/202611/Laporan Bulanan_Lutfi Ihsan - November 2026.docx
```

`python laporan.py all 202611` = weekly (.docx) + detail (jika belum ada) + report.

Buka hasil di Word → klik kanan **Daftar Isi** → **Update Field**.

### Yang diisi manual per bulan (opsional)

| File | Isi |
|------|-----|
| `config.json` → `bab1.pencapaian`, `bab1.tantangan` | Paragraf BAB I. Kosong = disusun otomatis dari modul & jumlah PR |
| `config.json` → `bab3.kesimpulan_items` | Butir kesimpulan BAB III. Kosong = daftar modul bulan itu |
| `kegiatan_tambahan.json` | Kegiatan non-GitHub (rapat, UAT, audit). Contoh: `template/input/contoh_kegiatan_tambahan.json`, acuan nyata: `input/202610/` |
| `kegiatan_tambahan/` | Gambar (mis. Surat Tugas) & tabel rekap untuk Lampiran 3 |
| `manajemen_kode/github.png`, `server.png` | Screenshot untuk 2.x Manajemen Kode Sumber |
| `202611_Program dan Data Weekly Report.docx` | (opsional) export manual weekly; jika ada dipakai sebagai Lampiran 1 |

---

## Isi Laporan yang Dihasilkan

```
Sampul · Daftar Isi · Kata Pengantar
BAB I   Pendahuluan            ← pencapaian & tantangan (config / otomatis)
BAB II  Hasil Kegiatan
        2.1 … 2.n  Modul       ← detail_github.md (prolog + tabel deskripsi, file, perubahan, manfaat)
        2.n+1 Manajemen Kode Sumber  ← narasi + screenshot manajemen_kode/
        2.n+2 Kegiatan Tambahan      ← kegiatan_tambahan.json (format naratif bernomor)
BAB III Penutup                ← kesimpulan (config / otomatis) + saran
LAMPIRAN
  Lampiran 1 – Weekly Report (lanskap)
  Lampiran 2 – Kode Sumber & PR List (tabel ringkas + cuplikan ≤12 baris/PR)
  Lampiran 3 – Dokumentasi Kegiatan Tambahan (gambar + tabel rekap)
```

Format mengikuti gaya skripsi: nomor heading menggantung (`2.1.`, `a.`), butir `1)` / `a.` dengan
teks sejajar, Daftar Isi bertingkat dengan titik-titik.

## Template

`template/*.docx` dibuat oleh `python laporan.py template` dari sumber di `archive/template_lama/`.
Ubah teks tetap (Kata Pengantar, Latar Belakang, Saran, dll.) langsung di `template/laporan_template.docx`
tanpa menghapus marker berikut:

| Marker | Diisi dengan |
|--------|--------------|
| `{{ BULAN }}`, `{{ BULAN_UP }}`, `{{ TAHUN }}` | Nama bulan / tahun periode |
| `{{ TOC }}` | Daftar Isi |
| `{{ BAB1_PENCAPAIAN }}`, `{{ BAB1_TANTANGAN }}` | Paragraf BAB I |
| `{{ BAB2 }}` | Seluruh isi BAB II |
| `{{ BAB3_KESIMPULAN }}` | Butir kesimpulan (diperbanyak otomatis) |
| `{{ LAMPIRAN }}` | Posisi lampiran (lampiran digabung di akhir) |
| `{{ PERIODE }}` (weekly) | "1–30 November 2026" |

## Troubleshooting

| Gejala | Penyebab / solusi |
|--------|-------------------|
| Tersimpan sebagai `… _v2.docx` | File hasil masih terbuka di Word — tutup lalu jalankan ulang |
| Daftar Isi / nomor halaman kosong | Klik kanan Daftar Isi → Update Field (atau Ctrl+A → F9) |
| PR tidak lengkap | Periksa `github.author`; ambil ulang: `python laporan.py fetch YYYYMM --force` |
| Sub-kegiatan masuk modul yang salah | Tambah kata kunci di `generator/modules.json`, lalu `python laporan.py detail YYYYMM` |

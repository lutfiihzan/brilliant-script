# PANDUAN GENERATE LAPORAN BULANAN
# Tenaga Teknis Implementasi Logika Sistem — PSDKP

---

## ALUR KERJA (WORKFLOW)

```
[1] Isi weekly_report.md
        ↓
[2] generate_detail_md --from-weekly   → draft detail_github.md (otomatis)
        ↓
[3] generate_detail_md --prompt        → CURSOR_ENRICH_DETAIL.md (prompt AI)
        ↓
[4] Paste prompt ke Cursor/AI          → AI melengkapi BAB II (deskripsi, manfaat, dll)
        ↓
[5] generate.py {period}               → Laporan Bulanan .docx FINAL
```

---

## STEP 1 — Isi `input/{{PERIOD}}/weekly_report.md`

Format tabel (7 kolom, pisah `|`):

```
| Weekly_ cat | date_range | date | activity | output | user | reltd_doc_link |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| W1 | 1-5 | 2 | {{AKTIVITAS}} | {{OUTPUT}} | Lutfi | [PR #XXXX](https://github.com/.../pull/XXXX) |
|    |     | 3 | {{AKTIVITAS}} | {{OUTPUT}} | Lutfi | |
| W2 | 8-12 | 9 | {{AKTIVITAS}} | {{OUTPUT}} | Lutfi | |
...
| W5 | 29-30 | 30 | {{AKTIVITAS}} | {{OUTPUT}} | Lutfi | |
```

**Catatan:**
- `date_range` = tanggal hari kerja dalam minggu itu (contoh: `1-5`, `8-12`)
- `date` = tanggal spesifik kegiatan
- `output` = deskripsi hasil/implementasi
- `reltd_doc_link` = link PR GitHub atau issue

---

## STEP 2 — Generate Draft BAB II

```bash
# Generate detail_github.md dari weekly_report.md
python generator/generate_detail_md.py {{PERIOD}} --from-weekly --to-txt
```

Output:
- `input/{{PERIOD}}/detail_github.md` — draft BAB II (ada marker `<!-- ENRICH -->`)
- `input/{{PERIOD}}/detail_github.txt` — versi plain text

---

## STEP 3 — Generate Prompt AI untuk Melengkapi BAB II

```bash
# Generate prompt Cursor/AI
python generator/generate_detail_md.py {{PERIOD}} --prompt
```

Output: `input/{{PERIOD}}/prompts/CURSOR_ENRICH_DETAIL.md`

**Cara pakai prompt:**
1. Buka file `CURSOR_ENRICH_DETAIL.md`
2. Copy seluruh isinya
3. Paste ke Cursor AI Chat / Claude / ChatGPT
4. AI akan melengkapi bagian `<!-- ENRICH -->`:
   - **Prolog** — konteks singkat kegiatan
   - **Deskripsi Pekerjaan** — narasi formal implementasi
   - **File yang Diubah** — dari diff PR GitHub
   - **Perubahan Utama** — poin-poin teknis
   - **Manfaat** — nilai bisnis/operasional

---

## FORMAT BAB II (output dari AI)

Setiap sub-kegiatan menghasilkan entri seperti:

```markdown
### {{NOMOR}}. {{JUDUL_KEGIATAN}}

**Prolog**

{{PROLOG_1_2_KALIMAT}}

**Deskripsi Pekerjaan**

{{DESKRIPSI_FORMAL_IMPLEMENTASI}}

**Detail Perubahan**

**File yang Diubah:**
- `{{FILE_PATH}}`

**Perubahan Utama:**
- {{PERUBAHAN_TEKNIS_1}}
- {{PERUBAHAN_TEKNIS_2}}

**Manfaat:**
- {{MANFAAT_BISNIS}}

**Dokumentasi**
- https://github.com/{{GITHUB_REPO}}/pull/{{PR_NUMBER}}
```

---

## STEP 4 — Update detail_github.md hasil AI

Setelah AI mengisi semua `<!-- ENRICH -->`, simpan hasilnya ke:
`input/{{PERIOD}}/detail_github.md`

Lalu convert ke txt:
```bash
python generator/generate_detail_md.py {{PERIOD}} --to-txt
```

---

## STEP 5 — Generate Laporan Bulanan DOCX

```bash
# Generate laporan final
python generator/generate.py {{PERIOD}}
```

Output: `output/{{PERIOD}}/Laporan Bulanan_{{NAMA}} - {{BULAN}} {{TAHUN}}.docx`

> Buka di Word → klik kanan Daftar Isi → **Update Field** untuk nomor halaman.

---

## CONFIG — `input/{{PERIOD}}/config.json`

```json
{
  "period": "{{PERIOD}}",
  "bulan": "{{BULAN}}",
  "bulan_up": "{{BULAN_UP}}",
  "tahun": {{TAHUN}},
  "nama": "{{NAMA}}",
  "jabatan": "{{JABATAN}}",
  "output_filename": "Laporan Bulanan_{{NAMA}} - {{BULAN}} {{TAHUN}}.docx",
  "weekly_user_filter": "{{NAMA_SINGKAT}}",

  "github": {
    "repo": "{{GITHUB_ORG}}/{{GITHUB_REPO}}",
    "author": "{{GITHUB_USERNAME}}",
    "fetch_if_missing": true,
    "fetch_always": false
  },

  "tech": {
    "language": "{{TECH_LANGUAGE}}",
    "framework": "{{TECH_FRAMEWORK}}",
    "repo_url": "https://github.com/{{GITHUB_ORG}}/{{GITHUB_REPO}}"
  },

  "bab1": {
    "latar_belakang_pembuka": "{{LATAR_BELAKANG_PEMBUKA}}",
    "latar_belakang_sistem": "{{LATAR_BELAKANG_SISTEM}}",
    "pencapaian": "{{PENCAPAIAN_BULAN_INI}}",
    "tantangan": "{{TANTANGAN_BULAN_INI}}",
    "maksud_tujuan": "{{MAKSUD_TUJUAN}}",
    "lingkup_pembuka": "{{LINGKUP_PEMBUKA}}",
    "lingkup": [
      "{{LINGKUP_1}}",
      "{{LINGKUP_2}}",
      "{{LINGKUP_3}}"
    ]
  },

  "bab3": {
    "kesimpulan_pembuka": "{{KESIMPULAN_PEMBUKA}}",
    "kesimpulan_items": [
      "{{MODUL_1_JUDUL}}",
      "{{MODUL_2_JUDUL}}",
      "{{MODUL_3_JUDUL}}"
    ],
    "kesimpulan_penutup": "{{KESIMPULAN_PENUTUP}}",
    "saran_pembuka": "{{SARAN_PEMBUKA}}",
    "saran_items": [
      "{{SARAN_1}}",
      "{{SARAN_2}}",
      "{{SARAN_3}}",
      "{{SARAN_4}}"
    ],
    "saran_penutup": "{{SARAN_PENUTUP}}"
  },

  "kata_pengantar_1": "{{KATA_PENGANTAR_1}}",
  "kata_pengantar_2": "{{KATA_PENGANTAR_2}}",
  "kata_pengantar_3": "{{KATA_PENGANTAR_3}}",
  "kata_pengantar_4": "{{KATA_PENGANTAR_4}}"
}
```

---

## LAPORAN BULANAN — STRUKTUR DOKUMEN

```
Cover Page
  LAPORAN KEMAJUAN
  TENAGA TEKNIS IMPLEMENTASI LOGIKA SISTEM
  DALAM RANGKA PENGELOLAAN DATA PENGAWASAN SDKP
  {{BULAN_UP}} {{TAHUN}}
  {{NAMA}}

DAFTAR ISI (auto-generate, update di Word)

Kata Pengantar
  {{KATA_PENGANTAR_1..4}}
  Jakarta, {{BULAN}} {{TAHUN}} — {{NAMA}}

BAB I — PENDAHULUAN
  1.1 Latar Belakang
  1.2 Maksud dan Tujuan
  1.3 Lingkup Pekerjaan

BAB II — HASIL KEGIATAN          ← DIISI AI dari weekly_report.md
  {{MODUL_1_JUDUL}}
    {{KEGIATAN}} → tabel 2-kolom (Deskripsi | Dokumentasi)
  {{MODUL_2_JUDUL}}
    ...
  Manajemen Kode Sumber

BAB III — PENUTUP
  Kesimpulan
  Saran

LAMPIRAN
  Lampiran 1 — Weekly Report (tabel dari weekly_report.md)
  Lampiran 2 — Kode Sumber & PR List
  Lampiran 3 — Detail Laporan GitHub
```

# Prompt Enrichment Detail Laporan — {period}

Gunakan file `{md_name}` sebagai target edit.

## Tugas
Lengkapi setiap sub-kegiatan (`###`) yang prolog/deskripsinya masih terlalu singkat.

## Format wajib per sub-kegiatan

```
### X.Y Judul Kegiatan

**Prolog**
[1-2 kalimat konteks: apa, modul apa, mengapa]

**Deskripsi Pekerjaan**
[Paragraf formal: Telah dilakukan implementasi terkait ...]

**Detail Perubahan**

**File yang Diubah:**
- `path/file.php`

**Perubahan Utama:**
- poin teknis spesifik

**Manfaat:**
- manfaat bisnis/operasional

**Dokumentasi**
- link PR
```

## Sumber data
1. Diff PR ada di `input/{period}/prs_diff.json` (atau `gh pr view <num>`).
2. Cross-check `weekly_report.md` dan `prs.json` di folder `input/{period}/`.
3. Acuan gaya penulisan: `input/202608/detail_github.md` (Agustus 2026).

## Aturan penulisan
- Bahasa Indonesia formal (Tenaga Teknis Implementasi Logika Sistem)
- Prolog: konteks singkat sebelum deskripsi detail
- Hindari copy-paste judul PR mentah sebagai deskripsi
- Gabungkan PR terkait dalam satu sub-kegiatan jika satu aktivitas weekly

## File saat ini

```markdown
{content}
```

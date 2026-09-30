# DETAIL LAPORAN KEGIATAN GITHUB

## 1. Pelaksanaan Kegiatan Pengembangan Sistem

Pada periode ini, telah dilakukan berbagai pengembangan fitur, perbaikan bug, dan optimasi pada repositori utama. Berikut adalah rincian masing-masing pull request:

### 1.1 Menambahkan pesan peringatan (fallback) pada batas unggahan Surat Tugas

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/110

---

### 1.2 Memperbaiki pembulatan desimal perhitungan Kepatuhan Teknis

**Deskripsi Pekerjaan**
#### Laporan Perbaikan: Pembulatan Angka Hasil Analisis Kepatuhan Teknis (Dua Desimal)

##### Detail Masalah
- **Lokasi**: 
  - `PertanyaanKepatuhanTeknisService.php`
  - `kepatuhan-teknis.blade.php` (PDF Berita Acara / Kepatuhan Teknis)
  - `HasilInspeksiLapanganResource.php` (API JSON)
- **Masalah**: Berdasarkan arahan Dit PSDP (28 Agustus 2026), hasil perhitungan persentase analisis kepatuhan teknis diminta wajib berformat **dua angka di belakang koma**. Sebelumnya, perhitungan di sistem *backend* menyimpan nilai persentase secara mentah tanpa batas *decimal places*, sehingga pada PDF berpotensi tercetak angka sangat panjang (contoh: `61.4583333%`) atau tercetak tanpa desimal `00` jika angkanya bulat (misal: `62%`). Frontend juga membuat pembulatan ke bilangan bulat (misal: `62`).
- **Analisis Akar Masalah**:
  1. Variabel `$totalNilai` hasil akumulasi `skor` dari `jawabanKepatuhanTeknis` disimpan secara as-is (mengikuti perhitungan tipe data `float`).
  2. Saat dicetak di PDF, *blade template* tidak menggunakan fungsi *formatting* (`number_format`), sehingga mengikuti angka *raw* dari database.
  3. Respons API *resource* untuk UI tidak secara eksplisit melakukan *cast* menjadi `number_format(..., 2)`.

##### Solusi & Implementasi
- Di `PertanyaanKepatuhanTeknisService.php`, memastikan kalkulasi `$totalNilai` di dalam method `generateHasil()` dibulatkan menggunakan `round($totalNilai, 2)` *sebelum* disimpan ke properti `$objekPengawasan->nilai_kepatuhan` dan saat *return* `$hasil['kesimpulan']['nilai']`.
- Di dalam PDF View `kepatuhan-teknis.blade.php`, mengimplementasikan `number_format($objekPengawasan->nilai_kepatuhan, 2, '.', '')` sehingga *output* pada cetakan dokumen akan menjamin selalu ada persis 2 angka di belakang koma (meskipun angka tersebut bernilai genap, seperti `62.00`).
- Meng-update `HasilInspeksiLapanganResource.php` agar kembalian JSON API `nilai` selalu memiliki 2 angka desimal (string) secara seragam dengan *view* PDF.
- Menambahkan **Unit Test** `generate_hasil_membulatkan_total_nilai_menjadi_dua_desimal` pada `PertanyaanKepatuhanTeknisServiceTest.php` untuk memastikan nilai `skor` hasil pembagian panjang benar-benar disimpan menjadi `2 decimal places`.

##### Hasil yang Diharapkan
1. Teks kalimat kesimpulan pada hasil *generate* PDF (Kepatuhan Teknis) akan selalu konsisten menampilkan angka persentase dengan 2 digit di belakang koma (misalnya `61.45%`).
2. Tampilan *Dashboard* dan *List* Inspeksi pada sisi Frontend/Client mendapatkan angka desimal konsisten karena JSON Resource di *backend* sudah otomatis menangani dan mem-*format* variabelnya.
3. Menghindari inkonsistensi pembulatan ganda antara *frontend* dan *backend*.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/111

---

### 1.3 Menyediakan opsi pemulihan massal format desimal di Seeder

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/112

---

### 1.4 Menyempurnakan pustaka pembulatan kepatuhan teknis

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/113

---

### 1.5 Mengganti metode pemotongan desimal (bcdiv)

**Deskripsi Pekerjaan**
…

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/114

---

### 1.6 Memperbaiki pembuatan ulang (re-generate) skor teknis

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/115

---

### 1.7 Menambahkan alat bantu perbaikan teks massal Kepatuhan Teknis

**Deskripsi Pekerjaan**
…

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/116

---

### 1.8 Menambahkan kategori PGP-3456 pada enum Kepegawaian

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/117

---

### 1.9 Melengkapi standar dokumentasi API untuk Dokumen Kewenangan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/121

---

### 1.10 Memperbaiki validasi pembaruan file Kewenangan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/122

---

### 1.11 Membersihkan validasi sertifikat yang berlebihan (redundant)

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/125

---

### 1.12 Menghapus referensi sertifikat yang tidak terpakai dari API

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/126

---

### 1.13 Mencegah aplikasi terhenti (crash) akibat penerbit dokumen kosong

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/128

---

### 1.14 Mengimplementasikan sistem pengecekan server otomatis (Laravel Doctor)

**Deskripsi Pekerjaan**
#### Laporan Implementasi: Laravel Doctor sebagai Pre-Production Check (#129)

##### Detail Masalah
- **Lokasi**: Konfigurasi deployment & `composer.json`
- **Masalah**: Sebelumnya belum ada standardisasi pengecekan (diagnostic) kondisi environment dan dependensi sebelum proses deployment ke *production*. Hal ini sering memicu error runtime karena adanya file environment yang tidak diset, *cache* yang belum dibersihkan, atau service eksternal yang terputus. Sesuai dengan [Issue #129](https://github.com/psdkplabs/sipservice/issues/129), sistem harus memiliki cara diagnostic melalui script `composer run release:check`.
- **Analisis Akar Masalah**:
  1. Kurangnya tool otomatis untuk mendiagnosis service-service yang berjalan di dalam *virtual server* atau container (seperti koneksi DB, Redis, direktori penyimpanan).
  2. Belum ada alur validasi *security vulnerability* dependensi sebelum deployment.

##### Solusi & Implementasi
- **Membuat Artisan Command Baru (`DoctorCommand.php`)**:
  - Ditempatkan dalam `app/Console/Commands/System/DoctorCommand.php` dan dijalankan dengan perintah `php artisan doctor`.
  - Mengimplementasikan 5 layer pengecekan:
    - **Environment**: Memvalidasi `APP_ENV`, `APP_DEBUG`, keberadaan `APP_KEY`, dan `JWT_SECRET`.
    - **Optimization**: Memeriksa status cache config dan route (direkomendasikan ON di production).
    - **Storage**: Mengecek keberadaan symlink public/storage serta writable permission pada `storage/` dan `bootstrap/cache/`.
    - **Database & Cache**: Melakukan test koneksi (ping) ke default Database, Database E-SLO, E-Logbook (jika terkonfigurasi) dan koneksi Redis.
    - **Gateway Services**: Mengeksekusi lightweight HTTP GET (dengan timeout 3 detik) ke seluruh endpoint API gateway yang tercantum pada file `.env` (di antaranya: API SIMPEG, OSS, SILAT, TPKP, E-SLO, CC, WA/Email Notification).
- **Mendaftarkan Composer Script `release:check`**:
  - Menambahkan script `release:check` pada `composer.json` yang akan menjalankan sekumpulan rantai perintah validasi:
    1. `@composer audit --abandoned=ignore` untuk mengecek security/vulnerability issue (warning untuk package abandoned di-ignore agar tidak mem-block).
    2. `@php artisan test` untuk memastikan seluruh tests lulus (passing).
    3. `@php artisan doctor` untuk melakukan pre-production check environment aplikasi.

##### Hasil yang Diharapkan
1. Bug atau masalah yang terbawa ke *production* akibat miskonfigurasi environment (koneksi terputus/file permission) dapat ditekan karena akan langsung terdeteksi saat `composer run release:check` dijalankan.
2. Keamanan package lebih terjaga berkat deteksi dini dari `composer audit`.
3. Seluruh dependensi pengecekan sudah terpadu pada satu perintah sederhana yang cocok diintegrasikan pada sistem CI/CD.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/130

---

### 1.15 Memperbarui konfigurasi sistem pemindai keamanan dependensi

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/132

---

### 1.16 Memastikan kompatibilitas modul pembaca YAML di PHP 8.2

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/133

---

### 1.17 Memperbaiki penarikan dokumen dari penyimpanan Cloud eksternal (S3)

**Deskripsi Pekerjaan**
#### Laporan Fix: Perbaikan Download File Eksternal (URL) pada Background Job KKPRL

**Tanggal:** 08 September 2026

##### Deskripsi Singkat
Laporan ini merangkum perbaikan pada fungsionalitas pengunduhan file pengawasan (dokumen KKPRL), di mana dokumen yang disimpan dengan _path_ URL absolut (seperti S3 Object URL) sebelumnya gagal disalin dan dikirim via email.

##### Detail Perubahan (Changelog)

###### 1. Perbaikan Proses Copy dan Zip File Eksternal
- File yang terdampak: `Modules/PengawasanPerizinanBerusaha/Jobs/SDK/DownloadKkprlFileJob.php`.
- Masalah sebelumnya adalah ketika dokumen memiliki format *path* URL eksternal (misalnya `https://sipservice.kkp.go.id...`), sistem tetap mencoba mengaksesnya menggunakan _local storage disk_ (`Storage::disk('public')->path()`). Hal ini menyebabkan _path_ menjadi *corrupt* (contoh: `/var/www/api-sip-prod/storage/app/public/https://...`) sehingga gagal ditemukan dan dibatalkan (tercatat *Job Gagal Copy* di log).
- **Perbaikan**: Menambahkan deteksi format URL menggunakan `str_starts_with` untuk `http://` dan `https://`. Jika file terdeteksi sebagai URL eksternal, sistem akan langsung mengunduh konten file tersebut menggunakan metode `file_get_contents()` ke dalam proses ZIP atau disalin ke direktori ekspor sementara.

##### Status Pengujian
- **Skenario Unduhan Tunggal (Copy)**: Mengunduh sebuah dokumen berformat PDF (disimpan sebagai remote S3 URL) berhasil.
- **Skenario Unduhan Jamak (ZIP)**: Mengunduh beberapa file campuran (sebagian lokal, sebagian remote URL) berhasil tergabung ke dalam ZIP tanpa terpotong.
- File GeoJSON lokal yang memang tidak ditemukan (*missing*) akan memberikan log peringatan namun tidak memengaruhi proses unduh PDF (*remote file*).

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/135

---

### 1.18 Menyatukan API Manajemen Dokumen Penjadwalan & Integrasi Pembaca Dokumen (OCR)

**Deskripsi Pekerjaan**
#### Laporan Fitur: Penyatuan API Manajemen Dokumen Penjadwalan & Ekstraksi Python

**Tanggal:** 10 September 2026

##### Deskripsi Singkat
Melakukan *refactoring* besar-besaran untuk proses manajemen dokumen pelengkap penjadwalan inspeksi lapangan (STKL, Surat Tugas, Notula, Surat Pemberitahuan) dari yang sebelumnya menggunakan pendekatan rute/upload terpisah per-dokumen menjadi satu rute universal yang dinamis (`/ppbbr/penjadwalan/dokumen/*`).
Fitur ini juga mengintegrasikan sistem OCR dan regex melalui wrapper script Python untuk membaca *metadata* (nomor surat, tanggal) di dalam dokumen PDF yang diunggah, serta menyamakan standar *response* ID terenkripsi pada seluruh payload dan respons Scramble API Docs.

##### Detail Perubahan (Changelog)

###### 1. Unified API Endpoints (Pencarian & Penyimpanan)
- **`/ppbbr/penjadwalan/dokumen/pencarian`**: Dibuat API tunggal untuk mencari dokumen. API ini memiliki *fallback* otomatis: mencari dokumen di database internal (Portal) terlebih dahulu, dan jika tidak ditemukan, akan meneruskan pencarian ke layanan *Gateway Korespondensi (CSRS)*.
- **`/ppbbr/penjadwalan/dokumen/simpan`**: API universal untuk menyimpan segala jenis dokumen penjadwalan. API ini menggantikan fungsi lama seperti `upload-stkl`, `upload-st`, dll. Mendukung *bulk insert* (melalui array `objek_pengawasan_ids`) untuk Objek Pengawasan majemuk yang tergabung dalam 1 surat. Mekanisme penyesuaian (Dual-Write) juga disertakan agar status *upload* di database *legacy* tetap tersinkronisasi.
- **`/ppbbr/penjadwalan/dokumen/{id}`**: API untuk melihat data dokumen existing atau dokumen awal (bawaan) yang mengikat pada suatu objek pengawasan.

###### 2. Integrasi Python Wrapper untuk Ekstraksi Dokumen
- **`/ppbbr/penjadwalan/dokumen/extract`**: Dibuat endpoint baru yang berfungsi membaca file PDF dan mengekstrak nomor dokumen/NKU.
- Proses ekstraksi memanfaatkan skrip `scripts/PPBBR/extract_dokumen.py` yang menggunakan dua layer pemrosesan:
  - *Native Text extraction* (menggunakan `PyMuPDF`/`fitz`) untuk PDF berbasis teks digital.
  - *OCR extraction* (menggunakan `pdf2image` dan `pytesseract`) sebagai *fallback* apabila dokumen merupakan hasil *scan* fisik (PDF gambar).
- Menggunakan pustaka standar PHP `Symfony\Component\Process\Process` untuk eksekusi Python yang aman dan dapat dipantau dari dalam Laravel Controller.

###### 3. Standarisasi Keamanan ID (Enkripsi/Dekripsi)
- Seluruh endpoint terbaru telah diimplementasikan dengan `EnkripsiHelper` milik SIP PSDKP.
- Endpoint menerima request berupa *encrypted string* (seperti `portal_dokumen_id` dan elemen `objek_pengawasan_ids`), lalu melakukan *dekripsi* di dalam Form Request dan Service sebelum menyentuh database.
- *Response JSON* secara otomatis melakukan enkripsi ulang pada atribut `id` objek agar *Frontend* tidak mengetahui ID aslinya.

###### 4. Implementasi Scramble API Docs & Response Stubs
- Dibuat *Stub Classes* (`PencarianDokumenResponseStub`, `EkstrakDokumenResponseStub`, `SimpanDokumenResponseStub`, dan `DaftarPenjadwalanResponseStub`) untuk menstandarisasi bentuk *Response Schema*.
- Melakukan pembersihan *Form Request* yang usang.
- Mengimplementasikan `api-docs` skill dengan melengkapi setiap *DocBlock* pada `PenjadwalanController.php` (berbahasa Indonesia dengan *summary* yang deskriptif) agar ter-render rapi pada layar antarmuka *Scalar UI* (Scramble).

##### Status Pengujian
- **Upload Single Dokumen**: Berhasil disimpan ke *table* `dokumen_metadata` dan disinkronkan ke kolom lama `objek_pengawasan` (Dual-Write berhasil).
- **Upload Bulk Dokumen**: ID majemuk pada `objek_pengawasan_ids` berhasil terurai dari array dan di-dekripsi, lalu dikaitkan pada ID dokumen tunggal.
- **Ekstraksi PDF berbasis Text & OCR**: Berhasil diproses, nomor/tanggal terekstrak di *response* `extractDokumen`.
- **Integrasi Frontend:** *Schema* API siap untuk dikonsumsi Frontend melalui spesifikasi OpenAPI (Scramble).
- Perubahan berhasil.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/149

---

### 1.19 Memperbaiki format respons daftar penjadwalan pada Scramble API

**Deskripsi Pekerjaan**
… parser

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/150

---

### 1.20 Membersihkan data null dari stub penjadwalan API

**Deskripsi Pekerjaan**
…e inference failure

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/151

---

### 1.21 Mengatur ekstraksi item array untuk kelancaran dokumentasi (AST)

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/152

---

### 1.22 Membangun alur unggah, ekstraksi, dan simpan untuk Laporan Inspeksi

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/153

---

### 1.23 Mengembangkan fitur melewati pertanyaan (skip logic) Kepatuhan Teknis

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/154

---

### 1.24 Melengkapi penerapan dua angka desimal di format inspeksi

**Deskripsi Pekerjaan**
Menutup Issue #127. Memastikan seluruh skor kepatuhan teknis dirender dengan format 2 desimal di backend API dan generate PDF.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/155

---

### 1.25 Memperbaiki pembacaan baris narasi Kepatuhan Teknis ber-skor Nol

**Deskripsi Pekerjaan**
…adi string

Skor pada struktur PDF kini berupa string hasil truncateDecimal (mis. '0.00'), sehingga pengecekan ! \->skor tidak lagi mendeteksi skor nol. Diubah ke pengecekan numerik (float) \->skor == 0 agar baris auto-jawab ber-skor nol tetap tampil sebagai baris keterangan (tanpa centang dan tanpa nilai).

Sekaligus mengembalikan perubahan spasi concatenation/closure yang tidak lolos Pint, dan memperbarui dokumen review.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/156

---

### 1.26 Menetapkan batasan ukuran unggahan file spesifik di server

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/161

---

### 1.27 Menyempurnakan hasil analisis dari pertanyaan yang terlewat

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/162

---

### 1.28 Mengembangkan fitur "Sleep Drip" anti-blokir untuk notifikasi WA

**Deskripsi Pekerjaan**
#### Laporan Feat: Implementasi "Sleep Drip" pada Notifikasi WA Objek Pengawasan

**Tanggal:** 12 September 2026

##### Deskripsi Singkat
Melakukan penyesuaian logika pengiriman notifikasi WhatsApp pada fitur "Kirim Objek Pengawasan" untuk menghindari deteksi *spam* oleh *provider* API pihak ketiga. Sebelumnya, notifikasi massal ke operator dan pengawas UPT dikirim dengan parameter jeda yang sama untuk satu *request* (menggunakan nilai dari `config`), yang rentan bermasalah jika dikonfigurasi terlalu lama atau gagal didistribusikan. Perbaikan dilakukan dengan menerapkan metode *Sleep Drip*, di mana setiap nomor penerima diproses satu per satu dalam *loop* dan diberikan durasi *delay* secara acak antara 2 hingga 240 detik, agar pengiriman tampak lebih natural.

##### Detail Perubahan (Changelog)

###### 1. Refactor `WhatsappService.php`
- Menambahkan metode `sendSleepDrip(array $numbers, $message, $notifiable = null, $maxDelay = 240)` untuk menangani perulangan nomor dan pembuatan *random delay* secara terpisah, sehingga tidak mengganggu *flow* notifikasi instan (misal OTP).
- Menyematkan `User-Agent: API-SIP-PSDKP/1.0` ke dalam *request* HTTP Guzzle untuk menghindari pemblokiran oleh Web Application Firewall (WAF) penyedia API.

###### 2. Modifikasi `WaNotifications.php`
- Memperbarui `kirimObjekPengawasanOperatorUPTWaNotification()` dan `kirimObjekPengawasanPengawasPerikananWaNotification()` agar tidak lagi menggabungkan nomor menggunakan `implode`.
- Mengganti penggunaan `WhatsappService::send` dengan `WhatsappService::sendSleepDrip(...)` secara *hardcoded* dengan toleransi jeda 240 detik, mengabaikan parameter *environment* lawas `PPBBR_WA_DELAY_OBJEK_PENGAWASAN` yang nilainya berpotensi terlampau besar.

###### 3. Penambahan Unit Test di `DispatchAfterCommitTest.php`
- Ditambahkan *unit test* `kirim_objek_db_tersimpan_dan_job_di_dispatch` untuk memvalidasi pembaruan *database* status objek dan pelemparan (*dispatching*) Job WA dan Email.
- Ditambahkan *unit test* `kirim_objek_db_aman_walau_queue_throw_exception` untuk memvalidasi mekanisme *failsafe* di mana perubah status DB akan tetap disimpan sekalipun pengiriman Job ke Queue (*Redis*) mengalami gangguan.

##### Status Pengujian
- **Test User-Agent Header**: Sukses tervalidasi pada parameter HTTP Guzzle.
- **Test Kirim Objek Pengawasan Unit Test**: Sukses (*PASS*), *database* terbarui dan *Queue* di-*dispatch* di luar *transaction* DB secara asinkron.
- Mekanisme *Sleep Drip* berhasil dijalankan tanpa menghambat atau menyebabkan lambatnya antarmuka aplikasi.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/163

---

### 1.29 Menggabungkan kode cadangan pembaruan inspeksi (master_backup)

**Deskripsi Pekerjaan**
##### Ringkasan

Merge `master_backup` ke `master` untuk menyatukan pekerjaan yang ada di `master_backup` namun belum masuk `master`.

`master` dan `master_backup` **diverged** (common ancestor: `995786dc9` / PR #135):
- `master` : 49 commit lebih maju (PR #110–#135, #149–#153)
- `master_backup` : 19 commit lebih maju (PR #154–#162)

##### Yang Masuk dari master_backup
- Kepatuhan Teknis: skip logic, akumulasi score & auto-yes, perbaikan skor/analisis.
- Perbaikan rendering desimal PDF (2 angka di belakang koma).
- Pemisahan grup Scramble **PPBBR-SDK** & kelengkapan dokumentasi inspeksi.
- Skill `kepatuhan_teknis_standards`, test, seeder, dan report pendukung.

##### Konflik yang Diselesaikan
- `app/Docs/ApiTagGroups.php` — memakai struktur dari `master_backup`:
  - Grup **PPBBR-SDK** dipisah menjadi modul tersendiri.
  - Penambahan tag `LaporanHasilInspeksi`.
  - Tag `HasilPengawasan`, `HasilSupervisi`, `IndikasiPelanggaran`, `Inspeksi`, `Pemantauan`, `RencanaZonasi`, `Supervisi` dipindah ke grup PPBBR-SDK (penamaan `PpbbrSdk*`).

##### Verifikasi
- `git merge-tree` menunjukkan hanya 1 konflik, sudah diselesaikan.
- `php -l app/Docs/ApiTagGroups.php` → tidak ada syntax error.
- Tidak menghapus perubahan `master` (merge biasa, bukan force).

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/164

---

### 1.30 Merilis Fitur Modul Penjadwalan Laporan Pengawasan Terintegrasi OCR

**Deskripsi Pekerjaan**
##### Ringkasan

PR untuk menggabungkan `fitur/laporan-hasil-pengawasan` ke `master`.

> ⚠️ **Urutan merge:** harap merge PR `master_backup → master` (#164) **lebih dulu**. Setelah #164 masuk, branch ini kemungkinan perlu di-*sync* ulang (lihat bagian Catatan).

##### Fitur Utama

###### 1. Modul Penjadwalan Pengawasan — Kelengkapan Dokumen (5 Jenis)
- Endpoint universal: `unggah` (multipart), `extract` (Regex NKU), `simpan` (mendukung Bulk Save), `pencarian` (Pilih/Cari CSRS).
- Urutan upload perdana: **Notula → SP (OSS/UPT) → STKL → Surat Tugas** (validasi di backend).
- Notula, SP OSS, STKL: unggah manual saja. SP UPT & ST: Pilih → Cari → Unggah.
- Rate limiter: Cari 2x/120s, Unggah 5x/120s → mengembalikan `sisa_kesempatan` & `cooldown_until` (tanpa HTTP 429).
- Validasi anti-waste 5 tahap pada keyword, validasi anti-spoofing (IDOR).
- Ekstraksi NKU via Python (`scripts/PPBBR/extract_dokumen.py`), simpan ke `ppbbr_dokumen_metadata`.

###### 2. Status & Penjadwalan (Hari H)
- Status baru: `Lengkapi Dokumen`, `Menunggu Inspeksi`.
- `evaluasiStatusPenjadwalan()` saat simpan + notifikasi WA/Email saat lengkap.
- Cron Hari H (bulk update): `Menunggu Inspeksi → Inspeksi Lapangan`, `Lengkapi Dokumen → Penjadwalan Terlewat` (file tidak dihapus).

###### 3. Migrasi Legacy & Dual-Write
- Tabel sentral `ppbbr_dokumen_penjadwalan` + audit ketergantungan kolom legacy (`surat_tugas`, `surat_pemberitahuan`, `stkl`).
- Artisan `ppbbr:migrate-legacy-penjadwalan`.

###### 4. Korespondensi CSRS
- Pencarian dokumen universal (`/master/korespondensi/dokumen/pencarian`).
- Sinkronisasi Satker (`portal_satkers`, command `portal:sinkron-satker`), filter KM, auto-tag **STWAP**.

###### 5. Dashboard
- Status baru dimasukkan ke kategori dashboard (`pie` & `card` Penjadwalan Inspeksi).

###### 6. Tools UAT
- Generator PDF dummy: Notula, ST, SP UPT (memuat NKU objek + NKU acak via `--nku-extra`).
- Endpoint reset objek pengawasan (`/fe-test/ppbbr/reset-objek-pengawasan/{id}`).

###### 7. Testing & Standards
- `phpunit.xml` + `.env.testing.example` (standar testing DB).
- Test: `UnggahDokumenRateLimitTest`.
- Skill: `database_testing_standards`, `git_commit_push_standards`, `github_app_psdkplabs`, `github_issue_standards`, `fqcn_import_standards`, `upload_penjadwalan_lhp_standards`.

###### 8. Dokumentasi
- PRD & Implementation Plan Penjadwalan Pengawasan.
- Dokumentasi integrasi FE di GitHub Issue #140 (induk) & #141–#145 (per dokumen).
- Berbagai response stub Scramble.

##### Konflik yang Diselesaikan
- `app/Http/Library/StringHelper.php` — memakai versi `master`:
  `truncateDecimal($value, int $decimals = 2): ?string`. Fitur memiliki duplikat method dari lineage berbeda, dihapus agar tidak dobel.

##### Catatan
- Setelah PR #164 (`master_backup → master`) di-merge, `master` berubah pada `app/Docs/ApiTagGroups.php` (pemisahan grup PPBBR-SDK). Branch ini mengubah 1 baris pada file yang sama (`DokumenPutusanKewenangan` pindah grup) → **kemungkinan perlu re-sync**.
- Stats: 69 file, +3497 / −670.

##### Verifikasi
- `git merge-tree origin/master HEAD` → **tanpa konflik** (setelah resolusi).
- `php -l` pada file terkait konflik → OK.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/165

---

### 1.31 Memperbaiki letak penyimpanan berkas PDF Notula uji coba (UAT)

**Deskripsi Pekerjaan**
Perbaikan pada path penyimpanan PDF saat generate notula dummy agar bisa diakses frontend (via \public/uat\).

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/166

---

### 1.32 Memaksa sistem untuk menulis berkas PDF ke disk lokal sistem

**Deskripsi Pekerjaan**
… UAT

- Memastikan storage PDF masuk ke direktori storage/app/public/uat/ dan bukan storage/app/public/public/uat/ yang terjadi bila default disk adalah public.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/167

---

### 1.33 Melanjutkan implementasi formulir Laporan Hasil Pengawasan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/168

---

### 1.34 Menyembunyikan rekam data ekstraksi untuk dokumen yang batal dipilih

**Deskripsi Pekerjaan**
…centang (unchecked)

- PenjadwalanService: memfilter (skip/continue) daftar metadata yang di-return pada endpoint `dokumenExisting` apabila item tersebut belum/tidak diceklis (`is_checked = false`), termasuk untuk data objek yang tidak valid.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/169

---

### 1.35 Merapikan format tampilan perintah surat uji coba ke tipe array JSON

**Deskripsi Pekerjaan**
- TestController: Mengubah balasan JSON untuk properti `output` dari raw string menjadi array string (`explode(\n, trim($output))`) agar tampilannya lebih rapi dan mudah di-render oleh frontend tanpa isu spasi/newline.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/170

---

### 1.36 Menyelaraskan izin penggunaan fitur Penjadwalan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/171

---

### 1.37 Memberikan hak akses membaca dan mengekstrak dokumen ke Operator

**Deskripsi Pekerjaan**
…r wasrisk

- AkunPenjadwalanLhpSeeder: Menambahkan permission `ppbbr.penjadwalan.dokumen.existing.show`, `ppbbr.penjadwalan.dokumen.extract.store`, dan `ppbbr.hasil-inspeksi.dokumen.extract.store` ke dalam array WRITE_PERMISSIONS.
- Hal ini diperlukan agar Role Operator Pusat dan UPT WasRisk memiliki akses penuh ke fitur Lengkapi Dokumen Penjadwalan maupun LHP (termasuk memuat data existing dan melakukan ekstraksi teks/OCR).

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/172

---

### 1.38 Mengubah urutan proses pengunggahan berkas jadwal pengawasan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/173

---

### 1.39 Mendaftarkan opsi pengembalian (reset) ke status "Sedang Inspeksi"

**Deskripsi Pekerjaan**
- Menambahkan 'sedang_inspeksi_lapangan' ke dalam $daftarTarget di TestController@resetObjekPengawasan agar sesuai dengan nama target yang dikirimkan.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/174

---

### 1.40 Memperbaiki fungsi pencarian ejaan Surat Tugas agar mentolerir format khusus

**Deskripsi Pekerjaan**
- Mengubah logika `where` menjadi `like '%...%'` pada pencarian `no_kode_proyek` dan `nomor_st`.
- Hal ini diperlukan karena kolom `no_kode_proyek` dapat menyimpan data dalam format array JSON atau dipisahkan koma, sehingga pencocokan exact match (=) berpotensi gagal.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/175

---

### 1.41 Mengatur otomatis jadwal menjadi lusa saat dokumen dikembalikan ke proses OSS

**Deskripsi Pekerjaan**
- TestController: ubah resetObjekPengawasan untuk target disetujui_oss dan bersih_total agar turut mengatur jadwal menjadi Carbon::now()->addDay().

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/176

---

### 1.42 Mempertahankan penugasan nama pengawas tatkala status dikembalikan (reset)

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/177

---

### 1.43 Merekam catatan spesifikasi produk (PRD) pasca penggabungan kerja (merge)

**Deskripsi Pekerjaan**
… test

- PR #173 (urutan Notula -> STKL -> SP -> ST): update PRD Penjadwalan (§1, §3), skill upload_penjadwalan_lhp_standards, dan test urutan upload.
- PR #175 (LIKE parsial NKU/Nomor ST): catat di PRD Penjadwalan §6 & PRD LHP extract; tambah test pencocokan parsial.
- PR #169 (sembunyikan details tak tercentang/invalid): catat di PRD §2.
- PR #171/#172 (MODUL_NAME + permission read/extract): update skill authorize_guard_standards + plan Fase 7.
- PR #174/#176/#177 (reset: target sedang_inspeksi_lapangan, jadwal H+1, pengawas dipertahankan): update PRD §10.5 + LHP §12.3.
- Tests: PenjadwalanUrutanUploadTest 15 + FlowTest 20 + Ekstrak 7 + Seeder 3 PASS mengikuti perilaku merged.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/178

---

### 1.44 Mengamankan kelanjutan data saat Scheduler harian (Cron Job) terhenti

**Deskripsi Pekerjaan**
…pired gagal

- InspeksiLapanganService: tambahkan objek dengan status Menunggu Inspeksi yang jadwalnya sudah hari-H atau terlewat ke dalam daftar Inspeksi Lapangan.
- ObjekPengawasan: tambahkan izin canInspeksiLapangan() untuk objek Menunggu Inspeksi pada hari-H atau terlewat.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/179

---

### 1.45 Meningkatkan kapasitas simulasi terlewat pada perkakas uji ke bentuk massal

**Deskripsi Pekerjaan**
- TestController: perbarui ubahKeInspeksiLapangan agar mengupdate seluruh objek berstatus Menunggu Inspeksi yang jadwalnya masuk hari H atau lewat, meniru perilaku cron job CekJadwalPengawasanTerlewat.
- web.php: hapus parameter {id} pada route ubah-ke-inspeksi-lapangan.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/180

---

### 1.46 Memperkaya tampilan dokumen pada arsip akhir Inspeksi

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/181

---

### 1.47 Melanjutkan standarisasi implementasi Laporan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/182

---

### 1.48 Mengelevasi kapabilitas Penjadwalan bersama Laporan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/183

---

### 1.49 Menyematkan metode simulasi dokumen tertinggal secara massal di alat simulasi

**Deskripsi Pekerjaan**
- TestController::resetObjekPengawasan target terlewat: pertahankan dokumen (+legacy), status PenjadwalanTerlewat + jadwal kemarin (simulasi overdue, mis. Disetujui OSS yg tanggalnya lewat karena scheduler mati).
- TestController::resetMassalPenjadwalan + route: reset massal berbasis status (default Terlewat, filter unit opsional) tanpa input ID.
- Tests: ResetObjekPengawasanTest + ResetMassalPenjadwalanTest.
- Docs: PRD §10.5.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/184

---

### 1.50 Mengoreksi nilai Sisa Hari penunjuk jadwal pengawasan di masa depan

**Deskripsi Pekerjaan**
- Carbon 3 diffInDays default signed sehingga jadwal besok tampil -1; tukar operan + cast int. Jadwal lewat tetap null.
- Tests: PenjadwalanSisaHariTest (mendatang +1, lewat null).

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/185

---

### 1.51 Memperketat persyaratan kecocokan dokumen (NKU / Surat) di tahap berjalan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/186

---

### 1.52 Melanjutkan integrasi stabilitas fitur Laporan Pengawasan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/187

---

### 1.53 Menyepadankan penamaan folder surat uji coba (UAT) ke format numerik ID

**Deskripsi Pekerjaan**
- UatGenerateLaporanCommand, UatGenerateSpUptCommand, UatGenerateStCommand: ubah nama folder tempat penyimpanan file UAT agar menggunakan $dokumenId (numeric) alih-alih $encryptedId.
- Ini memastikan file terbaca dengan benar oleh KorespondensiController yang sudah mengimplementasikan bypass dekripsi untuk ID numeric.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/188

---

### 1.54 Memberikan izin lintas platform pembaca dokumen nyata dengan ID numerik (Gateway)

**Deskripsi Pekerjaan**
- Pada KorespondensiService::lihatDokumenSurat, berikan fallback is_numeric agar ID yang belum dienkripsi tidak rusak saat dipanggil dekrip().
- Ini menyelesaikan masalah Timeout/500 saat hit endpoint file dengan ID numeric (non-enkripsi) untuk data riil dari Gateway.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/189

---

### 1.55 Mempermulus tahap pengisian formulir Laporan (Tahap 1)

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/190

---

### 1.56 Mempermulus tahap pengisian formulir Laporan (Tahap 2)

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/191

---

### 1.57 Mempermulus tahap pengisian formulir Laporan (Tahap Akhir)

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/192

---

### 1.58 Memperbaiki celah unggahan penerbitan Surat Tugas Kunjungan (STKL)

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/193

---

### 1.59 Membebaskan pewajiban STKL dan Surat Pemberitahuan pada kondisi legal

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/194

---

### 1.60 Menyapu residu rekaman usang saat objek dihapus

**Deskripsi Pekerjaan**
Tanpa ini evaluasiStatus tetap anggap lengkap via kolom stkl/surat_pemberitahuan lama. Status objek terlanjur ikut diturunkan + save.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/195

---

### 1.61 Memantapkan kontrak data API Laporan untuk antarmuka pengguna (Frontend)

**Deskripsi Pekerjaan**
- status_tombol.penjadwalan di resource LHP (catatan commit sip 5570d30)
- simpanLaporan terima link_dokumen_pendukung format FE {url,label}
- daftar_dokumen_csrs selalu array (sblmnya object saat keyword)
- extract tambah is_empty + pesan khusus saat hasil kosong
- stub docs + test menyesuaikan

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/196

---

### 1.62 Memberikan fleksibilitas pada folder uji coba pembaca dokumen

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/197

---

### 1.63 Mengedepankan hierarki pencarian dokumen server berstandar numerik

**Deskripsi Pekerjaan**
- KorespondensiController: ubah prioritas pencarian folder agar selalu mengecek folder ID numeric (decryptedId) terlebih dahulu.
- Jika URL menggunakan ID terenkripsi, fallback mencari folder dengan ID terenkripsi (UAT lama).
- Ini memperbaiki issue di mana URL terenkripsi gagal mendownload dokumen karena foldernya sudah menggunakan standar penamaan numeric yang baru.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/198

---

### 1.64 Mengikutsertakan nomenklatur kode (KM) pada arsip Surat Tugas lama

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/199

---

### 1.65 Mengatur kembali masa jeda pada batas kuota pengunggahan aplikasi

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/200

---

### 1.66 Menyelesaikan koreksi manual baca dokumen dan mendokumentasikan pembaruannya

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/201

---

### 1.67 Membuang rintangan perihal informasi tak terbaca pada halaman dokumen detail

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/211

---

### 1.68 Menyisipkan referensi penomoran hukum (KM) ke badan Laporan akhir

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/213

---

### 1.69 Membebaskan pengawas dari mesin pemindai ulang bila data sah terdeteksi

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/215

---

### 1.70 Menciptakan fungsionalitas pencarian acak dokumen penguji (UAT)

**Deskripsi Pekerjaan**
- --mode=acak|spdrut|cari (default acak, validasi di awal)
- ?mode= di endpoint TestController generate-st/sp-upt/laporan
- cari = tanpa prefix (untuk uji Cari), spdrut = untuk uji Pilih

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/217

---

### 1.71 Mempercepat antarmuka tahapan Pengisian Dokumen (Improvement)

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/218

---

### 1.72 Mencantumkan tautan file Berita Acara langsung di halaman Daftar Inspeksi

**Deskripsi Pekerjaan**
- InspeksiLapanganDenganPenanggungJawabResource: tambah array laporanHasilInspeksi khusus untuk status ObjekPengawasan::Selesai.
- Menyamakan format data laporan agar konsisten dengan endpoint detail hasil inspeksi.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/219

---

### 1.73 Merombak mutlak kepintaran AI pembaca dokumen Izin OSS (PKKPRL & PBUMKU)

**Deskripsi Pekerjaan**
Pipeline OSS (scripts/OSS/extract_file_izin/main.py):
- Tulis ulang. Library diselaraskan dengan pipeline PPBBR: pypdfium2 saja. pdfplumber dan dateparser dibuang (dateparser diganti tabel bulan Indonesia), sehingga satu venv melayani dua pipeline.
- Perbaiki bug laten: guard "PERIZINAN BERUSaha..." membungkus nomor DAN tanggal padahal frasa itu hanya ada di 1/20 dokumen -> nomor terisi 0/20 dan gagalnya DIAM (null, bukan exception).
- Pemetaan pola per jenis dokumen (analog KM_PER_JENIS): PKKPRL pakai "NOMOR :", PBBR pakai "IZIN :", PB-UMKU pakai "PB UMKU:".
- Deteksi jenis dari judul yang di-anchor ke awal baris, bukan substring (badan PKKPRL memuat frasa "Perizinan Berusaha Berbasis Risiko" di butir ketentuan). Tahan judul yang terpotong dua baris (kasus nyata PB-UMKU).
- Tanggal wajib satu baris dengan labelnya ([ \t]*, bukan \s*) + tolak string yang memuat nama jabatan -> hilangkan noise "a.n. Menteri Kelautan...".
- requirements.txt baru (sebelumnya tidak ada sama sekali).

Sisi PHP (Modules/Gateway/Jobs/OSS/SinkronFileIzinOssJob.php):
- decodeJsonPayload() 3 tingkat, selaras EkstrakDokumenService. Sebelumnya hanya strpos($joined,'{') satu tingkat: baris STATS {...} juga memuat '{', sehingga payload yang terbaca adalah objek statistik -> number/date null tanpa error apa pun.
- Path script jadi konfigurasi (services.python.oss_extract_script).

Hasil verifikasi (20 izin OSS nyata, public/bucket/s3_default/file/oss/):
- nomor 0/20 -> 20/20, tanggal 19/20 tanpa noise, jenis terdeteksi 20/20
- verifikasi silang independen: nomor 20/20 cocok, tanggal 17/17 cocok
- rata-rata 0,55 s/dokumen; uji_regex_nku.py PPBBR tetap semua lulus

Rapikan korpus & dokumentasi:
- dummySurat distandarkan ke lowercase-kebab-case satu tingkat (korpus/, data/, 03-hasil/, 04-arsip-uji-lama/), korpus dipisah per jenis.
- Tiga skrip uji lama yang terpecah digabung jadi uji_ekstraksi.py.
- Pindahkan path di SyncDummyWasriskCommand dan SyncSingleWasriskJob.

Catatan: SinkronFileIzinOssJob belum diuji di lingkungan ber-PHP (PHP tidak tersedia lokal) - perlu php -l dan uji job di staging.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/220

---

### 1.74 Melengkapi tata kelola antarmuka Pelaporan Pengawasan tahap berkelanjutan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/221

---

### 1.75 Menutup eksploitasi otorisasi data (IDOR) pada fasilitas Pemindaian Dokumen Cadangan

**Deskripsi Pekerjaan**
##### Ringkasan

Menutup **dua celah** pada pencocokan hasil ekstraksi NKU/Nomor ST ke
`ObjekPengawasan`, lalu **menyatukan** penyaringan peran yang tadinya tersalin
di tiga tempat.

##### 1. Penyaringan peran bisa dilewati dengan `queryBase = null`

Parameter kedua `EkstrakDokumenService::cocokkanKeObjek()` adalah `queryBase`.
Bila `null`, service jatuh ke `ObjekPengawasan::query()` — **seluruh tabel objek**,
tanpa pembatasan unit kerja.

Dua resource mengirim `null`:

- `HasilInspeksiLapanganResource:193`
- `InspeksiLapanganDenganPenanggungJawabResource:234`

Akibatnya pencocokan cadangan (objek lain) bisa menyentuh objek di luar
kewenangan user — mis. Operator UPT melihat objek unit lain.

**Perbaikan:** logika otorisasi dipindah dari method privat `PenjadwalanService`
ke scope `ObjekPengawasan::dalamKewenangan()` sebagai **sumber kebenaran
tunggal**, lalu dipakai oleh ketiga pemanggil. Tanpa login scope ini
**fail-closed** (`where('unit_kerja', null)` → `is null`).

##### 2. `$jenisDokumen` tidak dipakai di `queryBaseUntukEkstrak()`

Parameter diterima tapi tidak pernah dipakai — jadi filter per jenis dokumen
belum ada sama sekali. Parameter yang tidak berguna **dihapus**, dan jenis
dokumen kini diteruskan sebagai argumen ke-4 `cocokkanKeObjek()` untuk
mempersempit **hanya pencocokan cadangan** (objek lain):

| jenis dokumen | status yang dicari |
|---|---|
| `notula`, `surat_pemberitahuan_upt`, `surat_tugas`, `stkl` | `praInspeksi()` |
| `laporan` | `selesai()` |
| `null` (pemanggil lama) | tanpa filter — perilaku lama dipertahankan |

**Objek yang sedang dibuka (`currentObjekId`) sengaja TIDAK disaring status**,
supaya melengkapi ulang dokumen pada objek yang sudah `Selesai` tetap bisa.

Tanpa penyaringan ini, `->first()` pada pencocokan cadangan bisa menangkap objek
lama yang sudah `Selesai`, karena satu NKU dipakai banyak objek — **460 dari 1515
baris objek di `sip_dev` (30,4%)** berbagi NKU dengan objek lain; satu NKU bahkan
dipakai 30 objek.

##### 3. Penyaringan peran disatukan

Dua salinan `applyRoleAuthorization()` yang tersisa
(`HasilInspeksiLapanganService`, `InspeksiLapanganService`) logikanya identik
dengan scope baru — hanya beda null-safety (`$user->pegawaiInternal` vs
`$user?->pegawaiInternal`, hasilnya sama karena `??` sudah menutup rantai).
Keduanya kini mendelegasikan ke scope, sehingga definisinya hanya **satu**.

Ini penting karena scope yang sama dipakai resource hasil inspeksi lapangan:
kalau salinannya menyimpang, daftar dan detail bisa memberi hasil berbeda untuk
user yang sama.

Efek samping: trait `AuthHelpers` tidak lagi terpakai di kedua kelas
(satu-satunya pemakaian adalah `findRoleName()`/`jenisUnit()` di dalam method yang
dihapus; `checkAccount()` hanya dipanggil dari `AuthService` dan `AuthLkuService`).
Trait + import-nya dihapus. **76 baris duplikat hilang.**

##### Koreksi atas temuan sebelumnya

Sempat disimpulkan bahwa Nomor ST dari laporan tak akan pernah cocok karena
berprefix `PW`. **Itu keliru.** Bukti langsung dari `sip_dev`:

| objek | `ppbbr_dokumen_metadata.nilai` | `portal_dokumen.ref_number` |
|---|---|---|
| 18413 | `B.18413/PSDKPLan.3/KP.440/IX/2026` | `B.18413/PSDKPLan.3/PW.110/IX/2026` |

`nilai` untuk `laporan` berisi **Nomor ST** (`KP.440`), byte-identik dengan
`surat_tugas.manual_nomor_surat` objek yang sama. Nomor laporan sendiri
(`PW.110`) hanya ada di `ref_number`. Jadi cabang `nomor_st` yang mencari
`surat_tugas` **sudah benar untuk laporan** — tidak ada perubahan pencocokan
khusus laporan di PR ini.

##### Test

Test regresi ditambahkan:

- `EkstrakDokumenServiceTest` — 7 test baru: penyaringan status pra-inspeksi,
  penyaringan `Selesai` untuk laporan, pengecualian objek saat ini dari filter
  status, seluruh himpunan status pra-inspeksi, penolakan status di luar
  jendela, dan kompatibilitas pemanggil lama (`$jenisDokumen = null`).
- `ObjekPengawasanKewenanganScopeTest` (baru) — 5 test: Operator Pusat &
  Superuser bebas, Operator UPT per unit kerja, Pengawas per NIP, Operator UPT
  yang merangkap Pengawas tidak disaring NIP, dan fail-closed tanpa login.

```
php artisan test --filter=EkstrakDokumen
php artisan test --filter=ObjekPengawasanKewenanganScope
```

> Catatan: test **belum dijalankan** — mesin pengembang ini tidak punya binary
> PHP dan Docker daemon mati. Validasi yang dilakukan hanya pemeriksaan statis
> (keseimbangan delimiter + telaah diff). Mohon jalankan test di atas sebelum
> merge.

##### Catatan untuk reviewer

- `Lengkapi Dokumen` **sengaja ikut** di `STATUS_PRA_INSPEKSI` karena artinya
  "sebagian dokumen sudah diunggah" — membuangnya memutus alur Notula setelah
  STKL. Status ini **0 baris di `sip_dev`**, jadi cabang kode ini tidak bisa
  diuji lokal; perlu diuji di prod/stage.
- Status di `sip_dev`: Selesai 1395 · Disetujui (OSS) 53 · Belum Dijadwalkan 51 ·
  Objek Pengawasan Baru 16 · Menunggu Inspeksi 3 · Sudah Dijadwalkan 2 ·
  Inspeksi Lapangan 1 · Ditolak (OSS) 1 · Menunggu Persetujuan (OSS) 1.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/222

---

### 1.76 Menerapkan jaminan kekebalan sistem atas siklus pra-inspeksi dan unggah laporan

**Deskripsi Pekerjaan**
##### Ringkasan

Menambah `StatusPraInspeksiKonsistensiTest` (7 test) untuk **mengunci invarian** antara `ObjekPengawasan::STATUS_PRA_INSPEKSI` dan syarat tombol unggah dokumen.

##### Kenapa perlu

`STATUS_PRA_INSPEKSI` dipakai `EkstrakDokumenService::cocokkanKeObjek()` untuk mempersempit **pencocokan cadangan** (objek lain). Nilainya bukan kebijakan bebas — ia harus sama dengan gabungan syarat tombol unggah:

- `canUploadSuratTugas()` — 4 status
- `canUploadSuratPemberitahuan()` — 4 status
- `canLengkapiDokumen()` — 3 status (tanpa `Belum Upload Surat Tugas`)
- `canUploadSTKL()` — hanya `Disetujui (OSS)`

**Risiko yang dicegah:** kalau kelak bisnis mengizinkan unggah dokumen pada status yang lebih awal (mis. `Sudah Dijadwalkan`) dan hanya tombolnya yang diubah, pencocokan cadangan akan diam-diam mengembalikan `status = 'invalid'` padahal NKU-nya sah. Gejalanya membingungkan karena `kode_proyek` yang tampil identik — pengguna tidak bisa membedakan objek mana yang gagal tercocokkan.

##### Yang dikunci

| Test | Isi |
|---|---|
| `gabungan_syarat_tombol_unggah_sama_persis_dengan_status_pra_inspeksi` | Invarian utama |
| `can_lengkapi_dokumen_aktif_pada_pra_inspeksi_kecuali_belum_upload_st` | `Belum Upload Surat Tugas` dilayani tombol ST tersendiri |
| `can_upload_stkl_hanya_aktif_pada_disetujui_oss` | — |
| `status_di_luar_pra_inspeksi_tidak_bisa_mengunggah_apa_pun` | 12 status di luar jendela |
| `selesai_tidak_boleh_masuk_jendela_pra_inspeksi` | Regresi akar masalah `is_current` |
| `status_pra_inspeksi_saat_ini_tepat_empat_status` | Perubahan kebijakan harus disadari |
| `batas_h1_mematikan_tombol_lengkapi_dokumen` | Jadwal hari ini/kemarin terkunci; besok & tanpa jadwal boleh |

Status diambil via reflection dari konstanta model, jadi **status baru otomatis ikut teruji** tanpa perlu didaftarkan ulang.

##### Catatan cakupan

Tempat ketiga yang juga harus sinkron — `PenjadwalanService::validasiUrutanUpload()` — **tidak** diuji di sini karena method-nya privat dan terikat query `DokumenPenjadwalan`. Saat PR ini dibuat, isinya sudah diverifikasi sama persis (4 status yang sama); hal ini dicatat di docblock test.

##### Status verifikasi

Test PHP **belum dijalankan** (mesin pengembang tanpa binary PHP). Invariannya diverifikasi statis terhadap sumber `ObjekPengawasan.php` dan `PenjadwalanService.php`: ketiga tempat sinkron, dan seluruh assertion test lulus secara statis. Perlu dijalankan di CI:

```
php artisan test --filter=StatusPraInspeksiKonsistensi
```

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/223

---

### 1.77 Memperbaiki kegagalan ekstraksi Nomor Surat Tugas pada laporan berkode KP 440

**Deskripsi Pekerjaan**
…t Nomor ST

Laporan gagal extract ulang karena KM_PER_JENIS['laporan'] hanya mencari kode PW (nomor laporan), padahal logika bisnis laporan = ekstrak NOMOR ST (KP 440), bukan nomor laporan sendiri. Rantai: NKU → objek → Nomor ST → metadata laporan. Jadi saat PDF laporan berisi "Surat Tugas Nomor B.20900/.../KP.440/IX/2026", skrip Python tidak mengenali KP 440 sebagai kode yang sah untuk jenis_dokumen='laporan' → hasil_ekstrak kosong.

Perbaikan: tambah 'KP 440' ke KM_PER_JENIS['laporan'], sejajar dengan 'PW 110/120/130/240'. Sekarang extract laporan menangkap Nomor ST.

Ref: user report "laporan yang sudah selesai tidak bisa di-extract ulang, hasilnya kosong" (objek Selesai, NKU 202411-1115-5347-4088-270).

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/224

---

### 1.78 Menyelaraskan struktur perangkat Uji Coba Pengawasan (UAT)

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/225

---

### 1.79 Mewajibkan kelengkapan 100% Surat Pra-Inspeksi di dalam perangkat simulator (UAT)

**Deskripsi Pekerjaan**
- tolak bila Notula/STKL/SP/ST belum ber-file, dengan daftar yang kurang
- Nota Dinas selalu menarget Nomor ST objek (bukan dummy bebas)

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/227

---

### 1.80 Mengikuti kesepakatan notasi penonaktifan tombol lintas tim antar layanan

**Deskripsi Pekerjaan**
- PenjadwalanResource: negasi canSchedule() dan canLengkapiDokumen() sebelum dikirim ke FE.

- Konvensi FE: true = tombol di-disable; method model tetap bermakna can = boleh.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/228

---

### 1.81 Melindungi sistem dari anomali mogoknya tugas otomatis jadwal pengawasan (Fallback Status)

**Deskripsi Pekerjaan**
- PenjadwalanResource: tambah computedStatus() dengan dua kondisi.

- Kondisi 1 (by status): DB sudah PenjadwalanTerlewat -> ditampilkan langsung.

- Kondisi 2 (fallback by date): jadwal sudah H/lewat tapi status DB masih Disetujui OSS / LengkapiDokumen / MenungguInspeksi -> tampilkan PenjadwalanTerlewat ke FE agar konsisten dengan perilaku prod.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/229

---

### 1.82 Mengkonsentrasikan pencarian lintas siklus fase inspeksi ke pangkalan Model Dasar

**Deskripsi Pekerjaan**
- ObjekPengawasan (Model): tambah scopeFaseInspeksiLapangan dan scopeTanpaMenungguInspeksiTerlewat agar logika status tidak terduplikasi.
- InspeksiLapanganService: refactor method search menggunakan faseInspeksiLapangan().
- PenjadwalanService: refactor method penjadwalanSearch menggunakan tanpaMenungguInspeksiTerlewat().
- ObjekPengawasanResource: tambah fallback penyajian status dan disable/enable tombol bila scheduler tidak jalan tetapi jadwal sudah jatuh tempo.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/230

---

### 1.83 Membatasi izin peluncuran laporan eksklusif 100% mutlak pada saat Hari H kejadian

**Deskripsi Pekerjaan**
- InspeksiLapanganResource: ubah syarat enable tombol dari `>=` (atau lewat batas) menjadi exact `isSameDay()` sehingga di luar hari-H jadwal tombol terkunci mati.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/231

---

### 1.84 Merapikan dukungan kelayakan pada status arsip pelaporan pengawasan telat waktu

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/232

---

### 1.85 Mengedepankan kehadiran notifikasi daftar "Menunggu Inspeksi" sebelum Hari H datang

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/233

---

### 1.86 Memperbolehkan kelengkapan persyaratan unggahan pada tempo hari kejadian inspeksi

**Deskripsi Pekerjaan**
bukti

<img width="900" height="556" alt="image" src="https://github.com/user-attachments/assets/5d75642e-9ac5-4514-b9b5-b0f85aae6380" />

@SayyidMakarim

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/235

---

### 1.87 Memperbaiki wujud visual jadwal dan sisa indikator waktu di ambang tenggat waktu

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/236

---

### 1.88 Merestrukturisasi pilar tabel utama surat pendahuluan pengawasan (STKL dan Pemberitahuan)

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/237

---

### 1.89 Membetulkan interaktivitas dan status tombol penyelesaian Laporan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/238

---

### 1.90 Memigrasikan Sistem Penetesan Jeda Waktu Otomatis (Sleep Drip WA) ke Server Utama

**Deskripsi Pekerjaan**
##### Review & Cherry Pick
Berisi perbaikan logika notifikasi WA menggunakan sistem *Sleep Drip* untuk menghindari pemblokiran Anti-Spam API WA pihak ketiga.
- Melakukan perulangan nomor dan *random delay* secara terpisah (maks 240 detik).
- Menambahkan \User-Agent\ ke dalam payload \WhatsappService\.
- Mengimplementasikan \WhatsappService::sendSleepDrip()\ di \WaNotifications.php\.
- Menambahkan Unit test untuk validasi *failsafe* dispatch Job WA.
- Menghapus file sampah \lsp-*\ di \storage/framework\ dan menambahkan ke \.gitignore\.

Commit dari \eat/sleep-drip-wa-notification\ berhasil di *cherry-pick* dengan mulus (tanpa konflik) ke branch \production\.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/241

---

### 1.91 Mengelevasi tampilan antarmuka fungsi pengiriman fitur Laporan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/242

---

### 1.92 Memaksakan interogasi baca sandi (Extract) secara otoritatif bagi Surat Tugas / Laporan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/250

---

### 1.93 Mencekal serangan ekstraksi manipulatif pada formulir pengawasan kuno

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/251

---

### 1.94 Memberdayakan ulang instrumen penyusunan jadwal yang telah kandas dari admin pusat

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/252

---

### 1.95 Meniadakan jejak simbol perusak rahasia (Carriage Return) pada skrip Seeder Otorisasi

**Deskripsi Pekerjaan**
- AkunPenjadwalanLhpSeeder: hapus karakter \r literal yang tersembunyi di blok pertama array PERMISSIONS (baris 37-59); menyebabkan PHP parse error Unexpected StringLiteral Expected koma.
- Permission dan komentar yang terpotong (export.index, notifikasi-input-pengawas, aksi penjadwalan, dll.) dikembalikan ke posisi semula -- tidak ada perubahan logika.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/253

---

### 1.96 Mempartisi otonomi otorisasi kelompok Penjadwalan berpisah dari Kelola Dokumen

**Deskripsi Pekerjaan**
- Memisahkan permission baca dan aksi ke fitur 'Penjadwalan'
- Menyisakan permission kelola dokumen saja di 'Dokumen Penjadwalan'
- Perpindahan permission akan ditangani otomatis via updateOrCreate di seeder

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/255

---

### 1.97 Merinci tulisan kegagalan waktu eksekusi agar gampang direnungi pengguna akhir

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/258

---

### 1.98 Menyuntikkan label otomatis (HUWAP/NDLWP) kepada dokumen CSRS (Gateway)

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/259

---

### 1.99 Menyeleksi nomenklatur kode persuratan lama TU140

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/261

---

### 1.100 Melarang penyematan identitas dokumen pelengkap selain dalam bungkus Link (URL)

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/262

---

### 1.101 Memperbaiki celah lenyapnya borang kuesioner HACCP imbas putus jaringan OSS (Timeout)

**Deskripsi Pekerjaan**
#### Laporan Perbaikan: Bug Validasi HACCP, Timeout API OSS, dan Error Undefined Variable pada Pengawasan

**Tanggal:** 24 September 2026

##### 1. Perbaikan Bug Validasi, API OSS Timeout, dan Jawaban Kosong pada HACCP

###### Deskripsi Singkat
Melakukan perbaikan komprehensif terhadap insiden *blank* data pada BAP dan PDF HACCP (Objek Pengawasan PBUMKU). Bug ini disebabkan oleh kombinasi beberapa faktor:
1. API OSS yang *timeout* atau mengembalikan response `500` saat validasi `statusEkspor`, menyebabkan *tab* form HACCP di sisi *frontend* tiba-tiba menghilang (berubah status) dan menyebabkan *array jawaban* ikut terhapus.
2. Validasi *Request* Laravel yang salah logika (`required_if` alih-alih `required_unless`), sehingga *payload* ber-*array jawaban* kosong dari *frontend* tetap diloloskan ke sistem.
3. Looping `getAnswerableQuestion` pada generator PDF dan skrip *autofill* yang melewatkan struktur pertanyaan bersarang (*nested*) karena ada aturan cek *flag* `dijawab == true` peninggalan lawas.
4. Penggunaan *loose comparison* `!= null` yang secara tidak sengaja mem-filter nilai `0` (jawaban "Tidak") sehingga dianggap kosong.

###### Detail Perubahan (Changelog)

#### 1.1 Refactor `ObjekPengawasanService.php`
- Menambahkan **Redis Cache** pada *method* `statusEkspor()` untuk men-cache status ekspor (`flag_ekspor`) NIB selama 7 hari (`604800` detik) per NIB.
- Mencegah UI *Tab* HACCP menghilang (*flickering*) dan merusak *state* isian form *frontend* ketika terjadi gangguan jaringan API OSS pihak ketiga.

#### 1.2 Modifikasi `InspeksiLapanganService.php`
- Pada *method* `getAnswerableQuestion()`, aturan `$item->dijawab == true` dihapus, sehingga keseluruhan struktur anak-anak (ranting) pertanyaan dapat dibaca dengan utuh oleh sistem *autofill* maupun saat pembuatan PDF.

#### 1.3 Modifikasi `PertanyaanPbUmkuService.php`, `PertanyaanKepatuhanTeknisService.php`, & `PertanyaanSelfDeclareService.php`
- Menghapus *hardcode* `'dijawab' => true` pada form Kepatuhan Teknis dan Self Declare yang menyebabkan pertanyaan kosong (belum dijawab) selalu dirender dengan *checkbox* "Tidak" tercentang di dokumen PDF (karena evaluasi `!null == true`).
- Mengganti logika *loose comparison* dari `$jawabanDb->jawaban != null` menjadi *strict comparison* `$jawabanDb->jawaban !== null` secara menyeluruh pada ketiga *Service* tersebut.
- Hal ini mengatasi bug ganda: pertama, mencegah pilihan "Tidak" (nilai numerik `0`) terabaikan karena dianggap kosong. Kedua, memastikan kotak *checklist* Ya/Tidak di PDF akan benar-benar dibiarkan kosong apabila pengawas memang belum menjawab pertanyaan tersebut.

#### 1.4 Perbaikan Fatal Bug pada `JawabInspeksiLapanganRequest.php`
- Memperbaiki *rule* validasi `jawaban` dalam blok `pbUmku()` dengan mengganti aturan `required_if:kewajiban_haccp,0` menjadi `required_unless:kewajiban_haccp,0`.
- Memastikan sistem *backend* akan **menolak (*Validation Error*)** apabila form disimpan dengan *array* jawaban kosong, kecuali jika entitas tersebut memang memegang status "Negara Tujuan Tidak Mewajibkan".

#### 1.5 Penambahan Artisan Command `RecoverHaccpAnswers.php`
- Ditambahkan *command* `php artisan fix:haccp-answers` untuk memulihkan (*recover*) kasus *existing* di Production di mana jawaban HACCP bernilai **0 baris** di *database* namun file fotonya telanjur terunggah ke *Storage* VPS.
- *Command* ini bekerja dengan merangkum UUID pertanyaan dari penamaan file yang dikirim secara *asynchronous*, menyetel jawaban ke `1` (Ya) untuk ID tersebut, `0` (Tidak) untuk sisanya, dan meng-generate ulang dokumen PDF.

###### Status Pengujian
- **Uji Coba Generate PDF (ID 1002820)**: Berhasil mengembalikan seluruh kelengkapan format *checklist* dengan jawaban "Tidak" / 0 yang tertandai sempurna.
  - *Bukti Fisik File:* `storage/app/public/pengawasan_perizinan_berusaha/inspeksi_lapangan/dokumen/pbumku/20260924180546_a9WzQY5VkvABFsld.pdf`
- **Uji Coba Pemulihan Data (ID 1003899)**: Script memulihkan 367 jawaban (termasuk deteksi 4 jawaban "Ya" dari nama file), memperbarui total nilai di *database*, dan *re-generate* PDF tanpa masalah.
  - *Bukti Fisik File:* `storage/app/public/pengawasan_perizinan_berusaha/inspeksi_lapangan/dokumen/pbumku/20260924181902_JMei7V61dQr7Q6JG.pdf`

---

##### 2. Perbaikan Undefined Variable `$nomor`, `$urutan`, dan `$iterasi` pada Modul Pengawasan

Laporan ini mendokumentasikan perbaikan untuk error `Undefined variable` yang terjadi pada saat proses *generate* struktur pertanyaan dan pencarian kueri di modul Pengawasan Perizinan Berusaha, secara khusus pada class `PertanyaanSelfDeclareService`, `PertanyaanKepatuhanTeknisService`, `PertanyaanPbUmkuService`, dan `InspeksiLapanganService`.

###### 2.1 Perbaikan `Undefined variable $nomor` pada `PertanyaanSelfDeclareService`, `PertanyaanPbUmkuService`, & `InspeksiLapanganService`

**Deskripsi Masalah**
Terdapat *bug* yang menyebabkan sistem memunculkan error `Possible undefined variable '$nomor'` pada *method* penomoran soal. Hal ini terjadi karena variabel `$nomor` diinisialisasi berdasarkan indeks kedalaman (variabel `$sub` atau `$indent`) menggunakan kondisi statis statis. Jika kedalaman sub-pertanyaan melebihi kondisi tersebut, variabel `$nomor` tidak pernah terinisialisasi sehingga menyebabkan error fatal.

**Solusi yang Diterapkan**
- Melakukan inisialisasi awal variabel `$nomor = '';` sebelum masuk ke pengecekan kondisi, sehingga selalu memiliki nilai *default* minimum.
- Mengubah kondisi logika maksimum untuk simbol penomoran dari yang sebelumnya menggunakan operasi komparasi absolut (contoh: `if ($sub === 4)`) menjadi komparasi rentang (`elseif ($sub >= 4)` atau `elseif ($indent >= 60)`), agar berapapun tingkat kedalamannya setelah limit itu tercapai, penomoran tersebut tetap memiliki *fallback* dengan benar.

###### 2.2 Perbaikan `Undefined variable $urutan` dan `$iterasi` pada `PertanyaanKepatuhanTeknisService` & `InspeksiLapanganService`

**Deskripsi Masalah**
Muncul pesan error serupa `Possible undefined variable '$urutan'` atau `'$iterasi'` pada saat pemanggilan fungsi *helper* ataupun *closure* filter database. Hal ini disebabkan karena variabel tersebut sebelumnya hanya didefinisikan apabila suatu kodisi terpenuhi dan tidak memiliki nilai *default*.

**Solusi yang Diterapkan**
- Memastikan variabel (`$urutan = 1;` atau `$iterasi = null;`) diinisialisasi dengan status aman sebelum *loop* atau eksekusi fungsi dijalankan.
- Menambahkan dokumentasi *inline* untuk fungsi `if ($kriteriaSebelumnya != $kriteria) $urutan = 1;`, yang bertujuan memperjelas bahwa kode tersebut bertugas me-reset indeks penomoran ke angka `1` setiap kali sistem menemukan set ID kriteria penilaian baru.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/263

---

### 1.102 Meningkatkan kecanggihan pemulihan HACCP memakai teknik sapuan direktori sistem (Storage Scan)

**Deskripsi Pekerjaan**
Merombak ulang logika dari script RecoverHaccpAnswers.php agar tidak lagi bergantung pada tabel DokumenHasilPengawasan (karena bisa jadi saat timeout terjadi, dokumen gagal dibuat). Sebagai gantinya, script akan langsung melakukan scanning ke dalam sistem file server (storage foto) untuk mendeteksi sasaran pemulihan.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/264

---

### 1.103 Mengkoreksi urutan berjenjang kedalaman soal kuesioner pelaporan sepihak (Self Declare)

**Deskripsi Pekerjaan**
##### Ringkasan

Cherry-pick perbaikan 5fd4e7ef8 (PR #266) ke itur/laporan-hasil-pengawasan.

##### Masalah

Pada PertanyaanSelfDeclareService::generateStrukturPertanyaan(), pemanggilan rekursif tidak meneruskan level kedalaman (\ + 1). Akibatnya \ selalu

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/267

---

### 1.104 Meremediasi gagal jumlah akumulasi (Rollup) perhitungan Nilai Kepatuhan Teknis Parent (#244)

**Deskripsi Pekerjaan**
#### Laporan Perbaikan: Akumulasi Skor Parent Kepatuhan Teknis Tidak Terhitung (Issue #244)

**Tanggal:** 2026-09-25
**Environment terdampak:** Internal / Development (DB `sip_dev`) — akan berdampak ke Staging/Production saat fitur skip-logic dirilis
**Branch:** `fix/kepatuhan-teknis-akumulasi-rollup`
**Issue:** [#244](https://github.com/psdkplabs/sipservice/issues/244)
**Status:** ✅ Fix diterapkan (menunggu uji & recompute data existing)

---

##### 1. Masalah yang Dilaporkan

Pada modul **WasRisk → Hasil Inspeksi → Formulir penilaian kepatuhan teknis** (env Internal), ditemukan ketidaksesuaian nilai:

- Nilai yang muncul di **form** sudah sesuai/benar.
- Nilai pada **PDF** dan **tabel list Hasil Inspeksi** berbeda (jauh lebih kecil) dari form.
- Di **production** nilainya benar.

Contoh objek dari tautan issue: id `20958` (KBLI `03111`, skala Besar).

- Tersimpan saat ini: **25 → "kurang baik"**.
- Seharusnya: **100 → "baik sekali"**.

---

##### 2. Investigasi & Akar Masalah

Nilai akhir dihitung di `jawab()` → `generateHasil()`: total = **SUM skor pertanyaan top-level** (`parent_id NULL`) per kriteria. Skor top-level container seharusnya diisi oleh algoritma **rollup akumulasi** (blok FIX 1) di `jawab()`. Namun rollup gagal, sehingga beberapa kriteria bernilai `0` dan total jadi jauh lebih kecil.

Ditemukan **dua bug** pada rollup tersebut:

| # | Temuan | Akar Masalah |
|---|--------|--------------|
| 1 | Kriteria besar (mis. "Pemenuhan persyaratan khusus usaha" = 40 poin) selalu `0` walau seluruh sub-pertanyaan sudah dijawab | `$pertanyaanTerjawabIds->push($pertanyaan->id)` menambahkan ID parent yang **sudah ada** (node perantara yang punya record jawaban sendiri). Akibatnya `$pertanyaanTerjawabIds->intersect($pertanyaanChildId)->count()` bisa **lebih besar** dari jumlah child (mis. `9` vs `7`). Cek `if ($jawabanChildCount != $pertanyaanChildId->count()) continue;` jadi selalu `continue`, sehingga ancestor tidak pernah di-rollup |
| 2 | Kriteria yang memiliki baris "penjelasan" selalu `0` | Baris `isPenjelasan()` (`auto_check=1 && skor=0`) tidak pernah punya record jawaban, tetapi ikut dihitung dalam syarat "semua child harus terjawab", sehingga parent tidak pernah memenuhi syarat rollup |

> **Catatan regresi:** kedua bug ini berada di dalam fitur akumulasi skor + skip-logic (`commit 364cab3e3`) yang **belum ada di branch `production`**. Itulah sebabnya production benar sedangkan Internal/dev salah. Bug ini **akan terbawa ke production** saat fitur tersebut dirilis bila tidak diperbaiki lebih dulu.

---

##### 3. Solusi yang Diterapkan

Perbaikan lokal pada `PertanyaanKepatuhanTeknisService::jawab()` (blok `FIX 1`):

1. Cek "semua child _answerable_ sudah terjawab" memakai `diff` (kebal terhadap ID duplikat) menggantikan `intersect()->count()`.
2. Menambahkan `->unique()` setelah `push()` agar `$pertanyaanTerjawabIds` tidak menumpuk duplikat.
3. Mengecualikan child `isPenjelasan()` dari syarat "semua child terjawab" sekaligus dari penjumlahan skor.

---

##### 4. Validasi

Simulasi ulang rollup + `generateHasil()` pada data dev (objek `20958`):

| Kriteria | Bobot | Sebelum | Sesudah |
|----------|------:|--------:|--------:|
| 1. Pemenuhan persyaratan umum usaha | 20 | 0 | 20 |
| 2. Pemenuhan persyaratan khusus usaha | 40 | 0 | 40 |
| 3. Pemenuhan sarana | 5 | 5 | 5 |
| 4. Kesesuaian struktur organisasi & SDM | 10 | 0 | 10 |
| 5. Pemenuhan pelayanan | 5 | 5 | 5 |
| 6. Pemenuhan persyaratan Produk/Proses/Jasa | 15 | 15 | 15 |
| 7. Pemenuhan sistem manajemen usaha | 5 | 0 | 5 |
| **Total** | **100** | **25 ("kurang baik")** | **100 ("baik sekali")** |

Rentang predikat subsektor 2: `0–49` kurang baik, `50–70` baik, `71–100` baik sekali.

- `php -l` pada file service: **No syntax errors detected**.

---

##### 5. File yang Berubah

| File | Perubahan |
|------|-----------|
| `app/Services/PengawasanPerizinanBerusaha/PertanyaanKepatuhanTeknisService.php` | Fix rollup akumulasi skor parent: `diff` check, `unique()` setelah `push()`, exclude baris `isPenjelasan()` |

---

##### 6. Langkah Selanjutnya

> [!IMPORTANT]
> - Fix ini hanya memperbaiki **penyimpanan ke depan**. Data objek yang sudah telanjur tersimpan salah **tidak berubah otomatis**.
> - Untuk data existing dibutuhkan **recompute** (bukan jawab ulang, bukan sekadar regenerate PDF): jalankan ulang rollup + `generateHasil()` dari jawaban yang sudah tersimpan, lalu regenerate PDF & BAP.
> - Belum tersedia command/seeder untuk recompute; disarankan menambahkan opsi **non-destruktif** pada `ResetObjekPengawasanSeeder` (mirip pola "Fix Teks Analisis").
> - Pastikan fix ini ikut ter-merge saat fitur skip-logic/akumulasi dirilis ke `production`.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/268

---

### 1.105 Mengusung perkakas bedah perbaikan angka (Non-Destruktif) beserta pembersihan modul teknis

**Deskripsi Pekerjaan**
##### Ringkasan
Lanjutan perbaikan Issue #244 (PR #268 sudah ter-merge). Berisi refactor + recompute data existing + penyamaan skor.

##### Perubahan
- **Refactor** `PertanyaanKepatuhanTeknisService`: logika inti `jawab()` diekstrak ke `prosesJawabanDanHasil()`, `storeJawabanDanSkor()`, `injectAutoYesOnNo()`, `rollupAkumulasiSkorParent()`, `simpanAnalisisHasil()` — perilaku tidak berubah.
- **`recalculateHasil(ObjekPengawasan)`**: recompute nilai/hasil dari jawaban tersimpan tanpa hapus/menjawab ulang (idempoten).
- **`ResetObjekPengawasanSeeder`**: opsi baru *Recompute Nilai & Hasil Kepatuhan Teknis (Rollup, tanpa hapus jawaban)* + regenerate PDF/BAP.
- **`pertanyaan()`**: kirim `skor` **mentah** (bukan `truncateDecimal`) sehingga FE/response/DB/PDF konsisten = 100; format 2 desimal hanya di layer tampilan.
- Update `docs/report/2026-09-25_fix-akumulasi-skor-parent-kepatuhan-teknis.md` (pembaruan lanjutan, catatan optimasi, catatan FE).

##### Verifikasi
- Unit test `PertanyaanKepatuhanTeknisServiceTest`: 4 passed. `php -l` & Pint bersih.
- Recompute objek 20958: **25 → 100** (idempoten); response leaf skor mentah (`0.125`) dengan jumlah = 100.

##### Catatan
- Optimasi N+1 (cache CPIB/CBIB, `keyBy('id')`, `upsert()` batch) sengaja belum diterapkan — dicatat di report §8.
- Catatan FE (repo `sip`, format tampilan 2 desimal) di report §9.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/269

---

### 1.106 Mencerabut buntut angka bayangan palsu imbas konversi numerik aplikasi

**Deskripsi Pekerjaan**
##### Masalah
Setelah `skor` dikirim mentah (PR #269), kolom `skor` bertipe `double(6,4)` membuat nilai seperti `1.91` terbaca sebagai `1.9100000000000001` dan ikut terkirim di response API.

Contoh (dev): node `90b21313` ("Daerah penangkapan ikan") -> `"skor": 1.9100000000000001`.

##### Perbaikan
Di `pertanyaanSkor()` (`generateStrukturPertanyaan()`), nilai dikembalikan dengan `round(x, 4)`:
- Membuang artefak float: `1.9100000000000001` -> `1.91`.
- Tetap mempertahankan presisi bobot 3-desimal (`0.125` tetap `0.125`).
- Tidak memakai `round(x, 2)` karena akan merusak `0.125` -> `0.13`.

##### Verifikasi
- API: `90b21313` -> `1.91`; leaf `0.125` tetap; jumlah leaf skor = `100`.
- Unit test `PertanyaanKepatuhanTeknisServiceTest`: 4 passed. `php -l` & Pint bersih.

##### Catatan
- Response dev yang dilaporkan juga menampilkan `analisis: "total nilai 25"` — itu **data lama yang belum di-recompute** (bukan bug kode). Jalankan opsi seeder *Recompute Nilai & Hasil Kepatuhan Teknis* (atau `recalculateHasil()`) untuk objek tersebut agar `nilai_kepatuhan` & analisis konsisten (100).

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/270

---

### 1.107 Memperbaiki celah pengecekan soal dari fitur waktu lampau

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/271

---

### 1.108 Menyumbat kehadiran rincian antrean daftar tunggu pengawasan di ambang kalender usang

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/272

---

### 1.109 Menempatkan jam pasir (Hitung Mundur) hari pengawasan berbarengan injeksi kode KM Surat Pemberitahuan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/276

---

### 1.110 Menyiagakan sisipan penjelasan keterangan panduan BKPM form

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/278

---

### 1.111 Merinci besaran maksimum data terunggah di jendela pemberitahuan server (Validation Message)

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/279

---

### 1.112 Memperketat rute validasi induk tautan URL (Host) pada dokumen penyerta pengawasan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/280

---

### 1.113 Merekam tipe identitas jenis usaha ke pusat form data perusahaan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/282

---

### 1.114 Menghidupkan alarm pewajiban perlengkapan pindaian bukti lapangan di dokumen Laporan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/284

---

### 1.115 Menciptakan kerangka saringan penerimaan spesifikasi media dokumentasi Inspeksi

**Deskripsi Pekerjaan**
…on documentation validation

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/285

---

### 1.116 Memberdayakan utilitas pencatatan arsip awal formulir akhir secara sunyi (Draft Tab 3)

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/286

---

### 1.117 Memperbaiki letak rincian izin keamanan pada hak pengawas persuratan (Seeder)

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/287

---

### 1.118 Memasukkan nomenklatur (KM) tambahan di ranah berkas Pemberitahuan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/290

---

### 1.119 Mengkoreksi inkonsistensi perlakuan label administrasi PW129 kembali menuju PW120

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/292

---

### 1.120 Mendaftarkan parameter tambahan PW140 / PW150 ke tubuh KM Laporan Kunjungan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/293

---

### 1.121 Mengintegrasikan otomatisasi pengkategorian CSRS untuk naskah STWAP dan HUWAP Pusat

**Deskripsi Pekerjaan**
- Menghapus surat_pemberitahuan dan stkl dari list jenis manual agar mendukung CSRS

- Menambahkan mapping STKL ke STWAP sesuai aturan otomatisasi

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/294

---

### 1.122 Menyuntikkan alarm peringatan telat sinkron WhatsApp ke gawai ponsel Pengawas Lapangan (#288)

**Deskripsi Pekerjaan**
##### Perbaikan Notifikasi WA Laporan Hasil Pengawasan (Issue #288)

PR ini mengimplementasikan notifikasi pengingat sinkronisasi Nota Dinas Laporan Hasil Pengawasan (LHP) untuk **Pengawas Perikanan** sesuai dengan spesifikasi pada PRD LHP Bagian 9 & 12.2, serta menyelesaikan issue #288.

###### Perubahan yang Dilakukan:
1. **Format Teks Notifikasi WA (Sesuai PRD)**: 
   - Teks disesuaikan agar menyebutkan tautan FE (`<<tautan>>` -> `config('app.fe.url')`).
   - Tanggal deadline diformat secara spesifik: `"H+14 dan tanggal 2 awal kuartal berikutnya"` (contoh: *14 Agustus 2026 dan tanggal 2 Oktober 2026*). Format ini dihitung otomatis dengan bantuan `LaporanHasilPengawasanService::hitungDeadline()`.
2. **Perbaikan Gerbang Environment (UAT vs DEV_MODE)**:
   - Fitur *auto-generate Nota Dinas dummy* saat BAP disimpan yang sebelumnya digerbangi `config('app.uat')`, kini telah dikoreksi menjadi `config('app.dev_mode')`. 
   - Hal ini sesuai aturan arsitektur di `AGENTS.md` (DEV_MODE untuk produksi dokumen dummy) dan `PRD LHP §12.2` (API trigger generator UAT harus dilindungi middleware `dev.mode`).
3. **Pengembalian Arsitektur Single Lightweight Job (Cron)**:
   - Pengiriman WA ke pengawas dilakukan secara tersentralisasi via scheduler `NotifikasiSinkronisasiLaporanCommand` pada jam `08:00` pada **hari-H jatuh tempo**.
   - Hal ini mencegah bug pengiriman instan saat BAP baru saja disubmit, demi mematuhi *Single Responsibility* & *Single Lightweight Job* yang dituliskan di PRD.

###### Cara Melakukan Pengujian (Testing):
Karena notifikasi tidak dikirim seketika saat BAP disimpan (harus menunggu hari ke-14), gunakan cara ini untuk mengujinya secara instan tanpa perlu memutar waktu OS:

1. **Siapkan Objek ke Keadaan Jatuh Tempo:**
   ```bash
   php artisan ppbbr:uat-simulasi-laporan {id_objek} --skenario=notif --reset
   ```
   *(Perintah ini akan mereset laporan, mengatur tanggal BAP agar jatuh tempo tepat di hari ini, dan mengubah status menjadi Selesai)*

2. **Jalankan Scheduler Notifikasi Manual:**
   ```bash
   php artisan ppbbr:notifikasi-sinkronisasi-laporan
   ```
   *(Perintah ini akan memicu pengiriman pesan WA pengingat. Silakan periksa inbox WA Pengawas Perikanan terkait. Pastikan No. HP Pengawas terisi).*

###### Jika Anda Ingin Mengulang Input Form BAP dari UI:
Gunakan command Seeder ini untuk mengembalikan status objek menjadi "Sedang Inspeksi Lapangan" tanpa menghapus jawaban yang sudah Anda ketik:
```bash
php artisan db:seed --class="Database\Seeders\PPBBR\InspeksiLapangan\ResetObjekPengawasanSeeder"
```
Kemudian masukkan `NIB` / `ID Objek` Anda, dan pilih opsi:
**`[0] Hanya Reset Dokumen + Jadwal + Status (Inspeksi)`**

Closes #288

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/295

---

### 1.123 Mengimplementasikan percepatan drastis penemuan pegawai staf lewat penahanan data (24-Hour Cache)

**Deskripsi Pekerjaan**
- Mencari pegawai ke DB internal terlebih dahulu untuk memangkas waktu tunggu API

- Memanfaatkan kolom updated_at sebagai penanda usia data (cache).

- Jika data berusia kurang dari 24 jam, langsung kembalikan dari DB (sangat cepat).

- Jika data lebih dari 24 jam atau belum ada, hit Gateway KKP untuk memperbarui/mengisi data.

- Tetap fallback ke data lama jika Gateway mengalami gangguan.

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/296

---

### 1.124 Melindungi aplikasi dari kegagalan komunikasi perpustakaan rujukan (Master Data Kategori) otomatis

**Deskripsi Pekerjaan**
- Mencegah SP dan STKL tampil sebagai N/A di Korespondensi jika master data belum tersinkronisasi

- Mengubah Category::where()->first() menjadi Category::firstOrCreate() beserta keterangannya

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/297

---

### 1.125 Menyertakan rujukan nomor Laporan simulasi dan URL bersih pada terusan pesan simulasi (UAT)

**Deskripsi Pekerjaan**
- Menyertakan nomor surat Laporan Hasil Pengawasan (LHP) dummy pada notifikasi WhatsApp UAT agar pengawas mudah melakukan pencarian

- Mengubah tautan file LHP dari route API yang ter-auth menjadi path public langsung (bucket) agar bisa dibuka via WhatsApp

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/298

---

### 1.126 Membenahi anomali penulisan berderet saat ralat persuratan (Edit Offset) STKL / SP

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/299

---

### 1.127 Mewajibkan mesin memilah kecocokan file berjalan seraya mengawal kelengkapan metadata file lama

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/301

---

### 1.128 Menyiapkan peralatan pelacak deteksi kerusakan nama dan pindaian palsu tanpa OCR Ekstrak

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/303

---

### 1.129 Mengamankan arus fungsi penuangan (Ekspor Excel) laporan massal pada kasus kekosongan data

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/304

---

### 1.130 Mewajibkan kepastian relevansi berkas NKU asli pada kelengkapan arsip bawaan Pengawasan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/305

---

### 1.131 Mengeksekusi penutupan perlindungan penyertaan unggahan selaras dengan syarat Notula berjalan

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/306

---

### 1.132 Merapikan literasi panduan rute peringatan (Notification UAT) gerbang aplikasi internal

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/307

---

### 1.133 Mengurung perlengkapan rujukan tautan Berita Acara seutuhnya di ambang ruang kerja simulasi (DEV MODE)

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/308

---

### 1.134 Menyisipkan jejak langkah STKL pada jendela persetujuan OSS

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/309

---

### 1.135 Memperbaiki kecacatan pelengkapan form saat informasi ST turunan dinyatakan invalid

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/312

---

### 1.136 Fitur/laporan hasil pengawasan: perbaiki reset data jomplang

**Deskripsi Pekerjaan**
*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*

**Dokumentasi**
- https://github.com/psdkplabs/sipservice/pull/313

---

# DETAIL LAPORAN KEGIATAN GITHUB

## 1. Penyusunan Webservice Modul Penanganan Pelanggaran

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem menyusun webservice Modul Penanganan Pelanggaran, sebagai berikut:

### 1.1 Menyusun webservice penetapan sanksi administrasi

**Deskripsi Pekerjaan**
Telah disusun webservice penetapan sanksi administrasi pada Modul Penanganan Pelanggaran, termasuk pencarian data pelanggaran, kelompok pelanggar, dan pencarian data Portal KKPRL.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Gateway/Entities/OSS/PerizinanProyek.php
- Modules/Gateway/Http/Controllers/PortalData/PencarianPerizinanKKPRLController.php
- Modules/Gateway/Routes/api.php
- Modules/Gateway/Services/PORTALDATA/PencarianPerizinanKKPRLService.php
- Modules/PenangananPelanggaran/Config/.gitkeep
- Modules/PenangananPelanggaran/Config/config.php
- Modules/PenangananPelanggaran/Console/.gitkeep
- Modules/PenangananPelanggaran/Database/Migrations/.gitkeep
- Modules/PenangananPelanggaran/Database/Seeders/.gitkeep
- Modules/PenangananPelanggaran/Database/Seeders/PenangananPelanggaranDatabaseSeeder.php

**Perubahan Utama:**
- Endpoint penetapan sanksi administrasi.
- Pencarian pelanggaran dan peningkatan kelompok pelanggar.
- Pencarian data Portal untuk KKPRL.

**Manfaat:**
- Penetapan sanksi administrasi dapat dicatat di dalam sistem.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/167deac764df376faa76f817377317bcadbbed65

---

### 1.2 Memperbaharui penandaan penetapan sanksi dan subjek hukum

**Deskripsi Pekerjaan**
Telah diperbarui penandaan (tandai) penetapan sanksi serta pemilihan subjek hukum lebih dari satu.

**Detail Perubahan**

**File yang Diubah:**
- Modules/PenangananPelanggaran/Services/PenetapanSanksiService.php
- Modules/Gateway/Entities/OSS/PerizinanProyek.php
- Modules/Gateway/Entities/PortalDokumen.php
- Modules/PenangananPelanggaran/Http/Requests/PenetapanSanksi/TandaiPenetapanSanksiRequest.php
- Modules/PenangananPelanggaran/Transformers/PenetapanSanksiResource.php
- Modules/Userman/Database/Migrations/2026_03_06_064823_add_nib_to_portal_dokumen_pelanggaran_table.php
- Modules/Userman/Database/Migrations/2026_03_06_065742_add_has_related_subjek_hukum_to_portal_dokumen_table.php
- Modules/Userman/Database/Migrations/2026_03_06_080907_create_portal_subjek_hukum_table.php
- Modules/Userman/Entities/KKPRL/Perizinan.php
- Modules/Userman/Entities/Master/PortalKorespondensiCRS/PenangananPelanggaran.php

**Perubahan Utama:**
- Penandaan penetapan sanksi dan pembaruan data penandaan.
- Pemilihan lebih dari satu subjek hukum dan PenetapanSanksiResource.
- Filter tambahan dan perbaikan typo subjek hukum.

**Manfaat:**
- Satu penetapan sanksi dapat mencakup beberapa subjek hukum.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/f649f26b45c4eb3e0895d35737a13e8e632279ec
- https://github.com/psdkplabs/api-sip/commit/f50fc20c80714ca4de36f7b14a4838bafc5182e5

---

### 1.3 Filter dan response daftar penetapan sanksi

**Deskripsi Pekerjaan**
Telah diperbaiki filter daftar penetapan sanksi, pencarian berdasarkan tipe kategori, dan penyesuaian response jenis pelanggaran.

**Detail Perubahan**

**File yang Diubah:**
- Modules/PenangananPelanggaran/Services/PenetapanSanksiService.php
- Modules/PenangananPelanggaran/Transformers/PenetapanSanksiResource.php

**Perubahan Utama:**
- Perbaikan filter penetapan sanksi.
- Pencarian berdasarkan kategori dan tipe kategori.
- Penyesuaian response jenis pelanggaran pada daftar.

**Manfaat:**
- Daftar penetapan sanksi mudah disaring.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/199cc398498fdf7a8932a43a8b5758e30a5cd47f
- https://github.com/psdkplabs/api-sip/commit/c78bdf272c60cc7ecb973dd8c0dc76a3e5b086e3
- https://github.com/psdkplabs/api-sip/commit/94021231ae249fdc32e11a0d777507ee95f0e07c

---

### 1.4 Penanganan error dan perbaikan data penetapan sanksi

**Deskripsi Pekerjaan**
Telah ditambahkan penanganan error dan URL dokumen pada penetapan sanksi serta perbaikan typo dan singkatan.

**Detail Perubahan**

**File yang Diubah:**
- Modules/PenangananPelanggaran/Services/PenetapanSanksiService.php
- Modules/PenangananPelanggaran/Transformers/PenetapanSanksiResource.php
- Modules/PenangananPelanggaran/Http/Requests/PenetapanSanksi/TandaiPenetapanSanksiRequest.php
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Gateway/Services/OSS/V2/PencarianPerizinanBerusahaService.php
- Modules/Gateway/Services/PORTALDATA/PencarianPerizinanKKPRLService.php
- app/Http/Resources/Gateway/OSS/V2/PelakuUsahaResource.php
- app/Http/Resources/Gateway/PortalData/IdentitasResource.php

**Perubahan Utama:**
- Penanganan error penetapan sanksi.
- Penambahan URL dokumen.
- Perbaikan typo dan singkatan.

**Manfaat:**
- Proses penetapan sanksi tidak terhenti karena error data.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/fd71918f2d6e1f1b104e3592bfa19a147679b7c9
- https://github.com/psdkplabs/api-sip/commit/c554548a327ae7094378b5f4a3965990573b9a17
- https://github.com/psdkplabs/api-sip/commit/4577f6685f6afba2023a4590cb4fee00e3367b0d
- https://github.com/psdkplabs/api-sip/commit/b689c2c986984a81772fa43af8492891e4388a17
- https://github.com/psdkplabs/api-sip/commit/0a75899c5dd170d0314a3196664fdf788be52807
- https://github.com/psdkplabs/api-sip/commit/f189aad84caf2ef072f200f45796c2d6cdc81101
- https://github.com/psdkplabs/api-sip/commit/2a460826027a420b39ab0754c40f16956ba90b34

---

### 1.5 Menyusun pengelolaan denda

**Deskripsi Pekerjaan**
Telah ditambahkan pengelolaan nilai denda pada penetapan sanksi administrasi beserta validasinya.

**Detail Perubahan**

**File yang Diubah:**
- Modules/PenangananPelanggaran/Http/Requests/PenetapanSanksi/TandaiPenetapanSanksiRequest.php
- Modules/PenangananPelanggaran/Transformers/PenetapanSanksiResource.php
- Modules/PenangananPelanggaran/Services/PenetapanSanksiService.php

**Perubahan Utama:**
- Flag denda pada penetapan sanksi.
- Validasi nilai denda dan penyesuaian field nilai_denda.
- Perbaikan validasi request.

**Manfaat:**
- Nilai denda tersimpan dengan format yang benar.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/65216fa6ae575929a268b824d2d863dcfb6995f6
- https://github.com/psdkplabs/api-sip/commit/3715dbc43da564ee3e0675844557d36572096a4e
- https://github.com/psdkplabs/api-sip/commit/d59d6631e4aa0be4ee790fec3c701f997d3025cf
- https://github.com/psdkplabs/api-sip/commit/9a4dc70455118b81f1f2d2fb6c6d7ce6590d1a70
- https://github.com/psdkplabs/api-sip/commit/074152b49a3d64b755c81d24aa1bcce4512d010a

---

### 1.6 Memperbaharui pencarian pelanggaran dan jenis pelanggaran

**Deskripsi Pekerjaan**
Telah diperbarui pencarian data pelanggaran berdasarkan kategori dan jenis pelanggaran.

**Detail Perubahan**

**File yang Diubah:**
- Modules/SadarGakum/Transformers/PencarianPelanggaranResource.php
- Modules/PenangananPelanggaran/Http/Requests/PenetapanSanksi/TandaiPenetapanSanksiRequest.php
- Modules/SadarGakum/Services/KategoriPelanggaranService.php
- Modules/SadarGakum/Entities/JenisPelanggaran.php
- Modules/Gateway/Services/PORTALDATA/KKPRLService.php
- Modules/SadarGakum/Services/PencarianPelanggaranService.php
- Modules/SadarGakum/Http/Controllers/JenisPelanggaranController.php

**Perubahan Utama:**
- Filter kategori pelanggaran dan pencarian berdasarkan jenis pelanggaran.
- Parameter usage pada jenis pelanggaran.
- Perbaikan validasi request, ID pelanggaran, dan validasi string tipe kategori.

**Manfaat:**
- Data pelanggaran mudah ditemukan saat penetapan sanksi.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/e1e0c82122d6b81daf416fc30de664291a6ed93b
- https://github.com/psdkplabs/api-sip/commit/349abba0a48432bad905e229b940665c25bd07fe
- https://github.com/psdkplabs/api-sip/commit/0b9313d096e6968bc02c5adf648c747e6d24b6d4
- https://github.com/psdkplabs/api-sip/commit/b093ad3fc7721d8d1e2b11d3712f07f825374d7f
- https://github.com/psdkplabs/api-sip/commit/46b6c5e7d6b5d9d7aa22e31ca89b0d4cb5120d2a
- https://github.com/psdkplabs/api-sip/commit/55dc2a302957b52aa6ac24d793ccf87c14c80540

---

### 1.7 Menyusun relasi pengamatan dengan penetapan sanksi

**Deskripsi Pekerjaan**
Telah disusun relasi data pengamatan tidak langsung dan pengamatan langsung dengan penetapan sanksi berdasarkan nomor penerbitan.

**Detail Perubahan**

**File yang Diubah:**
- Modules/PengawasanPerizinanBerusaha/Services/SDK/PemantauanService.php
- Modules/PenangananPelanggaran/Services/PenetapanSanksiService.php
- Modules/PengawasanPerizinanBerusaha/Transformers/SDK/PemantauanResource.php
- Modules/PenangananPelanggaran/Http/Requests/PenetapanSanksi/TandaiPenetapanSanksiRequest.php
- Modules/Userman/Database/Migrations/2026_03_05_105037_add_nomor_izin_to_portal_dokumen_pelanggaran_table.php
- Modules/Userman/Entities/KKPRL/Perizinan.php
- Modules/PenangananPelanggaran/Transformers/PenetapanSanksiResource.php
- app/Http/Resources/Gateway/OSS/V2/SubjekHukumResource.php

**Perubahan Utama:**
- Relasi pengamatan tidak langsung ke penetapan sanksi.
- Relasi pengamatan langsung berdasarkan nomor penerbitan.
- Perbaikan format jenis izin pada relasi.

**Manfaat:**
- Riwayat sanksi dapat dilihat dari data pengamatan.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/39d2186f12399022dce1054cf5887789c9edbbd4
- https://github.com/psdkplabs/api-sip/commit/b9b8680f7fb13bcd049552a092820e9602379aaa
- https://github.com/psdkplabs/api-sip/commit/4667b1ae3db9b6b810bc3a0b373af46d8bc4e151
- https://github.com/psdkplabs/api-sip/commit/e68a58c44a7700a2b2befab6e7000784e5c15f46

---

## 2. Pembaharuan Webservice Modul Master Data

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem memperbaharui webservice Modul Master Data, sebagai berikut:

### 2.1 Perbaikan master data berdasarkan dokumen perbaikan pengguna

**Deskripsi Pekerjaan**
Telah dilakukan perbaikan master data berdasarkan dokumen perbaikan dari pengguna, meliputi pengelolaan master data MOMI, filter tahun laporan, kategori wilayah, dan status izin.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Gateway/Entities/PortalDokumen.php
- Modules/PengawasanPerizinanBerusaha/Services/SDK/PemantauanService.php
- Modules/PengawasanPerizinanBerusaha/Transformers/SDK/PemantauanResource.php
- Modules/Userman/Exports/Master/KKPRLPerizinanExport.php
- Modules/Userman/Http/Controllers/MomiController.php
- Modules/Userman/Library/SortableService.php
- Modules/Userman/Services/Master/KKPRL/LaporanTahunanService.php
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Userman/Services/Master/KorespondensiCSRS/KorespondensiCRSService.php
- Modules/Userman/Services/Master/MomiService.php

**Perubahan Utama:**
- Pengelolaan master data MOMI.
- Filter tahun laporan dan kolom tambahan.
- Kategori wilayah dan status izin.

**Manfaat:**
- Master data sesuai dengan masukan pengguna.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/c6c4d3b2eeb96ea299d0f42d64a94909edacf569

---

### 2.2 Memperbaharui relasi, GeoJSON, dan middleware MOMI

**Deskripsi Pekerjaan**
Telah diperbaiki relasi MOMI pada pengamatan tidak langsung, tampilan GeoJSON MOMI, dan penambahan middleware.

**Detail Perubahan**

**File yang Diubah:**
- Modules/PengawasanPerizinanBerusaha/Services/SDK/PemantauanService.php
- Modules/PengawasanPerizinanBerusaha/Transformers/SDK/PemantauanResource.php
- Modules/Userman/Entities/KKPRL/Perizinan.php
- Modules/Userman/Transformers/PerizinanMomiResource.php
- Modules/Userman/Http/Controllers/MomiController.php

**Perubahan Utama:**
- Perbaikan relasi MOMI di pengamatan tidak langsung.
- Tampilan GeoJSON MOMI.
- Middleware pada MOMI.

**Manfaat:**
- Data MOMI tampil benar dan aksesnya terlindungi.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/cb1c56b021374ca5e072729821449ad5ed455223
- https://github.com/psdkplabs/api-sip/commit/d90c96e5e02f8d4f906b3a1e9f37893b955f30f6
- https://github.com/psdkplabs/api-sip/commit/df48271bb495b7dcbf8d7e9ffc71c8ad9ef66c02

---

### 2.3 Filter dan validasi MOMI

**Deskripsi Pekerjaan**
Telah ditambahkan filter MOMI serta perbaikan validasi dan resource MOMI.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Transformers/PerizinanMomiResource.php
- Modules/Userman/Http/Requests/Master/MOMI/AddMomiRequest.php
- Modules/PenangananPelanggaran/Transformers/PenetapanSanksiResource.php
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Userman/Services/Master/MomiService.php
- Modules/Userman/Transformers/KKPRL/PerizinanResource.php
- app/Http/Library/StringHelper.php

**Perubahan Utama:**
- Filter MOMI dan perbaikan URL dokumen.
- Pembaruan resource MOMI.
- Perbaikan validasi MOMI.

**Manfaat:**
- Input MOMI tervalidasi sebelum tersimpan.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/5c2d15ab7c6844b8c8e850afab7b41738a050fe8
- https://github.com/psdkplabs/api-sip/commit/367bace04670ed03a7d0bd29277b4c6a09c1f89d
- https://github.com/psdkplabs/api-sip/commit/0c0ffc27f7662a9fbf1a617e53dd980491a5ce7d
- https://github.com/psdkplabs/api-sip/commit/69ae485e335616e2c18ea517cd008404655d768c

---

### 2.4 Filter jenis keterangan dan kelengkapan KKPRL

**Deskripsi Pekerjaan**
Telah ditambahkan filter jenis keterangan dan filter data tidak lengkap untuk seluruh perizinan KKPRL.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Gateway/Services/OSS/V2/PencarianPerizinanBerusahaService.php
- Modules/Gateway/Services/PORTALDATA/PencarianPerizinanKKPRLService.php
- Modules/PenangananPelanggaran/Http/Controllers/PenangananPelanggaranController.php
- Modules/PenangananPelanggaran/Http/Requests/PenetapanSanksi/TandaiPenetapanSanksiRequest.php
- Modules/PenangananPelanggaran/Routes/api.php
- Modules/PenangananPelanggaran/Services/PenetapanSanksiService.php
- Modules/PenangananPelanggaran/Transformers/PenetapanSanksiResource.php
- Modules/Userman/Http/Controllers/Master/KKPRL/KKPRLController.php
- Modules/Userman/Transformers/KKPRL/PerizinanResource.php

**Perubahan Utama:**
- Filter keterangan true/false dan dropdown.
- Filter in_complete termasuk nilai null.
- Filter in_complete untuk seluruh perizinan KKPRL.

**Manfaat:**
- Data KKPRL yang belum lengkap mudah diidentifikasi.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/840e87cac021facef441762872893c0eeff3a689
- https://github.com/psdkplabs/api-sip/commit/52b1ac90b8a36d9c73b6ae2783d8656f90b8d8a6
- https://github.com/psdkplabs/api-sip/commit/57d239c0aae13e8390c86939bab5535624bed840

---

### 2.5 Menyusun PerizinanService dan pencarian KKPRL

**Deskripsi Pekerjaan**
Telah diimplementasikan PerizinanService untuk pengelolaan data perizinan KKPRL serta perbaikan pencarian dan tampilan NIB.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php

**Perubahan Utama:**
- PerizinanService untuk data perizinan KKPRL.
- Perbaikan pencarian KKPRL.
- Perbaikan tampilan NIB pada detail.

**Manfaat:**
- Logika perizinan KKPRL terpusat di satu service.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/3beccc35af34fcd4ba50293a0f4cae8bd8977304
- https://github.com/psdkplabs/api-sip/commit/7f4fafdbeb400f52365e5b392dd92d8d074f740a
- https://github.com/psdkplabs/api-sip/commit/afd1fef7723d125ae8ef87e087cfa5e96b315939
- https://github.com/psdkplabs/api-sip/commit/c3e1adc318297dfad80a174f5ba93712bfad7ae0

---

### 2.6 Perbaikan unit inspeksi, GeoJSON WIUP, dan middleware KKPRL

**Deskripsi Pekerjaan**
Telah diperbaiki penentuan unit inspeksi, tampilan GeoJSON berdasarkan kode WIUP, penanganan file kosong, serta middleware KKPRL dan penanganan pelanggaran.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Userman/Services/Master/MomiService.php
- Modules/Userman/Services/Sync/SyncMasterService.php
- Modules/Userman/Transformers/PerizinanMomiResource.php
- Modules/PenangananPelanggaran/Http/Controllers/PenangananPelanggaranController.php
- Modules/Userman/Http/Controllers/Master/KKPRL/KKPRLController.php

**Perubahan Utama:**
- Perbaikan unit inspeksi.
- Kode WIUP untuk menampilkan GeoJSON.
- Penanganan error getRealPath() on null.
- Middleware KKPRL dan penanganan pelanggaran.

**Manfaat:**
- Endpoint KKPRL stabil dan terlindungi.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/04d481c82985bd7cab975367d783788203a31312
- https://github.com/psdkplabs/api-sip/commit/28680e1d80081466fc5051bba326bd66a613521f
- https://github.com/psdkplabs/api-sip/commit/6ccbffaad0659bc73fd2057ecb35871ab1f90882
- https://github.com/psdkplabs/api-sip/commit/c1628ea1591fd7f591d74bfa7825538ca353bd51

---

### 2.7 Memperbaharui penyimpanan NIB, NPWP, dan sinkronisasi OSS

**Deskripsi Pekerjaan**
Telah diperbaiki penyimpanan NIB dan NPWP serta sinkronisasi OSS ketika NIB belum tersedia di database.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Http/Requests/Master/MOMI/AddMomiRequest.php
- Modules/Userman/Services/Master/MomiService.php
- Modules/Gateway/Services/OSS/V2/PencarianPerizinanBerusahaService.php

**Perubahan Utama:**
- Perbaikan penyimpanan NIB dan NPWP.
- Sinkronisasi OSS ketika NIB belum ada di database.

**Manfaat:**
- Data pelaku usaha mengikuti data terbaru OSS.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/68a42a0b55dcf59454515e680e7587a605458c57
- https://github.com/psdkplabs/api-sip/commit/c301da1d2bb17ae6a974bd8b703b0e44f8d9579f
- https://github.com/psdkplabs/api-sip/commit/59e354b40e5b2c4eec1964a4e9c30b2b571f97c9

---

### 2.8 Menyusun export korespondensi dan master data

**Deskripsi Pekerjaan**
Telah disusun export korespondensi serta refactor export MOMI, KKPRL, dan laporan tahunan beserta sorting.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/KorespondensiCSRS/KorespondensiCRSService.php
- routes/modul/master.php
- Modules/Userman/Exports/Master/KorespondensiExport.php
- Modules/Userman/Http/Controllers/Master/PotalCRS/KorespondensiCRSController.php
- Modules/Userman/Jobs/Email/ExportDataJob.php
- Modules/Userman/Services/Master/KKPRL/LaporanTahunanService.php
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Userman/Services/Master/MomiService.php
- app/Http/Controllers/API/V1/RBAC/FeatureController.php
- app/Http/Controllers/API/V1/RBAC/ModulController.php

**Perubahan Utama:**
- Export korespondensi.
- Refactor export MOMI, korespondensi, KKPRL, dan laporan tahunan.
- Perbaikan RBAC resource.

**Manfaat:**
- Data master dapat diunduh untuk pelaporan.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/f82e9a0936bed0ec3ea25aba6227ad9cb4ad3b1b
- https://github.com/psdkplabs/api-sip/commit/aa380feb41af35d2f2bed2fc5a07263f4abedccb
- https://github.com/psdkplabs/api-sip/commit/9aa3c3215b10a1915bef3c0b8a18604ea98e0336

---

### 2.9 Perbaikan penandaan dan tampilan file korespondensi

**Deskripsi Pekerjaan**
Telah diperbaiki penandaan korespondensi dan tampilan file surat serta refactor sinkron korespondensi.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/KorespondensiCSRS/KorespondensiCRSService.php
- Modules/PenangananPelanggaran/Transformers/PenetapanSanksiResource.php
- Modules/Userman/Jobs/Sync/SyncKorespondensiJob.php

**Perubahan Utama:**
- Perbaikan tandai korespondensi.
- Perbaikan error tampilan file korespondensi.
- Refactor sinkron korespondensi.

**Manfaat:**
- File surat dapat dibuka tanpa error.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/af17c2da31524072ea23e14cc6cb47f734bd280e
- https://github.com/psdkplabs/api-sip/commit/0156a6a0f1fbab856c52e4294ab50ac08fe2c717

---

### 2.10 Memperbaharui permission Master Data, Asta Data, dan Penanganan Pelanggaran

**Deskripsi Pekerjaan**
Telah disusun permission untuk menu Master Data, Asta Data, dan Penanganan Pelanggaran beserta export penetapan sanksi.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Gateway/Routes/api.php
- Modules/PenangananPelanggaran/Database/Seeders/AkunTableSeeder.php
- Modules/PenangananPelanggaran/Database/Seeders/PenangananPelanggaranDatabaseSeeder.php
- Modules/PenangananPelanggaran/Http/Controllers/PenangananPelanggaranController.php
- Modules/PenangananPelanggaran/Routes/api.php
- Modules/PenangananPelanggaran/Services/PenetapanSanksiService.php
- Modules/PengawasanPerizinanBerusaha/Database/Seeders/SDK/AkunTableSeeder.php
- Modules/PengawasanPerizinanBerusaha/Routes/api.php
- Modules/Userman/Database/Seeders/AkunMasterTableSeeder.php

**Perubahan Utama:**
- Permission master data dan penanganan pelanggaran.
- Export penetapan sanksi.

**Manfaat:**
- Akses menu baru sesuai peran pengguna.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/3b4ed7bf9ffcbb96083e113e4a4e8c991c83139d

---

## 3. Memperbaharui Webservice Integrasi OSS dan Portal Data

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem memperbaharui webservice integrasi OSS dan Portal Data pada modul Gateway, sebagai berikut:

### 3.1 Penambahan jenis izin dan NIK pada pencarian OSS dan Portal Data

**Deskripsi Pekerjaan**
Telah ditambahkan jenis izin dan NIK pada hasil pencarian OSS dan Portal Data.

**Detail Perubahan**

**File yang Diubah:**
- app/Http/Resources/Gateway/OSS/V2/PelakuUsahaResource.php
- app/Http/Resources/Gateway/PortalData/IdentitasResource.php
- Modules/PenangananPelanggaran/Http/Controllers/PenangananPelanggaranController.php
- Modules/PenangananPelanggaran/Routes/api.php
- Modules/PenangananPelanggaran/Services/PenetapanSanksiService.php
- Modules/PengawasanPerizinanBerusaha/Transformers/SDK/PemantauanDetailResource.php
- app/Http/Resources/Gateway/OSS/V2/PerizinanBerusahaResource.php

**Perubahan Utama:**
- Jenis izin pada Portal Data dan resource identitas.
- NIK pada response pencarian OSS dan Portal Data.

**Manfaat:**
- Hasil pencarian lebih informatif.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/cd212206f98c110af6034b2e195a10f48f678427
- https://github.com/psdkplabs/api-sip/commit/fd921e0b90dd2fa763da8562e3cf83188efcdf6e

---

### 3.2 Perbaikan pencarian perizinan berusaha

**Deskripsi Pekerjaan**
Telah diperbaiki service pencarian perizinan berusaha dan refactor bagian OSS yang terlewat.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Gateway/Transformers/OSS/PerizinanBerusahaKapal.php
- Modules/LaporanKegiatanUsaha/Services/PelaporanService.php
- app/Services/PengawasanPerizinanBerusaha/PertanyaanSelfDeclareService.php
- app/Imports/ObjekPengawasanImport.php

**Perubahan Utama:**
- Perbaikan pencarian perizinan berusaha service.
- Refactor OSS yang terlewat.

**Manfaat:**
- Pencarian perizinan berusaha mengembalikan data yang benar.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/9482cb84eb6abfb65aa426abe202697cc868c1a7
- https://github.com/psdkplabs/api-sip/commit/63c98937ae96cca3c8860044ceaf54f8b57be76a

---

### 3.3 Optimasi pencarian OSS dengan ProyekResource

**Deskripsi Pekerjaan**
Telah dioptimalkan pencarian OSS dengan resource proyek dan kapal perikanan serta perbaikan casting tanggal dan macro whereLike.

**Detail Perubahan**

**File yang Diubah:**
- app/Http/Resources/Gateway/OSS/ProyekResource.php
- app/Http/Resources/PengawasanPerizinanBerusaha/PencarianPerizinanBerusaha/ProyekResource.php
- app/Services/KapalPerikananService.php
- Modules/Gateway/Entities/OSS/PerizinanProyek.php
- app/Providers/MacroServiceProvider.php

**Perubahan Utama:**
- ProyekResource dan resource kapal perikanan.
- Perbaikan casting tanggal.
- Perbaikan macro whereLike.

**Manfaat:**
- Pencarian OSS lebih cepat.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/d1b71815f71e2117f359e36c2a96129e94bb3a89
- https://github.com/psdkplabs/api-sip/commit/36445615bfadf370c722ade06a99259f556bb453
- https://github.com/psdkplabs/api-sip/commit/dca173c6d01e26d801fc5b294f1affa694eb211f
- https://github.com/psdkplabs/api-sip/commit/382842e9c943317ed4e13035cae3049dd475fa19
- https://github.com/psdkplabs/api-sip/commit/868d10b24a43b0936ac6e57961af1abcbe10ded7

---

### 3.4 Refactor penggunaan data OSS pada layanan WasRisk

**Deskripsi Pekerjaan**
Telah dilakukan refactor penyimpanan proyek OSS dan service WasRisk yang menggunakan data OSS.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Gateway/Entities/OSS/PerizinanProyek.php
- Modules/Gateway/Http/Controllers/PencarianPerizinanBerusahaController.php
- Modules/Gateway/Services/OSS/PencarianPerizinanBerusahaService.php
- Modules/Gateway/Transformers/OSS/PerizinanBerusahaKapal.php
- Modules/LaporanKegiatanUsaha/Http/Controllers/AuthLkuController.php
- Modules/LaporanKegiatanUsaha/Services/AuthLkuService.php
- Modules/LaporanKegiatanUsaha/Services/PelaporanService.php
- app/Http/Library/StringHelper.php
- app/Http/Resources/PengawasanPerizinanBerusaha/InspeksiLapangan/InspeksiLapanganDenganPenanggungJawabResource.php
- app/Imports/ObjekPengawasanImport.php

**Perubahan Utama:**
- Refactor simpan proyek, PelaporanService, dan AuthLkuService.
- Refactor service objek pengawasan, inspeksi lapangan, BAP, self declare, dan import objek pengawasan.

**Manfaat:**
- Penggunaan data OSS seragam di seluruh layanan.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/291d8851327a22f51d6eb42c6dbf1aeca7b1ba4b
- https://github.com/psdkplabs/api-sip/commit/12ce1e712b3600edee243406fdc236a7a6a5eafd

---

### 3.5 Menyusun sinkronisasi pegawai dari Portal Data

**Deskripsi Pekerjaan**
Telah disusun sinkronisasi data pegawai dari Portal Data.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Gateway/Console/SIMPEG/SinkronPortalPegawaiCommand.php
- Modules/Gateway/Jobs/SIMPEG/SinkronDataPortalPegawai.php
- Modules/Gateway/Jobs/SIMPEG/SinkronDataSimpeg.php
- Modules/Gateway/Services/SIMPEG/PegawaiPortalDataService.php
- Modules/Userman/Jobs/Sync/KEPEGAWAIAN/SyncSimpegJob.php
- app/Console/Kernel.php
- app/Services/UserService.php
- database/seeders/UserManagement/Akun/SetupContactSeeder.php

**Perubahan Utama:**
- Job dan service sinkronisasi pegawai dari Portal Data.

**Manfaat:**
- Data pegawai mengikuti sumber resmi.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/0f2cef5ffbb59e52ddb2b0dc4ec3ed56cf508df7
- https://github.com/psdkplabs/api-sip/commit/de1dd2c3bfcfcf357dc7218e3a61e5648e3c44cb

---

## 4. Memperbaharui Webservice Modul WasRisk

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem memperbaharui webservice Modul WasRisk, sebagai berikut:

### 4.1 Perbaikan akses operator UPT yang juga pengawas perikanan

**Deskripsi Pekerjaan**
Telah diperbaiki akses operator UPT yang memiliki role Pengawas Perikanan serta validasi PPBBR.

**Detail Perubahan**

**File yang Diubah:**
- app/Services/PengawasanPerizinanBerusaha/BeritaAcaraPemeriksaanService.php
- app/Services/PengawasanPerizinanBerusaha/DokumenHasilInspeksiService.php
- app/Services/PengawasanPerizinanBerusaha/HasilInspeksiLapanganService.php
- app/Services/PengawasanPerizinanBerusaha/InspeksiLapanganService.php
- app/Services/PengawasanPerizinanBerusaha/ObjekPengawasanService.php
- app/Services/PengawasanPerizinanBerusaha/PenjadwalanService.php
- app/Services/PengawasanPerizinanBerusaha/PertanyaanKepatuhanTeknisService.php
- app/Services/PengawasanPerizinanBerusaha/PertanyaanPbUmkuService.php
- app/Services/PengawasanPerizinanBerusaha/PertanyaanSelfDeclareService.php
- app/Services/PengawasanPerizinanBerusaha/RiwayatPelakuUsahaService.php

**Perubahan Utama:**
- Operator UPT dengan role pengawas dapat mengakses data sesuai perannya.
- Perapian namespace dan perbaikan validasi PPBBR.

**Manfaat:**
- Pengguna dengan dua peran dapat bekerja tanpa bentrok.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/d362df14b5a20e8772dd37af982bc0f2a753750a

---

### 4.2 Perbaikan filter role penjadwalan, inspeksi, dan hasil inspeksi

**Deskripsi Pekerjaan**
Telah diperbaiki filter role pada penjadwalan, inspeksi lapangan, dan hasil inspeksi untuk operator UPT dan pengawas.

**Detail Perubahan**

**File yang Diubah:**
- app/Services/PengawasanPerizinanBerusaha/PenjadwalanService.php
- app/Services/PengawasanPerizinanBerusaha/HasilInspeksiLapanganService.php
- app/Services/PengawasanPerizinanBerusaha/InspeksiLapanganService.php
- app/Services/PengawasanPerizinanBerusaha/BeritaAcaraPemeriksaanService.php
- app/Services/PengawasanPerizinanBerusaha/DokumenHasilInspeksiService.php
- app/Services/PengawasanPerizinanBerusaha/ObjekPengawasanService.php
- app/Services/PengawasanPerizinanBerusaha/PertanyaanKepatuhanTeknisService.php
- app/Services/PengawasanPerizinanBerusaha/PertanyaanPbUmkuService.php
- app/Services/PengawasanPerizinanBerusaha/PertanyaanSelfDeclareService.php
- app/Services/PengawasanPerizinanBerusaha/RiwayatPelakuUsahaService.php

**Perubahan Utama:**
- Filter penjadwalan, inspeksi, dan hasil inspeksi berdasarkan role.
- Filter operator UPT dan pengawas.

**Manfaat:**
- Data yang tampil sesuai peran aktif pengguna.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/e3db0642ecd8f7fd9a51f09dc78c5948370e6a5a
- https://github.com/psdkplabs/api-sip/commit/9d29f03fd95e5d03abce378ae68c54dae4ba58c5
- https://github.com/psdkplabs/api-sip/commit/09844559205d97b0fb21fee0579bece193cb5a08
- https://github.com/psdkplabs/api-sip/commit/8b16040cfd0308d62bd0cdce22adb3848ddbe493
- https://github.com/psdkplabs/api-sip/commit/c9971981f15152c01cb672f03205063a04f5614b
- https://github.com/psdkplabs/api-sip/commit/22ce03b93b7455318fcddfc28274429f8065bdd8
- https://github.com/psdkplabs/api-sip/commit/468aa94c811e1223b0d1bb21a83a5e06c228de32
- https://github.com/psdkplabs/api-sip/commit/33ef667694cfbdff68345e4401bb9a904103ce4d

---

### 4.3 Memperbaharui template BAP dan notifikasi kirim objek pengawasan

**Deskripsi Pekerjaan**
Telah diperbarui format unit kerja pada template BAP serta notifikasi kirim objek pengawasan dengan jeda 5 menit.

**Detail Perubahan**

**File yang Diubah:**
- resources/views/header.blade.php
- app/Http/Library/WaNotifications.php
- app/Services/Gateway/WhatsappService.php
- app/Http/Controllers/API/V1/PengawasanPerizinanBerusaha/HasilInspeksiLapanganController.php
- app/Models/PengawasanPerizinanBerusaha/LaporanPengawasan/LaporanHasilInspeksi.php
- app/Models/PengawasanPerizinanBerusaha/LaporanPengawasan/RiwayatLaporanInspeksi.php
- app/Models/PengawasanPerizinanBerusaha/ObjekPengawasan/ObjekPengawasan.php
- app/Services/PengawasanPerizinanBerusaha/HasilInspeksiLapanganService.php
- database/migrations/2026_03_10_142121_crate_ppbbr_laporan_hasil_inspeksi_table.php
- routes/modul/ppbbr.php

**Perubahan Utama:**
- Format unit kerja pada BAP.
- Notifikasi kirim objek pengawasan dengan jeda 5 menit.

**Manfaat:**
- Dokumen BAP tercetak dengan data unit kerja yang benar.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/ef6558253d22e75b1691bd44c797a3c6d0823eca
- https://github.com/psdkplabs/api-sip/commit/c8d556a12606cb87c851a4b3c3f1bd54d6290fb6
- https://github.com/psdkplabs/api-sip/commit/ceb789786af097a5258921143f9de0f6937aafe8

---

### 4.4 Migrasi laporan hasil pengawasan dan perbaikan detail objek

**Deskripsi Pekerjaan**
Telah disusun migrasi tabel laporan hasil pengawasan serta perbaikan data wilayah yang kosong pada detail objek.

**Detail Perubahan**

**File yang Diubah:**
- app/Http/Controllers/API/V1/PengawasanPerizinanBerusaha/HasilInspeksiLapanganController.php
- app/Http/Resources/PengawasanPerizinanBerusaha/ObjekPengawasan/ObjekPengawasanResource.php
- app/Models/PengawasanPerizinanBerusaha/LaporanPengawasan/LaporanHasilInspeksi.php
- app/Models/PengawasanPerizinanBerusaha/LaporanPengawasan/RiwayatLaporanInspeksi.php
- app/Models/PengawasanPerizinanBerusaha/ObjekPengawasan/ObjekPengawasan.php
- app/Services/PengawasanPerizinanBerusaha/HasilInspeksiLapanganService.php
- database/migrations/2026_03_10_142121_crate_ppbbr_laporan_hasil_inspeksi_table.php
- routes/modul/ppbbr.php

**Perubahan Utama:**
- Migrasi tabel laporan hasil pengawasan.
- Perbaikan provinsi, kabupaten, kecamatan, dan kelurahan yang kosong.

**Manfaat:**
- Struktur data laporan siap digunakan.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/5182fe7b462cd5f5183427c9d54bfae7ca542ec2

---

### 4.5 Menyusun laporan dan verifikasi hasil inspeksi

**Deskripsi Pekerjaan**
Telah disusun webservice unggah laporan hasil inspeksi, permintaan revisi, dan verifikasi laporan beserta notifikasi WhatsApp.

**Detail Perubahan**

**File yang Diubah:**
- app/Enums/PengawasanPerizinanBerusaha/StatusLaporanEnum.php
- app/Http/Controllers/API/V1/PengawasanPerizinanBerusaha/HasilInspeksiLapanganController.php
- app/Http/Controllers/API/V1/PengawasanPerizinanBerusaha/LaporanHasilInspeksiController.php
- app/Http/Library/WaNotifications.php
- app/Http/Requests/PengawasanPerizinanBerusaha/HasilInspeksiLapangan/RequestRevisionRequest.php
- app/Http/Requests/PengawasanPerizinanBerusaha/HasilInspeksiLapangan/UploadLaporanRequest.php
- app/Http/Requests/PengawasanPerizinanBerusaha/HasilInspeksiLapangan/VerifyLaporanRequest.php
- app/Http/Resources/PengawasanPerizinanBerusaha/HasilInspeksiLapangan/HasilInspeksiLapanganResource.php
- app/Http/Resources/PengawasanPerizinanBerusaha/HasilInspeksiLapangan/VerifikasiLaporanResource.php
- app/Jobs/PengawasanPerizinanBerusaha/ProcessSendWaLaporanInspeksi.php

**Perubahan Utama:**
- Unggah laporan, permintaan revisi, dan verifikasi laporan hasil inspeksi.
- Status laporan dan resource verifikasi laporan.
- Job pengiriman notifikasi WhatsApp laporan inspeksi.

**Manfaat:**
- Laporan hasil inspeksi dapat diverifikasi secara berjenjang di dalam sistem.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/67a52ef9b833b8beacb8deb516c2bc850e0e7e64

---

### 4.6 Penambahan kolom STKL pada export hasil inspeksi

**Deskripsi Pekerjaan**
Telah ditambahkan kolom STKL pada export hasil inspeksi.

**Detail Perubahan**

**File yang Diubah:**
- app/Exports/PengawasanPerizinanBerusaha/HasilInspeksi/BahanVerifikasiPengawasanExport.php

**Perubahan Utama:**
- Kolom STKL pada export hasil inspeksi.

**Manfaat:**
- Data STKL ikut terunduh pada export.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/fcad4b7a80efce8861ff45defb25a72fc58ca722
- https://github.com/psdkplabs/api-sip/commit/f625a4cf3e75e77743b109f3a2b6acc7e1167fc5

---

### 4.7 Refactor notifikasi dengan notifiable dan delay

**Deskripsi Pekerjaan**
Telah dilakukan refactor notifikasi PPBBR dan Laporan Kegiatan Usaha menggunakan notifiable dan delay.

**Detail Perubahan**

**File yang Diubah:**
- Modules/AgendaPimpinan/Jobs/NotifikasiAgendaPegawai.php
- Modules/AgendaPimpinan/Jobs/NotifikasiAgendaPimpinan.php
- Modules/Gateway/Jobs/DEPHUB/SinkronKapal.php
- Modules/HaloPSDKP/Jobs/NotifikasiPertanyaanBaruKeAgen.php
- Modules/HaloPSDKP/Jobs/NotifikasiPertanyaanDijawab.php
- Modules/LaporanKegiatanUsaha/Jobs/PelaporanLKU/KonfirmasiPendaftaran.php
- Modules/LaporanKegiatanUsaha/Jobs/PelaporanLKU/NotifikasiKirimLKU.php
- Modules/LaporanKegiatanUsaha/Jobs/PelaporanLKU/NotifikasiKirimVerifikasiLKU.php
- Modules/LaporanKegiatanUsaha/Jobs/PelaporanLKU/OtpPendaftaranPelakuUsaha.php
- Modules/LaporanKegiatanUsaha/Jobs/PelaporanLKU/ReminderPenyampaianLKU.php

**Perubahan Utama:**
- Refactor notifikasi dengan notifiable dan delay.

**Manfaat:**
- Pengiriman notifikasi lebih teratur.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/a0c60f6c3783fdbf3bdd0246b5640fc60ec64fd2

---

## 5. Pemeliharaan Sistem dan Perbaikan Bug

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem melakukan pemeliharaan sistem dan perbaikan bug aplikasi, sebagai berikut:

### 5.1 Perbaikan QueryException pada PerizinanService

**Deskripsi Pekerjaan**
Telah diperbaiki QueryException pada PerizinanService dengan menonaktifkan relasi proyek dan pelaku usaha yang bermasalah.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Transformers/PerizinanOssResource.php

**Perubahan Utama:**
- Penyesuaian relasi proyek dan pelaku usaha.

**Manfaat:**
- Daftar perizinan tidak error.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/ae61e3ff67da9d1e4ea4c579daa137d75da094cf
- https://github.com/psdkplabs/api-sip/commit/4544babc5b04e7e0ac216b5411383d4c9151cc42

---

### 5.2 Refactor rekapitulasi ESLO harian

**Deskripsi Pekerjaan**
Telah dilakukan refactor generate rekapitulasi ESLO harian dan trip kapal yang sebelumnya menimbulkan exception.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Gateway/Http/Controllers/ESLOController.php
- Modules/Gateway/Services/ESLO/RekapitulasiService.php
- app/Jobs/Gateway/ESLO/GenerateRekapitulasiESLOHarian.php

**Perubahan Utama:**
- Refactor rekap ESLO dan trip kapal.

**Manfaat:**
- Rekap harian ESLO tergenerate tanpa error.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/dced73b300b2509359364f822ed9563a7c52d7a8
- https://github.com/psdkplabs/api-sip/commit/3147b912180df0be67a29154ec6781dab5a03158

---

### 5.3 Perbaikan import KoordinatController

**Deskripsi Pekerjaan**
Telah diperbaiki import controller koordinat yang hilang dan typo pada request hapus izin akses.

**Detail Perubahan**

**File yang Diubah:**
- app/Http/Requests/Userman/RBAC/AccessModule/deleteIjinAksesRequest.php
- routes/api.php

**Perubahan Utama:**
- Penggantian KonversiController menjadi KoordinatController.
- Perbaikan typo pada DeleteIjinAksesRequest.

**Manfaat:**
- Endpoint koordinat dapat diakses kembali.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/eaaa10e34d2197ba4ba76a3cfea7f8e2a004398b
- https://github.com/psdkplabs/api-sip/commit/8fc625c9822ee808b95d3b2229d982b4e385e63e

---

### 5.4 Perbaikan WhatsappService

**Deskripsi Pekerjaan**
Telah diperbaiki error explode pada WhatsappService.

**Detail Perubahan**

**File yang Diubah:**
- app/Services/Gateway/WhatsappService.php

**Perubahan Utama:**
- Penanganan TypeError pada explode.

**Manfaat:**
- Notifikasi WhatsApp tidak gagal terkirim.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/60a4ad7a21661da3f257c336340d02a9d4b7b72c
- https://github.com/psdkplabs/api-sip/commit/7b25e887fcbd1257a0c11e59fcc0b2bd805c03d2

---

### 5.5 Perbaikan issue rate limit

**Deskripsi Pekerjaan**
Telah diperbaiki konfigurasi rate limit yang membatasi akses pengguna.

**Detail Perubahan**

**File yang Diubah:**
- app/Providers/RouteServiceProvider.php
- generate_tree.ps1

**Perubahan Utama:**
- Penyesuaian rate limit.

**Manfaat:**
- Pengguna tidak terblokir saat penggunaan normal.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/8392c180612da2b68237bde0b95e7fb2211d2457
- https://github.com/psdkplabs/api-sip/commit/a0d5af12dbfb65eaee76d60e62d0fde93eb12f12

---

### 5.6 Persiapan upgrade Laravel 11 dan dokumentasi API

**Deskripsi Pekerjaan**
Telah dilakukan persiapan upgrade aplikasi ke Laravel 11 berupa perbaikan autoload PSR-4 dan pembaruan dokumentasi API.

**Detail Perubahan**

**File yang Diubah:**
- composer.json
- .env.example
- .gitignore
- Modules/Gateway/Jobs/Kejaksaan/SinkronDataInfoPerkaraPerSatker.php
- Modules/Gateway/Services/MahkamahKonstitusi/MahkamahKonstitusiService.php
- app/Console/Kernel.php
- app/Exceptions/Handler.php
- app/Http/Kernel.php
- app/Services/Gateway/NotificationOtpService.php
- app/Services/Master/PelabuhanService.php

**Perubahan Utama:**
- Perbaikan PSR-4.
- Pembaruan dokumentasi API.

**Manfaat:**
- Aplikasi siap untuk upgrade framework.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/18ee30d943cbb4feaa7bd1cfdf05a0364e5d3504
- https://github.com/psdkplabs/api-sip/commit/5ebf0fcfe4321d0a484e12d7fce2e063f94ae4a9
- https://github.com/psdkplabs/api-sip/commit/001fd54fe82af9733ff8bafb27e6dab1b63c0a67

---

### 5.7 Upgrade aplikasi ke Laravel 11 dan pembaruan dokumentasi

**Deskripsi Pekerjaan**
Telah dilakukan upgrade aplikasi ke Laravel 11 secara bersih dari perubahan branch internal, perbaikan kompatibilitas, serta pembaruan dokumentasi README dan CHANGELOG.

**Detail Perubahan**

**File yang Diubah:**
- Dockerfile
- Modules/DashboardPimpinan/Http/Controllers/KeragaanPSDKPController.php
- Modules/DashboardPimpinan/Routes/api.php
- Modules/DashboardPimpinan/Transformers/KeragaanPSDKP/KeragaanPSDKPResource.php
- Modules/Userman/Entities/Master/DJPT/KapalDJPT.php
- Modules/Userman/Entities/Master/DJPT/KapalDaerahDJPT.php
- Modules/Userman/Imports/DjptKapalDaerahImport.php
- Modules/Userman/Services/Master/DJPTService.php
- app/Console/Kernel.php
- app/Exceptions/Handler.php

**Perubahan Utama:**
- Upgrade ke Laravel 11 dan pemulihan file konfigurasi infrastruktur.
- Perbaikan Guzzle, autoload PSR-4, dan deprecation warning tipe nullable implisit.
- Penyusunan CHANGELOG standar Keep a Changelog dan pembaruan README beserta tautan dokumentasi API.

**Manfaat:**
- Aplikasi kompatibel dengan Laravel 11 dan riwayat perubahan terdokumentasi.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/57f7e72a21e7dc3b9ec66ab27677ae24a40357c6

---

### 5.8 Penonaktifan notifikasi Halo PSDKP

**Deskripsi Pekerjaan**
Telah dinonaktifkan sementara notifikasi Halo PSDKP.

**Detail Perubahan**

**File yang Diubah:**
- app/Console/Kernel.php

**Perubahan Utama:**
- Penonaktifan notifikasi Halo PSDKP.

**Manfaat:**
- Mencegah notifikasi yang tidak diperlukan.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/f537cd33adceda0b79cbe188e29204934d6e1602

---

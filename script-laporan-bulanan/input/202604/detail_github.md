# DETAIL LAPORAN KEGIATAN GITHUB

## 1. Pembaharuan Webservice Modul Master Data

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem memperbaharui webservice Modul Master Data, sebagai berikut:

### 1.1 Memperbaharui webservice korespondensi

**Deskripsi Pekerjaan**
Telah diperbarui webservice korespondensi, meliputi penambahan dokumen surat manual, penonaktifan dokumen surat, penandaan kategori, filter data, serta perbaikan penerima surat yang terduplikasi.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/KorespondensiCSRS/KorespondensiCRSService.php
- Modules/Userman/Http/Controllers/Master/PotalCRS/KorespondensiCRSController.php
- Modules/Userman/Http/Requests/Master/KorespondensiCRS/StoreManualDokumenRequest.php
- routes/modul/master.php
- Modules/Gateway/Jobs/Korespondensi/SimpanDataKorespondensiJob.php
- Modules/Gateway/Http/Controllers/KorespondensiController.php
- Modules/Userman/Database/Migrations/2026_04_10_153000_add_status_to_portal_dokumen_table.php
- Modules/Userman/Database/Migrations/2026_04_10_172800_add_manual_columns_to_portal_dokumen_table.php
- Modules/Userman/Http/Requests/Master/KorespondensiCRS/NonAktifkanSuratRequest.php
- Modules/Userman/Transformers/Master/PORTAL/DetailDokumenSuratResource.php

**Perubahan Utama:**
- Menambahkan input dokumen surat manual dan fitur nonaktifkan dokumen surat.
- Memperbaiki proses tandai dan hapus tandai kategori korespondensi.
- Menambahkan flag type dan penyesuaian filter data korespondensi.
- Memperbaiki pengambilan NIP penerima dan duplikasi penerima surat, serta refactor service korespondensi.

**Manfaat:**
- Surat yang tidak berasal dari sistem dapat dicatat di korespondensi.
- Daftar penerima surat akurat tanpa data ganda.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/888ba436530fd8cb1ffe1fffb8703729bf3a11e6
- https://github.com/psdkplabs/api-sip/commit/5624091a904e6ec52befc0112b741da639544723
- https://github.com/psdkplabs/api-sip/commit/d6a424f9804a62fe1fef0ac1a65d5c6cf2fa063d
- https://github.com/psdkplabs/api-sip/commit/4848b60c7a844445086b19c7471520f4c5bddcba
- https://github.com/psdkplabs/api-sip/commit/7ad7c8fbf69d6c768c2d9175e95364f40b433ecc
- https://github.com/psdkplabs/api-sip/commit/b5e9fb167da9d6db566ecf2262d3f845f221e7d2
- https://github.com/psdkplabs/api-sip/commit/734c571849ab9a35c2b88887def91b2133d80d47

---

### 1.2 Memperbaharui penentuan unit inspeksi berdasarkan koordinat dan GeoJSON

**Deskripsi Pekerjaan**
Telah diperbaiki logika penentuan unit kerja/unit inspeksi objek berdasarkan koordinat dan GeoJSON perizinan, termasuk penanganan data koordinat kosong dan penetapan unit inspeksi pusat.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLLokasiKerjaJob.php
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Userman/Entities/KKPRL/Perizinan.php
- .phpstorm.meta.php
- Modules/Userman/Services/Master/MomiService.php
- Modules/Userman/Tests/Feature/MomiServiceRestorationTest.php
- Modules/Userman/Tests/Feature/PerizinanFilterTest.php
- _ide_helper.php
- _ide_helper_models.php
- app/Http/Requests/Userman/RBAC/Peran/createPeranRequest.php

**Perubahan Utama:**
- Pengisian koordinat dari GeoJSON serta perbaikan job KKPRL dan SSE.
- Objek tanpa unit inspeksi ditandai tidak lengkap, dengan perbaikan filter keterangan unit inspeksi.
- Penentuan unit inspeksi pusat apabila koordinat dan GeoJSON tidak tersedia.
- Objek dengan koordinat dan GeoJSON kosong tidak dimasukkan ke unit tertentu, serta perbaikan data yang terlanjur masuk pusat.
- Filter berdasarkan ketersediaan unit kerja dan status, serta penetapan unit kerja apabila pengecekan GCP gagal.

**Manfaat:**
- Objek pengawasan terdistribusi ke unit kerja yang tepat sesuai lokasinya.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/ebc83d84ae63a0bbe60c811e6b40fa7945a0ea34
- https://github.com/psdkplabs/api-sip/commit/38b5f20e46dfc3576013fd5783752b17005dbb49
- https://github.com/psdkplabs/api-sip/commit/b79680a9bd18c959f1204383c598c950b28c8681
- https://github.com/psdkplabs/api-sip/commit/5fb36952171163cb3b19064ffd793b425403c203
- https://github.com/psdkplabs/api-sip/commit/d06bced8cad3f7035a2bfd44aea5deadcc321e64
- https://github.com/psdkplabs/api-sip/commit/f2026387947d02f86bca8263a0814c15cae612eb
- https://github.com/psdkplabs/api-sip/commit/6b2bf4f3e3c8ac55279887a84dc4268a6b159614
- https://github.com/psdkplabs/api-sip/commit/e97fa55611af51d55ac53cdb811f1c1d804e46e5

---

### 1.3 Memperbaharui webservice MOMI

**Deskripsi Pekerjaan**
Telah diperbarui webservice MOMI, meliputi refactor unggah GeoJSON, filter data, dan penanganan data duplikat.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/MomiService.php
- Modules/Userman/Services/Sync/SyncMasterService.php
- Modules/Userman/Database/Migrations/2026_04_23_164741_standardize_momi_perizinan_uniqueness.php
- Modules/Userman/Jobs/Sync/MOMI/SyncGeoJsonJob.php
- Modules/Userman/Exports/Master/PenetapanSanksiExport.php
- Modules/Userman/Exports/Master/PerizinanMomiExport.php
- Modules/Userman/Http/Controllers/MomiController.php

**Perubahan Utama:**
- Refactor unggah GeoJSON menggunakan firstOrCreate/updateOrCreate.
- Filter MOMI berdasarkan jenis keterangan beserta unit test.
- Perbaikan data MOMI yang terduplikasi.
- Menambahkan filter seluruh data (param all) pada MOMI.

**Manfaat:**
- Unggah ulang GeoJSON tidak lagi menghasilkan data ganda.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/7611f523a3dae3917197948c3732db7231929bf1
- https://github.com/psdkplabs/api-sip/commit/f6844f78916d7a46f8adac1293ce1daf02d5adad
- https://github.com/psdkplabs/api-sip/commit/123bf17e1a44c70e5ce311a82b5adf9111d39e18
- https://github.com/psdkplabs/api-sip/commit/b9fcf81431deef884c635bd82cd602fcabac3cd2

---

### 1.4 Memperbaharui kelengkapan NPWP, NIB, dan sinkronisasi OSS

**Deskripsi Pekerjaan**
Telah ditambahkan input kelengkapan NPWP dan NIB untuk sumber data non-OSS, sinkronisasi data OSS dari NIB manual, serta perbaikan pencarian dan unggah NIB.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Entities/KKPRL/Perizinan.php
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Userman/Services/Sync/SyncMasterService.php
- Modules/Userman/Http/Requests/Master/KKPRL/AddPerizinanRequest.php
- Modules/Userman/Tests/Feature/KKPRLSyncTest.php
- app/Http/Library/StringHelper.php
- app/Providers/MacroServiceProvider.php
- app/Services/IzinAksesUserModulService.php
- app/Services/Master/PelabuhanService.php
- app/Services/Master/PimpinanService.php

**Perubahan Utama:**
- Input NPWP untuk sumber non-OSS dan sinkronisasi NIB/NPWP manual ke data KKPRL berdasarkan subjek hukum.
- Validasi NPWP yang sudah ada namun belum aktif.
- Scheduler sinkronisasi OSS dari database NIB manual dan bulk sync perizinan.
- Penambahan data proyek, perbaikan relasi sinkron NIB, pencarian nama izin, dan unggah NIB.
- Peningkatan parameter khusus pada pencarian master data.

**Manfaat:**
- Data pelaku usaha non-OSS dapat dilengkapi dan terhubung dengan data perizinan.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/5384f9eef47fdbbb979ccb639ef1b1571f99d8c7
- https://github.com/psdkplabs/api-sip/commit/43771a05b72e6be3b76f5e997d7a10e5293eac77
- https://github.com/psdkplabs/api-sip/commit/b51fd63d1e468039fbd749d1c157e4b524cd3583
- https://github.com/psdkplabs/api-sip/commit/24ea763811516da21f8668ec0dec9fa6434dacc0
- https://github.com/psdkplabs/api-sip/commit/485895a1a6d500f9a39fbe866f51650d32791719
- https://github.com/psdkplabs/api-sip/commit/4d51f76c6c23e4db22ad39c9852e1e416d6ec3c5
- https://github.com/psdkplabs/api-sip/commit/6d72ed2b928c055be3bcfc2de507b5ac9f208c0d
- https://github.com/psdkplabs/api-sip/commit/fade5eb3c10d7203b39d62ebdeb536dc4c882bf7
- https://github.com/psdkplabs/api-sip/commit/e78185eb4ed4fa96ac76382cb88deff767c35f61

---

### 1.5 Menyusun filter dan export data Master Data

**Deskripsi Pekerjaan**
Telah diimplementasikan export data master dalam dua kondisi (langsung dan background job) serta penambahan filter dan parameter seluruh data pada berbagai menu master data.

**Detail Perubahan**

**File yang Diubah:**
- Modules/PenangananPelanggaran/Services/PenetapanSanksiService.php
- Modules/Userman/Exports/Master/PenetapanSanksiExport.php
- Modules/Userman/Exports/Master/KKPRLPerizinanExport.php
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Userman/Services/Master/MomiService.php
- Modules/Userman/Tests/Feature/ServiceExportFilterTest.php
- Modules/Userman/Exports/Master/KKRPLLaporanExport.php
- Modules/Userman/Exports/Master/PerizinanMomiExport.php
- Modules/Userman/Services/Master/KKPRL/LaporanTahunanService.php
- Modules/Userman/Exports/Master/KorespondensiExport.php

**Perubahan Utama:**
- Export standar dengan mode langsung atau background job untuk data besar.
- Filter dan export data OSS (perizinan, proyek, pelaku usaha).
- Filter export penetapan sanksi administrasi beserta unit test.
- Parameter all untuk mengambil seluruh data pada korespondensi, laporan tahunan, dan KKPRL.
- Perbaikan definisi response error dan typo parameter perPage.

**Manfaat:**
- Export data besar tidak membebani request karena diproses di background.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/6e76a0b26cd827804d4f4ede4937b9efcc3c4211
- https://github.com/psdkplabs/api-sip/commit/026d26a4fbcd1e1773c1444c583768b6ee8a2421
- https://github.com/psdkplabs/api-sip/commit/a3920d5414fd6887884e286742031ca46d0a2de2
- https://github.com/psdkplabs/api-sip/commit/c04a8a4d8411c06883829ba036e8217c4668b6b3
- https://github.com/psdkplabs/api-sip/commit/ed5a6cc49b6087eb7c862ab001acc62e4538793d
- https://github.com/psdkplabs/api-sip/commit/5fcca04c07149a5bf3a52bc297c90959fd81bf34
- https://github.com/psdkplabs/api-sip/commit/63ffaa10f0c397567cc8cd2326096321c351adb5
- https://github.com/psdkplabs/api-sip/commit/b4e4d3c5d72a16a6bff8b3645b10986343237aae
- https://github.com/psdkplabs/api-sip/commit/4aa633a450db53a69b15b3ce8b3255094a801e7e
- https://github.com/psdkplabs/api-sip/commit/cfb111dbd978cdaf869fef203386003e32715fea
- https://github.com/psdkplabs/api-sip/commit/2ff006c537cf7b9c7d576d4f5a4f197fcbc674a2

---

## 2. Pembaharuan Webservice Modul Asta Data

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem memperbaharui webservice Modul Asta Data (Pemantauan Tidak Langsung), sebagai berikut:

### 2.1 Memperbaharui sinkronisasi data KKPRL

**Deskripsi Pekerjaan**
Telah diperbaiki proses sinkronisasi data perizinan KKPRL, meliputi validasi GeoJSON, titik tengah dan koordinat, nomor penerbitan duplikat, tahun KKPRL, serta sinkronisasi laporan tahunan.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLPerizinanJob.php
- Modules/Userman/Database/Scripts/fix_missing_coordinates.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLSeamapJob.php
- Modules/Userman/Http/Controllers/Master/KKPRL/KKPRLController.php
- Modules/Userman/Services/Master/KKPRL/LaporanTahunanService.php
- routes/modul/master.php
- Modules/Userman/Database/Scripts/data_clean_empty_geojson.php
- Modules/Userman/Database/Scripts/data_clean_issuance_numbers.php
- app/Http/Library/StringHelper.php

**Perubahan Utama:**
- Melewati GeoJSON tidak valid dan membersihkan whitespace nomor penerbitan.
- Perbaikan titik tengah, koordinat kosong, dan nomor KKPRL duplikat.
- Menambahkan tahun KKPRL, daftar tahun, sumber Siloker, dan sektor.
- Penambahan file laporan pada laporan tahunan dan sinkronisasi laporan tahunan per tahun.
- Perbaikan detail perizinan KKPRL dan pemulihan fungsi filter tanggal.

**Manfaat:**
- Data KKPRL tersinkron lengkap dan dapat ditampilkan di peta.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/878eef9ec5b8e22dbf746dd481dd869abc45c298
- https://github.com/psdkplabs/api-sip/commit/45236e9068414a676abf02cfc9963c42352c8782
- https://github.com/psdkplabs/api-sip/commit/4c7e8f2a08d99588698496b8a91b6bab9a913438
- https://github.com/psdkplabs/api-sip/commit/2f315c1c36257ddf304936d37ee7f162cb15ed86
- https://github.com/psdkplabs/api-sip/commit/502ece4b3fed9e52d0fb2a3c89f55ce3b1e825ff
- https://github.com/psdkplabs/api-sip/commit/e63bd2b29ea60ad4abf3a7d9db6ee55894c4b13b
- https://github.com/psdkplabs/api-sip/commit/fd97e4783fe8c3ca536df450499acab7bc4122c4
- https://github.com/psdkplabs/api-sip/commit/fe501bc07d278902357dbc15955bf4e3e1723a31
- https://github.com/psdkplabs/api-sip/commit/900d8407d42db4bee43b20e7a9698558aab3cf72
- https://github.com/psdkplabs/api-sip/commit/a534c331d16d43c85053e356d7667f8ba9e3d5bf

---

### 2.2 Memperbaharui overview dan status laporan Pemantauan Tidak Langsung

**Deskripsi Pekerjaan**
Telah diperbarui webservice Pemantauan Tidak Langsung, meliputi perhitungan overview, status laporan berkala, filter wilayah dan KBLI, serta detail objek.

**Detail Perubahan**

**File yang Diubah:**
- Modules/PengawasanPerizinanBerusaha/Services/SDK/PemantauanService.php
- Modules/PengawasanPerizinanBerusaha/Transformers/SDK/PemantauanDetailResource.php
- Modules/PengawasanPerizinanBerusaha/Transformers/SDK/PemantauanResource.php
- Modules/Userman/Entities/KKPRL/Perizinan.php
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Userman/Database/Migrations/2026_04_21_170300_standardize_jenis_usaha_kkprl.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLPerizinanJob.php
- Modules/Userman/Tests/Feature/PerizinanFilterTest.php
- Modules/Userman/Services/Master/MomiService.php
- getColumnListing('portal_category'))

**Perubahan Utama:**
- Perbaikan bug presedensi SQL pada filter pencarian dan optimasi N+1 query.
- Filter kategori wilayah beserta jumlah per kategori.
- Detail pemantauan tidak langsung berdasarkan ID dan perbaikan jumlah overview.
- Status laporan berkala disesuaikan dengan logika baru, termasuk status belum wajib menyampaikan untuk KKPRL yang baru terbit.
- Penambahan subjek_hukum_count, dokumen laporan tahunan pada detail pengamatan, dan filter KBLI.
- Penyeragaman jenis usaha.

**Manfaat:**
- Angka overview dan status pelaporan pelaku usaha tampil sesuai kondisi sebenarnya.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/376f603201b8c5892d6a431c49b82f7d8c5fc495
- https://github.com/psdkplabs/api-sip/commit/49ced13475c251faae99d0ab2ac1896344bb4b5c
- https://github.com/psdkplabs/api-sip/commit/6ddd9c6491dc447e71cdef2612dd5199f59764c4
- https://github.com/psdkplabs/api-sip/commit/182e09f2cca9680c3e91f0252ccb93c879a706dd
- https://github.com/psdkplabs/api-sip/commit/a225172bd2eec6226dc5a68420089d0e88cfdde6
- https://github.com/psdkplabs/api-sip/commit/c488a15cae8b41de8de9ab16e9d6e2910972fe30
- https://github.com/psdkplabs/api-sip/commit/a1d1c102c032e4a526efef39347a6ac6fe0fd1e8
- https://github.com/psdkplabs/api-sip/commit/a738407137c4452df187d080ff962c5a651c2110
- https://github.com/psdkplabs/api-sip/commit/c014328b744e8025cd14cf47c1c80bd04036f358
- https://github.com/psdkplabs/api-sip/commit/b68f726f434f14dbd4fd83b3d180e1518bde8c27
- https://github.com/psdkplabs/api-sip/commit/9c4e09ab393d63830b69ae3e5bd2a6f9a4f67fa7
- https://github.com/psdkplabs/api-sip/commit/a4501ced24c7f3aa62a69d7a844a0b758e5ff75f
- https://github.com/psdkplabs/api-sip/commit/e74804db668f7ad8358f50444ea4d0ed3e64c28d
- https://github.com/psdkplabs/api-sip/commit/d6b33b9ecf4e3d8372c1048f8d31b842fa7c1faa
- https://github.com/psdkplabs/api-sip/commit/4377af5bb62bb8401aac8482ca31a4f64a548f95
- https://github.com/psdkplabs/api-sip/commit/d48c3bd744d223d719d428411d7141833d94fa22
- https://github.com/psdkplabs/api-sip/commit/905113a98b1336f76302badb9207c48437551418

---

## 3. Memperbaharui Webservice Modul WasRisk

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem memperbaharui webservice Modul WasRisk, sebagai berikut:

### 3.1 Memperbaharui filter data admin dan bentrok role operator pengawas

**Deskripsi Pekerjaan**
Telah diperbaiki penyaringan data WasRisk agar akun admin tidak bentrok dengan role operator dan pengawas pada Berita Acara Pemeriksaan serta laporan dan verifikasi hasil inspeksi.

**Detail Perubahan**

**File yang Diubah:**
- app/Services/PengawasanPerizinanBerusaha/HasilInspeksiLapanganService.php
- app/Services/PengawasanPerizinanBerusaha/InspeksiLapanganService.php
- app/Services/PengawasanPerizinanBerusaha/PenjadwalanService.php
- app/Console/Kernel.php
- app/Enums/PengawasanPerizinanBerusaha/StatusLaporanEnum.php
- app/Http/Controllers/API/V1/PengawasanPerizinanBerusaha/HasilInspeksiLapanganController.php
- app/Http/Controllers/API/V1/PengawasanPerizinanBerusaha/LaporanHasilInspeksiController.php
- app/Http/Library/WaNotifications.php
- app/Http/Requests/PengawasanPerizinanBerusaha/HasilInspeksiLapangan/RequestRevisionRequest.php
- app/Http/Requests/PengawasanPerizinanBerusaha/HasilInspeksiLapangan/UploadLaporanRequest.php

**Perubahan Utama:**
- Filter akun admin pada data WasRisk.
- Penyesuaian route serta laporan dan verifikasi hasil inspeksi.
- Penyelesaian konflik role Operator Pusat/Admin yang juga berperan sebagai Pengawas.

**Manfaat:**
- Data yang tampil sesuai dengan peran pengguna.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/5e2288280fb793c576932a750d9c65f9c5204f7b
- https://github.com/psdkplabs/api-sip/commit/99676075dcf5c2c0d79f45c926d9c029ef91e903
- https://github.com/psdkplabs/api-sip/commit/3761554d6de9faef757db3c5fe63dbf856841fce
- https://github.com/psdkplabs/api-sip/commit/ffd49d81e818813d7258ba568ee944264a43565d

---

### 3.2 Perbaikan unduh PDF hasil inspeksi

**Deskripsi Pekerjaan**
Telah diperbaiki proses unduh dokumen PDF pada menu hasil inspeksi dan inspeksi lapangan WasRisk.

**Detail Perubahan**

**File yang Diubah:**
- app/Exports/PengawasanPerizinanBerusaha/HasilInspeksi/HasilInspeksiExport.php
- app/Exports/PengawasanPerizinanBerusaha/InspeksiLapangan/InspeksiLapanganExport.php
- app/Exports/PengawasanPerizinanBerusaha/Penjadwalan/PenjadwalanExport.php
- app/Services/PengawasanPerizinanBerusaha/HasilInspeksiLapanganService.php
- app/Services/PengawasanPerizinanBerusaha/InspeksiLapanganService.php
- app/Services/PengawasanPerizinanBerusaha/PenjadwalanService.php

**Perubahan Utama:**
- Perbaikan proses unduh PDF pada service hasil inspeksi dan inspeksi lapangan.

**Manfaat:**
- Pengguna dapat mengunduh dokumen hasil inspeksi tanpa kendala.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/3a5883b84446272d51fbe9819e6f2f0d2aa65bea
- https://github.com/psdkplabs/api-sip/commit/3f21bf60598a21a4b20015e99ca7bd2cce00ebcb

---

### 3.3 Stabilisasi notifikasi penjadwalan PPBBR

**Deskripsi Pekerjaan**
Telah dilakukan stabilisasi notifikasi PPBBR, penambahan tool kirim ulang notifikasi manual, serta perbaikan konflik nama job notifikasi unggah laporan.

**Detail Perubahan**

**File yang Diubah:**
- app/Console/Commands/ImportirPreborder/CekPengesahanDokumenPengesahan.php
- app/Console/Commands/PengawasanPerizinanBerusaha/CekJadwalPengawasanTerlewat.php
- app/Console/Commands/PengawasanPerizinanBerusaha/ResendNotification.php
- app/Jobs/PengawasanPerizinanBerusaha/NotifikasiInputPengawas.php
- app/Jobs/PengawasanPerizinanBerusaha/NotifikasiPenjadwalanTerlewat.php
- app/Jobs/PengawasanPerizinanBerusaha/NotifikasiUnggahLaporanWasrisk.php
- app/Services/PengawasanPerizinanBerusaha/PenjadwalanService.php
- database/factories/BeritaAcaraPemeriksaanFactory.php
- database/factories/ObjekPengawasanFactory.php
- app/Services/PengawasanPerizinanBerusaha/LaporanHasilInspeksiService.php

**Perubahan Utama:**
- Stabilisasi notifikasi PPBBR dan perbaikan bug terkait.
- Tool kirim ulang notifikasi dengan opsi --to untuk penerima tertentu.
- Penggantian nama job menjadi NotifikasiUnggahLaporanWasrisk untuk menghindari konflik.

**Manfaat:**
- Notifikasi yang gagal dapat dikirim ulang tanpa mengubah data.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/0a15e38ebbab3d318e8690672b51750bd2c632e3
- https://github.com/psdkplabs/api-sip/commit/7a1568d7712a8688a60e7fdd669e149a9c3751c1

---

### 3.4 Validasi NIB dan Nomor Kode Proyek pada import objek pengawasan

**Deskripsi Pekerjaan**
Telah ditambahkan validasi NIB dan Nomor Kode Proyek terhadap database dan Gateway OSS pada proses import objek pengawasan, serta batas ukuran file import.

**Detail Perubahan**

**File yang Diubah:**
- app/Http/Requests/PengawasanPerizinanBerusaha/ObjekPengawasan/TambahObjekPengawasanRequest.php
- app/Imports/ObjekPengawasanImport.php
- app/Services/PengawasanPerizinanBerusaha/ObjekPengawasanService.php

**Perubahan Utama:**
- Validasi NIB dan Nomor Kode Proyek pada import Excel objek pengawasan.
- Batas ukuran file import Excel maksimal 5MB.

**Manfaat:**
- Mencegah objek pengawasan dengan NIB/kode proyek tidak valid masuk ke sistem.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/5c5a1052629246cd382999fdff0a7f1a04c327d9

---

## 4. Pembaharuan Webservice Modul User Management

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem memperbaharui webservice Modul User Management, sebagai berikut:

### 4.1 Memperbaharui role verifikator LKU dan URL SKP

**Deskripsi Pekerjaan**
Telah diperbaiki role verifikator Laporan Kegiatan Usaha (LKU) dan URL dokumen SKP pegawai.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Transformers/SKPPenerbitanResource.php
- database/seeders/UserManagement/RBAC/SetRoleTypeSeeder.php
- app/Console/Kernel.php

**Perubahan Utama:**
- Perbaikan URL dokumen SKP.
- Penyesuaian role verifikator LKU.

**Manfaat:**
- Verifikator LKU memiliki akses sesuai perannya.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/9032627f0a5663093a2246a3b5182bdeb5eadea6
- https://github.com/psdkplabs/api-sip/commit/47fbdee51153e914c4b10c83d5d78b454a5f3616
- https://github.com/psdkplabs/api-sip/commit/210765545a0ee16cae8566bebf7d53d6f9dc70c5
- https://github.com/psdkplabs/api-sip/commit/cad261cbe0fc24a7ef456a0171e800cfcbbf764f

---

### 4.2 Perbaikan deadlock job permission dan pencarian pegawai

**Deskripsi Pekerjaan**
Telah diperbaiki deadlock pada job pembaruan permission, penyesuaian RBAC, serta pencarian user/pegawai berdasarkan NIP.

**Detail Perubahan**

**File yang Diubah:**
- app/Services/UserService.php
- Modules/Gateway/Jobs/SIMPEG/SinkronDataPortalPegawai.php
- Modules/Gateway/Services/SIMPEG/PegawaiPortalDataService.php
- app/Services/KewenanganModulAccessService.php
- app/Services/PeranModulAccessService.php
- app/Http/Requests/PengawasanPerizinanBerusaha/ObjekPengawasan/TambahObjekPengawasanRequest.php
- app/Imports/ObjekPengawasanImport.php
- app/Services/PengawasanPerizinanBerusaha/ObjekPengawasanService.php
- app/Services/PengawasanPerizinanBerusaha/PenjadwalanService.php

**Perubahan Utama:**
- Perbaikan deadlock job update permission.
- Perbaikan minor RBAC.
- Pencarian user/pegawai berdasarkan NIP melalui Gateway.
- Cherry-pick perbaikan RBAC, validasi import objek pengawasan, dan log lokasi kerja ke branch rilis.

**Manfaat:**
- Pembaruan hak akses berjalan stabil saat diproses bersamaan.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/ec7ed4dd770f5367600c19336120d1870ea3d0d8
- https://github.com/psdkplabs/api-sip/commit/37515c6f4085b1b6ade7eb34cfc020f831c674f1
- https://github.com/psdkplabs/api-sip/commit/282f3abcb358075360fc9598d250bf66f609f614
- https://github.com/psdkplabs/api-sip/commit/8184b1244917b4c028fdd1497e162c8a1fe2155d

---

## 5. Pemeliharaan Sistem dan Infrastruktur

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem melakukan pemeliharaan sistem dan infrastruktur aplikasi, sebagai berikut:

### 5.1 Upgrade aplikasi ke Laravel 11

**Deskripsi Pekerjaan**
Telah dilakukan upgrade framework aplikasi API SIP ke Laravel 11 beserta migrasi exception handler dan penyesuaian FrankenPHP.

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
- Migrasi exception handler ke struktur Laravel 11.
- Penyesuaian konfigurasi FrankenPHP dan token service.

**Manfaat:**
- Aplikasi menggunakan versi framework yang didukung dan lebih aman.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/f472cc9780fd5c932b1cab03bb2feab6b167a2a1
- https://github.com/psdkplabs/api-sip/commit/e438cccf286ddb5c23ca9e276c9a3dca90818ff1
- https://github.com/psdkplabs/api-sip/commit/6e1b2bbd51fd21757e268730223e945de5ed44a3

---

### 5.2 Implementasi Sentry dan perbaikan isu yang dilaporkan

**Deskripsi Pekerjaan**
Telah diimplementasikan Sentry untuk pemantauan error aplikasi beserta perbaikan isu yang dilaporkan, termasuk N+1 query dan konflik macro whereLike.

**Detail Perubahan**

**File yang Diubah:**
- config/sentry.php
- app/Exceptions/Handler.php
- app/Providers/AuthServiceProvider.php
- composer.json
- config/log-viewer.php
- config/logging.php
- app/Providers/MacroServiceProvider.php
- .gitignore
- Modules/Gateway/Jobs/OSS/SinkronFileIzinOssJob.php
- Modules/Gateway/Services/OSS/OSSService.php

**Perubahan Utama:**
- Implementasi Sentry dengan dukungan environment.
- Perbaikan Livewire ComponentNotFoundException.
- Perbaikan N+1 query pada job simpan data OSS dan pengawas perikanan.
- Penyeragaman macro whereLikeAttributes dan penyelesaian konflik whereLike.

**Manfaat:**
- Error aplikasi terpantau secara real-time dan dapat ditindaklanjuti lebih cepat.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/8e98e2851a928db3b6a0d6b6beed7122ffaced02
- https://github.com/psdkplabs/api-sip/commit/ccc36110af1b7b981a8e9a4ad911b9b2c134392f
- https://github.com/psdkplabs/api-sip/commit/40bb38c383f7da8aa59cb23289473cc7bb8bb72c
- https://github.com/psdkplabs/api-sip/commit/ba00b2eb0474414ec4dbd251ff573d0abc79a3be
- https://github.com/psdkplabs/api-sip/commit/b303b4baf80221cad153a370298a11b173305a2b
- https://github.com/psdkplabs/api-sip/commit/b733162d10202fccf67d3bd962b1d4e88f209c5a
- https://github.com/psdkplabs/api-sip/commit/b47fb4884a8fa1c27bad624934f2e0d15ee9743c

---

### 5.3 Hotfix penonaktifan integrasi dan notifikasi

**Deskripsi Pekerjaan**
Telah dilakukan hotfix untuk menonaktifkan sementara integrasi SILAT/SIMKADA melalui flag konfigurasi serta notifikasi Halo PSDKP dan Agenda Pimpinan.

**Detail Perubahan**

**File yang Diubah:**
- app/Http/Resources/Gateway/OSS/ProyekResource.php
- app/Http/Resources/PengawasanPerizinanBerusaha/PencarianPerizinanBerusaha/ProyekResource.php
- .env.example
- config/services.php
- Modules/HaloPSDKP/Services/AdminService.php
- routes/console.php

**Perubahan Utama:**
- Menambahkan konfigurasi GATEWAY_SILAT_SIMKADA_ENABLED beserta test integrasi.
- Menonaktifkan notifikasi Halo PSDKP dan Agenda Pimpinan serta perbaikan linting.

**Manfaat:**
- Integrasi dapat diaktifkan/nonaktifkan tanpa perubahan kode.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/a5cce3918e4ad15050130caf2e951d7f016958c2
- https://github.com/psdkplabs/api-sip/commit/644717fc317dbacbb8c868393ea1960516cadc73
- https://github.com/psdkplabs/api-sip/commit/999c375c57ac25013a98d11afb2804b31fafc8cf
- https://github.com/psdkplabs/api-sip/commit/774970bef52b54aedad51e245e2d0f331dd27890
- https://github.com/psdkplabs/api-sip/commit/3e22370c0071369a62a8cb3318d72385f5d5bbf4

---

### 5.4 Keamanan dependensi dan standarisasi Git workflow

**Deskripsi Pekerjaan**
Telah diselesaikan peringatan kerentanan dependensi npm dari Dependabot serta disusun kebijakan standar Git workflow dan branching.

**Detail Perubahan**

**File yang Diubah:**
- package-lock.json
- package.json
- scripts/gf.ps1

**Perubahan Utama:**
- Pembaruan dependensi npm untuk menutup peringatan kerentanan.
- Dokumentasi Git workflow, strategi branching, dan script otomasi interaktif.

**Manfaat:**
- Mengurangi risiko keamanan dan menyeragamkan alur kerja tim.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/5a61cd24669ef89155e27784cd637cd58a67136c
- https://github.com/psdkplabs/api-sip/commit/258e905cbd5e1322346251c6fc48ce8c1b697f1a
- https://github.com/psdkplabs/api-sip/commit/0524b6d53bbbc5e7009f88ec9ab1d7cd144c1205
- https://github.com/psdkplabs/api-sip/commit/f23496693e8777e1645572e6b95969b13fcf607e

---

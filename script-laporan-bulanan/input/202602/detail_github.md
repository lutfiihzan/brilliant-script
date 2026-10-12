# DETAIL LAPORAN KEGIATAN GITHUB

## 1. Pembaharuan Webservice Modul Master Data - Perizinan KKPRL

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem memperbaharui webservice perizinan KKPRL pada Modul Master Data, sebagai berikut:

### 1.1 Perbaikan sinkronisasi SEAMAP dan progres SSE

**Deskripsi Pekerjaan**
Telah diperbaiki logika sinkronisasi data SEAMAP, penanganan Server-Sent Events (SSE) ketika data kosong, serta reset cache lama saat sinkronisasi dimulai.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLSeamapJob.php
- Modules/Userman/Services/SSE/SseMasterService.php
- Modules/Userman/Library/SyncStateManager.php

**Perubahan Utama:**
- Perbaikan logika sinkronisasi SEAMAP.
- Penanganan SSE ketika tidak ada data.
- Reset cache lama di awal sinkronisasi.

**Manfaat:**
- Progres sinkronisasi tampil akurat dan tidak memakai data usang.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/69bf9907c872dc0e6df5a36d240f885e3c2801ae
- https://github.com/psdkplabs/api-sip/commit/4e9391ec45bc1ff24f7fe4fa7e7004f6e456ca94
- https://github.com/psdkplabs/api-sip/commit/2b5bf53378f4c9a601bfae5425890fd9bf970b4d

---

### 1.2 Refactor resource perizinan dan laporan tahunan KKPRL

**Deskripsi Pekerjaan**
Telah dilakukan refactor resource perizinan KKPRL serta penyusunan data laporan tahunan pada perizinan.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Entities/KKPRL/Perizinan.php
- Modules/Userman/Jobs/Sync/KAPAL/SILAT/SyncSilatApiJob.php
- Modules/Userman/Jobs/Sync/KAPAL/SILAT/SyncSilatKapalJob.php
- Modules/Userman/Jobs/Sync/KAPAL/SILAT/SyncSilatPBUMKUJob.php
- Modules/Userman/Jobs/Sync/KAPAL/SILAT/SyncSilatSiupJob.php
- Modules/Userman/Jobs/Sync/KAPAL/SIMKADA/SyncSimkadaKapalJob.php
- Modules/Userman/Jobs/Sync/KEJAKSAAN/SyncInfoPerkaraKejaksaanJob.php
- Modules/Userman/Jobs/Sync/KEJAKSAAN/SyncSatkerKejaksaanJob.php
- Modules/Userman/Jobs/Sync/KEPEGAWAIAN/SyncSimpegJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLManualJob.php

**Perubahan Utama:**
- Refactor resource perizinan.
- Laporan tahunan pada data perizinan KKPRL.

**Manfaat:**
- Struktur data perizinan lebih rapi dan siap dikembangkan.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/e2098a974e69a48a4ecf48979ebec8b031a748ea

---

### 1.3 Optimasi N+1 query dan riwayat sinkronisasi

**Deskripsi Pekerjaan**
Telah dioptimalkan query data perizinan KKPRL dengan mengatasi masalah N+1 query serta perbaikan format riwayat.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Userman/Transformers/KKPRL/PerizinanDetailResource.php
- Modules/Userman/Transformers/KKPRL/PerizinanResource.php

**Perubahan Utama:**
- Perbaikan N+1 query pada daftar perizinan.
- Perbaikan array riwayat sinkronisasi.

**Manfaat:**
- Daftar perizinan dimuat lebih cepat.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/011459171842e7a07c75266ea8336a64811de5bd
- https://github.com/psdkplabs/api-sip/commit/d34bad59e87a3ccf2b08aab1393999d1c8fa4f1e
- https://github.com/psdkplabs/api-sip/commit/14ade732370f2882b5a0ef9e20f04f913c9de351

---

### 1.4 Penanganan file duplikat pada sinkronisasi

**Deskripsi Pekerjaan**
Telah ditambahkan penanganan file duplikat pada sinkronisasi manual, OSS, SEAMAP, dan perizinan KKPRL.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Userman/Transformers/KKPRL/PerizinanDetailResource.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLManualJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLOSSJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLPerizinanJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLSeamapJob.php

**Perubahan Utama:**
- Penanganan file duplikat pada syncManual, syncOss, syncSeamap, dan syncPerizinan.

**Manfaat:**
- Penyimpanan tidak terisi file ganda.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/fdb33f84be1679fbf84384a59549fd376697d116
- https://github.com/psdkplabs/api-sip/commit/fcb00308515f40d12b3d09e5d0b42e9ac2a518eb

---

### 1.5 Perbaikan simpan GeoJSON dan job status kelengkapan

**Deskripsi Pekerjaan**
Telah diperbaiki kegagalan simpan GeoJSON dan pembaruan status kelengkapan, termasuk pemisahan proses pembaruan kelengkapan ke job tersendiri.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLPerizinanJob.php
- Modules/Userman/Entities/KKPRL/Perizinan.php
- Modules/Userman/Services/Master/KKPRL/KKPRLService.php
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLCompletenessJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLManualJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLOSSJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLSeamapJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLWilayahJob.php
- Modules/Userman/Services/Sync/SyncMasterService.php

**Perubahan Utama:**
- Penanganan gagal simpan GeoJSON dan pembaruan status kelengkapan.
- Job terpisah untuk pembaruan status kelengkapan.
- Menjalankan script Python ketika perizinan sudah ada.

**Manfaat:**
- Status kelengkapan selalu diperbarui walaupun ada data spasial yang gagal disimpan.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/35522187855e50da44ca17c40cb6f1719c2a6820
- https://github.com/psdkplabs/api-sip/commit/ecb3640a906aae2da27d71e08a3447d051db6f87

---

### 1.6 Integrasi API KKPRL dan sinkronisasi OSS berdasarkan nomor penerbitan

**Deskripsi Pekerjaan**
Telah disusun KKPRLService untuk integrasi dengan API KKPRL serta sinkronisasi data OSS berdasarkan nomor penerbitan.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Gateway/Services/PORTALDATA/KKPRLService.php
- Modules/Gateway/Database/Migrations/2026_02_26_200545_modify_column_to_oss_perizinan_proyek_table.php
- Modules/Userman/Entities/KKPRL/Perizinan.php
- Modules/Userman/Http/Requests/Master/KKPRL/AddPerizinanRequest.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLLokasiKerjaJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLOSSDataJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLOSSDokumenJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLPerizinanJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLSeamapJob.php
- Modules/Userman/Library/SyncStateManager.php

**Perubahan Utama:**
- KKPRLService untuk integrasi API KKPRL.
- Sinkronisasi OSS berdasarkan nomor penerbitan dan dari sumber lain.
- Pesan aksi untuk sinkronisasi SEAMAP.

**Manfaat:**
- Data KKPRL dapat diambil langsung dari sumber resmi.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/d21ca55f84978014206f52467bc2724eecbbc144
- https://github.com/psdkplabs/api-sip/commit/6d7472c12eb2c92bcd74f23b401ce6460c2b98b0

---

### 1.7 Validasi unggah koordinat melalui Excel

**Deskripsi Pekerjaan**
Telah diperbaiki validasi koordinat dan template pada unggah data spasial melalui Excel serta proses konversi koordinat.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/Kewilayahan/SpasialService.php
- app/Http/Library/Conversion/GeoJsonHelper.php
- routes/api.php

**Perubahan Utama:**
- Validasi koordinat yang salah pada unggah Excel.
- Perbaikan template unggah.
- Perbaikan konversi koordinat.

**Manfaat:**
- Koordinat yang tidak valid ditolak sebelum tersimpan.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/396af9976160612d517bf38f0db21853922f0c55
- https://github.com/psdkplabs/api-sip/commit/50b0800a5f99ab4629103d012a31735b24b3c6af
- https://github.com/psdkplabs/api-sip/commit/1cfa7352550e812e6e77ed5ffc4b7178409c4b48

---

### 1.8 Unggah multi geometri dan pencarian poligon

**Deskripsi Pekerjaan**
Telah ditambahkan dukungan unggah multi geometri serta pencarian poligon berdasarkan kode WIUP.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/Kewilayahan/SpasialService.php
- Modules/Userman/Transformers/Kewilayahan/Spasial/SpasialDetailResource.php
- Modules/Userman/Services/Master/MomiService.php

**Perubahan Utama:**
- Unggah multi geometri khusus.
- Pencarian poligon berdasarkan kode_wiup.

**Manfaat:**
- Data spasial dengan banyak bentuk dapat diunggah dan dicari.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/d12b1403d27852ef83e77c361a951ea018c640f8
- https://github.com/psdkplabs/api-sip/commit/12941769d93d15d7d9fe11785bfa023e58edccd3

---

### 1.9 Perbaikan riwayat unggah file

**Deskripsi Pekerjaan**
Telah diperbaiki pencatatan riwayat unggah file perizinan yang sebelumnya tidak tersimpan.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php

**Perubahan Utama:**
- Data unggah file tercatat pada riwayat.

**Manfaat:**
- Setiap unggahan dapat ditelusuri.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/da2d5c5242be82b154b30c0373f16ac24ce45f63
- https://github.com/psdkplabs/api-sip/commit/84432373274c7bbe58815e45a3a22133c9785562
- https://github.com/psdkplabs/api-sip/commit/034db14b617a8b70deab64191ce8b6d10b75451a
- https://github.com/psdkplabs/api-sip/commit/510f37364d6f7d85563606e87ba2c9069bb37e9f

---

### 1.10 Aktivasi input manual data spasial

**Deskripsi Pekerjaan**
Telah diaktifkan fungsi input manual pada data spasial utama dan sub-spasial.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/Kewilayahan/WilayahSpasialService.php
- Modules/Userman/Transformers/KKPRL/PerizinanDetailResource.php
- Modules/Userman/Transformers/KKPRL/PerizinanResource.php

**Perubahan Utama:**
- Aktivasi input manual spasial utama dan sub-spasial.
- Konversi keterangan menjadi boolean.

**Manfaat:**
- Operator dapat menginput data spasial secara manual.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/ef7b6dc49e17da226f5424034fb96224c9c824bb

---

### 1.11 Penyempurnaan validasi master spasial

**Deskripsi Pekerjaan**
Telah disempurnakan validasi input master spasial (lanjutan pekerjaan Januari) dan seluruh pekerjaan master spasial digabungkan ke branch utama.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Http/Controllers/Master/Kewilayahan/WilayahSpasialController.php
- Modules/Userman/Http/Requests/Kewilayahan/CreateSpasialRequest.php
- Modules/Userman/Http/Requests/Kewilayahan/UpdateSpasialRequest.php
- Modules/Userman/Http/Requests/Kewilayahan/ActivateSpasialRequest.php

**Perubahan Utama:**
- Validasi jumlah titik berdasarkan bentuk geometri serta validasi format DM dan DMS.
- Penanganan nama spasial yang sudah ada pada step 2 dan format nama spasial.
- Format GeoJSON mentah, status aktivasi, dan resource yang hilang.

**Manfaat:**
- Data spasial yang diinput sesuai dengan bentuk geometrinya.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/a35dac2bd4803fd1272b20a12b5832e7ec610d16

---

### 1.12 Menyusun input kelengkapan NIB, NPWP, dan data usaha

**Deskripsi Pekerjaan**
Telah disusun input kelengkapan data perizinan KKPRL berupa NIB, NPWP, data kegiatan, dan SK IUP, termasuk kelengkapan melalui sinkronisasi OSS.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/MomiService.php
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Userman/Transformers/PerizinanMomiResource.php
- routes/modul/master.php
- Modules/Userman/Http/Requests/Master/MOMI/UpdateMomiRequest.php
- Modules/Userman/Entities/KKPRL/Perizinan.php
- Modules/Userman/Http/Controllers/Master/KKPRL/KKPRLController.php
- Modules/Userman/Http/Requests/Master/MOMI/AddMomiRequest.php
- Modules/Userman/Transformers/KKPRL/PerizinanDetailResource.php
- Modules/Userman/Transformers/KKPRL/PerizinanResource.php

**Perubahan Utama:**
- Input NIB KKPRL dan kelengkapan NPWP.
- Input kelengkapan melalui sinkron OSS dan flag kesesuaian subjek hukum.
- Penambahan data kegiatan dan SK IUP.
- Perbaikan relasi sibling KKPRL dan tampilan NPWP pada detail.

**Manfaat:**
- Data pelaku usaha pada perizinan menjadi lengkap.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/9643efafae8d5415cb631164fa8f078dc4e30cc5
- https://github.com/psdkplabs/api-sip/commit/fa3e1ff21c6616a6c8d9fd2d7e4339dd483e99b3
- https://github.com/psdkplabs/api-sip/commit/4a8a84f016562c91edf2ee9a6f8b7e2639b7a6fc
- https://github.com/psdkplabs/api-sip/commit/418f4fc50e4a7b351bd63abfef24e329d1114620
- https://github.com/psdkplabs/api-sip/commit/2c9b1a5a54f57e41aa04d5e80e750c50ff7a0e39
- https://github.com/psdkplabs/api-sip/commit/d4ef85c36f01d55dbc2db3dcf1c73a6de916ea5a
- https://github.com/psdkplabs/api-sip/commit/91ec104b5af0f0096a535bebabe805cacf5632c0

---

### 1.13 Memperbaharui aksi update dan status kelengkapan perizinan

**Deskripsi Pekerjaan**
Telah dipisahkan aksi update perizinan, ditambahkan flag tombol input data, serta disederhanakan status kelengkapan KKPRL.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Transformers/PerizinanMomiResource.php
- Modules/Userman/Services/Master/MomiService.php
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Userman/Transformers/KKPRL/PerizinanDetailResource.php
- routes/modul/master.php
- Modules/Userman/Http/Requests/Master/MOMI/UpdateMomiRequest.php
- Modules/PengawasanPerizinanBerusaha/Http/Requests/SDK/Pemantauan/PemantauanDownloadRequest.php
- Modules/PengawasanPerizinanBerusaha/Http/Requests/SDK/Pemantauan/PemantauanExportRequest.php
- Modules/PengawasanPerizinanBerusaha/Services/SDK/PemantauanService.php
- Modules/Userman/Database/Seeders/AkunMasterTableSeeder.php

**Perubahan Utama:**
- Pemisahan aksi update perizinan dan status_aksi.
- Flag untuk mengaktifkan tombol input data.
- Status kelengkapan menjadi lengkap dan tidak lengkap.
- Daftar KKPRL dengan nomor yang sama dan penghapusan key related_oss.

**Manfaat:**
- Tombol aksi di frontend sesuai dengan kondisi data.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/fd45ce41e837caf9b3a8ff1ea513d921f46afbd6
- https://github.com/psdkplabs/api-sip/commit/8d4f193046dd5f19d896597d99a297b1324130e4
- https://github.com/psdkplabs/api-sip/commit/93b81677b8fd32c1c212c0403e95cf992ebc78ae
- https://github.com/psdkplabs/api-sip/commit/d7a8c2283e168a2181435830ce585070cf8272e1
- https://github.com/psdkplabs/api-sip/commit/b05f7d9149c50df691c15e22375f856515f47f33
- https://github.com/psdkplabs/api-sip/commit/fce458b8b8776702e2e3006388b380e0efdd6613

---

### 1.14 Menyusun manajemen perizinan KKPRL dengan sumber baru

**Deskripsi Pekerjaan**
Telah disusun manajemen perizinan KKPRL dengan request baru dan atribut sumber data.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Http/Requests/Master/KKPRL/AddPerizinanRequest.php
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Userman/Database/Seeders/AkunMasterTableSeeder.php
- Modules/Userman/Http/Controllers/Master/KKPRL/KKPRLController.php
- routes/modul/master.php
- Modules/Userman/Database/Migrations/2026_02_25_133658_add_column_to_kkprl_perizinan.php
- Modules/Userman/Entities/KKPRL/Perizinan.php
- Modules/Userman/Transformers/KKPRL/PerizinanDetailResource.php

**Perubahan Utama:**
- Request dan service manajemen perizinan KKPRL.
- Atribut source pada perizinan.

**Manfaat:**
- Asal data perizinan dapat dibedakan.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/96e5f6f63a402a7725cb7af23306107ef5368716
- https://github.com/psdkplabs/api-sip/commit/ce3bf4ae1a50ee36e3590d579ff20e01e5242476

---

## 2. Penyusunan Webservice Modul Master Data - MOMI

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem menyusun webservice perizinan MOMI pada Modul Master Data, sebagai berikut:

### 2.1 Menyusun unggah GeoJSON MOMI dan permission

**Deskripsi Pekerjaan**
Telah disusun unggah GeoJSON MOMI, rollback laporan, dan pembaruan permission.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Gateway/Services/PORTALDATA/KKPRLService.php
- Modules/Gateway/Services/SEAMAP/LaporanTahunanService.php
- Modules/PengawasanPerizinanBerusaha/Http/Controllers/SDK/PemantauanController.php
- Modules/PengawasanPerizinanBerusaha/Routes/api.php
- Modules/PengawasanPerizinanBerusaha/Services/SDK/PemantauanService.php
- Modules/PengawasanPerizinanBerusaha/Transformers/SDK/PemantauanResource.php
- Modules/Userman/Database/Migrations/2026_02_09_182405_add_polygon_id_to_momi_perizinan_table.php
- Modules/Userman/Database/Migrations/2026_02_09_220138_add_column_to_momi_polygon_table.php
- Modules/Userman/Database/Seeders/AkunMasterTableSeeder.php
- Modules/Userman/Entities/KKPRL/Perizinan.php

**Perubahan Utama:**
- Refactor unggah GeoJSON MOMI.
- Rollback laporan dan catatan.
- Pembaruan permission dan route sinkronisasi.

**Manfaat:**
- Data spasial MOMI dapat diunggah dengan aman.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/05bed9a42eab8bab21cd4646980e827c0b4fa618
- https://github.com/psdkplabs/api-sip/commit/b024b6f318046c50121ef96a746e54731279c94d

---

### 2.2 Menyusun detail, kelengkapan, dan hapus perizinan MOMI

**Deskripsi Pekerjaan**
Telah disusun detail perizinan MOMI, pelengkapan data, hapus perizinan, serta tampilan relasi data MOMI.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/MomiService.php
- Modules/Userman/Database/Seeders/AkunMasterTableSeeder.php
- Modules/Userman/Http/Controllers/MomiController.php
- routes/modul/master.php
- Modules/Userman/Transformers/PerizinanMomiResource.php
- Modules/Userman/Database/Migrations/2026_02_12_115343_add_nib_npwp_to_momi_perizinan_table.php
- Modules/Userman/Database/Migrations/2026_02_12_121555_add_berkas_iup_to_momi_perizinan_table.php
- Modules/Userman/Database/Migrations/2026_02_12_122957_create_momi_history_file_perizinan.php
- Modules/Userman/Entities/Momi/Perizinan.php
- Modules/Userman/Entities/Momi/RiwayatPerizinan.php

**Perubahan Utama:**
- Detail dan kelengkapan data perizinan MOMI.
- Hapus perizinan MOMI.
- Relasi data MOMI pada detail dan daftar.

**Manfaat:**
- Data perizinan MOMI dapat dikelola dari satu menu.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/22da57d608b7fd9cee6426cca2e841c863fe3665
- https://github.com/psdkplabs/api-sip/commit/5756b1ebfa7abe887a22a3041fe4ace71d15ee54
- https://github.com/psdkplabs/api-sip/commit/22eb579b7cf58a0c136ce4ad92537ebcfdcdc6f8
- https://github.com/psdkplabs/api-sip/commit/f0758f1c5f763e8160ef6a1539e2be4125efbd93

---

### 2.3 Sinkronisasi GeoJSON dan resource perizinan MOMI

**Deskripsi Pekerjaan**
Telah diimplementasikan sinkronisasi GeoJSON perizinan MOMI, service pengelolaan perizinan, dan resource perizinan MOMI.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Transformers/PerizinanMomiResource.php
- Modules/Userman/Database/Migrations/2026_02_23_114555_add_kategori_wilayah_to_momi_perizinan_table.php
- Modules/Userman/Jobs/Sync/MOMI/SyncGeoJsonJob.php
- Modules/Userman/Services/Master/MomiService.php
- app/Http/Resources/Gateway/OSS/V2/PelakuUsahaResource.php
- Modules/Userman/Transformers/KKPRL/PerizinanDetailResource.php
- Modules/Userman/Transformers/KKPRL/PerizinanResource.php

**Perubahan Utama:**
- Sinkronisasi GeoJSON perizinan MOMI.
- Service perizinan MOMI dan PerizinanMomiResource.
- Perubahan key file_shp menjadi file_geojson.

**Manfaat:**
- Format data spasial MOMI seragam dengan data lain.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/5e83c42875e318072fb8a787833b36d4488bff87
- https://github.com/psdkplabs/api-sip/commit/0d0fc5cd02c965ab56106edaa346faf02316aa38
- https://github.com/psdkplabs/api-sip/commit/364a983f5b6af551c48b545c28dd6c3a312d49d8

---

### 2.4 Menyusun konfirmasi kelengkapan MOMI bertahap

**Deskripsi Pekerjaan**
Telah disusun alur pengelolaan perizinan MOMI secara bertahap (multi-step) hingga konfirmasi kelengkapan pada langkah ketiga.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Http/Requests/Master/MOMI/AddMomiRequest.php
- Modules/Userman/Services/Master/MomiService.php
- Modules/Userman/Transformers/PerizinanMomiResource.php
- Modules/Gateway/Services/OSS/V2/PencarianPerizinanBerusahaService.php
- Modules/Userman/Database/Migrations/2026_02_26_072858_add_status_aksi_to_momi_perizinan.php
- app/Http/Resources/Gateway/OSS/V2/PelakuUsahaResource.php
- Modules/Userman/Database/Migrations/2026_02_26_075424_add_nomor_kode_proyek_to_momi_perizinan.php

**Perubahan Utama:**
- AddMomiRequest untuk alur multi-step.
- Konfirmasi kelengkapan MOMI pada step 3.
- Pencarian izin usaha OSS v2 pada alur MOMI.

**Manfaat:**
- Input perizinan MOMI lebih terarah dan minim kesalahan.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/43ba2da876db185bf09e5009b0a5088f5facb6df
- https://github.com/psdkplabs/api-sip/commit/29a78eae52c9a0970385533ba68f9459d26073aa

---

## 3. Pembaharuan Webservice Korespondensi dan Penanganan Pelanggaran

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem memperbaharui webservice korespondensi dan penanganan pelanggaran, sebagai berikut:

### 3.1 Menyusun sinkronisasi korespondensi custom

**Deskripsi Pekerjaan**
Telah disusun service sinkronisasi Portal secara manual, perbaikan SKP, dan filter pencarian dokumen korespondensi.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Gateway/Http/Controllers/KorespondensiController.php
- Modules/Gateway/Http/Requests/PORTAL/GetSPKPRequest.php
- Modules/Gateway/Http/Requests/PORTAL/SyncKorespondensiRequest.php
- Modules/Gateway/Jobs/Korespondensi/SimpanDataKorespondensiManualJob.php
- Modules/Gateway/Jobs/Korespondensi/SimpanDataKorespondensiYesterdayJob.php
- Modules/Gateway/Routes/api.php
- Modules/Gateway/Services/PORTAL/PortalService.php
- Modules/Userman/Jobs/Sync/SyncSKPJob.php
- Modules/Userman/Services/Master/SKPService.php
- Modules/Userman/Transformers/SKPPenerbitanResource.php

**Perubahan Utama:**
- Service sinkron Portal manual.
- Perbaikan SKP dan filter pencarian dokumen.

**Manfaat:**
- Korespondensi dapat disinkronkan sesuai kebutuhan.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/6c80f00d8fafc82fb8a6ed9b00f8fb76069d81fa
- https://github.com/psdkplabs/api-sip/commit/23fe9a1002dfa55c4411a7182511b20a9f0756e8

---

### 3.2 Refactor sinkronisasi korespondensi manual dan terjadwal

**Deskripsi Pekerjaan**
Telah dilakukan refactor sinkronisasi korespondensi manual dengan state management serta sinkronisasi terjadwal.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Gateway/Jobs/Korespondensi/SimpanDataKorespondensiJob.php
- Modules/Gateway/Services/PORTAL/KorespondensiService.php
- Modules/Userman/Jobs/Sync/SyncKorespondensiJob.php
- app/Console/Commands/Gateway/Portal/SinkronDataKorespondensi.php
- config/master.php

**Perubahan Utama:**
- Sinkron manual dengan state management.
- Refactor sinkron terjadwal.

**Manfaat:**
- Status proses sinkronisasi dapat dipantau.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/b3d20dc07a347b761959bd04e75b023c1ec31c79

---

### 3.3 Memperbaharui penandaan kategori korespondensi

**Deskripsi Pekerjaan**
Telah diperbaiki penandaan kategori korespondensi, termasuk penandaan berulang dan validasi penetapan flag type.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/KorespondensiCSRS/KorespondensiCRSService.php
- Modules/Userman/Http/Requests/Master/KorespondensiCRS/giveFlagTypeRequest.php
- Modules/Userman/Transformers/Master/PORTAL/DetailDokumenSuratResource.php
- Modules/Userman/Transformers/Master/PORTAL/DokumenSuratResource.php
- Modules/Gateway/Routes/api.php
- Modules/Userman/Services/Master/KorespondensiCSRS/CategoryService.php

**Perubahan Utama:**
- Penandaan kategori dan perbaikan CategoryService.
- Perbaikan penandaan yang tidak berubah setelah lebih dari 5 kali.
- Validasi request penetapan flag type.

**Manfaat:**
- Kategori surat tersimpan sesuai pilihan pengguna.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/2c1ff6c6459ab3717f20aa0ad0da102ce23478a7
- https://github.com/psdkplabs/api-sip/commit/566580b1d3a40e2e4ba3175bac715655aef7e496
- https://github.com/psdkplabs/api-sip/commit/ec5a09e5df6add020b7a6ddea65fe7688561890f
- https://github.com/psdkplabs/api-sip/commit/6da264b0d38f417611f43fc4736d0ff2c127d2ed
- https://github.com/psdkplabs/api-sip/commit/db0df24be88585a2268e4efae849caa03adf6ffd
- https://github.com/psdkplabs/api-sip/commit/1ac34830afb1c551d6181e975e170ec9b76daaf9

---

### 3.4 Filter dan sorting korespondensi berdasarkan kategori

**Deskripsi Pekerjaan**
Telah diperbaiki filter dan sorting korespondensi berdasarkan kategori serta penambahan field kategori wilayah.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/KorespondensiCSRS/KorespondensiCRSService.php
- Modules/Userman/Transformers/PerizinanMomiResource.php

**Perubahan Utama:**
- Sorting dan filter korespondensi berdasarkan kategori.
- Field kategori_wilayah.

**Manfaat:**
- Surat mudah ditemukan berdasarkan kategorinya.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/6ecb1658feb1ff8bdcf3e77efa6275c0248777a0

---

### 3.5 Menyusun awal webservice penanganan pelanggaran

**Deskripsi Pekerjaan**
Telah disusun tahap awal webservice penanganan pelanggaran beserta overview dan penandaan kategori.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/KorespondensiCSRS/PenangananPelanggaranService.php
- Modules/Userman/Transformers/Master/PORTAL/DetailDokumenSuratResource.php
- Modules/Userman/Transformers/Master/PORTAL/DokumenSuratResource.php
- Modules/Userman/Transformers/Master/PORTAL/PenangananPelanggaranResource.php
- Modules/Gateway/Database/Migrations/2026_02_15_183737_add_flag_type_to_portal_dokumen_table.php
- Modules/Gateway/Entities/PortalDokumen.php
- Modules/Gateway/Http/Controllers/KorespondensiController.php
- Modules/PengawasanPerizinanBerusaha/Exports/SDK/PemantauanExport.php
- Modules/PengawasanPerizinanBerusaha/Http/Controllers/SDK/PemantauanController.php
- Modules/PengawasanPerizinanBerusaha/Http/Requests/SDK/Pemantauan/PemantauanExportRequest.php

**Perubahan Utama:**
- Struktur awal penanganan pelanggaran dan overview.
- Penandaan kategori pada penanganan pelanggaran.

**Manfaat:**
- Menjadi dasar pengembangan modul penanganan pelanggaran.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/e7f924e0f6cb1129fb3f65248ad4910d9caec22f
- https://github.com/psdkplabs/api-sip/commit/741247d08943ae0668a6a0b6b80a2255927d973a

---

## 4. Pembaharuan Webservice Modul Asta Data

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem memperbaharui webservice Modul Asta Data (Pemantauan Tidak Langsung), sebagai berikut:

### 4.1 Memperbaharui resource laporan berkala dan provinsi

**Deskripsi Pekerjaan**
Telah diperbarui resource laporan berkala (diambil 5 tahun terakhir), resource provinsi, serta penanda pemeriksaan Polsus pada pemantauan.

**Detail Perubahan**

**File yang Diubah:**
- Modules/PengawasanPerizinanBerusaha/Transformers/SDK/PemantauanResource.php
- Modules/PengawasanPerizinanBerusaha/Services/SDK/PemantauanService.php
- Modules/Userman/Entities/KKPRL/Perizinan.php
- config/master.php

**Perubahan Utama:**
- Resource laporan berkala 5 tahun terakhir.
- Resource provinsi dan informasi tambahan KKPRL.
- Flag has_check polsus pada resource pemantauan.

**Manfaat:**
- Riwayat pelaporan pelaku usaha tampil ringkas.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/b97f72e3a321d4c2a0d68b03084c879b3a8e3515
- https://github.com/psdkplabs/api-sip/commit/4dc4a5cadf70c1bc8b6b80003cde7364baaa7dce
- https://github.com/psdkplabs/api-sip/commit/f35f9eb35d48c076cebb5efb2bc54a54462f449d
- https://github.com/psdkplabs/api-sip/commit/44b265dbc46630b761510bbd43cfb4f1da25fb38
- https://github.com/psdkplabs/api-sip/commit/f10a54be44bab25a3c2b4fb5932c4c3d0a6fface
- https://github.com/psdkplabs/api-sip/commit/2ae194f6b74ca9b7cbc09dc2ee1ad7ad49bd458e
- https://github.com/psdkplabs/api-sip/commit/e5aaa8433e14dfff03189094c5b440e2e1d1e752

---

### 4.2 Memperbaharui detail pemantauan tidak langsung

**Deskripsi Pekerjaan**
Telah dilengkapi detail pemantauan tidak langsung dengan lokasi kerja, penanggung jawab, operator, MOMI, file KKPRL, unit inspeksi, aplikasi SEA, dan riwayat inspeksi.

**Detail Perubahan**

**File yang Diubah:**
- Modules/PengawasanPerizinanBerusaha/Transformers/SDK/PemantauanDetailResource.php
- Modules/PengawasanPerizinanBerusaha/Services/SDK/PemantauanService.php
- Modules/PengawasanPerizinanBerusaha/Http/Controllers/SDK/PemantauanController.php
- Modules/PengawasanPerizinanBerusaha/Routes/api.php
- Modules/PengawasanPerizinanBerusaha/Transformers/SDK/PemantauanResource.php
- Modules/Userman/Entities/KKPRL/Perizinan.php

**Perubahan Utama:**
- Lokasi kerja dan detail pemantauan.
- Resource penanggung jawab, operator, dan MOMI.
- File KKPRL dan unit inspeksi pada detail.
- Resource app_sea, riwayat inspeksi, dan PemantauanService.

**Manfaat:**
- Seluruh informasi objek pemantauan tampil dalam satu halaman.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/0c3530d3d8d0664d6cc8b7b0c6220f107af26d28
- https://github.com/psdkplabs/api-sip/commit/867d21f78ae112cb05d64fcfbaf455b64bbd3e23
- https://github.com/psdkplabs/api-sip/commit/47fd5b06500fc54c8e4797fa79e7840046974040
- https://github.com/psdkplabs/api-sip/commit/9321ab6d00272ec7d32e29478ee9a8e9a299e666
- https://github.com/psdkplabs/api-sip/commit/3e3e4d8e1ec6acb487f5f2a75e599902cfe27324
- https://github.com/psdkplabs/api-sip/commit/0328b7877fa3d3e053d84c9811ea5d8a2b5caef2
- https://github.com/psdkplabs/api-sip/commit/a999824829e3c9dc6ef94fe7f7611cbfcbe23225
- https://github.com/psdkplabs/api-sip/commit/81015d2c18e163a075787f8a3640fa4f2b84f27b

---

### 4.3 Perbaikan data detail pemantauan

**Deskripsi Pekerjaan**
Telah diperbaiki logika status NIB, URL file, data OSS kosong, serta laporan yang tidak muncul pada pemantauan.

**Detail Perubahan**

**File yang Diubah:**
- Modules/PengawasanPerizinanBerusaha/Transformers/SDK/PemantauanDetailResource.php
- Modules/PengawasanPerizinanBerusaha/Services/SDK/PemantauanService.php
- Modules/PengawasanPerizinanBerusaha/Transformers/SDK/PemantauanResource.php

**Perubahan Utama:**
- Perbaikan logika status NIB.
- Perbaikan URL file dan data OSS null.
- Perbaikan laporan yang tidak muncul.

**Manfaat:**
- Data pemantauan tampil tanpa error.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/688f438ab07e693a753f1ebc94aba4bb9328651c
- https://github.com/psdkplabs/api-sip/commit/dbd902afb3f452793f1f1783456806a506cb4324
- https://github.com/psdkplabs/api-sip/commit/73449f3810b2395ba0c300321a0bab837d073e67
- https://github.com/psdkplabs/api-sip/commit/d424a411f3e8578fd6666822b343a15422d3f5b6
- https://github.com/psdkplabs/api-sip/commit/c017bd90a5213922b757a767e0fb2328f34247b6

---

### 4.4 Filter pemantauan berdasarkan periode, lokasi, dan unit kerja

**Deskripsi Pekerjaan**
Telah ditambahkan filter periode, lokasi kerja, dan unit kerja pada pemantauan tidak langsung.

**Detail Perubahan**

**File yang Diubah:**
- Modules/PengawasanPerizinanBerusaha/Services/SDK/PemantauanService.php
- Modules/PengawasanPerizinanBerusaha/Transformers/SDK/PemantauanDetailResource.php
- Modules/PengawasanPerizinanBerusaha/Transformers/SDK/PemantauanResource.php

**Perubahan Utama:**
- Filter periode.
- Filter lokasi kerja.
- Filter unit kerja.

**Manfaat:**
- Pengguna dapat menyaring objek sesuai wilayah kerjanya.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/776b1c4b9b1a317a0a7b309b3b81b68cf6100b35
- https://github.com/psdkplabs/api-sip/commit/d8d5b2311c309694aa912828b55927658c2de4cc
- https://github.com/psdkplabs/api-sip/commit/29826c0975158d688ef5fb1c4f0279bcd065a822
- https://github.com/psdkplabs/api-sip/commit/a4f1bd595111ca9cb12e17e7a3d039d8434c6357
- https://github.com/psdkplabs/api-sip/commit/485d9a3efaaf9179d272c0784ec21820f56997b0

---

### 4.5 Filter status laporan dan perbaikan overview

**Deskripsi Pekerjaan**
Telah ditambahkan filter status laporan serta diperbaiki jumlah overview, sorting default, dan relasi OSS.

**Detail Perubahan**

**File yang Diubah:**
- Modules/PengawasanPerizinanBerusaha/Services/SDK/PemantauanService.php
- Modules/PengawasanPerizinanBerusaha/Http/Controllers/SDK/PemantauanController.php
- Modules/PengawasanPerizinanBerusaha/Routes/api.php
- Modules/PengawasanPerizinanBerusaha/Transformers/SDK/PemantauanDetailResource.php

**Perubahan Utama:**
- Filter status laporan.
- Perbaikan jumlah overview dan tabel data.
- Sorting default berdasarkan tanggal penerbitan dan relasi OSS berdasarkan nomor penerbitan.

**Manfaat:**
- Angka overview sesuai dengan data tabel.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/5e76a91ad213f7a4695c4db1f14e1c4193f2dc7b
- https://github.com/psdkplabs/api-sip/commit/152c86d2122d033d44815bf5f27e3a49f5201c75
- https://github.com/psdkplabs/api-sip/commit/3dcf2c846be4881daa692ce86cfd501a14daabc4
- https://github.com/psdkplabs/api-sip/commit/27a68d983cb0d943a39c08b8ca61d1155617665c

---

### 4.6 Menyusun fitur unduh file KKPRL

**Deskripsi Pekerjaan**
Telah disusun fitur unduh file dokumen KKPRL pada pemantauan tidak langsung.

**Detail Perubahan**

**File yang Diubah:**
- Modules/PengawasanPerizinanBerusaha/Http/Requests/SDK/Pemantauan/PemantauanDownloadRequest.php
- Modules/PengawasanPerizinanBerusaha/Jobs/SDK/DownloadKkprlFileJob.php
- Modules/PengawasanPerizinanBerusaha/Services/SDK/PemantauanService.php

**Perubahan Utama:**
- Endpoint unduh file KKPRL beserta perbaikannya.

**Manfaat:**
- Dokumen KKPRL dapat diunduh langsung dari aplikasi.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/cb8df0ac536b3679ad7931782ae639075ef9c03c
- https://github.com/psdkplabs/api-sip/commit/05d29039cca8f1e1a99bdf9091ad73f116832c92

---

## 5. Memperbaharui Webservice Integrasi OSS

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem memperbaharui webservice integrasi OSS, sebagai berikut:

### 5.1 Refactor service OSS dan penyusunan OSS v2

**Deskripsi Pekerjaan**
Telah dilakukan refactor service OSS dan penyusunan pencarian OSS versi 2.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Gateway/Http/Controllers/OSS/PencarianPerizinanBerusahaController.php
- Modules/Gateway/Http/Controllers/PencarianPerizinanBerusahaController.php
- Modules/Gateway/Http/Requests/OSS/PencarianPerizinanBerusahaRequest.php
- Modules/Gateway/Routes/api.php
- Modules/Gateway/Services/OSS/PencarianPerizinanBerusahaService.php
- Modules/Gateway/Services/OSS/V2/PencarianPerizinanBerusahaService.php
- Modules/LaporanKegiatanUsaha/Http/Controllers/AuthLkuController.php
- Modules/LaporanKegiatanUsaha/Services/AuthLkuService.php
- Modules/LaporanKegiatanUsaha/Services/PelaporanService.php
- Modules/Userman/Http/Controllers/OSSController.php

**Perubahan Utama:**
- Refactor service OSS.
- Pencarian OSS v2.

**Manfaat:**
- Integrasi OSS lebih terstruktur.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/18bbd685250aec5ab5d9db31ffb2eb28bad94e07

---

### 5.2 Pencarian OSS langsung ke database

**Deskripsi Pekerjaan**
Telah disusun pencarian data OSS langsung ke database, relasi KKPRL ke pelaku usaha, serta pencarian berdasarkan nama perseroan.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Gateway/Services/OSS/V2/PencarianPerizinanBerusahaService.php
- Modules/Gateway/Http/Controllers/OSS/PencarianPerizinanBerusahaController.php
- Modules/Gateway/Http/Requests/OSS/PencarianPerizinanBerusahaRequest.php
- Modules/Gateway/Routes/api.php
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php
- Modules/Userman/Transformers/KKPRL/PerizinanDetailResource.php
- Modules/Userman/Transformers/KKPRL/PerizinanResource.php
- app/Http/Resources/Gateway/OSS/V2/OperatorResource.php
- app/Http/Resources/Gateway/OSS/V2/PelakuUsahaResource.php
- app/Http/Resources/Gateway/OSS/V2/PenanggungJawabResource.php

**Perubahan Utama:**
- Pencarian OSS direct database.
- Relasi KKPRL ke pelaku usaha.
- Pencarian OSS berdasarkan nama perseroan.

**Manfaat:**
- Pencarian lebih cepat tanpa bergantung pada API eksternal.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/93273a34710b6e37668cea57020386ebfa49789c
- https://github.com/psdkplabs/api-sip/commit/6eaeffe46790912549fa7438473a9239b8d642a1

---

### 5.3 Perbaikan sinkronisasi proyek OSS dan pencarian NIB

**Deskripsi Pekerjaan**
Telah diperbaiki sinkronisasi proyek OSS, validasi format NIB 13 digit, serta pencarian NIB secara langsung.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Gateway/Services/OSS/PencarianPerizinanBerusahaService.php
- Modules/Gateway/Services/OSS/V2/PencarianPerizinanBerusahaService.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLPerizinanJob.php
- Modules/Userman/Services/Sync/SyncMasterService.php
- app/Http/Library/StringHelper.php
- app/Imports/Gateway/OSS/DataNIBImport.php
- app/Jobs/Gateway/OSS/SimpanDataOSS.php
- app/Jobs/Gateway/OSS/SimpanDataProyek.php
- app/Services/WilayahAdministratifService.php
- Modules/Gateway/Http/Controllers/OSS/PencarianPerizinanBerusahaController.php

**Perubahan Utama:**
- Sinkronisasi proyek OSS.
- Validasi NIB 13 digit.
- PencarianPerizinanBerusahaService dan parameter pencarian NIB langsung.

**Manfaat:**
- Data proyek dan NIB tersinkron dengan format yang benar.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/9e1b83220d3b20ec2cca1d05b33974bf8171b06f
- https://github.com/psdkplabs/api-sip/commit/f90e4153689864baf8e57c5b254ea87798fb7b36

---

## 6. Pemeliharaan Sistem dan Perbaikan Bug

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem melakukan pemeliharaan sistem dan perbaikan bug, sebagai berikut:

### 6.1 Perbaikan middleware Gateway dan status SIMKADA

**Deskripsi Pekerjaan**
Telah ditambahkan middleware yang belum terpasang pada route Gateway serta diperbaiki kolom status SIMKADA.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Gateway/Http/Controllers/ELogbookController.php
- Modules/Gateway/Http/Controllers/ESLOController.php
- Modules/Gateway/Http/Controllers/ESLOPermohonanController.php
- Modules/Gateway/Http/Controllers/KejaksaanController.php
- Modules/Gateway/Http/Controllers/KorespondensiController.php
- Modules/Gateway/Http/Controllers/MahkamahKonstitusiController.php
- .gitignore
- Modules/Gateway/Jobs/SIMKADA/SimpanDataPerizinanBerusahaKapal.php
- routes/api.php

**Perubahan Utama:**
- Middleware pada route Gateway.
- Perbaikan kolom status SIMKADA.

**Manfaat:**
- Endpoint Gateway terlindungi.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/f8c2d08ed16355a2d535b2afcb7b739b259abed9
- https://github.com/psdkplabs/api-sip/commit/5a48b6815c12a1a2a81724070dfddd76f158b1e4
- https://github.com/psdkplabs/api-sip/commit/9f8d6a8f0171430207aae193d5b040e9db8de088

---

### 6.2 Penyamaran data kontak

**Deskripsi Pekerjaan**
Telah diterapkan penyamaran (asterisk) pada data kontak yang ditampilkan.

**Detail Perubahan**

**File yang Diubah:**
- app/Http/Resources/Auth/UserResource.php

**Perubahan Utama:**
- Penyamaran data kontak dengan tanda bintang.

**Manfaat:**
- Data pribadi tidak tampil utuh.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/865e3b398957c33339e31fa0d124c28d1f2c91e3
- https://github.com/psdkplabs/api-sip/commit/582f6ad201f2e81413ea9b6166589c51b8aca92c

---

### 6.3 Persiapan upgrade framework ke Laravel 11

**Deskripsi Pekerjaan**
Telah dimulai persiapan upgrade framework aplikasi ke Laravel 11, meliputi pembaruan paket, middleware, schedule, dan exception handler.

**Detail Perubahan**

**File yang Diubah:**
- .gitignore
- Modules/Gateway/Services/MahkamahKonstitusi/MahkamahKonstitusiService.php
- app/Console/Kernel.php
- app/Exceptions/Handler.php
- app/Http/Kernel.php
- app/Services/Gateway/NotificationOtpService.php
- bootstrap/app.php
- composer.json
- composer_backup.json
- routes/console.php

**Perubahan Utama:**
- Pembaruan framework dan paket composer.
- Migrasi middleware, schedule, dan exception handler ke struktur baru.
- Perbaikan strict typing Carbon pada NotificationOtpService dan penanganan error WAF Cloudflare.

**Manfaat:**
- Menjadi dasar proses upgrade aplikasi ke versi framework yang didukung.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/1ef92b1b489a92583bd4b16e3ca8c7e5ae55d7e2

---

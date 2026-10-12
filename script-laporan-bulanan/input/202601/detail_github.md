# DETAIL LAPORAN KEGIATAN GITHUB

## 1. Pembaharuan Webservice Modul Master Data - Sinkronisasi KKPRL

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem memperbaharui webservice sinkronisasi perizinan KKPRL pada Modul Master Data, sebagai berikut:

### 1.1 Implementasi sinkronisasi KKPRL berantai multi sumber

**Deskripsi Pekerjaan**
Telah diimplementasikan sinkronisasi data perizinan KKPRL secara berantai dari berbagai sumber (Portal, ESEAMAP, OSS, Plus Code, dan input manual) dalam satu alur proses, termasuk penyimpanan data GeoJSON hasil sinkronisasi.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Http/Requests/Master/SyncMasterRequest.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLFinishJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLLokasiKerjaJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLOSSJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLPerizinanJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLReportJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLSeamapJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLWilayahJob.php
- Modules/Userman/Jobs/Sync/SyncKkprlLokasiKerjaJob.php
- Modules/Userman/Jobs/Sync/SyncKkprlPerizinanJob.php

**Perubahan Utama:**
- Alur sinkronisasi berantai seluruh sumber KKPRL.
- Script ESEAMAP untuk pengambilan data KKPRL.
- Perbaikan script SKP.

**Manfaat:**
- Seluruh data KKPRL dapat disinkronkan dalam satu proses.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/7ba30637b87b07dfd3e550953f6751f70de2321c

---

### 1.2 Memperbaharui job sinkronisasi dan laporan progres

**Deskripsi Pekerjaan**
Telah diperbarui job sinkronisasi KKPRL agar setiap tahap mengirimkan event progres dan tetap tercatat ketika salah satu tahap gagal.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Sync/SyncMasterService.php
- Modules/Userman/Library/SyncStateManager.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLOSSJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLWilayahJob.php
- Modules/Userman/Services/SSE/SseMasterService.php

**Perubahan Utama:**
- Pembaruan job sinkronisasi dan perbaikan class job.
- Pengiriman event progres untuk 5 tahap job.
- Penanganan progres tahap yang gagal.

**Manfaat:**
- Proses sinkronisasi dapat dipantau secara realtime oleh pengguna.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/ab9c7da5bc8111933e5725f0fbbbf095b2361654
- https://github.com/psdkplabs/api-sip/commit/5db18017c14da6dde20571d97995041ca803d864
- https://github.com/psdkplabs/api-sip/commit/63bb012d1a849e56ac23811f7a8c927e379303e9
- https://github.com/psdkplabs/api-sip/commit/6f5d51a34bd67da1aab4a593dc180ba3852983c5

---

### 1.3 Memperbaharui sumber data Plus Code, manual, dan ESEAMAP

**Deskripsi Pekerjaan**
Telah diperbaiki pengambilan data dari sumber Plus Code, input manual, dan ESEAMAP pada sinkronisasi KKPRL.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLWilayahJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLSeamapJob.php
- .gitignore
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLLokasiKerjaJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLOSSJob.php
- Modules/Userman/Library/SyncStateManager.php

**Perubahan Utama:**
- Perbaikan sumber Plus Code dan input manual.
- Penyesuaian sinkronisasi hingga tahap ESEAMAP.
- Perbaikan typo wilayah menjadi manual dan pembaruan gitignore.

**Manfaat:**
- Data dari setiap sumber tersimpan dengan label sumber yang benar.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/4fcc127dd7dc1c483c931f9ccbb7014fb6f5e488
- https://github.com/psdkplabs/api-sip/commit/b354607f345136b24ea37b1f473c310191ab791b
- https://github.com/psdkplabs/api-sip/commit/be9e5fd1134395d13653fb2e6912814850efc55c
- https://github.com/psdkplabs/api-sip/commit/2605d81671664d3c92a605b1a22a2a1471b4d69b

---

### 1.4 Penyesuaian label tahapan sinkronisasi

**Deskripsi Pekerjaan**
Telah disesuaikan label tahapan sinkronisasi KKPRL yang ditampilkan kepada pengguna.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Library/SyncStateManager.php

**Perubahan Utama:**
- Perbaikan label tahapan sinkronisasi.

**Manfaat:**
- Pengguna memahami tahap sinkronisasi yang sedang berjalan.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/1722d448803b678c9eb16dfa764ca604d3e6b381

---

### 1.5 Menyusun status kelengkapan dokumen, GeoJSON, dan koordinat

**Deskripsi Pekerjaan**
Telah disusun pengecekan status kelengkapan data perizinan KKPRL (dokumen, GeoJSON, dan koordinat) pada setiap sumber sinkronisasi menggunakan state manager dinamis.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Transformers/PerizinanKkprlResource.php
- .gitignore
- Modules/Userman/Database/Migrations/2026_01_14_122205_add_column_to_kkprl_perizinan_table.php
- Modules/Userman/Entities/PerizinanKkprl.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLOSSJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLPerizinanJob.php
- Modules/Userman/Jobs/Sync/KKPRL/SyncKKPRLSeamapJob.php
- Modules/Userman/Library/SyncStateManager.php
- Modules/Userman/Providers/UsermanServiceProvider.php
- Modules/Userman/Services/Master/KKPRLService.php

**Perubahan Utama:**
- Penambahan kolom status_kelengkapan.
- Pengecekan kelengkapan pada data ESEAMAP, OSS, dan perizinan.
- State manager dinamis untuk status kelengkapan.

**Manfaat:**
- Data perizinan yang belum lengkap teridentifikasi otomatis.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/cb251d251debade07548721897a8594ff5ad4db0
- https://github.com/psdkplabs/api-sip/commit/d030e423783f3f4646e4c001580dc08d47038f4a

---

### 1.6 Perbaikan resource dan status kelengkapan

**Deskripsi Pekerjaan**
Telah diperbaiki resource perizinan KKPRL serta penanganan status kelengkapan yang bernilai null.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Transformers/PerizinanKkprlResource.php
- Modules/Userman/Entities/PerizinanKkprl.php

**Perubahan Utama:**
- Perbaikan resource perizinan.
- Penanganan status null dan penghapusan keterangan tidak ada koordinat.

**Manfaat:**
- Status kelengkapan tampil konsisten.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/3e7d443b8005c709ebd4822225677ba7fde775dc
- https://github.com/psdkplabs/api-sip/commit/6fb286b61f8fb4454ae41ed696fb89362f041cf3

---

### 1.7 Menyusun sinkronisasi manual interaktif dan daftar perizinan tidak lengkap

**Deskripsi Pekerjaan**
Telah disusun sinkronisasi manual interaktif, unggah manual dengan validasi unggah ulang, serta daftar perizinan yang belum lengkap.

**Detail Perubahan**

**File yang Diubah:**
- Modules/PengawasanPerizinanBerusaha/Entities/SDK/Penjadwalan.php
- Modules/PengawasanPerizinanBerusaha/Services/SDK/HasilInpeksiService.php
- Modules/PengawasanPerizinanBerusaha/Services/SDK/InspeksiService.php
- Modules/PengawasanPerizinanBerusaha/Services/SDK/PenjadwalanService.php
- Modules/Userman/Database/Migrations/2026_01_18_154059_create_kkprl_file_history_table.php
- Modules/Userman/Database/Migrations/2026_01_18_170003_add_status_to_file_perizinan_table.php
- Modules/Userman/Database/Seeders/KKPRL/InjectGeojsonFileSeeder.php
- Modules/Userman/Database/Seeders/KKPRL/UpdateLatlongPerizinanTableSeeder.php
- Modules/Userman/Entities/FilePerizinanKkprl.php
- Modules/Userman/Entities/KKPRL/FilePerizinan.php

**Perubahan Utama:**
- Sinkronisasi manual interaktif dengan pembaruan status kelengkapan.
- Validasi unggah ulang dokumen.
- Endpoint daftar perizinan yang belum lengkap.

**Manfaat:**
- Operator dapat melengkapi data tanpa menunggu sinkronisasi terjadwal.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/e307e9513621b172af2403bdd3ef952e9348205e

---

### 1.8 Menyusun unggah banyak file PDF

**Deskripsi Pekerjaan**
Telah ditambahkan dukungan unggah banyak file sekaligus untuk dokumen bertipe PDF.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php

**Perubahan Utama:**
- Unggah multiple file untuk tipe PDF.

**Manfaat:**
- Dokumen pendukung dapat diunggah sekaligus.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/5b748e2910cab461e1bdc827247f0a1a92509b32

---

### 1.9 Penyederhanaan resource dan sorting daftar perizinan

**Deskripsi Pekerjaan**
Telah disederhanakan resource daftar utama perizinan KKPRL, sorting kolom, serta ditambahkan informasi jenis usaha.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Transformers/KKPRL/PerizinanDetailResource.php
- Modules/Userman/Transformers/KKPRL/PerizinanResource.php
- Modules/Userman/Services/Master/KKPRL/PerizinanService.php

**Perubahan Utama:**
- Pemisahan detail dari resource utama dan pembaruan resource detail.
- Penyederhanaan sorting kolom daftar utama.
- Penambahan jenis usaha pada resource utama.

**Manfaat:**
- Daftar perizinan dimuat lebih cepat dan informatif.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/455bdc5bcfb7bb68308a59ef3054878de229d0e1
- https://github.com/psdkplabs/api-sip/commit/0e261e2e791bea9f5c88ad79c313762435eda2f9
- https://github.com/psdkplabs/api-sip/commit/ca816c89f1e2186227e8dede42683b2c6edac7cf
- https://github.com/psdkplabs/api-sip/commit/d5d0b5e148171397ab206eb4783ed430fac7a812

---

## 2. Penyusunan Webservice Modul Master Data - Master Spasial

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem menyusun webservice master spasial pada Modul Master Data, sebagai berikut:

### 2.1 Menyusun input koordinat dinamis (DD/DMS/DM)

**Deskripsi Pekerjaan**
Telah disusun webservice master spasial dengan input koordinat dinamis dalam format DD, DMS, dan DM beserta validasinya, serta penyimpanan data spasial dari PDF.

**Detail Perubahan**

**File yang Diubah:**
- Modules/SadarGakum/Services/KategoriPeraturanService.php
- Modules/SadarGakum/Transformers/KategoriPeraturanResource.php
- Modules/Userman/Database/Migrations/2025_07_29_173524_create_mst_kategori_spasial_table.php
- Modules/Userman/Database/Migrations/2025_07_29_173638_create_mst_spasial_table.php
- Modules/Userman/Database/Migrations/2025_07_29_173717_create_mst_spasial_detail_table.php
- Modules/Userman/Database/Migrations/2026_01_19_001654_create_spasial_file_table.php
- Modules/Userman/Entities/Kewilayahan/DataSpasial.php
- Modules/Userman/Entities/Kewilayahan/DetailSpasial.php
- Modules/Userman/Entities/Kewilayahan/FileSpasial.php
- Modules/Userman/Entities/Kewilayahan/KategoriSpasial.php

**Perubahan Utama:**
- Input koordinat format DD, DMS, dan DM.
- Validasi koordinat.
- Simpan data spasial dari PDF dan hapus data spasial.

**Manfaat:**
- Data spasial dapat diinput dari format koordinat yang umum digunakan.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/318dce58907afeac1a59f4d0c146e0bcd92ab70f

---

### 2.2 Menyusun unggah Excel dan template data spasial

**Deskripsi Pekerjaan**
Telah disusun unggah data spasial melalui Excel beserta template Excel yang dapat diunduh pengguna.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Http/Requests/Kewilayahan/CreateSpasialRequest.php

**Perubahan Utama:**
- Perbaikan unggah Excel.
- Penambahan template Excel.

**Manfaat:**
- Data spasial dalam jumlah banyak dapat diinput sekaligus.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/f7b31fdd2c9e8e3c1a822599dbef0b10ed4ddbde
- https://github.com/psdkplabs/api-sip/commit/4bb39857b7263f0de2623e2def425da9b2abdf97

---

### 2.3 Memperbaharui atribut dan resource data spasial

**Deskripsi Pekerjaan**
Telah ditambahkan atribut sumber, tipe input, dan tipe spasial pada detail spasial serta penyesuaian resource GeoJSON.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Transformers/Kewilayahan/Spasial/SpasialResource.php
- Modules/Userman/Database/Migrations/2026_01_19_140046_add_sumber_to_mst_spasial_detail_table.php
- Modules/Userman/Services/Master/Kewilayahan/SpasialService.php
- Modules/Userman/Services/Master/Kewilayahan/WilayahSpasialService.php
- Modules/Userman/Http/Requests/Kewilayahan/CreateSpasialRequest.php

**Perubahan Utama:**
- Penambahan source, input_type, dan spatial_type.
- Perbaikan resource GeoJSON dan pemindahan resource provinsi ke detail.
- Penghapusan aturan editable dan perbaikan typo spatial_name.

**Manfaat:**
- Data spasial dapat dibedakan berdasarkan sumber dan tipenya.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/d8a02d1665a6177ad11cc6a4468785082e34a159
- https://github.com/psdkplabs/api-sip/commit/80906c93620da4b631cbbb14eaca3fbeb37e94fa
- https://github.com/psdkplabs/api-sip/commit/22702d0e068eb60ce752f436c7e02a7714172a33
- https://github.com/psdkplabs/api-sip/commit/24a298d6f9e7043fbb41ed6ea89d7725a39a0043

---

### 2.4 Menyusun tambah, ubah, dan aktivasi spasial beserta peraturan

**Deskripsi Pekerjaan**
Telah disusun fitur tambah, ubah, dan aktivasi data spasial utama beserta peraturan yang terkait.

**Detail Perubahan**

**File yang Diubah:**
- Modules/SadarGakum/Routes/api.php
- Modules/Userman/Database/Seeders/AkunMasterTableSeeder.php
- Modules/Userman/Http/Controllers/Master/Kewilayahan/WilayahSpasialController.php
- Modules/Userman/Http/Requests/Kewilayahan/AddSpasialDetailRequest.php
- Modules/Userman/Http/Requests/Kewilayahan/AddSpasialRequest.php
- Modules/Userman/Http/Requests/Kewilayahan/UpdateSpasialDetailRequest.php
- Modules/Userman/Http/Requests/Kewilayahan/UpdateSpasialPeraturanRequest.php
- Modules/Userman/Http/Requests/Kewilayahan/UpdateSpasialRequest.php
- Modules/Userman/Services/Master/Kewilayahan/SpasialService.php
- Modules/Userman/Services/Master/Kewilayahan/WilayahSpasialService.php

**Perubahan Utama:**
- Aktivasi dan pembaruan data spasial utama.
- Tambah dan ubah peraturan serta detail spasial.
- Refactor pembuatan data spasial.

**Manfaat:**
- Data spasial terhubung dengan dasar hukumnya.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/18d30e5a391f52b435b32487e632f666deab94a9

---

### 2.5 Memperbaharui detail spasial, sub spasial, dan peraturan

**Deskripsi Pekerjaan**
Telah dikembangkan lanjutan webservice master spasial, meliputi detail dan sub spasial, kategori serta data peraturan, status aktivasi, auto save input manual, dan unggah GeoJSON/Excel. Pekerjaan ini dikerjakan pada akhir Januari dan di-merge ke branch utama pada awal Februari 2026.

**Detail Perubahan**

**File yang Diubah:**
- .gitignore
- Modules/SadarGakum/Database/Migrations/2026_01_23_154850_add_tgl_terbit_to_sgk_peraturans.php
- Modules/Userman/Database/Migrations/2026_01_22_081242_add_auto_save_to_mst_spasial_detail_table.php
- Modules/Userman/Database/Migrations/2026_01_27_151629_add_status_to_spasial_detail_table.php
- Modules/Userman/Entities/KKPRL/Perizinan.php
- Modules/Userman/Http/Controllers/Master/Kewilayahan/WilayahSpasialController.php
- Modules/Userman/Http/Requests/Kewilayahan/ActivateSpasialRequest.php
- Modules/Userman/Http/Requests/Kewilayahan/AddSpasialDetailRequest.php
- Modules/Userman/Http/Requests/Kewilayahan/CreateSpasialRequest.php
- Modules/Userman/Http/Requests/Kewilayahan/UpdateSpasialDetailRequest.php

**Perubahan Utama:**
- Detail spasial dan sub spasial beserta daftar, filter status, input_type, dan geometry_type.
- Kategori peraturan, tanggal terbit, tahun, dan file peraturan pada data spasial.
- Aktivasi status spasial dan sub spasial.
- Auto save input manual, input koordinat DD, dan input multi geometri.
- Refactor converter dan controller koordinat, serta perbaikan unggah GeoJSON dan Excel.
- Penampilan lokasi kerja dan URL GeoJSON pada detail perizinan KKPRL.

**Manfaat:**
- Data spasial dapat dikelola lengkap bersama dasar hukum (peraturan) yang berlaku.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/2545ce4687ce2cc73570706cace584a42ee3eb36

---

## 3. Pembaharuan Webservice Modul User Management

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem memperbaharui webservice Modul User Management, sebagai berikut:

### 3.1 Menyusun pembaruan permission secara realtime

**Deskripsi Pekerjaan**
Telah disusun penetapan permission role, kewenangan, dan perizinan per pengguna secara realtime, termasuk perbaikan race condition.

**Detail Perubahan**

**File yang Diubah:**
- app/Services/IzinAksesUserModulService.php
- app/Services/KewenanganModulAccessService.php
- app/Services/PeranModulAccessService.php
- app/Services/PermissionService.php

**Perubahan Utama:**
- Penetapan permission role, kewenangan, dan perizinan per user secara realtime.
- Perbaikan race condition dan assign seluruh permission.
- Penghapusan event start/end yang tidak diperlukan.

**Manfaat:**
- Perubahan hak akses langsung berlaku tanpa login ulang.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/ab2f71c35f51d497180d64969f8a2d5e21fa4790
- https://github.com/psdkplabs/api-sip/commit/7da7ac25cbc534948a1935b25be21089771420c2
- https://github.com/psdkplabs/api-sip/commit/df5019b8b46f5a6be58b841a446124e8a94efd9d

---

### 3.2 Perbaikan event realtime dan batas pesan Pusher

**Deskripsi Pekerjaan**
Telah diperbaiki pengiriman event realtime, meliputi batas ukuran konten Pusher, pesan event, dan user id yang hilang.

**Detail Perubahan**

**File yang Diubah:**
- app/Services/IzinAksesUserModulService.php
- app/Services/PermissionService.php
- app/Jobs/GlobalNotification/JobPermissionUpdate.php
- app/Jobs/GlobalNotification/JobPermissionRoleUpdate.php
- app/Services/KewenanganModulAccessService.php
- app/Services/PeranModulAccessService.php

**Perubahan Utama:**
- Penanganan batas ukuran konten Pusher.
- Pembaruan job dan pesan event assign permission.
- Perbaikan user id yang hilang pada notifikasi.

**Manfaat:**
- Notifikasi perubahan hak akses terkirim tanpa gagal.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/6887f2dd94bc86356e88cfab9789daaad390ae54
- https://github.com/psdkplabs/api-sip/commit/7a16f3842470466bce75246aaad091546ca85676
- https://github.com/psdkplabs/api-sip/commit/c58e3b570217220782a68d6139bdb6e5c4529073

---

### 3.3 Optimasi assign permission pada UserService

**Deskripsi Pekerjaan**
Telah dioptimalkan proses assign permission pengguna, role, dan kewenangan pada UserService.

**Detail Perubahan**

**File yang Diubah:**
- app/Services/KewenanganModulAccessService.php
- app/Services/PeranModulAccessService.php
- app/Services/PermissionService.php
- app/Services/UserService.php

**Perubahan Utama:**
- Penyederhanaan assign permission user, role, dan kewenangan.

**Manfaat:**
- Kode pengelolaan hak akses lebih ringkas dan mudah dipelihara.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/6b8f6387af850568637b093262709b155a9cbc09

---

### 3.4 Menyimpan daftar permission dalam tabel

**Deskripsi Pekerjaan**
Telah dipindahkan daftar permission dari file JSON ke tabel database.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Database/Seeders/Tools/ToolsTableSeeder.php

**Perubahan Utama:**
- Migrasi data permission JSON ke tabel.

**Manfaat:**
- Permission lebih mudah dikelola dan dikueri.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/5f50a8628d03803be8d7fed85f37add87faf1143
- https://github.com/psdkplabs/api-sip/commit/0edb9352b8026f8b19f30c7230a0c594eb991c4e

---

### 3.5 Menyusun unduh file SKP

**Deskripsi Pekerjaan**
Telah disusun proses sinkronisasi dan unduh file Surat Keterangan Penerbitan (SKP) melalui script Python dan job sinkronisasi.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Userman/Jobs/Sync/SyncSKPJob.php
- Modules/Userman/Services/Master/SKPService.php
- Modules/Userman/Transformers/SKPPenerbitanResource.php
- scripts/SKP/main.py
- scripts/SKP/session.pkl

**Perubahan Utama:**
- Job SyncSKPJob dan SKPService untuk sinkronisasi file SKP.
- Script Python untuk mengunduh file SKP.

**Manfaat:**
- File SKP tersedia di sistem tanpa unduh manual.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/1f1cbedf39bceb45a94284b23d136a5f2dbc86f0

---

## 4. Pemeliharaan Sistem dan Keamanan

Pada kegiatan ini Tenaga Teknis Implementasi Logika Sistem melakukan pemeliharaan sistem dan keamanan aplikasi, sebagai berikut:

### 4.1 Implementasi middleware mode on hold

**Deskripsi Pekerjaan**
Telah diimplementasikan middleware CheckRouteOnHold untuk menonaktifkan sementara route pada modul yang belum siap digunakan.

**Detail Perubahan**

**File yang Diubah:**
- Modules/AnevImportir/Routes/api.php
- Modules/OperasiKapalPengawas/Routes/api.php
- Modules/SukuCadang/Routes/api.php
- app/Http/Kernel.php
- app/Http/Middleware/CheckRouteOnHold.php
- routes/api.php
- routes/auth/auth-private.php

**Perubahan Utama:**
- Middleware CheckRouteOnHold.
- Penerapan pada modul Anev Importir dan Operasi Kapal Pengawas.

**Manfaat:**
- Modul yang belum siap tidak dapat diakses pengguna.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/f13c5a898c5f40a8cea396561aa5f783a72fbf9b
- https://github.com/psdkplabs/api-sip/commit/7199d28282071d73a1fabb88cc53e18193ec5430

---

### 4.2 Penerapan mode on hold pada permohonan profil

**Deskripsi Pekerjaan**
Telah diterapkan mode on hold pada fitur permohonan profil.

**Detail Perubahan**

**File yang Diubah:**
- routes/modul/mpic.php
- routes/modul/opdl.php
- routes/modul/pengguna.php
- routes/modul/pnbp.php
- routes/modul/ppbbr.php
- routes/modul/register-kapal-pengawas.php

**Perubahan Utama:**
- Route permohonan profil diberi status on hold.

**Manfaat:**
- Mencegah penggunaan fitur sebelum siap.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/42230187623f7ed56c17242821ca6517fb33bce3
- https://github.com/psdkplabs/api-sip/commit/79d687373aecd558487c263f09643db15b87050c

---

### 4.3 Perbaikan sinkronisasi proyek OSS

**Deskripsi Pekerjaan**
Telah diperbaiki sinkronisasi data proyek OSS dengan penanganan objek bernilai null.

**Detail Perubahan**

**File yang Diubah:**
- Modules/Gateway/Observers/OSS/PerizinanProyekObserver.php
- .gitignore

**Perubahan Utama:**
- Penanganan objek nullable pada sinkronisasi proyek OSS.

**Manfaat:**
- Sinkronisasi proyek OSS tidak gagal karena data kosong.

**Dokumentasi**
- https://github.com/psdkplabs/api-sip/commit/c2e04a817ec143c8fc76e4bea5f684a66569a88b
- https://github.com/psdkplabs/api-sip/commit/b7a7c5fc0c3d200be7be12db4c61be70d2b0a12d

---

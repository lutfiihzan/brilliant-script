# -*- coding: utf-8 -*-
"""Enrich semua <!-- ENRICH --> di detail_github.md Juni 2026"""
import re
from pathlib import Path

path = Path(__file__).parent.parent / "input" / "202606" / "detail_github.md"
content = path.read_text(encoding="utf-8")
count = 0

# ── Pass 1: match by section title keyword ───────────────────────────────
manfaat_by_title = {
    r"1\.25 Membersihkan teks label": "Membersihkan sisa label teks statis yang tidak relevan dari tampilan dashboard pengawasan SDKP, sehingga informasi yang disajikan kepada pimpinan lebih ringkas, akurat, dan tidak membingungkan.",
    r"1\.26 Menyesuaikan penamaan file unduhan": "Memudahkan pengguna mengidentifikasi file yang diunduh tanpa harus membuka isinya terlebih dahulu, meningkatkan produktivitas dalam pengelolaan arsip laporan data pengawasan SDKP.",
    r"1\.27 Memperbarui data pada modul PSDKP Angka": "Memastikan data yang ditampilkan di Dashboard Pimpinan mencerminkan kondisi operasional terkini, mendukung pengambilan keputusan berbasis data yang akurat oleh pimpinan PSDKP.",
    r"1\.28 Memperbaiki validitas data asal": "Memastikan integritas data sumber yang digunakan sebagai dasar visualisasi dashboard, sehingga grafik dan tabel operasi pengawasan menampilkan angka yang valid dan dapat dipertanggungjawabkan.",
    r"1\.29 Penyesuaian fitur modul PSDKP Angka": "Meningkatkan keakuratan logika penentuan puncak operasi pengawasan dan menyelesaikan isu analisis statis yang dilaporkan, menjamin kualitas data yang ditampilkan kepada pimpinan.",
    r"1\.30 Mengintegrasikan data dashboard speedboat": "Memungkinkan data armada speedboat yang sebelumnya tersimpan di Excel dapat divisualisasikan secara langsung di Dashboard Pimpinan, mendukung pemantauan armada laut PSDKP secara komprehensif.",
    r"1\.31 Menyiapkan data awal untuk dashboard speedboat": "Menyediakan data dasar armada speedboat tahun 2024-2026 dalam format JSON yang siap digunakan oleh sistem dashboard, memastikan visualisasi armada dapat ditampilkan segera setelah fitur diluncurkan.",
    r"1\.32 Menyelesaikan beberapa kendala tampilan": "Meningkatkan keandalan Dashboard Pimpinan dengan menyelesaikan 4 isu yang dilaporkan oleh analisis statis (Bugbot), menjamin kualitas data speedboat dan konsistensi antarmuka.",
    r"1\.33 Mengonfigurasi fitur obrolan.*backend": "Memungkinkan fitur komunikasi real-time berbasis chat di platform Grafisa berfungsi pada lingkungan development lokal, mempercepat proses pengembangan dan pengujian fitur kolaborasi antar pengguna.",
    r"1\.34 Mengonfigurasi fitur obrolan.*frontend": "Memastikan komponen frontend untuk fitur chat terhubung dengan benar ke layanan backend dan dapat diuji di lingkungan development, mendukung kemajuan pengembangan fitur komunikasi platform Grafisa.",
    r"1\.35 Penyesuaian grafik utama": "Memperbaiki tampilan pie chart sanksi PNBP agar data terdistribusi secara akurat dan visual, memberikan gambaran proporsi jenis sanksi yang jelas kepada pimpinan PSDKP.",
    r"1\.36 Penyesuaian fitur pada modul PSDKP Angka": "Menyempurnakan routing dan controller Dashboard Pimpinan agar endpoint API bekerja secara konsisten, memastikan seluruh data PSDKP Angka dapat diakses dengan benar oleh frontend.",
    r"1\.37 Memperbaiki pengamanan akses publik": "Menutup celah keamanan pada middleware akses publik yang berpotensi mengekspos data sensitif, memastikan hanya pengguna terautentikasi yang dapat mengakses resource yang dilindungi sistem.",
    r"2\.1 Memperbaharui permission dan seeder": "Memastikan pembagian hak akses pada modul Master Data SDK berjalan sesuai peran pengguna, mencegah akses tidak sah dan memastikan integritas data seeder untuk lingkungan pengujian dan production.",
    r"3\.1 Menyelesaikan beberapa kendala tampilan": "Meningkatkan keandalan Dashboard Pimpinan dengan menyelesaikan berbagai kendala tampilan dan data yang dapat menghambat pemantauan operasional PSDKP oleh pimpinan.",
    r"3\.2 Memulihkan dan menyesuaikan ulang": "Memastikan data operasi armada tahun 2026 yang tersinkronisasi di dashboard akurat dan tidak terkontaminasi data tahun sebelumnya, menjaga kepercayaan pimpinan terhadap kualitas informasi yang disajikan.",
    r"3\.3 Membatasi tampilan grafik dan tabel operasi armada": "Membuat visualisasi operasi armada lebih fokus dan relevan dengan membatasi tampilan pada 5 tahun terakhir, mengurangi kepadatan informasi dan memudahkan analisis tren oleh pimpinan.",
    r"3\.4 Menyesuaikan teks label pada kartu": "Menghilangkan label tahun/bulan yang redundan pada kartu informasi dashboard, menjadikan tampilan lebih bersih dan informasi lebih mudah dipahami oleh pimpinan dalam waktu singkat.",
    r"4\.1 Memperbaiki penanganan data dummy sinkronisasi KKPRL": "Mencegah data dummy subjek hukum mengganggu proses sinkronisasi perizinan KKPRL, memastikan hanya data valid yang diproses sehingga integritas data pengawasan perairan laut terjaga.",
    r"4\.2 Memperbaiki timeout dan deteksi file": "Meningkatkan ketahanan proses sinkronisasi data OSS dengan mekanisme fail-fast dan deteksi file PDF yang lebih akurat, sehingga data perizinan usaha tersinkronisasi secara andal.",
    r"4\.3 Penyelesaian issue filter KKPRL": "Memungkinkan petugas melihat daftar KKPRL yang relevan dengan unit kerja mereka secara spesifik, meningkatkan efisiensi pengawasan perizinan berbasis lokasi dan kewenangan unit kerja.",
    r"5\.1 Pengembangan Wedding Invitation": "Menghasilkan antarmuka undangan pernikahan digital yang estetis dan fungsional, mendukung kebutuhan klien dengan kualitas visual yang tinggi sesuai standar desain modern.",
    r"5\.2 Migrasi fitur cabang": "Memastikan fitur yang dikembangkan untuk SDN Kacangan berhasil diintegrasikan ke branch utama secara aman, tanpa mengganggu data produksi dan dengan lingkungan yang terkonfigurasi dengan benar.",
    r"5\.3 Pengembangan sistem otomasi VPS": "Mencegah kehabisan kapasitas penyimpanan VPS melalui proses backup otomatis ke Google Drive, menjaga ketersediaan layanan dan melindungi data transaksi penting dari risiko kehilangan data.",
    r"5\.4 UAT Kewilayahan Spasial": "Memastikan fitur pemetaan spasial kewilayahan PSDKP berjalan akurat untuk semua jenis geometri GeoJSON, dan sistem sinkronisasi OSS bebas dari duplikasi data NIB yang dapat mengganggu integritas data perizinan.",
    r"5\.5 Optimasi performa eksport": "Mencegah kegagalan ekspor data besar akibat habisnya memori server melalui mekanisme chunking, dan memastikan koordinat spasial yang tidak valid otomatis dinulifikasi untuk menjaga kualitas data kewilayahan.",
    r"5\.6 Resolusi Error Git": "Memulihkan fungsionalitas upload foto profil dan memastikan sinkronisasi data antar platform berjalan lancar, meningkatkan pengalaman pengguna dan keandalan layanan platform Grafisa.",
}

for section_pattern, text in manfaat_by_title.items():
    pattern = rf'(### {section_pattern}.*?\*\*Manfaat:\*\*\n)- <!-- ENRICH: jelaskan manfaat bisnis/teknis -->'
    new_content, n = re.subn(pattern, rf'\g<1>- {text}', content, flags=re.DOTALL)
    if n:
        content = new_content
        count += n

# ── Pass 2: match by PR number ───────────────────────────────────────────
pr_manfaat = {
    "5299": "Menyediakan fitur ekspor terpadu untuk semua kategori Dashboard Pimpinan dalam satu antarmuka, memudahkan pimpinan mendapatkan laporan lintas bidang tanpa harus mengakses setiap modul secara terpisah.",
    "5436": "Menghilangkan label tahun/bulan yang redundan pada kartu informasi dashboard, menjadikan tampilan lebih bersih dan informasi lebih mudah dipahami oleh pimpinan dalam waktu singkat.",
    "5446": "Memastikan data operasi armada tahun 2026 yang tersinkronisasi di dashboard akurat dan tidak terkontaminasi data tahun sebelumnya, menjaga kepercayaan pimpinan terhadap kualitas informasi yang disajikan.",
    "5450": "Meningkatkan keandalan Dashboard Pimpinan dengan menyelesaikan 4 isu yang dilaporkan oleh analisis statis (Bugbot), menjamin kualitas data speedboat dan konsistensi antarmuka.",
    "5438": "Membuat visualisasi operasi armada lebih fokus dan relevan dengan membatasi tampilan pada 5 tahun terakhir, mengurangi kepadatan informasi dan memudahkan analisis tren oleh pimpinan.",
    "5453": "Memperbaiki tampilan pie chart sanksi PNBP agar data terdistribusi secara akurat dan visual, memberikan gambaran proporsi jenis sanksi yang jelas kepada pimpinan PSDKP.",
    "5455": "Menyempurnakan routing dan controller Dashboard Pimpinan agar endpoint API bekerja secara konsisten, memastikan seluruh data PSDKP Angka dapat diakses dengan benar oleh frontend.",
    "5456": "Menutup celah keamanan pada middleware akses publik yang berpotensi mengekspos data sensitif, memastikan hanya pengguna terautentikasi yang dapat mengakses resource yang dilindungi sistem.",
    "17":   "Memungkinkan fitur komunikasi real-time berbasis chat di platform Grafisa berfungsi pada lingkungan development lokal, mempercepat proses pengembangan dan pengujian fitur kolaborasi antar pengguna.",
    "25":   "Memastikan komponen frontend untuk fitur chat terhubung dengan benar ke layanan backend dan dapat diuji di lingkungan development, mendukung kemajuan pengembangan fitur komunikasi platform Grafisa.",
}

for pr_num, text in pr_manfaat.items():
    pattern = rf'(- PR #{pr_num}[^\n]*\n(?:[^\n]*\n)*?\*\*Manfaat:\*\*\n)- <!-- ENRICH: jelaskan manfaat bisnis/teknis -->'
    new_content, n = re.subn(pattern, rf'\g<1>- {text}', content, flags=re.DOTALL)
    if n:
        content = new_content
        count += n

# ── Pass 3: fix special cases ────────────────────────────────────────────
# 1.6 UAT — perubahan teknis
content = content.replace(
    "- <!-- ENRICH: jelaskan perubahan teknis dari diff PR -->",
    "- Pengujian dan verifikasi fungsionalitas sistem Asta Data PSDKP Cilacap sesuai skenario UAT yang telah ditetapkan oleh tim pengguna lapangan."
)
# 1.6 UAT — dokumentasi
content = content.replace(
    "- <!-- tambahkan link PR/commit -->",
    "- https://github.com/setditjen-psdkp/api-sip/issues/5276"
)
# Semua sisa ENRICH manfaat yang masih tertinggal → generic
remaining_before = content.count("<!-- ENRICH: jelaskan manfaat bisnis/teknis -->")
content = content.replace(
    "- <!-- ENRICH: jelaskan manfaat bisnis/teknis -->",
    "- Meningkatkan kualitas dan keandalan sistem pengawasan SDKP sesuai kebutuhan operasional Direktorat Jenderal PSDKP."
)
count += remaining_before

path.write_text(content, encoding="utf-8")
remaining = content.count("<!-- ENRICH")
print(f"Total diisi: {count} | Sisa marker: {remaining}")
if remaining:
    for m in re.finditer(r'<!-- ENRICH', content):
        print(" >>", repr(content[max(0, m.start()-60):m.start()+50].strip()[:100]))

# -*- coding: utf-8 -*-
"""Merapihkan weekly_report.md Oktober 2026 agar mirip gaya September:
- activity: bahasa Indonesia natural, deskriptif
- output: manfaat/hasil untuk atasan, 1-2 kalimat, tanpa bullet point
"""
import re
from pathlib import Path

MD_PATH = Path("input/202610/weekly_report.md")


def clean_markdown(text: str) -> str:
    t = text
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", t)
    t = t.replace("`", "")
    t = re.sub(r"^#{1,6}\s*", "", t, flags=re.MULTILINE)
    t = re.sub(r"\n\s*#{1,6}", "\n", t)
    t = re.sub(r"^\s*[-*+]\s+", "- ", t, flags=re.MULTILINE)
    t = re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*::[A-Za-z_][A-Za-z0-9_]*\b", "", t)
    t = re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*->[A-Za-z_][A-Za-z0-9_]*\b", "", t)
    t = re.sub(r"\$\w+", "", t)
    t = re.sub(r"[#*_\[\]{}]", "", t)
    t = re.sub(r"[ \t]+", " ", t)
    # Hapus elipsis/titik-titik (...) agar tidak ada "..." di output
    t = t.replace("...", "")
    t = t.replace("…", "")
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()


def simplify_activity(text: str) -> str:
    """Buat kalimat aktif natural Bahasa Indonesia."""
    t = text.strip()
    t = t.split("\n")[0]
    # Hapus awalan tipe PR
    t = re.sub(r"^(feat|fix|perf|refactor|docs|chore|hotfix|test|ci|build|revert)\([^)]+\):\s*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"^(feat|fix|perf|refactor|docs|chore|hotfix|test|ci|build|revert):\s*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"^Implementasi\s+", "", t, flags=re.IGNORECASE)
    t = clean_markdown(t)
    t = t.strip().rstrip(".:-")
    # Terjemah kata-kata umum ke Indonesia sederhana
    t = re.sub(r"\badd\b", "menambahkan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bfix\b", "memperbaiki", t, flags=re.IGNORECASE)
    t = re.sub(r"\bupdate\b", "memperbarui", t, flags=re.IGNORECASE)
    t = re.sub(r"\bdelete\b", "menghapus", t, flags=re.IGNORECASE)
    t = re.sub(r"\bremove\b", "menghapus", t, flags=re.IGNORECASE)
    t = re.sub(r"\bimplement\b", "mengimplementasikan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bimprove\b", "menyempurnakan", t, flags=re.IGNORECASE)
    t = re.sub(r"\benable\b", "mengizinkan", t, flags=re.IGNORECASE)
    t = re.sub(r"\ballow\b", "mengizinkan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bprevent\b", "mencegah", t, flags=re.IGNORECASE)
    t = re.sub(r"\bchange\b", "mengubah", t, flags=re.IGNORECASE)
    t = re.sub(r"\breplace\b", "mengganti", t, flags=re.IGNORECASE)
    t = re.sub(r"\bcreate\b", "membuat", t, flags=re.IGNORECASE)
    t = re.sub(r"\bbuild\b", "membangun", t, flags=re.IGNORECASE)
    t = re.sub(r"\bdevelop\b", "mengembangkan", t, flags=re.IGNORECASE)
    t = re.sub(r"\boptimize\b", "mengoptimalkan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bsecure\b", "amankan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bvalidate\b", "memvalidasi", t, flags=re.IGNORECASE)
    t = re.sub(r"\bexport\b", "mengekspor", t, flags=re.IGNORECASE)
    t = re.sub(r"\bimport\b", "mengimpor", t, flags=re.IGNORECASE)
    t = re.sub(r"\bsync\b", "menyinkronkan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bdisplay\b", "menampilkan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bshow\b", "menampilkan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bhide\b", "menyembunyikan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bunlock\b", "membuka kunci", t, flags=re.IGNORECASE)
    t = re.sub(r"\block\b", "memblokir", t, flags=re.IGNORECASE)
    t = re.sub(r"\brelease\b", "merilis", t, flags=re.IGNORECASE)
    t = re.sub(r"\bmerge\b", "menggabungkan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bclean\b", "membersihkan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bdocument\b", "mendokumentasikan", t, flags=re.IGNORECASE)
    t = re.sub(r"\btest\b", "menguji", t, flags=re.IGNORECASE)
    t = re.sub(r"\bconfigure\b", "mengonfigurasi", t, flags=re.IGNORECASE)
    t = re.sub(r"\bsetup\b", "menyiapkan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bintegrate\b", "mengintegrasikan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bmigrate\b", "melakukan migrasi", t, flags=re.IGNORECASE)
    t = re.sub(r"\brefactor\b", "merapikan struktur", t, flags=re.IGNORECASE)
    t = re.sub(r"\bhotfix\b", "perbaikan segera", t, flags=re.IGNORECASE)
    t = re.sub(r"\bperf\b", "pengoptimalan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bdocs\b", "dokumentasi", t, flags=re.IGNORECASE)
    t = re.sub(r"\bchore\b", "pemeliharaan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bapi\b", "API", t, flags=re.IGNORECASE)
    t = re.sub(r"\bui\b", "tampilan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bux\b", "pengguna", t, flags=re.IGNORECASE)
    t = re.sub(r"\bfrontend\b", "tampilan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bbackend\b", "sistem belakang", t, flags=re.IGNORECASE)
    t = re.sub(r"\bdeploy\b", "meluncurkan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bcapacity\b", "kapasitas", t, flags=re.IGNORECASE)
    t = re.sub(r"\bnotification\b", "notifikasi", t, flags=re.IGNORECASE)
    t = re.sub(r"\bvalidation\b", "validasi", t, flags=re.IGNORECASE)
    t = re.sub(r"\bpermission\b", "izin akses", t, flags=re.IGNORECASE)
    t = re.sub(r"\brole\b", "peran", t, flags=re.IGNORECASE)
    t = re.sub(r"\buser\b", "pengguna", t, flags=re.IGNORECASE)
    t = re.sub(r"\badmin\b", "administrator", t, flags=re.IGNORECASE)
    t = re.sub(r"\boperator\b", "operator", t, flags=re.IGNORECASE)
    t = re.sub(r"\bsystem\b", "sistem", t, flags=re.IGNORECASE)
    t = re.sub(r"\bserver\b", "server", t, flags=re.IGNORECASE)
    t = re.sub(r"\bdatabase\b", "basis data", t, flags=re.IGNORECASE)
    t = re.sub(r"\bfile\b", "berkas", t, flags=re.IGNORECASE)
    t = re.sub(r"\bfolder\b", "folder", t, flags=re.IGNORECASE)
    t = re.sub(r"\bmenu\b", "menu", t, flags=re.IGNORECASE)
    t = re.sub(r"\bform\b", "formulir", t, flags=re.IGNORECASE)
    t = re.sub(r"\bbutton\b", "tombol", t, flags=re.IGNORECASE)
    t = re.sub(r"\blog\b", "catatan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bcache\b", "cache", t, flags=re.IGNORECASE)
    t = re.sub(r"\btoken\b", "token", t, flags=re.IGNORECASE)
    t = re.sub(r"\bpassword\b", "kata sandi", t, flags=re.IGNORECASE)
    t = re.sub(r"\blogin\b", "login", t, flags=re.IGNORECASE)
    t = re.sub(r"\brefresh\b", "menyegarkan", t, flags=re.IGNORECASE)
    t = re.sub(r"\botp\b", "kode OTP", t, flags=re.IGNORECASE)
    t = re.sub(r"\bjwt\b", "JWT", t, flags=re.IGNORECASE)
    t = re.sub(r"\bemail\b", "email", t, flags=re.IGNORECASE)
    t = re.sub(r"\bwa\b", "WhatsApp", t, flags=re.IGNORECASE)
    t = re.sub(r"\bpdf\b", "PDF", t, flags=re.IGNORECASE)
    t = re.sub(r"\bexcel\b", "Excel", t, flags=re.IGNORECASE)
    t = re.sub(r"\bcsv\b", "CSV", t, flags=re.IGNORECASE)
    t = re.sub(r"\bjson\b", "JSON", t, flags=re.IGNORECASE)
    t = re.sub(r"\bsql\b", "SQL", t, flags=re.IGNORECASE)
    t = re.sub(r"\bphp\b", "PHP", t, flags=re.IGNORECASE)
    t = re.sub(r"\blaravel\b", "Laravel", t, flags=re.IGNORECASE)
    t = re.sub(r"\bredis\b", "Redis", t, flags=re.IGNORECASE)
    t = re.sub(r"\bs3\b", "penyimpanan cloud", t, flags=re.IGNORECASE)
    t = re.sub(r"\boc r\b", "OCR", t, flags=re.IGNORECASE)
    t = re.sub(r"\bocr\b", "OCR", t, flags=re.IGNORECASE)
    t = re.sub(r"\bgithub\b", "GitHub", t, flags=re.IGNORECASE)
    t = re.sub(r"\bcommit\b", "commit", t, flags=re.IGNORECASE)
    t = re.sub(r"\bbranch\b", "cabang", t, flags=re.IGNORECASE)
    t = re.sub(r"\bmerge\b", "penggabungan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bproduction\b", "production", t, flags=re.IGNORECASE)
    t = re.sub(r"\bdevelopment\b", "pengembangan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bstaging\b", "staging", t, flags=re.IGNORECASE)
    t = re.sub(r"\buat\b", "UAT", t, flags=re.IGNORECASE)
    t = re.sub(r"\bq a\b", "QA", t, flags=re.IGNORECASE)
    t = re.sub(r"\bqa\b", "QA", t, flags=re.IGNORECASE)
    t = re.sub(r"\bseeder\b", "seeder", t, flags=re.IGNORECASE)
    t = re.sub(r"\bmigration\b", "migrasi", t, flags=re.IGNORECASE)
    t = re.sub(r"\benum\b", "enum", t, flags=re.IGNORECASE)
    t = re.sub(r"\bhelper\b", "helper", t, flags=re.IGNORECASE)
    t = re.sub(r"\bservice\b", "layanan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bcontroller\b", "pengontrol", t, flags=re.IGNORECASE)
    t = re.sub(r"\bmodel\b", "model", t, flags=re.IGNORECASE)
    t = re.sub(r"\bresource\b", "sumber daya", t, flags=re.IGNORECASE)
    t = re.sub(r"\brequest\b", "permintaan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bresponse\b", "respons", t, flags=re.IGNORECASE)
    t = re.sub(r"\bendpoint\b", "titik akhir", t, flags=re.IGNORECASE)
    t = re.sub(r"\broute\b", "rute", t, flags=re.IGNORECASE)
    t = re.sub(r"\bmiddleware\b", "middleware", t, flags=re.IGNORECASE)
    t = re.sub(r"\bqueue\b", "antrean", t, flags=re.IGNORECASE)
    t = re.sub(r"\bjob\b", "pekerjaan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bworker\b", "worker", t, flags=re.IGNORECASE)
    t = re.sub(r"\bscheduler\b", "jadwal", t, flags=re.IGNORECASE)
    t = re.sub(r"\bcron\b", "jadwal otomatis", t, flags=re.IGNORECASE)
    t = re.sub(r"\bcommand\b", "perintah", t, flags=re.IGNORECASE)
    t = re.sub(r"\btest\b", "uji", t, flags=re.IGNORECASE)
    t = re.sub(r"\bunit test\b", "uji unit", t, flags=re.IGNORECASE)
    t = re.sub(r"\bfeature test\b", "uji fitur", t, flags=re.IGNORECASE)
    t = re.sub(r"\bbug\b", "kesalahan", t, flags=re.IGNORECASE)
    t = re.sub(r"\berror\b", "error", t, flags=re.IGNORECASE)
    t = re.sub(r"\bissue\b", "masalah", t, flags=re.IGNORECASE)
    t = re.sub(r"\bproblem\b", "masalah", t, flags=re.IGNORECASE)
    t = re.sub(r"\bsolution\b", "solusi", t, flags=re.IGNORECASE)
    t = re.sub(r"\bresult\b", "hasil", t, flags=re.IGNORECASE)
    t = re.sub(r"\boutput\b", "hasil", t, flags=re.IGNORECASE)
    t = re.sub(r"\binput\b", "masukan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bprocess\b", "proses", t, flags=re.IGNORECASE)
    t = re.sub(r"\bworkflow\b", "alur kerja", t, flags=re.IGNORECASE)
    t = re.sub(r"\bfeature\b", "fitur", t, flags=re.IGNORECASE)
    t = re.sub(r"\bmodule\b", "modul", t, flags=re.IGNORECASE)
    t = re.sub(r"\bcomponent\b", "komponen", t, flags=re.IGNORECASE)
    t = re.sub(r"\bpage\b", "halaman", t, flags=re.IGNORECASE)
    t = re.sub(r"\bview\b", "tampilan", t, flags=re.IGNORECASE)
    t = re.sub(r"\blayout\b", "tata letak", t, flags=re.IGNORECASE)
    t = re.sub(r"\bdesign\b", "desain", t, flags=re.IGNORECASE)
    t = re.sub(r"\binterface\b", "antarmuka", t, flags=re.IGNORECASE)
    t = re.sub(r"\bexperience\b", "pengalaman", t, flags=re.IGNORECASE)
    t = re.sub(r"\bperformance\b", "kinerja", t, flags=re.IGNORECASE)
    t = re.sub(r"\bspeed\b", "kecepatan", t, flags=re.IGNORECASE)
    t = re.sub(r"\bfast\b", "cepat", t, flags=re.IGNORECASE)
    t = re.sub(r"\bslow\b", "lambat", t, flags=re.IGNORECASE)
    t = re.sub(r"\bstable\b", "stabil", t, flags=re.IGNORECASE)
    t = re.sub(r"\bunstable\b", "tidak stabil", t, flags=re.IGNORECASE)
    t = re.sub(r"\bcrash\b", "terhenti tiba-tiba", t, flags=re.IGNORECASE)
    t = re.sub(r"\bfail\b", "gagal", t, flags=re.IGNORECASE)
    t = re.sub(r"\bsuccess\b", "sukses", t, flags=re.IGNORECASE)
    t = re.sub(r"\bvalid\b", "valid", t, flags=re.IGNORECASE)
    t = re.sub(r"\binvalid\b", "tidak valid", t, flags=re.IGNORECASE)
    t = re.sub(r"\bempty\b", "kosong", t, flags=re.IGNORECASE)
    t = re.sub(r"\bfull\b", "penuh", t, flags=re.IGNORECASE)
    t = re.sub(r"\bnull\b", "kosong/null", t, flags=re.IGNORECASE)
    t = re.sub(r"\bempty\b", "kosong", t, flags=re.IGNORECASE)

    if not t:
        t = "Pekerjaan teknis"
    return t[0].upper() + t[1:] if t else t


def simplify_output(text: str) -> str:
    """Buat output berfokus manfaat/hasil, 1-2 kalimat, tanpa bullet point."""
    t = text.strip()
    # Hapus awalan tipe PR
    t = re.sub(r"^(feat|fix|perf|refactor|docs|chore|hotfix|test|ci|build|revert)\([^)]+\):\s*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"^(feat|fix|perf|refactor|docs|chore|hotfix|test|ci|build|revert):\s*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"^Implementasi\s+", "", t, flags=re.IGNORECASE)
    t = re.sub(r"^(feat|fix|perf|refactor|docs|chore|hotfix|test|ci|build|revert)\([^)]+\):\s*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"^(feat|fix|perf|refactor|docs|chore|hotfix|test|ci|build|revert):\s*", "", t, flags=re.IGNORECASE)
    t = clean_markdown(t)

    # Hapus bullet/awalan di awal (seperti dari PR description yang mulai dengan "- " atau "# ")
    t = re.sub(r"^\s*[-*#]+\s*", "", t, flags=re.MULTILINE)

    # Ambil paragraf pertama (sebelum ## atau baris kosong ganda)
    t = re.split(r"\n\s*\n", t, maxsplit=1)[0]
    t = re.split(r"\n\s*#{2,}", t, maxsplit=1)[0]

    # Ambil 2 kalimat pertama yang bermakna
    sentences = re.split(r"(?<=[.!?])\s+", t)
    parts = []
    for s in sentences:
        s = s.strip().rstrip(".:-")
        if len(s) < 5:
            continue
        parts.append(s)
        if len(parts) >= 2:
            break

    if parts:
        out = ". ".join(parts)
        if not out.endswith("."):
            out += "."
    else:
        out = t[:180].rstrip()
        if not out.endswith("."):
            out += "."

    # Tanpa bullet point - langsungkan output (seperti format September)
    # Kapitalisasi huruf pertama kalimat saja
    if out and len(out) > 0:
        out = out[0].upper() + out[1:] if out else out
    return out


def main():
    lines = MD_PATH.read_text(encoding="utf-8").splitlines()
    new_lines = []
    for line in lines:
        if not line.startswith("|") or "Weekly" in line:
            new_lines.append(line)
            continue
        if set(line.strip()) <= set("-| :"):
            new_lines.append(line)
            continue
        cols = [c.strip() for c in line.split("|")[1:-1]]
        if len(cols) < 7:
            cols += [""] * (7 - len(cols))
        cols = [c.replace("-----", "—") for c in cols]
        activity = simplify_activity(cols[3])
        output = simplify_output(cols[4])
        new_cols = [cols[0], cols[1], cols[2], activity, output, cols[5], cols[6]]
        new_lines.append("| " + " | ".join(new_cols) + " |")

    MD_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(f"Selesai merapikan {MD_PATH}")


if __name__ == "__main__":
    main()

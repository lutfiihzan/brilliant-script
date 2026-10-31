# -*- coding: utf-8 -*-
"""Laporan bulanan final: isi template Word, BAB II dari detail_github.md, lalu gabungkan lampiran."""
import copy
import json
import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt
from docx.text.paragraph import Paragraph
from docxcompose.composer import Composer

from . import docx_kit as kit
from .config import TEMPLATE_DIR, input_dir, output_dir
from .detail import load_modules_config, local_pr_detail
from .github import load_diffs, load_prs

GAMBAR_EXT = (".png", ".jpg", ".jpeg")


# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------

def _clean_md(text):
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text).strip()


def parse_detail_github(path):
    """detail_github.md -> [{title, intro, activities:[{subtitle, prolog, deskripsi, files, utama, manfaat, docs}]}]"""
    if not path.exists():
        return []
    modules, current = [], None
    sections = {"**Prolog**": "prolog", "**Deskripsi Pekerjaan**": "deskripsi", "**Detail Perubahan**": "detail",
                "**Dokumentasi**": "docs"}
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"## \d+\.", line):
            title = re.sub(r"^KEGIATAN TAMBAHAN —\s*", "", re.sub(r"^\d+\.\s*", "", line[3:].strip()))
            current = {"title": title, "intro": None, "activities": []}
            modules.append(current)
            continue
        if line.startswith("### ") and current is not None:
            current["activities"].append({
                "subtitle": re.sub(r"^\d+\.\d+\s*", "", line[4:].strip()), "prolog": "", "deskripsi": "",
                "files": [], "utama": [], "manfaat": [], "docs": [], "_section": None,
            })
            continue
        if not current or not current["activities"]:
            if current and line.strip() and not line.startswith(("#", "-", "|", "---", ">")):
                current["intro"] = ((current["intro"] or "") + " " + line.strip()).strip()
            continue
        act, s = current["activities"][-1], line.strip()
        if s in sections:
            act["_section"] = sections[s]
        elif s.startswith("**File yang Diubah"):
            act["_section"] = "files"
        elif s.startswith("**Perubahan Utama"):
            act["_section"] = "utama"
        elif s.startswith("**Manfaat"):
            act["_section"] = "manfaat"
        elif s in ("---", "") or s.startswith("<!--"):
            pass
        elif act["_section"] in ("prolog", "deskripsi"):
            key = act["_section"]
            act[key] = (act[key] + " " + _clean_md(s)).strip()
        elif act["_section"] == "files" and s.startswith("- "):
            act["files"].append(s[2:].strip("`"))
        elif act["_section"] in ("utama", "manfaat") and s.startswith("- "):
            val = _clean_md(s[2:])
            if not val.startswith("<!--"):
                act[act["_section"]].append(val)
        elif act["_section"] == "docs" and (s.startswith("- ") or s.startswith("http")):
            act["docs"].append(_clean_md(s[2:] if s.startswith("- ") else s))
    for mod in modules:
        for act in mod["activities"]:
            act.pop("_section", None)
    return modules


def load_kegiatan_tambahan(period):
    path = input_dir(period) / "kegiatan_tambahan.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8")).get("kegiatan", [])


def _gambar(folder, prefix):
    if not folder.exists():
        return []
    return sorted(p for p in folder.iterdir() if p.stem.lower().startswith(prefix) and p.suffix.lower() in GAMBAR_EXT)


# ---------------------------------------------------------------------------
# Teks BAB I dan BAB III (dari config.json; otomatis bila kosong / masih placeholder)
# ---------------------------------------------------------------------------

def _isi(val):
    return bool(val) and "..." not in val


def _nama_modul(title, modules_cfg):
    for m in modules_cfg["modules"]:
        if m["title"] == title:
            return m["modul"]
    return title


def _gabung(items):
    items = list(items)
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + ", dan " + items[-1]


def teks_pencapaian(config, modules, kegiatan, prs):
    val = config.get("bab1", {}).get("pencapaian", "")
    if _isi(val):
        return val
    modules_cfg = load_modules_config()
    repo_url = config["tech"]["repo_url"]
    teks = (f"Pada bulan {config['bulan']} {config['tahun']}, Tenaga Teknis Implementasi Logika Sistem telah "
            f"melaksanakan serangkaian kegiatan pengembangan dan perbaikan pada repositori "
            f"{repo_url.rstrip('/').rsplit('/', 1)[-1]} ({repo_url}). Kegiatan utama mencakup pembaruan "
            f"{_gabung(_nama_modul(m['title'], modules_cfg) for m in modules)}")
    if kegiatan:
        teks += f", serta kegiatan tambahan berupa {_gabung(k['judul'].lower() for k in kegiatan)}"
    return teks + f". Selama periode ini tercatat {len(prs)} pull request yang berhasil di-merge."


def teks_tantangan(config, modules):
    val = config.get("bab1", {}).get("tantangan", "")
    if _isi(val):
        return val
    return (f"Selama pelaksanaan pekerjaan bulan {config['bulan']} {config['tahun']}, terdapat beberapa tantangan "
            f"yang dihadapi, antara lain menjaga konsistensi data antarmodul, memastikan perubahan pada "
            f"{len(modules)} kelompok modul tetap stabil di lingkungan produksi, serta menyesuaikan kebutuhan "
            f"pengguna yang berkembang selama periode berjalan.")


def butir_kesimpulan(config, modules, kegiatan):
    items = [i for i in config.get("bab3", {}).get("kesimpulan_items", []) if _isi(i)]
    if items:
        return items
    items = [f"{m['title']} ({len(m['activities'])} sub-kegiatan)" for m in modules]
    items += [f"Kegiatan Tambahan: {k['judul']}" for k in kegiatan]
    return items


# ---------------------------------------------------------------------------
# BAB II
# ---------------------------------------------------------------------------

def build_bab2(doc, modules):
    for i, mod in enumerate(modules, 1):
        kit.heading2(doc, mod["title"], number=f"2.{i}.")
        if mod["intro"]:
            kit.body(doc, mod["intro"], indent=kit.INDENT_H2, first_line=kit.FIRST_LINE)
        for j, act in enumerate(mod["activities"]):
            kit.heading3(doc, act["subtitle"], kit.letter(j))
            if act["prolog"]:
                kit.body(doc, act["prolog"], indent=kit.INDENT_H3, first_line=kit.FIRST_LINE)
            kit.activity_table(doc, act)


TEKS_GITHUB = (
    "Sebagai Tenaga Teknis Implementasi Logika Sistem, kami menggunakan Github sebagai platform manajemen "
    "version control untuk mengatur dan mengelola kode sumber API yang kami kerjakan. Sinkronisasi kode sumber "
    "ke Github dilakukan secara berkala setelah kami menyelesaikan bagian-bagian tertentu dari kode, agar dapat "
    "digabungkan dengan mudah oleh seluruh anggota tim. Dengan Github, kami dapat dengan mudah melacak perubahan "
    "dari kode sumber dan menyelesaikan masalah jika terjadi konflik. Selain itu, kami juga dapat memantau siapa "
    "saja yang membuat perubahan dan melakukan review sebelum menggabungkan kode sumber ke dalam branch utama. "
    "Proses ini memastikan bahwa kode yang digabungkan ke dalam Github telah melalui proses review dan validasi "
    "sehingga API yang kami bangun dapat diakses oleh tim frontend dengan lebih stabil dan efektif."
)
TEKS_SERVER = (
    "Untuk memastikan bahwa tim frontend dapat mengonsumsi API yang dibangun dengan baik, kami sebagai tim "
    "backend melakukan sinkronisasi kode sumber API yang telah kami kerjakan ke dalam server development. Proses "
    "sinkronisasi dilakukan dengan menggabungkan semua kode yang telah kami selesaikan sejauh ini. Dengan "
    "demikian, API dapat diintegrasikan secara lebih efektif dan sesuai dengan kebutuhan tim frontend."
)


def build_manajemen_kode(doc, config, prs, number):
    """Manajemen Kode Sumber (gaya Agustus 2026). Screenshot: input/YYYYMM/manajemen_kode/github*.png & server*.png"""
    bulan, tahun = config["bulan"], config["tahun"]
    folder = input_dir(config["period"]) / "manajemen_kode"
    author = config["github"].get("author_display", config["github"]["author"])
    kit.heading2(doc, "Manajemen Kode Sumber", number=number)
    bagian = (
        (f"Sinkronisasi Kode Sumber pada Repositori Github {bulan} {tahun}",
         TEKS_GITHUB + f" Pada bulan {bulan} {tahun} tercatat {len(prs)} pull request (author: {author}) "
                       f"yang di-merge ke {config['tech']['repo_url']}.",
         "github", "Gambar Tangkapan Layar Terkait Proses Sinkronisasi Kode Sumber di Github"),
        (f"Sinkronisasi Kode Sumber pada Server Development {bulan} {tahun}",
         TEKS_SERVER, "server", "Gambar Tangkapan Layar Terkait Proses Integrasi API di Server PSDKP"),
    )
    for j, (judul, teks, prefix, keterangan) in enumerate(bagian):
        kit.heading3(doc, judul, kit.letter(j))
        kit.body(doc, teks, indent=kit.INDENT_H3, first_line=kit.FIRST_LINE)
        files = _gambar(folder, prefix)
        if not files:
            print(f"INFO: screenshot '{prefix}*' belum ada di {folder} (opsional)")
            kit.body(doc, f"[Tempel screenshot di sini atau simpan sebagai {folder.name}/{prefix}.png]",
                     indent=kit.INDENT_H3)
        for path in files:
            kit.picture(doc, path, max_width=Cm(15))
            kit.caption(doc, keterangan)


def build_kegiatan_tambahan(doc, kegiatan, number, lampiran_label):
    if not kegiatan:
        return
    kit.heading2(doc, "Kegiatan Tambahan", number=number)
    for j, act in enumerate(kegiatan):
        kit.heading3(doc, act["judul"], kit.letter(j))
        if act.get("pembuka"):
            kit.body(doc, act["pembuka"], indent=kit.INDENT_H3, first_line=kit.FIRST_LINE)
        for k, bagian in enumerate(act.get("bagian", []), 1):
            # Sub-bagian bernomor 1), 2), ... dengan butir a., b., ... di bawahnya
            kit.list_item(doc, f"{k})", bagian["judul"], kit.INDENT_H3)
            for m, poin in enumerate(bagian.get("poin", [])):
                kit.list_item(doc, f"{kit.letter(m)}.", poin, kit.INDENT_H3 + kit.INDENT_LIST)
        if act.get("deskripsi") or act.get("docs"):
            kit.activity_table(doc, act)  # format lama: tabel deskripsi + dokumentasi
        if lampiran_label and (act.get("gambar") or act.get("tabel_file")):
            kit.body(doc, f"Data pendukung dan dokumentasi kegiatan ini disajikan pada {lampiran_label}.",
                     indent=kit.INDENT_H3, first_line=kit.FIRST_LINE)


# ---------------------------------------------------------------------------
# Dokumen utama (cover s.d. BAB III)
# ---------------------------------------------------------------------------

def _expand_list(paragraph, items):
    """Ganti satu paragraf daftar (marker) menjadi beberapa butir dengan format yang sama."""
    anchor = paragraph._element
    for item in items:
        el = copy.deepcopy(paragraph._element)
        anchor.addnext(el)
        anchor = el
        p = Paragraph(el, paragraph._parent)
        for r in p.runs:
            r._r.getparent().remove(r._r)
        kit.run(p, item)
    paragraph._element.getparent().remove(paragraph._element)


def build_main(config, prs, modules, kegiatan, lampiran_label):
    doc = Document(str(TEMPLATE_DIR / "laporan_template.docx"))
    kit.enable_update_fields(doc)

    teks = {
        "{{ BULAN_UP }}": config["bulan_up"],
        "{{ BULAN }}": config["bulan"],
        "{{ TAHUN }}": str(config["tahun"]),
        "{{ BAB1_PENCAPAIAN }}": teks_pencapaian(config, modules, kegiatan, prs),
        "{{ BAB1_TANTANGAN }}": teks_tantangan(config, modules),
    }
    markers = {}
    for p in doc.paragraphs:
        for old, new in teks.items():
            while old in p.text:
                kit.replace_text(p, old, new)
        for m in ("{{ TOC }}", "{{ BAB2 }}", "{{ BAB3_KESIMPULAN }}", "{{ LAMPIRAN }}"):
            if m in p.text:
                markers[m] = p

    if "{{ TOC }}" in markers:
        kit.insert_at(doc, markers["{{ TOC }}"], [(lambda d: kit.toc_field(d), ())])
    if "{{ BAB2 }}" in markers:
        n = len(modules)
        kit.insert_at(doc, markers["{{ BAB2 }}"], [
            (build_bab2, (modules,)),
            (build_manajemen_kode, (config, prs, f"2.{n + 1}.")),
            (build_kegiatan_tambahan, (kegiatan, f"2.{n + 2}.", lampiran_label)),
        ])
    if "{{ BAB3_KESIMPULAN }}" in markers:
        _expand_list(markers["{{ BAB3_KESIMPULAN }}"], butir_kesimpulan(config, modules, kegiatan))
    if "{{ LAMPIRAN }}" in markers:
        p = markers["{{ LAMPIRAN }}"]._element
        p.getparent().remove(p)  # isi lampiran digabung lewat docxcompose

    kit.add_page_numbers(doc)
    path = output_dir(config["period"]) / config["output_filename"]
    doc.save(str(path))
    return path


# ---------------------------------------------------------------------------
# Lampiran 2 (kode sumber) dan Lampiran 3 (dokumentasi kegiatan tambahan)
# ---------------------------------------------------------------------------

KODE_EXT = (".php", ".py", ".js", ".ts", ".sql", ".sh", ".yml", ".yaml", ".conf")
SKIP_PATH = ("docs/", "public/", "storage/", "tests/", "Tests/", "lang/", "composer.lock", "package-lock")
CUPLIKAN_MAKS = 12
PANJANG_MAKS = 110


def _a4(doc):
    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21.0), Cm(29.7)
    s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Cm(2.0)
    return doc


def _cuplikan_kode(diff_text):
    """Baris tambahan (maks. CUPLIKAN_MAKS) dari file kode pertama yang relevan pada diff."""
    for block in re.split(r"(?m)^diff --git ", diff_text or "")[1:]:
        m = re.match(r"a/(\S+) b/(\S+)", block)
        if not m:
            continue
        path = m.group(2)
        if not path.endswith(KODE_EXT) or any(s in path for s in SKIP_PATH):
            continue
        lines = []
        for line in block.splitlines():
            if line.startswith("+") and not line.startswith("+++") and line[1:].strip():
                line = line[1:].rstrip()
                lines.append(line[:PANJANG_MAKS] + " …" if len(line) > PANJANG_MAKS else line)
            if len(lines) >= CUPLIKAN_MAKS:
                break
        if lines:
            return path, lines
    return None, []


def build_lampiran_kode(config, prs, diffs):
    doc = _a4(Document())
    prs_by_num = {pr["number"]: pr for pr in prs}
    kit.heading2(doc, "Lampiran 2 – Kode Sumber & PR List")
    kit.body(doc, f"Bahasa Pemrograman\t: {config['tech']['language']}")
    kit.body(doc, f"Framework\t\t\t: {config['tech']['framework']}")
    kit.body(doc, f"Repositori\t\t\t: {config['tech']['repo_url']}")
    author = config["github"].get("author_display", config["github"]["author"])
    kit.body(doc, f"Daftar Pull Request Bulan {config['bulan']} {config['tahun']} (Author: {author}) — Total: {len(prs)} PR")

    baris = []
    for i, pr in enumerate(prs, 1):
        det = local_pr_detail(pr["number"], prs_by_num, diffs) or {}
        baris.append([str(i), f"#{pr['number']}", pr["title"], str(len(det.get("files", []))),
                      f"+{det.get('additions', 0)}/-{det.get('deletions', 0)}"])
    kit.simple_table(doc, ["No", "PR", "Judul", "File", "Baris"], baris,
                     widths=[Cm(1.0), Cm(1.4), Cm(10.6), Cm(1.2), Cm(2.2)], size=Pt(8))

    kit.body(doc, "")
    kit.body(doc, f"Cuplikan Kode Sumber (maksimal {CUPLIKAN_MAKS} baris tambahan per PR, diambil dari file kode utama)")
    for pr in prs:
        path, lines = _cuplikan_kode(diffs.get(str(pr["number"]), ""))
        if not lines:
            continue
        p = doc.add_paragraph()
        p.paragraph_format.space_before, p.paragraph_format.space_after = Pt(10), Pt(2)
        p.paragraph_format.keep_with_next = True
        kit.run(p, f"PR #{pr['number']}: {pr['title']}", bold=True, size=Pt(9))
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        kit.run(p, path, italic=True, size=Pt(8))
        for line in lines:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.left_indent = Pt(10)
            r = p.add_run(line)
            r.font.name = "Courier New"
            r.font.size = Pt(8)
    return doc


def build_lampiran_kegiatan(config, kegiatan, number):
    """Dokumentasi kegiatan tambahan: gambar (mis. Surat Tugas) lalu tabel rekap."""
    inp = input_dir(config["period"])
    items = [k for k in kegiatan if k.get("gambar") or k.get("tabel_file")]
    if not items:
        return None
    doc = _a4(Document())
    kit.heading2(doc, f"Lampiran {number} – Dokumentasi Kegiatan Tambahan")
    no_tabel = no_gambar = 0
    for j, act in enumerate(items):
        kit.heading3(doc, act["judul"], kit.letter(j))
        for g in act.get("gambar", []):
            path = inp / g["file"]
            if not path.exists():
                print("PERINGATAN: gambar lampiran tidak ditemukan:", path)
                continue
            no_gambar += 1
            kit.picture(doc, path)
            kit.caption(doc, f"Gambar {number}.{no_gambar}. {g['keterangan']}")
        if act.get("tabel_file"):
            path = inp / act["tabel_file"]
            if not path.exists():
                print("PERINGATAN: tabel lampiran tidak ditemukan:", path)
                continue
            for tbl in json.loads(path.read_text(encoding="utf-8")).get("tabel", []):
                no_tabel += 1
                cap = kit.caption(doc, f"Tabel {number}.{no_tabel}. {tbl['judul']}", bold=True, italic=False, before=12)
                cap.paragraph_format.space_after = Pt(0)
                cap.paragraph_format.keep_with_next = True
                kit.simple_table(doc, tbl["kolom"], tbl["baris"])
                if tbl.get("catatan"):
                    kit.run(doc.add_paragraph(), tbl["catatan"], italic=True, size=Pt(8))
    return doc


# ---------------------------------------------------------------------------
# Rangkai semuanya
# ---------------------------------------------------------------------------

def _new_section(master, src_doc):
    """Section baru (halaman baru) dengan ukuran & margin mengikuti dokumen sumber."""
    sect = master.add_section(WD_SECTION.NEW_PAGE)
    src = src_doc.sections[0]
    for attr in ("orientation", "page_width", "page_height",
                 "left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sect, attr, getattr(src, attr))
    return sect


def _save(composer, path):
    try:
        composer.save(str(path))
        return path
    except PermissionError:
        alt = path.with_name(path.stem + " _v2" + path.suffix)
        print(f"File sedang dibuka di Word, disimpan sebagai: {alt.name}")
        composer.save(str(alt))
        return alt


def build(config, force_fetch=False):
    period = config["period"]
    inp = input_dir(period)
    prs = load_prs(config, force=force_fetch)
    diffs = load_diffs(config, prs, force=force_fetch)
    modules = parse_detail_github(inp / "detail_github.md")
    kegiatan = load_kegiatan_tambahan(period)
    dok_kegiatan = build_lampiran_kegiatan(config, kegiatan, 3)

    main_path = build_main(config, prs, modules, kegiatan, "Lampiran 3" if dok_kegiatan else None)
    master = Document(str(main_path))
    composer = Composer(master)

    # Lampiran 1: weekly report (export manual bila ada, selain itu hasil `laporan.py weekly`)
    weekly = inp / f"{period}_Program dan Data Weekly Report.docx"
    if not weekly.exists():
        weekly = inp / "weekly_report.docx"
    if weekly.exists():
        dok_weekly = Document(str(weekly))
        _new_section(master, dok_weekly)
        kit.heading2(master, f"Lampiran 1 – Weekly Report {config['bulan']} {config['tahun']}")
        composer.append(dok_weekly)
    else:
        print(f"PERINGATAN: weekly report tidak ditemukan ({weekly.name}); jalankan: python laporan.py weekly {period}")

    # Lampiran 2: kode sumber; Lampiran 3: dokumentasi kegiatan tambahan
    for dok in (build_lampiran_kode(config, prs, diffs), dok_kegiatan):
        if dok is not None:
            _new_section(master, dok)
            composer.append(dok)

    out = _save(composer, main_path)
    print("Selesai:", out)
    print("Total PR:", len(prs))
    print("Buka di Word -> klik kanan Daftar Isi -> Update Field untuk nomor halaman.")
    return out

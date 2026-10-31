# -*- coding: utf-8 -*-
import zipfile
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.image.image import Image as DocxImage
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, Emu
import copy
import json
import re
from .config import input_dir, output_dir, template_dir, weekly_report_path
from .parser import load_kegiatan_tambahan, parse_detail_github, parse_weekly_report
from .pr_details import local_pr_detail

FONT = "Arial"
SIZE_BODY    = None   # inherit from Normal style
SIZE_HEADING = Pt(14)
SIZE_LAMPIRAN     = Pt(58)
SIZE_TABLE_CELL   = Pt(10)
LINE_SPACING      = 1.5   # 1.5 lines

# Indentasi format skripsi
INDENT_H2   = Cm(1.0)    # teks judul "2.1." mulai di sini
INDENT_H3   = Cm(1.75)   # teks judul "a." dan isi sub-kegiatan mulai di sini
INDENT_LIST = Cm(0.65)   # jarak penanda butir ke teks
FIRST_LINE  = Cm(1.0)    # indentasi baris pertama paragraf

def _set_line_spacing(pf, spacing=LINE_SPACING):
    pf.line_spacing = spacing

def _run(p, text, bold=False, size=None, italic=False):
    r = p.add_run(text)
    r.font.name = FONT
    r.bold = bold
    r.italic = italic
    if size:
        r.font.size = size
    return r

def enable_update_fields(doc):
    update = OxmlElement("w:updateFields")
    update.set(qn("w:val"), "true")
    doc.settings.element.append(update)


def add_page_numbers(doc):
    """Insert a centered PAGE field in the footer of every section.
    Cover page (first page of first section) is excluded via different_first_page.
    """
    for i, section in enumerate(doc.sections):
        if i == 0:
            # Cover: first page gets no page number
            section.different_first_page_header_footer = True
            # first_page_footer stays empty — no action needed

        footer = section.footer
        footer.is_linked_to_previous = False
        fp = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        fp.clear()
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _set_line_spacing(fp.paragraph_format)
        r = fp.add_run()
        r.font.name = FONT
        # PAGE field: begin
        fld_begin = OxmlElement("w:fldChar")
        fld_begin.set(qn("w:fldCharType"), "begin")
        r._r.append(fld_begin)
        # instruction
        instr = OxmlElement("w:instrText")
        instr.set(qn("xml:space"), "preserve")
        instr.text = " PAGE "
        r._r.append(instr)
        # PAGE field: end
        fld_end = OxmlElement("w:fldChar")
        fld_end.set(qn("w:fldCharType"), "end")
        r._r.append(fld_end)


def ensure_toc_styles(doc):
    """Style Daftar Isi ala skripsi: nomor menggantung, sub-judul menjorok di bawah teks induknya."""
    from docx.enum.style import WD_STYLE_TYPE
    from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER
    sec = doc.sections[0]
    text_width = sec.page_width - sec.left_margin - sec.right_margin
    for name, style_id, left, hang in (("toc 2", "TOC2", INDENT_H2, INDENT_H2),
                                       ("toc 3", "TOC3", INDENT_H3, INDENT_H3 - INDENT_H2)):
        try:
            style = doc.styles[name]
        except KeyError:
            style = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
            style.style_id = style_id
            style.base_style = doc.styles["Normal"]
            # Harus dikenali Word sebagai style bawaan, bukan kustom (agar tidak diganti nama "TOC 21")
            style.element.attrib.pop(qn("w:customStyle"), None)
        pf = style.paragraph_format
        pf.space_after = Pt(2)
        _hanging(pf, left, hang)
        pf.tab_stops.add_tab_stop(text_width, WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)

def add_toc(doc):
    """Inject a Word TOC field that auto-populates when opened in Word."""
    p = doc.add_paragraph()
    p.style = doc.styles["Normal"]
    _set_line_spacing(p.paragraph_format)
    r = p.add_run()
    # fldChar begin
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    r._r.append(fld_begin)
    # instrText
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = ' TOC \\o "1-3" \\h \\z \\u '
    r._r.append(instr)
    # fldChar separate
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    r._r.append(fld_sep)
    # fldChar end
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    r._r.append(fld_end)

def _hanging(pf, left, hang):
    """Indentasi gantung ala skripsi: nomor di kiri, teks (termasuk baris lanjutan) sejajar di `left`."""
    pf.left_indent = left
    pf.first_line_indent = -hang
    pf.tab_stops.add_tab_stop(left)

def add_body(doc, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=None, first_line=None):
    p = doc.add_paragraph()
    p.style = doc.styles["Normal"]
    p.alignment = align
    _set_line_spacing(p.paragraph_format)
    if indent is not None:
        p.paragraph_format.left_indent = indent
    if first_line is not None:
        p.paragraph_format.first_line_indent = first_line
    _run(p, text)
    return p

def add_list_item(doc, marker, text, indent):
    """Butir daftar bernomor/berbutir dengan teks sejajar setelah penanda."""
    p = doc.add_paragraph()
    p.style = doc.styles["Normal"]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    _set_line_spacing(p.paragraph_format)
    _hanging(p.paragraph_format, indent + INDENT_LIST, INDENT_LIST)
    _run(p, f"{marker}\t{text}")
    return p

def add_module_heading(doc, text, number=None):
    """Module/BAB heading — uses Heading 2 style so TOC picks it up."""
    p = doc.add_paragraph(style="Heading 2")
    _set_line_spacing(p.paragraph_format)
    if number:
        text = f"{number}\t{text}"
        _hanging(p.paragraph_format, INDENT_H2, INDENT_H2)
    # Clear existing runs from style and add our own
    for run in p.runs:
        run.text = ""
    r = p.add_run(text)
    r.font.name = FONT
    r.bold = True
    r.font.size = SIZE_HEADING
    return p

def add_activity_name(doc, text, letter=None):
    """Sub-activity name — uses Heading 3 style so TOC picks it up."""
    p = doc.add_paragraph(style="Heading 3")
    _set_line_spacing(p.paragraph_format)
    if letter:
        text = f"{letter}.\t{text}"
        _hanging(p.paragraph_format, INDENT_H3, INDENT_H3 - INDENT_H2)
    else:
        p.paragraph_format.left_indent = INDENT_H2
    for run in p.runs:
        run.text = ""
    r = p.add_run(text)
    r.font.name = FONT
    r.bold = False
    r.font.size = SIZE_HEADING
    return p

def add_lampiran_heading(doc):
    p = doc.add_paragraph()
    p.style = doc.styles["Normal"]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _set_line_spacing(p.paragraph_format)
    _run(p, "LAMPIRAN", bold=True, size=SIZE_LAMPIRAN)
    return p

# -------------------------------------------------------------------
# Activity table (2-col: label | content)
# -------------------------------------------------------------------

def _cell_run(cell, text, bold=False):
    for p in cell.paragraphs:
        for r in p.runs:
            r.clear()
    p = cell.paragraphs[0]
    _set_line_spacing(p.paragraph_format)
    r = p.add_run(text)
    r.font.name = FONT
    r.font.size = SIZE_TABLE_CELL
    r.bold = bold
    return r

def _add_cell_para(cell, text, bold=False, bullet=False):
    p = cell.add_paragraph()
    _set_line_spacing(p.paragraph_format)
    if bullet:
        _hanging(p.paragraph_format, Cm(0.45), Cm(0.45))
        text = f"•\t{text}"
    r = p.add_run(text)
    r.font.name = FONT
    r.font.size = SIZE_TABLE_CELL
    r.bold = bold
    return p

def _set_table_indent(table, indent):
    tbl_pr = table._tbl.tblPr
    tbl_ind = tbl_pr.find(qn("w:tblInd"))
    if tbl_ind is None:
        # Urutan elemen tblPr wajib sesuai skema: tblStyle, tblW, jc, tblInd, ...
        tbl_ind = OxmlElement("w:tblInd")
        anchor = tbl_pr.find(qn("w:jc"))
        if anchor is None:
            anchor = tbl_pr.find(qn("w:tblW"))
        if anchor is None:
            anchor = tbl_pr.find(qn("w:tblStyle"))
        if anchor is not None:
            anchor.addnext(tbl_ind)
        else:
            tbl_pr.insert(0, tbl_ind)
    tbl_ind.set(qn("w:w"), str(int(indent.twips)))
    tbl_ind.set(qn("w:type"), "dxa")

def add_activity_table(doc, activity):
    COL0_W = Emu(1028700)   # ~0.81 in
    COL1_W = Emu(5382260)   # ~4.24 in

    deskripsi_text = activity.get("deskripsi", "")
    files = activity.get("files", [])
    utama = activity.get("utama", [])
    manfaat = activity.get("manfaat", [])

    table = doc.add_table(rows=2, cols=2)
    table.style = "Table Grid"
    _set_table_indent(table, INDENT_H3)

    for row in table.rows:
        row.cells[0].width = COL0_W
        row.cells[1].width = COL1_W

    _cell_run(table.rows[0].cells[0], "Deskripsi Pekerjaan", bold=True)
    c1 = table.rows[0].cells[1]
    _cell_run(c1, deskripsi_text, bold=False)

    if files or utama or manfaat:
        _add_cell_para(c1, "", bold=False)
        _add_cell_para(c1, "Detail Perubahan", bold=True)
        if files:
            _add_cell_para(c1, "File yang Diubah:", bold=True)
            for f in files:
                # zero-width space setelah "/" agar path panjang bisa terpotong rapi di dalam sel
                _add_cell_para(c1, f.replace("/", "/​"), bullet=True)
        if utama:
            _add_cell_para(c1, "Perubahan Utama:", bold=True)
            for u in utama:
                _add_cell_para(c1, u, bullet=True)
        if manfaat:
            _add_cell_para(c1, "Manfaat:", bold=True)
            for m in manfaat:
                _add_cell_para(c1, m, bullet=True)

    _cell_run(table.rows[1].cells[0], "Dokumentasi", bold=True)
    docs = activity.get("docs", [])
    c1_dok = table.rows[1].cells[1]
    if docs:
        _cell_run(c1_dok, docs[0], bold=False)
        for d in docs[1:]:
            _add_cell_para(c1_dok, d)
    else:
        _cell_run(c1_dok, "-", bold=False)

    doc.add_paragraph()  # spacer after table

# -------------------------------------------------------------------
# Builders for BAB II and Lampiran
# -------------------------------------------------------------------

def get_letter(num):
    import string
    res = ""
    while num >= 0:
        res = string.ascii_lowercase[num % 26] + res
        num = num // 26 - 1
    return res

def build_bab2(doc, modules):
    for i, mod in enumerate(modules, 1):
        add_module_heading(doc, mod["title"], number=f"2.{i}.")
        if mod["intro"]:
            add_body(doc, mod["intro"], indent=INDENT_H2, first_line=FIRST_LINE)
        for j, act in enumerate(mod["activities"]):
            add_activity_name(doc, act["subtitle"], letter=get_letter(j))
            if act["prolog"]:
                add_body(doc, act["prolog"], indent=INDENT_H3, first_line=FIRST_LINE)
            add_activity_table(doc, act)

def build_kegiatan_tambahan(doc, kegiatan, number=None, lampiran_label=None):
    if not kegiatan:
        return
    add_module_heading(doc, "Kegiatan Tambahan", number=number)
    for j, act in enumerate(kegiatan):
        add_activity_name(doc, act["judul"], letter=get_letter(j))
        if act.get("pembuka"):
            add_body(doc, act["pembuka"], indent=INDENT_H3, first_line=FIRST_LINE)
        for k, bagian in enumerate(act.get("bagian", []), 1):
            # Sub-bagian bernomor 1), 2), ... dengan butir a., b., ... di bawahnya
            add_list_item(doc, f"{k})", bagian["judul"], INDENT_H3)
            for m, poin in enumerate(bagian.get("poin", [])):
                add_list_item(doc, f"{get_letter(m)}.", poin, INDENT_H3 + INDENT_LIST)
        if act.get("deskripsi") or act.get("docs"):
            add_activity_table(doc, act)
        if lampiran_label and (act.get("gambar") or act.get("tabel_file")):
            add_body(
                doc,
                f"Data pendukung dan dokumentasi kegiatan ini disajikan pada {lampiran_label}.",
                indent=INDENT_H3, first_line=FIRST_LINE,
            )

def ensure_media(media_dir, template_path):
    if media_dir.exists() and any(media_dir.iterdir()):
        return
    media_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(template_path) as z:
        for name in z.namelist():
            if name.startswith("word/media/"):
                (media_dir / name.split("/")[-1]).write_bytes(z.read(name))

def add_image_if_exists(doc, media_dir, name, width=Inches(6.0)):
    path = media_dir / name
    if path.exists():
        doc.add_picture(str(path), width=width)
        return True
    return False

def build_manajemen_kode(doc, config, prs, media_dir, number=None):
    add_module_heading(doc, "Manajemen Kode Sumber", number=number)
    bulan = config.get("bulan", "")
    tahun = config.get("tahun", "")
    repo = config["github"]["repo"]
    author = config["github"]["author"]

    add_activity_name(doc, f"Sinkronisasi Kode Sumber pada Repositori Github {bulan} {tahun}", letter="a")
    add_body(doc, f"Pada bulan {bulan} {tahun} dilakukan {len(prs)} pull request (author: {author}) di https://github.com/{repo}.",
             indent=INDENT_H3, first_line=FIRST_LINE)

    if not add_image_if_exists(doc, media_dir, "image3.jpeg", width=Inches(6.0)):
        add_body(doc, "[Screenshot GitHub terlampir]", indent=INDENT_H3)

    add_activity_name(doc, f"Sinkronisasi Kode Sumber pada Server Development {bulan} {tahun}", letter="b")
    add_body(doc, "Sinkronisasi kode sumber API ke server development setelah perubahan di-merge.",
             indent=INDENT_H3, first_line=FIRST_LINE)
    if not add_image_if_exists(doc, media_dir, "image4.jpeg", width=Inches(6.0)):
        add_body(doc, "[Screenshot server terlampir]", indent=INDENT_H3)

# -------------------------------------------------------------------
# Lampiran
# -------------------------------------------------------------------

def _simple_table(doc, kolom, baris, widths=None, size=Pt(9)):
    """Tabel rekap sederhana: baris judul tebal, angka rata kanan."""
    table = doc.add_table(rows=1, cols=len(kolom))
    table.style = "Table Grid"
    table.alignment = 1  # center
    for idx, judul in enumerate(kolom):
        p = table.rows[0].cells[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(str(judul))
        r.bold = True
        r.font.name = FONT
        r.font.size = size
    for row_vals in baris:
        cells = table.add_row().cells
        for idx, val in enumerate(row_vals[:len(kolom)]):
            val = str(val)
            p = cells[idx].paragraphs[0]
            if re.fullmatch(r"[+\-#]?[\d.,%/ +\-]+", val.strip() or "x"):
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if idx else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = FONT
            r.font.size = size
    if widths:
        for row in table.rows:
            for idx, w in enumerate(widths):
                row.cells[idx].width = w
    return table

def _caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(12)
    _run(p, text, italic=True, size=Pt(10))
    return p

def _set_a4(doc):
    """Lampiran tegak memakai A4 seperti badan laporan."""
    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21.0), Cm(29.7)
    s.left_margin = s.right_margin = Cm(2.0)
    s.top_margin = s.bottom_margin = Cm(2.0)

def build_lampiran_kegiatan(config, kegiatan, number):
    """Lampiran dokumentasi kegiatan tambahan: tabel rekap dan gambar."""
    inp = input_dir(config["period"])
    items = [k for k in kegiatan if k.get("gambar") or k.get("tabel_file")]
    if not items:
        return None
    doc = Document()
    _set_a4(doc)
    add_module_heading(doc, f"Lampiran {number} – Dokumentasi Kegiatan Tambahan")
    no_tabel = no_gambar = 0
    for j, act in enumerate(items):
        add_activity_name(doc, act["judul"], letter=get_letter(j))
        # Gambar (mis. Surat Tugas) ditampilkan lebih dulu, lalu tabel rekap
        for g in act.get("gambar", []):
            path = inp / g["file"]
            if not path.exists():
                print("WARNING: gambar lampiran tidak ditemukan:", path)
                continue
            no_gambar += 1
            img = DocxImage.from_file(str(path))
            if img.px_height > img.px_width:
                doc.add_picture(str(path), height=Cm(19))  # halaman dokumen tegak (surat)
            else:
                doc.add_picture(str(path), width=Cm(16))
            pic_p = doc.paragraphs[-1]
            pic_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pic_p.paragraph_format.space_before = Pt(12)
            pic_p.paragraph_format.keep_with_next = True
            _caption(doc, f"Gambar {number}.{no_gambar}. {g['keterangan']}")
        tabel_path = inp / act["tabel_file"] if act.get("tabel_file") else None
        if tabel_path and tabel_path.exists():
            for tbl in json.loads(tabel_path.read_text(encoding="utf-8")).get("tabel", []):
                no_tabel += 1
                cap = doc.add_paragraph()
                cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cap.paragraph_format.space_before = Pt(12)
                cap.paragraph_format.keep_with_next = True
                _run(cap, f"Tabel {number}.{no_tabel}. {tbl['judul']}", bold=True, size=Pt(10))
                _simple_table(doc, tbl["kolom"], tbl["baris"])
                if tbl.get("catatan"):
                    note = doc.add_paragraph()
                    _run(note, tbl["catatan"], italic=True, size=Pt(8))
        elif tabel_path:
            print("WARNING: tabel lampiran tidak ditemukan:", tabel_path)

    base_name = config["output_filename"].replace(".docx", "")
    output_path = output_dir(config["period"]) / f"{base_name} - Lampiran Kegiatan.docx"
    doc.save(str(output_path))
    return output_path

KODE_EXT = (".php", ".py", ".js", ".ts", ".sql", ".sh", ".yml", ".yaml", ".conf")
SKIP_PATH = ("docs/", "public/", "storage/", "tests/", "Tests/", "lang/", "composer.lock", "package-lock")
CUPLIKAN_MAKS = 12
PANJANG_MAKS = 110

def _cuplikan_kode(diff_text):
    """Ambil cuplikan singkat (baris tambahan) dari file kode pertama yang relevan pada diff."""
    blocks = re.split(r"(?m)^diff --git ", diff_text or "")
    for block in blocks[1:]:
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
                if len(line) > PANJANG_MAKS:
                    line = line[:PANJANG_MAKS] + " …"
                lines.append(line)
            if len(lines) >= CUPLIKAN_MAKS:
                break
        if lines:
            return path, lines
    return None, []

def build_diff_document(config, prs, diffs):
    doc = Document()
    _set_a4(doc)
    bulan = config.get("bulan", "")
    tahun = config.get("tahun", "")
    prs_by_num = {pr["number"]: pr for pr in prs}

    add_module_heading(doc, "Lampiran 2 – Kode Sumber & PR List")
    add_body(doc, f"Bahasa Pemrograman\t: {config['tech']['language']}")
    add_body(doc, f"Framework\t\t\t: {config['tech']['framework']}")
    add_body(doc, f"Repositori\t\t\t: {config['tech']['repo_url']}")

    author_str = config['github'].get('author_display', config['github']['author'])
    add_body(doc, f"Daftar Pull Request Bulan {bulan} {tahun} (Author: {author_str}) — Total: {len(prs)} PR")

    # 1. Tabel ringkas seluruh PR
    baris = []
    for i, pr in enumerate(prs, 1):
        det = local_pr_detail(pr["number"], prs_by_num, diffs) or {}
        baris.append([
            str(i), f"#{pr['number']}", pr["title"],
            str(len(det.get("files", []))),
            f"+{det.get('additions', 0)}/-{det.get('deletions', 0)}",
        ])
    _simple_table(doc, ["No", "PR", "Judul", "File", "Baris"], baris,
                  widths=[Cm(1.0), Cm(1.4), Cm(10.6), Cm(1.2), Cm(2.2)], size=Pt(8))

    # 2. Cuplikan kode singkat per PR (hanya file kode, maks. CUPLIKAN_MAKS baris)
    add_body(doc, "")
    add_body(doc, f"Cuplikan Kode Sumber (maksimal {CUPLIKAN_MAKS} baris tambahan per PR, diambil dari file kode utama)")
    for pr in prs:
        path, lines = _cuplikan_kode(diffs.get(str(pr["number"]), ""))
        if not lines:
            continue
        title_p = doc.add_paragraph()
        title_p.paragraph_format.space_before = Pt(10)
        title_p.paragraph_format.space_after = Pt(2)
        title_p.paragraph_format.keep_with_next = True
        _run(title_p, f"PR #{pr['number']}: {pr['title']}", bold=True, size=Pt(9))
        file_p = doc.add_paragraph()
        file_p.paragraph_format.space_after = Pt(2)
        file_p.paragraph_format.keep_with_next = True
        _run(file_p, path, italic=True, size=Pt(8))
        for line in lines:
            diff_p = doc.add_paragraph()
            diff_p.paragraph_format.space_after = Pt(0)
            diff_p.paragraph_format.line_spacing = 1.0
            diff_p.paragraph_format.left_indent = Pt(10)
            diff_r = diff_p.add_run(line)
            diff_r.font.name = "Courier New"
            diff_r.font.size = Pt(8)

    # Save the document
    output_dir_path = output_dir(config["period"])
    base_name = config["output_filename"].replace(".docx", "")
    output_path = output_dir_path / f"{base_name} - Lampiran Diff.docx"
    doc.save(str(output_path))
    return output_path

# -------------------------------------------------------------------
# The Core Splicing engine
# -------------------------------------------------------------------
def splice_elements(marker_p, builder_funcs, args_list):
    temp_doc = Document()
    for func, args in zip(builder_funcs, args_list):
        func(temp_doc, *args)
    
    curr = marker_p._element
    for el in temp_doc.element.body:
        if el.tag.endswith('sectPr'): continue
        new_el = copy.deepcopy(el)
        curr.addnext(new_el)
        curr = new_el
    marker_p._element.getparent().remove(marker_p._element)

def build_report(config, prs, diffs=None):
    if diffs is None:
        diffs = {}
    period   = config["period"]
    inp, tpl = input_dir(period), template_dir()
    media_dir    = tpl / "media"
    template_path = tpl / "laporan_template.docx"
    output_path  = output_dir(period) / config["output_filename"]

    ensure_media(media_dir, template_path)
    modules      = parse_detail_github(inp / "detail_github.md") if (inp / "detail_github.md").exists() else []
    weekly_rows  = parse_weekly_report(
        weekly_report_path(period), 
        config.get("weekly_user_filter", "Lutfi"),
        repo_filter=config.get("github", {}).get("repo")
    )
    kegiatan     = load_kegiatan_tambahan(inp / "kegiatan_tambahan.json")

    doc = Document(str(template_path))
    enable_update_fields(doc)
    ensure_toc_styles(doc)

    # Simple placeholder replacement on the original doc template
    bulan_up = config.get('bulan_up', config['bulan'].upper())
    replacements = {
        '{{ BAB1_PENCAPAIAN }}': config.get('bab1', {}).get('pencapaian', ''),
        '{{ BAB1_TANTANGAN }}': config.get('bab1', {}).get('tantangan', ''),
    }
    # BAB 3 Kesimpulan is a list, join them with newlines
    kesimpulan = "\n".join(config.get('bab3', {}).get('kesimpulan_items', []))
    replacements['{{ BAB3_KESIMPULAN }}'] = kesimpulan
    
    for p in doc.paragraphs:
        # 1. Apply Heading 1 to BAB headings so they enter TOC
        p_text_stripped = p.text.strip()
        if p_text_stripped in ["BAB I", "PENDAHULUAN", "BAB II", "HASIL KEGIATAN", "BAB III", "PENUTUP"]:
            p.style = "Heading 1"

        # 2. Handle template placeholders
        for old_t, new_t in replacements.items():
            if old_t in p.text:
                for r in p.runs:
                    if old_t in r.text:
                        r.text = r.text.replace(old_t, new_t)
                        
        # 3. Handle split-run month replacements (Mei -> config['bulan'])
        if 'Mei' in p.text or 'MEI' in p.text:
            for r in p.runs:
                if 'Mei' in r.text:
                    r.text = r.text.replace('Mei', config['bulan'])
                if 'MEI' in r.text:
                    r.text = r.text.replace('MEI', bulan_up)
            # Template memisahkan "Mei" dan "2026" pada run berbeda tanpa spasi
            runs = p.runs
            for r, nxt in zip(runs, runs[1:]):
                if r.text.endswith(config['bulan']) and nxt.text[:1].isdigit():
                    r.text += " "

    toc_p = None
    bab2_p = None
    lampiran_p = None
    kata_pengantar_p = None
    for p in doc.paragraphs:
        if '{{ TOC }}' in p.text: toc_p = p
        if '{{ BAB2 }}' in p.text: bab2_p = p
        if '{{ LAMPIRAN }}' in p.text: lampiran_p = p
        if 'Kata Pengantar' == p.text.strip() and kata_pengantar_p is None:
            kata_pengantar_p = p

    # Inject TOC: if explicit marker found use it, else inject before Kata Pengantar
    if toc_p:
        splice_elements(toc_p, [add_toc], [()])
    elif kata_pengantar_p is not None:
        curr = kata_pengantar_p._element
        temp_doc = Document()
        # DAFTAR ISI heading + TOC field — NO leading page break,
        # template already provides natural page boundary before Kata Pengantar
        # Reuse the default empty paragraph Document() always creates,
        # instead of add_paragraph() which would create a second blank para
        # that becomes a blank page when injected.
        h_p = temp_doc.paragraphs[0] if temp_doc.paragraphs else temp_doc.add_paragraph()
        h_p.style = temp_doc.styles["Normal"]
        h_r = h_p.add_run("DAFTAR ISI")
        h_r.font.name = FONT
        h_r.bold = True
        h_r.font.size = SIZE_HEADING
        _set_line_spacing(h_p.paragraph_format)
        # TOC field
        add_toc(temp_doc)
        # Page break AFTER TOC so Kata Pengantar starts on new page
        pb2_p = temp_doc.add_paragraph()
        pb2_p.style = temp_doc.styles["Normal"]
        br2 = OxmlElement("w:br")
        br2.set(qn("w:type"), "page")
        pb2_p._p.append(br2)
        # Insert before kata_pengantar_p
        for el in temp_doc.element.body:
            if el.tag.endswith('sectPr'): continue
            new_el = copy.deepcopy(el)
            curr.addprevious(new_el)


    if bab2_p:
        n = len(modules)
        lampiran_label = "Lampiran 3" if any(k.get("gambar") or k.get("tabel_file") for k in kegiatan) else None
        splice_elements(
            bab2_p,
            [build_bab2, build_manajemen_kode, build_kegiatan_tambahan],
            [(modules,), (config, prs, media_dir, f"2.{n + 1}."), (kegiatan, f"2.{n + 2}.", lampiran_label)],
        )

    if lampiran_p:
        # Delete the {{ LAMPIRAN }} marker, as we will append the lampiran using docxcompose
        lampiran_p._element.getparent().remove(lampiran_p._element)

    add_page_numbers(doc)
    doc.save(str(output_path))
    return output_path


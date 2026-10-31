# -*- coding: utf-8 -*-
"""Helper format Word ala skripsi: heading bernomor, butir menggantung, tabel, field, dan gambar."""
import re
import string

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.image.image import Image as DocxImage
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

FONT = "Arial"
SIZE_HEADING = Pt(14)
SIZE_TABLE_CELL = Pt(10)
LINE_SPACING = 1.5

# Indentasi format skripsi
INDENT_H2 = Cm(1.0)    # teks judul "2.1." mulai di sini
INDENT_H3 = Cm(1.75)   # teks judul "a." dan isi sub-kegiatan mulai di sini
INDENT_LIST = Cm(0.65)  # jarak penanda butir ke teks
FIRST_LINE = Cm(1.0)    # indentasi baris pertama paragraf


def letter(num):
    """0 -> a, 25 -> z, 26 -> aa, ..."""
    res = ""
    while num >= 0:
        res = string.ascii_lowercase[num % 26] + res
        num = num // 26 - 1
    return res


def run(p, text, bold=False, size=None, italic=False):
    r = p.add_run(text)
    r.font.name = FONT
    r.bold = bold
    r.italic = italic
    if size:
        r.font.size = size
    return r


def hanging(pf, left, hang):
    """Indentasi gantung: penanda di kiri, teks (termasuk baris lanjutan) sejajar di `left`."""
    pf.left_indent = left
    pf.first_line_indent = -hang
    pf.tab_stops.add_tab_stop(left)


def body(doc, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=None, first_line=None):
    p = doc.add_paragraph(style="Normal")
    p.alignment = align
    p.paragraph_format.line_spacing = LINE_SPACING
    if indent is not None:
        p.paragraph_format.left_indent = indent
    if first_line is not None:
        p.paragraph_format.first_line_indent = first_line
    run(p, text)
    return p


def list_item(doc, marker, text, indent):
    p = doc.add_paragraph(style="Normal")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = LINE_SPACING
    hanging(p.paragraph_format, indent + INDENT_LIST, INDENT_LIST)
    run(p, f"{marker}\t{text}")
    return p


def heading2(doc, text, number=None):
    """Judul modul (Heading 2, masuk Daftar Isi)."""
    p = doc.add_paragraph(style="Heading 2")
    p.paragraph_format.line_spacing = LINE_SPACING
    if number:
        text = f"{number}\t{text}"
        hanging(p.paragraph_format, INDENT_H2, INDENT_H2)
    run(p, text, bold=True, size=SIZE_HEADING)
    return p


def heading3(doc, text, letter_=None):
    """Judul sub-kegiatan (Heading 3, masuk Daftar Isi)."""
    p = doc.add_paragraph(style="Heading 3")
    p.paragraph_format.line_spacing = LINE_SPACING
    if letter_:
        text = f"{letter_}.\t{text}"
        hanging(p.paragraph_format, INDENT_H3, INDENT_H3 - INDENT_H2)
    else:
        p.paragraph_format.left_indent = INDENT_H2
    run(p, text, size=SIZE_HEADING)
    return p


def caption(doc, text, bold=False, italic=True, before=0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(12)
    run(p, text, bold=bold, italic=italic, size=Pt(10))
    return p


def picture(doc, path, max_width=Cm(16), portrait_height=Cm(19)):
    """Gambar di tengah; gambar tegak (mis. halaman surat) dibatasi tingginya."""
    img = DocxImage.from_file(str(path))
    if img.px_height > img.px_width:
        doc.add_picture(str(path), height=portrait_height)
    else:
        doc.add_picture(str(path), width=max_width)
    p = doc.paragraphs[-1]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.keep_with_next = True
    return p


def page_break(doc):
    p = doc.add_paragraph(style="Normal")
    br = OxmlElement("w:br")
    br.set(qn("w:type"), "page")
    p._p.append(br)
    return p


# ---------------------------------------------------------------------------
# Tabel
# ---------------------------------------------------------------------------

def table_indent(table, indent):
    tbl_pr = table._tbl.tblPr
    tbl_ind = tbl_pr.find(qn("w:tblInd"))
    if tbl_ind is None:
        # Urutan elemen tblPr wajib sesuai skema: tblStyle, tblW, jc, tblInd, ...
        tbl_ind = OxmlElement("w:tblInd")
        anchor = next((tbl_pr.find(qn(t)) for t in ("w:jc", "w:tblW", "w:tblStyle")
                       if tbl_pr.find(qn(t)) is not None), None)
        if anchor is not None:
            anchor.addnext(tbl_ind)
        else:
            tbl_pr.insert(0, tbl_ind)
    tbl_ind.set(qn("w:w"), str(int(indent.twips)))
    tbl_ind.set(qn("w:type"), "dxa")


def _cell_text(cell, text, bold=False):
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = LINE_SPACING
    r = run(p, text, bold=bold, size=SIZE_TABLE_CELL)
    return r


def _cell_para(cell, text, bold=False, bullet=False):
    p = cell.add_paragraph()
    p.paragraph_format.line_spacing = LINE_SPACING
    if bullet:
        hanging(p.paragraph_format, Cm(0.45), Cm(0.45))
        text = f"•\t{text}"
    run(p, text, bold=bold, size=SIZE_TABLE_CELL)
    return p


def activity_table(doc, act):
    """Tabel 2 kolom sub-kegiatan: Deskripsi Pekerjaan (+ Detail Perubahan) dan Dokumentasi."""
    table = doc.add_table(rows=2, cols=2)
    table.style = "Table Grid"
    table_indent(table, INDENT_H3)
    for row in table.rows:
        # Lebar total = lebar teks (18,46 cm) dikurangi indentasi INDENT_H3
        row.cells[0].width = Cm(2.6)
        row.cells[1].width = Cm(14.1)

    _cell_text(table.rows[0].cells[0], "Deskripsi Pekerjaan", bold=True)
    desc = table.rows[0].cells[1]
    _cell_text(desc, act.get("deskripsi", ""))
    files, utama, manfaat = act.get("files", []), act.get("utama", []), act.get("manfaat", [])
    if files or utama or manfaat:
        _cell_para(desc, "")
        _cell_para(desc, "Detail Perubahan", bold=True)
        for label, items in (("File yang Diubah:", files), ("Perubahan Utama:", utama), ("Manfaat:", manfaat)):
            if not items:
                continue
            _cell_para(desc, label, bold=True)
            for item in items:
                if label.startswith("File"):
                    # zero-width space setelah "/" agar path panjang terpotong rapi di dalam sel
                    item = item.replace("/", "/​")
                _cell_para(desc, item, bullet=True)

    _cell_text(table.rows[1].cells[0], "Dokumentasi", bold=True)
    docs = act.get("docs") or ["-"]
    dok = table.rows[1].cells[1]
    _cell_text(dok, docs[0])
    for d in docs[1:]:
        _cell_para(dok, d)
    doc.add_paragraph()  # jarak setelah tabel
    return table


def simple_table(doc, kolom, baris, widths=None, size=Pt(9)):
    """Tabel rekap: baris judul tebal, angka rata kanan."""
    table = doc.add_table(rows=1, cols=len(kolom))
    table.style = "Table Grid"
    table.alignment = 1  # tengah
    for idx, judul in enumerate(kolom):
        p = table.rows[0].cells[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run(p, str(judul), bold=True, size=size)
    for row_vals in baris:
        cells = table.add_row().cells
        for idx, val in enumerate(row_vals[:len(kolom)]):
            val = str(val)
            p = cells[idx].paragraphs[0]
            if re.fullmatch(r"[+\-#]?[\d.,%/ +\-]+", val.strip() or "x"):
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if idx else WD_ALIGN_PARAGRAPH.CENTER
            run(p, val, size=size)
    if widths:
        for row in table.rows:
            for idx, w in enumerate(widths):
                row.cells[idx].width = w
    return table


# ---------------------------------------------------------------------------
# Field, footer, dan penyisipan konten di posisi marker
# ---------------------------------------------------------------------------

def _field(run_, instr_text):
    for kind, text in (("begin", None), (None, instr_text), ("separate", None), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run_._r.append(el)


def toc_field(doc):
    p = doc.add_paragraph(style="Normal")
    _field(p.add_run(), ' TOC \\o "1-3" \\h \\z \\u ')
    return p


def enable_update_fields(doc):
    update = OxmlElement("w:updateFields")
    update.set(qn("w:val"), "true")
    doc.settings.element.append(update)


def add_page_numbers(doc):
    """Nomor halaman di tengah footer; halaman sampul tanpa nomor."""
    for i, section in enumerate(doc.sections):
        if i == 0:
            section.different_first_page_header_footer = True
        footer = section.footer
        footer.is_linked_to_previous = False
        fp = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        fp.clear()
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = fp.add_run()
        r.font.name = FONT
        _field(r, " PAGE ")


def insert_at(doc, marker_p, builders):
    """Jalankan builder (yang menambah konten di akhir dokumen) lalu pindahkan hasilnya ke posisi marker.

    Konten dibangun langsung di dokumen tujuan sehingga gambar & style tetap terhubung.
    """
    body_el = doc.element.body
    # Simpan referensi elemen (bukan id()): proxy lxml bisa dibuat ulang sehingga id() tidak stabil
    before = set(body_el)
    for func, args in builders:
        func(doc, *args)
    new = [el for el in body_el if el not in before and not el.tag.endswith("sectPr")]
    anchor = marker_p._element
    for el in new:
        anchor.addnext(el)
        anchor = el
    marker_p._element.getparent().remove(marker_p._element)


def replace_text(paragraph, old, new):
    """Ganti teks walau terpecah di beberapa run (format run pertama dipertahankan)."""
    if old not in paragraph.text:
        return False
    for r in paragraph.runs:
        if old in r.text:
            r.text = r.text.replace(old, new)
            return True
    full = paragraph.text.replace(old, new)
    for i, r in enumerate(paragraph.runs):
        r.text = full if i == 0 else ""
    return True

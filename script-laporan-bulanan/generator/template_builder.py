# -*- coding: utf-8 -*-
"""Bangun template Word yang bersih (template/*.docx) dari sumber asli di archive/template_lama/.

Template laporan memakai marker:
  {{ BULAN }} {{ BULAN_UP }} {{ TAHUN }}          — nama bulan & tahun
  {{ TOC }}                                       — Daftar Isi
  {{ BAB1_PENCAPAIAN }} {{ BAB1_TANTANGAN }}      — paragraf BAB I
  {{ BAB2 }}                                      — seluruh isi BAB II
  {{ BAB3_KESIMPULAN }}                           — butir kesimpulan BAB III (diperbanyak otomatis)
  {{ LAMPIRAN }}                                  — posisi lampiran (dihapus; lampiran digabung di akhir)
Template weekly memakai marker {{ PERIODE }} dan tabel berisi baris judul saja.
"""
import copy
import re

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from docx.text.paragraph import Paragraph

from . import docx_kit as kit
from .config import ROOT, TEMPLATE_DIR
from .weekly import COL_WIDTHS

SOURCE_DIR = ROOT / "archive" / "template_lama"
BAB_HEADINGS = {"BAB I", "PENDAHULUAN", "BAB II", "HASIL KEGIATAN", "BAB III", "PENUTUP"}


def _set_text(p, text):
    for i, r in enumerate(p.runs):
        r.text = text if i == 0 else ""


def _new_paragraph_before(p, text="", bold=False, size=None):
    el = OxmlElement("w:p")
    p._p.addprevious(el)
    new = Paragraph(el, p._parent)
    if text:
        kit.run(new, text, bold=bold, size=size)
    return new


def _add_builtin_styles(doc):
    """Tambahkan style 'Table Grid' serta 'toc 2'/'toc 3' (format skripsi) ke template."""
    if "Table Grid" not in [s.name for s in doc.styles]:
        src = Document().styles["Table Grid"].element
        doc.styles.element.append(copy.deepcopy(src))

    sec = doc.sections[0]
    text_width = sec.page_width - sec.left_margin - sec.right_margin
    for name, style_id, left, hang in (("toc 2", "TOC2", kit.INDENT_H2, kit.INDENT_H2),
                                       ("toc 3", "TOC3", kit.INDENT_H3, kit.INDENT_H3 - kit.INDENT_H2)):
        names = [s.name for s in doc.styles]
        if name in names:
            style = doc.styles[name]
        else:
            style = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
            style.style_id = style_id
            style.base_style = doc.styles["Normal"]
            # Harus dikenali Word sebagai style bawaan (bukan kustom) agar tidak diganti nama "TOC 21"
            style.element.attrib.pop(qn("w:customStyle"), None)
        pf = style.paragraph_format
        pf.space_after = Pt(2)
        kit.hanging(pf, left, hang)
        pf.tab_stops.add_tab_stop(text_width, WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)


def _fix_penomoran_bab3(doc):
    """Sub-judul BAB III (Kesimpulan, Saran) harus bernomor 3.1, 3.2 — template asli mulai dari 2."""
    kesimpulan = next(p for p in doc.paragraphs if p.text.strip() == "Kesimpulan")
    num_id = kesimpulan._p.pPr.numPr.numId.val
    numbering = doc.part.numbering_part.element
    num = next(n for n in numbering.findall(qn("w:num")) if n.get(qn("w:numId")) == str(num_id))
    abstract_id = num.find(qn("w:abstractNumId")).get(qn("w:val"))
    abstract = next(a for a in numbering.findall(qn("w:abstractNum")) if a.get(qn("w:abstractNumId")) == abstract_id)
    lvl0 = next(l for l in abstract.findall(qn("w:lvl")) if l.get(qn("w:ilvl")) == "0")
    lvl0.find(qn("w:start")).set(qn("w:val"), "3")


def build_laporan_template():
    doc = Document(str(SOURCE_DIR / "laporan_template.docx"))
    paragraphs = list(doc.paragraphs)
    hapus = []
    in_kesimpulan = False

    for p in paragraphs:
        text = p.text
        stripped = text.strip()

        if stripped in BAB_HEADINGS:
            p.style = "Heading 1"
        if stripped.startswith("{{ BAB1_"):
            for r in p.runs:  # run marker asli tanpa font -> tampil serif
                r.font.name = kit.FONT
        if stripped == "2026":  # tahun di sampul
            _set_text(p, "{{ TAHUN }}")
        if re.search(r"Mei|MEI|Teknsi", text):
            baru = re.sub(r"MEI\s*2026", "{{ BULAN_UP }} {{ TAHUN }}", text)
            baru = re.sub(r"Mei\s*2026", "{{ BULAN }} {{ TAHUN }}", baru)
            baru = re.sub(r"\bMei\b", "{{ BULAN }}", baru).replace("Teknsi", "Teknis")
            _set_text(p, baru)

        # Daftar Isi tepat sebelum Kata Pengantar, diakhiri pindah halaman
        if stripped == "Kata Pengantar":
            judul = _new_paragraph_before(p, "DAFTAR ISI", bold=True, size=kit.SIZE_HEADING)
            judul.paragraph_format.line_spacing = kit.LINE_SPACING
            _new_paragraph_before(p, "{{ TOC }}")
            brk = _new_paragraph_before(p)
            br = OxmlElement("w:br")
            br.set(qn("w:type"), "page")
            brk._p.append(OxmlElement("w:r"))
            brk._p[-1].append(br)

        # BAB III: sisakan satu butir marker, buang daftar modul lama
        if "{{ BAB3_KESIMPULAN }}" in text:
            in_kesimpulan = True
            continue
        if in_kesimpulan:
            if p.style.name == "List Paragraph":
                hapus.append(p)
            else:
                in_kesimpulan = False

    for p in hapus:
        p._element.getparent().remove(p._element)

    _fix_penomoran_bab3(doc)
    _add_builtin_styles(doc)
    out = TEMPLATE_DIR / "laporan_template.docx"
    doc.save(str(out))
    return out


def build_weekly_template():
    doc = Document(str(SOURCE_DIR / "weekly_report_template.docx"))

    section = doc.sections[0]
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width, section.page_height = Cm(29.7), Cm(21.0)
    section.left_margin = section.right_margin = Cm(1.8)
    section.top_margin = section.bottom_margin = Cm(1.5)

    for p in doc.paragraphs:
        if "LOG Book" in p.text:
            _set_text(p, "Log Book Aktivitas Personil Timja Program dan Data")
            el = OxmlElement("w:p")
            p._p.addnext(el)
            periode = Paragraph(el, p._parent)
            periode.alignment = WD_ALIGN_PARAGRAPH.CENTER
            kit.run(periode, "Periode: {{ PERIODE }}", size=Pt(10))
        elif p.text.strip() == "Pic: Data":
            _set_text(p, "PIC: Data")

    table = doc.tables[0]
    while len(table.rows) > 1:
        table._tbl.remove(table.rows[-1]._tr)
    table.autofit = False

    # Posisi tabel: tanpa indentasi negatif, di tengah halaman
    tbl_pr = table._tbl.tblPr
    total = int(sum(Cm(w).twips for w in COL_WIDTHS))
    for tag, attrs in (("w:tblW", {"w:w": str(total), "w:type": "dxa"}),
                       ("w:jc", {"w:val": "center"}),
                       ("w:tblInd", {"w:w": "0", "w:type": "dxa"})):
        el = tbl_pr.find(qn(tag))
        if el is not None:
            for k, v in attrs.items():
                el.set(qn(k), v)
    grid = table._tbl.tblGrid
    for col, w in zip(grid.findall(qn("w:gridCol")), COL_WIDTHS):
        col.set(qn("w:w"), str(int(Cm(w).twips)))
    for change in grid.findall(qn("w:tblGridChange")):
        grid.remove(change)

    header = table.rows[0]
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    header._tr.get_or_add_trPr().append(tbl_header)
    for idx, cell in enumerate(header.cells):
        cell.width = Cm(COL_WIDTHS[idx])
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        for r in p.runs:
            r.font.size = Pt(7.5)
            r.font.name = "Arial"
            r.bold = True

    out = TEMPLATE_DIR / "weekly_report_template.docx"
    doc.save(str(out))
    return out


def build_all():
    return [build_laporan_template(), build_weekly_template()]

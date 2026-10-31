# -*- coding: utf-8 -*-
"""Generate weekly_report.docx dari weekly_report.md"""
import argparse
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from docx.text.paragraph import Paragraph

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.config import input_dir, project_root

# Lebar kolom (cm) untuk halaman A4 lanskap dengan margin 1,8 cm
COL_WIDTHS = [1.7, 2.0, 1.0, 5.1, 10.3, 1.4, 4.4]
FONT_BODY = 9
FONT_HEADER = 7.5
FONT_LINK = 8


def clean_md_links(text):
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    return text.replace("\\_", "_").strip()


def parse_md_rows(md_path):
    rows = []
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "Weekly" in line or "-----" in line:
            continue
        cols = [clean_md_links(c.strip()) for c in line.split("|")[1:-1]]
        if len(cols) < 7:
            cols += [""] * (7 - len(cols))
        rows.append(cols[:7])
    return rows


def set_repeat_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def _rapikan_paragraf(p, align, hanging=False):
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.0
    if hanging:
        pf.left_indent = Cm(0.35)
        pf.first_line_indent = Cm(-0.35)


def set_cell(cell, text, size=FONT_BODY, align=WD_ALIGN_PARAGRAPH.LEFT, hanging=False):
    cell.text = ""
    p = cell.paragraphs[0]
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    _rapikan_paragraf(p, align, hanging)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.name = "Arial"
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def set_cell_link(cell, url, label="PR"):
    cell.text = ""
    p = cell.paragraphs[0]
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    _rapikan_paragraf(p, WD_ALIGN_PARAGRAPH.CENTER)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    r_id = p.part.relate_to(url, RT.HYPERLINK, is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)

    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    rfonts = OxmlElement("w:rFonts")
    rfonts.set(qn("w:ascii"), "Arial")
    rfonts.set(qn("w:hAnsi"), "Arial")
    rpr.append(rfonts)
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    rpr.append(color)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(FONT_LINK * 2)))
    rpr.append(sz)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    rpr.append(underline)
    run.append(rpr)

    t = OxmlElement("w:t")
    t.text = label
    run.append(t)
    hyperlink.append(run)
    p._p.append(hyperlink)


def rapikan_judul(doc, period):
    """Perbaiki ejaan judul template dan tambahkan keterangan periode."""
    bulan = {
        "01": "Januari", "02": "Februari", "03": "Maret", "04": "April",
        "05": "Mei", "06": "Juni", "07": "Juli", "08": "Agustus",
        "09": "September", "10": "Oktober", "11": "November", "12": "Desember",
    }.get(period[-2:], "")
    tahun = period[:4]

    for p in doc.paragraphs:
        if "LOG Book" in p.text:
            for run in p.runs:
                run.text = ""
            if p.runs:
                p.runs[0].text = "Log Book Aktivitas Personil Timja Program dan Data"
            else:
                p.add_run("Log Book Aktivitas Personil Timja Program dan Data")

            baru_p = OxmlElement("w:p")
            p._p.addnext(baru_p)
            baru = Paragraph(baru_p, p._parent)
            baru.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = baru.add_run(f"Periode: 1–{akhir_bulan(period)} {bulan} {tahun}")
            r.font.size = Pt(10)
            r.font.name = "Arial"
            break

    for p in doc.paragraphs:
        if p.text.strip() == "Pic: Data":
            if p.runs:
                p.runs[0].text = "PIC: Data"
            break


def rapikan_posisi_tabel(table):
    """Hapus indentasi negatif bawaan template dan posisikan tabel di tengah halaman."""
    tbl_pr = table._tbl.tblPr
    total_dxa = int(sum(Cm(w).twips for w in COL_WIDTHS))

    tbl_w = tbl_pr.find(qn("w:tblW"))
    if tbl_w is not None:
        tbl_w.set(qn("w:w"), str(total_dxa))
        tbl_w.set(qn("w:type"), "dxa")

    tbl_ind = tbl_pr.find(qn("w:tblInd"))
    if tbl_ind is not None:
        tbl_ind.set(qn("w:w"), "0")

    jc = tbl_pr.find(qn("w:jc"))
    if jc is None:
        jc = OxmlElement("w:jc")
        tbl_pr.append(jc)
    jc.set(qn("w:val"), "center")


def akhir_bulan(period):
    import calendar

    tahun = int(period[:4])
    bulan = int(period[-2:])
    return calendar.monthrange(tahun, bulan)[1]


def build_weekly_docx(period):
    root = project_root()
    inp = input_dir(period)
    md_path = inp / "weekly_report.md"
    template = root / "template" / "weekly_report_template.docx"
    output = inp / "weekly_report.docx"

    if not md_path.exists():
        raise FileNotFoundError(md_path)
    if not template.exists():
        raise FileNotFoundError(template)

    rows = parse_md_rows(md_path)
    doc = Document(str(template))
    rapikan_judul(doc, period)

    section = doc.sections[0]
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width = Cm(29.7)
    section.page_height = Cm(21.0)
    section.left_margin = Cm(1.8)
    section.right_margin = Cm(1.8)
    section.top_margin = Cm(1.5)
    section.bottom_margin = Cm(1.5)

    table = doc.tables[0]
    table.autofit = False
    for idx, width in enumerate(COL_WIDTHS):
        table.columns[idx].width = Cm(width)
    rapikan_posisi_tabel(table)

    while len(table.rows) - 1 < len(rows):
        table.add_row()
    while len(table.rows) - 1 > len(rows) and len(table.rows) > 1:
        table._tbl.remove(table.rows[-1]._tr)

    header = table.rows[0]
    set_repeat_header(header)
    for idx, cell in enumerate(header.cells):
        cell.width = Cm(COL_WIDTHS[idx])
        _rapikan_paragraf(cell.paragraphs[0], WD_ALIGN_PARAGRAPH.CENTER)
        for run in cell.paragraphs[0].runs:
            run.font.size = Pt(FONT_HEADER)
            run.font.name = "Arial"
            run.bold = True
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    for i, cols in enumerate(rows, start=1):
        row = table.rows[i]
        for j, val in enumerate(cols):
            cell = row.cells[j]
            cell.width = Cm(COL_WIDTHS[j])
            if j in (0, 1, 2, 5):
                set_cell(cell, val, align=WD_ALIGN_PARAGRAPH.CENTER)
            elif j == 6 and val.startswith("http"):
                nomor = val.rstrip("/").rsplit("/", 1)[-1]
                set_cell_link(cell, val, f"PR #{nomor}")
            elif j == 4:
                set_cell(cell, val, hanging=val.startswith("- "))
            else:
                set_cell(cell, val)

    doc.save(str(output))
    return output, len(rows)


def main():
    parser = argparse.ArgumentParser(description="Generate weekly_report.docx dari markdown")
    parser.add_argument("period", help="YYYYMM contoh 202605")
    args = parser.parse_args()

    output, count = build_weekly_docx(args.period)
    print("Selesai:", output)
    print("Baris:", count)


if __name__ == "__main__":
    main()

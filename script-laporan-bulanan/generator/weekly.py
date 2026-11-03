# -*- coding: utf-8 -*-
"""Weekly report: ringkasan PR untuk kurasi, susun weekly_report.md, cek kualitas, dan ekspor .docx."""
import json
import re

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from .config import TEMPLATE_DIR, input_dir

# Lebar kolom (cm) untuk A4 lanskap dengan margin 1,8 cm — sama dengan template
COL_WIDTHS = [1.7, 2.0, 1.0, 5.1, 10.3, 1.4, 4.4]
FONT_BODY = 9
FONT_LINK = 8
MD_HEADER = (
    "# Weekly Report\n\nPic: Data\n\n"
    "| Weekly_ cat | date_range | date | activity | output | user | reltd_doc_link |\n"
    "| ----- | ----- | ----- | ----- | ----- | ----- | ----- |\n"
)


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------

def weekly_category(day):
    if day <= 10:
        return "W1", "1-10"
    if day <= 20:
        return "W2", "11-20"
    return "W3", "21-31"


def _one_line(text):
    return " ".join((text or "").split()).replace("|", "-")


def parse_md_rows(md_path):
    """Baris tabel 7 kolom dari weekly_report.md (tanpa header)."""
    rows = []
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "Weekly" in line or "-----" in line:
            continue
        cols = [re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", c.strip()).replace("\\_", "_").strip()
                for c in line.split("|")[1:-1]]
        rows.append((cols + [""] * 7)[:7])
    return rows


def build_md(period, raw_prs, user="Lutfi"):
    """Susun weekly_report.md dari raw_prs.json.

    Jika curated.json ada ([nomor, activity, output] per PR, bahasa Indonesia), teksnya dipakai.
    Jika belum ada, judul & body PR dipakai apa adanya (draf mentah untuk dipoles,
    lihat generator/prompts/poles_weekly.md).
    """
    inp = input_dir(period)
    curated_path = inp / "curated.json"
    curated = {}
    if curated_path.exists():
        curated = {(int(n) if str(n).isdigit() else n): (a.strip(), o.strip())
                   for n, a, o in json.loads(curated_path.read_text(encoding="utf-8"))}
        missing = [p["number"] for p in raw_prs if p["number"] not in curated]
        if missing:
            print("PERINGATAN: PR belum dikurasi:", missing)

    rows = []
    for pr in raw_prs:
        num = pr["number"]
        if curated:
            if num not in curated:
                continue
            activity, output = curated[num]
        else:
            activity = pr["title"]
            output = pr.get("body", "").strip() or f"Implementasi {pr['title']}"
        activity, output = _one_line(activity), _one_line(output)
        if not activity or not output:
            print(f"PERINGATAN: PR #{num} memiliki teks kosong.")
            continue
        day = int(pr["mergedAt"][8:10])
        cat, drange = weekly_category(day)
        rows.append(f"| {cat} | {drange} | {day} | {activity} | {output} | {user} | {pr['url']} |")

    out_path = inp / "weekly_report.md"
    out_path.write_text(MD_HEADER + "\n".join(rows) + "\n", encoding="utf-8")
    sumber = "curated.json" if curated else "judul/body PR (mentah)"
    print(f"weekly_report.md: {len(rows)} baris dari {len(raw_prs)} PR, sumber teks: {sumber}")
    return out_path


def digest(raw_prs, start=0, end=None, body_len=220):
    """Cetak ringkasan PR (judul + potongan body) sebagai bahan kurasi curated.json."""
    def clean(s):
        s = re.sub(r"```.*?```", " ", s or "", flags=re.S)
        s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
        s = re.sub(r"[#*`>|]+", " ", s)
        s = re.sub(r"[�\u0000-\u001f]", " ", s)
        return re.sub(r"\s+", " ", s).strip()

    for i, pr in enumerate(raw_prs[start:end], start + 1):
        print(f"{i}. #{pr['number']} {pr['mergedAt'][:10]} :: {clean(pr['title'])}")
        body = clean(pr.get("body", ""))
        if body:
            print(f"   B: {body[:body_len]}")


# ---------------------------------------------------------------------------
# Pemeriksaan kualitas (gaya bahasa instansi pemerintah)
# ---------------------------------------------------------------------------

KATA_INGGRIS = {
    "the", "and", "for", "with", "from", "this", "that", "these", "those", "is", "are", "was",
    "were", "to", "of", "in", "on", "by", "when", "not", "add", "fix", "update", "remove", "use",
    "shows", "show", "hide", "allow", "prevent", "handle", "apply", "avoid", "keep", "make",
    "based", "issue", "support", "instead", "only", "now", "still", "should", "must", "before",
    "after", "while", "which", "there", "their", "into", "over", "under", "than", "then",
}


def check_md(md_path):
    problems = []
    for idx, line in enumerate(md_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|") or "Weekly" in line or "-----" in line:
            continue
        cols = [c.strip() for c in line.split("|")[1:-1]]
        if len(cols) != 7:
            problems.append(f"baris {idx}: jumlah kolom {len(cols)}")
            continue
        activity, output = cols[3], cols[4]
        for label, val in (("activity", activity), ("output", output)):
            if "..." in val or "…" in val:
                problems.append(f"baris {idx} {label}: mengandung elipsis")
            if re.search(r"\s(?:dan|atau|untuk|dengan|yang|di|ke|pada|dari|serta|agar|karena|sebagai)\s*$", val, re.I):
                problems.append(f"baris {idx} {label}: berakhir kata sambung -> {val[-50:]}")
            if val.endswith((",", "-", ":")):
                problems.append(f"baris {idx} {label}: tanda akhir tidak lazim")
            en = sorted({w for w in re.findall(r"[A-Za-z][A-Za-z'-]+", val.lower()) if w in KATA_INGGRIS})
            if en:
                problems.append(f"baris {idx} {label}: kata Inggris {en} -> {val[:70]}")
            if len(val) > 320:
                problems.append(f"baris {idx} {label}: terlalu panjang ({len(val)} karakter)")
        if not re.match(r"^(Men|Mem|Meng|Meny|Memb|Me|Per|Pen)", activity):
            problems.append(f"baris {idx} activity: tidak diawali kata kerja -> {activity[:50]}")
    return problems


# ---------------------------------------------------------------------------
# DOCX (Lampiran 1)
# ---------------------------------------------------------------------------

def _rapikan_paragraf(p, align, hanging=False):
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = pf.space_after = Pt(0)
    pf.line_spacing = 1.0
    if hanging:
        pf.left_indent = Cm(0.35)
        pf.first_line_indent = Cm(-0.35)


def _set_cell(cell, text, align=WD_ALIGN_PARAGRAPH.LEFT, hanging=False):
    cell.text = ""
    p = cell.paragraphs[0]
    _rapikan_paragraf(p, align, hanging)
    run = p.add_run(text)
    run.font.size = Pt(FONT_BODY)
    run.font.name = "Arial"
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def _set_cell_link(cell, url, label):
    cell.text = ""
    p = cell.paragraphs[0]
    _rapikan_paragraf(p, WD_ALIGN_PARAGRAPH.CENTER)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), p.part.relate_to(url, RT.HYPERLINK, is_external=True))
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    for tag, attrs in (("w:rFonts", {"w:ascii": "Arial", "w:hAnsi": "Arial"}),
                       ("w:color", {"w:val": "0563C1"}),
                       ("w:sz", {"w:val": str(FONT_LINK * 2)}),
                       ("w:u", {"w:val": "single"})):
        el = OxmlElement(tag)
        for k, v in attrs.items():
            el.set(qn(k), v)
        rpr.append(el)
    run.append(rpr)
    t = OxmlElement("w:t")
    t.text = label
    run.append(t)
    hyperlink.append(run)
    p._p.append(hyperlink)


def to_docx(period, config):
    """weekly_report.md -> weekly_report.docx memakai template/weekly_report_template.docx."""
    inp = input_dir(period)
    rows = parse_md_rows(inp / "weekly_report.md")
    doc = Document(str(TEMPLATE_DIR / "weekly_report_template.docx"))

    periode = f"1–{config['akhir_bulan']} {config['bulan']} {config['tahun']}"
    for p in doc.paragraphs:
        if "{{ PERIODE }}" in p.text:
            for r in p.runs:
                r.text = r.text.replace("{{ PERIODE }}", periode)

    table = doc.tables[0]
    for cols in rows:
        cells = table.add_row().cells
        for j, val in enumerate(cols):
            cells[j].width = Cm(COL_WIDTHS[j])
            if j in (0, 1, 2, 5):
                _set_cell(cells[j], val, align=WD_ALIGN_PARAGRAPH.CENTER)
            elif j == 6 and val.startswith("http"):
                ujung = val.rstrip("/").rsplit("/", 1)[-1]
                _set_cell_link(cells[j], val, f"Commit {ujung[:7]}" if "/commit/" in val else f"PR #{ujung}")
            elif j == 4:
                _set_cell(cells[j], val, hanging=val.startswith("- "))
            else:
                _set_cell(cells[j], val)

    output = inp / "weekly_report.docx"
    doc.save(str(output))
    return output, len(rows)

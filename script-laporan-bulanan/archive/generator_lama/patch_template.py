# -*- coding: utf-8 -*-
"""
Patch laporan_template.docx untuk menambahkan marker dinamis:
  {{ BAB1_PENCAPAIAN }}  — diganti dari config['bab1']['pencapaian']
  {{ BAB1_TANTANGAN }}   — diganti dari config['bab1']['tantangan']
  {{ BAB3_KESIMPULAN }}  — diganti dari config['bab3']['kesimpulan_items']

Jalankan sekali saja dari folder script-laporan-bulanan/:
  python generator/patch_template.py
"""
import shutil
import zipfile
from pathlib import Path

from lxml import etree

ROOT  = Path(__file__).resolve().parent.parent
TPL   = ROOT / "template" / "laporan_template.docx"
BACKUP = ROOT / "template" / "laporan_template_backup.docx"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def para_text(p):
    return "".join((t.text or "") for t in p.findall(".//w:t", NS))


def clear_content(p):
    """Remove all child elements except pPr, bookmarkStart, bookmarkEnd."""
    keep = {"pPr", "bookmarkStart", "bookmarkEnd"}
    for child in list(p):
        local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if local not in keep:
            p.remove(child)


def make_run(text):
    r = etree.Element(f"{{{W}}}r")
    t = etree.SubElement(r, f"{{{W}}}t")
    t.text = text
    return r


def set_marker(p, marker):
    clear_content(p)
    p.append(make_run(marker))


def main():
    if not TPL.exists():
        print("Template tidak ditemukan:", TPL)
        return

    # Backup
    shutil.copy2(TPL, BACKUP)
    print("Backup:", BACKUP)

    # Read all files in zip
    with zipfile.ZipFile(TPL, "r") as z:
        names = z.namelist()
        files = {n: z.read(n) for n in names}

    xml_bytes = files["word/document.xml"]
    tree = etree.fromstring(xml_bytes)
    body = tree.find(".//w:body", NS)
    paras = body.findall("w:p", NS)

    changes = []

    # --- Collect indices by keyword ---
    # BAB1_PENCAPAIAN: paragraph starting with "Pada bulan Mei2026"
    # BAB1_TANTANGAN:  paragraph starting with "Selama penyusunan"
    # BAB3_KESIMPULAN: all "Modul ..." list items (replace first, remove rest)
    bab3_start = None
    bab3_end   = None

    for i, p in enumerate(paras):
        txt = para_text(p)

        if "Mei2026" in txt and "kami telah mencapai" in txt:
            changes.append((i, "{{ BAB1_PENCAPAIAN }}"))

        elif txt.startswith("Selama penyusunan"):
            changes.append((i, "{{ BAB1_TANTANGAN }}"))

        elif txt.startswith("Modul ") and bab3_start is None:
            bab3_start = i

        elif bab3_start is not None and bab3_end is None:
            # Continue until non-list paragraph
            if txt.startswith("Modul "):
                bab3_end = i  # last Modul para so far
            elif txt == "":
                pass  # blank para, keep scanning
            else:
                break  # stop at first non-Modul non-blank para

    # Apply simple marker replacements
    for idx, marker in changes:
        set_marker(paras[idx], marker)
        print(f"  Para {idx}: -> {marker}")

    # BAB3: replace first Modul para with marker, remove the rest
    if bab3_start is not None:
        end = bab3_end if bab3_end is not None else bab3_start
        set_marker(paras[bab3_start], "{{ BAB3_KESIMPULAN }}")
        print(f"  Para {bab3_start}: -> {{{{ BAB3_KESIMPULAN }}}}")
        for i in range(bab3_start + 1, end + 1):
            txt = para_text(paras[i])
            if txt.startswith("Modul "):
                body.remove(paras[i])
                print(f"  Para {i}: removed ({txt[:40]})")

    # Write back
    new_xml = etree.tostring(tree, xml_declaration=True, encoding="UTF-8", standalone=True)
    files["word/document.xml"] = new_xml

    with zipfile.ZipFile(TPL, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in names:
            zout.writestr(name, files[name])

    print("Template diperbarui:", TPL)


if __name__ == "__main__":
    main()

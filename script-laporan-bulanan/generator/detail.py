# -*- coding: utf-8 -*-
"""detail_github.md: rincian BAB II per modul, disusun dari weekly_report.md + data PR lokal."""
import json
import re
from collections import defaultdict

from .config import GENERATOR_DIR, input_dir

PR_URL_RE = re.compile(r"github\.com/[^/]+/[^/]+/(?:pull|commit)/(\d+|[a-f0-9]{40})", re.I)
DIFF_FILE_RE = re.compile(r"^diff --git a/(\S+) b/(\S+)", re.M)
MANFAAT_DEFAULT = (
    "Sistem menjadi lebih stabil, akurat, dan dapat memberikan pengalaman pengguna "
    "yang lebih baik untuk mendukung operasional PSDKP."
)


# ---------------------------------------------------------------------------
# Modul (generator/modules.json)
# ---------------------------------------------------------------------------

def load_modules_config():
    return json.loads((GENERATOR_DIR / "modules.json").read_text(encoding="utf-8"))


def match_module(activity, output, modules_cfg):
    """Pilih modul berdasarkan kata kunci; kata kunci pada activity lebih berbobot."""
    activity_text, output_text = (activity or "").lower(), (output or "").lower()
    best, best_score = None, 0
    for mod in modules_cfg["modules"]:
        score = 2 * sum(1 for kw in mod["keywords"] if kw.lower() in activity_text)
        score += sum(1 for kw in mod["keywords"] if kw.lower() in output_text)
        if score > best_score:
            best, best_score = mod, score
    return best


def build_module_intro(mod, modules_cfg):
    return modules_cfg.get("module_intro_template", "").format(verb=mod["verb"], modul=mod["modul"])


def _activity_phrase(activity):
    if not activity:
        return activity
    if activity.lower().startswith(("men", "mem", "me", "per", "pen", "meny", "meng")):
        return activity[0].lower() + activity[1:]
    return f"melakukan {activity[0].lower() + activity[1:]}"


def build_prolog(activity, mod, output, modules_cfg):
    konteks = ""
    if output and len(output) > 20:
        # Ambil kalimat pertama; jika masih panjang, potong di batas kata
        short = output.strip().split(". ")[0].strip()
        if len(short) > 200:
            short = short[:200].rsplit(" ", 1)[0].rstrip(",;:")
        if not short.endswith("."):
            short += "."
        konteks = f" Kegiatan ini berkaitan dengan: {short}"
    return modules_cfg.get("prolog_template", "").format(
        kegiatan=_activity_phrase(activity), modul=mod["modul"], konteks=konteks)


# ---------------------------------------------------------------------------
# Data PR lokal (prs.json + prs_diff.json)
# ---------------------------------------------------------------------------

def extract_pr_numbers(text):
    nums = [int(m.group(1)) for m in PR_URL_RE.finditer(text or "") if m.group(1).isdigit()]
    return list(dict.fromkeys(nums))


def load_local_pr_data(inp_dir):
    prs_by_num, diffs = {}, {}
    if (inp_dir / "prs.json").exists():
        prs_by_num = {pr["number"]: pr for pr in json.loads((inp_dir / "prs.json").read_text(encoding="utf-8"))}
    if (inp_dir / "prs_diff.json").exists():
        diffs = json.loads((inp_dir / "prs_diff.json").read_text(encoding="utf-8"))
    return prs_by_num, diffs


def local_pr_detail(number, prs_by_num, diffs):
    """Judul, file yang diubah, dan jumlah baris +/- satu PR dari data lokal (tanpa memanggil gh)."""
    diff = diffs.get(str(number))
    pr = prs_by_num.get(number)
    if not diff and not pr:
        return None
    files, adds, dels = [], 0, 0
    if diff:
        files = list(dict.fromkeys(m.group(2) for m in DIFF_FILE_RE.finditer(diff)))
        for line in diff.splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                adds += 1
            elif line.startswith("-") and not line.startswith("---"):
                dels += 1
    return {"number": number, "title": (pr or {}).get("title", ""),
            "files": files, "additions": adds, "deletions": dels}


def _utama(detail):
    title = detail["title"]
    if len(title) > 75:
        title = title[:72].rstrip() + "…"
    return f"PR #{detail['number']}: {title} (+{detail['additions']}/-{detail['deletions']} baris)."


# ---------------------------------------------------------------------------
# Susun detail_github.md
# ---------------------------------------------------------------------------

def parse_weekly_activities(path, user_filter="Lutfi"):
    rows = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "Weekly" in line or "-----" in line:
            continue
        cols = [c.strip() for c in line.split("|")[1:-1]]
        if len(cols) < 7:
            continue
        weekly, date_range, day, activity, output, user, links = cols[:7]
        if not activity.strip() or (user_filter and user_filter.lower() not in user.lower()):
            continue
        rows.append({
            "activity": re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", activity).strip(),
            "output": re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", output).strip(),
            "links": links.strip(),
            "pr_numbers": extract_pr_numbers(links),
        })
    return rows


def _bersihkan_output(output):
    """Ubah output berbutir menjadi kalimat mengalir."""
    baris = [re.sub(r"^\s*[-*•]\s*", "", b).strip() for b in output.splitlines()]
    teks = re.sub(r"\s+", " ", " ".join(b for b in baris if b)).strip()
    if teks and not teks.endswith("."):
        teks += "."
    return teks


def render_activity_md(act, mod, modules_cfg, repo, sub_idx, pr_data):
    output = _bersihkan_output(act["output"])
    kegiatan = act["activity"][:1].lower() + act["activity"][1:]
    prolog = build_prolog(act["activity"], mod, output, modules_cfg)
    # Format acuan Agustus 2026: "Telah dilakukan implementasi terkait [kegiatan]. [output]"
    deskripsi = re.sub(r"\s{2,}", " ", f"Telah dilakukan implementasi terkait {kegiatan}. {output}").strip()

    details = [d for d in (local_pr_detail(n, *pr_data) for n in act["pr_numbers"]) if d]
    files = list(dict.fromkeys(f for d in details for f in d["files"]))
    manfaat = mod.get("manfaat") or modules_cfg.get("manfaat_default", MANFAAT_DEFAULT)

    docs = [f"https://github.com/{repo}/pull/{num}" for num in act["pr_numbers"]]
    for m in re.finditer(r"https://github\.com/[^\s\)]+/commit/[a-f0-9]+", act["links"]):
        if m.group(0) not in docs:
            docs.append(m.group(0))

    lines = [f"### {sub_idx} {act['activity']}", "", "**Prolog**", "", prolog, "",
             "**Deskripsi Pekerjaan**", "", deskripsi, "", "**Detail Perubahan**", ""]
    if files:
        lines += ["**File yang Diubah:**"] + [f"- `{f}`" for f in files] + [""]
    if details:
        lines += ["**Perubahan Utama:**"] + [f"- {_utama(d)}" for d in details] + [""]
    lines += ["**Manfaat:**", f"- {manfaat}", "", "**Dokumentasi**", ""]
    lines += [f"- {d}" for d in docs] or ["- Tidak ada tautan dokumentasi."]
    lines += ["", "---", ""]
    return "\n".join(lines)


def build_from_weekly(config):
    period = config["period"]
    inp = input_dir(period)
    modules_cfg = load_modules_config()
    repo = config["github"]["repo"]
    activities = parse_weekly_activities(inp / "weekly_report.md", config.get("weekly_user_filter", "Lutfi"))
    pr_data = load_local_pr_data(inp)

    fallback = next((m for m in modules_cfg["modules"] if m["id"] == "lainnya"), None) or {
        "id": "lainnya", "title": "Kegiatan Pendukung dan Pemeliharaan Sistem",
        "verb": "melaksanakan", "modul": "Sistem Informasi Pengawasan SDKP", "keywords": []}
    grouped = defaultdict(list)
    for act in activities:
        mod = match_module(act["activity"], act["output"], modules_cfg) or fallback
        grouped[mod["id"]].append(act)

    bulan, tahun = config["bulan"], config["tahun"]
    lines = [
        f"# DETAIL LAPORAN KEGIATAN — {config.get('nama', 'Lutfi Ihsan').upper()}",
        f"## Bulan {bulan} {tahun}",
        "",
        "Dokumen ini memuat rincian kegiatan Tenaga Teknis Implementasi Logika Sistem "
        f"pada bulan {bulan} {tahun} berdasarkan data pekerjaan yang tercatat pada "
        f"repositori GitHub {repo}.",
        "",
        f"- Jumlah sub-kegiatan: **{len(activities)}**",
        f"- Sumber data: `input/{period}/weekly_report.md`",
        "", "---", "",
    ]

    rekap = []
    mods = [m for m in modules_cfg["modules"] if grouped.get(m["id"])]
    if grouped.get("lainnya") and fallback not in mods:
        mods.append(fallback)
    for num, mod in enumerate(mods, 1):
        items = grouped[mod["id"]]
        rekap.append((mod["title"], len(items)))
        lines += [f"## {num}. {mod['title']}", "", build_module_intro(mod, modules_cfg), ""]
        for sub_idx, act in enumerate(items, 1):
            lines.append(render_activity_md(act, mod, modules_cfg, repo, f"{num}.{sub_idx}", pr_data))

    lines += ["## RINGKASAN KEGIATAN", "", f"Total sub-kegiatan bulan {bulan} {tahun}: **{len(activities)}**", ""]
    lines += [f"{i}. {title}: {jumlah} sub-kegiatan" for i, (title, jumlah) in enumerate(rekap, 1)]
    return "\n".join(lines) + "\n"


def inject_prologs(md_content, refresh=False):
    """Tambahkan (atau perbarui) **Prolog** pada sub-kegiatan yang belum punya."""
    modules_cfg = load_modules_config()
    lines = md_content.splitlines()
    out, i = [], 0
    current_mod = modules_cfg["modules"][0]
    while i < len(lines):
        line = lines[i]
        if line.startswith("### "):
            subtitle = re.sub(r"^\d+\.\d+\s*", "", line[4:].strip())
            out.append(line)
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            has_prolog = i < len(lines) and lines[i].strip() == "**Prolog**"
            if has_prolog and refresh:
                i += 1
                while i < len(lines) and lines[i].strip() != "**Deskripsi Pekerjaan**":
                    i += 1
            if refresh or not has_prolog:
                out.extend(["", "**Prolog**", "", build_prolog(subtitle, current_mod, "", modules_cfg), ""])
            continue
        out.append(line)
        if re.match(r"## \d+\.", line):
            title = re.sub(r"^KEGIATAN TAMBAHAN —\s*", "", re.sub(r"^\d+\.\s*", "", line[3:].strip()))
            for mod in modules_cfg["modules"]:
                if mod["title"].lower() in title.lower() or title.lower() in mod["title"].lower():
                    current_mod = mod
                    break
        i += 1
    return "\n".join(out)


def md_to_txt(md_content):
    """Versi teks polos detail_github.md (untuk ditempel ke dokumen lain)."""
    lines = []
    for raw in md_content.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            lines.append("")
            continue
        if stripped == "---":
            lines.append("-" * 72)
            continue
        if stripped.startswith("<!--") and stripped.endswith("-->"):
            continue
        line = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", line)
        line = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", line)
        line = re.sub(r"`([^`]+)`", r"\1", line)
        line = re.sub(r"\*\*([^*]+)\*\*", r"\1", line)
        line = re.sub(r"\*([^*]+)\*", r"\1", line)
        if line.startswith("# "):
            title = line[2:].strip()
            lines.extend(["", title.upper(), "=" * len(title), ""])
        elif line.startswith("## "):
            title = line[3:].strip()
            lines.extend(["", title, "-" * len(title), ""])
        elif line.startswith("### "):
            lines.extend(["", line[4:].strip(), ""])
        elif line.startswith("> "):
            lines.append(line[2:].strip())
        elif line.startswith("- "):
            lines.append("  * " + line[2:].strip())
        else:
            lines.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"


def save(md_content, period):
    inp = input_dir(period)
    md_path, txt_path = inp / "detail_github.md", inp / "detail_github.txt"
    md_path.write_text(md_content, encoding="utf-8")
    txt_path.write_text(md_to_txt(md_content), encoding="utf-8")
    return md_path, txt_path


def build_enrich_prompt(period):
    """Prompt AI untuk melengkapi deskripsi pada detail_github.md."""
    md_path = input_dir(period) / "detail_github.md"
    template = (GENERATOR_DIR / "prompts" / "enrich_detail.md").read_text(encoding="utf-8")
    content = md_path.read_text(encoding="utf-8")
    body = content[:8000] + ("\n..." if len(content) > 8000 else "")
    return template.replace("{period}", period).replace("{md_name}", md_path.name).replace("{content}", body)

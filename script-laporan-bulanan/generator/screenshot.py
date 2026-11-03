# -*- coding: utf-8 -*-
"""Gambar Manajemen Kode Sumber dari data asli, dirender lewat browser headless (Edge/Chrome).

a. Daftar pull request closed bulan berjalan, bergaya halaman GitHub (25 PR per halaman, seperti GitHub).
b. Riwayat merge ke branch production (atau master bila production belum ada) pada periode laporan,
   hasil `git log` di clone lokal, bergaya jendela terminal Bitvise xterm.

Hasil: input/YYYYMM/manajemen_kode/github_NN.png, server.png, dan keterangan.json (teks keterangan gambar).
"""
import html
import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

from .config import input_dir
from .github import _env, nomor_key

PER_HALAMAN = 25
BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]
BULAN_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

ICON_MERGED = ('<svg viewBox="0 0 16 16" width="16" height="16" fill="#8250df"><path d="M5.45 5.154A4.25 4.25 0 0 0 '
               '9.25 7.5h1.378a2.251 2.251 0 1 1 0 1.5H9.25A5.734 5.734 0 0 1 5 7.123v3.505a2.25 2.25 0 1 1-1.5 '
               '0V5.372a2.25 2.25 0 1 1 1.95-.218ZM4.25 13.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm8.5-4.5a.75.75 0 '
               '1 0 0-1.5.75.75 0 0 0 0 1.5ZM5 3.25a.75.75 0 1 0 0 .001Z"/></svg>')
ICON_PR = ('<svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor"><path d="M1.5 3.25a2.25 2.25 0 1 1 3 '
           '2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 '
           '10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 '
           '1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354Z"/></svg>')
ICON_CHECK = ('<svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor"><path d="M13.78 4.22a.75.75 0 0 1 '
              '0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.75.75 0 0 1 1.06-1.06L6 10.94l6.72-6.72a.75.75 0 '
              '0 1 1.06 0Z"/></svg>')
ICON_REPO = ('<svg viewBox="0 0 16 16" width="16" height="16" fill="#59636e"><path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75'
             '.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 '
             '1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 '
             '12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 '
             '0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"/></svg>')


def _browser():
    for path in BROWSERS:
        if Path(path).exists():
            return path
    found = shutil.which("msedge") or shutil.which("chrome")
    if not found:
        raise RuntimeError("Edge/Chrome tidak ditemukan untuk merender gambar.")
    return found


def render(page_html, out_path, width, height):
    """Render HTML ke PNG dengan ukuran jendela tetap (skala 2x agar tajam saat dicetak)."""
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "page.html"
        src.write_text(page_html, encoding="utf-8")
        subprocess.run([
            _browser(), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
            f"--user-data-dir={Path(tmp) / 'profile'}", "--force-device-scale-factor=2",
            f"--window-size={width},{height}", f"--screenshot={out_path}", src.as_uri(),
        ], check=True, capture_output=True, timeout=120)
    _trim_bawah(out_path)
    return out_path


def _trim_bawah(path, margin=24):
    """Buang ruang kosong di bawah konten (tinggi jendela ditaksir sedikit berlebih)."""
    from PIL import Image
    img = Image.open(path).convert("RGB")
    w, h = img.size
    bg = img.getpixel((w // 2, h - 1))
    px = img.load()
    y = h - 1
    while y > 0 and all(px[x, y] == bg for x in range(0, w, 7)):
        y -= 1
    img.crop((0, 0, w, min(h, y + 1 + margin))).save(path)


# ---------------------------------------------------------------------------
# a. Daftar PR closed bergaya GitHub
# ---------------------------------------------------------------------------

def _pr_meta(config, raw_prs):
    """Login author per PR (dari gh bila bisa; selain itu author pertama di config)."""
    gh = config["github"]
    authors = [a.strip() for a in gh["author"].split(",")] if isinstance(gh["author"], str) else gh["author"]
    meta = {}
    ym = f"{config['tahun']}-{int(config['period'][4:]):02d}"
    try:
        env = _env(gh)
        for author in authors:
            res = subprocess.run(
                ["gh", "pr", "list", "-R", gh["repo"], "-S", f"author:{author} merged:{ym}-01..{ym}-{config['akhir_bulan']:02d}",
                 "--state", "merged", "-L", "300", "--json", "number,author"],
                capture_output=True, text=True, encoding="utf-8", env=env, timeout=120)
            for pr in json.loads(res.stdout or "[]") if res.returncode == 0 else []:
                meta[pr["number"]] = pr["author"]["login"]
    except Exception as exc:  # gh opsional
        print("INFO: author PR dari config (gh tidak tersedia):", exc)
    return {pr["number"]: meta.get(pr["number"], authors[0]) for pr in raw_prs}


def _tanggal_en(iso):
    d = datetime.fromisoformat(iso[:10])
    return f"{BULAN_EN[d.month - 1]} {d.day}, {d.year}"


def github_page_html(config, rows, page, pages, total):
    owner, repo = config["github"]["repo"].split("/")
    gh = config["github"]
    authors = gh["author"] if isinstance(gh["author"], str) else ",".join(gh["author"])
    ym = f"{config['tahun']}-{int(config['period'][4:]):02d}"
    query = (f"is:pr is:closed {' '.join('author:' + a.strip() for a in authors.split(','))} "
             f"merged:{ym}-01..{ym}-{config['akhir_bulan']:02d}")
    items = []
    for pr in rows:
        nomor = pr["number"]
        label = f"#{nomor}" if isinstance(nomor, int) else str(nomor)
        items.append(f"""
      <div class="row">
        <div class="ic">{ICON_MERGED}</div>
        <div class="main">
          <a class="title">{html.escape(pr['title'])}</a>
          <div class="meta">{label} by <a>{html.escape(pr['login'])}</a> was merged on {_tanggal_en(pr['mergedAt'])}</div>
        </div>
      </div>""")
    pager = "".join(f'<span class="pg{" cur" if i == page else ""}">{i}</span>' for i in range(1, pages + 1))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#fff;font:14px -apple-system,"Segoe UI",Helvetica,Arial,sans-serif;color:#1f2328}}
.top{{background:#f6f8fa;border-bottom:1px solid #d1d9e0;padding:16px 32px 0}}
.repo{{display:flex;align-items:center;gap:8px;font-size:20px}} .repo a{{color:#0969da}} .repo b{{color:#0969da}}
.pub{{border:1px solid #d1d9e0;border-radius:2em;font-size:12px;padding:0 7px;color:#59636e;margin-left:4px}}
.tabs{{display:flex;gap:4px;margin-top:16px}} .tab{{padding:8px 12px;color:#1f2328}}
.tab.sel{{border-bottom:2px solid #fd8c73;font-weight:600}} .cnt{{background:#818b981f;border-radius:2em;padding:0 6px;font-size:12px;margin-left:4px}}
.wrap{{padding:24px 32px}}
.bar{{display:flex;gap:8px;margin-bottom:16px}} .filters{{border:1px solid #d1d9e0;border-radius:6px;padding:5px 12px;background:#f6f8fa;font-weight:600}}
.search{{flex:1;border:1px solid #d1d9e0;border-radius:6px;padding:5px 12px;color:#59636e;background:#f6f8fa}}
.btn{{background:#1f883d;color:#fff;border-radius:6px;padding:5px 16px;font-weight:600}}
.box{{border:1px solid #d1d9e0;border-radius:6px}}
.bh{{background:#f6f8fa;padding:16px;display:flex;gap:16px;border-bottom:1px solid #d1d9e0;align-items:center}}
.bh .st{{display:flex;gap:4px;align-items:center;color:#59636e}} .bh .st.on{{color:#1f2328;font-weight:600}}
.bh .sp{{flex:1}} .bh .f{{color:#59636e}}
.row{{display:flex;gap:8px;padding:8px 16px;border-top:1px solid #d1d9e0}} .row:first-of-type{{border-top:0}}
.ic{{padding-top:3px}} .title{{font-weight:600;font-size:16px;color:#1f2328}}
.meta{{color:#59636e;font-size:12px;margin-top:4px}} .meta a{{color:#59636e}}
.pager{{display:flex;justify-content:center;gap:4px;margin-top:16px;color:#59636e}}
.pg{{padding:5px 10px;border-radius:6px}} .pg.cur{{background:#0969da;color:#fff}}
</style></head><body>
<div class="top">
  <div class="repo">{ICON_REPO}<a>{owner}</a>/<b>{repo}</b></div>
  <div class="tabs"><span class="tab">Code</span><span class="tab">Issues</span>
    <span class="tab sel">Pull requests</span><span class="tab">Actions</span><span class="tab">Projects</span>
    <span class="tab">Security</span><span class="tab">Insights</span></div>
</div>
<div class="wrap">
  <div class="bar"><span class="filters">Filters ▾</span><span class="search">{html.escape(query)}</span>
    <span class="filters">Labels</span><span class="filters">Milestones</span><span class="btn">New pull request</span></div>
  <div class="box">
    <div class="bh"><span class="st">{ICON_PR} 0 Open</span><span class="st on">{ICON_CHECK} {total} Closed</span>
      <span class="sp"></span><span class="f">Author ▾</span><span class="f">Label ▾</span><span class="f">Projects ▾</span>
      <span class="f">Milestones ▾</span><span class="f">Reviews ▾</span><span class="f">Assignee ▾</span><span class="f">Sort ▾</span></div>
    {''.join(items)}
  </div>
  <div class="pager"><span class="pg">‹ Previous</span>{pager}<span class="pg">Next ›</span></div>
</div></body></html>"""


def github_images(config, raw_prs, folder):
    login = _pr_meta(config, raw_prs)
    # Hanya PR sungguhan (entri WIP-* adalah commit branch yang belum menjadi PR); GitHub: terbaru di atas
    prs = sorted((p for p in raw_prs if isinstance(p["number"], int)), key=lambda p: p["mergedAt"], reverse=True)
    for pr in prs:
        pr["login"] = login[pr["number"]]
    pages = max(1, -(-len(prs) // PER_HALAMAN))
    keterangan = {}
    for i in range(pages):
        rows = prs[i * PER_HALAMAN:(i + 1) * PER_HALAMAN]
        out = folder / f"github_{i + 1:02d}.png"
        height = 270 + 62 * len(rows) + 70
        render(github_page_html(config, rows, i + 1, pages, len(prs)), out, 1280, height)
        keterangan[out.name] = (f"Daftar pull request berstatus closed (merged) bulan {config['bulan']} "
                                f"{config['tahun']} pada repositori {config['github']['repo']} "
                                f"(halaman {i + 1} dari {pages})")
    return keterangan


# ---------------------------------------------------------------------------
# b. Riwayat merge ke production bergaya terminal Bitvise xterm
# ---------------------------------------------------------------------------

def _git(repo_path, *args):
    res = subprocess.run(["git", "-C", str(repo_path), *args], capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} gagal: {res.stderr.strip()}")
    return res.stdout


def _repo_lokal(config):
    path = config["github"].get("local_repo_path")
    if not path or not Path(path).exists():
        raise RuntimeError("Isi github.local_repo_path di config.json dengan clone lokal repositori.")
    remote = _git(path, "remote", "get-url", "origin").strip()
    if config["github"]["repo"].lower() not in remote.lower():
        raise RuntimeError(f"Clone {path} menunjuk {remote}, bukan {config['github']['repo']}.")
    return Path(path)


def terminal_image(config, folder, fetch=True):
    repo_path = _repo_lokal(config)
    if fetch:
        try:
            _git(repo_path, "fetch", "-q", "origin")
        except RuntimeError as exc:
            print("INFO: fetch gagal, memakai data lokal:", exc)
    ym = f"{config['tahun']}-{int(config['period'][4:]):02d}"
    since, until = f"{ym}-01 00:00", f"{ym}-{config['akhir_bulan']:02d} 23:59"
    branch = "production"
    log_args = ["log", "--first-parent", f"--since={since}", f"--until={until}",
                "--date=format:%Y-%m-%d %H:%M", "--format=%h  %ad  %s"]
    out = _git(repo_path, *log_args, f"origin/{branch}").strip()
    if not out:  # belum ada rilis ke production pada periode ini -> PR ke master
        branch = "master"
        out = _git(repo_path, *log_args, f"origin/{branch}").strip()
    lines = out.splitlines()

    nama = config["github"]["repo"].split("/")[-1]
    perintah = (f'git log origin/{branch} --first-parent --since="{since}" --until="{until}" '
                f'--date=format:"%Y-%m-%d %H:%M" --format="%h  %ad  %s"')
    body = [f"<span class='p'>~/{nama}$</span> git fetch origin",
            f"<span class='p'>~/{nama}$</span> {html.escape(perintah)}"]
    body += [html.escape(l) for l in lines] or ["(tidak ada merge pada periode ini)"]
    body += [f"<span class='p'>~/{nama}$</span> git log origin/{branch} --first-parent --since=\"{since}\" "
             f"--until=\"{until}\" --oneline | wc -l", str(len(lines)),
             f"<span class='p'>~/{nama}$</span> <span class='cur'> </span>"]
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#f0f0f0;font-family:"Segoe UI",sans-serif}}
.win{{border:1px solid #6b6b6b;background:#000}}
.tb{{height:30px;background:#fff;display:flex;align-items:center;font-size:12px;color:#000;border-bottom:1px solid #ccc}}
.tb .ico{{width:16px;height:16px;margin:0 8px;background:linear-gradient(135deg,#1e5aa8,#4aa3df);border-radius:3px}}
.tb .t{{flex:1}} .tb .b{{width:46px;text-align:center;font-size:14px}}
.term{{padding:6px 8px;font:15px/20px Consolas,"Lucida Console",monospace;color:#c0c0c0;white-space:pre-wrap;word-break:break-all}}
.p{{color:#c0c0c0}} .cur{{background:#c0c0c0}}
</style></head><body><div class="win">
<div class="tb"><span class="ico"></span><span class="t">Bitvise xterm - {nama} [{branch}]</span>
<span class="b">&#8212;</span><span class="b">&#9744;</span><span class="b">&#10005;</span></div>
<div class="term">{"<br>".join(body)}</div></div></body></html>"""
    # tinggi: baris panjang terbungkus (±125 karakter per baris pada lebar 1280)
    baris = sum(max(1, -(-len(l) // 125)) for l in body)
    out_path = folder / "server.png"
    render(page, out_path, 1280, 40 + 20 * baris + 20)
    return {out_path.name: (f"Riwayat penggabungan (merge) kode sumber ke branch {branch} repositori "
                            f"{config['github']['repo']} periode {config['bulan']} {config['tahun']} "
                            f"({len(lines)} merge)")}


def build(config, raw_prs):
    folder = input_dir(config["period"]) / "manajemen_kode"
    folder.mkdir(exist_ok=True)
    for old in folder.glob("github_*.png"):
        old.unlink()
    keterangan = github_images(config, raw_prs, folder)
    keterangan.update(terminal_image(config, folder))
    (folder / "keterangan.json").write_text(json.dumps(keterangan, ensure_ascii=False, indent=2) + "\n",
                                            encoding="utf-8")
    return folder, keterangan

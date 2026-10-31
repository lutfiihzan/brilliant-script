# -*- coding: utf-8 -*-
"""Ambil data PR dari GitHub lewat `gh` CLI (opsional memakai token GitHub App)."""
import json
import os
import subprocess
import time

from .config import ROOT, input_dir


def _env(gh_cfg):
    """Environment untuk `gh`; isi GH_TOKEN bila kredensial GitHub App tersedia."""
    env = os.environ.copy()
    if not (gh_cfg.get("app_id") and gh_cfg.get("pem_path") and gh_cfg.get("installation_id")):
        return env
    try:
        import jwt
        import requests
    except ImportError as exc:
        raise ImportError("Autentikasi GitHub App butuh: pip install PyJWT requests") from exc

    pem_path = ROOT / gh_cfg["pem_path"]
    now = int(time.time())
    token = jwt.encode({"iat": now - 60, "exp": now + 600, "iss": str(gh_cfg["app_id"])},
                       pem_path.read_bytes(), algorithm="RS256")
    resp = requests.post(
        f"https://api.github.com/app/installations/{gh_cfg['installation_id']}/access_tokens",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"},
    )
    if resp.status_code != 201:
        raise RuntimeError(f"Gagal mendapatkan token GitHub App: {resp.text}")
    env["GH_TOKEN"] = resp.json()["token"]
    return env


def _authors(gh_cfg):
    author = gh_cfg["author"]
    return [a.strip() for a in author.split(",")] if isinstance(author, str) else list(author)


def _search(repo, query, fields, env, limit=150):
    result = subprocess.run(
        ["gh", "pr", "list", "-R", repo, "-S", query, "--state", "merged",
         "-L", str(limit), "--json", fields],
        capture_output=True, text=True, encoding="utf-8", env=env,
    )
    if result.returncode != 0:
        raise RuntimeError(f"gh gagal ({query}): {result.stderr}")
    return json.loads(result.stdout or "[]")


def _unique(prs):
    seen, out = set(), []
    for pr in prs:
        if pr["number"] not in seen:
            seen.add(pr["number"])
            out.append(pr)
    return out


def fetch_prs(config):
    """PR untuk laporan (prs.json): dibuat dalam date_ranges periode, sudah di-merge."""
    gh = config["github"]
    env = _env(gh)
    prs = []
    for dr in gh["date_ranges"]:
        for author in _authors(gh):
            prs += _search(gh["repo"], f"author:{author} created:{dr}", "number,title,state", env, limit=100)
    return sorted(_unique(prs), key=lambda p: p["number"])


def fetch_raw_prs(config):
    """PR untuk weekly report (raw_prs.json): di-merge dalam bulan periode, lengkap dengan body."""
    gh = config["github"]
    env = _env(gh)
    ym = f"{config['tahun']}-{int(config['period'][4:]):02d}"
    query_date = f"merged:{ym}-01..{ym}-{config['akhir_bulan']:02d}"
    prs = []
    for author in _authors(gh):
        prs += _search(gh["repo"], f"author:{author} {query_date}", "number,title,mergedAt,url,body", env)
    return sorted(_unique(prs), key=lambda p: p["mergedAt"])


def fetch_diffs(config, prs):
    gh = config["github"]
    env = _env(gh)
    diffs = {}
    print(f"Mengambil diff {len(prs)} PR...")
    for pr in prs:
        result = subprocess.run(["gh", "pr", "diff", str(pr["number"]), "--repo", gh["repo"]],
                                capture_output=True, text=True, encoding="utf-8", env=env)
        if result.returncode == 0:
            diffs[str(pr["number"])] = result.stdout
        else:
            diffs[str(pr["number"])] = "Gagal mengambil diff: " + result.stderr
            print(f"Gagal mengambil diff PR {pr['number']}")
    return diffs


def _cached(path, fetch, force):
    if path.exists() and not force:
        return json.loads(path.read_text(encoding="utf-8"))
    data = fetch()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


def load_prs(config, force=False):
    gh = config["github"]
    force = force or gh.get("fetch_always", False)
    path = input_dir(config["period"]) / "prs.json"
    if not path.exists() and not force and not gh.get("fetch_if_missing", True):
        return []
    prs = _cached(path, lambda: fetch_prs(config), force)
    return sorted(prs, key=lambda p: p["number"])


def load_diffs(config, prs, force=False):
    force = force or config["github"].get("fetch_always", False)
    return _cached(input_dir(config["period"]) / "prs_diff.json", lambda: fetch_diffs(config, prs), force)


def load_raw_prs(config, force=False):
    return _cached(input_dir(config["period"]) / "raw_prs.json", lambda: fetch_raw_prs(config), force)

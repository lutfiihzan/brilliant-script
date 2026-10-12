# -*- coding: utf-8 -*-
"""Sumber PR dari clone lokal (merge commit "Merge pull request #N from ...").

Dipakai untuk periode yang repo GitHub-nya sudah tidak bisa diakses
(mis. setditjen-psdkp/api-sip sebelum pindah ke psdkplabs/sipservice).
Aktif bila config.github.local_repo_path diisi.

Item yang dihasilkan per periode (kombinasi):
  1. PR yang di-merge pada periode tsb (number = int).
  2. Commit yang DIBUAT pada periode tsb tetapi PR-nya baru di-merge setelah
     periode / tidak pernah di-merge, dikelompokkan per PR/branch
     (number = "WIP-<PR atau branch>", dengan daftar "commits").
"""
import re
import subprocess

MERGE_RE = re.compile(r"Merge pull request #(\d+) from (\S+)")
# Rentang lookback untuk memetakan commit ke PR yang memuatnya
LOOKBACK_SINCE = "2025-01-01"


def _git(repo_path, *args):
    r = subprocess.run(["git", "-C", repo_path, *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError("git " + " ".join(args) + " gagal: " + r.stderr)
    return r.stdout


def _since_until(date_ranges):
    starts = [dr.split("..")[0] for dr in date_ranges]
    ends = [dr.split("..")[1] for dr in date_ranges]
    return min(starts), max(ends)


def _all_merges(repo_path, since, until):
    out = _git(repo_path, "log", "--all", "--merges", f"--since={since} 00:00", f"--until={until} 23:59:59",
               "--format=%H%x1f%ad%x1f%s%x1f%b%x1e", "--date=short")
    prs = {}
    for rec in out.split("\x1e"):
        parts = rec.strip("\n").split("\x1f")
        if len(parts) < 4:
            continue
        sha, date, subject, body = parts
        m = MERGE_RE.match(subject)
        if not m:
            continue
        num = int(m.group(1))
        # merge pertama (paling awal) yang dipakai
        if num in prs and prs[num]["mergedAt"] <= date:
            continue
        title = body.strip().splitlines()[0] if body.strip() else m.group(2)
        prs[num] = {
            "number": num, "title": title, "state": "MERGED",
            "sha": sha, "branch": m.group(2).split("/", 1)[-1], "mergedAt": date,
        }
    return prs


def _wip_items(repo_path, since, until, merges_all):
    """Commit periode ini yang PR-nya di-merge setelah periode atau tidak pernah."""
    owner = {}
    for pr in sorted(merges_all.values(), key=lambda p: p["mergedAt"]):
        for c in _git(repo_path, "log", "--no-merges", "--format=%H", f"{pr['sha']}^1..{pr['sha']}^2").split():
            owner.setdefault(c, pr)
    rows = _git(repo_path, "log", "--all", "--no-merges", f"--since={since} 00:00", f"--until={until} 23:59:59",
                "--format=%H%x1f%ad%x1f%s", "--date=short").splitlines()
    groups = {}
    for row in rows:
        sha, date, subject = row.split("\x1f", 2)
        if subject.startswith("Revert "):
            continue
        pr = owner.get(sha)
        if pr and pr["mergedAt"] <= until:
            continue
        key = f"WIP-{pr['number']}" if pr else "WIP-tanpa-PR"
        g = groups.setdefault(key, {
            "number": key, "state": "WIP", "commits": [], "mergedAt": None,
            "branch": pr["branch"] if pr else "-",
            "title": (f"{pr['title']} (dikerjakan, di-merge #{pr['number']} {pr['mergedAt']})"
                      if pr else "Commit langsung tanpa pull request"),
        })
        g["commits"].append(sha)
        g["mergedAt"] = max(g["mergedAt"] or date, date)
    return list(groups.values())


def list_merged_prs(repo_path, date_ranges):
    """Return PR merged di periode + item WIP, urut nomor (int dulu, lalu WIP)."""
    since, until = _since_until(date_ranges)
    merges_all = _all_merges(repo_path, LOOKBACK_SINCE, "2099-12-31")
    merged = [p for p in merges_all.values() if since <= p["mergedAt"] <= until]
    items = sorted(merged, key=lambda p: p["number"]) + _wip_items(repo_path, since, until, merges_all)
    return items


def _is_wip(pr):
    return bool(pr.get("commits"))


def pr_detail(repo_path, pr):
    """Body = pesan commit, files = file yang berubah."""
    if _is_wip(pr):
        shas = pr["commits"]
        files = sorted({f for f in _git(repo_path, "show", "--name-only", "--format=", *shas).splitlines() if f})
        commits = [f"- {s}" for s in _git(repo_path, "show", "-s", "--format=%s", *shas).splitlines()]
        sha = shas[0]
    else:
        sha = pr["sha"]
        files = [f for f in _git(repo_path, "diff", "--name-only", f"{sha}^1", sha).splitlines() if f]
        commits = _git(repo_path, "log", "--format=- %s", f"{sha}^1..{sha}^2").splitlines()
    return {
        "number": pr["number"], "title": pr["title"], "mergedAt": pr["mergedAt"],
        "headRefName": pr["branch"], "sha": sha, "files": files, "body": "\n".join(commits),
    }


def pr_diff(repo_path, pr):
    if _is_wip(pr):
        return _git(repo_path, "show", "--format=commit %h %s", *reversed(pr["commits"]))
    return _git(repo_path, "diff", f"{pr['sha']}^1", pr["sha"])

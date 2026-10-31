# -*- coding: utf-8 -*-
import json
import re
import subprocess
from functools import lru_cache

PR_URL_RE = re.compile(r"github\.com/[^/]+/[^/]+/(?:pull|commit)/(\d+|[a-f0-9]{40})", re.I)


def extract_pr_numbers(text):
    numbers = []
    for m in PR_URL_RE.finditer(text or ""):
        val = m.group(1)
        if val.isdigit():
            numbers.append(int(val))
    return list(dict.fromkeys(numbers))


@lru_cache(maxsize=512)
def fetch_pr_detail(repo, pr_number):
    result = subprocess.run(
        ["gh", "pr", "view", str(pr_number), "--repo", repo,
         "--json", "title,body,files,additions,deletions,state"],
        capture_output=True, text=True, encoding="utf-8",
    )
    if result.returncode != 0:
        return None
    data = json.loads(result.stdout or "{}")
    data["number"] = pr_number
    return data


def pr_files(detail):
    if not detail:
        return []
    return [f["path"] for f in detail.get("files", []) if f.get("path")]


def pr_title(detail):
    return (detail or {}).get("title", "")


DIFF_FILE_RE = re.compile(r"^diff --git a/(\S+) b/(\S+)", re.M)


def local_pr_detail(number, prs_by_num, diffs):
    """Detail PR dari prs.json + prs_diff.json lokal (tanpa memanggil gh)."""
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
    return {
        "number": number,
        "title": (pr or {}).get("title", ""),
        "files": [{"path": f} for f in files],
        "additions": adds,
        "deletions": dels,
    }


def build_utama_from_details(details):
    items = []
    for detail in details:
        title = detail.get("title", "")
        if len(title) > 75:
            title = title[:72].rstrip() + "…"
        items.append(f"PR #{detail['number']}: {title} (+{detail['additions']}/-{detail['deletions']} baris).")
    return items


def build_utama_from_prs(repo, pr_numbers):
    items = []
    for num in pr_numbers:
        detail = fetch_pr_detail(repo, num)
        if not detail:
            continue
        title = detail.get("title", "")
        adds = detail.get("additions", 0)
        dels = detail.get("deletions", 0)
        items.append(f"PR #{num}: {title} (+{adds}/-{dels} baris).")
    return items

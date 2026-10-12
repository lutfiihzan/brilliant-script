# -*- coding: utf-8 -*-
"""
Bangun detail_github.md bergaya laporan Mei dari pengelompokan PR yang dikurasi.

Input:
  input/YYYYMM/detail_groups.json  - modul -> sub-kegiatan -> daftar PR + narasi
  input/YYYYMM/prs_detail.json     - body & file per PR (auto-fetch via gh jika belum ada)

Usage:
  python generator/build_detail_from_groups.py 202609 [--fetch]
"""
import argparse
import collections
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.config import input_dir, load_config
from lib.github import get_env_with_token

MAX_FILES = 10
SKIP_PREFIX = ("docs/", "tests/", ".agents/", ".claude/", "storage/", "public/")


def fetch_pr_details(repo, prs, gh_config=None):
    env = get_env_with_token(gh_config or {})
    out = []
    for p in prs:
        r = subprocess.run(
            ["gh", "pr", "view", str(p["number"]), "-R", repo,
             "--json", "number,title,body,files,mergedAt,headRefName"],
            capture_output=True, text=True, encoding="utf-8", env=env,
        )
        if r.returncode != 0:
            raise RuntimeError(f"gh pr view #{p['number']} gagal: {r.stderr}")
        d = json.loads(r.stdout)
        d["files"] = [f["path"] for f in d["files"]]
        out.append(d)
    return out


def collect_files(numbers, details):
    counter = collections.Counter()
    for n in numbers:
        for f in details.get(n, {}).get("files", []):
            if f.startswith(SKIP_PREFIX) or f.endswith(".md"):
                continue
            counter[f] += 1
    return [f for f, _ in counter.most_common(MAX_FILES)]


def doc_link(repo, number, details):
    # PR dari clone lokal (repo lama tanpa PR) ditautkan ke merge commit di repo backup
    sha = details.get(number, {}).get("sha")
    if sha:
        return f"https://github.com/{repo}/commit/{sha}"
    return f"https://github.com/{repo}/pull/{number}"


def render(groups, details, repo):
    lines = ["# DETAIL LAPORAN KEGIATAN GITHUB", ""]
    for i, mod in enumerate(groups["modules"], 1):
        lines += [f"## {i}. {mod['title']}", "", mod["intro"], ""]
        for j, act in enumerate(mod["activities"], 1):
            nums = act["prs"]
            lines += [f"### {i}.{j} {act['subtitle']}", ""]
            if act.get("prolog"):
                lines += ["**Prolog**", act["prolog"], ""]
            lines += ["**Deskripsi Pekerjaan**", act["deskripsi"], "", "**Detail Perubahan**", ""]
            files = act.get("files") or collect_files(nums, details)
            if files:
                lines += ["**File yang Diubah:**"] + [f"- {f}" for f in files] + [""]
            if act.get("utama"):
                lines += ["**Perubahan Utama:**"] + [f"- {u}" for u in act["utama"]] + [""]
            if act.get("manfaat"):
                lines += ["**Manfaat:**"] + [f"- {m}" for m in act["manfaat"]] + [""]
            lines += ["**Dokumentasi**"] + [f"- {doc_link(repo, n, details)}" for n in nums]
            lines += ["", "---", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("period")
    ap.add_argument("--fetch", action="store_true", help="Paksa fetch ulang prs_detail.json")
    args = ap.parse_args()

    config = load_config(args.period)
    repo = config["github"]["repo"]
    inp = input_dir(args.period)
    prs = json.loads((inp / "prs.json").read_text(encoding="utf-8"))

    detail_path = inp / "prs_detail.json"
    if args.fetch or not detail_path.exists():
        local = config["github"].get("local_repo_path")
        print(f"Fetch detail {len(prs)} PR dari {local or repo}...")
        if local:
            from lib.local_git import pr_detail
            details = [pr_detail(local, p) for p in prs]
        else:
            details = fetch_pr_details(repo, prs, config["github"])
        detail_path.write_text(json.dumps(details, ensure_ascii=False, indent=1), encoding="utf-8")
    details = {d["number"]: d for d in json.loads(detail_path.read_text(encoding="utf-8"))}

    groups = json.loads((inp / "detail_groups.json").read_text(encoding="utf-8"))

    used = [n for m in groups["modules"] for a in m["activities"] for n in a["prs"]]
    all_nums = {p["number"] for p in prs}
    # "exclude": PR sinkronisasi branch (mis. merge master -> internal) yang bukan pekerjaan baru
    excluded = set(groups.get("exclude", []))
    missing = sorted(all_nums - set(used) - excluded)
    dup = sorted(n for n, c in collections.Counter(used).items() if c > 1)
    unknown = sorted(set(used) - all_nums)
    if missing:
        print("WARNING: PR belum dikelompokkan:", missing)
    if dup:
        print("WARNING: PR muncul di lebih dari satu kegiatan:", dup)
    if unknown:
        print("WARNING: PR tidak ada di prs.json:", unknown)

    out = inp / "detail_github.md"
    out.write_text(render(groups, details, repo), encoding="utf-8")
    n_act = sum(len(m["activities"]) for m in groups["modules"])
    print(f"Selesai: {out} ({len(groups['modules'])} modul, {n_act} kegiatan, {len(set(used))}/{len(all_nums)} PR)")


if __name__ == "__main__":
    main()

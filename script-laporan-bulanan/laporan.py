# -*- coding: utf-8 -*-
"""Generator Laporan Bulanan — satu pintu untuk seluruh alur kerja.

  python laporan.py init     202611 [--from 202610]   siapkan input/202611/ dari template/input/
  python laporan.py fetch    202611 [--force]         ambil PR (raw_prs.json, prs.json, prs_diff.json)
  python laporan.py weekly   202611 --digest [A B]    ringkasan PR sebagai bahan curated.json
  python laporan.py weekly   202611 --build           susun weekly_report.md (curated.json / PR mentah)
  python laporan.py weekly   202611                   cek kualitas weekly_report.md + buat weekly_report.docx
  python laporan.py detail   202611                   detail_github.md dari weekly_report.md
          (opsi: --add-prolog | --refresh-prolog | --to-txt | --prompt)
  python laporan.py report   202611 [--fetch-prs]     laporan Word final -> output/202611/
  python laporan.py all      202611                   weekly (docx) + detail + report
  python laporan.py template                          bangun ulang template/*.docx dari archive/template_lama/
"""
import argparse
import json
import shutil
import sys

from generator import detail, github, report, template_builder, weekly
from generator.config import ROOT, TEMPLATE_DIR, input_dir, load_config, output_dir, period_defaults

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def cmd_init(args):
    target = input_dir(args.period)
    target.mkdir(parents=True, exist_ok=True)
    (target / "manajemen_kode").mkdir(exist_ok=True)
    output_dir(args.period)

    src_cfg = input_dir(args.source) / "config.json" if args.source else TEMPLATE_DIR / "input" / "config.json"
    cfg = json.loads(src_cfg.read_text(encoding="utf-8"))
    # Field bulanan diturunkan otomatis dari periode; isi BAB I/III dikosongkan untuk bulan baru
    for key in ("period", "bulan", "bulan_up", "tahun", "output_filename", "detail_docx", "detail_txt",
                "code_snippet", "media"):
        cfg.pop(key, None)
    cfg.get("github", {}).pop("date_ranges", None)
    cfg["bab1"] = {"pencapaian": "", "tantangan": ""}
    cfg["bab3"] = {"kesimpulan_items": []}
    cfg_path = target / "config.json"
    if cfg_path.exists():
        print("config.json sudah ada, tidak ditimpa:", cfg_path)
    else:
        cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for name in ("kegiatan_tambahan.json",):
        if not (target / name).exists():
            shutil.copy2(TEMPLATE_DIR / "input" / name, target / name)

    d = period_defaults(args.period)
    print(f"Folder siap: {target} ({d['bulan']} {d['tahun']})")
    print("Langkah berikutnya:")
    print(f"  python laporan.py fetch {args.period}")
    print(f"  python laporan.py weekly {args.period} --digest   (lalu tulis curated.json)")
    print(f"  python laporan.py weekly {args.period} --build")
    print(f"  python laporan.py all {args.period}")


def cmd_fetch(args):
    config = load_config(args.period)
    raw = github.load_raw_prs(config, force=args.force)
    prs = github.load_prs(config, force=args.force)
    github.load_diffs(config, prs, force=args.force)
    print(f"raw_prs.json: {len(raw)} PR | prs.json: {len(prs)} PR | prs_diff.json siap")


def cmd_weekly(args):
    config = load_config(args.period)
    inp = input_dir(args.period)
    if args.digest is not None:
        raw = github.load_raw_prs(config)
        start = args.digest[0] if args.digest else 0
        end = args.digest[1] if len(args.digest) > 1 else None
        weekly.digest(raw, start, end)
        return
    if args.build:
        weekly.build_md(args.period, github.load_raw_prs(config), config.get("weekly_user_filter", "Lutfi"))

    md_path = inp / "weekly_report.md"
    problems = weekly.check_md(md_path)
    print(f"Cek kualitas weekly_report.md: {len(problems)} catatan")
    for p in problems[:40]:
        print(" -", p)
    out, count = weekly.to_docx(args.period, config)
    print(f"Selesai: {out} ({count} baris)")


def cmd_detail(args):
    config = load_config(args.period)
    md_path = input_dir(args.period) / "detail_github.md"
    if args.prompt:
        prompts = input_dir(args.period) / "prompts"
        prompts.mkdir(exist_ok=True)
        out = prompts / "CURSOR_ENRICH_DETAIL.md"
        out.write_text(detail.build_enrich_prompt(args.period), encoding="utf-8")
        print("Prompt AI:", out)
        return
    if args.add_prolog or args.refresh_prolog or args.to_txt:
        if not md_path.exists():
            sys.exit(f"File tidak ada: {md_path}")
        content = md_path.read_text(encoding="utf-8")
        if not args.to_txt:
            content = detail.inject_prologs(content, refresh=args.refresh_prolog)
    else:
        content = detail.build_from_weekly(config)
    md, txt = detail.save(content, args.period)
    print("MD :", md)
    print("TXT:", txt)


def cmd_report(args):
    report.build(load_config(args.period), force_fetch=args.fetch_prs)


def cmd_all(args):
    args.digest, args.build = None, False
    cmd_weekly(args)
    args.prompt = args.add_prolog = args.refresh_prolog = args.to_txt = False
    if (input_dir(args.period) / "detail_github.md").exists():
        print("detail_github.md sudah ada, dipakai apa adanya (buat ulang: python laporan.py detail", args.period + ")")
    else:
        cmd_detail(args)
    args.fetch_prs = False
    cmd_report(args)


def cmd_template(args):
    for path in template_builder.build_all():
        print("Template:", path.relative_to(ROOT))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="siapkan folder input bulan baru")
    p.add_argument("period")
    p.add_argument("--from", dest="source", help="salin config dari periode sebelumnya")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("fetch", help="ambil data PR dari GitHub")
    p.add_argument("period")
    p.add_argument("--force", action="store_true", help="abaikan cache, ambil ulang")
    p.set_defaults(func=cmd_fetch)

    p = sub.add_parser("weekly", help="weekly report (md -> docx)")
    p.add_argument("period")
    p.add_argument("--digest", nargs="*", type=int, metavar="N", help="cetak ringkasan PR [mulai akhir]")
    p.add_argument("--build", action="store_true", help="susun ulang weekly_report.md dari raw_prs.json")
    p.set_defaults(func=cmd_weekly)

    p = sub.add_parser("detail", help="detail_github.md untuk BAB II")
    p.add_argument("period")
    for flag in ("--add-prolog", "--refresh-prolog", "--to-txt", "--prompt"):
        p.add_argument(flag, action="store_true")
    p.set_defaults(func=cmd_detail)

    p = sub.add_parser("report", help="laporan Word final")
    p.add_argument("period")
    p.add_argument("--fetch-prs", action="store_true", help="ambil ulang PR & diff dari GitHub")
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("all", help="weekly + detail + report")
    p.add_argument("period")
    p.set_defaults(func=cmd_all)

    p = sub.add_parser("template", help="bangun ulang template Word")
    p.set_defaults(func=cmd_template)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Generate detail_github.md + .txt dari weekly report + PR GitHub.

Contoh:
  python generator/generate_detail_md.py 202605 --from-weekly
  python generator/generate_detail_md.py 202605 --add-prolog
  python generator/generate_detail_md.py 202605 --to-txt
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.config import input_dir, load_config
from lib.detail_md_builder import build_enrich_prompt, build_from_weekly, inject_prologs
from lib.md_to_txt import save_detail_outputs


def main():
    parser = argparse.ArgumentParser(description="Generate detail_github.md + .txt")
    parser.add_argument("period", help="YYYYMM contoh 202605")
    parser.add_argument("--from-weekly", action="store_true")
    parser.add_argument("--add-prolog", action="store_true")
    parser.add_argument("--refresh-prolog", action="store_true")
    parser.add_argument("--to-txt", action="store_true")
    parser.add_argument("--prompt", action="store_true")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    from lib.config import project_root, weekly_report_path

    config = load_config(args.period)
    inp = input_dir(args.period)
    out_path = Path(args.output) if args.output else inp / "detail_github.md"
    weekly_path = weekly_report_path(args.period)

    if args.from_weekly:
        md = build_from_weekly(weekly_path, config, config.get("weekly_user_filter", "Lutfi"))
        paths = save_detail_outputs(md, args.period, project_root)
        print("MD  :", paths["input_md"])
        print("TXT :", paths["input_txt"])
        print("Langkah berikutnya: python generator/generate_detail_md.py", args.period, "--prompt")
        return

    if args.add_prolog or args.refresh_prolog:
        if not out_path.exists():
            print("File tidak ada:", out_path)
            sys.exit(1)
        updated = inject_prologs(out_path.read_text(encoding="utf-8"), refresh=args.refresh_prolog)
        paths = save_detail_outputs(updated, args.period, project_root)
        print("Diperbarui:", paths["input_md"])
        print("TXT     :", paths["input_txt"])
        return

    if args.to_txt:
        if not out_path.exists():
            print("File tidak ada:", out_path)
            sys.exit(1)
        paths = save_detail_outputs(out_path.read_text(encoding="utf-8"), args.period, project_root)
        print("TXT:", paths["input_txt"])
        return

    if args.prompt:
        if not out_path.exists():
            print("File tidak ada:", out_path)
            sys.exit(1)
        prompts_dir = inp / "prompts"
        prompts_dir.mkdir(exist_ok=True)
        prompt_path = prompts_dir / "CURSOR_ENRICH_DETAIL.md"
        prompt_path.write_text(build_enrich_prompt(out_path, args.period), encoding="utf-8")
        print("Prompt Cursor:", prompt_path)
        return

    parser.print_help()


if __name__ == "__main__":
    main()

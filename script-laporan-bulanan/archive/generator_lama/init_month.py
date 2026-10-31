# -*- coding: utf-8 -*-
import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description="Inisialisasi folder input bulan baru")
    parser.add_argument("period", help="YYYYMM contoh 202606")
    parser.add_argument("--from", dest="source", default=None, help="Salin dari periode sebelumnya")
    args = parser.parse_args()

    target = ROOT / "input" / args.period
    target.mkdir(parents=True, exist_ok=True)
    (target / "prompts").mkdir(exist_ok=True)
    (ROOT / "output" / args.period).mkdir(parents=True, exist_ok=True)

    if args.source:
        src = ROOT / "input" / args.source
        for name in ["kegiatan_tambahan.json"]:
            if (src / name).exists():
                shutil.copy2(src / name, target / name)

    template = json.loads((ROOT / "generator" / "config_template.json").read_text(encoding="utf-8"))
    template.pop("_petunjuk", None)
    template["period"] = args.period
    (target / "config.json").write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")

    for fname, content in {
        "weekly_report.md": "# Weekly Report\n",
        "detail_github.md": "# DETAIL LAPORAN KEGIATAN GITHUB\n\n## 1. Judul Modul\n",
    }.items():
        path = target / fname
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    print("Folder siap:", target)
    print("Edit config.json, weekly_report.md, detail_github.md lalu jalankan:")
    print("  python generator/generate.py", args.period)


if __name__ == "__main__":
    main()

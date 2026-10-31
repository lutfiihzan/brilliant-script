# -*- coding: utf-8 -*-
"""Lokasi folder dan pemuatan config.json per periode (YYYYMM)."""
import calendar
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "template"
GENERATOR_DIR = ROOT / "generator"

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]


def input_dir(period):
    return ROOT / "input" / period


def output_dir(period):
    path = ROOT / "output" / period
    path.mkdir(parents=True, exist_ok=True)
    return path


def period_defaults(period, nama="Lutfi Ihsan"):
    """Field yang selalu bisa diturunkan dari periode."""
    tahun, bulan_no = int(period[:4]), int(period[4:])
    bulan = BULAN[bulan_no - 1]
    akhir = calendar.monthrange(tahun, bulan_no)[1]
    ym = f"{tahun}-{bulan_no:02d}"
    return {
        "period": period,
        "bulan": bulan,
        "bulan_up": bulan.upper(),
        "tahun": tahun,
        "akhir_bulan": akhir,
        "output_filename": f"Laporan Bulanan_{nama} - {bulan} {tahun}.docx",
        "date_ranges": [f"{ym}-01..{ym}-10", f"{ym}-11..{ym}-20", f"{ym}-21..{ym}-{akhir:02d}"],
    }


def load_config(period):
    path = input_dir(period) / "config.json"
    if not path.exists():
        raise FileNotFoundError(f"Config tidak ditemukan: {path} (jalankan: python laporan.py init {period})")
    cfg = json.loads(path.read_text(encoding="utf-8"))

    defaults = period_defaults(period, cfg.get("nama", "Lutfi Ihsan"))
    gh = cfg.setdefault("github", {})
    gh.setdefault("date_ranges", defaults.pop("date_ranges"))
    for key, val in defaults.items():
        cfg.setdefault(key, val)
    cfg["period"] = period

    # Kredensial GitHub App bersama (opsional) dari config_global.json
    global_path = ROOT / "config_global.json"
    if global_path.exists():
        for key, val in json.loads(global_path.read_text(encoding="utf-8")).get("github", {}).items():
            gh.setdefault(key, val)
    return cfg

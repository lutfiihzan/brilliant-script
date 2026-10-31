# -*- coding: utf-8 -*-
import json
from pathlib import Path


def load_modules_config():
    path = Path(__file__).resolve().parent.parent / "modules.json"
    if not path.exists():
        path = Path(__file__).resolve().parent / "modules.json"
    return json.loads(path.read_text(encoding="utf-8"))


def match_module(activity, output, modules_cfg):
    """Pilih modul berdasarkan kata kunci; kata kunci pada activity lebih berbobot."""
    activity_text = (activity or "").lower()
    output_text = (output or "").lower()
    best = None
    best_score = 0
    for mod in modules_cfg["modules"]:
        score = 2 * sum(1 for kw in mod["keywords"] if kw.lower() in activity_text)
        score += sum(1 for kw in mod["keywords"] if kw.lower() in output_text)
        if score > best_score:
            best_score = score
            best = mod
    return best


def build_module_intro(mod, modules_cfg):
    tpl = modules_cfg.get("module_intro_template", "")
    return tpl.format(verb=mod["verb"], modul=mod["modul"])


def _activity_phrase(activity):
    if not activity:
        return activity
    lower = activity.lower()
    if lower.startswith(("men", "mem", "me", "per", "pen", "meny", "meng")):
        return activity[0].lower() + activity[1:]
    return f"melakukan {activity[0].lower() + activity[1:]}"


def build_prolog(activity, mod, output, modules_cfg):
    tpl = modules_cfg.get("prolog_template", "")
    konteks = ""
    if output and len(output) > 20:
        # Ambil kalimat pertama; jika masih panjang, potong di batas kata
        short = output.strip().split(". ")[0].strip()
        if len(short) > 200:
            short = short[:200].rsplit(" ", 1)[0].rstrip(",;:")
        if not short.endswith("."):
            short += "."
        konteks = f" Kegiatan ini berkaitan dengan: {short}"
    kegiatan = _activity_phrase(activity)
    return tpl.format(kegiatan=kegiatan, modul=mod["modul"], konteks=konteks)

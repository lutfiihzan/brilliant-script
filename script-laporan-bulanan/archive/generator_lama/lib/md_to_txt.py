# -*- coding: utf-8 -*-
import re


def md_to_txt(md_content):
    lines = []
    for raw in md_content.splitlines():
        line = raw.rstrip()
        if not line.strip():
            lines.append("")
            continue
        if line.strip() == "---":
            lines.append("-" * 72)
            continue
        if line.strip().startswith("<!--") and line.strip().endswith("-->"):
            continue

        line = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", line)
        line = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", line)
        line = re.sub(r"`([^`]+)`", r"\1", line)
        line = re.sub(r"\*\*([^*]+)\*\*", r"\1", line)
        line = re.sub(r"\*([^*]+)\*", r"\1", line)

        if line.startswith("# "):
            title = line[2:].strip()
            lines.extend(["", title.upper(), "=" * len(title), ""])
            continue
        if line.startswith("## "):
            title = line[3:].strip()
            lines.extend(["", title, "-" * len(title), ""])
            continue
        if line.startswith("### "):
            lines.extend(["", line[4:].strip(), ""])
            continue
        if line.startswith("> "):
            lines.append(line[2:].strip())
            continue
        if line.startswith("- "):
            lines.append("  * " + line[2:].strip())
            continue

        lines.append(line)

    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def save_detail_outputs(md_content, period, project_root_fn):
    root = project_root_fn()
    inp = root / "input" / period
    inp.mkdir(parents=True, exist_ok=True)

    paths = {
        "input_md": inp / "detail_github.md",
        "input_txt": inp / "detail_github.txt",
    }
    txt_content = md_to_txt(md_content)
    paths["input_md"].write_text(md_content, encoding="utf-8")
    paths["input_txt"].write_text(txt_content, encoding="utf-8")
    return paths

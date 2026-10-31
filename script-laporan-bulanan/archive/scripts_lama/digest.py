import json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

prs = json.loads(Path('input/202610/raw_prs.json').read_text(encoding='utf-8'))


def clean(s):
    s = re.sub(r'\r', ' ', s or '')
    s = re.sub(r'```.*?```', ' ', s, flags=re.S)
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = re.sub(r'[#*`>|]+', ' ', s)
    s = re.sub(r'[\ufffd\u0000-\u001f]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


start = int(sys.argv[1])
end = int(sys.argv[2])
blen = int(sys.argv[3]) if len(sys.argv) > 3 else 220
for i, p in enumerate(prs[start:end], start + 1):
    print(f"{i}. #{p['number']} {p['mergedAt'][:10]} :: {clean(p['title'])}")
    b = clean(p.get('body', ''))
    if b:
        print(f"   B: {b[:blen]}")

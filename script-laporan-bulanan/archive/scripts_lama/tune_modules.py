import json
from pathlib import Path

p = Path('generator/modules.json')
cfg = json.loads(p.read_text(encoding='utf-8'))
for m in cfg['modules']:
    if m['id'] == 'user' and 'token' not in m['keywords']:
        m['keywords'].append('token')
    if m['id'] == 'gateway':
        for kw in ['simpandataproyek', 'simpan data proyek']:
            if kw not in m['keywords']:
                m['keywords'].append(kw)
p.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('ok')

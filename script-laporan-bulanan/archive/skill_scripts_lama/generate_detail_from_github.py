import json
import subprocess
import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Generate detail_github.md using direct PR descriptions")
    parser.add_argument("period", help="YYYYMM contoh 202608")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent.parent.parent.parent / "script-laporan-bulanan"
    config_path = root / "input" / args.period / "config.json"
    
    if not config_path.exists():
        print(f"Error: Config {config_path} tidak ditemukan.")
        sys.exit(1)

    with open(config_path, encoding='utf-8') as f:
        config = json.load(f)

    # Load global config for GitHub App credentials
    global_config_path = root / "config_global.json"
    if global_config_path.exists():
        with open(global_config_path, encoding='utf-8') as f:
            g_config = json.load(f)
            config.update(g_config)

    repo = config.get("github", {}).get("repo")
    author = config.get("github", {}).get("author")
    tahun = int(config.get("tahun"))
    bulan_int = int(args.period[-2:])
    
    import calendar
    last_day = calendar.monthrange(tahun, bulan_int)[1]
    bulan_str = f"{bulan_int:02d}"
    
    date_query = f"merged:{tahun}-{bulan_str}-01..{tahun}-{bulan_str}-{last_day}"
    
    authors = [a.strip() for a in author.split(',')]
    
    sys.path.append(str(root / "generator"))
    try:
        from lib import github as gh_lib
        env = gh_lib.get_env_with_token(config.get("github", {}))
    except Exception as e:
        print(f"Warning: gagal load GitHub App token, menggunakan env default. Error: {e}")
        env = None

    prs = []
    for auth in authors:
        print(f"Fetching PRs from {repo} for author {auth} in {date_query}...")
        cmd = ['gh', 'pr', 'list', '-R', repo, '-S', f'author:{auth} {date_query}', '--state', 'merged', '--json', 'number,title,url,body', '-L', '150']
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8', env=env)
            prs.extend(json.loads(result.stdout))
        except Exception as e:
            print(f"Error executing gh for {auth}: {e}")
            sys.exit(1)
        
    # Parse weekly_report.md to get polished titles
    weekly_path = root / "input" / args.period / "weekly_report.md"
    url_to_title = {}
    if weekly_path.exists():
        for line in weekly_path.read_text(encoding='utf-8').splitlines():
            if line.startswith("|") and not "Weekly" in line and not "-----" in line:
                cols = [c.strip() for c in line.split("|")[1:-1]]
                if len(cols) >= 7:
                    activity = cols[3]
                    url = cols[6]
                    url_to_title[url] = activity

    prs.sort(key=lambda x: x['number'])

    md_lines = ["# DETAIL LAPORAN KEGIATAN GITHUB\n\n## 1. Pelaksanaan Kegiatan Pengembangan Sistem\n\nPada periode ini, telah dilakukan berbagai pengembangan fitur, perbaikan bug, dan optimasi pada repositori utama. Berikut adalah rincian masing-masing pull request:\n"]

    for i, pr in enumerate(prs, 1):
        url = pr['url']
        title = url_to_title.get(url, pr['title']) # Use polished title if available
        body = pr.get('body', '').strip()
        
        # Downgrade headers so they don't break the document TOC
        safe_body = []
        for line in body.split('\n'):
            if line.startswith('### '):
                safe_body.append('###### ' + line[4:])
            elif line.startswith('## '):
                safe_body.append('##### ' + line[3:])
            elif line.startswith('# '):
                safe_body.append('#### ' + line[2:])
            else:
                safe_body.append(line)
                
        body_text = '\n'.join(safe_body)
        if not body_text:
            body_text = "*(Tidak ada deskripsi spesifik, mengacu pada judul PR)*"
        
        # Use EXACT strings expected by parser.py (no colons)
        section = f"### 1.{i} {title}\n\n**Deskripsi Pekerjaan**\n{body_text}\n\n**Dokumentasi**\n- {url}\n\n---\n"
        md_lines.append(section)

    out_path = root / "input" / args.period / "detail_github.md"
    out_path.write_text("\n".join(md_lines), encoding='utf-8')
    print(f"Sukses! detail_github.md berhasil dibuat untuk {len(prs)} kegiatan.")

if __name__ == "__main__":
    main()

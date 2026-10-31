import json
import subprocess
import datetime
import argparse
import sys
import os
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Fetch PRs and generate raw weekly_report.md")
    parser.add_argument("period", help="YYYYMM contoh 202608")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent.parent.parent.parent / "script-laporan-bulanan"
    sys.path.insert(0, str(root))
    
    from generator.lib.config import load_config
    from generator.lib.github import get_env_with_token

    config = load_config(args.period)
    gh_config = config.get("github", {})
    env = get_env_with_token(gh_config)
    
    repo = gh_config.get("repo")
    author_val = gh_config.get("author")
    authors = [a.strip() for a in author_val.split(',')] if isinstance(author_val, str) else [author_val]

    tahun = int(config.get("tahun"))
    bulan_int = int(args.period[-2:])
    
    import calendar
    last_day = calendar.monthrange(tahun, bulan_int)[1]
    
    bulan_str = f"{bulan_int:02d}"
    date_query = f"merged:{tahun}-{bulan_str}-01..{tahun}-{bulan_str}-{last_day}"
    
    prs = []
    for a in authors:
        print(f"Fetching PRs from {repo} for author {a} in {date_query}...")
        cmd = ['gh', 'pr', 'list', '-R', repo, '-S', f'author:{a} {date_query}', '--state', 'merged', '--json', 'number,title,mergedAt,url,body', '-L', '150']
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, env=env, encoding="utf-8")
            if result.stdout:
                prs.extend(json.loads(result.stdout))
        except subprocess.CalledProcessError as e:
            print(f"Error executing gh: {e.stderr}")
            sys.exit(1)
            
    # Remove duplicates
    seen = set()
    unique_prs = []
    for pr in prs:
        if pr['number'] not in seen:
            seen.add(pr['number'])
            unique_prs.append(pr)
            
    prs = unique_prs
    prs.sort(key=lambda x: x['mergedAt'])

    rows = []
    for pr in prs:
        dt = datetime.datetime.fromisoformat(pr['mergedAt'].replace('Z', '+00:00'))
        day = dt.day
        
        if 1 <= day <= 10:
            cat = "W1"
            drange = "1-10"
        elif 11 <= day <= 20:
            cat = "W2"
            drange = "11-20"
        else:
            cat = "W3"
            drange = "21-31"
            
        title = pr['title'].replace('|', '-')
        body = pr.get('body', '').strip()
        
        if body:
            # Clean up newlines so it fits in one table row
            body = ' '.join(body.split())
            body = body.replace('|', '-')
        else:
            body = f"Implementasi {title}"
            
        rows.append(f"| {cat} | {drange} | {day} | {title} | {body} | Lutfi | {pr['url']} |")

    md_content = "# Weekly Report\n\nPic: Data\n\n| Weekly_ cat | date_range | date | activity | output | user | reltd_doc_link |\n| ----- | ----- | ----- | ----- | ----- | ----- | ----- |\n"
    md_content += "\n".join(rows) + "\n"

    out_path = root / "input" / args.period / "weekly_report.md"
    out_path.write_text(md_content, encoding='utf-8')
    print(f"Sukses! {len(prs)} PR telah diekstrak ke {out_path}.")
    print("Gunakan AI Prompt (PROMPT_POLES_WEEKLY.md) untuk merapikan tabel sebelum di-convert ke DOCX.")

if __name__ == "__main__":
    main()

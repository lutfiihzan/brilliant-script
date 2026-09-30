# -*- coding: utf-8 -*-
import os
import json
import subprocess
import time

try:
    import jwt
    import requests
except ImportError:
    jwt = None
    requests = None

def get_github_app_token(app_id, pem_path, installation_id):
    if jwt is None or requests is None:
        raise ImportError("Modul 'PyJWT' dan 'requests' diperlukan untuk autentikasi GitHub App. Silakan install dengan: pip install PyJWT requests")
    
    with open(pem_path, 'rb') as pem_file:
        signing_key = pem_file.read()
        
    payload = {
        'iat': int(time.time()) - 60, # Kurangi 1 menit untuk handle clock skew
        'exp': int(time.time()) + (10 * 60),
        'iss': str(app_id)
    }
    encoded_jwt = jwt.encode(payload, signing_key, algorithm='RS256')

    headers = {
        'Authorization': f'Bearer {encoded_jwt}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.post(
        f'https://api.github.com/app/installations/{installation_id}/access_tokens',
        headers=headers
    )
    
    if response.status_code == 201:
        return response.json()['token']
    else:
        raise Exception(f"Gagal mendapatkan token: {response.text}")

def get_env_with_token(gh_config):
    env = os.environ.copy()
    if gh_config.get('app_id') and gh_config.get('pem_path') and gh_config.get('installation_id'):
        token = get_github_app_token(gh_config['app_id'], gh_config['pem_path'], gh_config['installation_id'])
        env['GH_TOKEN'] = token
    return env

def fetch_prs(repo, author, date_ranges, gh_config=None):
    gh_config = gh_config or {}
    env = get_env_with_token(gh_config)
    
    authors = [a.strip() for a in author.split(',')] if isinstance(author, str) else author
    
    all_prs = []
    seen = set()
    for dr in date_ranges:
        for a in authors:
            result = subprocess.run(
                ["gh", "pr", "list", "-R", repo, "-S", f"author:{a} created:{dr}",
                 "-L", "100", "--json", "number,title,state", "--state", "merged"],
                capture_output=True, text=True, encoding="utf-8",
                env=env
            )
            if result.returncode != 0:
                raise RuntimeError("gh search gagal (" + dr + ", " + a + "): " + result.stderr)
            for pr in json.loads(result.stdout or "[]"):
                if pr["number"] not in seen:
                    seen.add(pr["number"])
                    all_prs.append(pr)
    all_prs.sort(key=lambda x: x["number"])
    return all_prs

def load_or_fetch_prs(config, prs_path):
    gh = config.get("github", {})
    if prs_path.exists() and not gh.get("fetch_always", False):
        return sorted(json.loads(prs_path.read_text(encoding="utf-8")), key=lambda x: x["number"])
    if not gh.get("fetch_if_missing", True) and not gh.get("fetch_always", False):
        return []
    prs = fetch_prs(gh["repo"], gh["author"], gh["date_ranges"], gh_config=gh)
    prs_path.write_text(json.dumps(prs, ensure_ascii=False, indent=2), encoding="utf-8")
    return prs

def fetch_diffs(repo, prs, gh_config=None):
    gh_config = gh_config or {}
    env = get_env_with_token(gh_config)
    
    diffs = {}
    print(f"Fetching diffs for {len(prs)} PRs...")
    for pr in prs:
        num = pr["number"]
        result = subprocess.run(
            ["gh", "pr", "diff", str(num), "--repo", repo],
            capture_output=True, text=True, encoding="utf-8",
            env=env
        )
        if result.returncode == 0:
            diffs[str(num)] = result.stdout
        else:
            diffs[str(num)] = "Gagal mengambil diff: " + result.stderr
            print(f"Failed to fetch diff for PR {num}")
    return diffs

def load_or_fetch_diffs(config, prs, prs_diff_path):
    gh = config.get("github", {})
    if prs_diff_path.exists() and not gh.get("fetch_always", False):
        return json.loads(prs_diff_path.read_text(encoding="utf-8"))
    
    diffs = fetch_diffs(gh["repo"], prs, gh_config=gh)
    prs_diff_path.write_text(json.dumps(diffs, ensure_ascii=False, indent=2), encoding="utf-8")
    return diffs

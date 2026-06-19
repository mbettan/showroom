#!/usr/bin/env python3
"""
fetch_repos.py
--------------
Fetches all public GitHub repositories for a given username and outputs a
pretty-printed projects.json consumed by the portfolio frontend.

USAGE:
    1. (Optional) Set a Personal Access Token to avoid rate limits:
         export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"   (macOS/Linux)
         set GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx        (Windows CMD)
         $env:GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"     (PowerShell)

    2. Run:
         python fetch_repos.py --username YOUR_GITHUB_USERNAME

    3. projects.json will be written next to this script.

REQUIREMENTS:
    pip install requests
"""

import argparse
import json
import os
import sys
from datetime import datetime

import requests

API_BASE = "https://api.github.com"
DEFAULT_DESCRIPTION = "A project worth exploring — open it to learn more."
PLACEHOLDER_THUMB = "images/placeholder.png"
IMAGES_DIR = "docs/images"

# Repos you may want to hide (forks, archived, the portfolio repo itself, etc.)
SKIP_NAMES = {"showroom", "showcase"}
SKIP_FORKS = True
SKIP_ARCHIVED = False


def clean_title(repo_name: str) -> str:
    """Turn 'my-cool-repo' / 'my_cool_repo' into 'My Cool Repo'."""
    spaced = repo_name.replace("-", " ").replace("_", " ").strip()
    # Keep common acronyms uppercase
    acronyms = {
        "api", "ai", "ml", "cli", "css", "html", "js", "ui", "ux",
        "sql", "gcp", "aws", "pdf", "json", "id", "rag", "bq", "db",
        "mcp", "adk", "stt", "tts", "ios", "poc", "llm", "uuid"
    }
    
    # Specific casing mapping for common words
    custom_casing = {
        "finops": "FinOps",
        "realestate": "RealEstate",
        "playwright": "Playwright",
    }
    
    words = []
    for w in spaced.split():
        w_lower = w.lower()
        if w_lower in acronyms:
            words.append(w.upper())
        elif w_lower in custom_casing:
            words.append(custom_casing[w_lower])
        elif any(c.isupper() for c in w[1:]):
            # If the word already has camelCase/PascalCase (upper letters inside), preserve it
            words.append(w)
        else:
            words.append(w.capitalize())
            
    return " ".join(words) if words else repo_name



def build_headers() -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
        print("🔑 Using GITHUB_TOKEN for authentication.")
    else:
        print("⚠️  No GITHUB_TOKEN found — running unauthenticated (lower rate limit).")
    return headers


def fetch_all_repos(username: str, headers: dict) -> list:
    """Paginate through all public repos."""
    repos, page = [], 1
    while True:
        url = f"{API_BASE}/users/{username}/repos"
        params = {"per_page": 100, "page": page, "sort": "updated"}
        resp = requests.get(url, headers=headers, params=params, timeout=30)

        if resp.status_code == 404:
            sys.exit(f"❌ User '{username}' not found.")
        if resp.status_code == 403:
            sys.exit("❌ Rate limited (403). Set a GITHUB_TOKEN and try again.")
        resp.raise_for_status()

        batch = resp.json()
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    print(f"📦 Fetched {len(repos)} repositories.")
    return repos


def fetch_topics(username: str, repo_name: str, headers: dict) -> list:
    """
    Topics are usually included in the repo payload, but if missing we can
    request them via the dedicated endpoint. We try the cheap path first.
    """
    url = f"{API_BASE}/repos/{username}/{repo_name}/topics"
    h = dict(headers)
    h["Accept"] = "application/vnd.github.mercy-preview+json"
    try:
        resp = requests.get(url, headers=h, timeout=15)
        if resp.status_code == 200:
            return resp.json().get("names", [])
    except requests.RequestException:
        pass
    return []


def resolve_thumbnail(repo_name: str) -> str:
    """Use local images/{repo}.png if present, else placeholder."""
    local_path = os.path.join(IMAGES_DIR, f"{repo_name}.png")
    if os.path.isfile(local_path):
        return f"images/{repo_name}.png"
    return PLACEHOLDER_THUMB


def transform(repo: dict, username: str, headers: dict) -> dict:
    repo_name = repo["name"]

    homepage = (repo.get("homepage") or "").strip()
    if not homepage:
        homepage = f"https://{username}.github.io/{repo_name}"

    topics = repo.get("topics") or []
    if not topics:
        topics = fetch_topics(username, repo_name, headers)

    return {
        "id": repo["id"],
        "name": repo_name,
        "title": clean_title(repo_name),
        "description": (repo.get("description") or DEFAULT_DESCRIPTION).strip(),
        "github_url": repo["html_url"],
        "homepage_url": homepage,
        "topics": topics,
        "language": repo.get("language") or "Other",
        "stars": repo.get("stargazers_count", 0),
        "created_at": repo.get("created_at"),
        "updated_at": repo.get("updated_at"),
        "thumbnail": resolve_thumbnail(repo_name),
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub repos → projects.json")
    parser.add_argument("--username", "-u", required=True, help="GitHub username")
    parser.add_argument("--output", "-o", default="docs/projects.json", help="Output file")
    args = parser.parse_args()

    headers = build_headers()
    raw_repos = fetch_all_repos(args.username, headers)

    projects = []
    for repo in raw_repos:
        if repo["name"] in SKIP_NAMES:
            continue
        if SKIP_FORKS and repo.get("fork"):
            continue
        if SKIP_ARCHIVED and repo.get("archived"):
            continue
        
        # Filter: Only projects starting September 6, 2025 or after (includes wealth-dashboard)
        created_at = repo.get("created_at")
        if created_at and created_at < "2025-09-06T19:40:02Z":
            continue
            
        projects.append(transform(repo, args.username, headers))

    # Sort by stars (descending), then by creation date (descending)
    projects.sort(key=lambda p: (p.get("stars", 0), p.get("created_at") or ""), reverse=True)

    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "username": args.username,
        "count": len(projects),
        "projects": projects,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"✅ Wrote {len(projects)} projects to {args.output}")


if __name__ == "__main__":
    main()

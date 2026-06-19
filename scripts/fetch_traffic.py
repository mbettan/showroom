#!/usr/bin/env python3
"""
fetch_traffic.py
----------------
Fetches 14-day traffic statistics (total views and unique visitors) for all
projects listed in docs/projects.json and displays them sorted by popularity.

USAGE:
    1. Set your GITHUB_TOKEN (must have push/repo access to these repositories):
         export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
    2. Run:
         python scripts/fetch_traffic.py
"""

import json
import os
import sys
import requests

API_BASE = "https://api.github.com"

def get_headers():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ Error: GITHUB_TOKEN environment variable is not set.")
        print("\nThe GitHub Traffic API requires authentication with push/owner permissions.")
        print("Please generate a Personal Access Token (classic or fine-grained) and set it:")
        print("    export GITHUB_TOKEN=\"your_token_here\"")
        sys.exit(1)
    
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}"
    }

def load_dotenv():
    """Load variables from .env file into os.environ if it exists."""
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(dotenv_path):
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip().strip('"').strip("'")


def main():
    load_dotenv()
    projects_file = "docs/projects.json"
    if not os.path.exists(projects_file):
        print(f"❌ Error: {projects_file} not found. Please run fetch_repos.py first.")
        sys.exit(1)

    with open(projects_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    username = data.get("username")
    projects = data.get("projects", [])

    if not username or not projects:
        print("❌ Error: projects.json is empty or invalid.")
        sys.exit(1)

    headers = get_headers()
    
    print(f"📊 Fetching 14-day traffic views for {len(projects)} repositories under @{username}...\n")

    results = []
    
    for p in projects:
        repo_name = p["name"]
        url = f"{API_BASE}/repos/{username}/{repo_name}/traffic/views"
        
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            
            if resp.status_code == 403:
                print(f"⚠️  Rate limited or forbidden when accessing {repo_name}. Skipping...")
                continue
            elif resp.status_code == 404:
                # GitHub returns 404 if the token does not have push access to the repository
                print(f"⚠️  Could not access traffic for '{repo_name}' (returned 404).")
                print("   Ensure your GITHUB_TOKEN has push/owner access to this repository.")
                continue
            
            resp.raise_for_status()
            traffic_data = resp.json()
            
            total_views = traffic_data.get("count", 0)
            unique_visitors = traffic_data.get("uniques", 0)
            
            results.append({
                "name": repo_name,
                "title": p["title"],
                "views": total_views,
                "uniques": unique_visitors,
                "language": p["language"]
            })
            print(f"✅ {repo_name}: {total_views} views ({unique_visitors} uniques)")
            
        except requests.RequestException as e:
            print(f"❌ Failed to fetch traffic for {repo_name}: {e}")

    if not results:
        print("\n❌ No traffic data could be retrieved. Check your GITHUB_TOKEN permissions.")
        sys.exit(1)

    # Sort by total views descending, then unique visitors descending
    results.sort(key=lambda x: (x["views"], x["uniques"]), reverse=True)

    print("\n" + "=" * 80)
    print(f"🏆 TRAFFIC RANKINGS (Last 14 Days) - @{username}")
    print("=" * 80)
    
    # Print headers
    print(f"{'Rank':<5} | {'Project Name':<25} | {'Total Views':<12} | {'Unique Visitors':<16} | {'Language':<12}")
    print("-" * 80)
    
    for idx, r in enumerate(results, start=1):
        rank_str = f"#{idx}"
        # Highlight top 1
        if idx == 1:
            rank_str = f"👑 #{idx}"
            
        print(f"{rank_str:<5} | {r['name']:<25} | {r['views']:<12} | {r['uniques']:<16} | {r['language']:<12}")
        
    print("=" * 80)
    print(f"\n🎉 Most viewed repository: {results[0]['title']} ({results[0]['views']} views)!")

if __name__ == "__main__":
    main()

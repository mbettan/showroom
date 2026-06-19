# 🏪 Showroom · Automated Developer Portfolio & Analytics

### A sleek, dark-themed portfolio showcase and developer analytics dashboard for GitHub repositories — 100% serverless and automatically synced.

**Showroom** is a premium, data-driven portfolio template built with an obsidian-black and mint-green glassmorphic design system. It automatically catalogs your repositories, tracks developer adoption metrics (views, clones, stars, forks), archives historical traffic to bypass GitHub's 14-day API limits, and renders a stunning interactive analytics dashboard using Chart.js.

---

## 🌟 Features

*   **Dual-View SPA Architecture:** Seamlessly toggle between the **Showroom** (project cards grid) and **Analytics** (interactive dashboard) via a smooth sidebar navigation menu.
*   **Archival Traffic Ledger:** Features a date-keyed **Local Traffic Ledger** (`docs/traffic_history.json`) that merges daily API hits to build a permanent, growing database of views and clones, bypassing GitHub's rolling 14-day data-loss window.
*   **Interactive Chart.js Dashboard:**
    *   *Adoption Trajectory:* Glowing cumulative area line chart mapping portfolio growth.
    *   *Daily Activity Peaks:* Daily traffic bar chart highlighting viewer spikes.
    *   *Adoption Share:* Colorful doughnut chart breaking down traffic distribution.
*   **Dynamic Controls:** Filter charts and KPI cards by specific repository and time ranges (Last 7, 14, 30 days, or All-Time).
*   **Set-and-Forget Cloud Automation:** Pre-configured GitHub Actions workflow automatically syncs stats and redeploys your site every night at midnight.
*   **Premium Web Aesthetics:** Sleek, responsive grid and list layouts, custom scrollbars, glowing border effects, and responsive mobile adaptation.
*   **SEO & Social Optimization:** Integrated JSON-LD schema metadata, Open Graph (OG) tags, search engine robot rules, and sitemaps.

---

## 📁 Project Structure

```text
showroom/
├── .github/
│   └── workflows/
│       └── update_showroom.yml # GitHub Actions daily sync & auto-deploy cron
├── scripts/
│   ├── fetch_repos.py          # Python API query engine & ledger aggregator
│   └── fetch_traffic.py        # Standalone terminal traffic analyzer CLI
├── docs/                       # Production web assets served by GitHub Pages
│   ├── index.html              # Showroom frontend and dashboard interface
│   ├── style.css               # Obsidian/mint layout styling & animations
│   ├── projects.json           # Compiled repository database (auto-generated)
│   ├── traffic_history.json    # Flat-file database ledger (auto-generated)
│   ├── robots.txt              # Search engine index rules
│   ├── sitemap.xml             # XML sitemap for search indexing
│   ├── logo.png                # Brand monogram logo (512x512)
│   └── images/
│       ├── placeholder.png     # Default card fallback thumbnail
│       └── {repo-name}.png     # Custom project card thumbnails
└── README.md
```

---

## 🚀 Getting Started

### 🧹 How to Start Fresh (Clean Slate)

If you are cloning this repository as a template to showcase your own projects, you should clear out the default demo databases and custom thumbnails before running your first sync:

```bash
# 1. Delete the pre-existing repository database and traffic ledger
rm -f docs/projects.json docs/traffic_history.json

# 2. Clear all custom project thumbnails (keeping only the default placeholder)
find docs/images -type f ! -name 'placeholder.png' -delete
```

After running these cleanup commands, you can proceed to the local setup below to build your own showroom from scratch!

### 1. Local Setup & Testing

To generate the database files and run the showroom locally on your machine:

```bash
# 1. Clone the repository
git clone https://github.com/<username>/showroom.git
cd showroom

# 2. Install Python dependencies
pip install requests

# 3. Create a local environment credentials file
echo 'GITHUB_TOKEN="your_personal_access_token"' > .env

# 4. Generate the database and traffic ledger files
python scripts/fetch_repos.py --username <username>
```

> 💡 **Personal Access Tokens**: The GitHub Traffic API (views and clones) requires a token with `repo` or `public_repo` scope to authorize data retrieval. If no token is provided, the script will skip traffic fetching and compile basic public repository metadata.

### 2. View Locally

Serve the `docs/` folder using any static web server:

```bash
# Start a lightweight local server
python3 -m http.server 8082 --directory docs
```

Open **`http://localhost:8082`** in your browser to view your portfolio and interactive charts!

---

## 📊 CLI Traffic Analyzer

You can also analyze your repository traffic directly in your terminal using the standalone CLI utility:

```bash
# Prints a beautifully sorted 14-day traffic breakdown in the terminal
python scripts/fetch_traffic.py
```

---

## 🤖 Cloud Automation (GitHub Actions)

You can automate the showcase so it updates itself and redeploys to **GitHub Pages** every night at midnight completely for free.

### 1. Add your Token to GitHub Secrets
Because the GitHub Actions runner runs in the cloud, you must securely provide your Personal Access Token as an encrypted environment secret:
1. Open your repository on GitHub.
2. Go to **Settings** -> **Secrets and variables** -> **Actions**.
3. Click **New repository secret**.
4. Configure it as follows:
    *   **Name:** `PORTFOLIO_GITHUB_TOKEN`
    *   **Value:** Paste your Personal Access Token (`ghp_...`).
5. Click **Add secret**.

### 2. Enable GitHub Pages
1. Go to **Settings** -> **Pages**.
2. Under **Build and deployment**, set the Source to **Deploy from a branch**.
3. Choose the **`main`** branch and select the **`/docs`** folder.
4. Click **Save**.

### 3. Push and Forget!
Once the secrets and pages are enabled, commit and push the project. The background worker will run automatically **every day at midnight UTC**. 

To trigger a manual sync at any time:
1. Go to the **Actions** tab of your repository.
2. Select **"Update Showroom Portfolio"** in the left sidebar.
3. Click the **Run workflow** dropdown on the right and click the green button.

---

## 🛠️ Configuration & Customization

You can customize your showcase filters and thresholds directly inside [scripts/fetch_repos.py](scripts/fetch_repos.py):

*   `SKIP_NAMES`: Add repository names you want to hide from your grid (e.g., `{"showroom", "dotfiles"}`).
*   `SKIP_FORKS`: Set to `True` (default) to hide repositories you've forked.
*   `SKIP_ARCHIVED`: Set to `True` to hide archived/read-only repositories.
*   `START_DATE`: Filter out older repositories by setting a creation date threshold (e.g., `"2025-09-06T19:40:02Z"`).

---

## 📄 License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this project except in compliance with the License. You may obtain a copy of the License at:

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

© 2026 Michaël Bettan.

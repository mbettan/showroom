# 🏪 Showroom · Michaël Bettan

### A sleek, dark-themed portfolio showcase for developer repositories, automatically synced from GitHub.

A curated showroom of projects, auto-synced from GitHub, built using a premium obsidian-black and mint-green design system. 

Built with 💚 by [**Michaël Bettan**](https://www.linkedin.com/in/mbettan/).

---

## 🌟 Features

- **Dynamic Syncing**: Runs a Python script to pull data from GitHub's REST API and compile a lightweight `projects.json` file.
- **Premium Aesthetics**: Reuses the gorgeous obsidian & mint color palette, custom scrollbars, glowing borders, and smooth transitions.
- **Interactive Sidebar**: Real-time filtering by programming language (Categories) and topic tags.
- **Real-Time Search**: High-performance instant search across project titles, descriptions, languages, and tags.
- **Layout Toggle**: Seamlessly switch between a high-fidelity **Grid View** and a detailed **List View**.
- **SEO & Social Ready**: Equipped with complete JSON-LD structured schema metadata, Open Graph (OG), sitemaps, and search engine rules.

---

## 📁 Project Structure

```
showroom/
├── scripts/
│   └── fetch_repos.py      # Python script to generate projects.json
├── docs/                   # Production-ready web assets served by GitHub Pages
│   ├── index.html          # The showroom frontend website
│   ├── style.css           # Obsidian/mint CSS layout & animations
│   ├── projects.json       # Auto-generated database (do not edit by hand)
│   ├── robots.txt          # Search engine visibility rules
│   ├── sitemap.xml         # XML sitemap for SEO indexing
│   ├── logo.png            # Rebranded glowing "MB" monogram logo (512x512)
│   └── images/
│       ├── placeholder.png # Premium default project thumbnail
│       └── {repo-name}.png # Bespoke custom-generated project thumbnails
└── README.md
```

---

## 🚀 Getting Started

### 1. Generate the Projects Database

The showroom is powered by a dynamic `projects.json` file. To fetch your latest public repositories:

```bash
# 1. Install Python dependencies
pip install requests

# 2. Run the generator script from the project root
python scripts/fetch_repos.py --username mbettan
```

> 💡 **Rate Limits**: GitHub limits unauthenticated requests to 60 per hour. To avoid rate limits, you can export a Personal Access Token:
> ```bash
> export GITHUB_TOKEN="your_github_token_here"
> python scripts/fetch_repos.py --username mbettan
> ```

### 2. Run the Showroom Locally

To serve the site locally, spin up any static web server and point it to the `docs/` directory:

```bash
# Serve the docs/ folder directly
python3 -m http.server 8080 --directory docs
```

Now open [http://localhost:8080](http://localhost:8080) in your browser!

---

## 🛠️ Configuration

You can customize the script's filtering rules directly inside [scripts/fetch_repos.py](scripts/fetch_repos.py):
- `SKIP_NAMES`: Add repository names you want to hide (e.g., `{"showroom", "showcase", "dotfiles"}`).
- `SKIP_FORKS`: Set to `True` (default) to ignore repositories you've forked.
- `SKIP_ARCHIVED`: Set to `True` to hide archived/read-only repositories.

---

## 📄 License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this project except in compliance with the License. You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

© 2026 Michaël Bettan.

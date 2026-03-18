#!/usr/bin/env python3
"""
Auto-generate index.html from newsletter HTML files.
Scans all jlw-*.html files, extracts titles/dates, renders archive page.
"""

import re
import sys
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup


def extract_metadata(html_path: Path) -> dict | None:
    """Extract title and date from a newsletter HTML file."""
    try:
        content = html_path.read_text(errors="replace")
        soup = BeautifulSoup(content, "html.parser")

        title_tag = soup.find("title")
        title = title_tag.string.strip() if title_tag and title_tag.string else html_path.stem

        # Try to extract date from filename (jlw-YYYY-MM-DD-*.html)
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", html_path.name)
        if date_match:
            date_str = date_match.group(1)
            date = datetime.strptime(date_str, "%Y-%m-%d")
        else:
            date = datetime.fromtimestamp(html_path.stat().st_mtime)

        # Extract subtitle/description if available
        subtitle = ""
        hero_subtitle = soup.find(class_="hero-subtitle")
        if hero_subtitle:
            subtitle = hero_subtitle.get_text(strip=True)[:200]

        # Get hero image for thumbnail
        hero_img = soup.find(class_="hero-image")
        thumbnail = ""
        if hero_img:
            img = hero_img.find("img")
            if img:
                thumbnail = img.get("src", "")

        return {
            "path": html_path.name,
            "title": title,
            "date": date,
            "date_str": date.strftime("%B %d, %Y"),
            "subtitle": subtitle,
            "thumbnail": thumbnail,
        }
    except Exception:
        return None


def generate_index(repo_path: Path) -> str:
    """Generate index.html content from all newsletters."""
    newsletters = []

    # Skip version variants (keep only highest version or base)
    seen_bases = {}
    for html_file in sorted(repo_path.glob("jlw-*.html"), reverse=True):
        # Determine base name (strip -v2, -v3, etc.)
        base_match = re.match(r"(jlw-\d{4}-\d{2}-\d{2}(?:-[a-z][\w-]*)??)(?:-v\d+)?\.html", html_file.name)
        if base_match:
            base = base_match.group(1)
            if base not in seen_bases:
                seen_bases[base] = html_file
        else:
            seen_bases[html_file.stem] = html_file

    for html_file in seen_bases.values():
        meta = extract_metadata(html_file)
        if meta:
            newsletters.append(meta)

    newsletters.sort(key=lambda n: n["date"], reverse=True)

    # Build HTML entries
    entries = []
    for nl in newsletters:
        entries.append(f'''
        <a href="{nl['path']}" class="newsletter-entry">
            <time datetime="{nl['date'].strftime('%Y-%m-%d')}">{nl['date_str']}</time>
            <h2>{nl['title']}</h2>
            {f'<p>{nl["subtitle"]}</p>' if nl['subtitle'] else ''}
        </a>''')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JLW Newsletter Archive</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #FDFBF7; --text: #1A1815; --accent: #B85C38;
            --border: #E8E2D9; --font-display: 'Fraunces', serif;
            --font-body: 'Source Sans 3', sans-serif; --font-mono: 'JetBrains Mono', monospace;
        }}
        @media (prefers-color-scheme: dark) {{
            :root {{ --bg: #141210; --text: #F5F1EA; --border: #2A2520; }}
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: var(--bg); color: var(--text); font-family: var(--font-body); line-height: 1.6; }}
        .container {{ max-width: 680px; margin: 0 auto; padding: 3rem 1.5rem; }}
        h1 {{ font-family: var(--font-display); font-size: 2.4rem; margin-bottom: 0.5rem; }}
        .subtitle {{ font-family: var(--font-mono); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.15em; opacity: 0.6; margin-bottom: 3rem; }}
        .newsletter-entry {{ display: block; padding: 1.5rem 0; border-bottom: 1px solid var(--border); text-decoration: none; color: inherit; transition: opacity 0.2s; }}
        .newsletter-entry:hover {{ opacity: 0.7; }}
        .newsletter-entry time {{ font-family: var(--font-mono); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.5; }}
        .newsletter-entry h2 {{ font-family: var(--font-display); font-size: 1.3rem; margin: 0.3rem 0; }}
        .newsletter-entry p {{ font-size: 0.95rem; opacity: 0.7; margin-top: 0.3rem; }}
        .count {{ font-family: var(--font-mono); font-size: 0.72rem; opacity: 0.5; margin-top: 3rem; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Newsletter Archive</h1>
        <p class="subtitle">An experiment in AI-generated curiosities</p>
        {''.join(entries)}
        <p class="count">{len(newsletters)} issues</p>
    </div>
</body>
</html>'''


if __name__ == "__main__":
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    output = generate_index(repo)
    index_path = repo / "index.html"
    index_path.write_text(output)
    print(f"Generated index.html with entries from {repo}")

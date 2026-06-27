#!/usr/bin/env python3
"""
Auto-generate index.html from newsletter HTML files.

Scans all jlw-*.html files (via the shared newsletter_lib single-parse pass),
extracts titles/dates/thumbnails, and renders a responsive card-grid archive
page grouped by year. Also emits sitemap.xml, robots.txt and a brandmark
favicon.svg alongside the page.
"""

import argparse
from html import escape
from pathlib import Path

from newsletter_lib import (
    SITE_URL,
    absolutize,
    canonical_newsletters,
)


SITE_DESCRIPTION = (
    "An experiment in AI-generated curiosities about technology, science, "
    "and culture."
)

FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="JLW">
  <rect width="64" height="64" rx="13" fill="#FDFBF7"/>
  <text x="32" y="43" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="26" font-weight="700" fill="#B85C38">JLW</text>
</svg>
"""


def _render_card(nl: dict) -> str:
    """Render one newsletter as a card (hero thumbnail + date + title + blurb)."""
    href = escape(nl["path"], quote=True)
    title = escape(nl["title"])
    date_attr = escape(nl["date"].strftime("%Y-%m-%d"), quote=True)
    date_str = escape(nl["date_str"])
    title_attr = escape(nl["title"], quote=True)

    thumb_html = ""
    if nl.get("thumbnail"):
        thumb_html = (
            f'<img class="card-thumb" loading="lazy" alt="" '
            f'src="{escape(nl["thumbnail"], quote=True)}">'
        )

    subtitle_html = ""
    if nl.get("subtitle"):
        subtitle_html = f'<p class="card-subtitle">{escape(nl["subtitle"])}</p>'

    return f'''
            <a href="{href}" class="newsletter-entry card" data-title="{title_attr}">
                {thumb_html}
                <div class="card-body">
                    <time datetime="{date_attr}">{date_str}</time>
                    <h3 class="card-title">{title}</h3>
                    {subtitle_html}
                </div>
            </a>'''


def _render_year_sections(newsletters: list) -> str:
    """Group newsletters by year (newest-first) with a heading per year."""
    sections = []
    current_year = None
    cards: list = []

    def flush():
        if current_year is None:
            return ""
        body = "".join(cards)
        return (
            f'\n        <section class="year-section">'
            f'\n            <h2 class="year">{current_year}</h2>'
            f'\n            <div class="card-grid">{body}\n            </div>'
            f'\n        </section>'
        )

    for nl in newsletters:
        if nl["year"] != current_year:
            if current_year is not None:
                sections.append(flush())
            current_year = nl["year"]
            cards = []
        cards.append(_render_card(nl))
    if current_year is not None:
        sections.append(flush())

    return "".join(sections)


def generate_index(repo_path: Path, newsletters: list | None = None) -> str:
    """Generate index.html content from all newsletters. ``newsletters`` may be
    passed in to reuse an already-computed single parse pass."""
    if newsletters is None:
        newsletters = canonical_newsletters(repo_path)

    year_sections = _render_year_sections(newsletters)

    # OpenGraph image: newest newsletter's hero thumbnail when available.
    og_image = ""
    for nl in newsletters:
        if nl.get("thumbnail"):
            og_image = absolutize(nl["thumbnail"])
            break
    og_image_tag = (
        f'\n    <meta property="og:image" content="{escape(og_image, quote=True)}">'
        if og_image
        else ""
    )

    desc = escape(SITE_DESCRIPTION, quote=True)
    site_url = escape(SITE_URL, quote=True)

    csp = (
        "default-src 'self'; "
        "img-src 'self' data: https:; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src https://fonts.gstatic.com; "
        "script-src 'self' 'unsafe-inline'; "
        "base-uri 'self'; "
        "form-action 'none'"
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="{csp}">
    <title>JLW Newsletter Archive</title>
    <meta name="description" content="{desc}">
    <meta property="og:title" content="JLW Newsletter Archive">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{site_url}/">{og_image_tag}
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="apple-touch-icon" href="/favicon.svg">
    <link rel="alternate" type="application/rss+xml" title="JLW Newsletter Podcast" href="podcast.rss">
    <link rel="alternate" type="application/rss+xml" title="JLW Newsletter Articles" href="articles.rss">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous">
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet" crossorigin="anonymous">
    <style>
        :root {{
            --bg: #FDFBF7; --text: #1A1815; --accent: #B85C38;
            --border: #E8E2D9; --font-display: 'Fraunces', serif;
            --font-body: 'Source Sans 3', sans-serif; --font-mono: 'JetBrains Mono', monospace;
        }}
        @media (prefers-color-scheme: dark) {{
            :root {{ --bg: #141210; --text: #F5F1EA; --border: #2A2520; --accent: #D88B6A; }}
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: var(--bg); color: var(--text); font-family: var(--font-body); line-height: 1.6; }}
        .container {{ max-width: 1080px; margin: 0 auto; padding: 3rem 1.5rem; }}
        h1 {{ font-family: var(--font-display); font-size: 2.4rem; margin-bottom: 0.5rem; }}
        .subtitle {{ font-family: var(--font-mono); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.15em; opacity: 0.6; margin-bottom: 1.5rem; }}
        .subscribe {{ display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; font-family: var(--font-mono); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1.5rem; }}
        .subscribe .label {{ opacity: 0.5; }}
        .subscribe a {{ color: var(--accent); text-decoration: none; }}
        .subscribe a:hover {{ text-decoration: underline; }}
        .filter-wrap {{ margin: 0 0 2.5rem; }}
        #archive-filter {{ width: 100%; padding: 0.75rem 1rem; font-family: var(--font-body); font-size: 1rem; color: var(--text); background: transparent; border: 1px solid var(--border); border-radius: 8px; }}
        #archive-filter:focus {{ outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px rgba(184, 92, 56, 0.15); }}
        .year-section {{ margin-bottom: 3rem; }}
        .year {{ font-family: var(--font-display); font-size: 1.6rem; margin: 0 0 1.3rem; padding-bottom: 0.4rem; border-bottom: 2px solid var(--accent); }}
        .card-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }}
        .newsletter-entry.card {{ display: flex; flex-direction: column; overflow: hidden; border: 1px solid var(--border); border-radius: 12px; text-decoration: none; color: inherit; transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease; }}
        .newsletter-entry.card:hover {{ transform: translateY(-4px); box-shadow: 0 14px 30px rgba(0, 0, 0, 0.14); border-color: var(--accent); }}
        .newsletter-entry.card:hover .card-title {{ color: var(--accent); }}
        .card-thumb {{ width: 100%; aspect-ratio: 16 / 9; object-fit: cover; display: block; background: var(--border); }}
        .card-body {{ padding: 1.1rem 1.2rem 1.3rem; }}
        .card-body time {{ font-family: var(--font-mono); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.5; }}
        .card-title {{ font-family: var(--font-display); font-size: 1.2rem; margin: 0.3rem 0 0.4rem; transition: color 0.2s ease; }}
        .card-subtitle {{ font-size: 0.92rem; opacity: 0.72; }}
        .count {{ font-family: var(--font-mono); font-size: 0.72rem; opacity: 0.5; margin-top: 2rem; }}
        .empty {{ opacity: 0.6; font-style: italic; margin: 2rem 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Newsletter Archive</h1>
        <p class="subtitle">An experiment in AI-generated curiosities</p>
        <div class="subscribe">
            <span class="label">Subscribe</span>
            <a href="podcast.rss">Podcast RSS</a>
            <a href="articles.rss">Articles RSS</a>
        </div>
        <div class="filter-wrap">
            <input type="search" id="archive-filter" placeholder="Filter by title…" aria-label="Filter newsletters by title" autocomplete="off">
        </div>
        <div class="archive">{year_sections if year_sections else '<p class="empty">No newsletters yet.</p>'}
        </div>
        <p class="count">{len(newsletters)} issues</p>
    </div>
    <script>
    (function () {{
        var input = document.getElementById('archive-filter');
        if (!input) return;
        var entries = Array.prototype.slice.call(document.querySelectorAll('.newsletter-entry'));
        var sections = Array.prototype.slice.call(document.querySelectorAll('.year-section'));
        input.addEventListener('input', function () {{
            var q = input.value.trim().toLowerCase();
            entries.forEach(function (el) {{
                var t = (el.getAttribute('data-title') || '').toLowerCase();
                el.style.display = (!q || t.indexOf(q) !== -1) ? '' : 'none';
            }});
            sections.forEach(function (sec) {{
                var es = sec.querySelectorAll('.newsletter-entry');
                var anyShown = false;
                for (var i = 0; i < es.length; i++) {{
                    if (es[i].style.display !== 'none') {{ anyShown = true; break; }}
                }}
                sec.style.display = anyShown ? '' : 'none';
            }});
        }});
    }})();
    </script>
</body>
</html>'''


def write_sitemap(repo_path: Path, newsletters: list) -> Path:
    """Write sitemap.xml listing the site root + every newsletter URL."""
    urls = [f"{SITE_URL}/"]
    urls += [f"{SITE_URL}/{nl['path']}" for nl in newsletters]
    body = "\n".join(
        f"  <url><loc>{escape(u)}</loc></url>" for u in urls
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        "</urlset>\n"
    )
    path = repo_path / "sitemap.xml"
    path.write_text(xml)
    return path


def write_robots(repo_path: Path) -> Path:
    """Write a minimal robots.txt (allow all + Sitemap reference)."""
    content = (
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )
    path = repo_path / "robots.txt"
    path.write_text(content)
    return path


def write_favicon(repo_path: Path) -> Path:
    """Write the brandmark favicon.svg (JLW monogram in the brand accent)."""
    path = repo_path / "favicon.svg"
    path.write_text(FAVICON_SVG)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate index.html (plus sitemap.xml, robots.txt and favicon.svg) "
            "from the jlw-*.html newsletters in a repo directory."
        )
    )
    parser.add_argument(
        "repo",
        nargs="?",
        default=".",
        help="Repo/output directory containing the newsletters (default: cwd).",
    )
    args = parser.parse_args()

    repo = Path(args.repo)
    newsletters = canonical_newsletters(repo)

    output = generate_index(repo, newsletters)
    (repo / "index.html").write_text(output)

    write_sitemap(repo, newsletters)
    write_robots(repo)
    write_favicon(repo)

    print(f"Generated index.html with entries from {repo}")
    print(f"Wrote sitemap.xml, robots.txt, favicon.svg ({len(newsletters)} issues)")


if __name__ == "__main__":
    main()

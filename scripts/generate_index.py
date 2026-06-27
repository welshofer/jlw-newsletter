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
    atomic_write_bytes,
    atomic_write_text,
    canonical_newsletters,
)


SITE_DESCRIPTION = (
    "An experiment in AI-generated curiosities about technology, science, "
    "and culture."
)

# Single source of truth for the Content-Security-Policy. Used both for the
# in-page <meta> tag and the Cloudflare Pages `_headers` file so they match.
CSP = (
    "default-src 'self'; "
    "img-src 'self' data: https:; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com; "
    "script-src 'self' 'unsafe-inline'; "
    "base-uri 'self'; "
    "form-action 'none'"
)

FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="JLW">
  <rect width="64" height="64" rx="13" fill="#FDFBF7"/>
  <text x="32" y="43" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="26" font-weight="700" fill="#B85C38">JLW</text>
</svg>
"""


def _webp_sibling(thumbnail: str, repo_path: Path) -> str:
    """Return the relative ``.webp`` path when a sibling of ``thumbnail`` exists
    on disk in ``repo_path``; otherwise an empty string. Remote/absolute/data
    URLs are skipped (we can only test local files)."""
    if not thumbnail or thumbnail.startswith(
        ("http://", "https://", "//", "data:")
    ):
        return ""
    webp_rel = Path(thumbnail).with_suffix(".webp")
    if (repo_path / webp_rel).exists():
        return webp_rel.as_posix()
    return ""


def _render_card(nl: dict, repo_path: Path) -> str:
    """Render one newsletter as a card (hero thumbnail + date + title + blurb).

    When a ``.webp`` sibling of the raster thumbnail exists on disk, the image
    is wrapped in a ``<picture>`` with a WebP ``<source>`` so capable browsers
    fetch the smaller file while older ones fall back to the original raster.
    """
    href = escape(nl["path"], quote=True)
    title = escape(nl["title"])
    date_attr = escape(nl["date"].strftime("%Y-%m-%d"), quote=True)
    date_str = escape(nl["date_str"])
    title_attr = escape(nl["title"], quote=True)

    thumb_html = ""
    thumbnail = nl.get("thumbnail")
    if thumbnail:
        img_tag = (
            f'<img class="card-thumb" loading="lazy" alt="" '
            f'src="{escape(thumbnail, quote=True)}">'
        )
        webp_src = _webp_sibling(thumbnail, repo_path)
        if webp_src:
            thumb_html = (
                "<picture>"
                f'<source type="image/webp" srcset="{escape(webp_src, quote=True)}">'
                f"{img_tag}"
                "</picture>"
            )
        else:
            thumb_html = img_tag

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


def _render_year_sections(newsletters: list, repo_path: Path) -> str:
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
        cards.append(_render_card(nl, repo_path))
    if current_year is not None:
        sections.append(flush())

    return "".join(sections)


def generate_index(repo_path: Path, newsletters: list | None = None) -> str:
    """Generate index.html content from all newsletters. ``newsletters`` may be
    passed in to reuse an already-computed single parse pass."""
    if newsletters is None:
        newsletters = canonical_newsletters(repo_path)

    year_sections = _render_year_sections(newsletters, repo_path)

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

    csp = CSP

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
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
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
        .newsletter-entry.card {{ display: flex; flex-direction: column; overflow: hidden; border: 1px solid var(--border); border-radius: 12px; text-decoration: none; color: inherit; }}
        .newsletter-entry.card:hover {{ box-shadow: 0 14px 30px rgba(0, 0, 0, 0.14); border-color: var(--accent); }}
        .newsletter-entry.card:hover .card-title {{ color: var(--accent); }}
        .newsletter-entry.card:focus-visible {{ outline: none; box-shadow: 0 14px 30px rgba(0, 0, 0, 0.14); border-color: var(--accent); }}
        .newsletter-entry.card:focus-visible .card-title {{ color: var(--accent); }}
        @media (prefers-reduced-motion: no-preference) {{
            .newsletter-entry.card {{ transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease; }}
            .newsletter-entry.card:hover {{ transform: translateY(-4px); }}
            .newsletter-entry.card:focus-visible {{ transform: translateY(-4px); }}
        }}
        .card-thumb {{ width: 100%; aspect-ratio: 16 / 9; object-fit: cover; display: block; background: var(--border); }}
        .card-body {{ padding: 1.1rem 1.2rem 1.3rem; }}
        .card-body time {{ font-family: var(--font-mono); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.5; }}
        .card-title {{ font-family: var(--font-display); font-size: 1.2rem; margin: 0.3rem 0 0.4rem; transition: color 0.2s ease; }}
        .card-subtitle {{ font-size: 0.92rem; opacity: 0.72; }}
        .count {{ font-family: var(--font-mono); font-size: 0.72rem; opacity: 0.5; margin-top: 2rem; }}
        .empty {{ opacity: 0.6; font-style: italic; margin: 2rem 0; }}
        .no-results {{ opacity: 0.6; font-style: italic; margin: 2rem 0; }}
        .no-results[hidden] {{ display: none; }}
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
        <p class="no-results" id="no-results" role="status" hidden></p>
        <p class="count" id="archive-count">{len(newsletters)} issues</p>
    </div>
    <script>
    (function () {{
        var input = document.getElementById('archive-filter');
        if (!input) return;
        var entries = Array.prototype.slice.call(document.querySelectorAll('.newsletter-entry'));
        var sections = Array.prototype.slice.call(document.querySelectorAll('.year-section'));
        var countEl = document.getElementById('archive-count');
        var noResults = document.getElementById('no-results');
        var total = entries.length;
        input.addEventListener('input', function () {{
            var raw = input.value.trim();
            var q = raw.toLowerCase();
            var visible = 0;
            entries.forEach(function (el) {{
                var t = (el.getAttribute('data-title') || '').toLowerCase();
                var show = (!q || t.indexOf(q) !== -1);
                el.style.display = show ? '' : 'none';
                if (show) visible++;
            }});
            sections.forEach(function (sec) {{
                var es = sec.querySelectorAll('.newsletter-entry');
                var anyShown = false;
                for (var i = 0; i < es.length; i++) {{
                    if (es[i].style.display !== 'none') {{ anyShown = true; break; }}
                }}
                sec.style.display = anyShown ? '' : 'none';
            }});
            if (countEl) {{
                countEl.textContent = (q ? visible : total) + ' issues';
            }}
            if (noResults) {{
                if (q && visible === 0) {{
                    noResults.textContent = 'No issues match "' + raw + '"';
                    noResults.hidden = false;
                }} else {{
                    noResults.hidden = true;
                }}
            }}
        }});
    }})();
    </script>
</body>
</html>'''


def write_sitemap(repo_path: Path, newsletters: list) -> Path:
    """Write sitemap.xml listing the site root + every newsletter URL (each
    newsletter URL carrying a ``<lastmod>`` from its record date)."""
    lines = [f"  <url><loc>{escape(SITE_URL)}/</loc></url>"]
    for nl in newsletters:
        loc = escape(f"{SITE_URL}/{nl['path']}")
        lastmod = nl["date"].strftime("%Y-%m-%d")
        lines.append(
            f"  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod></url>"
        )
    body = "\n".join(lines)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        "</urlset>\n"
    )
    return atomic_write_text(repo_path / "sitemap.xml", xml)


def write_robots(repo_path: Path) -> Path:
    """Write a minimal robots.txt (allow all + Sitemap reference)."""
    content = (
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )
    return atomic_write_text(repo_path / "robots.txt", content)


def write_favicon(repo_path: Path) -> Path:
    """Write the brandmark favicon.svg (JLW monogram in the brand accent)."""
    return atomic_write_text(repo_path / "favicon.svg", FAVICON_SVG)


def write_headers(repo_path: Path) -> Path:
    """Emit a Cloudflare Pages `_headers` file applying security headers to all
    paths, including a header-form CSP that matches the in-page <meta> CSP."""
    content = (
        "/*\n"
        "  Strict-Transport-Security: max-age=63072000; includeSubDomains; preload\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  X-Frame-Options: DENY\n"
        f"  Content-Security-Policy: {CSP}\n"
    )
    return atomic_write_text(repo_path / "_headers", content)


def write_apple_touch_icon(repo_path: Path) -> Path | None:
    """Render a 180x180 PNG JLW monogram as apple-touch-icon.png (iOS renders
    SVG touch icons blank). Returns the path, or ``None`` when Pillow is not
    installed so the rest of the run still succeeds."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return None

    import io

    size = 180
    bg = (253, 251, 247)   # --bg light (#FDFBF7)
    fg = (184, 92, 56)     # --accent  (#B85C38)
    text = "JLW"

    img = Image.new("RGB", (size, size), bg)
    draw = ImageDraw.Draw(img)

    font = None
    for name in ("DejaVuSans-Bold.ttf", "Arial Bold.ttf", "Arial.ttf"):
        try:
            font = ImageFont.truetype(name, 60)
            break
        except Exception:
            continue
    if font is None:
        font = ImageFont.load_default()

    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pos = ((size - tw) / 2 - bbox[0], (size - th) / 2 - bbox[1])
    except Exception:
        tw, th = draw.textlength(text, font=font), 60
        pos = ((size - tw) / 2, (size - th) / 2)

    draw.text(pos, text, fill=fg, font=font)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return atomic_write_bytes(repo_path / "apple-touch-icon.png", buf.getvalue())


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate index.html (plus sitemap.xml, robots.txt, favicon.svg, "
            "_headers and apple-touch-icon.png) from the jlw-*.html newsletters "
            "in a repo directory."
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
    atomic_write_text(repo / "index.html", output)

    write_sitemap(repo, newsletters)
    write_robots(repo)
    write_favicon(repo)
    write_headers(repo)
    icon = write_apple_touch_icon(repo)

    print(f"Generated index.html with entries from {repo}")
    extras = "sitemap.xml, robots.txt, favicon.svg, _headers"
    if icon is not None:
        extras += ", apple-touch-icon.png"
    else:
        print("note: Pillow unavailable; skipped apple-touch-icon.png")
    print(f"Wrote {extras} ({len(newsletters)} issues)")


if __name__ == "__main__":
    main()

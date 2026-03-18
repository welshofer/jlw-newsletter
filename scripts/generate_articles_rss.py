#!/usr/bin/env python3
"""
Generate an articles RSS feed from newsletter HTML files.
Separate from podcast.rss — this is for RSS readers subscribing to the written content.
"""

import re
import sys
from datetime import datetime
from email.utils import format_datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

from bs4 import BeautifulSoup


SITE_URL = "https://jlw-newsletter.pages.dev"


def extract_article_metadata(html_path: Path) -> dict | None:
    """Extract metadata from a newsletter HTML file for RSS."""
    try:
        content = html_path.read_text(errors="replace")
        soup = BeautifulSoup(content, "html.parser")

        title_tag = soup.find("title")
        title = title_tag.string.strip() if title_tag and title_tag.string else html_path.stem

        # Extract date from filename
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", html_path.name)
        if date_match:
            pub_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
        else:
            pub_date = datetime.fromtimestamp(html_path.stat().st_mtime)

        # Extract description from hero subtitle or first paragraph
        description = ""
        hero_subtitle = soup.find(class_="hero-subtitle")
        if hero_subtitle:
            description = hero_subtitle.get_text(strip=True)[:500]
        if not description:
            first_p = soup.find("p")
            if first_p:
                description = first_p.get_text(strip=True)[:500]

        return {
            "title": title,
            "link": f"{SITE_URL}/{html_path.name}",
            "description": description,
            "pub_date": pub_date,
            "guid": f"{SITE_URL}/{html_path.name}",
        }
    except Exception:
        return None


def generate_articles_rss(repo_path: Path) -> str:
    """Generate articles.rss from all newsletter HTML files."""
    articles = []

    for html_file in sorted(repo_path.glob("jlw-*.html"), reverse=True):
        # Skip version variants
        if re.search(r"-v\d+\.html$", html_file.name):
            continue
        meta = extract_article_metadata(html_file)
        if meta:
            articles.append(meta)

    # Build RSS XML
    rss = Element("rss", version="2.0")
    channel = SubElement(rss, "channel")

    SubElement(channel, "title").text = "JLW Newsletter"
    SubElement(channel, "link").text = SITE_URL
    SubElement(channel, "description").text = "AI-generated curiosities about technology, science, and culture"
    SubElement(channel, "language").text = "en-us"
    if articles:
        SubElement(channel, "lastBuildDate").text = format_datetime(articles[0]["pub_date"])

    for article in articles[:50]:  # Last 50 articles
        item = SubElement(channel, "item")
        SubElement(item, "title").text = article["title"]
        SubElement(item, "link").text = article["link"]
        SubElement(item, "description").text = article["description"]
        SubElement(item, "pubDate").text = format_datetime(article["pub_date"])
        guid = SubElement(item, "guid")
        guid.text = article["guid"]
        guid.set("isPermaLink", "true")

    raw_xml = tostring(rss, encoding="unicode")
    pretty = parseString(raw_xml).toprettyxml(indent="  ", encoding=None)
    # Remove extra XML declaration from toprettyxml
    lines = pretty.split("\n")
    if lines[0].startswith("<?xml"):
        lines[0] = '<?xml version="1.0" encoding="UTF-8"?>'
    return "\n".join(lines)


if __name__ == "__main__":
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    rss_content = generate_articles_rss(repo)
    rss_path = repo / "articles.rss"
    rss_path.write_text(rss_content)
    print(f"Generated articles.rss with entries from {repo}")

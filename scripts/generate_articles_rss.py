#!/usr/bin/env python3
"""
Generate an articles RSS feed from newsletter HTML files.
Separate from podcast.rss — this is for RSS readers subscribing to the written content.

Shares the single parse pass in newsletter_lib so the HTML is globbed and parsed
once (rather than independently from generate_index.py). The shared parser also
narrows its exception handling and warns on stderr instead of silently dropping
files. ElementTree handles all XML escaping.
"""

import sys
from email.utils import format_datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

from newsletter_lib import SITE_URL, canonical_newsletters


def generate_articles_rss(repo_path: Path) -> str:
    """Generate articles.rss from all newsletter HTML files."""
    # canonical_newsletters parses each file exactly once and returns the
    # canonical (non-variant / newest) record per issue, sorted newest-first.
    newsletters = canonical_newsletters(repo_path)
    articles = [
        {
            "title": nl["title"],
            "link": f"{SITE_URL}/{nl['path']}",
            "description": nl["description"],
            "pub_date": nl["date"],
            "guid": f"{SITE_URL}/{nl['path']}",
        }
        for nl in newsletters
    ]

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

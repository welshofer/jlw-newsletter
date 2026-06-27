#!/usr/bin/env python3
"""
Generate an articles RSS feed from newsletter HTML files.
Separate from podcast.rss — this is for RSS readers subscribing to the written content.

Shares the single parse pass in newsletter_lib so the HTML is globbed and parsed
once (rather than independently from generate_index.py). The shared parser also
narrows its exception handling and warns on stderr instead of silently dropping
files. ElementTree handles all XML escaping.
"""

import argparse
from email.utils import format_datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, register_namespace, tostring
from xml.dom.minidom import parseString

from newsletter_lib import SITE_URL, atomic_write_text, canonical_newsletters


# RSS 1.0 content module — carries the full HTML body in <content:encoded>.
CONTENT_NS = "http://purl.org/rss/1.0/modules/content/"
register_namespace("content", CONTENT_NS)


def _cdata(raw: str) -> str:
    """Wrap ``raw`` HTML in a CDATA section, escaping any nested ``]]>`` so it
    cannot prematurely terminate the section."""
    return "<![CDATA[" + (raw or "").replace("]]>", "]]]]><![CDATA[>") + "]]>"


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
            "content": nl.get("body_html", ""),
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

    # ElementTree cannot emit raw CDATA, so each <content:encoded> gets a unique
    # sentinel as its text which is swapped for the real CDATA after serializing.
    cdata_blocks: dict[str, str] = {}

    for idx, article in enumerate(articles[:50]):  # Last 50 articles
        item = SubElement(channel, "item")
        SubElement(item, "title").text = article["title"]
        SubElement(item, "link").text = article["link"]
        SubElement(item, "description").text = article["description"]
        if article["content"]:
            token = f"__JLW_CDATA_{idx}__"
            cdata_blocks[token] = _cdata(article["content"])
            SubElement(item, f"{{{CONTENT_NS}}}encoded").text = token
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
    out = "\n".join(lines)
    for token, block in cdata_blocks.items():
        out = out.replace(token, block)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate articles.rss from the jlw-*.html newsletters in a repo "
            "directory."
        )
    )
    parser.add_argument(
        "repo",
        nargs="?",
        default=".",
        help="Repo/output directory containing the newsletters (default: cwd).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output path for the feed (default: <repo>/articles.rss).",
    )
    args = parser.parse_args()

    repo = Path(args.repo)
    rss_content = generate_articles_rss(repo)
    out_path = Path(args.output) if args.output else repo / "articles.rss"
    atomic_write_text(out_path, rss_content)
    print(f"Generated {out_path} with entries from {repo}")


if __name__ == "__main__":
    main()

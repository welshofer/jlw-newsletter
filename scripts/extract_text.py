#!/usr/bin/env python3
"""Extract readable text from newsletter HTML, stripping CSS/JS/tags.

Usage:
    python3 scripts/extract_text.py <input.html> [output.md]
    python3 scripts/extract_text.py <input.html> -o output.md
    python3 scripts/extract_text.py <input.html> --title-only

If output is omitted, prints to stdout.
Used by generate_video.sh to prepare content for NotebookLM ingestion.
"""

import argparse
import re
import sys
from html.parser import HTMLParser


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script"):
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self.skip = False
        if tag in ("p", "h1", "h2", "h3", "blockquote", "div", "article", "section"):
            self.text.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)


def extract_title(html: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
    return m.group(1).strip() if m else "Newsletter"


def extract_text(html: str) -> str:
    extractor = TextExtractor()
    extractor.feed(html)
    return re.sub(r"\n{3,}", "\n\n", "".join(extractor.text)).strip()


def main():
    parser = argparse.ArgumentParser(
        description="Extract readable text from newsletter HTML, stripping CSS/JS/tags."
    )
    parser.add_argument("input", metavar="input.html", help="HTML file to extract from")
    parser.add_argument(
        "output",
        metavar="output.md",
        nargs="?",
        default=None,
        help="output file (defaults to stdout)",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_opt",
        metavar="output.md",
        default=None,
        help="output file (alternative to the positional output argument)",
    )
    parser.add_argument(
        "--title-only",
        action="store_true",
        help="print only the extracted <h1> title and exit",
    )
    args = parser.parse_args()

    output_path = args.output_opt or args.output

    with open(args.input) as f:
        html = f.read()

    title = extract_title(html)

    if args.title_only:
        result = title
    else:
        text = extract_text(html)
        result = f"# {title}\n\n{text}"

    if output_path:
        with open(output_path, "w") as f:
            f.write(result)
        if args.title_only:
            print(f"Wrote title → {output_path}", file=sys.stderr)
        else:
            text_len = len(result) - len(f"# {title}\n\n")
            print(f"Extracted {text_len} chars → {output_path}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()

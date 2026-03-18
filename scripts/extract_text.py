#!/usr/bin/env python3
"""Extract readable text from newsletter HTML, stripping CSS/JS/tags.

Usage:
    python3 scripts/extract_text.py <input.html> [output.md]

If output is omitted, prints to stdout.
Used by generate_video.sh to prepare content for NotebookLM ingestion.
"""

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
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input.html> [output.md]", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    with open(input_path) as f:
        html = f.read()

    title = extract_title(html)
    text = extract_text(html)
    result = f"# {title}\n\n{text}"

    if output_path:
        with open(output_path, "w") as f:
            f.write(result)
        print(f"Extracted {len(text)} chars → {output_path}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()

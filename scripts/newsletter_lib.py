#!/usr/bin/env python3
"""
Shared helpers for the newsletter static-site generators.

A single parse pass (``iter_newsletters``) globs every ``jlw-*.html`` file in a
repo, BeautifulSoup-parses each file exactly once, and yields a record that is
rich enough for BOTH the archive index and the articles RSS feed. This avoids
the two generators independently globbing and re-parsing the same files.
"""

import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Iterator, Optional

from bs4 import BeautifulSoup


# Canonical public site URL (used for feeds, sitemap, OpenGraph, etc.).
SITE_URL = "https://jlw-newsletter.pages.dev"


def atomic_write_text(path: Path, text: str, encoding: str = "utf-8") -> Path:
    """Write ``text`` to ``path`` atomically: write to a temp file in the same
    directory then ``os.replace()`` over the target so readers never observe a
    half-written file and no partial output survives a crash."""
    path = Path(path)
    fd, tmp = tempfile.mkstemp(
        dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding=encoding) as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    return path


def atomic_write_bytes(path: Path, data: bytes) -> Path:
    """Binary counterpart to :func:`atomic_write_text` (temp file + replace)."""
    path = Path(path)
    fd, tmp = tempfile.mkstemp(
        dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    return path


def make_soup(content: str) -> BeautifulSoup:
    """Parse HTML with the fast ``lxml`` parser, falling back to the stdlib
    ``html.parser`` when lxml is not installed in the environment."""
    try:
        return BeautifulSoup(content, "lxml")
    except Exception:
        # bs4 raises FeatureNotFound when the lxml parser is unavailable.
        return BeautifulSoup(content, "html.parser")


def smart_truncate(text: str, limit: int = 200) -> str:
    """Truncate ``text`` on a word boundary (never mid-word) and append an
    ellipsis when the text was actually shortened."""
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rstrip()
    space = cut.rfind(" ")
    if space > 0:
        cut = cut[:space].rstrip()
    return cut + "…"


def absolutize(url: str) -> str:
    """Resolve a possibly-relative asset URL against ``SITE_URL``."""
    if not url:
        return url
    if url.startswith(("http://", "https://", "//")):
        return url
    return f"{SITE_URL}/{url.lstrip('/')}"


def _newsletter_stem(name: str) -> str:
    return name[:-5] if name.endswith(".html") else name


def is_variant(name: str) -> bool:
    """True when the filename carries a ``-vN`` version suffix."""
    return re.search(r"-v\d+$", _newsletter_stem(name)) is not None


def newsletter_base(name: str) -> str:
    """The base identity of a newsletter, ignoring any ``-vN`` suffix, so all
    variants of the same issue collapse to one key."""
    return re.sub(r"-v\d+$", "", _newsletter_stem(name))


def _parse_one(html_path: Path) -> Optional[dict]:
    """Parse a single newsletter HTML file into a record. On a recoverable
    error a warning is printed to stderr and ``None`` is returned (so the file
    is skipped) instead of silently swallowing it."""
    try:
        content = html_path.read_text(errors="replace")
        soup = make_soup(content)

        title_tag = soup.find("title")
        title = (
            title_tag.string.strip()
            if title_tag and title_tag.string
            else html_path.stem
        )

        # Prefer the date encoded in the filename (jlw-YYYY-MM-DD-*.html).
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", html_path.name)
        if date_match:
            date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
        else:
            date = datetime.fromtimestamp(html_path.stat().st_mtime)

        # Hero subtitle drives both the index card text and the RSS description.
        subtitle_raw = ""
        hero_subtitle = soup.find(class_="hero-subtitle")
        if hero_subtitle:
            subtitle_raw = hero_subtitle.get_text(strip=True)

        description = subtitle_raw
        if not description:
            first_p = soup.find("p")
            if first_p:
                description = first_p.get_text(strip=True)

        # Hero image -> thumbnail / OpenGraph image.
        thumbnail = ""
        hero_img = soup.find(class_="hero-image")
        if hero_img:
            img = hero_img.find("img")
            if img:
                thumbnail = img.get("src", "") or ""

        # Full body HTML for the articles feed's <content:encoded>. Prefer the
        # semantic <article>/<main> container, falling back to <body>.
        body_html = ""
        container = soup.find("article") or soup.find("main") or soup.find("body")
        if container is not None:
            try:
                body_html = container.decode_contents()
            except Exception:
                body_html = container.get_text()

        return {
            "path": html_path.name,
            "base": newsletter_base(html_path.name),
            "is_variant": is_variant(html_path.name),
            "mtime": html_path.stat().st_mtime,
            "title": title,
            "date": date,
            "date_str": date.strftime("%B %d, %Y"),
            "year": date.year,
            "subtitle": smart_truncate(subtitle_raw, 200),
            "description": description[:500],
            "body_html": body_html,
            "thumbnail": thumbnail,
        }
    except (OSError, ValueError, UnicodeDecodeError) as exc:
        print(
            f"warning: skipping {html_path}: {exc.__class__.__name__}: {exc}",
            file=sys.stderr,
        )
        return None


def iter_newsletters(repo_path: Path) -> Iterator[dict]:
    """Glob and parse every ``jlw-*.html`` newsletter in ``repo_path`` exactly
    once, yielding one record per file (variants included)."""
    for html_file in sorted(repo_path.glob("jlw-*.html")):
        record = _parse_one(html_file)
        if record is not None:
            yield record


def _rank(rec: dict) -> tuple:
    """Lower is better: prefer the non-variant file, then the newest mtime."""
    return (1 if rec["is_variant"] else 0, -rec["mtime"])


def _choose_best(existing: Optional[dict], candidate: dict) -> dict:
    if existing is None:
        return candidate
    return candidate if _rank(candidate) < _rank(existing) else existing


def dedupe_newsletters(records) -> list:
    """Collapse variant files to a single canonical record per base, preferring
    the non-variant file and otherwise the newest one (matches the ranking used
    by the podcast feed)."""
    best: dict = {}
    for rec in records:
        best[rec["base"]] = _choose_best(best.get(rec["base"]), rec)
    return list(best.values())


def canonical_newsletters(repo_path: Path) -> list:
    """Convenience: parse once, dedupe to canonical, sort newest-first."""
    records = dedupe_newsletters(iter_newsletters(repo_path))
    records.sort(key=lambda r: r["date"], reverse=True)
    return records

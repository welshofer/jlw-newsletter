#!/usr/bin/env python3
import argparse
import json
import os
import re
import wave
from contextlib import closing
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from typing import Optional, Tuple, Dict, List
from xml.etree import ElementTree as ET

try:
    from bs4 import BeautifulSoup  # type: ignore
except Exception:  # pragma: no cover
    BeautifulSoup = None

NS = {
    "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
    "media": "http://search.yahoo.com/mrss/",
    "atom": "http://www.w3.org/2005/Atom",
}

for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def safe_join_url(base: str, filename: str) -> str:
    if not base.endswith("/"):
        base += "/"
    return base + filename


def absolutize_url(base: str, path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if path.startswith("//"):
        return "https:" + path
    if path.startswith("../"):
        path = path.lstrip("./")
        # remove leading ../ segments
        while path.startswith("../"):
            path = path[3:]
    return base.rstrip("/") + "/" + path.lstrip("/")


def rfc2822_from_ts(ts: float) -> str:
    dt = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone()
    return format_datetime(dt)


def get_birth_or_mtime(path: Path) -> float:
    st = path.stat()
    return getattr(st, "st_birthtime", st.st_mtime)


def duration_from_wav(path: Path) -> Optional[int]:
    try:
        with closing(wave.open(str(path), "rb")) as w:
            frames = w.getnframes()
            rate = w.getframerate()
            if rate == 0:
                return None
            return int(round(frames / rate))
    except Exception:
        return None


def format_duration(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def title_from_basename(name: str) -> str:
    # Keep original casing; just replace separators for a readable default.
    name = name.replace("_", " ").replace("-", " ")
    name = re.sub(r"\s+", " ", name).strip()
    return name


def extract_title_blurb(html_path: Path) -> Tuple[Optional[str], Optional[str]]:
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    if BeautifulSoup:
        soup = BeautifulSoup(text, "html.parser")
        h1 = soup.find("h1")
        title = h1.get_text(strip=True) if h1 else None
        blurb = None
        if h1:
            p = h1.find_next("p")
            if p:
                blurb = p.get_text(" ", strip=True)
        if not title:
            t = soup.find("title")
            title = t.get_text(strip=True) if t else None
        return title, blurb

    # Fallback: basic regex extraction
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.IGNORECASE | re.DOTALL)
    title = (
        re.sub(r"<[^>]+>", "", title_match.group(1)).strip()
        if title_match
        else None
    )
    blurb = None
    if title_match:
        after = text[title_match.end() :]
        p_match = re.search(r"<p[^>]*>(.*?)</p>", after, re.IGNORECASE | re.DOTALL)
        if p_match:
            blurb = re.sub(r"<[^>]+>", "", p_match.group(1)).strip()
    if not title:
        title_match = re.search(
            r"<title[^>]*>(.*?)</title>", text, re.IGNORECASE | re.DOTALL
        )
        title = (
            re.sub(r"<[^>]+>", "", title_match.group(1)).strip()
            if title_match
            else None
        )
    return title, blurb


def extract_image_src(html_path: Path) -> Optional[str]:
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    if BeautifulSoup:
        soup = BeautifulSoup(text, "html.parser")
        for key in ("og:image", "twitter:image"):
            tag = soup.find("meta", property=key) or soup.find("meta", attrs={"name": key})
            if tag and tag.get("content"):
                return tag["content"].strip()
        img = soup.find("img")
        if img and img.get("src"):
            return img["src"].strip()
        return None

    # Fallback: naive regex for first img src
    m = re.search(r"<img[^>]+src=[\"']([^\"']+)[\"']", text, re.IGNORECASE)
    return m.group(1).strip() if m else None


def extract_audio_src(html_path: Path) -> Optional[str]:
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    if BeautifulSoup:
        soup = BeautifulSoup(text, "html.parser")
        # Prefer explicit <source> inside <audio>
        for source in soup.find_all("source"):
            src = source.get("src")
            if src and (src.endswith(".wav") or src.endswith(".mp3")):
                return src.strip()
        audio = soup.find("audio")
        if audio and audio.get("src"):
            return audio.get("src").strip()
        return None

    # Fallback: regex for audio sources
    m = re.search(r"\\bsrc=[\"']([^\"']+\\.(?:wav|mp3))[\"']", text, re.IGNORECASE)
    return m.group(1).strip() if m else None


def slugify_title(title: str) -> str:
    t = title.lower()
    t = t.replace("&", "and")
    t = re.sub(r"[’']s\b", "", t)
    t = re.sub(r"[’']", "", t)
    t = re.sub(r"[^a-z0-9]+", "-", t)
    t = re.sub(r"-{2,}", "-", t).strip("-")
    return t


def slug_variants(title: str) -> set[str]:
    base = slugify_title(title)
    variants = {base}
    for article in ("the-", "a-", "an-"):
        if base.startswith(article):
            variants.add(base[len(article) :])
    return variants


def is_variant_filename(base: str) -> bool:
    return re.search(r"-v\\d+(\\b|$)", base) is not None


def build_html_index(base_dir: Path) -> Tuple[Dict[str, dict], Dict[str, dict], Dict[str, dict], List[dict]]:
    html_paths = list(base_dir.glob("*.html"))
    newsletters = base_dir / "newsletters"
    if newsletters.exists():
        html_paths += list(newsletters.glob("*.html"))

    def rank(rec: dict) -> tuple[int, int, float]:
        return (
            1 if rec["is_variant"] else 0,
            1 if rec["in_newsletters"] else 0,
            -rec["mtime"],
        )

    def choose_best(existing: Optional[dict], candidate: dict) -> dict:
        if existing is None:
            return candidate
        return candidate if rank(candidate) < rank(existing) else existing

    base_best: Dict[str, dict] = {}
    slug_best: Dict[str, dict] = {}
    audio_best: Dict[str, dict] = {}
    records: List[dict] = []

    for path in html_paths:
        title, blurb = extract_title_blurb(path)
        if not title:
            continue
        slug = slugify_title(title)
        audio_src = extract_audio_src(path)
        audio_stem = None
        if audio_src:
            audio_name = os.path.basename(audio_src)
            if audio_name.lower().endswith(".wav") or audio_name.lower().endswith(".mp3"):
                audio_stem = os.path.splitext(audio_name)[0]

        rec = {
            "path": path,
            "base": path.stem,
            "title": title,
            "blurb": blurb,
            "slug": slug,
            "image_src": extract_image_src(path),
            "audio_src": audio_src,
            "audio_stem": audio_stem,
            "in_newsletters": path.parent.name == "newsletters",
            "is_variant": is_variant_filename(path.stem),
            "mtime": path.stat().st_mtime,
        }
        records.append(rec)

        base_best[rec["base"]] = choose_best(base_best.get(rec["base"]), rec)
        for variant in slug_variants(title):
            slug_best[variant] = choose_best(slug_best.get(variant), rec)
        if audio_stem:
            audio_best[audio_stem] = choose_best(audio_best.get(audio_stem), rec)

    return base_best, slug_best, audio_best, records


def build_feed(cfg: dict, base_dir: Path) -> ET.Element:
    audio_dir = base_dir / cfg.get("audio_dir", "audio")
    wav_dir = base_dir / cfg.get("wav_dir", cfg.get("audio_dir", "audio"))
    audio_base_url = (cfg.get("audio_base_url") or "").strip()
    if not audio_base_url:
        raise SystemExit("Missing required config: audio_base_url")
    audio_base_url = audio_base_url.rstrip("/")

    mp3_files = sorted(audio_dir.glob("*.mp3"))
    if not mp3_files:
        raise SystemExit(f"No .mp3 files found in {audio_dir}")

    title_overrides = cfg.get("title_overrides", {})
    desc_overrides = cfg.get("description_overrides", {})
    desc_template = cfg.get("episode_description_template", "{title}")

    base_html, slug_html, audio_html, html_records = build_html_index(base_dir)

    site_base_url = (cfg.get("site_base_url") or "").strip().rstrip("/")
    channel_image_from = cfg.get("channel_image_from", "latest_episode")

    index_path = base_dir / "index.html"
    index_title = None
    index_desc = None
    if index_path.exists():
        index_title, index_desc = extract_title_blurb(index_path)

    def fuzzy_match(base_slug: str) -> Optional[dict]:
        if len(base_slug) < 6:
            return None
        best = None
        best_score = None
        for rec in html_records:
            slug = rec["slug"]
            if base_slug in slug:
                ratio = len(base_slug) / max(len(slug), 1)
            elif slug in base_slug:
                ratio = len(slug) / max(len(base_slug), 1)
            else:
                continue
            if ratio < 0.5:
                continue
            score = abs(len(slug) - len(base_slug))
            if best is None or score < best_score:
                best = rec
                best_score = score
        return best

    items = []
    # Only include audio files that are referenced by an HTML page.
    allowed_audio = set(audio_html.keys())

    for mp3 in mp3_files:
        base = mp3.stem
        if base not in allowed_audio:
            continue
        wav = wav_dir / f"{base}.wav"
        ts = get_birth_or_mtime(wav if wav.exists() else mp3)
        pub_date = rfc2822_from_ts(ts)

        base_slug = base
        html_rec = audio_html.get(base) or base_html.get(base) or slug_html.get(base_slug)
        if not html_rec:
            html_rec = fuzzy_match(base_slug)

        title = title_overrides.get(base)
        if not title and html_rec:
            title = html_rec.get("title")
        if not title:
            title = title_from_basename(base)

        description = desc_overrides.get(base)
        if not description and html_rec:
            description = html_rec.get("blurb")
        if not description:
            description = desc_template.format(title=title)

        item_link = None
        item_image = None
        if html_rec and site_base_url:
            rel = html_rec["path"].relative_to(base_dir).as_posix()
            item_link = absolutize_url(site_base_url, rel)
            if html_rec.get("image_src"):
                item_image = absolutize_url(site_base_url, html_rec["image_src"])

        duration = duration_from_wav(wav) if wav.exists() else None
        items.append(
            {
                "base": base,
                "mp3": mp3,
                "wav": wav if wav.exists() else None,
                "title": title,
                "description": description,
                "pub_date": pub_date,
                "timestamp": ts,
                "duration": duration,
                "item_link": item_link,
                "item_image": item_image,
            }
        )

    # Newest first
    items.sort(key=lambda x: x["timestamp"], reverse=True)

    rss = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(rss, "channel")

    channel_title = (cfg.get("title") or "").strip() or index_title or "Podcast"
    channel_desc = (cfg.get("description") or "").strip() or index_desc or "Podcast feed"
    channel_link = (cfg.get("link") or "").strip()
    if not channel_link and site_base_url:
        channel_link = site_base_url + "/"

    ET.SubElement(channel, "title").text = channel_title
    if channel_link:
        ET.SubElement(channel, "link").text = channel_link
    ET.SubElement(channel, "description").text = channel_desc
    if cfg.get("language"):
        ET.SubElement(channel, "language").text = cfg["language"]

    if cfg.get("feed_url"):
        atom_link = ET.SubElement(channel, f"{{{NS['atom']}}}link")
        atom_link.set("href", cfg["feed_url"])
        atom_link.set("rel", "self")
        atom_link.set("type", "application/rss+xml")

    if cfg.get("author"):
        ET.SubElement(channel, f"{{{NS['itunes']}}}author").text = cfg["author"]

    if cfg.get("owner_name") or cfg.get("owner_email"):
        owner = ET.SubElement(channel, f"{{{NS['itunes']}}}owner")
        if cfg.get("owner_name"):
            ET.SubElement(owner, f"{{{NS['itunes']}}}name").text = cfg["owner_name"]
        if cfg.get("owner_email"):
            ET.SubElement(owner, f"{{{NS['itunes']}}}email").text = cfg["owner_email"]

    channel_image_url = (cfg.get("image_url") or "").strip()
    if not channel_image_url and channel_image_from == "latest_episode" and site_base_url:
        for rec in sorted(html_records, key=lambda r: r["mtime"], reverse=True):
            src = rec.get("image_src")
            if src:
                channel_image_url = absolutize_url(site_base_url, src)
                break

    if channel_image_url:
        image = ET.SubElement(channel, "image")
        ET.SubElement(image, "url").text = channel_image_url
        ET.SubElement(image, "title").text = channel_title
        if channel_link:
            ET.SubElement(image, "link").text = channel_link

        itunes_image = ET.SubElement(channel, f"{{{NS['itunes']}}}image")
        itunes_image.set("href", channel_image_url)

    if cfg.get("category"):
        categories = cfg["category"]
        if isinstance(categories, str):
            categories = [categories]
        for cat in categories:
            cat_el = ET.SubElement(channel, f"{{{NS['itunes']}}}category")
            cat_el.set("text", cat)

    if cfg.get("explicit") is not None:
        ET.SubElement(channel, f"{{{NS['itunes']}}}explicit").text = str(cfg["explicit"])

    if items:
        ET.SubElement(channel, "lastBuildDate").text = items[0]["pub_date"]

    for item in items:
        it = ET.SubElement(channel, "item")
        ET.SubElement(it, "title").text = item["title"]
        ET.SubElement(it, "description").text = item["description"]
        ET.SubElement(it, "pubDate").text = item["pub_date"]
        if item.get("item_link"):
            ET.SubElement(it, "link").text = item["item_link"]

        audio_url = safe_join_url(audio_base_url, f"{item['base']}.mp3")
        guid = ET.SubElement(it, "guid")
        guid.set("isPermaLink", "true")
        guid.text = audio_url

        enclosure = ET.SubElement(it, "enclosure")
        enclosure.set("url", audio_url)
        enclosure.set("length", str(item["mp3"].stat().st_size))
        enclosure.set("type", "audio/mpeg")

        if item["duration"] is not None:
            ET.SubElement(it, f"{{{NS['itunes']}}}duration").text = format_duration(
                item["duration"]
            )

        if item.get("item_image"):
            it_img = ET.SubElement(it, f"{{{NS['itunes']}}}image")
            it_img.set("href", item["item_image"])

    return rss


def find_unreferenced_mp3(cfg: dict, base_dir: Path) -> list:
    audio_dir = base_dir / cfg.get("audio_dir", "audio")
    mp3_files = sorted(audio_dir.glob("*.mp3"))
    if not mp3_files:
        return []
    _, _, audio_html, _ = build_html_index(base_dir)
    allowed_audio = set(audio_html.keys())
    return [p.stem for p in mp3_files if p.stem not in allowed_audio]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Spotify-compatible podcast RSS feed."
    )
    parser.add_argument(
        "--config", default="podcast_feed.json", help="Path to feed config JSON"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output RSS file (overrides config output_path)",
    )
    parser.add_argument(
        "--report-missing",
        action="store_true",
        help="Report MP3 files that are not referenced by any HTML page",
    )
    parser.add_argument(
        "--report-missing-output",
        default=None,
        help="Write missing MP3 basenames to a file (one per line)",
    )
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    cfg = load_config(config_path)
    base_dir = config_path.parent

    output_path = args.output or cfg.get("output_path", "podcast.rss")
    output_path = (base_dir / output_path).resolve()

    rss = build_feed(cfg, base_dir)
    xml = ET.tostring(rss, encoding="utf-8", xml_declaration=True)
    output_path.write_bytes(xml)
    print(f"Wrote {output_path}")

    if args.report_missing or args.report_missing_output:
        missing = find_unreferenced_mp3(cfg, base_dir)
        print(f"Missing HTML references: {len(missing)}")
        for name in missing:
            print(name)
        if args.report_missing_output:
            out_path = Path(args.report_missing_output).resolve()
            out_path.write_text("\n".join(missing) + ("\n" if missing else ""), encoding="utf-8")
            print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()

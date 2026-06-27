"""Tests for scripts/generate_podcast_rss.py pure logic.

The headline case is STAB-1: the `is_variant_filename` regex used to contain
doubled backslashes inside a raw string (`r"-v\\d+(\\b|$)"`), so it never
matched a real `-vN` filename and the feed could pick a draft over the
canonical issue.
"""
import generate_podcast_rss as prss


# --- STAB-1: the regression that motivated the test suite -------------------

def test_is_variant_filename_matches_real_variant():
    assert prss.is_variant_filename("jlw-2026-01-30-v2") is True
    assert prss.is_variant_filename("jlw-2026-01-30-v13") is True


def test_is_variant_filename_rejects_non_variant():
    assert prss.is_variant_filename("jlw-2026-01-30") is False
    assert prss.is_variant_filename("jlw-2026-01-30-feynman") is False


# --- slug logic -------------------------------------------------------------

def test_slugify_basic():
    assert prss.slugify_title("Hello, World!") == "hello-world"


def test_slugify_ampersand_becomes_and():
    assert prss.slugify_title("A & B") == "a-and-b"


def test_slug_variants_strips_leading_article():
    variants = prss.slug_variants("The Big Thing")
    assert "the-big-thing" in variants
    assert "big-thing" in variants


# --- duration / url helpers -------------------------------------------------

def test_format_duration():
    assert prss.format_duration(3661) == "01:01:01"
    assert prss.format_duration(59) == "00:00:59"


def test_absolutize_url_passthrough_and_join():
    assert prss.absolutize_url("https://x.com", "https://y.com/a.png") == "https://y.com/a.png"
    assert prss.absolutize_url("https://x.com/", "/img.png") == "https://x.com/img.png"


def test_safe_join_url_inserts_single_slash():
    assert prss.safe_join_url("https://x.com", "a.mp3") == "https://x.com/a.mp3"
    assert prss.safe_join_url("https://x.com/", "a.mp3") == "https://x.com/a.mp3"

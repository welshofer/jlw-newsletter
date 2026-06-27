"""Tests for scripts/newsletter_lib.py (shared single-parse helpers)."""
import newsletter_lib as nl


# --- variant identity (FUNC-4 foundation) -----------------------------------

def test_is_variant_and_base():
    assert nl.is_variant("jlw-2026-01-30-v2.html") is True
    assert nl.is_variant("jlw-2026-01-30.html") is False
    assert nl.is_variant("jlw-2026-01-30-feynman.html") is False
    assert nl.newsletter_base("jlw-2026-01-30-v2.html") == "jlw-2026-01-30"
    assert nl.newsletter_base("jlw-2026-01-30-feynman-v3.html") == "jlw-2026-01-30-feynman"


# --- FUNC-4: dedupe prefers canonical, then newest --------------------------

def test_dedupe_prefers_non_variant():
    recs = [
        {"base": "x", "is_variant": False, "mtime": 100.0},
        {"base": "x", "is_variant": True, "mtime": 999.0},  # newer but a variant
    ]
    best = nl.dedupe_newsletters(recs)
    assert len(best) == 1
    assert best[0]["mtime"] == 100.0  # non-variant wins despite older mtime


def test_dedupe_among_variants_picks_newest():
    recs = [
        {"base": "y", "is_variant": True, "mtime": 100.0},
        {"base": "y", "is_variant": True, "mtime": 300.0},
    ]
    best = nl.dedupe_newsletters(recs)
    assert len(best) == 1
    assert best[0]["mtime"] == 300.0


# --- USE-4: word-boundary truncation ----------------------------------------

def test_smart_truncate_short_text_unchanged():
    assert nl.smart_truncate("hello world", 200) == "hello world"


def test_smart_truncate_breaks_on_word_boundary():
    text = "the quick brown fox jumps over the lazy dog " * 10
    out = nl.smart_truncate(text, 50)
    assert out.endswith("…")
    assert len(out) <= 51
    # never cut mid-word: the char before the ellipsis is a full word
    assert not out[:-1].endswith(" ")
    assert " " in out  # contains whole words


# --- absolutize -------------------------------------------------------------

def test_absolutize_relative_and_absolute():
    assert nl.absolutize("images/x.png") == f"{nl.SITE_URL}/images/x.png"
    assert nl.absolutize("https://cdn.example/x.png") == "https://cdn.example/x.png"
    assert nl.absolutize("") == ""

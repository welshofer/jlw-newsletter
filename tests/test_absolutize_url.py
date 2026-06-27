"""Regression tests for STAB-1: scripts/generate_podcast_rss.py absolutize_url.

The old implementation used ``path.lstrip("./")`` (a character-set strip, not a
prefix strip) and special-cased ``../`` incorrectly, so a ``./images/h.png``
reference resolved to a malformed ``https://site.com/./images/h.png``. These
tests pin the correct behaviour: ``./`` and ``../`` are resolved, while
already-absolute and protocol-relative URLs pass through.
"""
import generate_podcast_rss as prss


def test_dot_slash_relative_is_resolved():
    # The headline STAB-1 case: no malformed "/./" in the result.
    result = prss.absolutize_url("https://site.com", "./images/h.png")
    assert result == "https://site.com/images/h.png"
    assert "/./" not in result


def test_dot_dot_relative_is_resolved():
    # "../" segments are collapsed rather than left in the path.
    assert prss.absolutize_url("https://site.com", "../a/b.png") == "https://site.com/a/b.png"
    assert (
        prss.absolutize_url("https://site.com/blog/", "../a/b.png")
        == "https://site.com/a/b.png"
    )


def test_absolute_url_passes_through_unchanged():
    assert (
        prss.absolutize_url("https://site.com", "https://x/y.png") == "https://x/y.png"
    )
    assert (
        prss.absolutize_url("https://site.com", "http://x/y.png") == "http://x/y.png"
    )


def test_protocol_relative_url_gets_scheme():
    assert prss.absolutize_url("https://site.com", "//cdn/z.png") == "https://cdn/z.png"


def test_plain_relative_and_absolute_path_refs():
    assert (
        prss.absolutize_url("https://site.com", "images/h.png")
        == "https://site.com/images/h.png"
    )
    # Absolute-path reference is anchored at the host root.
    assert prss.absolutize_url("https://site.com/", "/img.png") == "https://site.com/img.png"

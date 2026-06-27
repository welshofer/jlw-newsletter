"""Shared styling and output-path helpers for the newsletter chart/image generators.

This module centralizes two things that used to be copy-pasted (and hardcoded)
across the ``generate_*.py`` scripts:

* The output base directory.  It now defaults to the historical production path
  but can be overridden with the ``JLW_OUTPUT_DIR`` environment variable.  When
  the variable is unset, ``output_path(...)`` returns byte-for-byte the same
  strings the scripts used to hardcode.
* The chart typography.  ``apply_brand_style()`` points matplotlib at the
  newsletter's brand fonts (Source Sans 3 for body, Fraunces for display)
  instead of the off-brand Helvetica Neue / SF Pro stacks the scripts used.
"""

import os

# ---------------------------------------------------------------------------
# Output directory
# ---------------------------------------------------------------------------
# Defaults to the exact historical production path so behavior is unchanged when
# JLW_OUTPUT_DIR is unset.  Set JLW_OUTPUT_DIR to redirect every generator's
# output somewhere else (CI, a worktree, a test sandbox, ...).
OUTPUT_BASE = os.environ.get("JLW_OUTPUT_DIR", "/Users/welshofer/clawd/jlw-newsletter")


def output_path(*parts):
    """Join ``parts`` onto the configured output base directory.

    ``output_path("images", "chart-x.png")`` returns
    ``"<OUTPUT_BASE>/images/chart-x.png"``.  With ``JLW_OUTPUT_DIR`` unset this
    is identical to the formerly hardcoded literals.
    """
    return os.path.join(OUTPUT_BASE, *parts)


# ---------------------------------------------------------------------------
# Brand palette (mirrors the site's CSS custom properties)
# ---------------------------------------------------------------------------
ACCENT = "#B85C38"   # --accent (terracotta)
BG = "#FDFBF7"       # --bg (cream)
TEXT = "#1A1815"     # --text (near-black)

# Brand typography.  Source Sans 3 is the site body font; Fraunces the display
# face.  Fallbacks keep charts legible on machines without the brand fonts.
BRAND_SANS = ["Source Sans 3", "Source Sans Pro", "Helvetica Neue", "Arial", "sans-serif"]
BRAND_SERIF = ["Fraunces", "Georgia", "serif"]


def apply_brand_style():
    """Point matplotlib rcParams at the newsletter brand fonts.

    Sets only the font-family rcParams so it can be called after a chart script
    has configured its own colors / sizes without clobbering them.
    """
    import matplotlib

    matplotlib.rcParams["font.family"] = "sans-serif"
    matplotlib.rcParams["font.sans-serif"] = BRAND_SANS
    matplotlib.rcParams["font.serif"] = BRAND_SERIF

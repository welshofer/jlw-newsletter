#!/usr/bin/env bash
# build.sh — Regenerate all derived newsletter content BEFORE deploying.
#
# Usage:
#   ./scripts/build.sh [CONTENT_DIR] [--deploy] [--optimize-images]
#
# CONTENT_DIR resolution (first match wins):
#   1. first non-flag positional argument
#   2. $DEPLOY_DIR environment variable
#   3. default: $HOME/clawd/jlw-newsletter
#
# Regenerates, against CONTENT_DIR:
#   - index.html   (+ sitemap.xml / robots.txt / favicon.svg)  via generate_index.py
#   - articles.rss                                              via generate_articles_rss.py   (FUNC-1 wiring)
#   - podcast.rss  (tolerant — skipped if audio/ or feed config absent) via generate_podcast_rss.py
#   - optional image optimization                               via optimize_images.py (--optimize-images)
#
# By default this does NOT deploy. Pass --deploy to chain to ./scripts/deploy.sh afterwards.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"

# --- Parse args -------------------------------------------------------------
DO_DEPLOY=0
DO_OPTIMIZE=0
CONTENT_DIR_ARG=""

for arg in "$@"; do
    case "$arg" in
        --deploy)          DO_DEPLOY=1 ;;
        --optimize-images) DO_OPTIMIZE=1 ;;
        -h|--help)
            grep '^#' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        --*)
            echo "ERROR: unknown flag: $arg" >&2
            exit 1
            ;;
        *)
            if [[ -z "$CONTENT_DIR_ARG" ]]; then
                CONTENT_DIR_ARG="$arg"
            else
                echo "ERROR: unexpected extra argument: $arg" >&2
                exit 1
            fi
            ;;
    esac
done

CONTENT_DIR="${CONTENT_DIR_ARG:-${DEPLOY_DIR:-$HOME/clawd/jlw-newsletter}}"

if [[ ! -d "$CONTENT_DIR" ]]; then
    echo "ERROR: Content directory not found: $CONTENT_DIR" >&2
    exit 1
fi

echo "🏗  Building derived content"
echo "   Content dir: $CONTENT_DIR"
echo "   Python:      $PYTHON"
echo ""

# --- 1. index.html (+ sitemap.xml / robots.txt / favicon.svg) ---------------
echo "▶ [1/4] generate_index.py — index.html + SEO files"
"$PYTHON" "$SCRIPT_DIR/generate_index.py" "$CONTENT_DIR"
echo ""

# --- 2. articles.rss (FUNC-1) -----------------------------------------------
echo "▶ [2/4] generate_articles_rss.py — articles.rss"
"$PYTHON" "$SCRIPT_DIR/generate_articles_rss.py" "$CONTENT_DIR"
echo ""

# --- 3. podcast.rss (tolerant / optional) -----------------------------------
echo "▶ [3/4] generate_podcast_rss.py — podcast.rss"
if [[ -f "$CONTENT_DIR/podcast_feed.json" ]]; then
    # Tolerant: a missing audio/ dir or zero mp3s makes the generator exit non-zero;
    # that should warn but never abort the whole build.
    if "$PYTHON" "$SCRIPT_DIR/generate_podcast_rss.py" --config "$CONTENT_DIR/podcast_feed.json"; then
        echo "   podcast.rss generated."
    else
        echo "   WARNING: podcast feed generation failed (no audio/ or no mp3s?) — skipping podcast.rss." >&2
    fi
else
    echo "   SKIP: no podcast_feed.json in $CONTENT_DIR — skipping podcast.rss."
fi
echo ""

# --- 4. optional image optimization -----------------------------------------
echo "▶ [4/4] optimize_images.py — image optimization (optional)"
if [[ "$DO_OPTIMIZE" -eq 1 ]]; then
    if [[ -d "$CONTENT_DIR/images" ]]; then
        "$PYTHON" "$SCRIPT_DIR/optimize_images.py" "$CONTENT_DIR/images"
    else
        echo "   SKIP: no images/ dir in $CONTENT_DIR."
    fi
else
    echo "   SKIP: pass --optimize-images to enable."
fi
echo ""

echo "✅ Build complete for: $CONTENT_DIR"

# --- Deploy (opt-in) --------------------------------------------------------
if [[ "$DO_DEPLOY" -eq 1 ]]; then
    echo ""
    echo "🚀 --deploy set — chaining to deploy.sh"
    exec "$SCRIPT_DIR/deploy.sh"
else
    echo ""
    echo "ℹ  Not deploying (no --deploy flag). To publish, run:"
    echo "     ./scripts/deploy.sh"
fi

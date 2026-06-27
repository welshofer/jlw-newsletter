#!/usr/bin/env bash
# build.sh — Regenerate all derived newsletter content BEFORE deploying.
#
# Usage:
#   ./scripts/build.sh [CONTENT_DIR] [--deploy] [--no-optimize]
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
#   - image optimization (ON by default)                        via optimize_images.py (--no-optimize to skip)
#
# By default this does NOT deploy. Pass --deploy to chain to ./scripts/deploy.sh afterwards.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"

# --- Parse args -------------------------------------------------------------
# PERF-1: image optimization runs BY DEFAULT. Pass --no-optimize to skip it.
DO_DEPLOY=0
DO_OPTIMIZE=1
CONTENT_DIR_ARG=""

for arg in "$@"; do
    case "$arg" in
        --deploy)          DO_DEPLOY=1 ;;
        --no-optimize)     DO_OPTIMIZE=0 ;;
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

# --- 4. image optimization (ON by default; PERF-1) --------------------------
echo "▶ [4/4] optimize_images.py — image optimization (default ON)"
if [[ "$DO_OPTIMIZE" -eq 1 ]]; then
    if [[ -d "$CONTENT_DIR/images" ]]; then
        "$PYTHON" "$SCRIPT_DIR/optimize_images.py" "$CONTENT_DIR/images"
    else
        echo "   SKIP: no images/ dir in $CONTENT_DIR."
    fi
else
    echo "   SKIP: --no-optimize passed — shipping images as-is."
fi
echo ""

echo "✅ Build complete for: $CONTENT_DIR"

# --- Deploy (opt-in) --------------------------------------------------------
# REL-3: deploy.sh now calls build.sh first to regenerate content. To avoid an
# infinite loop (build --deploy -> deploy -> build -> deploy ...), deploy.sh sets
# JLW_SKIP_DEPLOY_CHAIN=1 when it invokes us. In that case we must NOT chain back.
if [[ "$DO_DEPLOY" -eq 1 ]]; then
    if [[ -n "${JLW_SKIP_DEPLOY_CHAIN:-}" ]]; then
        echo ""
        echo "ℹ  --deploy ignored: invoked by deploy.sh (JLW_SKIP_DEPLOY_CHAIN set) — not chaining back."
    else
        echo ""
        echo "🚀 --deploy set — chaining to deploy.sh"
        # Tell deploy.sh the content is already freshly built so it does NOT
        # re-run build.sh (which would re-enter this script). Net effect: exactly
        # one regeneration per publish.
        export JLW_ALREADY_BUILT=1
        exec "$SCRIPT_DIR/deploy.sh"
    fi
else
    echo ""
    echo "ℹ  Not deploying (no --deploy flag). To publish, run:"
    echo "     ./scripts/deploy.sh"
fi

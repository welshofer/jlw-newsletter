#!/usr/bin/env bash
# deploy.sh — Deploy newsletter content to Cloudflare Pages
#
# Usage: ./scripts/deploy.sh
#
# Deploys ~/clawd/jlw-newsletter/ to Cloudflare Pages (production).
# Excludes WAVs, videos (served from R2), scripts, and dev files.
#
# IMPORTANT: --branch=main is required or it deploys to Preview, not Production.

set -euo pipefail

DEPLOY_SOURCE="$HOME/clawd/jlw-newsletter"

if [[ ! -d "$DEPLOY_SOURCE" ]]; then
    echo "ERROR: Deploy source not found: $DEPLOY_SOURCE" >&2
    exit 1
fi

# REL-4: refuse to deploy an empty/half-synced source that could wipe the live site.
if [[ ! -f "$DEPLOY_SOURCE/index.html" ]]; then
    echo "ERROR: Refusing to deploy — $DEPLOY_SOURCE/index.html is missing." >&2
    echo "       Run ./scripts/build.sh first to regenerate derived content." >&2
    exit 1
fi

echo "🚀 Deploying to Cloudflare Pages (production)"
echo "   Source: $DEPLOY_SOURCE"

# Get API token from Keychain
CF_TOKEN=$(security find-generic-password -s "cloudflare-pages-token" -a "welshofer" -w)

# Create temp deploy directory excluding large/dev files
DEPLOY_DIR=$(mktemp -d)
trap "rm -rf $DEPLOY_DIR" EXIT

rsync -a \
    --exclude='*.wav' \
    --exclude='.git' \
    --exclude='.venv' \
    --exclude='charts-venv' \
    --exclude='scripts' \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='*.py' \
    --exclude='*.pyc' \
    --exclude='newsletters' \
    --exclude='firebase-debug.log' \
    --exclude='video' \
    "$DEPLOY_SOURCE/" "$DEPLOY_DIR/"

SYNCED_FILES=$(find "$DEPLOY_DIR" -type f | wc -l | tr -d ' ')
echo "   Synced $SYNCED_FILES files to temp dir"

# REL-4: a healthy deploy has more than a handful of files. Abort if the synced
# temp dir looks empty/half-synced so we never push a near-empty site to prod.
MIN_FILES=5
if [[ ! -f "$DEPLOY_DIR/index.html" ]]; then
    echo "ERROR: Synced temp dir has no index.html — aborting deploy." >&2
    exit 1
fi
if (( SYNCED_FILES <= MIN_FILES )); then
    echo "ERROR: Only $SYNCED_FILES files synced (need > $MIN_FILES) — aborting deploy." >&2
    exit 1
fi

# Deploy — MUST use --branch=main for production
CLOUDFLARE_API_TOKEN="$CF_TOKEN" wrangler pages deploy "$DEPLOY_DIR" \
    --project-name=jlw-newsletter --branch=main --commit-dirty=true 2>&1

echo ""
echo "✅ Deployment complete!"
echo "   Site: https://jlw-newsletter.pages.dev/"

# REL-1: actually verify the live site responds 200, so a broken deploy fails loudly.
echo ""
echo "🔎 Verifying https://jlw-newsletter.pages.dev/ ..."
HTTP_STATUS=$(curl -sS -o /dev/null -w '%{http_code}' https://jlw-newsletter.pages.dev/ || echo "000")
echo "   HTTP status: $HTTP_STATUS"
if [[ "$HTTP_STATUS" != "200" ]]; then
    echo "ERROR: Live site returned $HTTP_STATUS (expected 200) — deploy verification failed." >&2
    exit 1
fi
echo "✅ Verified live site is healthy (200)."

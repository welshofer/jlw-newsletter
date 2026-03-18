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

echo "   Synced $(find "$DEPLOY_DIR" -type f | wc -l | tr -d ' ') files to temp dir"

# Deploy — MUST use --branch=main for production
CLOUDFLARE_API_TOKEN="$CF_TOKEN" wrangler pages deploy "$DEPLOY_DIR" \
    --project-name=jlw-newsletter --branch=main --commit-dirty=true 2>&1

echo ""
echo "✅ Deployment complete!"
echo "   Site: https://jlw-newsletter.pages.dev/"
echo ""
echo "   Verify: curl -sI https://jlw-newsletter.pages.dev/ | head -3"

#!/usr/bin/env bash
# upload_r2.sh — Upload files to Cloudflare R2 media bucket
#
# Usage: ./scripts/upload_r2.sh <relative-path> [content-type]
#
# Examples:
#   ./scripts/upload_r2.sh video/the-code-writes-itself.mp4
#   ./scripts/upload_r2.sh video/my-video.mp4 video/mp4
#
# The file is read from ~/clawd/jlw-newsletter/<relative-path>
# and uploaded to the jlw-newsletter-media R2 bucket at the same path.
#
# Public URL: https://pub-04f1a1ed27294b9d818e453c58db49ae.r2.dev/<relative-path>

set -euo pipefail

DEPLOY_DIR="$HOME/clawd/jlw-newsletter"
BUCKET="jlw-newsletter-media"
R2_PUBLIC="https://pub-04f1a1ed27294b9d818e453c58db49ae.r2.dev"

# --- Args ---
REL_PATH="${1:?Usage: upload_r2.sh <relative-path> [content-type]}"
LOCAL_FILE="$DEPLOY_DIR/$REL_PATH"

if [[ ! -f "$LOCAL_FILE" ]]; then
    echo "ERROR: File not found: $LOCAL_FILE" >&2
    exit 1
fi

# Auto-detect content type from extension
if [[ -n "${2:-}" ]]; then
    CONTENT_TYPE="$2"
else
    case "${REL_PATH##*.}" in
        mp4) CONTENT_TYPE="video/mp4" ;;
        webm) CONTENT_TYPE="video/webm" ;;
        mp3) CONTENT_TYPE="audio/mpeg" ;;
        wav) CONTENT_TYPE="audio/wav" ;;
        jpg|jpeg) CONTENT_TYPE="image/jpeg" ;;
        png) CONTENT_TYPE="image/png" ;;
        gif) CONTENT_TYPE="image/gif" ;;
        webp) CONTENT_TYPE="image/webp" ;;
        *) CONTENT_TYPE="application/octet-stream" ;;
    esac
fi

SIZE=$(du -h "$LOCAL_FILE" | cut -f1)
echo "⬆️  Uploading to R2"
echo "   File: $LOCAL_FILE ($SIZE)"
echo "   Bucket: $BUCKET/$REL_PATH"
echo "   Content-Type: $CONTENT_TYPE"

# Get Cloudflare token from Keychain
CF_TOKEN=$(security find-generic-password -s "cloudflare-pages-token" -a "welshofer" -w)

CLOUDFLARE_API_TOKEN="$CF_TOKEN" wrangler r2 object put \
    "$BUCKET/$REL_PATH" \
    --file "$LOCAL_FILE" \
    --content-type "$CONTENT_TYPE" \
    --remote 2>&1

echo ""
echo "🔍 Verifying upload..."
HTTP_STATUS=$(curl -sI "$R2_PUBLIC/$REL_PATH" | head -1 | awk '{print $2}')

if [[ "$HTTP_STATUS" == "200" ]]; then
    echo "✅ Upload verified — HTTP 200"
    echo "   URL: $R2_PUBLIC/$REL_PATH"
else
    echo "❌ Verification FAILED — HTTP $HTTP_STATUS" >&2
    echo "   Expected 200 from: $R2_PUBLIC/$REL_PATH" >&2
    echo "   Did you forget --remote? (This script includes it.)" >&2
    exit 1
fi

#!/usr/bin/env bash
# generate_video.sh — Generate cinematic video via NotebookLM + Veo 3
#
# Usage: ./scripts/generate_video.sh <newsletter.html> <slug> [prompt]
#
# Example:
#   ./scripts/generate_video.sh ~/clawd/jlw-newsletter/jlw-2026-03-18.html the-code-writes-itself
#   ./scripts/generate_video.sh ~/clawd/jlw-newsletter/jlw-2026-03-18.html the-code-writes-itself "Ken Burns style documentary..."
#
# Outputs:
#   ~/clawd/jlw-newsletter/video/<slug>.mp4
#
# Requires: notebooklm CLI (dev branch)

set -euo pipefail

NOTEBOOKLM="/Users/welshofer/Developer/notebooklm-py/.venv/bin/notebooklm"
DEPLOY_DIR="$HOME/clawd/jlw-newsletter"
POLL_INTERVAL=120  # seconds between status checks
MAX_WAIT=7200      # 2 hours max

# --- Args ---
HTML_FILE="${1:?Usage: generate_video.sh <newsletter.html> <slug> [prompt]}"
SLUG="${2:?Usage: generate_video.sh <newsletter.html> <slug> [prompt]}"
CUSTOM_PROMPT="${3:-}"

if [[ ! -f "$HTML_FILE" ]]; then
    echo "ERROR: File not found: $HTML_FILE" >&2
    exit 1
fi

# --- Extract title from HTML ---
TITLE=$(python3 -c "
import re, sys
with open('$HTML_FILE') as f:
    m = re.search(r'<h1[^>]*>(.*?)</h1>', f.read(), re.DOTALL)
    print(m.group(1).strip() if m else 'Newsletter')
")
echo "📽️  Generating cinematic video for: $TITLE"
echo "   Slug: $SLUG"

# --- Step 1: Extract text from HTML ---
echo "📄 Extracting text from HTML..."
TMPTEXT=$(mktemp /tmp/newsletter-text-XXXXX.md)
python3 -c "
from html.parser import HTMLParser
import re

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ('style', 'script'): self.skip = True
    def handle_endtag(self, tag):
        if tag in ('style', 'script'): self.skip = False
        if tag in ('p', 'h1', 'h2', 'h3', 'blockquote', 'div', 'article', 'section'): self.text.append('\n')
    def handle_data(self, data):
        if not self.skip: self.text.append(data)

with open('$HTML_FILE') as f:
    html = f.read()
extractor = TextExtractor()
extractor.feed(html)
text = re.sub(r'\n{3,}', '\n\n', ''.join(extractor.text)).strip()
with open('$TMPTEXT', 'w') as f:
    f.write('# $TITLE\n\n' + text)
print(f'   Extracted {len(text)} chars')
"

# --- Step 2: Create notebook ---
echo "📓 Creating NotebookLM notebook..."
NOTEBOOK_JSON=$($NOTEBOOKLM create "Newsletter: $TITLE" --json 2>&1)
NOTEBOOK_ID=$(echo "$NOTEBOOK_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['notebook_id'])")
echo "   Notebook ID: $NOTEBOOK_ID"

$NOTEBOOKLM use "$NOTEBOOK_ID" >/dev/null 2>&1

# --- Step 3: Add text source ---
echo "📎 Adding text source..."
SOURCE_JSON=$($NOTEBOOKLM source add "$TMPTEXT" --json 2>&1)
SOURCE_ID=$(echo "$SOURCE_JSON" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('source_id', d.get('id', '')))")
echo "   Source ID: $SOURCE_ID"
echo "   Waiting for source processing..."
$NOTEBOOKLM source wait "$SOURCE_ID" --timeout 120 2>&1 || true

# --- Step 4: Add images as sources ---
echo "📸 Adding image sources..."
for img in "$DEPLOY_DIR/images/hero-${SLUG}"*.{jpg,png} "$DEPLOY_DIR/images/article-01-"*.{jpg,png}; do
    if [[ -f "$img" ]]; then
        echo "   Adding: $(basename "$img")"
        $NOTEBOOKLM source add "$img" --json >/dev/null 2>&1 || true
    fi
done

# --- Step 5: Generate cinematic video ---
if [[ -z "$CUSTOM_PROMPT" ]]; then
    CUSTOM_PROMPT="A dramatic documentary exploring the themes of this newsletter. Ken Burns meets modern tech documentary — sweeping establishing shots, intimate close-ups of relevant scenes, tension between past and future. Tone: thoughtful, compelling, and visually rich."
fi

echo "🎬 Requesting cinematic video generation..."
GEN_JSON=$($NOTEBOOKLM generate cinematic-video "$CUSTOM_PROMPT" --language en --json 2>&1)
ARTIFACT_ID=$(echo "$GEN_JSON" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('artifact_id', d.get('id', d.get('task_id', ''))))")
echo "   Artifact ID: $ARTIFACT_ID"

# --- Step 6: Poll for completion ---
echo "⏳ Waiting for video generation (this can take 30-120 minutes)..."
ELAPSED=0
while [[ $ELAPSED -lt $MAX_WAIT ]]; do
    STATUS=$($NOTEBOOKLM artifact list --json 2>&1 | python3 -c "
import sys, json
data = json.load(sys.stdin)
for a in data.get('artifacts', []):
    if a['id'] == '$ARTIFACT_ID':
        print(a['status'])
        break
else:
    print('unknown')
" 2>/dev/null || echo "error")

    if [[ "$STATUS" == "completed" ]] || [[ "$STATUS" == "pending" ]]; then
        echo "   Status: $STATUS (after ${ELAPSED}s)"
        break
    elif [[ "$STATUS" == "failed" ]]; then
        echo "ERROR: Video generation failed after ${ELAPSED}s" >&2
        exit 1
    fi

    printf "   [%dm %ds] Status: %s\r" $((ELAPSED / 60)) $((ELAPSED % 60)) "$STATUS"
    sleep "$POLL_INTERVAL"
    ELAPSED=$((ELAPSED + POLL_INTERVAL))
done

if [[ $ELAPSED -ge $MAX_WAIT ]]; then
    echo "ERROR: Timed out after ${MAX_WAIT}s" >&2
    exit 1
fi

# --- Step 7: Download video ---
echo "⬇️  Downloading video..."
mkdir -p "$DEPLOY_DIR/video"
$NOTEBOOKLM download video "$DEPLOY_DIR/video/${SLUG}.mp4" \
    -a "$ARTIFACT_ID" -n "$NOTEBOOK_ID" 2>&1

if [[ ! -f "$DEPLOY_DIR/video/${SLUG}.mp4" ]]; then
    echo "ERROR: Download failed — file not found" >&2
    exit 1
fi

SIZE=$(du -h "$DEPLOY_DIR/video/${SLUG}.mp4" | cut -f1)
echo ""
echo "✅ Video generated successfully!"
echo "   File: $DEPLOY_DIR/video/${SLUG}.mp4"
echo "   Size: $SIZE"
echo ""
echo "Next steps:"
echo "  1. Upload to R2:  ./scripts/upload_r2.sh video/${SLUG}.mp4"
echo "  2. Verify:        curl -sI https://pub-04f1a1ed27294b9d818e453c58db49ae.r2.dev/video/${SLUG}.mp4"

# Cleanup
rm -f "$TMPTEXT"

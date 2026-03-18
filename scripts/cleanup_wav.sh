#!/bin/bash
# After verifying MP3 integrity, remove old WAV files (keeping last 5 as buffer)
set -euo pipefail

AUDIO_DIR="${1:-audio}"
KEEP_RECENT=5

# Get all WAV files sorted by modification time (newest first)
wavs=($(ls -1t "$AUDIO_DIR"/*.wav 2>/dev/null))
total=${#wavs[@]}

if [ "$total" -le "$KEEP_RECENT" ]; then
    echo "Only $total WAV files, keeping all (threshold: $KEEP_RECENT)"
    exit 0
fi

deleted=0
for wav in "${wavs[@]:$KEEP_RECENT}"; do
    mp3="${wav%.wav}.mp3"
    if [ -f "$mp3" ] && [ "$(stat -f%z "$mp3")" -gt 0 ]; then
        rm "$wav"
        ((deleted++))
    else
        echo "Skipping $wav (no valid MP3 transcode)"
    fi
done

echo "Deleted $deleted WAV files (kept $KEEP_RECENT most recent)"

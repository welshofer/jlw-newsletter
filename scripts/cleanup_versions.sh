#!/bin/bash
# Remove version variant files, keeping only the highest version for each base
set -euo pipefail

REPO="${1:-.}"
DRY_RUN="${2:---dry-run}"

cd "$REPO"

declare -A highest_version

# First pass: find highest version for each base
for f in jlw-*-v[0-9]*.html; do
    [ -f "$f" ] || continue
    base=$(echo "$f" | sed -E 's/-v[0-9]+\.html/.html/')
    version=$(echo "$f" | grep -oE 'v([0-9]+)' | grep -oE '[0-9]+')
    current=${highest_version[$base]:-0}
    if [ "$version" -gt "$current" ]; then
        highest_version[$base]=$version
    fi
done

# Second pass: delete everything except the highest version
deleted=0
for f in jlw-*-v[0-9]*.html; do
    [ -f "$f" ] || continue
    base=$(echo "$f" | sed -E 's/-v[0-9]+\.html/.html/')
    version=$(echo "$f" | grep -oE 'v([0-9]+)' | grep -oE '[0-9]+')
    highest=${highest_version[$base]:-0}
    if [ "$version" -lt "$highest" ]; then
        if [ "$DRY_RUN" = "--execute" ]; then
            git rm "$f"
            ((deleted++))
        else
            echo "Would delete: $f (keeping v$highest)"
            ((deleted++))
        fi
    fi
done

echo "$deleted files to clean up"
[ "$DRY_RUN" = "--execute" ] && echo "Deleted." || echo "Run with --execute to delete."

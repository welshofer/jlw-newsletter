#!/usr/bin/env python3
"""Optimize newsletter images: resize and compress for web delivery."""

import sys
from pathlib import Path
from PIL import Image


def optimize_image(path: Path, max_width: int = 1920, quality: int = 80) -> int:
    """Optimize a single image. Returns bytes saved."""
    original_size = path.stat().st_size

    with Image.open(path) as img:
        # Resize if wider than max
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)

        # Save optimized
        if path.suffix.lower() in (".jpg", ".jpeg"):
            img.save(path, "JPEG", quality=quality, optimize=True)
        elif path.suffix.lower() == ".png":
            img.save(path, "PNG", optimize=True)

    return original_size - path.stat().st_size


def optimize_directory(image_dir: Path) -> dict:
    """Optimize all images in a directory."""
    results = {"optimized": 0, "skipped": 0, "bytes_saved": 0}

    for img_path in image_dir.glob("*"):
        if img_path.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        if img_path.stat().st_size < 100_000:  # Skip < 100KB
            results["skipped"] += 1
            continue

        saved = optimize_image(img_path)
        results["optimized"] += 1
        results["bytes_saved"] += saved

    return results


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("images")
    results = optimize_directory(target)
    saved_mb = results["bytes_saved"] / (1024 * 1024)
    print(f"Optimized {results['optimized']} images, saved {saved_mb:.1f} MB")

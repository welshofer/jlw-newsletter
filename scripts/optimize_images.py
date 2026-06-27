#!/usr/bin/env python3
"""Optimize newsletter images: resize and compress for web delivery."""

import argparse
import os
import tempfile
from pathlib import Path

from PIL import Image

# Quality used for the generated .webp siblings (separate from the JPEG quality
# applied to the in-place re-encode of the original).
DEFAULT_WEBP_QUALITY = 82

# Sidecar marker suffix. After an image is optimized we drop a hidden marker
# next to it (e.g. "hero.jpg" -> ".hero.jpg.optimized"). Its mere existence is
# our idempotence guard: a robust, simple heuristic that does not depend on the
# post-optimization file size (lossy/poorly-compressible images can stay large)
# and that survives across runs. Re-running therefore never re-encodes an
# already-processed image, avoiding generational JPEG quality decay. Delete the
# marker to force re-optimization (e.g. after changing --max-width/--quality).
MARKER_SUFFIX = ".optimized"


def _marker_path(path: Path) -> Path:
    """Return the hidden sidecar marker path for an image."""
    return path.with_name("." + path.name + MARKER_SUFFIX)


def _atomic_save(img: Image.Image, dest: Path, image_format: str, **save_kwargs) -> None:
    """Save *img* to *dest* atomically.

    Writes to a temp file in the same directory, then os.replace()s it over the
    destination. os.replace is atomic on the same filesystem, so a crash mid-save
    can never leave a truncated/corrupt file at *dest* (it keeps the old bytes, or
    in the case of a brand-new sibling, simply does not appear).
    """
    fd, tmp_name = tempfile.mkstemp(dir=str(dest.parent), suffix=dest.suffix or ".tmp")
    tmp_path = Path(tmp_name)
    try:
        os.close(fd)
        img.save(tmp_path, image_format, **save_kwargs)
        # mkstemp creates the temp file 0600; preserve the destination's existing
        # mode (in-place overwrite) or fall back to umask-respecting web-readable
        # perms (new sibling), so optimization never silently restricts access.
        if dest.exists():
            os.chmod(tmp_path, dest.stat().st_mode)
        else:
            umask = os.umask(0)
            os.umask(umask)
            os.chmod(tmp_path, 0o666 & ~umask)
        os.replace(tmp_path, dest)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise


def optimize_image(
    path: Path,
    max_width: int = 1920,
    quality: int = 80,
    emit_webp: bool = True,
    webp_quality: int = DEFAULT_WEBP_QUALITY,
) -> dict:
    """Optimize a single image.

    Returns a dict: {"bytes_saved": int, "webp_bytes": int, "skipped": bool}.
    "bytes_saved" is the size reduction of the original; "webp_bytes" is the size
    of the generated .webp sibling (0 if none). "skipped" is True when the
    idempotence marker already exists and the image was left untouched.
    """
    # Idempotence guard: already optimized -> do nothing (no quality decay).
    marker = _marker_path(path)
    if marker.exists():
        return {"bytes_saved": 0, "webp_bytes": 0, "skipped": True}

    original_size = path.stat().st_size
    suffix = path.suffix.lower()
    webp_bytes = 0

    with Image.open(path) as img:
        # Resize if wider than max
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)

        # Save optimized (atomically, never in-place).
        if suffix in (".jpg", ".jpeg"):
            _atomic_save(img, path, "JPEG", quality=quality, optimize=True)
        elif suffix == ".png":
            _atomic_save(img, path, "PNG", optimize=True)

        # Emit a .webp sibling for the modern, smaller format served elsewhere.
        if emit_webp and suffix in (".jpg", ".jpeg", ".png"):
            webp_path = path.with_suffix(".webp")
            webp_img = img.convert("RGB") if suffix in (".jpg", ".jpeg") else img
            _atomic_save(webp_img, webp_path, "WEBP", quality=webp_quality, method=6)
            webp_bytes = webp_path.stat().st_size

    bytes_saved = original_size - path.stat().st_size

    # Drop the marker only after all writes succeeded, so a crash leaves the
    # image un-marked and the next run redoes the work cleanly.
    marker.touch()

    return {"bytes_saved": bytes_saved, "webp_bytes": webp_bytes, "skipped": False}


def optimize_directory(
    image_dir: Path,
    max_width: int = 1920,
    quality: int = 80,
    emit_webp: bool = True,
) -> dict:
    """Optimize all images in a directory."""
    results = {"optimized": 0, "skipped": 0, "bytes_saved": 0, "webp_bytes": 0}

    for img_path in image_dir.glob("*"):
        if img_path.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        if img_path.stat().st_size < 100_000:  # Skip < 100KB
            results["skipped"] += 1
            continue

        res = optimize_image(
            img_path,
            max_width=max_width,
            quality=quality,
            emit_webp=emit_webp,
        )
        if res["skipped"]:
            results["skipped"] += 1
        else:
            results["optimized"] += 1
            results["bytes_saved"] += res["bytes_saved"]
        results["webp_bytes"] += res["webp_bytes"]

    return results


def main(argv: list | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Resize and compress newsletter images for web delivery."
    )
    parser.add_argument(
        "image_dir",
        nargs="?",
        default="images",
        type=Path,
        help="Directory of images to optimize (default: images).",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=1920,
        help="Resize images wider than this many pixels (default: 1920).",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=80,
        help="JPEG quality for re-encoded originals (default: 80).",
    )
    parser.add_argument(
        "--no-webp",
        dest="emit_webp",
        action="store_false",
        help="Do not emit .webp siblings (emitted by default).",
    )
    args = parser.parse_args(argv)

    results = optimize_directory(
        args.image_dir,
        max_width=args.max_width,
        quality=args.quality,
        emit_webp=args.emit_webp,
    )
    saved_mb = results["bytes_saved"] / (1024 * 1024)
    print(f"Optimized {results['optimized']} images, saved {saved_mb:.1f} MB")
    if args.emit_webp:
        webp_mb = results["webp_bytes"] / (1024 * 1024)
        print(f"Generated {webp_mb:.1f} MB of .webp siblings")


if __name__ == "__main__":
    main()

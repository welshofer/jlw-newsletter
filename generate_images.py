# /// script
# dependencies = ["google-genai", "pillow"]
# ///
import os
import io
import sys
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image as PILImage
from chart_style import output_path

OUTPUT_DIR = Path(output_path("images"))


def safe_output_path(filename: str) -> Path:
    """Resolve ``filename`` inside OUTPUT_DIR, rejecting path traversal.

    A ``../..`` segment or an absolute path could otherwise escape OUTPUT_DIR and
    let a caller write anywhere on disk. We reject any filename that carries a
    directory component, then assert the resolved path stays directly under
    OUTPUT_DIR. Raises ``ValueError`` on anything suspicious.
    """
    name = Path(filename).name
    if filename != name or name in ("", ".", ".."):
        raise ValueError(
            f"invalid filename (no path separators allowed): {filename!r}"
        )
    resolved = (OUTPUT_DIR / name).resolve()
    if resolved.parent != OUTPUT_DIR.resolve():
        raise ValueError(f"filename escapes output directory: {filename!r}")
    return resolved


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    model = "gemini-3-pro-image-preview"
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        exit(1)

    # Get prompt and filename from args
    if len(sys.argv) < 3:
        print("Usage: python generate_images.py <filename> <prompt>")
        exit(1)

    filename = sys.argv[1]
    prompt = sys.argv[2]
    aspect = sys.argv[3] if len(sys.argv) > 3 else "16:9"

    # Validate the destination BEFORE any network call so a malicious filename is
    # rejected up front (and cannot escape OUTPUT_DIR via ../.. or an absolute path).
    try:
        out_file = safe_output_path(filename)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

    print(f"Generating: {filename}")
    print(f"Aspect: {aspect}")

    try:
        client = genai.Client(api_key=api_key)

        config = types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio=aspect,
                image_size="2K"
            )
        )

        response = client.models.generate_content(
            model=model,
            contents=[prompt],
            config=config
        )

        if not response.parts:
            print("Error: No image generated in response")
            exit(1)

    except Exception as e:
        print(f"Error during image generation: {e}")
        exit(1)

    for part in response.parts:
        if part.inline_data is not None:
            genai_image = part.as_image()
            pil_image = PILImage.open(io.BytesIO(genai_image.image_bytes))

            pil_image.save(out_file, "WEBP", quality=92)
            print(f"Saved: {out_file}")
            print(f"Size: {pil_image.size}")


if __name__ == "__main__":
    main()

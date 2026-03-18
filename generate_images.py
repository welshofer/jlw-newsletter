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

OUTPUT_DIR = Path("/Users/welshofer/clawd/jlw-newsletter/images")
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

        output_path = OUTPUT_DIR / filename
        pil_image.save(output_path, "WEBP", quality=92)
        print(f"Saved: {output_path}")
        print(f"Size: {pil_image.size}")

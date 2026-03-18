# /// script
# dependencies = ["google-genai", "pillow"]
# ///
import os
import io
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image as PILImage

OUTPUT_DIR = Path("/Users/welshofer/clawd/jlw-newsletter/images")
OUTPUT_DIR.mkdir(exist_ok=True)

model = "gemini-3-pro-image-preview"

api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY or GOOGLE_API_KEY environment variable not set")
    exit(1)

client = genai.Client(api_key=api_key)

prompt = """Editorial illustration of a prestigious university campus under pressure.

Composition: Grand neo-classical academic buildings with iconic clock tower at center, long dramatic shadows stretching across the quad. In the background, ominous storm clouds gather with subtle lightning.

Overlaid elements: Faint algorithmic circuitry patterns flowing through the sky like digital aurora, suggesting AI disruption. Bare outlines of official vehicles at the campus perimeter, creating subtle tension.

Color palette: Deep indigo (#3A2D5C) dominates the shadows and sky, contrasted with warm amber (#D4A84B) from setting sun catching the building facades and windows. Institutional gray stone buildings. The overall mood is sophisticated, contemplative, and slightly ominous yet beautiful.

Style: Modern editorial illustration for a prestigious news publication, clean vector-influenced aesthetic with painterly atmosphere, dramatic lighting. Think New Yorker or Atlantic cover quality. No people visible - focus on architecture and atmosphere conveying institutional anxiety."""

try:
    config = types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
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

    for part in response.parts:
        if part.inline_data is not None:
            genai_image = part.as_image()
            pil_image = PILImage.open(io.BytesIO(genai_image.image_bytes))

            output_path = OUTPUT_DIR / "hero-campus-under-pressure.png"
            pil_image.save(output_path, "PNG")
            print(f"Saved: {output_path}")
            print(f"Dimensions: {pil_image.size}")

except Exception as e:
    print(f"Error during image generation: {e}")
    exit(1)

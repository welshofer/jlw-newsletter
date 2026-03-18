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

prompt = """Editorial illustration capturing the conflict between universities and federal authority.

Composition: A grand university building with classical columns and a domed rotunda, positioned center frame. The building stands firm but is caught between opposing forces - on one side, warm amber (#D4A84B) light streaming through windows suggesting intellectual warmth and tradition; on the other side, cold shadows with subtle bureaucratic document shapes floating in the air like falling leaves.

Key visual elements:
- A prominent American flag casting a long, dramatic shadow across the building's facade
- Lists and documents fragmenting and swirling in the wind around the campus
- Deep indigo (#3A2D5C) twilight sky with storm clouds gathering
- Distant figures (small, silhouetted) on the quad, creating sense of scale and human stakes

Style: Sophisticated editorial illustration, New Yorker or Atlantic cover quality. Clean vector-influenced aesthetic with painterly atmosphere. The mood should be tense yet dignified - the institution standing its ground against pressure.

Color palette: Deep indigo (#3A2D5C) for shadows and sky, warm amber (#D4A84B) for interior light and hope, institutional gray and cream for architecture. Strong contrast between warm and cold tones representing the conflict.

No text, no people's faces visible. Focus on architecture, light, shadow, and floating paper elements conveying institutional tension."""

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

            output_path = OUTPUT_DIR / "hero-universities-vs-power.png"
            pil_image.save(output_path, "PNG")
            print(f"Saved: {output_path}")
            print(f"Dimensions: {pil_image.size}")

except Exception as e:
    print(f"Error during image generation: {e}")
    exit(1)

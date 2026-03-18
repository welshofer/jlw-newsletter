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

prompt = """Editorial illustration capturing the theme of institutional dismantling and adaptation in higher education.

Composition: A grand university building (classical columns, rotunda) viewed from a low angle, with sections of the facade dissolving or fragmenting into geometric shards. The fragments drift upward like embers or leaves in wind. Some fragments reform into new shapes—suggesting both destruction and transformation.

Key visual elements:
- Deep indigo (#3A2D5C) night sky with subtle circuitry patterns suggesting surveillance
- Warm amber (#D4A84B) light glowing from windows that remain intact—the human warmth persisting
- Laboratory flasks and test tubes visible through one window, symbolizing research under threat
- Document fragments floating in the air with redacted sections
- A single figure silhouette walking toward the building, small but determined

Style: Sophisticated editorial illustration, New Yorker or Atlantic cover quality. The mood should be ominous yet resilient—institutions under pressure but not defeated. Clean vector-influenced aesthetic with painterly atmosphere.

Color palette: Deep indigo (#3A2D5C) dominating the sky and shadows, warm amber (#D4A84B) for interior light and hope, institutional gray and cream for architecture, subtle red accents on warning signs or tape.

No text, no readable words. Focus on architecture, fragmentation, and the tension between dissolution and endurance."""

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

            output_path = OUTPUT_DIR / "hero-institutional-dismantling.png"
            pil_image.save(output_path, "PNG")
            print(f"Saved: {output_path}")
            print(f"Dimensions: {pil_image.size}")

except Exception as e:
    print(f"Error during image generation: {e}")
    exit(1)

# /// script
# dependencies = ["google-genai", "pillow"]
# ///
"""
Generate hero image for Chronicle newsletter - January 28, 2026
Theme: The academy under legal/political siege - courts, legislatures, federal orders
"""

import os
import asyncio
import chart_style
from datetime import datetime
from google import genai
from google.genai import types
from PIL import Image
import io

# Initialize Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

PROMPT = """
A courthouse and university building merged into a single composite structure, architectural 
elements blending impossibly. On the left, neoclassical columns and a domed rotunda evoke 
federal power; on the right, Gothic academic spires and ivy-covered walls represent the 
university. Between them, a massive gavel casts a long shadow across a campus quad where 
tiny figures of students walk. Storm clouds gather overhead but warm amber light (#D4A84B) 
breaks through in places, illuminating scattered papers floating on the wind - legal briefs, 
research grants, visa documents. Deep indigo (#3A2D5C) dominates the shadows. Editorial 
illustration style, New Yorker cover aesthetic, dramatic composition, no text.
"""

async def generate_image():
    print(f"Generating hero image at {datetime.now().strftime('%H:%M:%S')}...")
    
    response = await client.aio.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=PROMPT,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="16:9",
            output_mime_type="image/png"
        )
    )
    
    # Save the image
    output_dir = chart_style.output_path("images")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "hero-courts-and-campuses.png")
    
    image_data = response.generated_images[0].image.image_bytes
    img = Image.open(io.BytesIO(image_data))
    
    # Upscale to 2K resolution for hero
    target_width = 2752
    target_height = 1536  # 16:9
    img_resized = img.resize((target_width, target_height), Image.LANCZOS)
    img_resized.save(output_path, "PNG", optimize=True)
    
    print(f"✓ Saved: {output_path}")
    print(f"  Dimensions: {img_resized.size[0]}x{img_resized.size[1]}")
    return output_path

if __name__ == "__main__":
    asyncio.run(generate_image())

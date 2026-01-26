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
import time

OUTPUT_DIR = Path("/Users/welshofer/clawd/jlw-newsletter/images")
OUTPUT_DIR.mkdir(exist_ok=True)

model = "gemini-3-pro-image-preview"

api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY or GOOGLE_API_KEY environment variable not set")
    sys.exit(1)

client = genai.Client(api_key=api_key)

# Define all images to generate
IMAGES = [
    {
        "name": "hero-ubi-social-fabric",
        "aspect": "16:9",
        "prompt": """Editorial illustration for a Universal Basic Income newsletter.

Composition: Abstract visualization of interconnected human hands forming a safety net pattern,
with flowing currency symbols and coins gently falling into the net from above.
The hands are diverse in skin tone and create a geometric web pattern.

Background: Deep indigo (#5B4B8A) gradient transitioning to warm violet (#7C5C8A) at edges.
The safety net glows with subtle golden (#D4A84B) highlights where hands connect.

Overlaid elements: Faint algorithmic patterns suggesting economic calculations,
subtle circuit-like pathways connecting the hands, representing systematic support.

Style: Modern editorial illustration for a prestigious economics publication,
clean vector-influenced aesthetic with painterly atmosphere.
Think New Yorker or Atlantic cover quality. Focus on the concept of
community support and economic security through elegant abstraction."""
    },
    {
        "name": "article-01-agi-anxiety",
        "aspect": "4:3",
        "prompt": """Editorial illustration of tech workers in urgent conversation.

Composition: Silhouettes of programmers at computer terminals, their screens
glowing with neural network visualizations. Above them, digital circuitry
patterns morph into organic brain-like structures.

Color palette: Deep indigo (#5B4B8A) dominates, with electric cyan (#00D4FF)
accents on screens and neural patterns. Warm amber (#D4A84B) highlights
human silhouettes creating contrast.

Mood: Technological anxiety meets intellectual urgency. The sense that
a critical threshold is being crossed.

Style: Modern editorial illustration, clean lines, atmospheric lighting,
sophisticated minimalism suggesting Hacker News community aesthetic."""
    },
    {
        "name": "article-02-stimulus-rumors",
        "aspect": "4:3",
        "prompt": """Editorial illustration about government stimulus confusion.

Composition: Abstract representation of dollar bills transforming into
question marks, scattered across a field of social media bubbles.
In the background, a faint federal building silhouette casts long shadows.

Color palette: Confused, swirling indigo (#5B4B8A) and violet (#7C5C8A)
tones, with green ($) elements fading to gray question marks.
Sharp contrast between hope and disappointment.

Mood: The gap between public demand and political reality.
Information chaos meeting bureaucratic silence.

Style: Modern editorial illustration, conceptual, slightly satirical,
evocative of political magazine covers."""
    },
    {
        "name": "article-03-musk-abundance",
        "aspect": "4:3",
        "prompt": """Editorial illustration of post-scarcity vision.

Composition: A futuristic robotic arm extending from the left,
offering an overflowing horn of plenty filled with goods, technology,
and abstract representations of abundance. A visionary figure silhouette
looks toward a cosmic horizon.

Color palette: Deep indigo (#5B4B8A) transitioning to golden (#D4A84B)
and cosmic purple, suggesting transformation from scarcity to abundance.
Starfield backdrop with technological aurora.

Mood: Techno-optimism meeting economic revolution.
Visionary aspiration with a hint of skepticism in the shadows.

Style: Futuristic editorial illustration, science-fiction influenced,
epic scale, magazine cover quality."""
    },
    {
        "name": "article-04-california-calubi",
        "aspect": "4:3",
        "prompt": """Editorial illustration of California's AI displacement response.

Composition: Stylized California golden bear silhouette holding
a protective net, with factory robots and tech workers in background.
Regulatory documents flow like rivers from Sacramento to Silicon Valley.

Color palette: Warm California sunset amber (#D4A84B) meeting
indigo tech blue (#5B4B8A), golden state iconography with policy gravitas.

Overlaid elements: Faint circuit patterns suggesting automation,
government seal watermarks, hopeful human figures being caught by the net.

Mood: Policy response to technological disruption.
Government action meeting economic transformation.

Style: Political poster meets editorial illustration,
sophisticated, civic-minded, California aesthetics."""
    },
    {
        "name": "article-05-foster-youth",
        "aspect": "4:3",
        "prompt": """Editorial illustration of foster youth at life crossroads.

Composition: A young adult figure standing at a metaphorical fork in the road.
One path leads to shadowy isolation (empty apartment outline),
the other shows supportive hands extending monthly checks, leading to light.
New York City skyline visible in distant background.

Color palette: Violet storm clouds (#7C5C8A) breaking to reveal
warm hopeful light (#D4A84B) on the supported path.
Deep shadows (#5B4B8A) on the unsupported side.

Mood: Vulnerability meeting opportunity.
The critical moment when support changes trajectories.

Style: Emotional editorial photography meets illustration,
human-centered, evocative, magazine feature quality."""
    },
    {
        "name": "article-06-cook-county-permanent",
        "aspect": "4:3",
        "prompt": """Editorial illustration of historic policy transition.

Composition: Cook County government building with a ceremonial banner
unfurling, transforming from "PILOT" to "PERMANENT" in elegant typography.
Diverse Chicago neighborhood families in the foreground,
some holding envelopes representing guaranteed income checks.

Color palette: Civic indigo (#5B4B8A) for government elements,
warm community amber (#D4A84B) for human elements,
golden light suggesting historic achievement.

Mood: Civic celebration of policy milestone.
Temporary experiment becoming permanent institution.

Style: Documentary photography meets editorial illustration,
community-centered, historic, civic pride aesthetic."""
    }
]


def generate_image(image_config):
    """Generate a single image with the given configuration."""
    name = image_config["name"]
    aspect = image_config["aspect"]
    prompt = image_config["prompt"]

    print(f"\n{'='*60}")
    print(f"Generating: {name}")
    print(f"Aspect: {aspect}")
    print(f"{'='*60}")

    try:
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
            print(f"Error: No image generated for {name}")
            return False

        for part in response.parts:
            if part.inline_data is not None:
                genai_image = part.as_image()
                pil_image = PILImage.open(io.BytesIO(genai_image.image_bytes))

                output_path = OUTPUT_DIR / f"{name}.png"
                pil_image.save(output_path, "PNG")
                print(f"Saved: {output_path}")
                print(f"Dimensions: {pil_image.size}")
                return True

        print(f"Error: No inline data found for {name}")
        return False

    except Exception as e:
        print(f"Error generating {name}: {e}")
        return False


def main():
    # Check which image to generate from command line
    if len(sys.argv) > 1:
        target = sys.argv[1]
        images_to_generate = [img for img in IMAGES if img["name"] == target]
        if not images_to_generate:
            print(f"Unknown image: {target}")
            print(f"Available: {[img['name'] for img in IMAGES]}")
            sys.exit(1)
    else:
        images_to_generate = IMAGES

    success_count = 0
    for img_config in images_to_generate:
        if generate_image(img_config):
            success_count += 1
        # Rate limit protection
        if len(images_to_generate) > 1:
            print("Waiting 5 seconds before next image...")
            time.sleep(5)

    print(f"\n{'='*60}")
    print(f"Complete: {success_count}/{len(images_to_generate)} images generated")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

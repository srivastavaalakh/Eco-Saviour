from app.utils import init_gemini_model
from PIL import Image
from agents.gemini_agents.prompts import TRASH_ANALYSIS_PROMPT
import json
import re

# Initialize Gemini model
model = init_gemini_model()

def classify_waste_image(image: Image.Image) -> dict:
    """
    Analyze a photo of trash or household waste and classify items
    as recyclable or non-recyclable.

    Args:
        image (PIL.Image): Image containing trash or daily use items.

    Returns:
        dict: Each item with name, material, recyclability, and reasoning.
    """

    try:
        # Prompt + image
        response = model.generate_content(
            [TRASH_ANALYSIS_PROMPT, image],
            stream=False
        )

        # Strip Markdown formatting
        raw = response.text.strip()
        cleaned = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()

        # Attempt to parse cleaned JSON
        parsed = json.loads(cleaned)

        if "items" not in parsed:
            return {
                "error": "Parsed successfully, but missing 'items' key.",
                "raw_output": raw
            }

        return parsed

    except Exception as e:
        return {
            "error": "Failed to parse Gemini response.",
            "raw_output": getattr(response, "text", "No response"),
            "exception": str(e)
        }

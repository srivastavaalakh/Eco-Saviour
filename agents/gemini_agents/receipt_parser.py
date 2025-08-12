from app.utils import init_gemini_model
from PIL import Image
from agents.gemini_agents.prompts import RECEIPT_PARSING_PROMPT
import json
import re
model = init_gemini_model()

def parse_receipt_image(image: Image.Image) -> dict:
    """
    Analyze a receipt image and extract structured item data.

    Args:
        image (PIL.Image): Receipt image.

    Returns:
        dict: List of items with name, quantity, category, and packaging type.
    """

    try:
        response = model.generate_content([RECEIPT_PARSING_PROMPT, image], stream=False)
        cleaned = re.sub(r"^```(?:json)?|```$", "", response.text.strip(), flags=re.MULTILINE).strip()
        return json.loads(cleaned)
    except Exception as e:
        return {
            "error": "Failed to parse Gemini response.",
            "raw_output": getattr(response, "text", "No response"),
            "exception": str(e)
        }
